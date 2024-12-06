import logging
import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

import networkx as nx
import numpy as np
from joblib import Parallel, delayed
from scipy.stats import entropy

from nxlu.config import CommunityMethod
from nxlu.processing.analyze import GraphProperties, approximate_diameter
from nxlu.processing.embed import SentenceTransformerEmbedding
from nxlu.processing.preprocess import (
    CleanGraph,
    CleanGraphConfig,
    GraphRescalingConfig,
    RescalingMethod,
    SubgraphSelectionConfig,
    lcc,
)
from nxlu.utils.misc import cosine_similarity

logger = logging.getLogger("nxlu")


__all__ = [
    "CommunityResolution",
    "ConsensusResult",
    "MultiResolutionDetector",
    "CommunityPriors",
    "CommunityQueryMatcher",
    "get_communities",
    "LeidenAlgorithm",
    "leiden_communities",
]


@dataclass
class CommunityResolution:
    """Community detection results at a specific resolution."""

    resolution: float
    communities: list[set[str]]
    modularity: float
    method: CommunityMethod = CommunityMethod.LEIDEN


@dataclass
class ConsensusResult:
    """Consensus community detection results."""

    communities: list[set[str]]
    modularity: float
    methods: list[CommunityMethod]
    hierarchical_levels: list[list[set[str]]]


class CommunityPriors(GraphProperties):
    """A subclass of GraphProperties with attributes specific to community detection."""

    def __init__(
        self,
        graph: nx.Graph,
        compute_peak_degree: bool = True,
        identify_hits: bool = True,
        z_threshold: float = 2.0,
    ):
        if graph.number_of_nodes() == 0:
            raise ValueError("Graph must have at least one node")

        super().__init__(graph, compute_peak_degree, identify_hits, z_threshold)
        if isinstance(graph, (nx.MultiGraph, nx.MultiDiGraph)):
            logger.debug(
                "Converting multigraph to simple graph for clustering computation..."
            )
            # TODO: find a more robust way of handling weights in multi-graph community
            # detection
            if nx.is_weighted(graph):
                simple_graph = nx.Graph()
                for u, v, data in graph.edges(data=True):
                    if simple_graph.has_edge(u, v):
                        simple_graph[u][v]["weight"] += data.get("weight", 1.0)
                    else:
                        simple_graph.add_edge(u, v, weight=data.get("weight", 1.0))
            else:
                simple_graph = nx.Graph(graph)
        else:
            simple_graph = graph

        super().__init__(simple_graph, compute_peak_degree, identify_hits, z_threshold)

        self.degree_entropy = self._compute_degree_entropy()

        try:
            self.clustering_coefs = list(
                nx.clustering(simple_graph, weight="weight").values()
            )
            self.clustering_std = (
                np.std(self.clustering_coefs) if self.clustering_coefs else 0.0
            )
        except Exception:
            logger.warning("Error computing clustering coefficients")
            self.clustering_coefs = []
            self.clustering_std = 0.0

        self.hierarchy_depth = self._estimate_hierarchy_depth()

    def _compute_degree_entropy(self) -> float:
        """Compute the entropy of the degree distribution."""
        logger.debug("Computing degree entropy...")
        if self.degree_counts.sum() == 0:
            return 0.0
        degree_dist = self.degree_counts / self.degree_counts.sum()
        return float(entropy(degree_dist))

    def _estimate_hierarchy_depth(self) -> int:
        """Estimate the number of hierarchical levels in the graph."""
        logger.debug("Estimating hierarchy depth...")
        try:
            if self.is_connected:
                depth = approximate_diameter(self.graph) / 2
            else:
                # for disconnected graphs, use LCC
                subgraph = self.graph.subgraph(lcc(self.graph))
                depth = approximate_diameter(subgraph) / 2

            # refine using k-core
            k_cores = nx.core_number(self.graph)
            max_core = max(k_cores.values())
            depth = max(depth, math.log2(max_core + 1))

            # consider clustering coef diversity
            unique_coefs = len(set(self.clustering_coefs))
            depth = max(depth, math.log2(unique_coefs + 1))

            return max(1, int(round(depth)))
        except Exception:
            logger.warning("Error estimating hierarchy depth, using default value of 1")
            return 1

    def _get_size_adjustment(self) -> float:
        """Compute adjustment factor based on graph size."""
        logger.debug("Getting size adjustment...")
        size_factor = math.log10(self.num_nodes + self.num_edges + 1) / 10
        return min(1.0, size_factor)

    def _get_density_adjustment(self) -> float:
        """Compute adjustment factor based on graph density."""
        logger.debug("Getting density adjustment...")
        density = self.density
        if density < 0.01:  # very sparse
            return 0.5
        if density < 0.1:  # sparse
            return 0.3
        if density < 0.3:  # moderate
            return 0.2
        return 0.1  # dense

    def _get_entropy_adjustment(self) -> float:
        """Compute adjustment factor based on degree distribution entropy."""
        logger.debug("Getting entropy adjustment...")
        max_entropy = math.log2(self.num_nodes) if self.num_nodes > 1 else 1
        norm_entropy = self.degree_entropy / max_entropy
        return min(0.5, norm_entropy)

    def _get_clustering_adjustment(self) -> float:
        """Compute adjustment factor based on clustering coefficient variation."""
        logger.debug("Getting density adjustment...")
        return min(0.3, self.clustering_std)

    def _get_hierarchy_adjustment(self) -> float:
        """Compute adjustment factor based on estimated hierarchy depth."""
        logger.debug("Getting hierarchy adjustment...")
        return min(0.5, math.log2(self.hierarchy_depth + 1) / 4)

    def _generate_hierarchical_resolutions(
        self, min_res: float, max_res: float, n_steps: int
    ) -> np.ndarray:
        """Generate resolution values optimized for hierarchical structure."""
        logger.debug("Generating hierarchical resolutions...")
        exp_values = np.exp(np.linspace(np.log(min_res), np.log(max_res), n_steps))

        # add focus points around estimated hierarchical levels
        hierarchy_depth = self.hierarchy_depth
        level_points = np.exp(
            np.linspace(np.log(min_res), np.log(max_res), hierarchy_depth)
        )

        # combine and sort resolutions
        combined = np.unique(np.concatenate([exp_values, level_points]))
        combined.sort()

        # interpolate to get desired number of steps
        indices = np.linspace(0, len(combined) - 1, n_steps)
        resolutions = np.interp(indices, np.arange(len(combined)), combined)

        return resolutions

    def compute_dynamic_resolutions(
        self,
        min_resolution: float = 0.1,
        max_resolution: float = 1.5,
        min_steps: int = 1,
        max_steps: int = 5,
    ) -> tuple[int, np.ndarray]:
        """Compute optimal number of resolution steps and values based on graph
        properties.
        """
        base_steps = (
            int(math.log2(self.num_nodes + 1)) if self.num_nodes > 0 else min_steps
        )

        # adjust steps based on graph props
        step_adjustments = {
            "size": self._get_size_adjustment(),
            "density": self._get_density_adjustment(),
            "degree_entropy": self._get_entropy_adjustment(),
            "clustering": self._get_clustering_adjustment(),
            "hierarchy": self._get_hierarchy_adjustment(),
        }

        # calculate final num steps
        total_adjustment = sum(step_adjustments.values())
        n_steps = max(
            min_steps, min(int(base_steps * (1 + total_adjustment)), max_steps)
        )

        if self.hierarchy_depth > 1:
            # non-linear spacing for hierarchical graphs
            resolutions = self._generate_hierarchical_resolutions(
                min_resolution, max_resolution, n_steps
            )
        else:
            # linear spacing for flat graphs
            resolutions = np.linspace(min_resolution, max_resolution, n_steps)

        logger.info(
            f"Computed {n_steps} resolution steps based on:"
            f"\n - Graph size: {self.num_nodes} nodes, {self.num_edges} edges"
            f"\n - Density: {self.density:.3f}"
            f"\n - Degree entropy: {self.degree_entropy:.3f}"
            f"\n - Clustering std: {self.clustering_std:.3f}"
            f"\n - Hierarchy depth: {self.hierarchy_depth}"
        )

        return n_steps, resolutions


class CommunityQueryMatcher:
    """Match queries to detected graph communities using semantic similarity.

    This class performs multi-resolution community detection on a graph and
    identifies the most semantically similar communities to a given query.

    Parameters
    ----------
    embedding_model_name : str
        Name of the sentence transformer model to use for embeddings

    Attributes
    ----------
    model : SentenceTransformer
        Model for computing text embeddings
    consensus : ConsensusResult
        Consensus community detection result
    community_embeddings : Dict[Tuple[int, str], np.ndarray]
        Cached embeddings for each community
    """

    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformerEmbedding(model_name=embedding_model_name)
        self.consensus: ConsensusResult | None = None
        self.community_embeddings: dict[tuple[int, str], np.ndarray] = {}

    def fit(self, graph: nx.Graph) -> None:
        """Detect communities and compute their embeddings.

        Parameters
        ----------
        graph : nx.Graph
            Input graph to analyze
        """
        self.consensus = get_communities(graph)

        self.community_embeddings = {}

        for level_idx, level_communities in enumerate(
            self.consensus.hierarchical_levels
        ):
            for community_idx, community in enumerate(level_communities):
                desc = self._get_community_description(graph, community)

                embedding = self.model.get_text_embeddings([desc])[0]

                self.community_embeddings[(level_idx, f"community_{community_idx}")] = (
                    embedding
                )

    def _get_community_description(self, graph: nx.Graph, nodes: set[str]) -> str:
        """Generate a text description of a community from node attributes.

        Parameters
        ----------
        graph : nx.Graph
            The input graph
        nodes : Set[str]
            Set of node IDs in the community

        Returns
        -------
        str
            Text description of the community
        """
        descriptions = []
        for node in nodes:
            node_data = graph.nodes[node]
            desc_parts = []

            if "label" in node_data:
                desc_parts.append(str(node_data["label"]))
            if "description" in node_data:
                desc_parts.append(str(node_data["description"]))
            if "type" in node_data:
                desc_parts.append(f"Type: {node_data['type']}")

            if desc_parts:
                descriptions.append(" ".join(desc_parts))

        if descriptions:
            return " ".join(descriptions)
        return " ".join(nodes)  # fallback to node IDs

    def transform(
        self, query: str, n_communities: int = 10, min_similarity: float = 0.2
    ) -> list[tuple[tuple[int, str], float]]:
        """Find the most semantically similar communities to a query.

        Parameters
        ----------
        query : str
            Input query text
        n_communities : int
            Maximum number of communities to return
        min_similarity : float
            Minimum cosine similarity threshold

        Returns
        -------
        List[Tuple[Tuple[int, str], float]]
            List of (community_id, similarity_score) pairs, sorted by similarity
        """
        if not self.community_embeddings:
            raise ValueError("Must call fit() before finding similar communities")

        query_embedding = self.model.get_query_embedding(query)

        # compute similarities with all communities
        similarities = []
        for comm_id, comm_embedding in self.community_embeddings.items():
            sim = cosine_similarity(
                query_embedding.reshape(1, -1), comm_embedding.reshape(1, -1)
            )[0][0]
            if sim >= min_similarity:
                similarities.append((comm_id, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:n_communities]

    def get_community_nodes(self, community_id: tuple[int, str]) -> set[str]:
        """Get the nodes belonging to a community.

        Parameters
        ----------
        community_id : Tuple[int, str]
            The (level, community_id) identifier

        Returns
        -------
        Set[str]
            Set of node IDs in the community
        """
        if not self.consensus or not self.consensus.hierarchical_levels:
            raise ValueError("Must call fit() before getting community nodes")

        level_idx, comm_id = community_id
        community_idx = int(comm_id.split("_")[1])
        return self.consensus.hierarchical_levels[level_idx][community_idx]


class LeidenAlgorithm:
    def __init__(
        self,
        graph: nx.Graph,
        resolution: float = 1.0,
        randomness: float = 0.01,
        seed: int | None = None,
    ):
        """Initialize the Leiden algorithm for community detection."""
        if not isinstance(graph, nx.Graph) or graph.is_directed():
            raise ValueError("Graph must be an undirected NetworkX graph")

        if resolution <= 0:
            raise ValueError("resolution must be a positive float")

        self.graph = graph
        self.resolution = resolution
        self.randomness = randomness
        self.seed = seed

    @classmethod
    def find_communities(
        cls,
        graph: nx.Graph,
        max_cluster_size: int = 1000,
        n_runs: int = 4,
        n_jobs: int = -1,
        seed: int | None = None,
        resolution: float = 1.0,
        randomness: float = 0.01,
        use_modularity: bool = True,
        weight_attribute: str = "weight",
        is_weighted: bool | None = None,
        weight_default: int | float = 1.0,
        max_iterations: int = 100,
    ) -> dict[Any, int]:
        """Run hierarchical Leiden algorithm and select best result based on modularity.

        Parameters
        ----------
        graph : nx.Graph
            Input graph.
        max_cluster_size : int
            Maximum allowed size of a community. Larger communities will be split.
        n_runs : int
            Number of parallel algorithm runs.
        n_jobs : int
            Number of parallel jobs. -1 to use all processors.
        seed : Optional[int]
            Random seed for reproducibility.
        resolution : float
            Resolution parameter controlling community granularity.
        randomness : float
            Randomness parameter θ controlling the degree of randomness in the
            refinement phase.
        use_modularity : bool
            Whether to use modularity as the quality function.
        weight_attribute : str
            Edge data attribute corresponding to weights.
        is_weighted : Optional[bool]
            Whether the graph is weighted.
        weight_default : Union[int, float]
            Default weight for edges.
        max_iterations : int
            Maximum number of iterations to run until convergence.

        Returns
        -------
        Dict[Any, int]
            Node to community mapping with the highest modularity.
        """
        from graspologic_native import hierarchical_leiden

        if len(graph) == 0:
            return {}
        if len(graph) == 1:
            return {next(iter(graph.nodes())): 0}

        cls._validate_common_arguments(
            resolution=resolution,
            randomness=randomness,
            random_seed=seed,
        )
        if max_iterations < 1:
            raise ValueError("max_iterations must be a positive integer")

        connected_nodes = {n for n in graph.nodes() if graph.degree(n) > 0}
        isolated_nodes = set(graph.nodes()) - connected_nodes

        subgraph = graph.subgraph(connected_nodes).copy()

        (
            node_list,
            node_to_unique_str,
            unique_str_to_node,
            edges,
        ) = cls._convert_graph(subgraph, is_weighted, weight_attribute, weight_default)

        logger.debug(f"Connected Nodes: {len(node_list)}, Edges: {len(edges)}")
        logger.debug(f"Sample edges: {edges[:5]}")

        def run_single(run_id: int) -> tuple[dict[Any, int], float]:
            run_seed = (seed + run_id) if seed is not None else None

            prev_assignments = None
            for iteration in range(max_iterations):
                community_assignments = hierarchical_leiden(
                    edges=edges,
                    resolution=resolution,
                    randomness=randomness,
                    max_cluster_size=max_cluster_size,
                    use_modularity=use_modularity,
                    seed=run_seed,
                    iterations=1,
                )

                final_assignments = cls._process_assignments(
                    community_assignments, unique_str_to_node
                )

                logger.debug(
                    f"Run {run_id}, Iteration {iteration}: Number of communities = "
                    f"{len(set(final_assignments.values()))}"
                )

                if prev_assignments == final_assignments:
                    logger.debug(
                        f"Run {run_id}: Converged after {iteration} iterations"
                    )
                    break
                prev_assignments = final_assignments.copy()
            else:
                logger.warning(
                    f"Run {run_id}: Did not converge after {max_iterations} iterations"
                )

            communities = [
                set(nodes) for nodes in nx.utils.groups(final_assignments).values()
            ]

            try:
                modularity = nx.community.modularity(
                    subgraph, communities, weight=weight_attribute
                )
            except Exception:
                logger.warning(f"Failed to compute modularity for run {run_id}")
                modularity = -1.0

            return final_assignments, modularity

        results = Parallel(n_jobs=n_jobs, backend="threading")(
            delayed(run_single)(i) for i in range(n_runs)
        )

        best_communities, best_modularity = max(results, key=lambda x: x[1])

        # assign unique community IDs to isolated nodes, e.g., -1
        for node in isolated_nodes:
            best_communities[node] = -1

        total_communities = len(set(best_communities.values()))
        logger.debug(f"Total Communities (including isolates): {total_communities}")

        logger.debug(f"Return type of find_communities: {type(best_communities)}")
        return best_communities

    @staticmethod
    def _process_assignments(community_assignments, unique_str_to_node):
        from graspologic_native import HierarchicalCluster

        final_assignments = {}

        if isinstance(community_assignments, int):
            for node in unique_str_to_node.values():
                final_assignments[node] = 0
        elif isinstance(community_assignments, list):
            for comm_id, cluster in enumerate(community_assignments):
                if isinstance(cluster, list):
                    for node_str in cluster:
                        if node_str in unique_str_to_node:
                            final_assignments[unique_str_to_node[node_str]] = comm_id
                elif isinstance(cluster, HierarchicalCluster):
                    node_str = cluster.node
                    try:
                        comm_id = int(cluster.cluster)
                    except ValueError:
                        logger.warning(
                            f"Cluster ID '{cluster.cluster}' for node '{node_str}' is "
                            f"not an integer."
                        )
                    if node_str in unique_str_to_node:
                        final_assignments[unique_str_to_node[node_str]] = comm_id
                elif hasattr(cluster, "membership"):
                    for node_str, community_id in cluster.membership.items():
                        if node_str in unique_str_to_node:
                            final_assignments[unique_str_to_node[node_str]] = (
                                community_id
                            )
                else:
                    node_str = str(cluster)
                    if node_str in unique_str_to_node:
                        final_assignments[unique_str_to_node[node_str]] = comm_id
        else:
            logger.warning("Unknown structure for community_assignments")
            for node in unique_str_to_node.values():
                final_assignments[node] = 0

        for node in unique_str_to_node.values():
            if node not in final_assignments:
                final_assignments[node] = len(final_assignments)

        return final_assignments

    @staticmethod
    def _convert_graph(
        graph: nx.Graph,
        is_weighted: bool | None,
        weight_attribute: str,
        weight_default: float,
    ) -> tuple[
        list[Any],
        dict[Any, str],
        dict[str, Any],
        list[tuple[str, str, float]],
    ]:
        """Convert NetworkX graph to edge list format compatible with graspologic.

        Parameters
        ----------
        graph : nx.Graph
            Input NetworkX graph.
        is_weighted : Optional[bool]
            Whether the graph is weighted.
        weight_attribute : str
            Edge data attribute for weights.
        weight_default : float
            Default weight for edges.

        Returns
        -------
        Tuple[
            List[Any],
            Dict[Any, str],
            Dict[str, Any],
            List[Tuple[str, str, float]],
        ]
            - List of nodes.
            - Mapping from original node to unique string identifier.
            - Mapping from unique string identifier back to original node.
            - List of weighted edges as tuples of (source_str, target_str, weight).
        """
        node_list = list(graph.nodes())
        node_to_unique_str = {node: f"node_{idx}" for idx, node in enumerate(node_list)}
        unique_str_to_node = {f"node_{idx}": node for idx, node in enumerate(node_list)}
        edges = []

        for source, target, data in graph.edges(data=True):
            if is_weighted is None or is_weighted:
                weight = float(data.get(weight_attribute, weight_default))
            else:
                weight = float(weight_default)
            source_str = node_to_unique_str[source]
            target_str = node_to_unique_str[target]
            edges.append((source_str, target_str, weight))

        return node_list, node_to_unique_str, unique_str_to_node, edges

    @staticmethod
    def _validate_common_arguments(
        resolution: float,
        randomness: float,
        random_seed: int | None,
    ) -> None:
        """Validate common arguments.

        Parameters
        ----------
        resolution : float
            Resolution parameter.
        randomness : float
            Randomness parameter θ.
        random_seed : Optional[int]
            Random seed.

        Raises
        ------
        ValueError
            If any argument is invalid.
        """
        if resolution <= 0:
            raise ValueError("resolution must be a positive float")
        if randomness <= 0:
            raise ValueError("randomness must be a positive float")
        if random_seed is not None and random_seed < 0:
            raise ValueError(
                "random_seed must be a non-negative integer (the native PRNG "
                "implementation is an unsigned 64 bit integer)"
            )


def leiden_communities(
    graph: nx.Graph,
    resolution: float = 1.0,
    randomness: float = 0.1,
    max_iterations: int = 100,
    n_runs: int = 4,
    n_jobs: int = -1,
    max_cluster_size: int = 1000,
    seed: int | None = 42,
    use_modularity: bool = True,
    weight_attribute: str = "weight",
    is_weighted: bool | None = None,
    weight_default: int | float = 1.0,
) -> dict[Any, int]:
    """Detect hierarchical Leiden communities.

    Parameters
    ----------
    graph : nx.Graph
        Input graph.
    resolution : float
        Resolution parameter controlling community granularity.
    randomness : float
        Randomness parameter θ controlling the degree of randomness.
    max_iterations : int
        Maximum number of iterations to run until convergence.
    n_runs : int
        Number of parallel algorithm runs.
    n_jobs : int
        Number of parallel jobs. -1 to use all processors.
    max_cluster_size : int
        Maximum allowed size of a community. Larger communities will be split.
    seed : Optional[int]
        Random seed for reproducibility.
    use_modularity : bool
        Whether to use modularity as the quality function.
    weight_attribute : str
        Edge data attribute for weights.
    is_weighted : Optional[bool]
        Whether the graph is weighted.
    weight_default : Union[int, float]
        Default weight for edges.

    Returns
    -------
    Dict[Any, int]
        Node to community mapping with the highest modularity.
    """
    return LeidenAlgorithm.find_communities(
        graph=graph,
        max_cluster_size=max_cluster_size,
        n_runs=n_runs,
        n_jobs=n_jobs,
        seed=seed,
        resolution=resolution,
        randomness=randomness,
        use_modularity=use_modularity,
        weight_attribute=weight_attribute,
        is_weighted=is_weighted,
        weight_default=weight_default,
        max_iterations=max_iterations,
    )


class MultiResolutionDetector:
    """Multi-resolution community detection using NetworkX's native algorithms.

    This class combines multiple NetworkX community detection approaches:
    - Louvain for resolution-parameterized modularity optimization
    - Girvan-Newman for hierarchical community structure
    - Label propagation for fast detection at different scales
    - Greedy modularity maximization as a baseline
    - Fluid communities for variable-size community detection
    - Leiden communities for fast, connected, hierarchical-assignment using a "local
    moving" approach

    The consensus approach combines results across methods and resolutions
    to find stable community structures.

    Parameters
    ----------
    graph : nx.Graph
        Input graph for community detection
    min_resolution : float, optional
        Minimum resolution parameter for modularity-based methods, by default 0.1
    max_resolution : float, optional
        Maximum resolution parameter for modularity-based methods, by default 2.0
    n_resolutions : int, optional
        Number of resolution steps to use, by default 10
    methods : List[CommunityMethod], optional
        Community detection methods to use, by default only the leiden method
    random_state : Optional[int], optional
        Random seed for reproducibility, by default None

    Attributes
    ----------
    resolutions : List[CommunityResolution]
        Results from each method/resolution combination
    consensus : Optional[ConsensusResult]
        Consensus clustering results if computed
    """

    def __init__(
        self,
        graph: nx.Graph,
        min_resolution: float = 0.1,
        max_resolution: float = 1.5,
        n_resolutions: int = 5,
        methods: list[CommunityMethod] | None = None,
        random_state: int | None = None,
    ):
        self.graph = graph.copy()
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.n_resolutions = n_resolutions
        self.methods = methods or list(CommunityMethod)
        self.random_state = random_state

        self.resolutions: list[CommunityResolution] = []
        self.consensus: ConsensusResult | None = None

        self.rng = np.random.RandomState(random_state)
        self.best_result: CommunityResolution | None = None

    def detect_communities(self, min_size: int = 5) -> ConsensusResult:
        """Perform multi-resolution community detection and return best partition."""
        logger.info("Starting multi-resolution community detection")

        resolutions = np.linspace(
            self.min_resolution, self.max_resolution, self.n_resolutions
        )

        best_modularity = -1.0
        best_communities = []
        best_resolution = None

        graph = self._preprocess_graph(self.graph, CommunityMethod.LEIDEN)

        def merge_small_communities(
            comm2nodes: dict[Any, set[str]], graph: nx.Graph
        ) -> dict[Any, set[str]]:
            """Merge communities smaller than min_size into their most connected
            neighboring communities.
            """
            small_communities = {
                comm_id: nodes
                for comm_id, nodes in comm2nodes.items()
                if len(nodes) < min_size
            }
            for comm_id, nodes in small_communities.items():
                if comm_id not in comm2nodes:
                    continue
                connections = defaultdict(int)
                for node in nodes:
                    for neighbor in graph.neighbors(node):
                        for other_id, other_comm in comm2nodes.items():
                            if other_id != comm_id and neighbor in other_comm:
                                connections[other_id] += 1
                if connections:
                    best_neighbor = max(connections.items(), key=lambda x: x[1])[0]
                    comm2nodes[best_neighbor].update(nodes)
                    del comm2nodes[comm_id]
            return comm2nodes

        def process_communities(
            communities: dict[Any, int], graph: nx.Graph, resolution: float
        ) -> tuple[list[set[str]], float]:
            """Convert community assignments to sets, merge small communities, and
            compute modularity.
            """
            comm2nodes = defaultdict(set)
            for node, comm_id in communities.items():
                comm2nodes[comm_id].add(str(node))

            comm2nodes = merge_small_communities(comm2nodes, graph)
            filtered_communities = list(comm2nodes.values())

            try:
                modularity = nx.community.modularity(
                    graph, filtered_communities, weight="weight", resolution=resolution
                )
                logger.debug(f"Modularity={modularity}")
            except Exception:
                logger.warning(
                    f"Failed to compute modularity at resolution {resolution}"
                )
                modularity = -1.0

            return filtered_communities, modularity

        # First pass: find best resolution with quick runs
        for resolution in resolutions:
            logger.debug(f"Resolution: {resolution}...")
            communities = leiden_communities(
                graph=graph,
                resolution=resolution,
                randomness=0.1,
                max_iterations=10,  # Quick run for scanning
                seed=self.random_state,
            )

            filtered_communities, modularity = process_communities(
                communities, graph, resolution
            )

            if modularity > best_modularity:
                best_modularity = modularity
                best_communities = filtered_communities
                best_resolution = resolution
                self.best_result = CommunityResolution(
                    resolution=resolution,
                    communities=filtered_communities,
                    modularity=modularity,
                    method=CommunityMethod.LEIDEN,
                )

        if not best_resolution:
            raise ValueError(
                "No valid communities found after merging small communities"
            )

        # Second pass: thorough run at best resolution
        logger.info(f"Running thorough partition at best resolution {best_resolution}")
        final_communities = leiden_communities(
            graph=graph,
            resolution=best_resolution,
            randomness=0.05,  # Lower randomness for final run
            max_iterations=100,  # More iterations for convergence
            seed=self.random_state,
        )

        final_filtered_communities, final_modularity = process_communities(
            final_communities, graph, best_resolution
        )

        if final_modularity > best_modularity:
            best_modularity = final_modularity
            best_communities = final_filtered_communities
            self.best_result = CommunityResolution(
                resolution=best_resolution,
                communities=final_filtered_communities,
                modularity=final_modularity,
                method=CommunityMethod.LEIDEN,
            )
            logger.info(f"Final partition has improved modularity {best_modularity}")
        else:
            logger.info(
                f"Final partition did not improve modularity. Using best modularity "
                f"{best_modularity}"
            )

        hierarchical_levels = self._generate_hierarchy(best_communities)

        return ConsensusResult(
            communities=best_communities,
            modularity=best_modularity,
            methods=[CommunityMethod.LEIDEN],
            hierarchical_levels=hierarchical_levels,
        )

    @staticmethod
    def _preprocess_graph(graph: nx.Graph, method: CommunityMethod) -> nx.Graph:
        """Preprocess graph conditionally according to community method being applied
        Note that this will not change the original graph -- we use it only for the
        sake of learning a set of partitions
        """
        preprocessing_config = CleanGraphConfig(
            force_symmetry=True,
            remove_self_loops=False,
            threshold=None,
            rescale=GraphRescalingConfig(method=RescalingMethod.normalize),
            subgraph=(
                SubgraphSelectionConfig(defragment=False, use_lcc=True)
                if method in (CommunityMethod.GIRVAN_NEWMAN, CommunityMethod.FLUID)
                else None
            ),
        )
        cleaner = CleanGraph(graph.copy(), preprocessing_config)
        return cleaner.clean()

    def _generate_hierarchy(
        self, base_communities: list[set[str]]
    ) -> list[list[set[str]]]:
        """Generate hierarchical community levels from base partition."""
        hierarchy = [base_communities]
        max_depth = 3

        for community in base_communities:
            if len(community) <= 3:
                continue

            subgraph = self.graph.subgraph(community).copy()
            try:
                self._recursive_greedy_modularity(
                    subgraph, current_level=1, max_depth=max_depth, hierarchy=hierarchy
                )
            except Exception:
                logger.warning(
                    f"Failed to generate hierarchy for community {community}"
                )
                continue

        return hierarchy

    def _recursive_greedy_modularity(
        self,
        subgraph: nx.Graph,
        current_level: int,
        max_depth: int,
        hierarchy: list[list[set[str]]],
    ) -> None:
        """Recursively apply greedy modularity to generate hierarchical communities."""
        if current_level > max_depth:
            return

        communities = list(
            nx.community.greedy_modularity_communities(subgraph, weight="weight")
        )
        if len(communities) <= 1:
            return

        hierarchy.append(
            [{str(node) for node in community} for community in communities]
        )

        for community in communities:
            if len(community) <= 3:
                continue
            community_subgraph = subgraph.subgraph(community).copy()
            self._recursive_greedy_modularity(
                community_subgraph, current_level + 1, max_depth, hierarchy
            )

    def _apply_preprocess(self, graph: nx.Graph, method: CommunityMethod) -> nx.Graph:
        """Apply preprocessing conditionally based on community method being applied"""
        if method == CommunityMethod.LOUVAIN:
            return self._preprocess_graph(graph, CommunityMethod.LOUVAIN)

        if method == CommunityMethod.LEIDEN:
            return self._preprocess_graph(graph, CommunityMethod.LEIDEN)

        if method == CommunityMethod.GIRVAN_NEWMAN:
            return self._preprocess_graph(graph, CommunityMethod.GIRVAN_NEWMAN)

        if method == CommunityMethod.LABEL_PROPAGATION:
            return self._preprocess_graph(graph, CommunityMethod.LABEL_PROPAGATION)

        if method == CommunityMethod.GREEDY_MODULARITY:
            return self._preprocess_graph(graph, CommunityMethod.GREEDY_MODULARITY)

        if method == CommunityMethod.FLUID:
            return self._preprocess_graph(graph, CommunityMethod.FLUID)

        return self._raise_unsupported_method_error(method)

    def _detect_with_method(
        self, graph: nx.Graph, method: CommunityMethod, resolution: int
    ) -> list[set[str]]:
        """Detect communities using specified method and resolution.

        Parameters
        ----------
        graph : nx.Graph
            Preprocessed input graph for community detection
        method : CommunityMethod
            Community detection method to use
        resolution : int
            Resolution parameter value

        Returns
        -------
        List[Set[str]]
            Detected communities as lists of node sets
        """
        try:
            if method == CommunityMethod.LOUVAIN:
                communities = nx.community.louvain_communities(
                    graph,
                    resolution=resolution,
                    seed=self.random_state,
                )
            elif method == CommunityMethod.LEIDEN:
                node2comm = leiden_communities(
                    graph,
                    resolution=resolution,
                    randomness=0.1,
                    max_iterations=10,
                    seed=self.random_state,
                )
                logger.debug(f"leiden_communities returned type: {type(node2comm)}")
                logger.debug(
                    f"leiden_communities sample: {list(node2comm.items())[:5]}"
                )
                comm2nodes = defaultdict(set)
                for node, comm_id in node2comm.items():
                    comm2nodes[comm_id].add(node)
                communities = list(comm2nodes.values())
            elif method == CommunityMethod.GIRVAN_NEWMAN:
                # use n_communities proportional to resolution
                n_communities = max(2, int(self.graph.number_of_nodes() * resolution))
                gn_communities = nx.community.girvan_newman(graph)
                for _ in range(n_communities - 1):
                    communities = next(gn_communities)

            elif method == CommunityMethod.LABEL_PROPAGATION:
                communities = nx.community.label_propagation_communities(graph)

            elif method == CommunityMethod.GREEDY_MODULARITY:
                communities = nx.community.greedy_modularity_communities(
                    graph,
                    resolution=resolution,
                )

            elif method == CommunityMethod.FLUID:
                k = max(2, int(self.graph.number_of_nodes() * resolution))
                communities = nx.community.asyn_fluidc(
                    graph,
                    k,
                    seed=self.random_state,
                )
            else:
                self._raise_unsupported_method_error(method)

            communities = [{str(n) for n in c} for c in communities]

        except Exception:
            logger.warning(
                f"Failed to detect communities with method {method} at resolution "
                f"{resolution}"
            )
            return []
        else:
            return communities

    @staticmethod
    def _raise_unsupported_method_error(method: CommunityMethod):
        raise ValueError(f"Unsupported community detection method: {method}")


def get_communities(
    graph: nx.Graph,
    methods: list[CommunityMethod] | None = None,
    seed: int = 42,
) -> ConsensusResult:
    if methods is None:
        methods = [CommunityMethod.LEIDEN]
    community_props = CommunityPriors(graph)
    n_steps, resolutions = community_props.compute_dynamic_resolutions()
    community_detector = MultiResolutionDetector(
        graph=graph,
        min_resolution=resolutions[0],
        max_resolution=resolutions[-1],
        n_resolutions=n_steps,
        methods=methods,
        random_state=seed,
    )
    return community_detector.detect_communities()

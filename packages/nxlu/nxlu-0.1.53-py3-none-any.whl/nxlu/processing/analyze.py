import inspect
import logging
import random
import threading
import types
import warnings
from collections.abc import Callable
from typing import Any

import networkx as nx
import numpy as np

from nxlu.constants import CUSTOM_ALGORITHMS, GENERATORS_TO_DICT
from nxlu.getters import get_available_algorithms
from nxlu.processing.embed import SentenceTransformerEmbedding
from nxlu.utils.misc import cosine_similarity

warnings.filterwarnings("ignore")

random.seed(42)
rng = np.random.default_rng(seed=42)
logger = logging.getLogger("nxlu")

AVAILABLE_ALGORITHMS = get_available_algorithms(nxlu_only=False)

__all__ = [
    "get_algorithm_function",
    "map_algorithm_result",
    "apply_algorithm",
    "register_custom_algorithm",
    "GraphProperties",
    "filter_relevant_nodes",
]

_hits_lock = threading.Lock()


def get_algorithm_function(
    algorithm_name: str, algorithm_dict: dict = AVAILABLE_ALGORITHMS
) -> Callable:
    """Retrieve the appropriate algorithm function by name.

    Parameters
    ----------
    algorithm_name : str
        The name of the algorithm to retrieve.
    algorithm_dict : Dict[str, Callable]
        Dictionary of available algorithms.

    Returns
    -------
    Callable
        The function corresponding to the algorithm.

    Raises
    ------
    ValueError
        If the algorithm is not found in NetworkX or custom algorithms.
    """
    if algorithm_name in CUSTOM_ALGORITHMS:
        return CUSTOM_ALGORITHMS[algorithm_name]

    if algorithm_name in algorithm_dict:
        return algorithm_dict[algorithm_name]

    raise ValueError(f"Algorithm '{algorithm_name}' not found.")


def map_algorithm_result(graph: nx.Graph, algorithm: str, result: Any) -> None:
    """
    Map the result of an algorithm to the graph's nodes, edges, or attributes.

    Parameters
    ----------
    graph : nx.Graph
        The NetworkX graph to map the results onto.
    algorithm : str
        The name of the algorithm.
    result : Any
        The result returned by the algorithm.
    """
    if isinstance(result, dict):
        if all(graph.has_node(node) for node in result):
            for node, value in result.items():
                graph.nodes[node].setdefault("algorithm_results", {})[algorithm] = value
            logger.info(f"Mapped node attributes for algorithm '{algorithm}'.")
            return

        if all(isinstance(key, tuple) and graph.has_edge(*key) for key in result):
            for edge, value in result.items():
                if graph.has_edge(*edge):
                    if isinstance(graph, nx.MultiGraph):
                        for key in graph[edge[0]][edge[1]]:
                            graph.edges[edge[0], edge[1], key].setdefault(
                                "algorithm_results", {}
                            )[algorithm] = value
                    else:
                        graph.edges[edge[0], edge[1]].setdefault(
                            "algorithm_results", {}
                        )[algorithm] = value
            logger.info(f"Mapped edge attributes for algorithm '{algorithm}'.")
            return

        graph.graph.setdefault("algorithm_results", {})[algorithm] = result
        logger.info(f"Mapped graph-level attribute for algorithm '{algorithm}'.")
        return

    if isinstance(result, list):
        if all(isinstance(item, tuple) and len(item) == 2 for item in result):
            for edge in result:
                if graph.has_edge(*edge):
                    if isinstance(graph, nx.MultiGraph):
                        for key in graph[edge[0]][edge[1]]:
                            graph.edges[edge[0], edge[1], key].setdefault(
                                "algorithm_results", {}
                            )[algorithm] = True
                    else:
                        graph.edges[edge[0], edge[1]].setdefault(
                            "algorithm_results", {}
                        )[algorithm] = True
            logger.info(f"Mapped edge presence for algorithm '{algorithm}'.")
            return

        graph.graph.setdefault("algorithm_results", {})[algorithm] = result
        logger.info(
            f"Mapped list as graph-level attribute for algorithm '{algorithm}'."
        )
        return

    if isinstance(result, (int, float, str)):
        graph.graph.setdefault("algorithm_results", {})[algorithm] = result
        logger.info(f"Mapped scalar graph-level attribute for algorithm '{algorithm}'.")
        return

    logger.warning(
        f"Unhandled result type for algorithm '{algorithm}'. No mapping performed."
    )


def analyze_relationships(graph: nx.Graph) -> str:
    """Generate a summary of all relationships within the graph, including edge
    weights and path-based insights.

    Parameters
    ----------
    graph : nx.Graph
        The NetworkX graph to analyze.

    Returns
    -------
    str
        A summary string of all relationships in the graph.
    """
    relationship_summary = ""

    for u, v, data in graph.edges(data=True):
        relation = data.get("relation", "EDGE")
        weight = data.get("weight", "N/A")
        relationship_summary += f"{u} -- {relation} (Weight: {weight}) --> {v}\n"

    path_str_header = "\n**Path-Based Relationships:**\n"
    path_error_str = "Error computing path-based relationships\n"

    path_summary = path_str_header

    is_directed = nx.is_directed(graph)

    try:
        all_shortest_paths = dict(nx.all_pairs_shortest_path(graph))

        if not is_directed:
            # For undirected graphs, avoid redundant paths by processing each unordered
            # pair once
            processed_pairs = set()
            for source, targets in all_shortest_paths.items():
                for target, path in targets.items():
                    if source == target:
                        continue
                    pair = tuple(sorted([source, target]))
                    if pair in processed_pairs:
                        continue
                    processed_pairs.add(pair)
                    path_length = len(path) - 1
                    path_summary += (
                        f"Shortest path from {source} to {target} (Length: "
                        f"{path_length}): {' <-> '.join(map(str, path))}\n"
                    )
        else:
            # For directed graphs, list all ordered pairs
            for source, targets in all_shortest_paths.items():
                for target, path in targets.items():
                    if source == target:
                        continue
                    path_length = len(path) - 1
                    path_summary += (
                        f"Shortest path from {source} to {target} (Length: "
                        f"{path_length}): "
                        f"{' -> '.join(map(str, path))}\n"
                    )
    except Exception:
        path_summary += path_error_str

    if path_summary not in (path_error_str, path_str_header):
        relationship_summary += path_summary
    return relationship_summary


def apply_algorithm(
    algorithm_encyclopedia: dict[str, dict[str, Any]],
    graph: nx.Graph,
    algorithm_name: str,
    **kwargs,
) -> Any:
    """Apply a NetworkX algorithm or a custom algorithm to the graph.

    Parameters
    ----------
    algorithm_encyclopedia : dict
        An encyclopedia of supported algorithms and their metadata.
    graph : nx.Graph
        The input graph.
    algorithm_name : str
        The name of the algorithm to apply.
    **kwargs : Additional keyword arguments for the algorithm.

    Returns
    -------
    Any
        The result of the algorithm.

    Raises
    ------
    ValueError
        If the algorithm is not found or an error occurs during application.
    """
    logger.info(f"Applying algorithm: {algorithm_name}")

    try:
        algorithm = get_algorithm_function(algorithm_name)
    except ValueError:
        logger.exception("Error getting algorithm function")
        raise

    graph_to_use = graph.copy()
    if graph_to_use.number_of_nodes() == 0:
        error_msg = f"Algorithm '{algorithm_name}' cannot be applied to an empty graph."
        logger.error(error_msg)
        raise ValueError(error_msg)
    algorithm_metadata = algorithm_encyclopedia.get(algorithm_name)

    if algorithm_metadata:
        # directedness?
        requires_directed = algorithm_metadata.get("directed", None)
        if requires_directed is True and not graph_to_use.is_directed():
            graph_to_use = graph_to_use.to_directed()
            logger.info(f"Converted graph to directed for algorithm '{algorithm_name}'")
        elif requires_directed is False and graph_to_use.is_directed():
            graph_to_use = graph_to_use.to_undirected()
            logger.info(
                f"Converted graph to undirected for algorithm '{algorithm_name}'"
            )

        # what should be the minimum number of nodes?
        min_nodes = algorithm_metadata.get("min_nodes", None)
        if min_nodes is not None and graph_to_use.number_of_nodes() < min_nodes:
            error_msg = (
                f"Algorithm '{algorithm_name}' requires at least {min_nodes} nodes, "
                f"but graph has {graph_to_use.number_of_nodes()} nodes."
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        # check if the algorithm requires a DAG
        requires_dag = algorithm_metadata.get("requires_dag", False)
        if requires_dag:
            if not graph_to_use.is_directed():
                error_msg = f"Algorithm '{algorithm_name}' requires a directed acyclic "
                "graph (DAG)."
                logger.error(error_msg)
                raise ValueError(error_msg)
            if not nx.is_directed_acyclic_graph(graph_to_use):
                error_msg = f"Algorithm '{algorithm_name}' requires a directed acyclic "
                "graph (DAG)."
                logger.error(error_msg)
                raise ValueError(error_msg)

        # does the alg require a tree?
        requires_tree = algorithm_metadata.get("requires_tree", False)
        if requires_tree:
            if graph_to_use.is_directed():
                if not nx.is_arborescence(graph_to_use):
                    error_msg = f"Algorithm '{algorithm_name}' requires the graph to "
                    "be a directed tree (arborescence)."
                    logger.error(error_msg)
                    raise ValueError(error_msg)
            elif not nx.is_tree(graph_to_use):
                error_msg = (
                    f"Algorithm '{algorithm_name}' requires the graph to be a tree."
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

        # does the alg require connectedness?
        requires_connectedness = algorithm_metadata.get("requires_connectedness", False)
        if requires_connectedness:
            if graph_to_use.is_directed():
                is_connected = nx.is_weakly_connected(graph_to_use)
            else:
                is_connected = nx.is_connected(graph_to_use)
            if not is_connected:
                # Use the largest connected component
                if graph_to_use.is_directed():
                    connected_components = nx.weakly_connected_components(graph_to_use)
                else:
                    connected_components = nx.connected_components(graph_to_use)
                largest_cc = max(connected_components, key=len)
                graph_to_use = graph_to_use.subgraph(largest_cc).copy()
                logger.info(f"Using LCC for algorithm '{algorithm_name}'")

        requires_weighted = algorithm_metadata.get("weighted", False)
        if requires_weighted and not nx.is_weighted(graph_to_use):
            for _u, _v, data in graph_to_use.edges(data=True):
                data["weight"] = 1.0
            logger.info(
                f"Assigned default weight to edges for algorithm '{algorithm_name}'"
            )
            if (
                "weight" in inspect.signature(algorithm).parameters
                and "weight" not in kwargs
            ):
                kwargs["weight"] = "weight"

        # Cceck if the algorithm requires symmetry (undirected graph)
        requires_symmetry = algorithm_metadata.get("requires_symmetry", False)
        if requires_symmetry and graph_to_use.is_directed():
            graph_to_use = graph_to_use.to_undirected()
            logger.info(
                f"Converted graph to undirected for algorithm '{algorithm_name}'"
            )

        # handle self_loops if necessary
        self_loops = algorithm_metadata.get("self_loops", None)
        if self_loops is not None and not self_loops:
            graph_to_use.remove_edges_from(nx.selfloop_edges(graph_to_use))
            logger.info(f"Removed self-loops for algorithm '{algorithm_name}'")

    try:
        sig = inspect.signature(algorithm)
        # set default for 'k' parameter
        if "k" in sig.parameters and "k" not in kwargs:
            if algorithm_name == "all_node_cuts":
                default_k = 2
            else:
                default_k = min(100, graph_to_use.number_of_nodes())
            kwargs["k"] = default_k
            logger.info(f"Parameter 'k' set to {default_k} by default.")

        if "weight" in sig.parameters and "weight" not in kwargs:
            if nx.is_weighted(graph_to_use):
                kwargs["weight"] = "weight"
                logger.info("Parameter 'weight' set to 'weight'.")
            else:
                for _u, _v, data in graph_to_use.edges(data=True):
                    data["weight"] = 1.0
                kwargs["weight"] = "weight"
                logger.info("Assigned default weight of 1.0 to edges.")

        # set 'normalized' parameter for 'rich_club_coefficient'
        if algorithm_name == "rich_club_coefficient":
            if "normalized" in sig.parameters and "normalized" not in kwargs:
                kwargs["normalized"] = False
                logger.info(
                    "Parameter 'normalized' set to False for 'rich_club_coefficient'."
                )

    except (ValueError, TypeError) as e:
        logger.warning(
            f"Could not inspect signature of '{algorithm_name}': {e}. Proceeding "
            f"without setting 'k' or 'weight'."
        )

    try:
        result = algorithm(graph_to_use, **kwargs)
        logger.info(f"Algorithm '{algorithm_name}' applied successfully.")
    except Exception as e:
        error_msg = f"Error applying algorithm '{algorithm_name}': {e!s}"
        logger.exception(error_msg)
        raise ValueError(error_msg)

    if algorithm_name in GENERATORS_TO_DICT:
        try:
            result = dict(result)
            logger.debug(f"Converted generator result of '{algorithm_name}' to dict.")
        except Exception as e:
            error_msg = f"Failed to convert generator result of '{algorithm_name}' "
            f"to dict: {e!s}"
            logger.exception(error_msg)
            raise ValueError(error_msg)
    elif isinstance(result, types.GeneratorType):
        result = list(result)
        logger.debug(f"Converted generator result of '{algorithm_name}' to list.")

    return result


def register_custom_algorithm(name: str, func: Callable) -> None:
    """Register a custom algorithm.

    Parameters
    ----------
    name : str
        The name of the custom algorithm.
    func : Callable
        The function implementing the custom algorithm.
    """
    CUSTOM_ALGORITHMS[name] = func


class GraphProperties:
    """A class to compute and store various properties of a NetworkX graph.

    This class provides a range of attributes describing the structural properties
    of a graph, such as whether it's connected, bipartite, weighted, or planar.
    It also includes methods for identifying hubs and authorities using the HITS
    algorithm.

    Attributes
    ----------
    graph : nx.Graph
        The input NetworkX graph.
    is_directed : bool
        Whether the graph is directed.
    num_nodes : int
        The number of nodes in the graph.
    num_edges : int
        The number of edges in the graph.
    density : float
        The density of the graph.
    is_strongly_connected : bool
        Whether the graph is strongly connected (only relevant for directed graphs).
    is_connected : bool
        Whether the graph is connected (weakly connected for directed graphs).
    is_bipartite : bool
        Whether the graph is bipartite.
    is_planar : bool
        Whether the graph is planar.
    is_tree : bool
        Whether the graph is a tree.
    has_edge_data : bool
        Whether the edges of the graph contain additional data.
    has_node_data : bool
        Whether the nodes of the graph contain additional data.
    is_multigraph : bool
        Whether the graph is a multigraph.
    is_weighted : bool
        Whether the graph is weighted.
    average_clustering : float
        The average clustering coefficient of the graph.
    degree_hist : list[int]
        The degree histogram of the graph.
    peak_degree : int or None
        The degree with the highest frequency in the graph, or None if no peak exists.
    hubs : list[str]
        List of influential hubs in the graph based on the HITS algorithm.
    authorities : list[str]
        List of influential authorities in the graph based on the HITS algorithm.

    Methods
    -------
    _identify_hits(G: nx.Graph, z_threshold: float = 1.5) -> tuple[list[str], list[str]]
    :
        Identify influential hubs and authorities in the graph using the HITS
        algorithm.
    _compute_peak_degree() -> int or None:
        Compute the peak degree of the graph based on the degree histogram.
    """

    def __init__(
        self,
        graph: nx.Graph,
        compute_peak_degree: bool = True,
        identify_hits: bool = True,
        z_threshold: float = 2.0,
    ):
        """Initialize the GraphProperties object and computes various properties of the
        graph.

        Parameters
        ----------
        graph : nx.Graph
            The input NetworkX graph.
        compute_peak_degree : bool
            Compute the peak degree of the graph based on the degree histogram. Default
            is True
        identify_hits : bool
            Identify influential hubs and authorities in the graph using the HITS
            algorithm. Default is True.
        z_threshold : float
            The z-score threshold for qualifying a node as a hub or authority.
        """
        self.graph = graph
        self.is_directed = graph.is_directed()
        self.num_nodes = graph.number_of_nodes()
        self.num_edges = graph.number_of_edges()
        self.density = nx.density(graph)
        self.is_strongly_connected = (
            nx.is_strongly_connected(graph) if self.is_directed else False
        )
        self.is_connected = (
            nx.is_connected(graph)
            if not self.is_directed
            else nx.is_weakly_connected(graph)
        )
        self.is_bipartite = nx.is_bipartite(graph)
        self.is_planar = nx.check_planarity(graph)[0]
        self.is_tree = (
            nx.is_tree(graph)
            if not self.is_directed and nx.is_connected(graph)
            else False
        )
        if isinstance(graph, (nx.MultiGraph, nx.MultiDiGraph)):
            self.has_edge_data = any(
                graph.edges[u, v, k] for u, v, k in graph.edges(keys=True)
            )
        else:
            self.has_edge_data = any(graph.edges[u, v] for u, v in graph.edges())

        self.has_node_data = any(graph.nodes[node] for node in graph.nodes())
        self.is_multigraph = graph.is_multigraph()
        self.is_weighted = nx.is_weighted(graph)
        self.degrees = [d for _, d in nx.degree(graph)]
        self.min_degree = min(self.degrees) if self.degrees else 0
        self.max_degree = max(self.degrees) if self.degrees else 0
        self.avg_degree = sum(self.degrees) / len(self.degrees) if self.degrees else 0
        self.degree_counts = np.bincount(self.degrees) if self.degrees else np.array([])
        self.degree_hist = (
            self.degree_counts / self.degree_counts.sum()
            if self.degree_counts.sum() > 0
            else []
        )
        if compute_peak_degree:
            self.peak_degree = self._compute_peak_degree()
        else:
            self.peak_degree = None
        if identify_hits:
            (
                self.hits_hub_scores,
                self.hits_authority_scores,
                self.hubs,
                self.authorities,
            ) = self._identify_hits(graph)
        else:
            self.hits_hub_scores = {}
            self.hits_authority_scores = {}
            self.hubs, self.authorities = [], []

    @staticmethod
    def _identify_hits(G: nx.Graph) -> tuple[dict, dict, list, list]:
        """Identify influential hubs and authorities in the graph using HITS."""
        try:
            hits_hub_scores, hits_authority_scores = nx.hits(
                G, max_iter=50, normalized=True
            )
            sorted_hubs = sorted(
                hits_hub_scores.items(), key=lambda item: item[1], reverse=True
            )
            sorted_authorities = sorted(
                hits_authority_scores.items(), key=lambda item: item[1], reverse=True
            )
            top_n = 5
            hubs = [node for node, score in sorted_hubs[:top_n]]
            authorities = [node for node, score in sorted_authorities[:top_n]]
        except Exception:
            logger.warning("Error in HITS computation")
            return {}, {}, [], []
        else:
            return hits_hub_scores, hits_authority_scores, hubs, authorities

    def _compute_peak_degree(self) -> int | None:
        """Compute the peak degree in the graph based on the degree histogram."""
        if self.degree_hist is not None and self.degree_hist.size > 0:
            peak_degree = int(np.argmax(self.degree_hist))
            return peak_degree
        return None


def filter_relevant_nodes(
    nodes: list[str],
    query: str | None,
    model: SentenceTransformerEmbedding,
    z_threshold: float = 1.0,
) -> list[str]:
    """Filter nodes based on their semantic relevance to the user's query using
    embeddings.
    """
    if not nodes:
        return []

    if query is None:
        top_n = 5
        return nodes[:top_n]

    query_embedding = model.get_query_embedding(query)
    node_embeddings = model.get_text_embeddings(nodes)

    similarities = cosine_similarity(node_embeddings, query_embedding).flatten()

    mean_sim = np.mean(similarities)
    std_sim = np.std(similarities)
    if std_sim == 0:
        std_sim = 1e-10

    threshold = mean_sim + z_threshold * std_sim
    relevant_nodes = [
        node for node, sim in zip(nodes, similarities) if sim >= threshold
    ]

    logger.info(f"{len(relevant_nodes)} nodes relevant to the query.")

    return relevant_nodes


def approximate_diameter(G: nx.Graph) -> float:
    """Approximate the diameter of a graph using the Double Sweep Algorithm.

    Parameters
    ----------
    G : nx.Graph
        The input graph (assumed to be connected).

    Returns
    -------
    float
        The approximate diameter of the graph.
    """
    try:
        # choose an arbitrary starting node
        arbitrary_node = next(iter(G.nodes))

        # first BFS to find the farthest node from the arbitrary node
        lengths = nx.single_source_shortest_path_length(G, arbitrary_node)
        farthest_node = max(lengths, key=lengths.get)
        max_distance = lengths[farthest_node]

        # second BFS from the farthest node found
        lengths = nx.single_source_shortest_path_length(G, farthest_node)
        farthest_node_2 = max(lengths, key=lengths.get)
        approximate_diam = lengths[farthest_node_2]

        logger.debug(
            f"Approximate diameter: {approximate_diam} (Exact diameter >= "
            f"{approximate_diam})"
        )
    except Exception:
        logger.warning("Error in approximate diameter computation")
        return 1.0  # default fallback
    else:
        return approximate_diam

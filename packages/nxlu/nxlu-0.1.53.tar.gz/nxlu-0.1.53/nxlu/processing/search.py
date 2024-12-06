import gc
import hashlib
import json
import logging
import warnings
from collections import defaultdict
from pathlib import Path
from typing import Any

import faiss
import networkx as nx
import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers.quantization import (
    quantize_embeddings,
    semantic_search_faiss,
)

from nxlu.config import Precision
from nxlu.processing.community import ConsensusResult

warnings.filterwarnings("ignore")

logger = logging.getLogger("nxlu")

__all__ = ["QueryCommunityMembers"]

faiss.omp_set_num_threads(1)

EDGE_ID_SEPARATOR = "||"


class QueryCommunityMembers:
    """Query for most semantically relevant nodes and edges within detected communities.

    This class uses FAISS to efficiently search for nodes and edges that are most
    semantically similar to a query within each community. It maintains separate indices
    for nodes and edges, with caching for performance.

    Parameters
    ----------
    similarity_metric : str
        The similarity metric used for querying ('cosine' or 'euclidean').
    mmr_threshold : float
        The threshold for Maximal Marginal Relevance (MMR).
    embedding_model_name : str
        Name of the pre-trained sentence transformer model.
    batch_size : int
        Batch size for embedding computation.
    precision : Precision
        Precision to use for embeddings.
    include_edges : bool
        Whether to also index and query edges.
    cache_dir : str
        Directory for caching FAISS indices.
    """

    def __init__(
        self,
        similarity_metric: str = "cosine",
        mmr_threshold: float = 0.1,
        embedding_model_name: str = "all-MiniLM-L6-v2",
        batch_size: int = 32,
        precision: Precision = Precision.FLOAT32,
        include_edges: bool = False,
        cache_dir: str = str(Path.home() / ".nxlu_cache"),
    ):
        self.similarity_metric = similarity_metric
        self.mmr_threshold = mmr_threshold
        self.batch_size = batch_size
        self.precision = (
            precision if isinstance(precision, Precision) else Precision.FLOAT32
        )
        self.embedding_model_name = embedding_model_name
        self.cache_dir = Path(cache_dir)
        self.include_edges = include_edges

        self.embedding_model = SentenceTransformer(
            embedding_model_name,
            cache_folder=str(self.cache_dir),
            model_kwargs={"torch_dtype": self.precision.value},
        )
        self.dim = self.embedding_model.get_sentence_embedding_dimension()

        self.consensus: ConsensusResult | None = None
        self.community_indices: dict[tuple[int, str], faiss.Index] = {}

        self.node_id_maps: dict[tuple[int, str], dict[int, str]] = {}
        self.edge_id_maps: dict[tuple[int, str], dict[int, str]] = {}

        self.node_text_maps: dict[tuple[int, str], list[str]] = {}
        self.edge_text_maps: dict[tuple[int, str], list[str]] = {}

        self.node_similarity_scores: dict[tuple[int, str], dict[str, float]] = (
            defaultdict(dict)
        )

    def prepare_community_indices(
        self,
        graph: nx.Graph,
        consensus: ConsensusResult,
        similar_communities: list[tuple[tuple[int, str], float]],
    ) -> None:
        """Prepare FAISS indices for the similar communities.

        Parameters
        ----------
        graph : nx.Graph
            The full graph
        consensus : ConsensusResult
            Community detection results
        similar_communities : List[Tuple[Tuple[int, str], float]]
            List of (community_id, similarity) pairs
        """
        self.consensus = consensus
        self.graph = graph

        for community_id, _similarity in similar_communities:
            level_idx, comm_name = community_id
            community_nodes = self.consensus.hierarchical_levels[level_idx][
                int(comm_name.split("_")[1])
            ]

            # get the community subgraph
            community_graph = graph.subgraph(community_nodes).copy()

            # prepare node index
            self._prepare_node_index(community_id, community_graph)

            # optionally prepare edge index
            if self.include_edges:
                self._prepare_edge_index(community_id, community_graph)

    def _prepare_node_index(
        self,
        community_id: tuple[int, str],
        community_graph: nx.Graph,
    ) -> None:
        """Prepare FAISS index for nodes in a community."""
        nodes_data = [
            (str(node), data) for node, data in community_graph.nodes(data=True)
        ]

        if not nodes_data:
            logger.warning(f"No nodes to index in community {community_id}")
            return

        texts = [
            f"Node: {node_id}, Attributes: {data}, Description: "
            f"{data.get('description', '')}"
            for node_id, data in nodes_data
        ]

        self.node_text_maps[community_id] = texts

        node_checksum = self._compute_checksum(
            texts, f"nodes_{community_id[0]}_{community_id[1]}"
        )
        index_path = self._get_index_path("nodes", node_checksum)

        if index_path.exists():
            logger.debug(f"Using existing node embedding indices: {index_path}")
            self.community_indices[community_id] = faiss.read_index(str(index_path))

            id_map_path = index_path.with_suffix(".json")
            if id_map_path.exists():
                with id_map_path.open() as f:
                    self.node_id_maps[community_id] = json.load(f)
        else:
            embeddings = self.embedding_model.encode(
                texts, batch_size=self.batch_size, convert_to_numpy=True
            )
            embeddings = quantize_embeddings(embeddings, precision=self.precision.value)

            if self.similarity_metric == "cosine":
                embeddings = embeddings / np.linalg.norm(
                    embeddings, axis=1, keepdims=True
                )

            index = self._initialize_faiss_index()
            index.add(embeddings)
            self.community_indices[community_id] = index

            faiss.write_index(index, str(index_path))

            self.node_id_maps[community_id] = {
                idx: node_id for idx, (node_id, _) in enumerate(nodes_data)
            }
            with index_path.with_suffix(".json").open("w") as f:
                json.dump(self.node_id_maps[community_id], f)

    def _prepare_edge_index(
        self,
        community_id: tuple[int, str],
        community_graph: nx.Graph,
    ) -> None:
        """Prepare FAISS index for edges in a community."""
        edge_data = []
        edge_ids = []

        if isinstance(community_graph, (nx.MultiGraph, nx.MultiDiGraph)):
            for u, v, key, data in community_graph.edges(keys=True, data=True):
                edge_id = f"{u}{EDGE_ID_SEPARATOR}{v}{EDGE_ID_SEPARATOR}{key}"
                edge_data.append((u, v, key, data, edge_id))
        else:
            for u, v, data in community_graph.edges(data=True):
                edge_id = f"{u}{EDGE_ID_SEPARATOR}{v}"
                edge_data.append((u, v, data, edge_id))

        if not edge_data:
            logger.warning(f"No edges to index in community {community_id}")
            return

        texts = []
        for entry in edge_data:
            if isinstance(community_graph, (nx.MultiGraph, nx.MultiDiGraph)):
                u, v, key, data, edge_id = entry
            else:
                u, v, data, edge_id = entry

            text = (
                f"Edge: {u} -- {data.get('relation', 'EDGE')} "
                f"(Weight: {data.get('weight', 'N/A')}) "
                f"--> {v} | ID: {edge_id}"
            )
            texts.append(text)
            edge_ids.append(edge_id)

        self.edge_text_maps[community_id] = texts

        # compute or load cached embeddings
        edge_checksum = self._compute_checksum(
            texts, f"edges_{community_id[0]}_{community_id[1]}"
        )
        index_path = self._get_index_path("edges", edge_checksum)

        if index_path.exists():
            logger.debug(f"Using existing edge embedding indices: {index_path}")
            self.community_indices[community_id] = faiss.read_index(str(index_path))

            id_map_path = index_path.with_suffix(".json")
            if id_map_path.exists():
                with id_map_path.open() as f:
                    self.edge_id_maps[community_id] = json.load(f)
        else:
            # create new index
            embeddings = self.embedding_model.encode(
                texts, batch_size=self.batch_size, convert_to_numpy=True
            )
            embeddings = quantize_embeddings(embeddings, precision=self.precision.value)

            if self.similarity_metric == "cosine":
                embeddings = embeddings / np.linalg.norm(
                    embeddings, axis=1, keepdims=True
                )

            index = self._initialize_faiss_index()
            index.add(embeddings)
            self.community_indices[community_id] = index

            faiss.write_index(index, str(index_path))

            self.edge_id_maps[community_id] = dict(enumerate(edge_ids))
            with index_path.with_suffix(".json").open("w") as f:
                json.dump(self.edge_id_maps[community_id], f)

    def query_communities(
        self,
        query: str,
        top_k_nodes: int = 500,
        top_k_edges: int = 1000,
    ) -> tuple[
        dict[tuple[int, str], list[str]], dict[tuple[int, str], list[tuple[str, ...]]]
    ]:
        """Query each community for relevant nodes and edges."""
        if not self.consensus:
            raise ValueError("Must call prepare_community_indices() before querying")

        if not self.community_indices:
            logger.warning("No community indices available for querying")
            return {}, {}

        query_embedding = self.embedding_model.encode(
            [query], convert_to_numpy=True
        ).reshape(1, -1)

        if self.similarity_metric == "cosine":
            query_embedding = query_embedding / np.linalg.norm(
                query_embedding, axis=1, keepdims=True
            )
        query_embedding = quantize_embeddings(
            query_embedding, precision=self.precision.value
        )

        community_nodes = {}
        community_edges = {}

        for community_id, index in self.community_indices.items():
            logger.debug(f"\nProcessing community {community_id}")
            logger.debug(f"Index contains {index.ntotal} vectors")

            if community_id in self.node_id_maps:
                logger.debug(f"Node text examples for community {community_id}:")
                if community_id in self.node_text_maps:
                    for i, text in enumerate(self.node_text_maps[community_id][:3]):
                        logger.debug(f"Node {i}: {text}")

                node_results = semantic_search_faiss(
                    query_embeddings=query_embedding,
                    corpus_index=index,
                    top_k=min(top_k_nodes, index.ntotal),
                    corpus_precision=self.precision.value,
                    rescore=False,
                    output_index=False,
                    exact=False,
                )[0]

                logger.debug(f"Retrieved {len(node_results)} results from FAISS")

                node_ids = []
                similarity_scores = []

                self.node_similarity_scores[community_id] = {}

                for hit in node_results:
                    corpus_id = str(int(hit[0]["corpus_id"]))
                    score = float(hit[0]["score"])

                    logger.debug(f"Hit - corpus_id: {corpus_id}, score: {score}")

                    node_id = self.node_id_maps[community_id].get(
                        corpus_id
                    ) or self.node_id_maps[community_id].get(int(corpus_id))

                    if node_id:
                        logger.debug(f"Found node_id: {node_id} with score: {score}")
                        if (
                            score > self.mmr_threshold
                        ):  # Only include if above threshold
                            node_ids.append(node_id)
                            similarity_scores.append(score)
                            self.node_similarity_scores[community_id][node_id] = score
                    else:
                        logger.warning(f"No node ID found for corpus_id {corpus_id}")

                if node_ids:
                    logger.info(
                        f"Community {community_id}: Found {len(node_ids)} relevant "
                        f"nodes with scores from {min(similarity_scores):.3f} to "
                        f"{max(similarity_scores):.3f}"
                    )
                    community_nodes[community_id] = node_ids
                else:
                    logger.warning(
                        f"No nodes above threshold found for community {community_id}"
                    )

            if self.include_edges and community_id in self.edge_id_maps:
                edge_results = semantic_search_faiss(
                    query_embeddings=query_embedding,
                    corpus_index=index,
                    top_k=min(top_k_edges, index.ntotal),
                    corpus_precision=self.precision.value,
                    rescore=False,
                    output_index=False,
                    exact=False,
                )[0]

                edge_tuples = []
                for hit in edge_results:
                    corpus_id = int(hit[0]["corpus_id"])
                    edge_id = self.edge_id_maps[community_id].get(str(corpus_id))
                    if edge_id is None:
                        edge_id = self.edge_id_maps[community_id].get(corpus_id)

                    if edge_id:
                        edge_tuple = tuple(edge_id.split(EDGE_ID_SEPARATOR))
                        if self._validate_edge_tuple(edge_tuple):
                            edge_tuples.append(edge_tuple)

                if edge_tuples:
                    community_edges[community_id] = edge_tuples

        logger.debug(f"Total communities with nodes: {len(community_nodes)}")
        logger.debug(f"Total communities with edges: {len(community_edges)}")

        return community_nodes, community_edges

    def create_query_subgraph(
        self,
        query: str,
        similar_communities: list[tuple[tuple[int, str], float]],
    ) -> dict[tuple[int, str], dict[str, Any]]:
        """Return dictionary of similar communities mapped to their subgraphs, nodes
        and edges.

        Parameters
        ----------
        query : str
            The query string
        similar_communities : List[Tuple[Tuple[int, str], float]]
            List of (community_id, similarity) pairs from CommunityQueryMatcher

        Returns
        -------
        Dict[Tuple[int, str], Dict[str, Any]]
            Dictionary mapping community IDs to:
                - subgraph: nx.Graph of the community
                - nodes: List of most similar nodes
                - edges: List of most similar edges
                - similarity_scores: Dict mapping nodes to their similarity scores
        """
        community_nodes, community_edges = self.query_communities(query)

        relevance_dict = {}

        for community_id, _similarity in similar_communities:
            level_idx, comm_name = community_id
            community_nodes_set = self.consensus.hierarchical_levels[level_idx][
                int(comm_name.split("_")[1])
            ]

            community_subgraph = self.graph.subgraph(community_nodes_set).copy()
            relevance_dict[community_id] = {
                "subgraph": community_subgraph,
                "nodes": [],
                "edges": [],
                "similarity_scores": {},
            }

            if (
                community_id in community_nodes
                and community_id in self.node_similarity_scores
            ):
                nodes = community_nodes[community_id]
                scores = self.node_similarity_scores[community_id]

                for node in nodes:
                    score = scores.get(node, 0)
                    relevance_dict[community_id]["nodes"].append(node)
                    relevance_dict[community_id]["similarity_scores"][node] = score

            if self.include_edges and community_id in community_edges:
                edges = community_edges[community_id]
                if isinstance(self.graph, (nx.MultiGraph, nx.MultiDiGraph)):
                    edges = [
                        (u, v, k)
                        for (u, v, k) in edges
                        if self.graph.has_edge(u, v, key=k)
                    ]
                else:
                    edges = [(u, v) for (u, v) in edges if self.graph.has_edge(u, v)]
                relevance_dict[community_id]["edges"] = edges

        logger.info(
            f"Found relevant nodes/edges across {len(relevance_dict)} communities for "
            f"query: '{query}'"
        )

        for community_id, data in relevance_dict.items():
            logger.debug(
                f"Community {community_id}: "
                f"subgraph size: {data['subgraph'].number_of_nodes()} nodes "
                f"and {data['subgraph'].number_of_edges()} edges, "
                f"similar nodes: {len(data['nodes'])}, "
                f"similar scores: {len(data['similarity_scores'])}, "
                f"similar edges: {len(data['edges'])}"
            )

        return relevance_dict

    def _initialize_faiss_index(self) -> faiss.Index:
        """Initialize a FAISS index based on the similarity metric."""
        if self.similarity_metric == "cosine":
            index = faiss.IndexFlatIP(self.dim)
        elif self.similarity_metric == "euclidean":
            index = faiss.IndexFlatL2(self.dim)
        else:
            raise ValueError(f"Unsupported similarity metric: {self.similarity_metric}")
        return index

    def _compute_checksum(self, texts: list[str], index_type: str) -> str:
        """Compute SHA256 checksum based on texts and embedding parameters."""
        try:
            data = {
                "index_type": index_type,
                "similarity_metric": self.similarity_metric,
                "embedding_model_name": self.embedding_model_name,
                "precision": self.precision,
                "texts": texts,
            }
            data_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
        except Exception as e:
            logger.exception("Failed to compute checksum.")
            raise
        return hashlib.sha256(data_bytes).hexdigest()

    def _get_index_path(self, base_type: str, checksum: str) -> Path:
        """Generate the file path for the FAISS index."""
        filename = f"{base_type}_index_{checksum}.faiss"
        return self.cache_dir / filename

    def _validate_edge_tuple(self, edge_tuple: tuple[str, ...]) -> bool:
        """Validate the edge tuple based on the graph type."""
        if isinstance(self.graph, (nx.MultiGraph, nx.MultiDiGraph)):
            return len(edge_tuple) == 3 and self.graph.has_edge(
                edge_tuple[0], edge_tuple[1], key=edge_tuple[2]
            )
        return len(edge_tuple) == 2 and self.graph.has_edge(
            edge_tuple[0], edge_tuple[1]
        )

    @staticmethod
    def _add_mst_edges(G: nx.Graph, subgraph: nx.Graph) -> nx.Graph:
        """Add edges from the Minimum Spanning Tree to ensure connectivity."""
        try:
            if subgraph.number_of_nodes() > 1:
                induced_graph = G.subgraph(subgraph.nodes())
                mst = nx.minimum_spanning_tree(induced_graph, weight="weight")
                subgraph.add_edges_from(mst.edges(data=True))
                logger.debug(
                    "Added MST edges from induced graph to ensure connectivity."
                )
        except Exception:
            logger.exception("Failed to compute MST on induced graph")
        return subgraph

    @staticmethod
    def _is_connected(graph: nx.Graph) -> bool:
        """Check if the graph is connected."""
        if nx.is_directed(graph):
            return nx.is_weakly_connected(graph)
        return nx.is_connected(graph)

    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up FAISS indices and embedding model.")
        if hasattr(self, "community_indices"):
            for key in list(self.community_indices.keys()):
                del self.community_indices[key]
        if hasattr(self, "embedding_model"):
            del self.embedding_model
        gc.collect()

    def __del__(self):
        try:
            self.cleanup()
        except Exception as e:
            logger.exception("Exception during cleanup in __del__.")

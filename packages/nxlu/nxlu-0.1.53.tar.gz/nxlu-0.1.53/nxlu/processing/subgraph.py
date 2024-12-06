from collections import defaultdict
from collections.abc import Mapping
from typing import Any

import networkx as nx
import numpy as np

__all__ = ["QuerySubgraphHandler"]


class QuerySubgraphHandler:
    """Handles the aggregation and analysis of query-relevant subgraphs.

    This class provides methods to combine and analyze multiple community subgraphs
    while preserving community structure and similarity information. It supports both
    unified analysis across all relevant subgraphs and community-specific analysis
    when needed.

    Parameters
    ----------
    community_relevance : Dict[Tuple[int, str], Dict[str, Any]]
        Dictionary mapping community IDs to their subgraphs and relevance data
    similarity_threshold : float, optional
        Minimum similarity score to consider a node relevant, by default 0.5
    preserve_communities : bool, optional
        Whether to maintain separate community labels, by default True
    """

    def __init__(
        self,
        community_relevance: Mapping[tuple[int, str], dict[str, Any]],
        similarity_threshold: float = 0.5,
        preserve_communities: bool = True,
    ):
        self.community_data = community_relevance
        self.similarity_threshold = similarity_threshold
        self.preserve_communities = preserve_communities
        self.unified_graph = nx.Graph()
        self.node_communities = {}
        self.node_similarities = {}
        self.community_bridges = set()

        self._build_unified_graph()

    def _build_unified_graph(self) -> None:
        """Build a unified graph from all relevant community subgraphs."""
        seen_nodes = set()

        for comm_id, data in self.community_data.items():
            if not isinstance(data, dict):
                continue

            subgraph = data.get("subgraph")
            if not isinstance(subgraph, nx.Graph):
                continue

            similar_nodes = set(data.get("nodes", []))
            similarity_scores = data.get("similarity_scores", {})

            for node in subgraph.nodes():
                if node not in seen_nodes:
                    attrs = dict(subgraph.nodes[node])
                    if self.preserve_communities:
                        attrs["community"] = comm_id
                    score = similarity_scores.get(node, 0.0)
                    attrs["similarity_score"] = score
                    attrs["query_relevant"] = node in similar_nodes

                    self.unified_graph.add_node(node, **attrs)
                    seen_nodes.add(node)
                    self.node_communities[node] = comm_id
                    self.node_similarities[node] = score

                elif self.preserve_communities:
                    current_score = self.node_similarities.get(node, 0.0)
                    new_score = similarity_scores.get(node, 0.0)
                    if new_score > current_score:
                        self.node_similarities[node] = new_score
                        self.unified_graph.nodes[node]["similarity_score"] = new_score
                    self.community_bridges.add(node)

            self.unified_graph.add_edges_from(subgraph.edges(data=True))

    def get_relevant_subgraph(self, min_similarity: float | None = None) -> nx.Graph:
        """Extract a subgraph containing only the most query-relevant nodes.

        Parameters
        ----------
        min_similarity : float, optional
            Override default similarity threshold, by default None

        Returns
        -------
        nx.Graph
            Subgraph containing high-similarity nodes and their connections
        """
        threshold = (
            min_similarity if min_similarity is not None else self.similarity_threshold
        )

        relevant_nodes = [
            node for node, score in self.node_similarities.items() if score >= threshold
        ]

        if not relevant_nodes:
            return nx.Graph()

        return self.unified_graph.subgraph(relevant_nodes).copy()

    def get_community_subgraphs(self) -> dict[tuple[int, str], nx.Graph]:
        """Get dictionary of community-specific subgraphs.

        Returns
        -------
        Dict[Tuple[int, str], nx.Graph]
            Mapping of community IDs to their subgraphs
        """
        community_graphs = {}

        for comm_id in self.community_data:
            nodes = [
                node for node, c_id in self.node_communities.items() if c_id == comm_id
            ]
            if nodes:
                community_graphs[comm_id] = self.unified_graph.subgraph(nodes).copy()

        return community_graphs

    def get_bridge_nodes(self) -> set:
        """Get nodes that appear in multiple communities.

        Returns
        -------
        Set
            Set of nodes that bridge communities
        """
        return self.community_bridges.copy()

    def get_node_metadata(self) -> dict[str, dict[str, Any]]:
        """Get consolidated node metadata including community and similarity info.

        Returns
        -------
        Dict[str, Dict[str, Any]]
            Dictionary mapping nodes to their metadata
        """
        metadata = defaultdict(dict)

        for node in self.unified_graph.nodes():
            metadata[node] = {
                "community": self.node_communities.get(node),
                "similarity_score": self.node_similarities.get(node, 0.0),
                "is_bridge": node in self.community_bridges,
                "attributes": dict(self.unified_graph.nodes[node]),
            }

        return dict(metadata)

    def rank_nodes_by_relevance(self) -> list[tuple[Any, float]]:
        """Rank nodes by their query similarity scores.

        Returns
        -------
        List[Tuple[Any, float]]
            List of (node, score) tuples sorted by descending similarity
        """
        return sorted(self.node_similarities.items(), key=lambda x: x[1], reverse=True)

    def get_community_overlap_matrix(self) -> tuple[np.ndarray, list]:
        """Calculate overlap between communities based on shared nodes.

        Returns
        -------
        Tuple[np.ndarray, List]
            Overlap matrix and list of community IDs
        """
        communities = list(self.community_data.keys())
        n_communities = len(communities)

        if n_communities == 0:
            return np.array([]), []

        overlap_matrix = np.zeros((n_communities, n_communities))

        for i, comm1 in enumerate(communities):
            nodes1 = {
                node for node, c_id in self.node_communities.items() if c_id == comm1
            }
            for j, comm2 in enumerate(communities[i:], i):
                nodes2 = {
                    node
                    for node, c_id in self.node_communities.items()
                    if c_id == comm2
                }
                overlap = len(nodes1 & nodes2)
                overlap_matrix[i, j] = overlap_matrix[j, i] = overlap

        return overlap_matrix, communities

    def __bool__(self) -> bool:
        """Return True if the handler contains any nodes.

        Returns
        -------
        bool
            True if the unified graph has any nodes, False otherwise
        """
        return self.unified_graph.number_of_nodes() > 0

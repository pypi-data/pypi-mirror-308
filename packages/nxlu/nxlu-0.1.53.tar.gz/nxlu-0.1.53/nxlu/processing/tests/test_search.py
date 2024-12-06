from pathlib import Path
from unittest.mock import Mock, patch

import faiss
import networkx as nx
import numpy as np
import pytest

from nxlu.config import Precision
from nxlu.processing.search import QueryCommunityMembers

# ==================== Mock Objects ====================


class MockSentenceTransformer:
    def __init__(self, model_name, cache_folder, model_kwargs):
        self.model_name = model_name
        self.cache_folder = cache_folder
        self.model_kwargs = model_kwargs

    def encode(self, texts, **kwargs):
        # Simulate encoding by returning random embeddings
        embedding_dim = self.get_sentence_embedding_dimension()
        return np.random.rand(len(texts), embedding_dim).astype(np.float32)

    def get_sentence_embedding_dimension(self):
        # Return a fixed embedding dimension
        return 384


def normalize_embedding(embedding):
    norm = np.linalg.norm(embedding)
    return (np.array(embedding) / norm).tolist()


@pytest.fixture
def mock_sentence_transformer():
    """Mock fixture for SentenceTransformer using the MockSentenceTransformer class."""
    mock_transformer = Mock(spec=MockSentenceTransformer)
    mock_transformer.encode.return_value = np.random.rand(10, 384).astype(np.float32)
    mock_transformer.get_sentence_embedding_dimension.return_value = 384
    return mock_transformer


@pytest.fixture
def mock_faiss(monkeypatch):
    """Mock fixture for FAISS operations."""
    mock_index = Mock()
    mock_index.ntotal = 10
    mock_index.add = Mock()

    monkeypatch.setattr("faiss.read_index", Mock(return_value=mock_index))
    monkeypatch.setattr("faiss.write_index", Mock())

    return mock_index


# ==================== Core Fixtures ====================


@pytest.fixture
def mock_semantic_search_default(monkeypatch):
    """
    Mock fixture for semantic_search_faiss with default parameters.
    Returns a list of lists of lists of dictionaries.
    """
    mock_return = [[[{"corpus_id": i, "score": 0.95 - i * 0.1}] for i in range(3)]]
    mock = Mock(return_value=mock_return)
    monkeypatch.setattr("nxlu.processing.search.semantic_search_faiss", mock)
    return mock


@pytest.fixture
def mock_semantic_search_parametrized(monkeypatch, request):
    params = request.param
    n_results = params.get("n_results", 3)
    score_decay = params.get("score_decay", 0.1)

    mock_return = [
        [[{"corpus_id": i, "score": 0.95 - i * score_decay}] for i in range(n_results)]
    ]
    mock = Mock(return_value=mock_return)
    monkeypatch.setattr("nxlu.processing.search.semantic_search_faiss", mock)
    return mock


@pytest.fixture
def mock_semantic_search_large(monkeypatch):
    """
    Mock fixture for semantic_search_faiss with a large number of results.
    Returns a list of lists where each hit is a list containing a dictionary.
    """
    mock_return = [[[{"corpus_id": i, "score": 0.95 - i * 0.01}] for i in range(500)]]
    mock = Mock(return_value=mock_return)
    monkeypatch.setattr("nxlu.processing.search.semantic_search_faiss", mock)
    return mock


@pytest.fixture
def query_community_members_instance(
    mock_sentence_transformer,
    mock_faiss,
    mock_semantic_search_default,
    tmp_path,
):
    """
    Fixture to create an instance of QueryCommunityMembers with mocked dependencies.
    Uses a temporary directory for caching to avoid FileNotFoundError.
    """
    with patch(
        "nxlu.processing.embed.SentenceTransformer",
        return_value=mock_sentence_transformer,
    ):
        with patch.object(Path, "exists", return_value=False):
            qcm = QueryCommunityMembers(
                similarity_metric="cosine",
                mmr_threshold=0.1,
                embedding_model_name="all-MiniLM-L6-v2",
                batch_size=32,
                precision=Precision.FLOAT32,
                include_edges=True,  # Set to True if your tests require edge handling
                cache_dir=str(tmp_path),  # Use the temporary directory
            )
            yield qcm
            qcm.cleanup()


@pytest.fixture
def sample_data():
    """Fixture to provide sample graph data."""
    data = [
        ("node1", "node2"),
        ("node2", "node3"),
        ("node3", "node4"),
        ("node4", "node5"),
    ]
    nodes = ["node1", "node2", "node3", "node4", "node5"]
    return data, nodes


@pytest.fixture
def complex_graph():
    """Fixture to provide a complex graph for testing."""
    graph = nx.Graph()
    graph.add_edges_from(
        [
            ("node1", "node2"),
            ("node2", "node3"),
            ("node3", "node4"),
            ("node4", "node5"),
            ("node6", "node7"),
            ("node7", "node8"),
        ]
    )
    return graph


class TestQueryCommunityMembersEdgeCases:
    def test_query_communities_with_all_token_nodes(
        self,
        query_community_members_instance,
        sample_data,
        mock_sentence_transformer,
        mock_faiss,
        mock_semantic_search_default,
    ):
        data, nodes = sample_data
        # Convert nodes list to a dictionary with attributes
        nodes = {str(node): {"type": "token"} for node in nodes}
        graph = nx.Graph()
        graph.add_edges_from(data)
        for node, attrs in nodes.items():
            graph.nodes[node].update(attrs)

        consensus = Mock()
        consensus.hierarchical_levels = {
            0: [["node1", "node2"], ["node3", "node4", "node5"]]
        }
        similar_communities = [((0, "Community_0"), 0.9), ((0, "Community_1"), 0.8)]

        query_community_members_instance.prepare_community_indices(
            graph=graph,
            consensus=consensus,
            similar_communities=similar_communities,
        )

        # Store IDs as integers in node_id_maps
        for community_id in query_community_members_instance.node_id_maps:
            query_community_members_instance.node_id_maps[community_id] = {
                int(k): v
                for k, v in query_community_members_instance.node_id_maps[
                    community_id
                ].items()
            }

        community_nodes, community_edges = (
            query_community_members_instance.query_communities(query="test query")
        )

        print(f"community_nodes: {community_nodes}")
        print(f"community_edges: {community_edges}")

        assert isinstance(community_nodes, dict)
        assert isinstance(community_edges, dict)


class TestQueryCommunityMembersAdvancedEdgeCases:
    def test_query_communities_with_large_k_edges(
        self,
        query_community_members_instance,
        sample_data,
        mock_sentence_transformer,
        mock_faiss,
        mock_semantic_search_large,
    ):
        data, nodes = sample_data
        nodes = {str(node): {"type": "token"} for node in nodes}
        graph = nx.Graph()
        graph.add_edges_from(data)
        for node, attrs in nodes.items():
            graph.nodes[node].update(attrs)

        consensus = Mock()
        consensus.hierarchical_levels = {
            0: [["node1", "node2"], ["node3", "node4", "node5"]]
        }
        similar_communities = [((0, "Community_0"), 0.9), ((0, "Community_1"), 0.8)]

        query_community_members_instance.prepare_community_indices(
            graph=graph,
            consensus=consensus,
            similar_communities=similar_communities,
        )

        # Store IDs as integers in node_id_maps
        for community_id in query_community_members_instance.node_id_maps:
            query_community_members_instance.node_id_maps[community_id] = {
                int(k): v
                for k, v in query_community_members_instance.node_id_maps[
                    community_id
                ].items()
            }

        community_nodes, community_edges = (
            query_community_members_instance.query_communities(
                query="test query",
                top_k_nodes=500,
                top_k_edges=10000,
            )
        )

        assert isinstance(community_nodes, dict)
        assert isinstance(community_edges, dict)

    def test_create_query_subgraph_with_disconnected_subgraph(
        self,
        query_community_members_instance,
        complex_graph,
        mock_sentence_transformer,
        mock_faiss,
        mock_semantic_search_default,
    ):
        consensus = Mock()
        consensus.hierarchical_levels = {
            0: [["node1", "node2"], ["node3", "node4", "node5"]]
        }
        similar_communities = [((0, "Community_0"), 0.9), ((0, "Community_1"), 0.8)]

        query_community_members_instance.prepare_community_indices(
            graph=complex_graph,
            consensus=consensus,
            similar_communities=similar_communities,
        )

        query_community_members_instance.node_id_maps = {
            (0, "Community_0"): {0: "node1", 1: "node2"},
            (0, "Community_1"): {0: "node3", 1: "node4", 2: "node5"},
        }

        with patch(
            "nxlu.processing.search.semantic_search_faiss",
            return_value=[
                [[{"corpus_id": 0, "score": 0.95}], [{"corpus_id": 1, "score": 0.85}]]
            ],
        ):
            subgraph = query_community_members_instance.create_query_subgraph(
                query="test query",
                similar_communities=similar_communities,
            )

        assert isinstance(subgraph, dict)
        assert (
            nx.is_connected(subgraph[(0, "Community_0")]["subgraph"])
            or subgraph[(0, "Community_0")]["subgraph"].number_of_nodes() <= 1
        )

    def test_graph_with_varied_community_sizes(
        self,
        query_community_members_instance,
        mock_sentence_transformer,
        mock_faiss,
        mock_semantic_search_default,
    ):
        """Test handling of communities with different sizes."""
        graph = nx.Graph()
        communities = {
            0: [f"node{i}" for i in range(5)],
            1: [f"node{i}" for i in range(5, 8)],
            2: [f"node{i}" for i in range(8, 15)],
        }

        for nodes in communities.values():
            graph.add_nodes_from(nodes)
            if len(nodes) > 1:
                for i in range(len(nodes) - 1):
                    graph.add_edge(nodes[i], nodes[i + 1])

        consensus = Mock()
        consensus.hierarchical_levels = {0: list(communities.values())}
        similar_communities = [
            ((0, f"Community_{i}"), 0.9 - i * 0.1) for i in communities
        ]

        query_community_members_instance.prepare_community_indices(
            graph=graph,
            consensus=consensus,
            similar_communities=similar_communities,
        )

        community_nodes, community_edges = (
            query_community_members_instance.query_communities(query="test query")
        )

        assert isinstance(community_nodes, dict)
        assert isinstance(community_edges, dict)


@pytest.mark.parametrize(
    "mock_semantic_search_parametrized",
    [
        {"n_results": 3, "score_decay": 0.1},
        {"n_results": 500, "score_decay": 0.01},
    ],
    indirect=True,
)
def test_parameterized_search(
    query_community_members_instance,
    sample_data,
    mock_sentence_transformer,
    mock_faiss,
    mock_semantic_search_parametrized,
):
    """Test with different search configurations."""
    data, nodes = sample_data
    nodes = {str(node): {"type": "token"} for node in nodes}
    graph = nx.Graph()
    graph.add_edges_from(data)
    for node, attrs in nodes.items():
        graph.nodes[node].update(attrs)

    consensus = Mock()
    consensus.hierarchical_levels = {
        0: [["node1", "node2"], ["node3", "node4", "node5"]]
    }
    similar_communities = [((0, "Community_0"), 0.9), ((0, "Community_1"), 0.8)]

    query_community_members_instance.prepare_community_indices(
        graph=graph,
        consensus=consensus,
        similar_communities=similar_communities,
    )

    for community_id in query_community_members_instance.node_id_maps:
        query_community_members_instance.node_id_maps[community_id] = {
            int(k): v
            for k, v in query_community_members_instance.node_id_maps[
                community_id
            ].items()
        }

    community_nodes, community_edges = (
        query_community_members_instance.query_communities(query="test query")
    )

    assert isinstance(community_nodes, dict)
    assert isinstance(community_edges, dict)


def test_compute_checksum(query_community_members_instance):
    texts = ["sample text"]
    index_type = "nodes_0_Community_0"
    checksum = query_community_members_instance._compute_checksum(texts, index_type)
    assert isinstance(checksum, str)
    assert len(checksum) == 64  # Length of SHA256 hash in hex


def test_get_index_path(query_community_members_instance, tmp_path):
    base_type = "nodes"
    checksum = "dummychecksum"
    expected_path = Path(tmp_path) / "nodes_index_dummychecksum.faiss"
    with patch.object(query_community_members_instance, "cache_dir", tmp_path):
        index_path = query_community_members_instance._get_index_path(
            base_type, checksum
        )
        assert index_path == expected_path


def test_validate_edge_tuple_graph(query_community_members_instance, sample_data):
    graph = nx.Graph()
    graph.add_edges_from(sample_data[0])
    query_community_members_instance.graph = graph

    # Valid edge
    valid_tuple = ("node1", "node2")
    assert query_community_members_instance._validate_edge_tuple(valid_tuple) is True

    # Invalid edge
    invalid_tuple = ("node1", "node3")
    assert query_community_members_instance._validate_edge_tuple(invalid_tuple) is False


def test_validate_edge_tuple_multigraph(query_community_members_instance, sample_data):
    graph = nx.MultiGraph()
    graph.add_edge("node1", "node2", key=0)
    query_community_members_instance.graph = graph

    # Valid edge with key
    valid_tuple = ("node1", "node2", 0)
    assert query_community_members_instance._validate_edge_tuple(valid_tuple) is True

    # Invalid edge
    invalid_tuple = ("node1", "node3", 0)
    assert query_community_members_instance._validate_edge_tuple(invalid_tuple) is False


def test_add_mst_edges(query_community_members_instance, complex_graph):
    subgraph = nx.Graph()
    subgraph.add_nodes_from(["node1", "node2"])  # Use connected nodes
    query_community_members_instance.graph = complex_graph

    updated_subgraph = query_community_members_instance._add_mst_edges(
        complex_graph, subgraph
    )

    assert nx.is_connected(updated_subgraph)
    assert updated_subgraph.has_edge("node1", "node2")


def test_prepare_community_indices_no_nodes(
    query_community_members_instance,
    mock_faiss,
    complex_graph,
    mock_sentence_transformer,
):
    consensus = Mock()
    consensus.hierarchical_levels = {0: [[]]}
    similar_communities = [((0, "Community_0"), 0.9)]

    with patch.object(
        query_community_members_instance, "_compute_checksum", return_value="checksum"
    ):
        query_community_members_instance.prepare_community_indices(
            graph=complex_graph,
            consensus=consensus,
            similar_communities=similar_communities,
        )

    assert not query_community_members_instance.community_indices


def test_query_communities_without_preparation(query_community_members_instance):
    with pytest.raises(
        ValueError, match=r"Must call prepare_community_indices\(\) before querying"
    ):
        query_community_members_instance.query_communities(query="test")


def test_create_query_subgraph_no_results(
    query_community_members_instance,
    complex_graph,
    mock_sentence_transformer,
    mock_faiss,
):
    consensus = Mock()
    consensus.hierarchical_levels = {0: [["node1"], ["node2"]]}
    similar_communities = [((0, "Community_0"), 0.9), ((0, "Community_1"), 0.8)]

    query_community_members_instance.prepare_community_indices(
        graph=complex_graph,
        consensus=consensus,
        similar_communities=similar_communities,
    )

    with patch.object(
        query_community_members_instance, "query_communities", return_value=({}, {})
    ):
        subgraph = query_community_members_instance.create_query_subgraph(
            query="no results", similar_communities=similar_communities
        )

    assert isinstance(subgraph, dict)
    for data in subgraph.values():
        community_subgraph = data["subgraph"]
        assert isinstance(community_subgraph, nx.Graph)
        assert community_subgraph.number_of_nodes() == 1
        assert community_subgraph.number_of_edges() == 0


def test_similarity_metrics_cosine(
    query_community_members_instance, mock_faiss, mock_semantic_search_default
):
    query_community_members_instance.similarity_metric = "cosine"
    query_community_members_instance.prepare_community_indices(
        graph=nx.Graph(),
        consensus=Mock(),
        similar_communities=[],
    )
    assert isinstance(
        query_community_members_instance._initialize_faiss_index(), faiss.IndexFlatIP
    )


def test_similarity_metrics_euclidean(
    query_community_members_instance, mock_faiss, mock_semantic_search_default
):
    query_community_members_instance.similarity_metric = "euclidean"
    query_community_members_instance.dim = 384
    index = query_community_members_instance._initialize_faiss_index()
    assert isinstance(index, faiss.IndexFlatL2)


def test_cleanup(query_community_members_instance, mock_faiss):
    query_community_members_instance.community_indices = {
        "community1": mock_faiss,
        "community2": mock_faiss,
    }
    query_community_members_instance.embedding_model = Mock()

    with patch("gc.collect") as mock_gc:
        query_community_members_instance.cleanup()
        assert len(query_community_members_instance.community_indices) == 0
        assert not hasattr(query_community_members_instance, "embedding_model")
        mock_gc.assert_called_once()

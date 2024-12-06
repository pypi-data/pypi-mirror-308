from unittest.mock import MagicMock, Mock, patch

import networkx as nx
import numpy as np
import pytest

from nxlu.processing.community import (
    CommunityMethod,
    CommunityPriors,
    CommunityQueryMatcher,
    CommunityResolution,
    ConsensusResult,
    LeidenAlgorithm,
    MultiResolutionDetector,
    get_communities,
    leiden_communities,
)


@pytest.fixture
def empty_graph():
    return nx.Graph()


@pytest.fixture
def single_node_graph():
    G = nx.Graph()
    G.add_node("A")
    return G


@pytest.fixture
def simple_graph():
    G = nx.Graph()
    G.add_edges_from(
        [
            ("A", "B"),
            ("B", "C"),
            ("C", "A"),
            ("C", "D"),
            ("D", "E"),
            ("E", "F"),
            ("F", "D"),
        ]
    )
    return G


@pytest.fixture
def disconnected_graph():
    G = nx.Graph()
    G.add_edges_from(
        [
            ("A", "B"),
            ("B", "C"),
            ("D", "E"),
            ("E", "F"),
        ]
    )
    return G


def test_community_resolution():
    resolution = 1.0
    communities = [{"A", "B", "C"}, {"D", "E", "F"}]
    modularity = 0.42
    method = "LEIDEN"

    cr = CommunityResolution(resolution, communities, modularity, method)

    assert cr.resolution == resolution
    assert cr.communities == communities
    assert cr.modularity == modularity
    assert cr.method == method


def test_consensus_result():
    communities = [{"A", "B"}, {"C", "D"}]
    modularity = 0.5
    methods = ["LEIDEN", "LOUVAIN"]
    hierarchical_levels = [[{"A", "B"}, {"C", "D"}], [{"A"}, {"B"}, {"C", "D"}]]

    cr = ConsensusResult(communities, modularity, methods, hierarchical_levels)

    assert cr.communities == communities
    assert cr.modularity == modularity
    assert cr.methods == methods
    assert cr.hierarchical_levels == hierarchical_levels


def test_community_priors_empty_graph(empty_graph):
    with pytest.raises(ValueError, match="Graph must have at least one node"):
        CommunityPriors(empty_graph)


def test_community_priors_single_node(single_node_graph):
    cp = CommunityPriors(single_node_graph)
    assert cp.num_nodes == 1
    assert cp.num_edges == 0
    assert cp.degree_entropy == 0.0
    assert cp.clustering_coefs == [0.0]
    assert cp.clustering_std == 0.0
    assert cp.hierarchy_depth == 1


def test_community_priors_simple_graph(simple_graph):
    cp = CommunityPriors(simple_graph)
    assert cp.num_nodes == 6
    assert cp.num_edges == 7
    assert cp.degree_entropy >= 0.0
    assert len(cp.clustering_coefs) == 6
    assert cp.hierarchy_depth >= 1


@patch("transformers.AutoConfig.from_pretrained")
@patch("transformers.AutoModel.from_pretrained")
@pytest.fixture
def mock_sentence_transformer():
    """Fixture that mocks SentenceTransformer and its dependencies."""

    def mock_get_text_embeddings(texts, *args, **kwargs):
        return np.zeros((len(texts), 1))

    def mock_get_query_embedding(query, *args, **kwargs):
        return np.array([0.1, 0.2, 0.3])

    mock_model = Mock()
    mock_model.get_text_embeddings.side_effect = mock_get_text_embeddings
    mock_model.get_query_embedding.side_effect = mock_get_query_embedding

    with patch("nxlu.processing.community.SentenceTransformerEmbedding") as mock_st:
        mock_st.return_value = mock_model
        yield mock_st


def test_community_query_matcher_fit(mock_sentence_transformer, simple_graph):
    cqm = CommunityQueryMatcher(embedding_model_name="mock-model")

    with patch("nxlu.processing.community.get_communities") as mock_get_communities:
        mock_get_communities.return_value = ConsensusResult(
            communities=[{"A", "B"}, {"C", "D"}],
            modularity=0.5,
            methods=["LEIDEN"],
            hierarchical_levels=[[{"A", "B"}, {"C", "D"}]],
        )
        cqm.fit(simple_graph)

    assert len(cqm.community_embeddings) > 0


def test_community_query_matcher_transform(mock_sentence_transformer, simple_graph):
    cqm = CommunityQueryMatcher(embedding_model_name="mock-model")

    with patch("nxlu.processing.community.get_communities") as mock_get_communities:
        mock_get_communities.return_value = ConsensusResult(
            communities=[{"A", "B"}, {"C", "D"}],
            modularity=0.5,
            methods=["LEIDEN"],
            hierarchical_levels=[[{"A", "B"}, {"C", "D"}]],
        )
        cqm.fit(simple_graph)

    with patch(
        "nxlu.processing.community.cosine_similarity",
        return_value=np.array([[0.9, 0.8]]).T,
    ):
        results = cqm.transform("Test query", n_communities=2, min_similarity=0.5)

    assert len(results) == 2
    assert results[0][1] >= results[1][1]


def test_community_query_matcher_get_community_nodes(simple_graph):
    cqm = CommunityQueryMatcher()

    # Create a proper hierarchical structure
    hierarchical_levels = [
        [{"A", "B"}, {"C", "D"}],  # Level 0
        [{"A"}, {"B"}, {"C", "D"}],  # Level 1
    ]

    with patch("nxlu.processing.community.get_communities") as mock_get_communities:
        mock_get_communities.return_value = ConsensusResult(
            communities=[{"A", "B"}, {"C", "D"}],
            modularity=0.5,
            methods=["LEIDEN"],
            hierarchical_levels=hierarchical_levels,
        )
        cqm.fit(simple_graph)

        # Test level 0
        nodes = cqm.get_community_nodes((0, "community_0"))
        assert nodes == {"A", "B"}

        nodes = cqm.get_community_nodes((0, "community_1"))
        assert nodes == {"C", "D"}

        # Test level 1
        nodes = cqm.get_community_nodes((1, "community_0"))
        assert nodes == {"A"}

        nodes = cqm.get_community_nodes((1, "community_1"))
        assert nodes == {"B"}

        nodes = cqm.get_community_nodes((1, "community_2"))
        assert nodes == {"C", "D"}

        # Test invalid level
        with pytest.raises(IndexError):
            cqm.get_community_nodes((2, "community_0"))


# Tests for LeidenAlgorithm
def test_leiden_algorithm_invalid_graph():
    # Directed graph should raise ValueError
    G = nx.DiGraph()
    G.add_edge("A", "B")
    with pytest.raises(ValueError, match="Graph must be an undirected NetworkX graph"):
        LeidenAlgorithm(graph=G)


def test_leiden_algorithm_single_node(single_node_graph):
    la = LeidenAlgorithm(graph=single_node_graph)
    communities = la.find_communities(single_node_graph)

    assert communities == {"A": 0}


def test_leiden_algorithm_simple_graph(simple_graph):
    with patch("graspologic_native.hierarchical_leiden") as mock_hierarchical_leiden:
        # Mock to return a list of clusters with membership information
        mock_cluster = MagicMock()
        mock_cluster.membership = {
            "node_0": 0,
            "node_1": 0,
            "node_2": 0,
            "node_3": 1,
            "node_4": 1,
            "node_5": 1,
        }
        mock_hierarchical_leiden.return_value = [mock_cluster]

        la = LeidenAlgorithm(graph=simple_graph, seed=42)
        communities = la.find_communities(simple_graph)

        expected = {"A": 0, "B": 0, "C": 0, "D": 1, "E": 1, "F": 1}
        assert communities == expected


def test_leiden_algorithm_with_seed(simple_graph):
    with patch("graspologic_native.hierarchical_leiden") as mock_hierarchical_leiden:
        # Mock to return a list of clusters with membership information
        mock_cluster = MagicMock()
        mock_cluster.membership = {
            "node_0": 0,
            "node_1": 0,
            "node_2": 0,
            "node_3": 1,
            "node_4": 1,
            "node_5": 1,
        }
        mock_hierarchical_leiden.return_value = [mock_cluster]

        la = LeidenAlgorithm(graph=simple_graph, seed=123)
        communities = la.find_communities(simple_graph)

        assert la.seed == 123
        expected = {"A": 0, "B": 0, "C": 0, "D": 1, "E": 1, "F": 1}
        assert communities == expected


def test_leiden_algorithm_invalid_resolution(simple_graph):
    with pytest.raises(ValueError, match="resolution must be a positive float"):
        LeidenAlgorithm(graph=simple_graph, resolution=-1.0)


# Tests for leiden_communities function
def test_leiden_communities_simple_graph(simple_graph):
    with patch(
        "nxlu.processing.community.LeidenAlgorithm.find_communities"
    ) as mock_find_communities:
        mock_find_communities.return_value = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 1,
            "E": 1,
            "F": 1,
        }

        communities = leiden_communities(graph=simple_graph, seed=42)

        mock_find_communities.assert_called_once()
        assert communities == {"A": 0, "B": 0, "C": 0, "D": 1, "E": 1, "F": 1}


def test_empty_graph_community_detection(empty_graph):
    """Test handling of empty graphs."""
    with (
        patch("nxlu.processing.community.CommunityPriors") as mock_priors,
        patch("nxlu.processing.community.MultiResolutionDetector") as mock_detector,
    ):

        # Mock CommunityPriors
        mock_cp = MagicMock()
        mock_cp.compute_dynamic_resolutions.return_value = (1, np.array([1.0]))
        mock_priors.return_value = mock_cp

        # Mock detector
        mock_mrd = MagicMock()
        mock_mrd.detect_communities.return_value = ConsensusResult(
            communities=[], modularity=0.0, methods=["LEIDEN"], hierarchical_levels=[[]]
        )
        mock_detector.return_value = mock_mrd

        result = get_communities(graph=empty_graph)
        assert result.communities == []
        assert result.modularity == 0.0
        assert result.methods == ["LEIDEN"]
        assert result.hierarchical_levels == [[]]


def test_multi_resolution_detector_detect_communities(simple_graph):
    with patch("nxlu.processing.community.leiden_communities") as mock_leiden:
        # Mocking leiden_communities to return consistent community assignments
        mock_leiden.side_effect = [
            {"A": 0, "B": 0, "C": 0, "D": 1, "E": 1, "F": 1},  # Resolution 0.1
            {"A": 0, "B": 0, "C": 0, "D": 1, "E": 1, "F": 1},  # Resolution 0.8
            {"A": 0, "B": 0, "C": 0, "D": 1, "E": 1, "F": 1},  # Resolution 1.5
            {"A": 0, "B": 0, "C": 0, "D": 1, "E": 1, "F": 1},  # Final thorough run
        ]

        mrd = MultiResolutionDetector(
            graph=simple_graph,
            min_resolution=0.1,
            max_resolution=1.5,
            n_resolutions=3,
            random_state=42,
        )

        def mock_modularity(graph, communities, **kwargs):
            # Check if communities match our expected structure
            comm_sets = [set(c) for c in communities]
            if {"A", "B", "C"} in comm_sets and {"D", "E", "F"} in comm_sets:
                return 0.5
            return -0.1

        # Mock hierarchy generation to return consistent structure
        base_level = [{"A", "B", "C"}, {"D", "E", "F"}]

        with (
            patch("networkx.community.modularity", side_effect=mock_modularity),
            patch.object(mrd, "_recursive_greedy_modularity"),
            patch.object(mrd, "_generate_hierarchy", return_value=[base_level]),
        ):

            # Call detect_communities with min_size=1 to prevent merging
            consensus = mrd.detect_communities(min_size=1)

            # Check the structure of the resulting communities
            assert len(consensus.communities) == 2
            assert {"A", "B", "C"} in consensus.communities
            assert {"D", "E", "F"} in consensus.communities

            # Verify modularity score
            assert consensus.modularity == 0.5

            # Verify hierarchical structure
            assert len(consensus.hierarchical_levels) == 1
            assert consensus.hierarchical_levels[0] == [
                {"A", "B", "C"},
                {"D", "E", "F"},
            ]

            # Verify method
            assert consensus.methods == [CommunityMethod.LEIDEN]


def test_multi_resolution_detector_no_communities(simple_graph):
    with patch("nxlu.processing.community.leiden_communities") as mock_leiden:
        mock_leiden.return_value = {}

        mrd = MultiResolutionDetector(
            graph=simple_graph,
            min_resolution=0.1,
            max_resolution=1.5,
            n_resolutions=3,
            random_state=42,
        )

        with (
            patch("networkx.community.modularity", return_value=-1.0),
            patch.object(mrd, "_generate_hierarchy"),
        ):

            with pytest.raises(
                ValueError,
                match="No valid communities found after merging small communities",
            ):
                mrd.detect_communities()


def test_get_communities_simple_graph(simple_graph):
    with (
        patch("nxlu.processing.community.CommunityPriors") as mock_community_priors,
        patch("nxlu.processing.community.MultiResolutionDetector") as mock_mrd,
        patch("nxlu.processing.community.get_communities") as mock_get_communities,
    ):

        # Mock the CommunityPriors
        mock_cp = MagicMock()
        mock_cp.compute_dynamic_resolutions.return_value = (
            3,
            np.array([0.1, 0.8, 1.5]),
        )
        mock_community_priors.return_value = mock_cp

        # Mock the MultiResolutionDetector
        mock_detector = MagicMock()
        mock_detector.detect_communities.return_value = ConsensusResult(
            communities=[{"A", "B", "C"}, {"D", "E", "F"}],
            modularity=0.6,
            methods=["LEIDEN"],
            hierarchical_levels=[[{"A", "B", "C"}, {"D", "E", "F"}]],
        )
        mock_mrd.return_value = mock_detector

        result = get_communities(graph=simple_graph, methods=["LEIDEN"], seed=42)

        # Assertions
        mock_community_priors.assert_called_once_with(simple_graph)
        mock_cp.compute_dynamic_resolutions.assert_called_once()
        mock_mrd.assert_called_once()
        mock_detector.detect_communities.assert_called_once()

        assert result.communities == [{"A", "B", "C"}, {"D", "E", "F"}]
        assert result.modularity == 0.6
        assert result.methods == ["LEIDEN"]
        assert result.hierarchical_levels == [[{"A", "B", "C"}, {"D", "E", "F"}]]


def test_disconnected_graph_community_detection(disconnected_graph):
    with (
        patch("nxlu.processing.community.CommunityPriors") as mock_community_priors,
        patch("nxlu.processing.community.MultiResolutionDetector") as mock_mrd,
    ):

        mock_cp = MagicMock()
        mock_cp.compute_dynamic_resolutions.return_value = (2, np.array([0.1, 1.0]))
        mock_community_priors.return_value = mock_cp

        mock_detector = MagicMock()
        mock_detector.detect_communities.return_value = ConsensusResult(
            communities=[{"A", "B", "C"}, {"D", "E", "F"}],
            modularity=0.4,
            methods=["LEIDEN"],
            hierarchical_levels=[[{"A", "B", "C"}, {"D", "E", "F"}]],
        )
        mock_mrd.return_value = mock_detector

        result = get_communities(graph=disconnected_graph)

        assert result.communities == [{"A", "B", "C"}, {"D", "E", "F"}]
        assert result.modularity == 0.4
        assert result.methods == ["LEIDEN"]
        assert result.hierarchical_levels == [[{"A", "B", "C"}, {"D", "E", "F"}]]


def test_community_priors_multi_graph():
    # Create a MultiGraph
    G = nx.MultiGraph()
    G.add_edge("A", "B", weight=1.0)
    G.add_edge("A", "B", weight=2.0)
    G.add_edge("B", "C", weight=1.0)
    cp = CommunityPriors(G)

    # After conversion, the weight between A and B should be 3.0
    assert cp.graph.has_edge("A", "B")
    assert cp.graph["A"]["B"]["weight"] == 3.0
    assert cp.graph.has_edge("B", "C")
    assert cp.graph["B"]["C"]["weight"] == 1.0


def test_leiden_algorithm_with_isolated_nodes():
    G = nx.Graph()
    G.add_edges_from(
        [
            ("A", "B"),
            ("B", "C"),
        ]
    )
    G.add_node("D")  # Isolated node

    with patch("graspologic_native.hierarchical_leiden") as mock_hierarchical_leiden:
        mock_hierarchical_leiden.return_value = {"A": 0, "B": 0, "C": 0}

        la = LeidenAlgorithm(graph=G, seed=42)
        communities = la.find_communities(G)

        expected = {"A": 0, "B": 0, "C": 0, "D": -1}
        assert communities == expected


def test_community_query_matcher_transform_without_fit():
    cqm = CommunityQueryMatcher()
    with pytest.raises(
        ValueError, match="Must call fit\\(\\) before finding similar communities"
    ):
        cqm.transform("Test query")


def test_multi_resolution_detector_no_valid_communities(simple_graph):
    with patch(
        "nxlu.processing.community.leiden_communities"
    ) as mock_leiden_communities:
        mock_leiden_communities.return_value = {}

        mrd = MultiResolutionDetector(
            graph=simple_graph,
            min_resolution=0.1,
            max_resolution=1.5,
            n_resolutions=3,
            methods=["LEIDEN"],
            random_state=42,
        )

        with patch("networkx.community.modularity", return_value=-1.0):
            with pytest.raises(
                ValueError,
                match="No valid communities found after merging small communities",
            ):
                mrd.detect_communities()

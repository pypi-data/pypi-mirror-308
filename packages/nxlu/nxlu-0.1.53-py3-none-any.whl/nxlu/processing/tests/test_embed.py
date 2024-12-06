from unittest.mock import patch

import pytest
import torch
from torch import nn

from nxlu.processing.embed import CustomModel


@pytest.fixture
def mock_transformer_model():
    with patch("nxlu.processing.embed.AutoModel") as MockAutoModel:
        mock_model = MockAutoModel.from_pretrained.return_value
        mock_model.config.hidden_size = 768
        yield MockAutoModel


def test_custom_model_initialization(mock_transformer_model):
    config = {
        "base_model": "bert-base-uncased",
        "fc_dropout": 0.3,
        "id2label": {0: "negative", 1: "positive"},
    }
    model = CustomModel(config)

    # Check if the base transformer model is loaded correctly
    mock_transformer_model.from_pretrained.assert_called_with("bert-base-uncased")
    assert isinstance(model.dropout, nn.Dropout)
    assert isinstance(model.fc, nn.Linear)
    assert model.fc.out_features == 2


def test_custom_model_forward(mock_transformer_model):
    config = {
        "base_model": "bert-base-uncased",
        "fc_dropout": 0.3,
        "id2label": {0: "negative", 1: "positive"},
    }
    model = CustomModel(config)

    # Create dummy input tensors
    input_ids = torch.randint(0, 1000, (2, 10))
    attention_mask = torch.ones((2, 10))

    # Mock the transformer model's output
    mtmfprv = mock_transformer_model.from_pretrained.return_value
    mtmfprv.return_value.last_hidden_state = torch.randn(2, 10, 768)

    output = model(input_ids, attention_mask)

    assert output.shape == (2, 2)
    assert torch.allclose(output.sum(dim=1), torch.ones(2))

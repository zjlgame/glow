from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import torch
import torch.nn.functional as F
from tests import utils


class SimpleLogSoftmaxModel(torch.nn.Module):
    def __init__(self, dimension):
        super(SimpleLogSoftmaxModel, self).__init__()
        self.dimension = dimension

    def forward(self, tensor):
        return F.log_softmax(tensor, self.dimension)


class TestLogSoftmax(utils.TorchGlowTestCase):
    @utils.deterministic_expand(
        [
            lambda: (-2, [2, 3]),
            lambda: (-1, [2, 3]),
            lambda: (0, [2, 3]),
            lambda: (1, [2, 3]),
            lambda: (-3, [2, 3, 4]),
            lambda: (-2, [2, 3, 4]),
            lambda: (-1, [2, 3, 4]),
            lambda: (0, [2, 3, 4]),
            lambda: (1, [2, 3, 4]),
            lambda: (2, [2, 3, 4]),
        ]
    )
    def test_log_softmax(self, dim, input_dims):
        module = SimpleLogSoftmaxModel(dim)
        input = torch.randn(input_dims)
        utils.compare_tracing_methods(module, input, fusible_ops={"aten::log_softmax"})

    def test_log_softmax_oob_neg_dim(self):
        """Test out of bounds negative dimension index for the PyTorch LogSoftMax Node on Glow."""

        with self.assertRaises(IndexError):
            utils.compare_tracing_methods(
                SimpleLogSoftmaxModel(-3),
                torch.randn(2, 3),
                fusible_ops={"aten::log_softmax"},
            )

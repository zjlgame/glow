from __future__ import absolute_import, division, print_function, unicode_literals

import torch
import torch.nn.functional as F
from tests import utils


class SimpleLinearModule(torch.nn.Module):
    def __init__(self):
        super(SimpleLinearModule, self).__init__()

    def forward(self, input, weight, bias=None):
        return F.linear((input + input), weight, bias)


class TestLinear(utils.TorchGlowTestCase):
    def test_linear_basic(self):
        """Basic test of the PyTorch aten::linear op on Glow."""

        def test_f(input, weight, bias=None):
            return F.linear((input + input), weight, bias)

        n = 5
        in_features = 4
        out_features = 3

        input = torch.randn(n, in_features)
        weight = torch.randn(out_features, in_features)

        utils.compare_tracing_methods(
            SimpleLinearModule(), input, weight, fusible_ops={"aten::linear"}
        )

    def test_linear_bias(self):
        """Test of the PyTorch aten::linear op on Glow."""

        def test_f(input, weight, bias=None):
            return F.linear((input + input), weight, bias)

        n = 5
        in_features = 4
        out_features = 3

        input = torch.randn(n, in_features)
        weight = torch.randn(out_features, in_features)
        bias = torch.randn(out_features)

        utils.compare_tracing_methods(
            SimpleLinearModule(), input, weight, bias, fusible_ops={"aten::linear"}
        )

    def test_linear_broadcast(self):
        """Test of the PyTorch aten::linear op with broadcasting on Glow."""

        def test_f(input, weight, bias=None):
            return F.linear((input + input), weight, bias)

        n = 5
        in_features = 4
        out_features = 3

        input = torch.randn(n, 9, 7, in_features)
        weight = torch.randn(out_features, in_features)

        utils.compare_tracing_methods(
            SimpleLinearModule(), input, weight, fusible_ops={"aten::linear"}
        )

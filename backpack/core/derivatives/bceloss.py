"""NLL extention for BCEWithLogits Loss."""
from typing import List, Tuple

from torch import Tensor, sigmoid
from torch.distributions import Binomial
from torch.nn import BCEWithLogitsLoss

from backpack.core.derivatives.nll_base import NLLLossDerivatives


class BCELossDerivatives(NLLLossDerivatives):
    """Derivatives of the BCEWithLogits Loss."""

    def __init__(self, use_autograd: bool = True):
        """Initialization for BCEWithLogits loss derivative.

        Args:
            use_autograd: Compute gradients with autograd (rather than manual)
                Defaults to ``False`` (manual computation).
        """
        super().__init__(use_autograd=use_autograd)

    def _verify_support(self, module: BCEWithLogitsLoss):
        """Verification of module support for BCEWithLogitsLoss.

        Currently BCEWithLogitsLoss only supports binary target tensors,
        2D inputs, and default parameters.

        Args:
            module: BCEWithLogitsLoss module
        """
        self._check_binary(module)
        self._check_is_default(module)
        self._check_input_dims(module)

    def _check_binary(self, module: BCEWithLogitsLoss):
        """Raises exception if labels are not binary.

        Args:
            module: BCEWithLogitsLoss module

        Raises:
            NotImplementedError: if labels are non-binary.
        """
        if any(x != 0 and x != 1 for x in module.input1.flatten()):
            raise NotImplementedError(
                "Only binary targets (0 and 1) are currently supported."
            )

    def _check_is_default(self, module: BCEWithLogitsLoss):
        """Raises exception if module parameters are not default.

        Args:
            module: BCEWithLogitsLoss module

        Raises:
            NotImplementedError: if module parameters non-default.
        """
        if module.weight is not None:
            raise NotImplementedError("Only None weight is currently supported.")
        if module.reduction != "mean":
            raise NotImplementedError("Only mean reduction is currently supported.")
        if module.pos_weight is not None:
            raise NotImplementedError("Only None pos_weight is currently supported.")

    def _check_input_dims(self, module: BCEWithLogitsLoss):
        """Raises an exception if the shapes of the input are not supported.

        Args:
            module: BCEWithLogitsLoss module

        Raises:
            NotImplementedError: if input is not 2D.
        """
        if module.input0.dim() != 2:
            raise NotImplementedError("Only 2D inputs are currently supported.")

    def _make_distribution(self, subsampled_input: Tensor):
        """Make the sampling distribution for the NLL loss form of BCEWithLogits.

        The BCEWithLogitsLoss ∝ ∑ᵢ₌₁ⁿ Yᵢ log 𝜎(xᵢ) + (1 − Yᵢ) log(1− 𝜎(xᵢ)).
        The log likelihood of the Binomial distribution is
        Yᵢ log p(xᵢ) + (1 − Yᵢ) log(1 − p(xᵢ)), so these are equivalent if
        p(xᵢ) = 𝜎(xᵢ).

        Args:
            subsampled_input: input after subsampling

        Returns:
            torch.distributions Binomial distribution with probabilities equal to
                the sigmoid of subsampled_input.
        """
        return Binomial(probs=sigmoid(subsampled_input))

    @staticmethod
    def _get_mean_normalization(input: Tensor) -> int:
        return input.shape[0]

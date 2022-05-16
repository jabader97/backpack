"""Contains util function for classification of modules."""
from torch.fx import GraphModule
from torch.nn import Module, Sequential
from torch.nn.modules.loss import BCEWithLogitsLoss, CrossEntropyLoss, _Loss

from backpack.core.derivatives.mseloss import MSELoss
from backpack.custom_module.branching import Parallel, _Branch
from backpack.custom_module.reduce_tuple import ReduceTuple


def is_loss(module: Module) -> bool:
    """Return whether `module` is a `torch` loss function.

    Args:
        module: A PyTorch module.

    Returns:
        Whether `module` is a loss function.
    """
    return isinstance(module, _Loss)


def is_mse(module: Module) -> bool:
    """Return whether 'module' is a MSELoss function.

    Args:
        module: A PyTorch module.

    Returns:
        Whether 'module' is an MSE loss function
    """
    return isinstance(module, MSELoss)


def is_bce(module: Module) -> bool:
    """Return whether 'module' is a BCEWithLogitsLoss function.

    Args:
        module: A PyTorch module.

    Returns:
        Whether 'module' is a BCEWithLogitsLoss function
    """
    return isinstance(module, BCEWithLogitsLoss)


def is_ce(module: Module) -> bool:
    """Return whether 'module' is a CrossEntropyLoss function.

    Args:
        module: A PyTorch module.

    Returns:
        Whether 'module' is a CrossEntropyLoss function
    """
    return isinstance(module, CrossEntropyLoss)


def is_no_op(module: Module) -> bool:
    """Return whether the module does no operation in graph.

    Args:
        module: module

    Returns:
        whether module is no operation
    """
    no_op_modules = (Sequential, _Branch, Parallel, ReduceTuple, GraphModule)
    return isinstance(module, no_op_modules)

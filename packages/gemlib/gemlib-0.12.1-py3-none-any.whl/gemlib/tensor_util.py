"""Tensor utilities"""

from functools import reduce as ft_reduce

import tensorflow as tf

__all__ = ["broadcast_fn", "broadcast_together"]


def broadcast_together(*tensors):
    """Broadcast tensors together

    Args:
      *tensors: tensors

    Returns:
      a tuple of tensors broadcast to have common shape
    """
    shapes = [tf.shape(x) for x in tensors]

    common_shape = ft_reduce(
        lambda a, x: tf.broadcast_dynamic_shape(a, x), shapes
    )
    broadcast_tensors = [tf.broadcast_to(x, common_shape) for x in tensors]

    if len(tensors) == 1:
        return broadcast_tensors[0]

    return tuple(broadcast_tensors)


def broadcast_fn(func):
    """Transform function `func` such that its outputs broadcast together"""

    def wrapped(*args, **kwargs):
        return broadcast_together(*func(*args, **kwargs))

    return wrapped

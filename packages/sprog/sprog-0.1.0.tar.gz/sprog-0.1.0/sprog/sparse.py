"""Utilities to implement pandas API with Yale sparse matrices."""

# ruff: noqa: S101

from collections.abc import Sequence
from numbers import Integral

import numpy as np
from scipy import sparse


def scatter(indices: Sequence[Integral], m: int = -1, n: int = -1) -> sparse.csr_array:
    """Scatter consecutive indices of x into (larger) result vector y.

    Args:
        indices: subset of range to populate (rest will be 0)
        m: length of range (defaults to :code:`max(indices) + 1`)
        n: length of domain (defaults to :code:`len(indices)`)

    Returns:
        sparse array in CSR format

    Roughly equivalent to::

        for i, j in enumerate(indices):
            y[j] = x[i]

    >>> scatter([1, 3]) @ [6, 7]
    array([0., 6., 0., 7.])

    """
    if m < 0:
        m = max(indices) + 1
    if n < 0:
        n = len(indices)
    assert m >= max(indices) + 1
    assert n >= len(indices)
    assert m >= n
    return sparse.csr_array(
        (np.ones(shape=len(indices)), (indices, range(len(indices)))),
        shape=(m, n),
    )


def gather(indices: Sequence[Integral], n: int = -1) -> sparse.csr_array:
    """Gather subset of x into (smaller) consecutive result vector y.

    Args:
        indices: subset of domain to select
        n: length of domain (defaults to :code:`max(indices) + 1`)

    Returns:
        sparse array in CSR format

    Roughly equivalent to::

        for i, j in enumerate(indices):
            y[i] = y[j]

    >>> gather([1, 3]) @ [4, 5, 6, 7]
    array([5., 7.])

    """
    m = len(indices)
    if n < 0:
        n = max(indices) + 1
    assert n >= max(indices) + 1
    return sparse.csr_array(
        (np.ones(shape=len(indices)), indices, range(len(indices) + 1)),
        shape=(m, n),
    )

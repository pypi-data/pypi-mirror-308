from __future__ import annotations

from ._dtypes import (
    _boolean_dtypes,
    _floating_dtypes,
    _real_floating_dtypes,
    _complex_floating_dtypes,
    _integer_dtypes,
    _integer_or_boolean_dtypes,
    _real_numeric_dtypes,
    _numeric_dtypes,
    _result_type,
)
from ._array_object import Array
from ._flags import requires_api_version
from ._creation_functions import asarray
from ._data_type_functions import broadcast_to, iinfo

from typing import Optional, Union

import numpy as np


def abs(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.abs <numpy.abs>`.

    See its docstring for more information.
    """
    if x.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in abs")
    return Array._new(np.abs(x._array), device=x.device)


# Note: the function name is different here
def acos(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.arccos <numpy.arccos>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in acos")
    return Array._new(np.arccos(x._array), device=x.device)


# Note: the function name is different here
def acosh(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.arccosh <numpy.arccosh>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in acosh")
    return Array._new(np.arccosh(x._array), device=x.device)


def add(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.add <numpy.add>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")

    if x1.dtype not in _numeric_dtypes or x2.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in add")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.add(x1._array, x2._array), device=x1.device)


# Note: the function name is different here
def asin(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.arcsin <numpy.arcsin>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in asin")
    return Array._new(np.arcsin(x._array), device=x.device)


# Note: the function name is different here
def asinh(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.arcsinh <numpy.arcsinh>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in asinh")
    return Array._new(np.arcsinh(x._array), device=x.device)


# Note: the function name is different here
def atan(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.arctan <numpy.arctan>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in atan")
    return Array._new(np.arctan(x._array), device=x.device)


# Note: the function name is different here
def atan2(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.arctan2 <numpy.arctan2>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_floating_dtypes or x2.dtype not in _real_floating_dtypes:
        raise TypeError("Only real floating-point dtypes are allowed in atan2")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.arctan2(x1._array, x2._array), device=x1.device)


# Note: the function name is different here
def atanh(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.arctanh <numpy.arctanh>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in atanh")
    return Array._new(np.arctanh(x._array), device=x.device)


def bitwise_and(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.bitwise_and <numpy.bitwise_and>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")

    if (
        x1.dtype not in _integer_or_boolean_dtypes
        or x2.dtype not in _integer_or_boolean_dtypes
    ):
        raise TypeError("Only integer or boolean dtypes are allowed in bitwise_and")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.bitwise_and(x1._array, x2._array), device=x1.device)


# Note: the function name is different here
def bitwise_left_shift(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.left_shift <numpy.left_shift>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")

    if x1.dtype not in _integer_dtypes or x2.dtype not in _integer_dtypes:
        raise TypeError("Only integer dtypes are allowed in bitwise_left_shift")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    # Note: bitwise_left_shift is only defined for x2 nonnegative.
    if np.any(x2._array < 0):
        raise ValueError("bitwise_left_shift(x1, x2) is only defined for x2 >= 0")
    return Array._new(np.left_shift(x1._array, x2._array), device=x1.device)


# Note: the function name is different here
def bitwise_invert(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.invert <numpy.invert>`.

    See its docstring for more information.
    """
    if x.dtype not in _integer_or_boolean_dtypes:
        raise TypeError("Only integer or boolean dtypes are allowed in bitwise_invert")
    return Array._new(np.invert(x._array), device=x.device)


def bitwise_or(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.bitwise_or <numpy.bitwise_or>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")

    if (
        x1.dtype not in _integer_or_boolean_dtypes
        or x2.dtype not in _integer_or_boolean_dtypes
    ):
        raise TypeError("Only integer or boolean dtypes are allowed in bitwise_or")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.bitwise_or(x1._array, x2._array), device=x1.device)


# Note: the function name is different here
def bitwise_right_shift(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.right_shift <numpy.right_shift>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")

    if x1.dtype not in _integer_dtypes or x2.dtype not in _integer_dtypes:
        raise TypeError("Only integer dtypes are allowed in bitwise_right_shift")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    # Note: bitwise_right_shift is only defined for x2 nonnegative.
    if np.any(x2._array < 0):
        raise ValueError("bitwise_right_shift(x1, x2) is only defined for x2 >= 0")
    return Array._new(np.right_shift(x1._array, x2._array), device=x1.device)


def bitwise_xor(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.bitwise_xor <numpy.bitwise_xor>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")

    if (
        x1.dtype not in _integer_or_boolean_dtypes
        or x2.dtype not in _integer_or_boolean_dtypes
    ):
        raise TypeError("Only integer or boolean dtypes are allowed in bitwise_xor")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.bitwise_xor(x1._array, x2._array), device=x1.device)


def ceil(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.ceil <numpy.ceil>`.

    See its docstring for more information.
    """
    if x.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in ceil")
    if x.dtype in _integer_dtypes:
        # Note: The return dtype of ceil is the same as the input
        return x
    return Array._new(np.ceil(x._array), device=x.device)

# WARNING: This function is not yet tested by the array-api-tests test suite.

# Note: min and max argument names are different and not optional in numpy.
@requires_api_version('2023.12')
def clip(
    x: Array,
    /,
    min: Optional[Union[int, float, Array]] = None,
    max: Optional[Union[int, float, Array]] = None,
) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.clip <numpy.clip>`.

    See its docstring for more information.
    """
    if isinstance(min, Array) and x.device != min.device:
        raise ValueError(f"Arrays from two different devices ({x.device} and {min.device}) can not be combined.")
    if isinstance(max, Array) and x.device != max.device:
        raise ValueError(f"Arrays from two different devices ({x.device} and {max.device}) can not be combined.")

    if (x.dtype not in _real_numeric_dtypes
        or isinstance(min, Array) and min.dtype not in _real_numeric_dtypes
        or isinstance(max, Array) and max.dtype not in _real_numeric_dtypes):
        raise TypeError("Only real numeric dtypes are allowed in clip")
    if not isinstance(min, (int, float, Array, type(None))):
        raise TypeError("min must be an None, int, float, or an array")
    if not isinstance(max, (int, float, Array, type(None))):
        raise TypeError("max must be an None, int, float, or an array")

    # Mixed dtype kinds is implementation defined
    if (x.dtype in _integer_dtypes
        and (isinstance(min, float) or
             isinstance(min, Array) and min.dtype in _real_floating_dtypes)):
        raise TypeError("min must be integral when x is integral")
    if (x.dtype in _integer_dtypes
        and (isinstance(max, float) or
             isinstance(max, Array) and max.dtype in _real_floating_dtypes)):
        raise TypeError("max must be integral when x is integral")
    if (x.dtype in _real_floating_dtypes
        and (isinstance(min, int) or
             isinstance(min, Array) and min.dtype in _integer_dtypes)):
        raise TypeError("min must be floating-point when x is floating-point")
    if (x.dtype in _real_floating_dtypes
        and (isinstance(max, int) or
             isinstance(max, Array) and max.dtype in _integer_dtypes)):
        raise TypeError("max must be floating-point when x is floating-point")

    if min is max is None:
        # Note: NumPy disallows min = max = None
        return x

    # Normalize to make the below logic simpler
    if min is not None:
        min = asarray(min)._array
    if max is not None:
        max = asarray(max)._array

    # min > max is implementation defined
    if min is not None and max is not None and np.any(min > max):
        raise ValueError("min must be less than or equal to max")

    # np.clip does type promotion but the array API clip requires that the
    # output have the same dtype as x. We do this instead of just downcasting
    # the result of xp.clip() to handle some corner cases better (e.g.,
    # avoiding uint64 -> float64 promotion).

    # Note: cases where min or max overflow (integer) or round (float) in the
    # wrong direction when downcasting to x.dtype are unspecified. This code
    # just does whatever NumPy does when it downcasts in the assignment, but
    # other behavior could be preferred, especially for integers. For example,
    # this code produces:

    # >>> clip(asarray(0, dtype=int8), asarray(128, dtype=int16), None)
    # -128

    # but an answer of 0 might be preferred. See
    # https://github.com/numpy/numpy/issues/24976 for more discussion on this issue.

    # At least handle the case of Python integers correctly (see
    # https://github.com/numpy/numpy/pull/26892).
    if type(min) is int and min <= iinfo(x.dtype).min:
        min = None
    if type(max) is int and max >= iinfo(x.dtype).max:
        max = None

    def _isscalar(a):
        return isinstance(a, (int, float, type(None)))
    min_shape = () if _isscalar(min) else min.shape
    max_shape = () if _isscalar(max) else max.shape

    result_shape = np.broadcast_shapes(x.shape, min_shape, max_shape)

    out = asarray(broadcast_to(x, result_shape), copy=True)._array
    device = x.device
    x = x._array

    if min is not None:
        a = np.broadcast_to(np.asarray(min), result_shape)
        ia = (out < a) | np.isnan(a)

        out[ia] = a[ia]
    if max is not None:
        b = np.broadcast_to(np.asarray(max), result_shape)
        ib = (out > b) | np.isnan(b)
        out[ib] = b[ib]
    return Array._new(out, device=device)

def conj(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.conj <numpy.conj>`.

    See its docstring for more information.
    """
    if x.dtype not in _complex_floating_dtypes:
        raise TypeError("Only complex floating-point dtypes are allowed in conj")
    return Array._new(np.conj(x._array), device=x.device)

@requires_api_version('2023.12')
def copysign(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.copysign <numpy.copysign>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")

    if x1.dtype not in _real_floating_dtypes or x2.dtype not in _real_floating_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in copysign")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.copysign(x1._array, x2._array), device=x1.device)

def cos(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.cos <numpy.cos>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in cos")
    return Array._new(np.cos(x._array), device=x.device)


def cosh(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.cosh <numpy.cosh>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in cosh")
    return Array._new(np.cosh(x._array), device=x.device)


def divide(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.divide <numpy.divide>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _floating_dtypes or x2.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in divide")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.divide(x1._array, x2._array), device=x1.device)


def equal(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.equal <numpy.equal>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.equal(x1._array, x2._array), device=x1.device)


def exp(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.exp <numpy.exp>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in exp")
    return Array._new(np.exp(x._array), device=x.device)


def expm1(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.expm1 <numpy.expm1>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in expm1")
    return Array._new(np.expm1(x._array), device=x.device)


def floor(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.floor <numpy.floor>`.

    See its docstring for more information.
    """
    if x.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in floor")
    if x.dtype in _integer_dtypes:
        # Note: The return dtype of floor is the same as the input
        return x
    return Array._new(np.floor(x._array), device=x.device)


def floor_divide(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.floor_divide <numpy.floor_divide>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_numeric_dtypes or x2.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in floor_divide")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.floor_divide(x1._array, x2._array), device=x1.device)


def greater(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.greater <numpy.greater>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_numeric_dtypes or x2.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in greater")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.greater(x1._array, x2._array), device=x1.device)


def greater_equal(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.greater_equal <numpy.greater_equal>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_numeric_dtypes or x2.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in greater_equal")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.greater_equal(x1._array, x2._array), device=x1.device)

@requires_api_version('2023.12')
def hypot(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.hypot <numpy.hypot>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_floating_dtypes or x2.dtype not in _real_floating_dtypes:
        raise TypeError("Only real floating-point dtypes are allowed in hypot")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.hypot(x1._array, x2._array), device=x1.device)

def imag(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.imag <numpy.imag>`.

    See its docstring for more information.
    """
    if x.dtype not in _complex_floating_dtypes:
        raise TypeError("Only complex floating-point dtypes are allowed in imag")
    return Array._new(np.imag(x._array), device=x.device)


def isfinite(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.isfinite <numpy.isfinite>`.

    See its docstring for more information.
    """
    if x.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in isfinite")
    return Array._new(np.isfinite(x._array), device=x.device)


def isinf(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.isinf <numpy.isinf>`.

    See its docstring for more information.
    """
    if x.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in isinf")
    return Array._new(np.isinf(x._array), device=x.device)


def isnan(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.isnan <numpy.isnan>`.

    See its docstring for more information.
    """
    if x.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in isnan")
    return Array._new(np.isnan(x._array), device=x.device)


def less(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.less <numpy.less>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_numeric_dtypes or x2.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in less")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.less(x1._array, x2._array), device=x1.device)


def less_equal(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.less_equal <numpy.less_equal>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_numeric_dtypes or x2.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in less_equal")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.less_equal(x1._array, x2._array), device=x1.device)


def log(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.log <numpy.log>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in log")
    return Array._new(np.log(x._array), device=x.device)


def log1p(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.log1p <numpy.log1p>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in log1p")
    return Array._new(np.log1p(x._array), device=x.device)


def log2(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.log2 <numpy.log2>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in log2")
    return Array._new(np.log2(x._array), device=x.device)


def log10(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.log10 <numpy.log10>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in log10")
    return Array._new(np.log10(x._array), device=x.device)


def logaddexp(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.logaddexp <numpy.logaddexp>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_floating_dtypes or x2.dtype not in _real_floating_dtypes:
        raise TypeError("Only real floating-point dtypes are allowed in logaddexp")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.logaddexp(x1._array, x2._array), device=x1.device)


def logical_and(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.logical_and <numpy.logical_and>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _boolean_dtypes or x2.dtype not in _boolean_dtypes:
        raise TypeError("Only boolean dtypes are allowed in logical_and")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.logical_and(x1._array, x2._array), device=x1.device)


def logical_not(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.logical_not <numpy.logical_not>`.

    See its docstring for more information.
    """
    if x.dtype not in _boolean_dtypes:
        raise TypeError("Only boolean dtypes are allowed in logical_not")
    return Array._new(np.logical_not(x._array), device=x.device)


def logical_or(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.logical_or <numpy.logical_or>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _boolean_dtypes or x2.dtype not in _boolean_dtypes:
        raise TypeError("Only boolean dtypes are allowed in logical_or")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.logical_or(x1._array, x2._array), device=x1.device)


def logical_xor(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.logical_xor <numpy.logical_xor>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _boolean_dtypes or x2.dtype not in _boolean_dtypes:
        raise TypeError("Only boolean dtypes are allowed in logical_xor")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.logical_xor(x1._array, x2._array), device=x1.device)

@requires_api_version('2023.12')
def maximum(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.maximum <numpy.maximum>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_numeric_dtypes or x2.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in maximum")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    # TODO: maximum(-0., 0.) is unspecified. Should we issue a warning/error
    # in that case?
    return Array._new(np.maximum(x1._array, x2._array), device=x1.device)

@requires_api_version('2023.12')
def minimum(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.minimum <numpy.minimum>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_numeric_dtypes or x2.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in minimum")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.minimum(x1._array, x2._array), device=x1.device)

def multiply(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.multiply <numpy.multiply>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _numeric_dtypes or x2.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in multiply")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.multiply(x1._array, x2._array), device=x1.device)


def negative(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.negative <numpy.negative>`.

    See its docstring for more information.
    """
    if x.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in negative")
    return Array._new(np.negative(x._array), device=x.device)


@requires_api_version('2024.12')
def nextafter(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.nextafter <numpy.nextafter>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_floating_dtypes or x2.dtype not in _real_floating_dtypes:
        raise TypeError("Only real floating-point dtypes are allowed in nextafter")
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.nextafter(x1._array, x2._array), device=x1.device)

def not_equal(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.not_equal <numpy.not_equal>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.not_equal(x1._array, x2._array), device=x1.device)


def positive(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.positive <numpy.positive>`.

    See its docstring for more information.
    """
    if x.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in positive")
    return Array._new(np.positive(x._array), device=x.device)


# Note: the function name is different here
def pow(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.power <numpy.power>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _numeric_dtypes or x2.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in pow")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.power(x1._array, x2._array), device=x1.device)


def real(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.real <numpy.real>`.

    See its docstring for more information.
    """
    if x.dtype not in _complex_floating_dtypes:
        raise TypeError("Only complex floating-point dtypes are allowed in real")
    return Array._new(np.real(x._array), device=x.device)


@requires_api_version('2024.12')
def reciprocal(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.reciprocal <numpy.reciprocal>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in reciprocal")
    return Array._new(np.reciprocal(x._array), device=x.device)

def remainder(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.remainder <numpy.remainder>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _real_numeric_dtypes or x2.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in remainder")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.remainder(x1._array, x2._array), device=x1.device)


def round(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.round <numpy.round>`.

    See its docstring for more information.
    """
    if x.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in round")
    return Array._new(np.round(x._array), device=x.device)


def sign(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.sign <numpy.sign>`.

    See its docstring for more information.
    """
    if x.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in sign")
    if x.dtype in _complex_floating_dtypes:
        return x/abs(x)
    return Array._new(np.sign(x._array), device=x.device)


@requires_api_version('2023.12')
def signbit(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.signbit <numpy.signbit>`.

    See its docstring for more information.
    """
    if x.dtype not in _real_floating_dtypes:
        raise TypeError("Only real floating-point dtypes are allowed in signbit")
    return Array._new(np.signbit(x._array), device=x.device)


def sin(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.sin <numpy.sin>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in sin")
    return Array._new(np.sin(x._array), device=x.device)


def sinh(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.sinh <numpy.sinh>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in sinh")
    return Array._new(np.sinh(x._array), device=x.device)


def square(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.square <numpy.square>`.

    See its docstring for more information.
    """
    if x.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in square")
    return Array._new(np.square(x._array), device=x.device)


def sqrt(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.sqrt <numpy.sqrt>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in sqrt")
    return Array._new(np.sqrt(x._array), device=x.device)


def subtract(x1: Array, x2: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.subtract <numpy.subtract>`.

    See its docstring for more information.
    """
    if x1.device != x2.device:
        raise ValueError(f"Arrays from two different devices ({x1.device} and {x2.device}) can not be combined.")
    if x1.dtype not in _numeric_dtypes or x2.dtype not in _numeric_dtypes:
        raise TypeError("Only numeric dtypes are allowed in subtract")
    # Call result type here just to raise on disallowed type combinations
    _result_type(x1.dtype, x2.dtype)
    x1, x2 = Array._normalize_two_args(x1, x2)
    return Array._new(np.subtract(x1._array, x2._array), device=x1.device)


def tan(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.tan <numpy.tan>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in tan")
    return Array._new(np.tan(x._array), device=x.device)


def tanh(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.tanh <numpy.tanh>`.

    See its docstring for more information.
    """
    if x.dtype not in _floating_dtypes:
        raise TypeError("Only floating-point dtypes are allowed in tanh")
    return Array._new(np.tanh(x._array), device=x.device)


def trunc(x: Array, /) -> Array:
    """
    Array API compatible wrapper for :py:func:`np.trunc <numpy.trunc>`.

    See its docstring for more information.
    """
    if x.dtype not in _real_numeric_dtypes:
        raise TypeError("Only real numeric dtypes are allowed in trunc")
    if x.dtype in _integer_dtypes:
        # Note: The return dtype of trunc is the same as the input
        return x
    return Array._new(np.trunc(x._array), device=x.device)

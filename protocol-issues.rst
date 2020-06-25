=======================================================
Issues with runtime checkable protocols from ``typing``
=======================================================

Abstract
========

In the ``typing`` module, the protocols ``SupportsInt``, ``SupportsFloat``, and ``SupportsComplex`` are decorated with ``@runtime_checkable``. However, at runtime they produce false negatives, false positives, and inconsistent results when used to check built-in numeric types and equivalent NumPy numeric types.

Setup
=====

Verify the Python version::

    >>> import sys
    >>> sys.version_info[:2]
    (3, 8)

To make this file runnable with ``doctest``, we start with some imports::

    >>> import numpy as np
    >>> from typing import SupportsComplex, SupportsFloat, SupportsInt
    
And some sample numbers::

    >>> type(1+0j), type(np.complex64(1+0j))
    (<class 'complex'>, <class 'numpy.complex64'>)
    >>> 1+0j, np.complex64(1+0j)
    ((1+0j), (1+0j))

Issues with ``SupportsInt``
===========================

Issue #1
--------

``SupportsInt`` checks whether the type implements ``__int__``,
but that does not mean you can convert to ``int``.

Can I convert a complex number to an ``int``? This suggests yes::

    >>> isinstance(1+0j, SupportsInt), isinstance(np.complex64(1+0j), SupportsInt)
    (True, True)
    
But actually, only a NumPy complex can be converted to an ``int``::

    >>> int(np.complex64(1+0j))
    1
    
The code above "works" but you get a warning about converting to "real"::

    ComplexWarning: Casting complex values to real discards the imaginary part

Trying the same with a Python built-in ``complex`` raises ``TypeError``::

    >>> int(1+0j)
    Traceback (most recent call last):
      ...
    TypeError: can't convert complex to int
    
In the typing-sig mailing list, Guido explained that the built-in ``complex`` implements ``__int__`` only to provide a better error message.

    >>> complex.__int__
    <slot wrapper '__int__' of 'complex' objects>
    
Issue #2
--------

While type checking, Mypy says a built-in ``complex`` is inconsistent with ``SupportsInt``, but at runtime, the same ``complex`` passes an ``isinstance`` check with ``SupportsInt``.

On typeshed, there is no method ``__int__`` in ``complex``. Mypy complains that ``complex`` is inconsistent with ``SupportsInt``::

    demo.py:16: error: Argument 1 to "to_int" has incompatible type "complex"; expected "SupportsInt"


Issues with ``SupportsFloat``
=============================

Issue #3
--------

**(Similar to #1)**
``isinstance(c, SupportsFloat)`` returns ``True`` for both complex types,
but only the NumPy complex can actually be converted to ``float``::

    >>> isinstance(1+0j, SupportsFloat), isinstance(np.complex64(1+0j), SupportsFloat)
    (True, True)
    >>> float(np.complex64(1+0j))
    1.0
    >>> float(1+0j)
    Traceback (most recent call last):
      ...
    TypeError: can't convert complex to float

In the typing-sig mailing list, Guido explained that the built-in ``complex`` implements ``__float__`` only to provide a better error message.

Issue #4
--------

**(Similar to #2)** While type checking, Mypy says a built-in ``complex`` is inconsistent with ``SupportsFloat``, but at runtime, the same ``complex`` passes an ``isinstance`` check with ``SupportsFloat``.

On typeshed, there is no method ``__float__`` in ``complex``. Mypy complains that ``complex`` is inconsistent with ``SupportsFloat``::

    demo.py:23: error: Argument 1 to "to_float" has incompatible type "complex"; expected "SupportsFloat"


Issue with ``SupportsComplex``
==============================

Please see `<SupportsComplex_issue.rst>`_

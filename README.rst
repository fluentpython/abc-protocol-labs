=================
abc-prococol-labs
=================

Experiments with Python Abstract Base Classes and runtime checkable Protocols.

To make this file runnable with ``doctest``, we start with some imports::

    >>> import numpy
    >>> from typing import SupportsComplex, SupportsFloat, SupportsInt
    
And some sample numbers::

    >>> py_complex = 1+0j
    >>> np_complex = numpy.complex64(py_complex)
    >>> type(py_complex), type(np_complex)
    (<class 'complex'>, <class 'numpy.complex64'>)
    >>> py_complex, np_complex
    ((1+0j), (1+0j))

Issues with ``SupportsInt``
===========================

**Issue #1:** ``SupportsInt`` checks whether the type implements ``__int__``,
but that does not mean you can convert to ``int``.

Can I convert a complex number to an ``int``? This suggests yes::

    >>> isinstance(py_complex, SupportsInt), isinstance(np_complex, SupportsInt)
    (True, True)
    
But actually, only a NumPy complex can be converted to an ``int``::

    >>> int(np_complex)
    1
    
The code above "works" but you get a warning about converting to "real"::

    ComplexWarning: Casting complex values to real discards the imaginary part

Trying the same with a Python built-in ``complex`` raises ``TypeError``::

    >>> int(py_complex)
    Traceback (most recent call last):
      ...
    TypeError: can't convert complex to int
    
In the typing-sig mailing list, Guido explained that the built-in ``complex`` implements ``__int__`` only to provide a better error message.

    >>> complex.__int__
    <slot wrapper '__int__' of 'complex' objects>
    
**Issue 2:** While type checking, Mypy says a ``complex`` is inconsistent with ``SupportsInt``, but at runtime, the same ``complex`` passes an ``isiinstance`` check with ``SupportsInt``.

On typeshed, there is no method ``__int__`` in ``complex``, so ``int(py_complex)`` is flagged with this error::

    demo.py:10: error: Argument 1 to "to_int" has incompatible type "complex"; expected "SupportsInt"

    
Issue with ``SupportsFloat``
============================

**Summary:** Same as above.
``isinstance(c, SupportsFloat)`` returns ``True`` for both complex types,
but only the NumPy complex can actually be converted to ``float``.

::
    >>> isinstance(py_complex, SupportsFloat), isinstance(np_complex, SupportsFloat)
    (True, True)
    >>> float(np_complex)
    1.0
    >>> float(py_complex)
    >>> int(py_complex)
    Traceback (most recent call last):
      ...
    TypeError: can't convert complex to float




 

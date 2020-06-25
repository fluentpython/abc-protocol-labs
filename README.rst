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

Issue with ``SupportsInt``
==========================

.. note:: Summary:
   ``SupportsInt`` checks whether the type implements ``__int__``,
   but that does not mean you can convert to ``int``.

Can I convert a complex number to an ``int``? This suggests yes::

    >>> isinstance(py_complex, SupportsInt), isinstance(np_complex, SupportsInt)
    (True, True)
    
But actually, only a NumPy complex can be converted to an ``int``::

    >>> int(np_complex)
    1
    
This "works" but I get a warning about converting to "real"::

    ComplexWarning: Casting complex values to real discards the imaginary part

Trying the same with a Python built-in ``complex`` raises ``TypeError``::

    >>> int(py_complex)
    Traceback (most recent call last):
      ...
    TypeError: can't convert complex to int
    

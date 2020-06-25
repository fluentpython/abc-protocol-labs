===================================
Questions about ``SupportsComplex``
===================================


I am trying to understand the rationale for the runtime checkable ``SupportsXxx`` protocols. Focusing on ``SupportsComplex``, here are three questions I can't answer yet, and I'd appreciate any help with them:

A) Why does ``typing.SupportsComplex`` handle some types differently while type checking versus at runtime?

B) What are the envisoned use cases for ``SupportsComplex``, given that at runtime it does not support ``isinstance`` checks on values of types that actually can be converted to ``complex``, such as built-in ``int`` and ``float``, as well as NumPy integer and float types like ``float16`` and ``uint8``?

C) How does Mypy consider instances of ``int``, ``float`` and ``complex`` consistent with ``SupportsComplex``
if only built-in ``complex`` has a ``__complex__`` method on typeshed?

I know PEP 484 treats those three numeric types as special cases [1], but is there also hard-coded logic for ``SupportsComplex`` in Mypy?

[1] https://www.python.org/dev/peps/pep-0484/#the-numeric-tower


Thanks!

-- LR


PS. If you got this far, you may want the...


Gory detatils
=============

(This message can be checked with ``python3.8 -m doctest message.rst``)

At runtime, ``isinstance(c, SupportsComplex)`` returns ``True`` for ``numpy.complex64`` and ``False`` for all the other numeric types I tested: built-ins ``complex``, ``float`` and ``int``, and also ``numpy.float16``, ``numpy.uint8``.

However, in practice, the ``complex()`` bult-in function handles instances of all these types with no errors or warnings::

    >>> import numpy as np
    >>> from typing import SupportsComplex
    >>> sample = [1+0j, np.complex64(1+0j), 1.0, np.float16(1.0), 1, np.uint8(1)]
    >>> [isinstance(x, SupportsComplex) for x in sample]
    [False, True, False, False, False, False]
    >>> [complex(x) for x in sample]
    [(1+0j), (1+0j), (1+0j), (1+0j), (1+0j), (1+0j)]

In the typing-sig mailing list, Guido explained that the built-in ``complex``
accepts a single argument, and that's why all the conversions work::

    >>> complex(1)
    (1+0j)

Mypy accepts arguments of all those six types in a call to a ``to_complex()`` function defined like this::

    def to_complex(n: SupportsComplex) -> complex:
        return complex(n)

NumPy has no type hints, so its numbers are all ``Any``.

But Mypy is somehow "aware" that ``int`` and ``float`` can be converted to ``complex``,
even though on typeshed only the built-in ``complex`` class has a ``__complex__`` method.
How does that work?


Sample script that Mypy accepts with no errors
==============================================

# SupportsComplex_demo.py
# This type checks with Mypy and runs with Python 3.8 without errors


import numpy as np  # type: ignore
from typing import SupportsComplex, List


def to_complex(n: SupportsComplex) -> complex:
    return complex(n)

c: List[complex] = [
    to_complex(1 + 0j),
    to_complex(np.complex64(1 + 0j)),
    to_complex(1.0),
    to_complex(np.float16(1.0)),
    to_complex(1),
    to_complex(np.uint8(1)),
]

print(c)

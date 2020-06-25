import numpy as np  # type: ignore
from typing import SupportsInt, SupportsFloat, SupportsComplex


def to_int(n: SupportsInt) -> int:
    return int(n)


def to_float(n: SupportsFloat) -> float:
    return float(n)


def to_complex(n: SupportsComplex) -> complex:
    return complex(n)

try:
    i0 = to_int(1+0j)
except TypeError as e:
    print(e)

i1 = to_int(np.complex64(1+0j))

try:
    f0 = to_float(1+0j)
except TypeError as e:
    print(e)

f1 = to_float(np.complex64(1+0j))

c0 = to_complex(1+0j)
c1 = to_complex(np.complex64(1+0j))
c2 = to_complex(1.0)
c3 = to_complex(np.float16(1.0))
c4 = to_complex(1)
c5 = to_complex(np.uint8(1))

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
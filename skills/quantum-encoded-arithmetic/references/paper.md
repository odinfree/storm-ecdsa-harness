# Source and transfer

[Encoded reversible addition v1](https://arxiv.org/html/2610.41142v1), sections 2, 4–6.
The representation maps an integer exponent to an element of a binary extension field; multiplication implements addition modulo 2^n-1. The paper's bounds assume encoded inputs. Conversion to binary involves discrete logarithm, while its table-loaded application avoids that boundary. In-place constructions use a valid encoded subspace and extra workspace.

Application hypothesis: an entire compatible region may amortize or avoid conversions. This is not a generic fast adder for prime-field arithmetic.

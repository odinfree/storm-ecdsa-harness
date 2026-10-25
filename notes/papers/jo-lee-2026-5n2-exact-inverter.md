# Jo, Lee 2026: Quantum Discrete Logarithms on Elliptic Curves with 5n/2 + o(n) Logical Qubits and O~(n^2) Toffoli

- **Citation / URL:** ePrint 2026/2014 (PDF returned 403; numbers from abstract/snippets). https://eprint.iacr.org/2026/2014

## Key result
- ECDLP with 5n/2 + o(n) qubits (~640 + o(n) at n=256) and O~(n^2) Toffoli; exact in-place modular inverter with 3n/2 + o(n) qubits and O~(n) Toffoli per Euclid step; controlled point addition 5n/2 + o(n) qubits.

## Concrete trick
Invariant R t + r T = p for consecutive remainders R > r and coefficients 0 <= T < t: store three of the four values and reconstruct the fourth on demand; recover per-step temporaries from the updated state and erase them; Hua's identity a - (a^-1 + (b^-1 - a)^-1)^-1 = aba turns the variable products of affine addition into chains of inversions; sublinear workspace via MBU.

# Luo, Yang, Luo, Wang, Su, Sun, Li, Li 2026: Quantum Algorithm for Elliptic Curve Discrete Logarithms with Space-Efficient Point Addition

- **Citation / URL:** arXiv:2607.13816 (supersedes 2604.02311, the 1,333-qubit EEA), 2026. https://arxiv.org/abs/2607.13816

## Key result
- Affine point addition in 3n + 6 floor(log2 n) + 19 = 835 logical qubits at n=256 with <= 1051 n^2 ~ 68.9M Toffoli (score 5.7e10); modular inversion 2n + 6 log n + O(1) = 579 qubits, 229 n^2 ~ 15M T; step bound 4 ceil(1.58 n) ~ 1,620; ECDLP 1056 n^3 / log n (2^30.88 per key).
- Register-shared Proos-Zalka EEA: two Work banks of n+3 qubits hold remainders, quotient bits and Bezout cofactors with moving boundaries tracked by O(log n) length registers; location-controlled add/sub/swap via unary iteration; cross-cofactor invariant alpha*c_beta + beta*c_alpha = p; quotient digits one bit at a time.
- Mid-circuit X-basis measurement of the stale y register to free 256 qubits as workspace for the inverse EEA; kickback (-1)^{b.y} cancelled later by recomputing y and applying Z's.
- Table 2 reference points: Babbush 1,175 q / 2^26.27, 1,425 / 2^25.94; Schrottenloher 1,192 / 2^26.11, 1,446 / 2^25.78 (per key).

## Concrete trick
Length registers + location-controlled arithmetic so one shared register pair hosts all Euclidean values; measure-and-later-Z-repair a register that surviving state determines.

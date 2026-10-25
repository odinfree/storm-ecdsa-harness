# Huang, Zhang, Gao, Zhou, Qu 2025: Choosing Coordinate Forms for Solving ECDLP Using Shor's Algorithm (+ closed formula-level alternatives)

- **Citations / URLs:** arXiv:2502.12441 (2025) https://arxiv.org/abs/2502.12441 ; Kim et al., New Quantum Circuits for ECDLP (depth-optimised), ePrint 2026/106; Chevignard-Fouque-Schrottenloher, Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves, EUROCRYPT 2026, ePrint 2026/280.

## Key results
- With the added point classical, affine Weierstrass beats projective Weierstrass (Renes-Costello-Batina complete formulas) and extended twisted-Edwards on depth, gates and qubits (n=256: ~77.6M vs 154.5M vs 79.7M gates; 2,835 vs 4,876 vs 4,620 qubits in a Häner-style model), because reversibility forces extra multiplications to restore auxiliaries plus a canonicalising division anyway. Kummer/x-only differential addition excluded (Shor's U cannot supply P-Q); secp256k1 has prime order so no Montgomery/Edwards model.
- Kim 2026: projective out-of-place additions for depth, more qubits; opposite objective.
- CFS 2026: 3.12n + o(n) qubits (1,193 at 256) via RNS projective kP + Legendre-symbol compression, no inversion, but O~(n^4) gates (2^38.98 per run x 22 runs).

## Concrete trick
n/a (negative results).

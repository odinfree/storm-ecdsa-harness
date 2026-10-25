# Gidney 2019: Windowed quantum arithmetic (+ 2025 windowed modular arithmetic for RSA, + Lee et al. 2026 Crandall reduction)

- **Citation / URL:** arXiv:1905.07682 (2019). https://arxiv.org/abs/1905.07682 ; Optimized circuits for windowed modular arithmetic, arXiv:2502.17325 (2025); Efficient Quantum Modular Reduction: Crandall reduction, arXiv:2608.11563 (2026); Rines-Chuang 2018 Montgomery/Barrett multipliers, arXiv:1801.01081.

## Key result
- QROM lookup of L entries costs L-1 Toffoli independent of entry width; measurement-based unlookup ~2 sqrt(L) (2502.17325: 2^u + 2^(l-u), minimised at 2 sqrt(L); deferred unary conversion halves it; ~3% total for RSA-2048).
- Multiply-by-classical-constant via n/w lookups of w-bit windows: O(n^2/log n).
- Crandall reduction for q = 2^n - c: fold the high half back as +c*high, one or two conditional subtractions; ~47% fewer T than folding Barrett at n=10.
- Rines-Chuang: in-place Montgomery/Barrett multipliers need the inverse multiplication.

## Concrete trick
Index a classical table by w quantum bits and add the looked-up multiple with one n-bit adder instead of w controlled adds; NAF folds for small c.

# Gidney 2019: Approximate encoded permutations and piecewise quantum adders (coset representation after Zalka 2006)

- **Citation / URL:** arXiv:1905.08488 (2019). https://arxiv.org/abs/1905.08488 ; Zalka, Shor's algorithm with fewer (pure) qubits, quant-ph/0601097 (2006).

## Key result
Coset_m(r) = 2^{-m/2} sum_{j<2^m} |r + jN> on n+m qubits: a plain 2's-complement addition on this encoding has deviation <= 2^-m per add (Thm 3.2); deviations add; trace distance <= 2 sqrt(k 2^-m) after k adds. Oblivious carry runways: m extra qubits per runway, n + m(r+1) Toffoli per modular add, deviation 2^-m per runway; a 4000-bit register with three 40-bit runways stays within 0.34% after 1e6 additions.

## Concrete trick
Delete the compare-and-correct of modular addition by letting the register wrap into the next coset; pay only at encode/decode.

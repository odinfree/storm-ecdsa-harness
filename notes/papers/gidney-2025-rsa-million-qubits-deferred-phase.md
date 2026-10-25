# Gidney 2025: How to factor 2048 bit RSA integers with less than a million noisy qubits (sec. 2.4 deferred phase corrections; approximate residue arithmetic)

- **Citation / URL:** arXiv:2505.15917 (2025). https://arxiv.org/abs/2505.15917

## Key result
- Approximate residue arithmetic (from Chevignard-Fouque-Schrottenloher 2024): modular exponentiation as an f-bit dot product of residue bits with classical constants, f = O(log log N); Pareto points chosen by minimising q^3 t; 1,399 logical qubits / 6.5e9 Toffoli at n=2048.
- Primitive costs used: n-qubit add n-1 Toffoli with n-1 ancilla; lookup on n address qubits 2^n - n - 1; phaseup ~ sqrt(2^n).
- Sec. 2.4: measurement-based uncomputation of modular additions whose deferred CZ corrections are merged into later phase fixups (the Z is applied wherever the measured value is re-formed later).

## Concrete trick
Measure a wire holding v(x) in the X basis; the residual phase (-1)^{m v(x)} is cancelled later by Z^m applied where v(x) is re-formed (as an XOR/carry-save form), legal whenever the remaining data still determines x.

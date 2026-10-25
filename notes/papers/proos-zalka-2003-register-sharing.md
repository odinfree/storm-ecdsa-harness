# Proos, Zalka 2003: Shor's discrete logarithm quantum algorithm for elliptic curves (register sharing, padding statistics)

- **Citation / URL:** quant-ph/0301141 (2003). https://arxiv.org/abs/quant-ph/0301141

## Key result
- Register sharing in extended Euclid: |bA - aB| = p so (a,A) and (b,B) each fit one n-bit register; four registers in 2n + 8 sqrt(n) qubits instead of 4n; total ~6n qubits.
- Measured "size perturbation" (bits above expected size) at n=256: mean 17.33, sd 2.17, max 25 over 10^6 runs; padding 2 sqrt(n) = 32 bits per register; quotients bounded to 3 log2 n bits (fidelity loss 12/n); 4.5n cycle bound, ~3.5n average.

## Concrete trick
Shrinking remainders and growing cofactors share one physical register with a moving boundary; pad each by a few sigma of the empirically measured width distribution and accept the tail as failure.

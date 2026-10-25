# Häner, Tripier, Young et al. (IonQ) 2026: Computing 256-bit elliptic curve discrete logarithms in 26 days on a fault-tolerant trapped-ion quantum computer with 20,000 qubits

- **Citation / URL:** arXiv:2609.05625, Sep 2026. https://arxiv.org/html/2609.05625

## Key result
- Windowed affine point add in the same formula order as HEAD (dx, dy, lambda in place, x1+2x2-lambda^2, lambda*(x2-x3)): ~1.196M T (max over 100 runs, excluding three 2^16 lookups), 1,457-1,462 logical qubits; total 28 x (1.196M + 3*2^16) ~ 39.0M T per key (down from 58M in Schrottenloher's circuits).
- In-place multiply via a modified dialog GCD: store v~ = v + (1-a)u, s~ = s - (1-a)r (a = parity of v), so each iteration is v~' = (v~ + (-1)^a' u)/2 with a' = v~[1] xor u[1] (the same parity steering as ping-pong) plus a swap conditioned on m_i = a' AND (u' > v~') and a persistent orientation qubit (no data-dependent swaps of registers).
- Conditionally-inverted additions (U if ctrl=0, U^dagger if 1) at ~half a controlled adder; 6 local history qubits compressed to 5; conditional one's complement around an approximate pseudo-Mersenne modular adder.
- Non-modular squarer x^2 = -x + sum (2x_i - 1) 2^(2i+1)(h_i + x_i) with T(n) = n(n+3)/2 - 1 (8,383 T at n=128); single-split Karatsuba modular square-subtract using B^2 == c.

## Concrete trick
Orientation qubit + conditional one's complement around an unconditional adder with carry-in: a Kaliski/Stein "subtract the smaller from the larger" step becomes swap-free and compare-free because the subtraction's own borrow IS the comparison.

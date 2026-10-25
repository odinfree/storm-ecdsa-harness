# Long et al. 2026: Efficient Record-and-Replay Arithmetic for Quantum Elliptic-Curve Point Addition

- **Citation / URL:** Long, Pender, Huang, ... Drake et al. (36 authors, ECDSA.fail contributors), arXiv:2609.28882, Sep 2026. https://arxiv.org/abs/2609.28882
- **Status vs HEAD:** direct ancestor of `pingpong.rs`; HEAD is ~33% cheaper per round and already past every number here.

## Key result
- Comparison-free ping-pong GCD: t' = (t + (-1)^e s)/2 with e = t[1] xor s[1], fixed target alternation, 1 transcript qubit per round, 704 rounds (~2.75 rounds per bit).
- Convergence over 10M random denominators: mean 621.5 rounds, max 743; exceedances at budgets 704/736/768 = 1,535 / 6 / 0.
- Fused reverse-replay cell z <- 2z +/- y mod p: 393 T at a 56-bit fold window (446 unfused), 87-88 workspace qubits; "common addition and phase comparisons" = 336 T of that.
- Static breakdown (windowed ping-pong, 1,338 Q x 1.128M T): GCD value updates 395k, field replay 552k, replay setup 828, squaring+slope masking 65k, coordinate updates 4k, lookup+address 167k. Peak: 512 payload + 704 tape + 16 values + 88 carries + 1-18 controls.
- Jump-2: 261 macro-steps, base-5 codec packs 3 symbols (5 reachable of 8) in 7 qubits: 609-qubit transcript vs 783 raw.
- Zero-payload repair flag h=[c=0] (+1 qubit, 0 failures on 100k inputs); exact chunk-carry predicate cout = [z<a] xor (cin and [z=a]).
- Reversible safegcd reference: 741 rounds, 3,300 Q, 7.5M T (unoptimised) vs ping-pong 768 rounds 2,320 Q 6.29M T.
- Karatsuba square vs product-register square differ by only 8,163 T.

## Concrete trick
Fuse the doubling overflow and the addition carry into one correction kappa in {-1,0,1,2} applied inside a truncated low window using the sparse F = 2^32+977; record 1 bit/round and replay on (y,0) for division, reversed for multiplication.

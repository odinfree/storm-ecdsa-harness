# Gu, Kemeny, Yelin, Lukin 2026: Discovering state-of-the-art quantum circuits with large language models (reversible divstep with branch recovery)

- **Citation / URL:** arXiv:2610.22367 (SI II + Appendix A), Oct 2026. https://arxiv.org/html/2610.22367v1

## Key result
- secp256k1 point add from a half-delta Bernstein-Yang divstep walk: 4.0M T x 935 Q (TQ 3.7e9); family 3.3M x 1,191 ... 7.9M x 893 by moving the history cutoff j_store (stack 198 -> 60 qubits at j_store=5; 24 at j_store=9). Four walks = 2.5M T (63%), field multiplications 1.4M (35%).
- Schedule 533 divsteps (worst case 590 for this prime, typical termination 505-530), zero-test/freeze only from step 499; failures ~1.6e-4 per addition.
- Branch recovery: swap bit s ALWAYS recoverable from the post-state (s=1 iff v2(fv') = 1); nonswap with z' >= 1 forces b=0; g'=0 forces b=1; the remaining ~1/3 "negative-counter nonswap" decisions decode as b = bit_{j-1}(gv' q^-1 mod 2^j), j = v2(fv'), q = fv'/2^j: a 2-adically local function of (j, f' mod 2^j, q mod 2^j). Decoder term counts 3/3/11/26/79/268/1092 for depths 2..8 (depth-2 = 2 Toffoli); decisions deeper than j_store go to a 60-qubit stack (avg 21, worst 263).
- Registers: (f, gv) and (g, fv) time-share two 256-qubit registers with build-time-fixed widths (bits(f)+bits(gv) ~ n from f*gv - g*fv = p). Carries propagated only through the low 58 bits (2^-26 per reduction), compares read the top 27 bits.
- Specialised Euclidean variant 20.5M x 843 (3.4x fewer T than Luo et al.). Search driver: OpenEvolve + MAP-Elites over the (T,Q) plane.

## Concrete trick
Decode instead of store: recover per-step branch bits from the arithmetic state during the reverse pass with depth-limited decoders; keep only undecodable decisions on a small stack; accept a bounded overflow probability.

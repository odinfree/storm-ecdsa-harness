# safegcd implementation notes (libsecp256k1): divstep bounds and batching; Brent 1976: Analysis of the binary Euclidean algorithm

- **Citations / URLs:** https://github.com/bitcoin-core/secp256k1/blob/master/doc/safegcd_implementation.md (Wuille, 2021; Bernstein-Yang 2019 "Fast constant-time gcd computation and modular inversion"); R. P. Brent, Analysis of the binary Euclidean algorithm, 1976, https://maths-people.anu.edu.au/~brent/pub/pub037.html

## Key results
- For 256-bit moduli: 741 divsteps suffice (BY Thm 11.2), 724 by the safegcd-bounds project, **590 with the half-delta (delta = 1/2) start** proven by convex-hull analysis; zeta = -(delta + 1/2) keeps the counter integral; divsteps batch into groups of N=62 as a 2x2 transition matrix (entries fit in N+1 bits) applied to (f,g) by shift and to (d,e) with an exact division by 2^N.
- Brent: right-shift binary GCD performs ~0.706 lg N subtract-and-shift iterations on random inputs (~181 at 256 bits) and ~1.41 lg N total shifts (~361); worst case <= 2 lg N shifts.

## Concrete trick
Magnitude-aware subtraction (larger minus smaller) plus full zero stripping gives ~1 bit of 2-adic progress per halving; a provable step bound (590) replaces a probabilistic schedule.

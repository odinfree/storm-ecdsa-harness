# Schrottenloher 2026: Optimized Point Addition Circuits for Elliptic Curve Discrete Logarithms

- **Citation / URL:** A. Schrottenloher, arXiv:2606.02235 / ePrint 2026/1128 (open reproduction of Google's circuits). https://arxiv.org/abs/2606.02235

## Key result
- secp256k1 windowed point add (w=16, window excluded): space-opt 1,192 Q / 2^21.19 ~ 2.39M T; gate-opt 1,446 Q / 2^20.83 ~ 1.86M T (Google: 1,175/2.7M and 1,425/2.1M). Full Shor = 28 x (Q_A + 3*2^16).
- Qubits 4.355n + O(sqrt n) = 2n Bezout pair + 2.355n garbage (information bound 2.12n = 1.5 bits x 1.413n iterations); padding c_pad*sqrt(n), c_pad ~ 2.3; iteration budget 1.413n + 2.4 sqrt(n) ~ 400 (each iteration removes factor 3/8 from u*v).
- Cost shares (space-opt): in-place multiplier+inverse 90% (Bezout reconstruction 54%, GCD recording 36%), squaring 9%; controlled modular adder 39%, hybrid adder 22%, controlled-swap 19%, Gidney constant adder 15%, modular double 8%.
- Garbage: 1.5 bits/iteration; three iterations (27 states) packed into 5 bits with 5 Toffoli -> 2.355n = 603 tape bits.
- Approximate comparisons on the top 40-50 bits only, failure ~2^-13.3 (no repair). CDKM (2n T) vs Gidney (n T, n ancilla) vs hybrid chosen per ancilla budget. Pseudo-Mersenne doubling = shift + controlled add of f into LSBs; x+y=q handling needed only in the first ~c sqrt(n) iterations.

## Concrete trick
Record pass (b0 = v odd, b1 = u > v; cswap, v -= u, v /= 2) + Bezout replay on (y,0) = inversion and in-place multiplication as one operation; free rails shrink 0.708 bits/iteration and hold the tape.

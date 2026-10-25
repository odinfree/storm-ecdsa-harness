# Häner, Jaques, Naehrig, Roetteler, Soeken 2020: Improved quantum circuits for elliptic curve discrete logarithms; Roetteler, Naehrig, Svore, Lauter 2017: Quantum resource estimates for computing ECDLP; Gouzien et al. 2023: 126,133 cat qubits

- **Citations / URLs:** arXiv:2001.09580 (PQCrypto 2020) https://arxiv.org/abs/2001.09580 ; arXiv:1706.06752 (2017); Gouzien, Ruiz, Le Régent, Guillaud, Sangouard, PRL 131, 040602 (2023), arXiv:2302.06639.

## Key results
- Häner 2020: P-256 full Shor low-width 2,124 qubits / 1.98 x 2^30 T-gates; low-T 2,619 Q; asymptotics 8n + 10.2 lg n qubits, 436 n^3 T. Kaliski inverter with 2n fixed iterations, controlled swaps + counter; windowed add-and-halve Montgomery multiplication (window 0.68 lg n + c); signed-digit windowing halves table size; adaptive pebbling of uncompute steps; AND gates with 0-T uncompute. Inversion ~1.24e8 T low-width (1,811 qubits), 7n + log n qubits.
- Roetteler 2017: point add 9n + 2 ceil(log n) + 10 = 2,330 qubits, ~224 n^2 log n + 2045 n^2 ~ 2.5e8 Toffoli; reversible Montgomery inverse, 2n rounds, 7n qubits.
- Gouzien 2023: leading-order per point add (Kaliski): Montgomery mult 3n^2, clean mult 6n^2, squaring 6n^2, Kaliski iteration 18n, inversion 36n^2, division 78n^2, whole addition 174 n^2 ~ 11.4M T; 9n + w_e + 4 qubits. Source of the affine schedule x -= ox, y -= oy, divide, x += 3ox, square, multiply, y -= oy, x = ox - x that HEAD also uses.

## Concrete trick
One arithmetic op per round steered by controlled swaps + a round counter (RNSL's four round variants collapsed); 2n-k Montgomery correction doublings run in parallel with uncompute rounds.

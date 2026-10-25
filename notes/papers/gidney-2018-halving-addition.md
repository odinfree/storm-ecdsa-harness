# Gidney 2018: Halving the cost of quantum addition

- **Citation / URL:** arXiv:1709.06648, Quantum 2, 74 (2018). https://arxiv.org/abs/1709.06648
- Companion primitives: Cuccaro-Draper-Kutin-Moulton 2004 (quant-ph/0410184: 2n-1 Toffoli, 1 ancilla, MAJ/UMA), Takahashi-Tani-Kunihiro 2009 (0910.2530: 2n-2 Toffoli, 0 ancilla), Draper-Kutin-Rains-Svore 2004 CLA (quant-ph/0406142: ~10n Toffoli, 2n ancilla, log depth), Luongo-Miti-Narasimhachar-Sireesh 2024 MBU for modular arithmetic (2407.20167: 10-25% T cuts in VBE/Beauregard adders).

## Key result
n-bit in-place adder with n-1 temporary ANDs (Toffoli-equivalents) and n-1 clean ancilla; each AND uncomputed by X-basis measurement + classically controlled CZ at 0 Toffoli (T-count 8n -> 4n). Controlled adder 2n Toffoli. A kept (temporary) adder costs the same and its result is uncomputed for free.

## Concrete trick
carry_i = MAJ(a_i, b_i, c_{i-1}) into a fresh ancilla with one AND; later measure in X and fix the (-1)^carry phase with a CZ on the recomputable inputs.

# Litinski 2024: Quantum schoolbook multiplication with fewer Toffoli gates (controlled add-subtract at n-1)

- **Citation / URL:** arXiv:2410.00899 (2024). https://arxiv.org/abs/2410.00899

## Key result
- Controlled add-subtract (add if control = 1, subtract if 0) costs n-1 Toffoli, the same as an uncontrolled Gidney add, versus 2n-1 for a controlled adder. Schoolbook multiplier n^2 + 4n + 3 Toffoli via +-1 digit recoding (step k adds (1-x_k) 2^{n+k} + (2x_k - 1) 2^k y, fixed up by three plain adds).
- Mod-p quantum x quantum multiply (Montgomery form) in n/w ModMultSteps: w controlled adds (2w(n+1)), a 2^w lookup, an (n+w)-bit add, 3*2^{w/2} unlookup; add-subtract variant n^2 + 6n + (n/w)(2^w + 3*2^{w/2} + 3n - 3), optimal w ~ log2(n/log2 n) + 2 -> ~103k T at n=256; 30% fewer Toffoli for 256-bit ECDLP than prior.

## Concrete trick
Conjugate the addend by multi-target CNOTs from the control so the AND ladder itself is uncontrolled; the sign choice rides on Cliffords.

# Litinski (PsiQuantum) 2023: How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates

- **Citation / URL:** arXiv:2306.08585, 2023. https://arxiv.org/abs/2306.08585 (follow-up: Litinski 2024, arXiv:2410.00899 "Quantum schoolbook multiplication with fewer Toffoli gates", lowering (44 + 65/k) to (30 + 73/k) million per key)

## Key result
- Per key (k parallel instances): (44k + 65) x 10^6 Toffoli, 6,000 logical qubits (3,000 memory); 13 of 16 windows computed, last 48 key bits brute-forced classically.
- Per point addition (Montgomery form, n=256): Kaliski inversion 2n iterations x 13n = 26n^2 + 2n ~ 1.70M T ("over 10x a multiplication"); windowed out-of-place multiplication (4-bit windows) 2.25n^2 + 9n ~ 150k; modular add 4n, controlled 5n, negation 2n, subtraction 6n; MSB-only parity reset in doubling. Qualtran-verified bloq costs (Papa 2025, arXiv:2506.03318): mod add 4n-1, controlled mod add 5n+1, mod sub 6n-3, equals n-1, Montgomery mult 2.25n^2+7.25n-1, Kaliski 26n^2+9n-1; point add ~126n^2 ~ 8.3M T.
- 2410.00899: controlled add-subtract (add if ctrl=1, subtract if 0) costs n-1 Toffoli like an uncontrolled Gidney add (vs 2n-1 for a controlled adder); mod-p schoolbook n^2 + 6n + (n/w)(2^w + 3*2^{w/2} + 3n - 3), w ~ log2(n/log2 n) + 2 -> ~103k T at n=256.

## Concrete trick
Montgomery batch inversion across k parallel instances (k inverses = 1 inversion + 3k-3 multiplications); windowed lookup multiplication; add/sub conjugation so the AND ladder is uncontrolled and the sign rides on Cliffords.

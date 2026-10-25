# Long et al. 2026: ECDSA.Fail: Open Autoresearch for Optimizing Elliptic-Curve Point Addition in Shor's Algorithm

- **Citation / URL:** arXiv:2609.09582 (v2), 2026; supplemental Note B at https://github.com/jieyilong/ecdsafail-supplemental-materials. https://arxiv.org/abs/2609.09582
- **Status vs HEAD:** the lineage paper of the public challenge tree; HEAD (9.39e8) is 25% below its best post-cutoff point.

## Key result
- Eras: two-pass Kaliski (2,715 -> 2,002 Q) -> streamed dialog-GCD (1,168) -> Jump-2 + base-5 codec (1,151). Best at cutoff 8e9c9a2: 1,151 Q x 1,299,453 T = 1.496e9 (-86% vs baseline 1.075e10). Post-cutoff ping-pong 3616dbf: 1,321 Q x 952,707 T = 1.259e9 (T -25.9%, Q +171). Windowed (w=16) variant: +11 Q, +29.6% T.
- Low-Q track: 980, 948 (54.8M T), 828 (448M), 825 (489M; 259+259+257+37+13), 813 Q.
- Note B census of 400 commits: dead-code/width truncation 61% of commits (39% of delta); register/scratch allocation 21%; fusion 18%; windowing 13%; uncompute strategy 8% from only 26 commits; 70 largest deltas = 91.6% of gross reduction; 8 of 11 "neutral" commits were actual gate removals visible only statically.
- Named big moves: boundary cswap-merge via cswap(p)cswap(q) = cswap(p xor q) with a frame-parity qubit (-274k T); comparator conjugation 4n -> 2n (-2.09M each); shared-operand scratch fusion (-524k); Solinas add + conditional unsub branch collapse (-656k); Bennett pairing of Kaliski call sites (-21.8M each); MB AND uncompute 2(n-1) -> n-1; ancilla-lifetime windowing (-256 Q at 0 T); 977 = 2^10-2^6+2^4+1; guaranteed-prefix specialisation (branch-free first 304 Kaliski iterations, -158k).
- Base-5 transcript codec: 5 of 8 Jump-2 symbol values reachable -> 3 symbols in 7 qubits; 261-step tape 609 Q instead of 783 (-174 Q).
- Karatsuba square-subtract specialised to p: lambda^2 = A + (C-A-B) + F*B mod p, build-apply-unbuild so A,B,C never co-live; 24,512 vs 32,640 AND products.
- States the score "can be gamed through support selection" (nonce grinding) and that modular inversion dominates.

## Concrete trick
Reachability-based transcript coding: store only reachable symbol combinations; stream the encoded tape into wires freed by shrinking operands; materialise the classical addend off-peak.

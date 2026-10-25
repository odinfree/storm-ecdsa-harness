# Khattar, Shutty, Gidney et al. (Google) 2025: Verifiable Quantum Advantage via Optimized DQI Circuits (origin of the "dialog" EEA)

- **Citation / URL:** arXiv:2510.10967, Oct 2025. https://arxiv.org/html/2510.10967v1

## Key result
- Two reversible EEA compilations: explicit Bezout (Zalka register sharing, quotients stored in the padding, 6n^2 quantum-quantum multiplications) and implicit "Dialog" (sequence of Bernstein-Yang transition matrices / swap decisions, 2n^2 multiplications, invariant len(poly)+len(dialog) = 2n so 2nb + O(log n) qubits).
- Direct division C*B^-1 by applying the dialog to [0, C] without materialising the inverse (4n^2 vs 7n^2 multiplications); multiplication = inverse replay of the same transcript.
- Authors warn the explicit/implicit trade-off "should be carefully re-evaluated" for prime fields; open question: can the dialog shrink from ~2n to ~n field elements when one GCD input is classical?

## Concrete trick
Record the decisions of a constant-time, division-free GCD; replay them linearly on (0, C) for division and in reverse for multiplication; reuse the freed remainder qubits for the growing dialog.

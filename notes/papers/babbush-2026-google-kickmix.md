# Babbush, Zalcman, Gidney et al. (Google Quantum AI) 2026: Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities

- **Citation / URL:** arXiv:2603.28846 / ePrint 2026/625, Mar 2026. https://arxiv.org/abs/2603.28846

## Key result
- ZK-attested caps for withheld point-addition circuits: low-qubit <= 2,700,000 executed CCX+CCZ at <= 1,175 logical qubits; low-gate <= 2,100,000 at <= 1,425; <= 17M total ops each; verified on 9,024 Fiat-Shamir inputs (the harness copies this protocol). Full ECDLP: (PA_Toff + 3*2^w)(2n/w - 4), w=16 -> 28 windowed additions; qubits PA_Q + w via a recycled QFT register. "Approximately 4.5n space" (1,152 + ~23 metadata).
- Appendix A.4 defines the "kickmix" gate class: classical reversible gates + X-basis measurement-based uncomputation + diagonal phase corrections (classically simulable): exactly the harness's op set.
- Correctness required only on "most inputs" (~2e-4 failure per addition budget on their side).

## Concrete trick
Measurement-based uncomputation with phase fix: measure an ancilla holding f(k) in X; on |-> apply a diagonal phase depending only on k, "usually cheaper than computing f(k), sometimes much less". Average-executed-Toffoli accounting: gates conditioned on classical bits that do not fire are not counted.

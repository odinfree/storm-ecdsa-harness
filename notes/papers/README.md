# Literature notes

Short notes on the papers and public work behind the ecdsa.fail circuits. Each note gives the citation, the key result
and the concrete trick. "HEAD" in a note means the public Layr-Labs/ecdsafail-challenge tree at PR #718 (mid-October 2026).

| Note | Authors | Topic |
|---|---|---|
| [babbush-2026-google-kickmix](babbush-2026-google-kickmix.md) | Babbush, Zalcman, Gidney et al. (Google Quantum AI) 2026 | Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities |
| [ecdsafail-pr-lineage-leapfrog-oct-2026](ecdsafail-pr-lineage-leapfrog-oct-2026.md) | ecdsa.fail solvers (public PRs), Oct 2026 | PR lineage from Leapfrog (#500) to HEAD (#718), plus the low-T and low-Q branches |
| [gidney-2018-halving-addition](gidney-2018-halving-addition.md) | Gidney 2018 | Halving the cost of quantum addition |
| [gidney-2019-coset-piecewise-adders](gidney-2019-coset-piecewise-adders.md) | Gidney 2019 | Approximate encoded permutations and piecewise quantum adders (coset representation after Zalka 2006) |
| [gidney-2019-windowed-arithmetic](gidney-2019-windowed-arithmetic.md) | Gidney 2019 | Windowed quantum arithmetic (+ 2025 windowed modular arithmetic for RSA, + Lee et al. 2026 Crandall reduction) |
| [gidney-2025-constant-adder-and-conditionally-clean](gidney-2025-constant-adder-and-conditionally-clean.md) | Gidney 2025; Khattar, Gidney 2024; Fedoriaka 2025; Häner, Roetteler, Svore 2016 | Constant adder, conditionally clean ancillae, dirty-ancilla primitives |
| [gidney-2025-rsa-million-qubits-deferred-phase](gidney-2025-rsa-million-qubits-deferred-phase.md) | Gidney 2025 | How to factor 2048 bit RSA integers with less than a million noisy qubits (sec. 2.4 deferred phase corrections; approximate residue arithmetic) |
| [gu-2026-llm-divstep-branch-decoding](gu-2026-llm-divstep-branch-decoding.md) | Gu, Kemeny, Yelin, Lukin 2026 | Discovering state-of-the-art quantum circuits with large language models (reversible divstep with branch recovery) |
| [haner-2020-improved-ecdlp-and-roetteler-2017](haner-2020-improved-ecdlp-and-roetteler-2017.md) | Häner, Jaques, Naehrig, Roetteler, Soeken 2020 | Improved quantum circuits for elliptic curve discrete logarithms; Roetteler, Naehrig, Svore, Lauter 2017: Quantum resource estimates for computing ECDLP; Gouzien et al. 2023: 126,133 cat qubits |
| [haner-2026-ionq-26-days](haner-2026-ionq-26-days.md) | Häner, Tripier, Young et al. (IonQ) 2026 | Computing 256-bit elliptic curve discrete logarithms in 26 days on a fault-tolerant trapped-ion quantum computer with 20,000 qubits |
| [huang-2025-coordinate-forms-and-negative-formulas](huang-2025-coordinate-forms-and-negative-formulas.md) | Huang, Zhang, Gao, Zhou, Qu 2025 | Choosing Coordinate Forms for Solving ECDLP Using Shor's Algorithm (+ closed formula-level alternatives) |
| [jo-lee-2026-5n2-exact-inverter](jo-lee-2026-5n2-exact-inverter.md) | Jo, Lee 2026 | Quantum Discrete Logarithms on Elliptic Curves with 5n/2 + o(n) Logical Qubits and O~(n^2) Toffoli |
| [karatsuba-squaring-gidney-parent-roetteler](karatsuba-squaring-gidney-parent-roetteler.md) | Gidney 2019 | Asymptotically Efficient Quantum Karatsuba Multiplication; Parent, Roetteler, Mosca 2017: Reversible circuits for Karatsuba-based integer multiplication |
| [khattar-shutty-2025-dqi-dialog](khattar-shutty-2025-dqi-dialog.md) | Khattar, Shutty, Gidney et al. (Google) 2025 | Verifiable Quantum Advantage via Optimized DQI Circuits (origin of the "dialog" EEA) |
| [litinski-2023-50m-toffoli](litinski-2023-50m-toffoli.md) | Litinski (PsiQuantum) 2023 | How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates |
| [litinski-2024-schoolbook-add-subtract](litinski-2024-schoolbook-add-subtract.md) | Litinski 2024 | Quantum schoolbook multiplication with fewer Toffoli gates (controlled add-subtract at n-1) |
| [long-2026-ecdsafail-autoresearch](long-2026-ecdsafail-autoresearch.md) | Long et al. 2026 | ECDSA.Fail: Open Autoresearch for Optimizing Elliptic-Curve Point Addition in Shor's Algorithm |
| [long-2026-record-and-replay](long-2026-record-and-replay.md) | Long et al. 2026 | Efficient Record-and-Replay Arithmetic for Quantum Elliptic-Curve Point Addition |
| [luo-2026-space-efficient-point-addition](luo-2026-space-efficient-point-addition.md) | Luo, Yang, Luo, Wang, Su, Sun, Li, Li 2026 | Quantum Algorithm for Elliptic Curve Discrete Logarithms with Space-Efficient Point Addition |
| [proos-zalka-2003-register-sharing](proos-zalka-2003-register-sharing.md) | Proos, Zalka 2003 | Shor's discrete logarithm quantum algorithm for elliptic curves (register sharing, padding statistics) |
| [safegcd-divstep-bounds-and-brent-1976](safegcd-divstep-bounds-and-brent-1976.md) | libsecp256k1 safegcd notes; Brent 1976 | Divstep bounds and batching; analysis of the binary Euclidean algorithm |
| [schrottenloher-2026-optimized-point-addition](schrottenloher-2026-optimized-point-addition.md) | Schrottenloher 2026 | Optimized Point Addition Circuits for Elliptic Curve Discrete Logarithms |
| [spooky-pebbles-gidney-kornerup](spooky-pebbles-gidney-kornerup.md) | Gidney 2019 (blog) | Spooky pebble games and irreversible uncomputation; Kornerup, Sadun, Soloveichik: Tight Bounds on the Spooky Pebble Game |
| [trailmix-and-competitor-toolchains](trailmix-and-competitor-toolchains.md) | Trail of Bits; BitWonka; Jieyi Long; MonitSharma | TrailMix and competitor toolchains (reference circuits, evaluator replicas, nonce screens) |

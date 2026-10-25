# Credits

Each entry names the person or project, what we took from them, where it shows up in this repository, and the
licence that covers their own work. "Derived from" means a skill restates or adapts their published material.
"Inspired by" means we took an idea or a practice and wrote our own text. We copy no third-party code except the
MIT-licensed templates in `skills/research-loop`.

If something here is missing or wrong, please open a
[credit correction](.github/ISSUE_TEMPLATE/credit-correction.md).

## Benchmarks and the people who run them

| Who | What | Link |
|---|---|---|
| ecdsa.fail team at Layr-Labs, with Gautham Anant | The open secp256k1 point-addition benchmark, its evaluator and leaderboard. The harness adapts code and data Google Quantum AI published with its 2026 paper; Kirk Baird (Sigma Prime) reviewed it. | [ecdsa.fail](https://ecdsa.fail), [Layr-Labs/ecdsafail-challenge](https://github.com/Layr-Labs/ecdsafail-challenge) |
| Sreeram Kannan | The article that framed ecdsa.fail as open agentic science. | [You beat Google](https://www.linkedin.com/pulse/you-beat-google-sreeram-kannan-rqehc) |
| Yukon and zkSecurity | The Proximity Prize and its accepted-proof record. | [better.codes](https://better.codes), [proximity-prize/proximity-prize](https://github.com/proximity-prize/proximity-prize) (Apache-2.0) |
| Kaggle | The "Squares in Squares" competition and its community notebooks. | [kaggle.com](https://www.kaggle.com) |

## People whose work the skills are built on

| Who | What we used | Where | Their licence |
|---|---|---|---|
| BitWonka | fasteval, the exact parallel replica of `eval_circuit`, and dead-ccx-finder. Used at run time from BitWonka's repository; not copied here. | `ecdsafail-fasteval` (derived from) | [BitWonka/ecdsafail-tools](https://github.com/BitWonka/ecdsafail-tools), no licence file |
| BitWonka | The loop-engine commands, converted into one skill. | `research-loop` (derived from; MIT notice kept) | [BitWonka/loop-engine](https://github.com/BitWonka/loop-engine), MIT |
| BitWonka | 26 public ecdsa.fail submission notes (Layr-Labs PRs 500-818). | `ecdsafail-lowq-playbook` and its digest (derived from) | the notes, cited by line |
| BitWonka | 31 public Proximity Prize notes and Discussion #537. | `proximity-prize-campaign` digests (derived from) | the notes, cited by line |
| gnuchev (Vasily Gnuchev) | 167 public ecdsa.fail submission notes. | `ecdsafail-pareto-ratchet`, `ecdsafail-scratch-diet` and their digests (derived from) | the notes, cited by line |
| gnuchev (Vasily Gnuchev) | Open Research Club's two-model review practice, including its review-record fields. | `cross-model-review-gate` (derived from) | [gnuchev/openresearch-club](https://github.com/gnuchev/openresearch-club), Apache-2.0 |
| bulengerk | 81 public ecdsa.fail submission notes: nine left moves and their descents. | `beachhead-ratchet`, `invariant-chart`, `shot-autopsy` (derived from) | the notes, cited by submission id |
| Jieyi Long and co-authors | The ECDSA.Fail paper (arXiv:2609.09582), its supplemental materials, the record-and-replay paper (arXiv:2609.28882), the ecdsafail_skills suite and the GPU island toolkit. | `notes/papers`; `ecdsafail-oracle-loop` points to the GPU island toolkit | [ecdsafail_skills](https://github.com/jieyilong/ecdsafail_skills) (no licence file), [ecdsafail_gpu_toolkit](https://github.com/jieyilong/ecdsafail_gpu_toolkit) (MIT), [supplemental materials](https://github.com/jieyilong/ecdsafail-supplemental-materials) (no licence file) |
| nasqret (Bartosz Naskrecki) | Broad qubit sweeps and memory-mechanism recombination. | `nasqret-playbook` (inspired by) | [nasqret](https://github.com/nasqret) |
| Teddy Pender (teddyjfpender) | Posted the August 2026 row that opened the ping-pong family; co-author of the record-and-replay paper. | `notes/papers/long-2026-record-and-replay.md` | [teddyjfpender/ecdsafail-challenge](https://github.com/teddyjfpender/ecdsafail-challenge) |
| tanweai and the PUA contributors | The repeated-failure method and completion-evidence checklist of the PIP edition. We wrote our own cards and left out its hooks, telemetry and pressure rhetoric. | `agent-unstuck`, `pip-discipline`, `ecdsafail-oracle-loop` (inspired by) | [tanweai/pua](https://github.com/tanweai/pua), no licence file |
| ShouqiaoW and OpenAI | Contract-style prompts for open problems (the erdos prompts, OpenAI's Cycle Double Cover prompt). Paraphrased, not copied. | `hard-problem-contract` (inspired by) | [ShouqiaoW/erdos](https://github.com/ShouqiaoW/erdos), MIT |
| Erich Friedman and the packing literature | Known square packings that set the starting frontier: Friedman's records, Ellsworth, Goebel, and the strip constructions of Erdős and Graham, Chung and Graham, Bui, and McClenagan. | `squares-in-squares-campaign` | [Packing Center](https://erich-friedman.github.io/packing/squinsqu/) |

## Solvers cited in the digests

The ecdsa.fail digests quote public rows and notes by jackylee0424, mochimodev, krishparadox, dysnasia, kaankolcu,
MonitSharma, edi3on, SnehalRaj, gopikannappan, zuiris and others. The Proximity Prize digest credits 0xLucqs for the
68.05 construction and cites zkfriendly's submission. Every quote points at the author's own note or pull request.

## Proximity Prize Discussion #537

The 116.13 upper-track digest summarises the public thread by BitWonka, dtumad, hybridnoise, yoyo930021, GordoAR,
jieyilong, CrystallineButterfly, lamb356 and raresbuhai, with each claim attributed to its author.

## Tools and services

[TypeSafe](https://github.com/typesafe-ai/skills) (Jev, MIT skill), [Elicit](https://elicit.com) (API),
[defuddle](https://github.com/kepano/defuddle) by kepano (MIT, used by research-loop),
[Trail of Bits TrailMix](https://github.com/trailofbits/trailmix) (reference circuits, cited in the notes),
[ArkLib](https://github.com/Verified-zkEVM/ArkLib) (Apache-2.0) and Mathlib, SageMath, Magma, OSCAR, Singular,
GAP/GUAVA, PARI/GP, Hecke, FLINT, Nemo, CryptoMiniSat, Z3, OR-Tools and Gurobi.

## Papers in notes/papers

Proos and Zalka (2003); Gidney (2018, 2019, 2025, and the 2019 spooky-pebble post) with Kornerup, Sadun and
Soloveichik; Parent, Roetteler and Mosca (2017); Roetteler, Naehrig, Svore and Lauter (2017); Häner, Jaques, Naehrig,
Roetteler and Soeken (2020); Gouzien et al. (2023); Litinski (2023, 2024); Khattar and Gidney (2024); Khattar, Shutty,
Gidney et al. (2025); Fedoriaka (2025); Häner, Roetteler and Svore (2016); Huang, Zhang, Gao, Zhou and Qu (2025);
Babbush, Zalcman, Gidney et al. (2026); Häner, Tripier, Young et al. (2026); Jo and Lee (2026); Gu, Kemeny, Yelin and
Lukin (2026); Luo et al. (2026); Schrottenloher (2026); Long et al. (2026, two papers); Zalka (2006); Lee et al.
(2026); Bernstein and Yang's safegcd as implemented in libsecp256k1, with Brent (1976). Each note gives the full
citation, and several name further companion papers. The Proximity Prize digests also rest on Dao, Kominers, Thaler
and Zheng (2026, ECCC TR26-237): BitWonka's binary-track proofs use their common-top principle (Lemma 6.1) and
their pole-pair construction.

## The first Storm harness

Gajesh Naik ([Gajesh2007](https://github.com/Gajesh2007)) inspired the custom agent setup; newjordan (Frosty40,
[overwatch](https://github.com/newjordan/overwatch)) the shared status board; Sam (karnot.xyz) the operator cards;
zuiris (Maksim) the split between a research lane and an engineering lane; Justin Drake and others in public
discussion helped frame the benchmark and its validation. Sam's and zuiris's ideas reached us through group
discussion and are not publicly documented.

## Models

Oli Freuler wrote these skills with Claude (Opus 5.5 and Fable 5.1, in Claude Code) and Codex. Codex, DeepSeek, Kimi
and TypeSafe Jev served as reviewers along the way. On 25 Oct 2026, before release, separate review agents (Claude Opus 5.5
and Fable 5.1) read every published file for leaked data and missing credit, and their findings were applied.

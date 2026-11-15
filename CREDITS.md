# Credits

Each entry names the person or project, what we took from them, where it shows up in this repository, and the
licence that covers their own work. "Derived from" means a skill restates or adapts their published material.
"Inspired by" means we took an idea or a practice and wrote our own text. We copy no third-party code or text except the
MIT-licensed templates in `skills/research-loop` and the MIT-licensed `skills/stop-slop`.

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
| BitWonka | The public greedyfrog rows of 27-28 Oct 2026, their notes and source: a Euclid walk whose state carries its own reverse decisions. Our text is a reconstruction; his prompts and prototypes are not public. | `greedyfrog-method` (derived from) | the rows and notes, cited by commit and line |
| BitWonka | His working practice as it shows in his public ecdsa.fail notes and in ecdsafail-tools: the exact evaluator replica, the calibrated static proxy, the reference model, the scoring-surface audit, lever switches with break controls, the fit probe, the inert-op screen. Numbers are quoted from the notes; none was re-measured. | `exact-evaluator-replica`, `calibrated-static-cost-proxy`, `reference-model-as-instrument`, `evaluator-scoring-surface-audit`, `lever-switches-and-break-controls`, `fit-probe-and-splice`, `inert-op-screen-to-structural-rule` (derived from) | the notes, cited as `N:<id>:<line>`; [BitWonka/ecdsafail-tools](https://github.com/BitWonka/ecdsafail-tools), no licence file, not copied |
| gnuchev (Vasily Gnuchev) | 167 public ecdsa.fail submission notes. | `ecdsafail-pareto-ratchet`, `ecdsafail-scratch-diet` and their digests (derived from) | the notes, cited by line |
| gnuchev (Vasily Gnuchev) | Open Research Club's two-model review practice, including its review-record fields. | `cross-model-review-gate` (derived from) | [gnuchev/openresearch-club](https://github.com/gnuchev/openresearch-club), Apache-2.0 |
| bulengerk | 81 public ecdsa.fail submission notes: nine left moves and their descents. | `beachhead-ratchet`, `invariant-chart`, `shot-autopsy` (derived from) | the notes, cited by submission id |
| Jieyi Long and co-authors | The ECDSA.Fail paper (arXiv:2609.09582), its supplemental materials, the record-and-replay paper (arXiv:2609.28882), the ecdsafail_skills suite and the GPU island toolkit. | `notes/papers`; `ecdsafail-oracle-loop` points to the GPU island toolkit | [ecdsafail_skills](https://github.com/jieyilong/ecdsafail_skills) (no licence file), [ecdsafail_gpu_toolkit](https://github.com/jieyilong/ecdsafail_gpu_toolkit) (MIT), [supplemental materials](https://github.com/jieyilong/ecdsafail-supplemental-materials) (no licence file) |
| nasqret (Bartosz Naskrecki) | Broad qubit sweeps and memory-mechanism recombination. | `nasqret-playbook` (inspired by) | [nasqret](https://github.com/nasqret) |
| nasqret (Bartosz Naskrecki) | His public Q660 and Q659 rows of 7-8 Nov 2026 (6d94a56a, 2e59f5be, 32ace839, 963dfad0, 4527e9d7, 15df559e, 389f99c3, 119047a6), their notes and public source: the exact post-pass chain, the commuting fold and the carry lending. | `exact-postpass-stack`, `bounded-commuting-fold`, `hosted-carry-lending` (derived from) | the rows and notes, cited by row id |
| Akashneelesh | His public ecdsa.fail rows and notes of the Q765 line (b297b7cd to ae715bcf, November 2026), and the public source of row ae715bcf read against its public parent d4dd7eb1. The method and every circuit are his and his credited lineage's; the notes are paraphrased, not copied. Our 763, 762 and 761 rows of 15 Nov 2026 are built on his 765 frame, row 8396ec91. | `paged-walk-descent` and its reference (derived from); `notes/campaign-2026-11-14-metalane.md` | the rows and notes, cited by row id |
| zuiris (Maksim) | His public Leapfrog product-line rows (e3b5c51f, 4cb9cf01, 39f92d49, d34ea609, f253a5ed, db050300) with their validate commits, and his 5 Nov 2026 batch (Q768-780, Q740) with 47 public notes. His generators are not public; the skills reconstruct the method from rows, notes and source. | `structural-binder-walk`, `zuiris-method` (derived from) | the rows and notes, cited by row id |
| zuiris (Maksim) | The hold pass of his public 740-wide row 94ce452b. Our Leiterli rows stand on our own row 34f7b24c, which stands on his, and give that pass extra always-zero wires. No code of his is in this repository. | `notes/campaign-2026-11-14-metalane.md`, `tools/brotofe` (describes the pipeline) | his public row |
| haotang1995 | Two public ecdsa.fail record notes of 29 Oct 2026 (b0380209, e5f4dddc) and his public environment-setup repository: the exact hold pass, the failure-rate exchange, the role-separated research pipeline. | `exact-hold-pass`, `lambda-exchange-desk`, `auto-autoresearch-pipeline` (derived from) | the notes, cited by submission id; [env-setup-neovim-tmux-wezterm-ai](https://github.com/haotang1995/env-setup-neovim-tmux-wezterm-ai) |
| jackylee0424 | His public research lab and 130 public ecdsa.fail notes (spookyfrog series), and the Q658 row a6098537: the leader-rebase patch stack, hash-pinned edit tables, the lane eviction. | `leader-rebase-stack`, `pinned-table-stacking`, `role-lane-eviction` (derived from) | [shor-ecdlp-contest](https://github.com/jackylee0424/shor-ecdlp-contest), MIT; the notes, cited by row |
| Teddy Pender (teddyjfpender) | Posted the August 2026 row that opened the ping-pong family; co-author of the record-and-replay paper. | `notes/papers/long-2026-record-and-replay.md` | [teddyjfpender/ecdsafail-challenge](https://github.com/teddyjfpender/ecdsafail-challenge) |
| Teddy Pender (teddyjfpender) | The move his 21 Aug 2026 row demonstrated: a structurally free descent beside the protected leader. The rules are our own reading of that public row, not his words. | `burn-the-house-down` (inspired by) | his public row |
| Jo and Lee | Exact in-place modular inversion (eprint 2026/2014): the lemmas behind the invariant checkers. The checker code is ours. | `reversible-circuit-invariants` (derived from) | the paper |
| tanweai and the PUA contributors | The repeated-failure method and completion-evidence checklist of the PIP edition. We wrote our own cards and left out its hooks, telemetry and pressure rhetoric. | `agent-unstuck`, `pip-discipline`, `ecdsafail-oracle-loop` (inspired by) | [tanweai/pua](https://github.com/tanweai/pua), no licence file |
| ShouqiaoW and OpenAI | Contract-style prompts for open problems (the erdos prompts, OpenAI's Cycle Double Cover prompt). Paraphrased, not copied. | `hard-problem-contract` (inspired by) | [ShouqiaoW/erdos](https://github.com/ShouqiaoW/erdos), MIT |
| Erich Friedman and the packing literature | Known square packings that set the starting frontier: Friedman's records, Ellsworth, Goebel, and the strip constructions of Erdős and Graham, Chung and Graham, Bui, and McClenagan. | `squares-in-squares-campaign` | [Packing Center](https://erich-friedman.github.io/packing/squinsqu/) |

## Papers behind the reversible-arithmetic research skills

Each `quantum-*` skill assesses whether one published mechanism transfers to a real circuit, and names its source
in its text or in `references/paper.md`: dense-encoding QROM (arXiv:2610.02321), Bona (arXiv:2608.08765),
"Discovering state-of-the-art quantum circuits with large language models" (arXiv:2610.22367), encoded reversible
addition (arXiv:2610.41142), MBUndo (arXiv:2611.02345), record-and-replay (arXiv:2609.28882), "Measurement-Based
Uncomputation from an Error Correction Perspective" (arXiv:2609.31605), agentic compilation (arXiv:2610.23832),
Khattar and Gidney on conditionally clean ancillae (arXiv:2407.17966), Hietala et al. on register permutations
(arXiv:1912.02250), and work on Boolean expansions and multiplicative complexity (arXiv:2601.02515,
arXiv:1407.6169). The skills restate no paper text; they say what to check before believing a transfer.

## Tools

The scripts under `tools/` are our own (MIT). What they lean on, none of it copied here:

- **BitWonka's fasteval** is the exact evaluator the gates and the verifier call. It has no licence file, so it is
  not bundled: Tüpflischiisser, Gwüssesbiss and Brotofe expect you to fetch it.
- **The `GLV1` gate-list format** that Fadespüeli reads is the one in which the public rows of Akashneelesh's Q765
  line ship their end machines.
- **Zileprob** tests a transfer of arXiv:2609.05625 (Häner, Tripier, Young et al., 2026) against the row emitter of
  Akashneelesh's public 765 frame (row 8396ec91).
- **Google's `colab` CLI** and **Antigravity CLI** (`agy`), **OpenAI's Codex CLI**, **Moonshot's Kimi Code CLI** and
  **Groq's API** are what Wolkeschieber, Besserwüsser and Stafettestab drive.
- The rows the campaign note cites stand on public parents credited in their own submission notes.

## Writing style

The README, the campaign note and the tool READMEs were edited with
[stop-slop-refined](https://github.com/welttowelt/stop-slop-refined) (welttowelt and contributors, MIT), which is
also vendored unchanged, apart from its title line, as `skills/stop-slop` with its LICENSE and ATTRIBUTION.md. That
skill names its own inspirations: Hardik Pandya's stop-slop, Conor Bronsdon's avoid-ai-writing, Siqi Chen's
humanizer and Jalaaldeen's anti-ai-slop-writing.

## Solvers cited in the digests

The ecdsa.fail digests quote public rows and notes by jackylee0424, mochimodev, krishparadox, dysnasia, kaankolcu,
MonitSharma, edi3on, SnehalRaj, gopikannappan, zuiris and others. The Proximity Prize digest credits 0xLucqs for the
68.05 construction and cites zkfriendly's submission. Every quote points at the author's own note or pull request.

## Proximity Prize Discussion #537

The 116.13 upper-track digest summarises the public thread by BitWonka, dtumad, hybridnoise, yoyo930021, GordoAR,
jieyilong, CrystallineButterfly, lamb356 and raresbuhai, with each claim attributed to its author.

## Tools and services

[TypeSafe](https://github.com/typesafe-ai/skills) (Jev, MIT skill), [Elicit](https://elicit.com) (API),
[arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) by blazickjp (used by arxiv-portable-research, not bundled),
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

The November 2026 additions (44 skills of our own, one vendored, `tools/`, the campaign note, the Swiss German names) come from campaign
material written with Claude Fable 5.2, Opus 5.5 and Sonnet 5.5, Codex, Kimi Code, and Gemini 4 Carbon and Argon.
Claude Fable 5.2 sanitized and assembled them on 15 Nov 2026. A separate Claude Fable 5.2 agent then read the
whole change with the brief to refute that it was safe to publish; it found private lane material in four skills,
group-chat quotes in one, wrong facts in the campaign note and bugs in six tools. Those findings were applied,
with two exceptions: the names Tüpflischiisser (which it called scatological) and Besserwüsser (which it said
sits on another vendor's model) were kept. A second pass by the same agent read all but one of the new skills in full
and found unpublished measurements in three more and one skill that did not belong here; those were fixed or
removed.

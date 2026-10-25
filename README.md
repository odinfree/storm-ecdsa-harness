# Storm skills

Agent skills for long optimization campaigns on open benchmarks. They come out of our work since June 2026 on
[ecdsa.fail](https://ecdsa.fail) (quantum circuits for secp256k1 point addition), the
[Proximity Prize](https://better.codes) (Lean proofs about codes) and Kaggle's "Squares in Squares", and from the
people whose public notes taught us most of what is here.

Each skill is a folder with a `SKILL.md` that Claude Code, Codex and other agents load when a task calls for it.
Where a skill is built on someone else's work, the table says so, and [CREDITS.md](CREDITS.md) gives the source and
licence.

## Install

```bash
git clone https://github.com/odinfree/storm-ecdsa-harness.git
cd storm-ecdsa-harness
./install.sh
```

`install.sh` links every skill into `~/.claude/skills` and `~/.codex/skills`, and into `~/.agents/skills` when that
directory exists. It never replaces a skill you already have. To take a single skill, copy its folder into your
agent's skills directory. On Windows, clone with `git -c core.symlinks=true` so `skills/agent-unstuck` resolves.

`agent-unstuck` also works without installing anything. Give your agent this URL:
`https://raw.githubusercontent.com/odinfree/storm-ecdsa-harness/main/skills/agent-unstuck.md`

## Skills

### Working with agents

| Skill | What it does | Built on |
|---|---|---|
| [agent-unstuck](skills/agent-unstuck.md) | Gets a stuck agent moving: diagnose the failure, test another explanation, verify before claiming success | tanweai/pua |
| [pip-discipline](skills/pip-discipline/SKILL.md) | Recovers a stalled ecdsa.fail lane with evidence instead of another parameter tweak | tanweai/pua |
| [mission-command](skills/mission-command/SKILL.md) | Runs one bounded mission with stated authority, one owner and a falsifiable closeout | Original |
| [hard-problem-contract](skills/hard-problem-contract/SKILL.md) | Frames a hard, decidable problem so the agent cannot settle for a partial answer | OpenAI's Cycle Double Cover prompt, ShouqiaoW/erdos |
| [deepseek-pressure-test](skills/deepseek-pressure-test/SKILL.md) | Has an outside model try to kill a route before you spend compute on it | Original (Storm harness) |
| [cross-model-review-gate](skills/cross-model-review-gate/SKILL.md) | Gets a second lab's model to review the work, recorded against the exact commit | gnuchev's Open Research Club |
| [send-to-claude-fable](skills/send-to-claude-fable/SKILL.md) | Hands a bounded task to Claude Fable and brings back its verdict | Original |
| [jev-second-perspective](skills/jev-second-perspective/SKILL.md) | Uses TypeSafe's Jev to rank levers or check claims against a lab log | TypeSafe |

### Research and measurement

| Skill | What it does | Built on |
|---|---|---|
| [research-loop](skills/research-loop/SKILL.md) | Runs a queue of research questions that refills itself, with parallel researcher agents | BitWonka's loop-engine (MIT) |
| [elicit-research](skills/elicit-research/SKILL.md) | Searches papers and runs systematic reviews through the Elicit API | Elicit |
| [verify-research-transfer](skills/verify-research-transfer/SKILL.md) | Checks that a paper supports an optimization before anyone builds it | Original |
| [verify-paired-native-measurements](skills/verify-paired-native-measurements/SKILL.md) | Audits paired benchmark evidence before a result is admitted | Original |
| [portable-source-assertions](skills/portable-source-assertions/SKILL.md) | Keeps Python AST source checks stable across interpreter versions | Original |
| [rust-archive-build-binding](skills/rust-archive-build-binding/SKILL.md) | Stops stale Cargo artifacts from contaminating benchmark comparisons | Original |

### ecdsa.fail circuits

| Skill | What it does | Built on |
|---|---|---|
| [ecdsafail-oracle-loop](skills/ecdsafail-oracle-loop/SKILL.md) | Iterates until the official evaluator says better, with a route journal that survives compaction | tanweai/pua (loop discipline) |
| [ecdsafail-fasteval](skills/ecdsafail-fasteval/SKILL.md) | Scores an `ops.bin` exactly like `eval_circuit`, in minutes, at about 20 bytes per op instead of 56 | BitWonka's fasteval |
| [ecdsafail-lowq-playbook](skills/ecdsafail-lowq-playbook/SKILL.md) | Takes qubits off a low-Q stream: census, cut, refactor, then budget lambda | BitWonka's 26 public notes |
| [ecdsafail-pareto-ratchet](skills/ecdsafail-pareto-ratchet/SKILL.md) | Holds Pareto rows with exact cuts and one-dial band sweeps | gnuchev's 167 public notes |
| [ecdsafail-scratch-diet](skills/ecdsafail-scratch-diet/SKILL.md) | Replaces clean scratch at the binding instant with borrowed, literal or re-encoded forms | gnuchev's October notes, our public rows |
| [beachhead-ratchet](skills/beachhead-ratchet/SKILL.md) | Takes a left move that costs Toffoli, then wins the cost back on your own tree | bulengerk's public notes |
| [invariant-chart](skills/invariant-chart/SKILL.md) | Drops register bits that an algebraic relation already determines | bulengerk's public notes |
| [shot-autopsy](skills/shot-autopsy/SKILL.md) | Turns a candidate-only failing shot into a named defect and a permanent regression | bulengerk's public notes |
| [circuit-edit-integration-safety](skills/circuit-edit-integration-safety/SKILL.md) | Finds why a primitive that is clean on its own dirties the full circuit | Original (Storm harness) |
| [route-compare-probe-discipline](skills/route-compare-probe-discipline/SKILL.md) | Compares baseline and candidate on the same shots before blaming one call | Original (Storm harness) |
| [nasqret-playbook](skills/nasqret-playbook/SKILL.md) | Rebuilds the route slate when a frontier move changes the search | nasqret's sweeps |

### Proofs and exact math

| Skill | What it does | Built on |
|---|---|---|
| [proximity-prize-campaign](skills/proximity-prize-campaign/SKILL.md) | Runs a Proximity Prize proof lane against the live frontier, with digests of the public record | BitWonka's 31 notes, the Discussion #537 authors |
| [proximity-prize-frontier-archaeology](skills/proximity-prize-frontier-archaeology/SKILL.md) | Compares each accepted proof only with its accepted predecessor | Original |
| [accepted-proof-exact-retune](skills/accepted-proof-exact-retune/SKILL.md) | Finds the smallest strict score step an accepted proof allows | Original |
| [lean-arklib-proofs](skills/lean-arklib-proofs/SKILL.md) | Formalizes claims in Lean 4 with ArkLib and gates them on a clean build and axiom audit | ArkLib, Mathlib |
| [fast-lean-proof-loop](skills/fast-lean-proof-loop/SKILL.md) | Speeds up Lean proof iteration without weakening the final gate | Original |
| [lean-finite-certificate-splitting](skills/lean-finite-certificate-splitting/SKILL.md) | Cuts kernel memory on large finite certificates | Original |
| [computer-algebra-oracles](skills/computer-algebra-oracles/SKILL.md) | Routes exact algebra questions to the right computer algebra system, with replayable output | Original |
| [constraint-construction-search](skills/constraint-construction-search/SKILL.md) | Encodes finite searches for SAT, SMT, CP-SAT or MIP and audits the result | Original |
| [exact-search-engineering](skills/exact-search-engineering/SKILL.md) | Builds exact searches in FLINT, Nemo, Julia, C++ or Rust | Original |

### Kaggle

| Skill | What it does | Built on |
|---|---|---|
| [squares-in-squares-campaign](skills/squares-in-squares-campaign/SKILL.md) | Packs unit squares into the smallest square: metric gates, tools, frontier structure, dead routes | Erich Friedman's packing records and the Kaggle community |

## Literature notes

[notes/papers](notes/papers/README.md) holds 24 short notes on the work behind these circuits: 22 papers, from Proos and Zalka
(2003) to the 2026 ECDSA.Fail paper, plus the October 2026 PR lineage and the public toolchains. Each note gives the
citation, the key result and the trick worth knowing.

## What is not here

Our own unpublished plans for boards that are still running stay private: ecdsa.fail, provably.fast, the Proximity
Prize and the QCC Kaggle competition. The skills here that touch live boards describe public records only. Kaggle's
rules forbid sharing competition code outside the team while a competition runs.

The first Storm harness (route packets, gate scripts, the Zellij control plane, June to July 2026) is still in the
git history at commit [`dd6a173`](https://github.com/odinfree/storm-ecdsa-harness/tree/dd6a173).

## Thank you

These skills exist because people did their work in the open.

- **BitWonka** wrote fasteval and dead-ccx-finder, the loop-engine harness behind research-loop, and 57 detailed
  public notes on ecdsa.fail and the Proximity Prize.
- **gnuchev (Vasily Gnuchev)** published 167 ecdsa.fail notes that taught us the Pareto ratchet and the scratch diet,
  and showed in the Open Research Club how two models from different labs can review each other.
- **bulengerk** made the left moves behind beachhead-ratchet, invariant-chart and shot-autopsy, and explained each
  one in the notes.
- **Jieyi Long** and co-authors wrote the ECDSA.Fail paper and its supplemental materials. Jieyi Long also published
  the ecdsafail_skills suite and the GPU island toolkit.
- **nasqret (Bartosz Naskręcki)** showed what broad qubit sweeps and mechanism recombination can do.
- **Teddy Pender** posted the August 2026 row that opened the ping-pong family, and co-wrote the record-and-replay paper.
- **jackylee0424, mochimodev, krishparadox, dysnasia, kaankolcu, MonitSharma, edi3on, SnehalRaj, gopikannappan** and
  every other ecdsa.fail solver whose public rows and notes the digests cite.
- **dtumad, hybridnoise, yoyo930021, GordoAR, CrystallineButterfly, lamb356 and raresbuhai**, who worked through the
  116.13 upper-track wall with BitWonka and Jieyi Long in Proximity Prize Discussion #537, and **0xLucqs, zkfriendly**
  and the other Proximity Prize solvers whose public submissions the digests cite.
- **The ecdsa.fail team** at Layr-Labs, with Gautham Anant, built the open benchmark from the code and data Google
  Quantum AI published with its 2026 paper. **Yukon and zkSecurity** run the Proximity Prize. **Kaggle** ran Squares in Squares.
- **tanweai and the PUA contributors** for the evidence discipline in agent-unstuck, pip-discipline and the oracle loop.
- **TypeSafe** (Jev), **Elicit**, **Trail of Bits** (TrailMix), **kepano** (defuddle), and the authors of every paper
  cited in the notes and digests.
- **Gajesh Naik, newjordan (Frosty40), Sam (karnot.xyz), zuiris (Maksim) and Justin Drake**, whose ideas shaped the
  first Storm harness.

Oli Freuler ([odinfree](https://github.com/odinfree)) wrote these skills with Claude and Codex; [CREDITS.md](CREDITS.md)
has sources, licences and how each skill was reviewed. If a credit is missing or wrong, please
[open a credit correction](https://github.com/odinfree/storm-ecdsa-harness/issues/new?template=credit-correction.md).

## License

MIT for our own text and code (see [LICENSE](LICENSE)). `skills/research-loop` keeps BitWonka's MIT licence.
Everything we learned from someone else is credited in [CREDITS.md](CREDITS.md). Apart from research-loop's MIT
templates, no third-party code is bundled.

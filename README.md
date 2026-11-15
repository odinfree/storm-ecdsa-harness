# Storm skills

Skills and tools for agents that run long optimization campaigns on open benchmarks. We wrote them between June and
November 2026 while working on [ecdsa.fail](https://ecdsa.fail) (quantum circuits for secp256k1 point addition), the
[Proximity Prize](https://better.codes) (Lean proofs about codes) and Kaggle's "Squares in Squares". Most of what
they say we learned from other solvers' public notes.

A skill is a folder with a `SKILL.md`. Claude Code, Codex and other agents load it when a task calls for it. Where a
skill rests on someone else's work, its table row names them, and [CREDITS.md](CREDITS.md) gives the source and
licence.

A [tool](#tools) is a script from our November 2026 ecdsa.fail campaign with our paths, accounts and hosts taken
out.

Every skill and tool has a Swiss German name beside its technical id. [NAMES.md](NAMES.md) lists them.

## Install

```bash
git clone https://github.com/odinfree/storm-ecdsa-harness.git
cd storm-ecdsa-harness
./install.sh
```

`install.sh` links every skill into `~/.claude/skills` and `~/.codex/skills`, and into `~/.agents/skills` when that
directory exists. It never replaces a skill you already have. To take a single skill, copy its folder into your
agent's skills directory. On Windows, clone with `git -c core.symlinks=true` so `skills/agent-unstuck` resolves.

The tools are not installed: run them from the clone. Each tool's README lists what it needs.

`agent-unstuck` also works without installing anything. Give your agent this URL:
`https://raw.githubusercontent.com/odinfree/storm-ecdsa-harness/main/skills/agent-unstuck.md`

## Skills

Agents load a skill by its id: the folder name and the frontmatter `name`. The Swiss name is in the title of each
SKILL.md.

### Working with agents

| Swiss name | Translation | Id | What it does | Built on |
|---|---|---|---|---|
| Chnorzlöser | knot-undoer: the one who ends the fumbling | [agent-unstuck](skills/agent-unstuck.md) | Gets a stuck agent moving: diagnose the failure, test another explanation, verify before claiming success | tanweai/pua |
| Tätschmeischter | drill master | [pip-discipline](skills/pip-discipline/SKILL.md) | Makes a stalled ecdsa.fail lane produce evidence before it tweaks another parameter | tanweai/pua |
| Chefli | little boss | [mission-command](skills/mission-command/SKILL.md) | Runs one bounded mission with stated authority, one owner and a falsifiable closeout | Original |
| Chnacknuss | hard nut to crack | [hard-problem-contract](skills/hard-problem-contract/SKILL.md) | Frames a hard, decidable problem so the agent cannot settle for a partial answer | OpenAI's Cycle Double Cover prompt, ShouqiaoW/erdos |
| Dampfchochtopf | pressure cooker | [deepseek-pressure-test](skills/deepseek-pressure-test/SKILL.md) | Has an outside model try to kill a route before you spend compute on it | Original (Storm harness) |
| Gägeläser | counter-reader | [cross-model-review-gate](skills/cross-model-review-gate/SKILL.md) | Gets a second lab's model to review the work, recorded against the exact commit | gnuchev's Open Research Club |
| Märlitante | fairy-tale auntie | [send-to-claude-fable](skills/send-to-claude-fable/SKILL.md) | Hands a bounded task to Claude Fable and brings back its verdict | Original |
| Schiedsrichterli | little referee | [jev-second-perspective](skills/jev-second-perspective/SKILL.md) | Uses TypeSafe's Jev to rank levers or check claims against a lab log | TypeSafe |
| Abbruchbire | wrecking ball | [burn-the-house-down](skills/burn-the-house-down/SKILL.md) | Escapes a local optimum by running a structurally free descent beside the protected incumbent | Teddy Pender's August 2026 row |
| Fliessband | assembly line | [auto-autoresearch-pipeline](skills/auto-autoresearch-pipeline/SKILL.md) | Splits an autonomous campaign into five roles so that no worker measures its own work | haotang1995's public notes |
| Huckepack | piggyback | [leader-rebase-stack](skills/leader-rebase-stack/SKILL.md) | Keeps your work as an ordered stack of idempotent patches that rebase onto whichever row leads | jackylee0424's public lab (MIT) and notes |
| Wolkefahrplan | cloud timetable | [colab-lane](skills/colab-lane/SKILL.md) | Runs jobs on Google Colab from the terminal, and says what each failure means and what a job costs | Original |
| Schwafelbräms | waffle brake | [stop-slop](skills/stop-slop/SKILL.md) | Removes common AI writing patterns from prose, or only flags them | welttowelt's stop-slop-refined (MIT, vendored) |
| Schuumlöffel | skimming ladle | [vacuous-evidence-audit](skills/vacuous-evidence-audit/SKILL.md) | Asks of every passing check whether it could have failed, when many agents merge small changes into one tree | Original (our 793-to-792 rung) |
| Verchehrskadett | traffic cadet | [quantum-structural-lanes](skills/quantum-structural-lanes/SKILL.md) | Sets the order of structural circuit research: mine the records, admit the paper, price the cliff, then gate | Original |

### Research and measurement

| Swiss name | Translation | Id | What it does | Built on |
|---|---|---|---|---|
| Hamsterrädli | hamster wheel | [research-loop](skills/research-loop/SKILL.md) | Runs a queue of research questions that refills itself, with parallel researcher agents | BitWonka's loop-engine (MIT) |
| Läseratte | reading rat (bookworm) | [elicit-research](skills/elicit-research/SKILL.md) | Searches papers and runs systematic reviews through the Elicit API | Elicit |
| Papiertiger | paper tiger | [verify-research-transfer](skills/verify-research-transfer/SKILL.md) | Checks that a paper supports an optimization before anyone builds it | Original |
| Zwillingswaag | twin scales | [verify-paired-native-measurements](skills/verify-paired-native-measurements/SKILL.md) | Audits paired benchmark evidence before a result is admitted | Original |
| Zügelchischte | moving box | [portable-source-assertions](skills/portable-source-assertions/SKILL.md) | Keeps Python AST source checks stable across interpreter versions | Original |
| Roschtchlämmerli | rust clothes-peg | [rust-archive-build-binding](skills/rust-archive-build-binding/SKILL.md) | Stops stale Cargo artifacts from contaminating benchmark comparisons | Original |
| Stärnegucker | stargazer | [arxiv-portable-research](skills/arxiv-portable-research/SKILL.md) | Mines arXiv papers and their LaTeX for mechanisms that transfer into a real implementation | Original (uses blazickjp's arxiv-mcp-server) |
| Doppelgängerli | little double | [exact-evaluator-replica](skills/exact-evaluator-replica/SKILL.md) | Builds and validates a fast, exact local copy of a benchmark's official evaluator | BitWonka's fasteval and public notes |
| Chliidruckts | the fine print | [evaluator-scoring-surface-audit](skills/evaluator-scoring-surface-audit/SKILL.md) | Reads the evaluator and scoring source for gaps between what is counted, checked and assumed | BitWonka's public notes |
| Stimmgable | tuning fork | [reference-model-as-instrument](skills/reference-model-as-instrument/SKILL.md) | Writes the exact classical reference model first and uses it as oracle, table generator, replayer and scanner | BitWonka's public notes |
| Pi-mal-Duume | pi times thumb (rule of thumb) | [calibrated-static-cost-proxy](skills/calibrated-static-cost-proxy/SKILL.md) | Computes the judged cost inside the generator and calibrates it against the official judge | BitWonka's public notes |
| Sicherigschaschte | fuse box | [lever-switches-and-break-controls](skills/lever-switches-and-break-controls/SKILL.md) | Lands each lever behind a default-on constant, with numbered deliberate breakages the tests must catch | BitWonka's public notes |
| Umchleidikabine | fitting room | [fit-probe-and-splice](skills/fit-probe-and-splice/SKILL.md) | Measures whether a foreign module builds under your cap, then imports it verbatim through an adapter | BitWonka's public notes |
| Fuulpelzfänger | lazybones catcher | [inert-op-screen-to-structural-rule](skills/inert-op-screen-to-structural-rule/SKILL.md) | Finds charged ops that never act on the verifier's inputs, then replaces the index list with a structural rule | BitWonka's notes and dead-ccx-finder |

### ecdsa.fail circuits

| Swiss name | Translation | Id | What it does | Built on |
|---|---|---|---|---|
| Chrischtallchugle | crystal ball | [ecdsafail-oracle-loop](skills/ecdsafail-oracle-loop/SKILL.md) | Iterates until the official evaluator says better, with a route journal that survives compaction | tanweai/pua (loop discipline) |
| Schnällrichter | summary judge | [ecdsafail-fasteval](skills/ecdsafail-fasteval/SKILL.md) | Scores an `ops.bin` exactly like `eval_circuit`, in minutes, at about 20 bytes per op where the original needs 56 | BitWonka's fasteval |
| Schmalhans | skinny Hans (short rations) | [ecdsafail-lowq-playbook](skills/ecdsafail-lowq-playbook/SKILL.md) | Takes qubits off a low-Q stream: census, cut, refactor, then budget lambda | BitWonka's 26 public notes |
| Rätschi | the ratchet (also: a chatterbox) | [ecdsafail-pareto-ratchet](skills/ecdsafail-pareto-ratchet/SKILL.md) | Holds Pareto rows with exact cuts and one-dial band sweeps | gnuchev's 167 public notes |
| Hungerkur | starvation diet | [ecdsafail-scratch-diet](skills/ecdsafail-scratch-diet/SKILL.md) | Replaces clean scratch at the binding instant with borrowed, literal or re-encoded forms | gnuchev's October notes, our public rows |
| Brüggechopf | bridgehead | [beachhead-ratchet](skills/beachhead-ratchet/SKILL.md) | Takes a left move that costs Toffoli, then wins the cost back on your own tree | bulengerk's public notes |
| Schatzchärtli | little treasure map | [invariant-chart](skills/invariant-chart/SKILL.md) | Drops register bits that an algebraic relation already determines | bulengerk's public notes |
| Liicheschau | post-mortem | [shot-autopsy](skills/shot-autopsy/SKILL.md) | Turns a candidate-only failing shot into a named defect and a permanent regression | bulengerk's public notes |
| Bastelunfall | craft accident | [circuit-edit-integration-safety](skills/circuit-edit-integration-safety/SKILL.md) | Finds why a primitive that is clean on its own dirties the full circuit | Original (Storm harness) |
| Öpfel-und-Bire | apples and pears | [route-compare-probe-discipline](skills/route-compare-probe-discipline/SKILL.md) | Compares baseline and candidate on the same shots before blaming one call | Original (Storm harness) |
| Rundumschlag | sweeping blow | [nasqret-playbook](skills/nasqret-playbook/SKILL.md) | Rebuilds the route slate when a frontier move changes the search | nasqret's sweeps |
| Blätterteig | puff pastry | [paged-walk-descent](skills/paged-walk-descent/SKILL.md) | Takes a cheaper public walk a few qubits wider and buys the qubits back with a page of low bits; includes a checklist for reviewing such a row | Akashneelesh's 17 public rows |
| Flaschehals | bottleneck | [structural-binder-walk](skills/structural-binder-walk/SKILL.md) | Moves the binding constraint of a product-score line with one structural mechanism per row | zuiris's public product-line rows |
| Wiissblatt | blank sheet | [zuiris-method](skills/zuiris-method/SKILL.md) | Checks whether a new inverter family fits a target width before building it, then releases it as a dial | zuiris's 5 Nov 2026 rows and notes |
| Gumpifrosch | hopping frog | [greedyfrog-method](skills/greedyfrog-method/SKILL.md) | Redesigns a reversible Euclid walk so the state carries its own reverse decisions | BitWonka's greedyfrog rows and notes |
| Pfandleihi | pawn shop | [exact-hold-pass](skills/exact-hold-pass/SKILL.md) | Runs an exact final pass that lends duplicated values and holds repeated products | haotang1995's public notes |
| Wächselstube | exchange bureau | [lambda-exchange-desk](skills/lambda-exchange-desk/SKILL.md) | Prices statistical trades at a fixed Toffoli-per-failure rate, with paired measurements and an out-of-sample guard | haotang1995's public notes |
| Milchbüechli | the little milk ledger | [hold-demand-ledger](skills/hold-demand-ledger/SKILL.md) | Measures the hold and loan economy of a record tree, with the four traps we fell into | Original (measured on a public record tree) |
| Tällerturm | tower of plates | [pinned-table-stacking](skills/pinned-table-stacking/SKILL.md) | Pins declarative edit tables to an exact gate list by length and hash and stacks them in call order | jackylee0424's public notes |
| Zwangsrüümig | forced eviction | [role-lane-eviction](skills/role-lane-eviction/SKILL.md) | Removes a whole scratch lane from a width-pinned circuit by rewriting every site that touches it | jackylee0424's Q658 row |
| Nachputzete | the cleaning after the cleaning | [exact-postpass-stack](skills/exact-postpass-stack/SKILL.md) | Ports or stacks exact stream-level post-passes on a finished op stream | nasqret's public Q660 rows |
| Faltschachtle | folding box | [bounded-commuting-fold](skills/bounded-commuting-fold/SKILL.md) | Cancels commuting gate pairs exactly on billion-op streams in bounded memory | nasqret's public notes and source |
| Untermieter | subtenant | [hosted-carry-lending](skills/hosted-carry-lending/SKILL.md) | Lends role wires that are proved clean during a column interval as exact scratch | nasqret's public 660 and 659 notes |
| Wurschtzipfel | sausage end | [schedule-tail-truncation](skills/schedule-tail-truncation/SKILL.md) | Cuts identical end-padding columns from a fixed walk schedule and prices the cut as a declared failure-rate trade | Original (our 660 and 659 rows) |
| Gipfelbuech | summit register | [peak-lifetime-ledger](skills/peak-lifetime-ledger/SKILL.md) | Maps peak-qubit pressure by phase before anyone edits or scales compute | Original |
| Tabällechnächt | table farmhand | [gpu-affine-table-synthesis](skills/gpu-affine-table-synthesis/SKILL.md) | Searches affine and ESOP forms for small dirty-table predicates and re-verifies each winner exactly | Original |
| Ruckwärtsgang | reverse gear | [reversible-circuit-invariants](skills/reversible-circuit-invariants/SKILL.md) | Runs executable invariant checks for space-efficient reversible arithmetic before a build | Jo and Lee (eprint 2026/2014) |

### Reversible arithmetic research

| Swiss name | Translation | Id | What it does | Built on |
|---|---|---|---|---|
| Goldwäscher | gold panner | [quantum-record-mining](skills/quantum-record-mining/SKILL.md) | Mines existing circuit records for overlooked measured gains before any new paper-driven work | Original |
| Bauinspäkter | building inspector | [quantum-verified-architecture-search](skills/quantum-verified-architecture-search/SKILL.md) | Runs evaluator-guided structural search with independent value, phase and scratch checks | arXiv:2610.23832 |
| Sardinebüchs | sardine tin | [quantum-dense-qrom](skills/quantum-dense-qrom/SKILL.md) | Tests dense Pauli-encoded QROM as a replacement for coherent table lookups | arXiv:2610.02321 |
| Dräckfink | mucky pup | [quantum-dirty-borrowing](skills/quantum-dirty-borrowing/SKILL.md) | Checks whether a dirty-safe block can run where the peak sits | arXiv:2608.08765 (Bona) |
| Brösmelispur | trail of breadcrumbs | [quantum-divstep-reconstruction](skills/quantum-divstep-reconstruction/SKILL.md) | Replaces stored branch history with decisions reconstructed from the successor state | arXiv:2610.22367 |
| Gheimschrift | secret writing | [quantum-encoded-arithmetic](skills/quantum-encoded-arithmetic/SKILL.md) | Tests whether a stretch of arithmetic can stay encoded from input to output | arXiv:2610.41142 |
| Iitagsflüge | mayfly | [quantum-mbundo-lifetimes](skills/quantum-mbundo-lifetimes/SKILL.md) | Finds where an ancilla is last used, so it can be measured away there | arXiv:2611.02345 (MBUndo) |
| Widerchäuer | cud-chewer | [quantum-replay-arithmetic](skills/quantum-replay-arithmetic/SKILL.md) | Designs the GCD walk, its transcript and the payload replay together | arXiv:2609.28882 (record-and-replay) |
| Putzequipe | cleaning crew | [quantum-syndrome-uncompute](skills/quantum-syndrome-uncompute/SKILL.md) | Tests syndrome-based uncomputation where the garbage has structure to exploit | arXiv:2609.31605 |
| Spickzettel | crib sheet | [quantum-affine-lookup-synthesis](skills/quantum-affine-lookup-synthesis/SKILL.md) | Lowers the Toffoli cost of a small repeated lookup by sharing nonlinear terms across outputs | arXiv:2601.02515, arXiv:1407.6169 |
| Schnorrichaib | the scrounger | [quantum-borrowed-wire-counterexample](skills/quantum-borrowed-wire-counterexample/SKILL.md) | Proves or falsifies a recovery rule for a borrowed qubit with two colliding reachable states | Khattar and Gidney (arXiv:2407.17966) |
| Trennwändli | little partition wall | [quantum-graded-divider-placement](skills/quantum-graded-divider-placement/SKILL.md) | Prices a divider width cut by trading retained quotient tags against reconstruction | Original |
| Hüetlispiler | shell-game player | [quantum-guarded-permutation-audit](skills/quantum-guarded-permutation-audit/SKILL.md) | Finds wrong-branch swaps and stale caches when a chunked optimizer changes endpoints | Hietala et al. (arXiv:1912.02250) |
| Zwickmüli | double bind | [quantum-residue-scan-ambiguity](skills/quantum-residue-scan-ambiguity/SKILL.md) | Diagnoses a residue scan in which more than one label passes a truncated predicate | Original |

### Proofs and exact math

| Swiss name | Translation | Id | What it does | Built on |
|---|---|---|---|---|
| Nöchberli | little neighbour | [proximity-prize-campaign](skills/proximity-prize-campaign/SKILL.md) | Runs a Proximity Prize proof lane against the live frontier, with digests of the public record | BitWonka's 31 notes, the Discussion #537 authors |
| Scherbehuufe | heap of shards | [proximity-prize-frontier-archaeology](skills/proximity-prize-frontier-archaeology/SKILL.md) | Compares each accepted proof only with its accepted predecessor | Original |
| Schrüblidräier | turner of little screws | [accepted-proof-exact-retune](skills/accepted-proof-exact-retune/SKILL.md) | Finds the smallest strict score step an accepted proof allows | Original |
| Magerquark | low-fat curd (lean) | [lean-arklib-proofs](skills/lean-arklib-proofs/SKILL.md) | Formalizes claims in Lean 4 with ArkLib and gates them on a clean build and axiom audit | ArkLib, Mathlib |
| Blitzdiät | crash diet | [fast-lean-proof-loop](skills/fast-lean-proof-loop/SKILL.md) | Speeds up Lean proof iteration without weakening the final gate | Original |
| Schiitlispalter | kindling splitter | [lean-finite-certificate-splitting](skills/lean-finite-certificate-splitting/SKILL.md) | Cuts kernel memory on large finite certificates | Original |
| Rächeschieber | slide rule | [computer-algebra-oracles](skills/computer-algebra-oracles/SKILL.md) | Routes exact algebra questions to the right computer algebra system, with replayable output | Original |
| Zwangsjagge | straitjacket | [constraint-construction-search](skills/constraint-construction-search/SKILL.md) | Encodes finite searches for SAT, SMT, CP-SAT or MIP and audits the result | Original |
| Nadle-im-Heustock | needle in the haystack | [exact-search-engineering](skills/exact-search-engineering/SKILL.md) | Builds exact searches in FLINT, Nemo, Julia, C++ or Rust | Original |

### Kaggle

| Swiss name | Translation | Id | What it does | Built on |
|---|---|---|---|---|
| Plättlileger | tiler | [squares-in-squares-campaign](skills/squares-in-squares-campaign/SKILL.md) | Packs unit squares into the smallest square: metric gates, tools, frontier structure, dead routes | Erich Friedman's packing records and the Kaggle community |

## Tools

These scripts ran our November 2026 ecdsa.fail campaign. Paths, accounts and hosts are now arguments and
environment variables. Each tool is a folder under `tools/`, named with the ASCII spelling of its Swiss name, and
its README gives inputs, outputs, a run line and the limits. [The campaign note](notes/campaign-2026-11-14-metalane.md)
tells what each tool did and what seven mistakes cost us.

| Swiss name | Translation | Technical id | What it does |
|---|---|---|---|
| [Türhüeter](tools/tuerhueter/README.md) | doorkeeper | `claim-gate.py` | Refuses a submit while another lane holds an open claim on the account |
| [Briefchaschte](tools/briefchaschte/README.md) | letterbox | `submit-dir.sh` | Submits one row package after about thirty guards, or refuses and says why |
| [Pöschtler](tools/poeschtler/README.md) | postman | `submit-wait.sh` | Waits for a free account, claims, submits one row and waits for the grade |
| [Drängeler](tools/draengeler/README.md) | queue-jumper (reformed) | `submit-queue.sh`, `auto-submit.sh` | Submits a ladder of ready rows unattended, each through every gate |
| [Notizbüechli](tools/notizbuechli/README.md) | little notebook | `zmknote.py` | Writes a row's note, dependency list and claim from machine-read values, and refuses a note with a hole in it |
| [Wätterfrosch](tools/waetterfrosch/README.md) | weather frog | `board-refresh.sh` | Keeps a note-free six-column snapshot of the board current, with a heartbeat |
| [Äugli](tools/aeugli/README.md) | little eye | `board-own.sh` | Reads the board once, on demand, into a lane's own folder |
| [Wolkeschieber](tools/wolkeschieber/README.md) | cloud pusher | `colab-lane` | Runs one job on a Colab runtime until done, downloads the results and stops the runtime |
| [Hofhund](tools/hofhund/README.md) | yard dog | `colab-detached.sh`, `colab-watchdog.sh` | Detaches the Colab supervisor from the agent session and kills hung CLI calls |
| [Hartnäckler](tools/hartnaeckler/README.md) | stubborn one | `retry.sh` (three variants) | Retries a refused cloud launch until it is up or a deadline passes |
| [Brotofe](tools/brotofe/README.md) | bread oven | `zjob.sh` | Runs a batch of per-row jobs in parallel on a VM and packs the results every two minutes |
| [Tüpflischiisser](tools/tuepflischiisser/README.md) | nitpicker (said less politely) | `verify-server.sh`, `vq-put.sh` | Rebuilds queued rows the official way on a big VM and compares the hash to the last digit |
| [Gwüssesbiss](tools/gwuessesbiss/README.md) | pang of conscience | `macgate2.sh` | Runs the full gate for one candidate on a workstation, one heavy process at a time |
| [Erbsezähler](tools/erbsezaehler/README.md) | pea counter | `cnt.sh`, `qcount.rs` | Prices an edit with a count-only build and counts qubit ids independently |
| [Müschterli](tools/mueschterli/README.md) | little sample | `mk_fv3.py` | Makes a probe tree from a recipe in which every edit must apply exactly once |
| [Schnitzmässer](tools/schnitzmaesser/README.md) | whittling knife | `mk_bcuts.sh` | Carries the hunks of a patch that still apply onto another tree and reports the rest |
| [Fadespüeli](tools/fadespueeli/README.md) | thread spool | `align.py`, `gl.py` | Reads, replays and aligns gate lists |
| [Zileprob](tools/zileprob/README.md) | row rehearsal | `zeileprob.py` | Enumerates one 16-wire digit slot and shows that signed rows give wrong results in multi-class slots |
| [Besserwüsser](tools/besserwuesser/README.md) | know-it-all | `carbon-advisor` | Asks another vendor's model for an adversarial second opinion |
| [Stafettestab](tools/stafettestab/README.md) | relay baton | `codex.sh`, `kimi.sh`, `groq.py` | Hands a prompt file to another model in a fixed role and brings back the answer |
| [Trockeschwümmer](tools/trockeschwuemmer/README.md) | dry swimmer | `walksim` | Simulates inversion walks classically: steps, halvings and transcript bits per rule |

## Literature notes

[notes/papers](notes/papers/README.md) holds 24 short notes on the work behind these circuits: 22 papers, from Proos and Zalka
(2003) to the 2026 ECDSA.Fail paper, plus the October 2026 PR lineage and the public toolchains. Each note gives the
citation, the key result and the trick worth knowing.

## Campaign notes

[Lehrgäld](notes/campaign-2026-11-14-metalane.md) (tuition fees) covers the ecdsa.fail campaign of 13 to 16 Nov 2026:
five graded rows, what each tool did, and seven mistakes with their cost.

## What is not here

Our own unpublished plans for boards that are still running stay private: ecdsa.fail, provably.fast, the Proximity
Prize and the QCC Kaggle competition. The skills and tools here that touch live boards describe public records, our
own graded rows and our own measurements of public trees. Kaggle's rules forbid sharing competition code outside the
team while a competition runs.

We wrote several skills from campaign records: evidence files, review transcripts, forensics catalogues. Those
records stay private, and each such skill says so. The tools come without the recipes, offsets and hashes of
specific rows, and without fasteval, which you fetch from BitWonka's repository.

The first Storm harness (route packets, gate scripts, the Zellij control plane, June to July 2026) is still in the
git history at commit [`dd6a173`](https://github.com/odinfree/storm-ecdsa-harness/tree/dd6a173).

## Thank you

These skills exist because people did their work in the open.

- **BitWonka** wrote fasteval and dead-ccx-finder, the loop-engine harness behind research-loop, and 57 detailed
  public notes on ecdsa.fail and the Proximity Prize. The greedyfrog method and seven of the measurement skills
  (replica, proxy, reference model, scoring-surface audit, lever switches, fit probe, inert-op screen) are his
  practice, written down from those notes.
- **gnuchev (Vasily Gnuchev)** published 167 ecdsa.fail notes that taught us the Pareto ratchet and the scratch diet,
  and showed in the Open Research Club how two models from different labs can review each other.
- **bulengerk** made the left moves behind beachhead-ratchet, invariant-chart and shot-autopsy, and explained each
  one in the notes.
- **Jieyi Long** and co-authors wrote the ECDSA.Fail paper and its supplemental materials. Jieyi Long also published
  the ecdsafail_skills suite and the GPU island toolkit.
- **nasqret (Bartosz Naskręcki)** showed what broad qubit sweeps and mechanism recombination can do, and published the
  Q660 post-pass chain behind exact-postpass-stack, bounded-commuting-fold and hosted-carry-lending.
- **Akashneelesh** took Q765 down by 80 million Toffoli in 37 hours and wrote down how; paged-walk-descent is his
  method, and our 763, 762 and 761 rows are built on his 765 frame.
- **zuiris (Maksim)** published the product-line rows behind structural-binder-walk and the clean-sheet families behind
  zuiris-method, and the 740-wide tree with the hold pass that our ladder rows stand on.
- **haotang1995** described his hold pass, his failure-rate exchange and his research pipeline in two
  record notes.
- **jackylee0424** published his research lab and 130 notes: the patch stack, the pinned
  tables and the lane eviction come from there.
- **Teddy Pender** posted the August 2026 row that opened the ping-pong family, and co-wrote the record-and-replay paper.
  burn-the-house-down is our reading of how that row came about.
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

MIT for our own text and code, the tools included (see [LICENSE](LICENSE)). `skills/research-loop` keeps BitWonka's
MIT licence, and `skills/stop-slop` keeps its own MIT licence and attribution file.
Everything we learned from someone else is credited in [CREDITS.md](CREDITS.md). Apart from research-loop's MIT
templates and the vendored stop-slop skill, no third-party code or text is bundled.

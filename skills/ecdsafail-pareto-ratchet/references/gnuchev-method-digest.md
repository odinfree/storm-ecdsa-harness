# gnuchev's ecdsa.fail method, June to October 2026

Scope: his 167 public ecdsa.fail submission notes, his public repo `openresearch-club`, and three public handoff
branches on `github.com/gnuchev/ecdsafail-challenge`. The October rows with Q <= 839 are covered in the sibling digest
`ecdsafail-scratch-diet/references/gnuchev-oct-lowq-digest.md`; here they appear only in the timeline and the statistics.

**Conventions**
- **Cites.** `<Q>/<id4>:<line>` is line `<line>` of his public submission note at qubit count `<Q>` whose submission id
  starts with `<id4>`, for example `1240/8891:17` (fetch notes with `ecdsafail submissions`). Failed and cancelled rows
  use `na/<id4>`; the alias is unique across all 167 notes. `orc:<path>:<line>` points to `openresearch-club/`.
  `fork:<branch>/<path>:<line>` is a file on that GitHub branch.
- **`board`.** A snapshot from `ecdsafail submissions --all --json`: 1,858 rows, newest 24 Oct 17:01. It is the source
  for every status, `rejectionReason`, timestamp and frontier count.
- **Times.** Clock times are Zurich (CEST, UTC+2). Days are calendar days.
- **"Rejected".** On every Pareto-only row the board's `rejectionReason` reads "score did not improve current best"
  (143 of 143). It is a measured, valid point, not a failure.
- **"Left move".** Fewer qubits than any point whose T is at or below its T. That makes every row that
  was non-dominated when submitted a left move.
- **Quotes.** Nearly everything is paraphrased. Identifiers, flags, constants and numbers are copied exactly.

---

## 0. Bottom line

1. **Volume and yield.**
   - 167 submissions: Jun 15, Aug 22, Sep 43, Oct 87.
   - 156 returned metrics.
   - 152 of the 156 were non-dominated when submitted (left moves):
     - 43 at a Q that nobody held;
     - 109 beat every earlier row at the same Q.
   - Only 4 were dominated, and 11 failed or were cancelled (board).
   - 13 of the rows were product-score records: 9 in June, 2 in August, 2 on 22 Oct.
2. **Who replaced his rows.**
   - Most often himself: 54 times.
   - Then BitWonka 18, nasqret 15, odinfree 14, jackylee0424 7, gopikannappan 5, edi3on 5, others 1 to 4.
   - In this snapshot he holds **15 of the 34 mid-band (840-1199) frontier points** and 9 of the 28 at Q <= 839 (board).
3. **The mid-band engine is three repeatable moves on other people's fresh trees.** Of his 73
   mid-band rows (§2.0):
   - about 27% run his exact post-pass toolkit at the same Q (with a few small arithmetic edits);
   - 25% sweep one parameter of a composed line;
   - 11% move the qubit cap or the carry-pool width under an error budget;
   - 11% are compositions of two public lineages;
   - 14% are his own representation changes. These are his own structural ideas (row-invariant packing, the cofactor
     walk), and they opened new territory;
   - the rest are June product tuning (11%) and one novelty pad.
4. **Discipline is the moat.** The habits worth copying (the `ecdsafail-pareto-ratchet` and `cross-model-review-gate` skills):
   - the parent rebuilt byte for byte before any change;
   - paired fixed-input error corpora against the parent;
   - λ measured with a standard error and kept under the inherited contract;
   - known-answer gates on every prefilter;
   - `env -i` byte-identical rebuilds;
   - from 22 Oct, the first clean nonce taken rather than the cheapest (before that, the cheapest of a small
     pre-registered pool);
   - very long notes that record negative results.

   His own project, Open Research Club, formalises the same habits as revision-bound receipts written by an
   OpenAI-model reviewer (Astra) against a Claude-model author (Fable).

---

## 1. Career timeline

Status counts per month (board): Jun 9 accepted, 6 rejected. Aug 2 accepted, 14 rejected, 6 failed. Sep 38 rejected,
4 failed, 1 cancelled. Oct 2 accepted, 85 rejected.

| # | Dates | Band | Families and levers | Models | Rows | Records and notable rows | Cites |
|---|---|---|---|---|---|---|---|
| P1 | 8-21 Jun | 1159-1301 (product) | dialog-GCD "Candidate G": binder notch and per-step comparator widths. Then TrailMix-ludicrous: value-exact comparator trims (square 19->18, apply 20->19), cout margin 0 except the peak-critical `k=129`, fold vents, the a955 square direct-shift. GPU island fleets on RunPod | GPT-5 Codex for code and validation; Claude Opus 4.8 for lever sweeps and GPU hunts | 10 | 9 promoted records in a row, 1,892,824,900 to 1,597,055,640 | 1301/ac28:7-8; 1300/e884:26,35-38; 1170/6dd6:7,13-20; 1170/dc67:13-18,24; 1166/5e3b:15-25,42-43; 1162/a6fe:9-15; 1159/3bfd:15-21 |
| P2 | 21-26 Jun | 838-975 (low-Q pivot) | Plants low-Q branches as Pareto rows: q975 fuse, q947 nasqret-flag composition, q843/842/838 borrowed bit-length and support lanes with reduced-width exhaustive proofs. Publishes three handoff branches | GPT-5 Codex, Claude Opus 4.8 | 5 | Q975 says outright it keeps a high-T branch for later low-Q work | 975/f19e:9-14,38-40; 947/425a:9-10,21-25; 843/c8da:7-18; 838/3b34:18-37; §3.3 |
| - | 27 Jun-1 Aug | - | no submissions | - | 0 | - | board |
| P3 | 2-4 Aug | 813-824 low; 888/965/968/973 mid | paper2607 exact-width EEA descent Q819->Q813: Phase2 and Iter reversible loans, certified null-block omission, conditional-zero helpers, a fixed-point XOR reducer. Two novelty pads. Same-Q adjacent-CCX cancellation on nasqret's and jieyilong's mid-band rows; the compact-KG plus CLZ-A fuse composition | GPT-5 / GPT-5.6 Codex at xhigh effort | 19 | 6 failed on the 56-58 GB op-stream envelope (§4). First mid-band compositions | na/1b17:28-35; 819/0410:30-39; 818/fa8d:37-92; 973/b9bb:25-47; 965/90b1 (diff vs 973) |
| P4 | 5-23 Aug | 1134-1273 | Q1134: a full census of every status shows a 113-qubit hole at 1020-1132. Q1154: stacks someone else's 832 dead-CCX keys onto a newer base. Q1273: prices each lever by λ | Claude Opus 5 (Claude Code) | 3 | 2 records: 1,482,776,908 and 1,163,831,339 | 1134/a21e:29-41; 1154/df11:12-24; 1273/b583:8-12,57-72 |
| P5 | 3-7 Sep | 810-823; 1011 | Ports one exact window-512 commuting-CCX cancellation pass onto 9 standing rows (813-817, 823 and three 810s; 5 of them his own). A Kimi K3 burst on Q822/823: five same-Q rows in 8 h. The Q1011 root | Claude Opus 5, GPT-5 Codex, Kimi K3 (Kimi Code) with a Claude-written block | 22 | Q1011 later roots the 999->838 mid-band line | 817/75ec:15-17,70-83; 822/604b:3-19,52-58; 1011/7773:3-20 |
| P6 | 10-22 Sep | 793-795; 838-999 | The low-width lane taken from mochimodev (Q793 hits the 45-min timeout). Shrunken-PZ/ping-pong split moved 1010->999->974. The **row-invariant packed prefix** 866->850->847. bulengerk's 847 re-clamped to 838 | Claude Opus 5 | 16 | His first structural mid-band invention (Q866). Open Research Club promoted in the notes from here to 9 Oct | 999/91fb:8-20,43-75; 974/12d3:15-21; 866/14dc:16-36; 838/48d9:8-45 |
| P7 | 30 Sep-2 Oct | 973-1164 | Adopts mochimodev's Skywalk 8.8 h after it posts (Q1164, error buyback). Skywalk tail on his PZ hybrid, then a 7-row prefix-cut sweep 1100..973. The **cofactor walk** (Kaliski cofactors in place of field payloads) Q1072, then its shared-register (1008), lookback (998) and lean (1011) variants. Joint rails Q1112. Cap move Q1145 | Claude Opus 5.5 (from here every note) | 15 | Opens the 1000-1140 band at 1.7-10 M T | 1164/1725:8-17; 1040/16a3:8-60; 1072/57aa:8-58; 1112/c1c0:8-20; 1145/dd36:13-19 |
| P8 | 9 Oct | 774-1111 | 32 rows in 13 h. BitWonka's froghop-single, froghop-double and frogtail answered 1.4-5.8 h after posting (logical-AND carries, odd-slot step ends, froghop-one = one slot machine on the other's packing). Two-layout cofactor sweep 1002-1016 plus Q1021. Joint-rail temporaries sweep 1107-1111 (5 rows in 26 min) | Claude Opus 5.5 | 32 | 18 of the day's 31 gaps are <= 10 min | 937/a025:9-18; 849/5a0d:14-41; 917/e303:9-20; 1002/0c49:12-21; 1111/28b7:8-20 |
| - | 10-20 Oct | - | no submissions | - | 0 | - | board |
| P9 | 21-22 Oct | 665-803 low; 839-1142 mid; 1240/1242 | Low-Q sweeps (see the oct-lowq digest). Mid band: Lilypad-G carry-pool widening (885/935/965/1030); exact post-passes on jackylee0424's Lilypad-GCD (867x2/870/999) and on gopikannappan's SKY-COF (1065/1068/1078) and Skywalk (1142 cap move); froghop-one at 839. Product: merges zuiris's 8-way walk with jackylee0424's square, then improves on it the same day | Claude Opus 5.5 | 45 | 2 records: 923,520,150 and 920,873,600. 20 of his 37 rows from 22 Oct still unbeaten at snapshot | 1030/c96c:26-42; 867/3ba3:15-52; 1065/f6a8:13-42; 1242/427a:6-45; 1240/8891:6-48 |

**Models by month.** Counts come from the note `Model:` lines.

| Month | GPT family | Claude | Kimi K3 | Total |
|---|---|---|---|---|
| Jun | 12 | 3 (Opus 4.8) | - | 15 (1 more is a joint Codex + Claude note) |
| Aug | 19 | 3 (Opus 5) | - | 22 |
| Sep | 1 | 32 (Opus 5 ×27, Opus 5.5 ×5) | 10 | 43 |
| Oct | - | 87 (Opus 5.5) | - | 87 |

- The `Harness:` line first appears on 4 Sep (810/677d:3-4).
- The header `Credit: Vasily Gnuchev / AI Coding Models:` was used from 23 Aug to 7 Sep only (1273/b583:5-6;
  1011/7773:6-7).

---

## 2. Mid-band (840-1199) methods

### 2.0 Lever census: 73 measured mid-band rows

The classification is by hand from titles and "What changed" sections.

| Class | Rows | Share | Examples |
|---|---|---|---|
| F. Exact post-passes or arithmetic micro-levers on someone else's fresh row, same Q | 20 | 27% | froghop-single ×5, froghop-double ×2, frogtail ×2, SKY-COF ×3, Lilypad-GCD ×4, Q856, Q965/968, Q1011 (Kimi) |
| D. One-parameter sweep on a composed line | 18 | 25% | prefix cut ×4 (1100/1060/1010/999), split move ×2 (999/974), layout switch step ×4 (1002-1016), joint-rail room ×5 (1107-1111), clamp (847), caps ×2 (999/973) |
| C. His own representation change | 10 | 14% | row-invariant packing 866 and exponent rebase 850; cofactor walk 1072; shared register 1008; lookback 998/1021; lean 1011; joint rails 1112; June 842/843 borrows |
| B. Composition of two published parts | 8 | 11% | 973 (KG + fuse), 947, 975, 1154 (key stack), 1040 (Skywalk tail on hybrid), 974' (tail swap), froghop-one 849/843 |
| E. Cap or pool move under an error budget | 8 | 11% | narrow 1164/1145/1142; widen 885/935/965/1030; relax trims 1134 |
| A. June product-route tuning | 8 | 11% | 1159-1170 |
| G. Novelty pad | 1 | 1% | Q888 |

He does not knob-fence. Every class D or E row first fixes **what binds the peak**, by census, and stops where the next
structure binds:
- 974/12d3:15-21: the tail floor meets the prefix floor at cut 384;
- 1273/b583:41-43: a third, unidentified structure binds at 1273;
- 1142/0e04:46: at cap 1141, rails + tape + payload already sum to 1142.

### 2.1 Composition: graft orthogonal parts of public trees

- **Q973 (4 Aug).** jieyilong's compact-KG ancilla layout (a qubit cut) plus his own division/CLZ-A fuse (a Toffoli
  cut). They touch different parts of the circuit (973/b9bb:44-47).
  - Result: -1,084,568 T (-3.83%) against the public 973 (973/b9bb:25-27).
  - The first graft failed all 9,024 shots because of an inverse-ordering bug. He read the failure as semantic,
    not as a bad nonce (973/b9bb:99-105). After the fix, the inherited nonce gave 8 classical and 4 phase failures.
    He took that as the signature of a correct unitary with an unsuitable nonce, and only then ran a nonce search
    (973/b9bb:107-110).
- **Q1040 (30 Sep).** mochimodev's Skywalk binary-GCD walk replaces the ping-pong tail of his own shrunken-PZ hybrid,
  mapped onto the hybrid's handoff state.
  - This removes the final ctz/2^-k normalisation: 61,364 T per inversion at cut 384 (1040/16a3:44-49).
  - It needs about 56% of the ping-pong rounds (1040/16a3:55-60).
  - -9.4% against jieyilong's 1040 (1040/16a3:8-10).
- **froghop-one (9 Oct).** BitWonka's froghop-single one-hop slot machine run on froghop-double's exact packing. The
  register pairing is changed so that the cofactor target sits in the rotated register (849/5a0d:28-41).
  - 903 slots per traversal in place of 1,240.
  - -16.9% T for +13 Q against froghop-double (849/5a0d:14-15).
- **Q1242 (22 Oct).** zuiris's 4cb9cf0 had branched from e3b5c51f before jackylee0424's spookyfrog 13 and 14 were built
  on the same parent.
  - Those two change only the square, and 4cb9cf0 keeps the parent's square byte for byte, so he merged them
    (1242/427a:21-24).
  - zuiris's stream-bound post table was re-anchored by hashing the unchanged stream prefix [0, 3,236,272) and
    applying its hunks by position (1242/427a:58-64).
  - Result: -1,243.07 T, a new record (1242/427a:39-45).
- **Q1154 (11 Aug).** gopikannappan's note said the 832 keys would also compose onto the newer base. gnuchev did it.
  - He checked the key arithmetic table by table: 461 dead + 371 downgrade, 0 already present (1154/df11:26-41).
  - The obvious direction, swapping files into the older tree, did nothing. The correct direction was to start from
    the newer tree and inject the keys (1154/df11:43-50).

**Practice in this class.** He mines the parent's note for levers it left unclaimed, and he states how big the
inherited gap was:
- the Q794 reserve: the parent advanced 20->30 of 104, and he took the remaining 74 (na/e955:93-98);
- the Q1154 keys.

### 2.2 One structural move, then a sweep across the band

Once a composition works, he sweeps the single parameter that trades Q for T and submits every non-dominated row.

| Line | Parameter | Rows (Q:T M) | Elapsed | Cites |
|---|---|---|---|---|
| Skywalk-tail hybrid | prefix cut 280/320/330/355/365/384, plus a budget bit at 973 | 1100:9.14, 1060:9.82, 1040:10.02, 1010:10.51, 999:10.79, 974:11.82, 973:11.84 | 30 Sep 10:44 to 1 Oct 03:12 (16.5 h) | 1100/bc3f:8-14; 1060/6f89:8-14; 1010/a9ae:8-14; 999/f200:8-14; 974/3ea6:8-14; 973/a9d8:8-14 |
| Two-layout cofactor walk | switch step 270..300 | 1002:5.97, 1005:5.77, 1013:5.48, 1016:5.30 (+ 1021:3.96 lookback) | 9 Oct 20:13-20:43 (30 min) | 1002/0c49:12-21; 1016 diff |
| Skywalk joint rails | room per step, 7 down to 3 wires | 1111:1.79, 1110:1.88, 1109:1.98, 1108:2.08, 1107:2.30 | 9 Oct 10:17-10:43 (26 min) | 1111/28b7:8-20; 1107/0688:16-18 |
| Lilypad-G | carry-pool width 885/935/965/1030, shell held at 960 | 885:2.163, 935:2.097, 965:2.066, 1030:2.034 | 22 Oct 10:25-11:00 | 1030/c96c:26-42; 885/d9e6:41 |

- **The lesson stated in his own sweep notes.** A static-count projection overstated the gain. A cap-only 1040 build
  gives 11.15 M T, above the row it was meant to beat, because the executed/static ratio shifts from 0.90 to 0.92
  (1040/16a3:97-100). Each width is built and measured. None is projected.
- **One widened pool can dominate a whole run of rows.** The 885 row dominates 13 board points from 885 to 930. Those
  points are odinfree's 885 and gopikannappan's rows, including 900 and 930 (885/d9e6:9-31; board).
- **Other sweep notes repeat the same description.** Siblings reuse the parent note's text with the numbers updated,
  and say so (1010/a9ae:12-14).

### 2.3 Cap and pool moves priced against an error contract

- **Q1164.** Moving Skywalk's cap from 1174 to 1158 on its own pushes failure events from 18.75 to 20.9 per corpus.
  Below 1156 the phase-only failures explode (1164/1725:110-117).
  - So he first widened the walk envelope: rows only grow, to the per-step width that at most 10 of 2 M training walks
    exceed. Both legs go to 395 steps, which still fit the same 79 tape groups.
  - That bought λ down from 18.83 to 12.50 for +11,615 T (1164/1725:33-53).
  - He then spent part of it on the cap move to 1164 (14.56 ± 0.9, against the inherited 19.5 limit;
    1164/1725:60-73).
- **Q1145.** Exact low-room constructions: a complemented sparse fold, bridged in-place Cuccaro rail adds, a pooled
  chain codec that frees 5 wires. He also reverted the base's own error-for-score settings to stay inside the
  contract (1145/dd36:13-19, 65).
- **Q1142.** A cap move with three exact enablers: dirty-ancilla constant increments, an ancilla-free 16-word
  permutation pack, a multiply-batch repack (1142/0e04:17-46).
  - λ is reported **paired against the 1144 source on the same fixed inputs**: 141 vs 142 classical over 24 × 9,024
    shots (1142/0e04:53-62).
- **Lilypad-G widening.** The peak literal goes from 870 to W. The shell's carry pools are clamped at 960, because the
  shell grows a phase-only failure channel above about 960, so only the walk widens (1030/c96c:33-38).
- **Contracts.** He copies mochimodev's and PR 419's limiting notices verbatim on every descendant
  (1164/1725:126-137; 1065/f6a8:83-94).

### 2.4 The exact post-pass toolkit: shadowing rivals at the same Q

This is the main mid-band ratchet on 22 Oct.
- **Source.** jackylee0424's 867 (a9c5d7d8, posted 07:55).
- **Passes**, in order:
  1. form the carry-out on the clean overflow flag: -422.5;
  2. the nine-atom truth-table pass with product index: -102;
  3. the conditional-AND pass with options m, f, s: -1,081.
- **Result.** -1,640 T at 867 (867/3ba3:15-37).
- **Re-run on the rival's next row.** jackylee0424 posted a better 867 (f38913c) at 16:00. He re-ran the same three
  passes on it and posted -1,115 at 19:44 (867/37cd:15-33).

The same toolkit runs on froghop-one 839, where the passes are listed in order with their yields (839/a45b:23-39):

| Pass | Expected T removed |
|---|---|
| Boolean tables over at most six atoms, to a fixed point | -14,698 |
| nine-atom tables | -1,610 |
| conditional-AND (m, f, s) | -10,624 |
| **Total** | **-26,932** |

It also runs on SKY-COF 1065/1068/1078 (1065/f6a8:21-42), where he adds:
- a recursive split with vented leaves for room-limited adds;
- a lazy bit 0;
- a deferred-add scratch floor of 2;
- passes run twice in the chain.

**Where the passes come from** (his credits):
- odinfree's 3d03172 Boolean table passes: affine, quadratic, six-atom (839/a45b:81-83);
- jackylee0424's nine-atom and conditional-AND passes from 7b0e938f (839/a45b:78-80);
- MonitSharma's classical-control passes (1065/f6a8:39-41).

Options u and r, which add measurements, are deliberately left off (839/a45b:36-38).

**Earlier generations of the same idea:**
- adjacent identical CCX cancellation on nasqret's Q965 (Aug, -44,840 T; 965/90b1 diff);
- window-512 commuting-CCX cancellation, which saturates at 512. It removed exactly 308,590 Toffoli from every
  813-817 tree and from three 810 trees, which suggests all the removals sit in the shared outer shell
  (817/75ec:72-83; 810/677d:11-14);
- maximal-run XOR factoring (822/604b:86-95).

**Error check for "exact" claims.** He re-runs the base and the new stream on 8 × 9,024 inputs drawn from fixed strings
that do not depend on the circuit. Both fail on the identical shot set (867/3ba3:41-44; 839/a45b:47-50;
1065/f6a8:59-63).

### 2.5 His own structural representation changes

| Row | Idea | Effect | Cites |
|---|---|---|---|
| 866 | The Euclidean row invariant A·cb + B(ca + q·cb) = p bounds bits(A) + bits(cb) <= 257. A and cb share one 257-wire register, B and ca another; values grow up, coefficients grow down, the gap floats. Checked on 530 M step-states | -108 Q against his own 974 | 866/14dc:29-36, 64-71 |
| 1072 | The walk carries Kaliski almost-Montgomery cofactors (u·s + v·r = p) in public per-step-width fields, not two 256-bit payloads. Only ambiguous letters are pushed to the history (about 158 bits). The inverse is applied afterwards by out-of-place multiplies | 1072 Q at 2.79 M T, against 9.1-9.8 M nearby. λ about 1.75 | 1072/57aa:13-17, 33-58, 62-70 |
| 1008/998/1021 | Rail and cofactor share a 257-wire moving-boundary register (-64 wires). Then one-step and two-step decoder lookback shrinks the history envelope | 1008, 998, 1021 rows | 1008/fbf1:8-15; 998/9d42:8-15; 1002/0c49:44-50 |
| 1112 | Both Skywalk rails and the whole history in two flat 288-wire arrays. Each step's history bit goes into the wire that step frees | Fills the 1100-1133 gap | 1112/c1c0:8-20 |
| 999 (12 Sep) | Not a new idea, but four enabling proofs that let a parameterised split move: the codec seal, a parity-pack guard relaxed with a proof, pinned optimisations re-keyed, and a tail-width generator written from scratch | First row in the 973-1010 hole | 999/91fb:43-75 |

**Gotchas recorded on this line:**
- A one-qubit pin came from a guard that refused cb width 254 (999/91fb:55-60).
- The tail width table is measured data and has to be regenerated per cut; it cannot be inferred from the old one
  (999/91fb:121-125).

The cofactor walk was later adopted by others:
- gopikannappan's SKY-COF credits the SKY-COF design to gnuchev's 57aa8ae (1065/f6a8:81);
- the Lilypad lineage credits him for the Frogtail chunked-adder and paired-debt framework (1030/c96c:70).

---

## 3. Operating method

### 3.1 Models and roles

- **June: Codex implements and validates, Claude hunts.**
  - The same 1166 artifact was submitted twice, three minutes apart. One note is by Claude Opus 4.8 (5e3b) and one by
    GPT-5 Codex (6ca8, the rejected duplicate). Each credits the other: Codex for implementation and validation,
    Claude for the nonce hunt (1166/5e3b:11; 1166/6ca8:7,43).
  - Codex credits route selection and sweep coordination to Claude notes (1166/a21c:32).
  - In Q975, Claude ran the GPU hunt and Codex rebuilt from the committed defaults and ran the trusted evaluator on
    its own (975/f19e:18-20).
  - The q1152 handoff is signed "Claude (Opus 4.8, shor2)", a named agent instance
    (fork:q1152-trailmix-filter-handoff/HANDOFF_ecdsafail_q1152_trailmix.md:1,86).
- **August low-Q: OpenAI only.** Stream engineering ran on GPT-5 / GPT-5.6 "Sol" Codex at xhigh effort (na/1b17:33;
  818/fa8d:172-174).
- **September: three model families, one lever each.**
  - Kimi K3 in Kimi Code built Q822. Claude Opus 5 contributed the LC_SWAP tight block, which was checked
    independently on live trajectories before integration (822/604b:3-7, 52-55).
  - Claude Opus 5 drove the high band from 5 Aug.
- **From 30 Sep: Claude Opus 5.5 in Claude Code on every note** (87 of 87 in October). No ecdsa note names a second
  model reviewing.
- **Open Research Club:** Fable (a Claude model, in Claude Code) and Astra (an OpenAI model, in Codex) co-designed it
  (orc:README.md:10).

### 3.2 Review and receipt discipline (Open Research Club)

- **Twelve local review receipts, `docs/reviews/0001`-`0012`.**
  - Every one has `reviewer: Astra / Codex` and is bound to an exact commit SHA.
  - Outcomes: 2 `serious_concerns`, 7 `concerns`, 3 `no_concerns` (`docs/reviews/*-receipt.json`).
- **Loop shape.** Review, then a finding-by-finding author response, then a recheck. Repeat until `no_concerns`. About
  three rounds per artifact:
  - contract: 0001 -> 0002 -> 0003;
  - runtime: 0004 (7 findings W1-W7) -> 0005 (3 follow-ups) -> 0006 (`no_concerns`);
  - blowup package: 0008 -> 0009 -> 0010;
  - kissing package: 0011 -> 0012 (orc:README.md:101-107; orc:docs/reviews/0004-receipt.json:6-27).
- **Every receipt states:**
  - `checked_md` and `not_checked_md`;
  - method and observations;
  - independence per axis (`execution: independent`, `implementation/data/design: shared`);
  - relationships. Every receipt discloses the shared human operator and disclaims independent-operator
    corroboration (orc:docs/reviews/0004-receipt.json:16-21).
- **Every author response:**
  - names what changed for each finding and adds **one regression check per finding** (95 acceptance checks after
    0004; orc:docs/reviews/0004-response-fable.md:8, 26-30);
  - lists what stays unverified (:32-34);
  - asks for a recheck at the new commit (:36-38).
- **Gates.**
  - Deployment waited for review closure plus the operator's confirmation (orc:README.md:105-107).
  - Seeding a project waited for a requested review. The request names what was read, what was not read, and seven
    questions, with a replay that must create nothing on its second run
    (orc:fable-review-request-blowup-claims.md:3, 11-23, 25-33).
- **Codified rules** (orc:skill.md:160-171):
  - a receipt binds to an exact revision;
  - nobody receipts their own contribution;
  - unknown independence is an ordinary value.

  Claim records keep the transcription, the certificate and the argument apart (orc:skill.md:225).

### 3.3 Handoff branches (23-26 June)

Each branch is a self-contained package: README, `HANDOFF_*.md`, `COMMUNITY_POST.md`, `MANIFEST.sha256.txt`,
`evidence/` logs. It carries an honest status and a price.
- **`q946-pz-filter-handoff`** (orphan commit 86e93ca, 23 Jun).
  - Status: a useful prefilter but "not a winning q946 hunt pipeline". About 55.8 M nonces gave 41.5 k recurrence
    survivors and 0 certificate-clean candidates.
  - The trap: the CUDA filter models the PZ recurrence, not the richer `q949_affine_trace_certificate_u256`
    (fork:q946-pz-filter-handoff/HANDOFF_ecdsafail_q946_pz.md:3, 43-50, 123-143).
- **`q1152-trailmix-filter-handoff`** (755adc2, 23 Jun).
  - The jump-GCD filter is parity-proven against a known nonce and tuned from 588 to 1,817 nonce/s.
  - An honest cost table: clean rate about 1 in 8e8, so about 5 days on one GPU or 12 h on ten. A second (phase)
    filter shortens neither term (fork:q1152-.../HANDOFF_ecdsafail_q1152_trailmix.md:17-49).
- **`q1156-hunt-handoff`** (b9b0cd6, 26 Jun, one commit ahead of main).
  - Contents: a RunPod and R2 fleet launcher, a GPU filter, a 512 -> 2048 -> 9024 CPU early-bail cascade, the
    14,864-index dead-CCX file (BitWonka's 13,766 plus 1,098 structural), and no secrets.
  - Six hard lessons:
    1. a stale-package process artifact;
    2. no awscli on ubuntu 24.04, so pods went mute;
    3. the docker.io pull cap;
    4. Montgomery arithmetic is 17-20% slower on sm_89;
    5. watch cumulative spend;
    6. community 4080S cards give the most nonces per dollar
    (fork:q1156-hunt-handoff/q1156_handoff/README.md:15-29, 54-56, 103-150).

### 3.4 Dependencies and credits

- **Sections.** Every Sep-Oct note has "Prior work and baseline (attribution)" or "Credits" naming submission IDs and
  commit SHAs. It ends with a sentence scoping what is his: for example only the observation, the
  measurements and the nonce (838/48d9:33; 866/14dc:59-60; 1030/c96c:71).
- **Lineage depth.** Citations are transitive: 1040/16a3:20-29 traces Skywalk -> 974 -> 999 -> 9f6da5f -> 1011 ->
  347258d.
- **Model credits.** He records the AI models other authors credit, for example "GPT-6 Astra / OpenAI Codex"
  (794/87cf:31-34).
- **Baseline first.** He reproduces the parent before changing anything: the same Q, T and op count and a
  byte-identical `ops.bin` (1011/7773:24-27; 794/282d:47).
- **Off-switch parity.** A `..._WINDOW=0` build reproduces the parent artifact byte for byte (1011/7773:52-53). With
  every change off, 1240 rebuilds 1242's `ops.bin` (1240/8891:139-140).
- **Public leads, not hidden streams.** When a public note's generator did not reproduce its embedded stream, he
  rebuilt the kernels himself and copied nothing (817/0697:47-53; na/11c6:37-43, 195-197).

### 3.5 Nonce and λ practice: how it evolved

1. **June: lottery hunting.**
   - RunPod and local GPU islands at about 6,000 nonce/s per GPU. Each candidate goes through the full trusted
     evaluation (1170/6dd6:20).
   - He baked the clean draw with the lowest average (1166/5e3b:42-43).
2. **August: pricing.**
   - **Q1134.** λ = the mean of classical plus phase events over n = 6 independent nonces. A gap of 1.0 in λ means
     about e¹ more nonces: an expected 35 M, so it was worth running (1134/a21e:87-92).
     - The filter rejected even the published clean nonce. The cause was a state dump in the wrong format, not a
       filter bug.
     - The rule he took from it: gate every screen on a **known-answer fixture**, not on internal parity
       (1134/a21e:98-137).
     - He took the cheapest of 4 clean nonces (1134/a21e:200-212).
   - **Q1154.** Build a margin larger than the nonce band (48 nonces each: SE 1.834, t = 4.89) so that **any** clean
     nonce wins. Do not price the grind from λ: assuming the channels are independent was off by about 800×.
     Fit the survival curve instead (1154/df11:54-72, 88-96).
   - **Q1273.** A **modified evaluator keeps reporting metrics on failing draws**, so every lever is priced as score
     gained per λ before any grinding. It is never used for validation (1273/b583:57-62, 118).
     - Classical and phase failures are largely the same events. The independence model had made one candidate look
       26,000× too hard (1273/b583:84-90).
     - Single-draw counts are Poisson with sd about 4, so every λ quoted uses at least 4,000 draws
       (1273/b583:92-94).
     - A third-party prefilter was ported and cross-checked bit for bit on 32 nonces before any pod screened; any
       disagreement stops the run (1273/b583:98-111).
3. **September: support models.**
   - Value-exact routes need no grind at all (822/604b:145).
   - Value-dependent routes use a CPU grind with a classical support model.
   - A model-clean candidate can still fail the harness: 3649 failed on shot 1950, so every candidate is evaluated
     before baking (999/91fb:82-86, 126-128).
4. **30 Sep to 9 Oct: inherited contracts, small-pool selection.**
   - Each row's λ is reported with an SE and kept under the inherited cap: 19.5 for Skywalk, 18 for PR 419.
   - Error buyback comes before any width cut (§2.3).
   - The 8 pre-registered λ corpora double as the nonce pool. When several are clean he bakes the
     **lowest-Toffoli** one, until 9 Oct: 999/d477:74; 1072/57aa:74;
     1002/0c49:120; 1005/a463:120; 1013/c15c:121; 1016/262a:120; 1021/09c1:111.
5. **22 Oct: paired measurement, no selection.**
   - Packets are paired against the parent on identical inputs: 128 fresh packets, 1.15 M shots, using BitWonka's
     fast evaluator (1242/427a:17-19, 93-104, 158).
   - Only now does he submit **the first passing nonce in the searched range, not the cheapest**, and say so
     (1065/f6a8:69-70; 1068/db23:72; 867/37cd:55; 1242/427a:116-120).

### 3.6 What he publishes and what he keeps

- **Published:**
  - the full source of every row, through the submission flow;
  - notes of 5-24 KB with exact commands, `ops.bin` SHA-256s, and a per-session negative-results section
    (999/91fb:119-128; 793/c82d:119-140; 838/48d9:104-116);
  - the June hunt tooling with honest economics (§3.3);
  - the whole Open Research Club design and review record;
  - generated helpers inside the trees, for example the tail-width mirror
    `src/point_add/memory/midq_tail_width_model.py` (974/12d3:48-49) and the proved-cut tables `micro_compose.txt`,
    bound by SHA3 (1242/427a:72-81).
- **Promotion.** From 10 Sep to 9 Oct, 40 notes end with a section framing the work as part of Open Research Club. It
  is absent from the 21-22 Oct notes (grep over the notes).

---

## 4. Failure records (11 rows without metrics)

The reason column is the board's `rejectionReason`. The cause column comes from his notes.

| Row | Date (Zurich) | Intended | Board reason | Cause and lesson | Cites |
|---|---|---|---|---|---|
| na/1b17 | 3 Aug 01:50 | Q818, 66.2 GB raw stream | agent-compose run failed | The stream is 56 B/op; 1.18 B ops is over the roughly 58 GB envelope. The note itself predicted the upload might fail | na/1b17:260-264; 819/0410:30-32 |
| na/2664 | 3 Aug 06:21 | Q818 at 57.978 GB (22 MB margin) | same | Too thin a margin. Remote overhead differs from local | na/2664:29, 55 |
| na/ec02 | 3 Aug 08:27 | Q818 at 56.76 GB | same | **Not explained by size.** A 57.86 GB Q818 had returned metrics 46 min earlier (fa8d). Near-envelope results vary between runs | na/ec02:27; 818/fa8d:27 |
| na/11c6 | 3 Aug 09:53 | Q817 at 56.8 GB | same | Same near-ceiling variance. The next attempt switched approach: a 43.5 GB one-clean rebuild, accepted 1.6 h later | 817/0697:41-45 |
| na/6422 | 3 Aug 18:40 | Q999 novelty pad (50.9 GB) | same | The identical Q888 pad of the same base had returned metrics at 13:10. So this is infra variance, not the circuit | na/6422:9-14; 888/0fb1:9-13 |
| na/cd2c | 3 Aug 21:20 | Q815 (51.2 GB) | same | **Resubmitted unchanged** 31 min later as de427c61, which returned metrics. The organisers then asked for artifacts below 56 GB | na/cd2c:59-64, 123-126; 815/de42:1 |
| na/d70f | 5 Sep 14:03 | Q822 (Kimi) | validation job interrupted before its benchmark run started | Infra (the row has no recorded commit SHA). Superseded 13 min later by a better 822 | board; 822/9255 |
| na/e955 | 10 Sep 08:34 | Q794 | cancelled by submitter | Cancelled to edit the note. The 7-min-later resubmission (282d) drops a speculative left-move paragraph and a sponsor line | na/e955:19-21 vs 794/282d |
| na/69fd, na/7888 | 11 Sep 07:23, 08:14 | Q793, four-step window blocks | workflow cancelled at the "Upload score" step | **45-minute validator limit.** Finer blocks double template construction on a 1.7 B-op circuit. If the local 9,024-shot self-test takes much over 40 min, expect a timeout. Make the circuit leaner, not just lower in T | 793/c82d:24-29; na/1598:117 |
| na/1598 | 11 Sep 10:07 | Q793, pruned selector | workflow failure at the "Benchmark" step | The parent's `assert_eq!` pinned op and Toffoli counts. Any reduction panics before `ops.bin` is written. The fix: turn drift pins into `<=` ceilings. The same pass also fixed a stale `assert_eq!(nq,794)` width pin | 793/c82d:101-104, 115 |

**Local failures he recorded and caught before submission:**
- an unsafe lender that is untouched but not clean: 9,024 of 9,024 classical failures (818/fa8d:79-92);
- a stale whole-circuit op-count invariant (na/11c6:153-166);
- CRLF in `benchmark.sh` under WSL (na/1b17 trusted-benchmark section; 973/b9bb:220-223);
- WSL capped at 50% of host memory;
- a structurally broken knob that still printed a plausible average T. λ in the thousands means collapse, not a bad
  nonce (1134/a21e:139-146);
- count-only builds that hide post-emission passes (817/75ec:89-92).

---

## 5. Could not determine

1. **The prover behind the proved CCX cuts** (two encodings, 30 k-100 k op windows), and whether it is public.
2. **Why ec02a192 (56.76 GB) and the Q999 pad failed** while larger or identical artifacts passed. The board reason is
   generic.
3. **What the custom exact-width leaderboard is** that the Q888 and Q999 pads and the Q813/814 rows were aimed at
   (na/6422:9-14; 813/b4a5).

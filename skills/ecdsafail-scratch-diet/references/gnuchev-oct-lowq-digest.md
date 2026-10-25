# gnuchev, October 2026, Q <= 839: how the left moves were made

Source set: gnuchev's 41 public ecdsa.fail submission notes with Q <= 839 (9, 21 and 22 Oct 2026). All 41 were
read; near-identical sibling notes in a series were diffed against the series head, line by line. Board context
comes from an ecdsa.fail API snapshot whose newest row is 24 Oct 07:17Z. "BW playbook" is the
`ecdsafail-lowq-playbook` skill in this repository.
Note text was treated as data throughout.

**Conventions.**
- Times are Zurich (CEST = UTC+2). The note headers are in UTC.
- "Rejected" is the API status on all 41 rows. It means "score did not improve current best" (the product score),
  not an invalid row: every one is a validated Pareto point (the API's `rejectionReason`).
- **L** = our left-move measure: how many qubits the row sits to the left of the leftmost *other author's* earlier
  point whose T is <= its T (computed from the API snapshot).
- Cites are `alias:line`. The alias is `<Q>-<first 4 hex of the submission id>`; the legend is in the appendix.
- Quotes are almost entirely paraphrase. Identifiers, env flags and formulas are given exactly.

## 0. Bottom line

1. **Twenty-one of the 23 frontier points at Q <= 839 in the snapshot are gnuchev's**, all posted on 22 Oct. The
   exceptions are bulengerk's 660 and edi3on's 818.
2. **He removed qubits only five times** in this set:
   - froghop-double scratch pool 7 -> 2 (-5 Q);
   - frogdrop 775 -> 774 (-1 Q; two binders, each cut its own way);
   - froghop-one quotient stack moved into the register gaps, twice (843 -> 819 and 839 -> 818; -24 and -21 Q);
   - froghop-double pi stored as pi >> 1 (-1 Q, the floor moves 794 -> 793).

   Every one is an exact rewrite with an unchanged failure model. **None trades lambda.**
3. **Most of his L comes from T, not from Q.** The largest L values are
   - 722 (L 48) and 724 (L 46): width-dial rows on BitWonka's 718 tree;
   - 799/800-803 (L 36-40): a pool dial on froghop-double;
   - 819 (L 121) and 818 (L 21): the gap stack;
   - 770 (L 27) and 718/698 (L 20-21): T cuts at a fixed width.

   Pattern: take the leftmost tree, then walk its width dial right until each row undercuts a far-right family.
4. **His signature move is the transplant sweep.** He takes 2-3 exact, tree-agnostic cuts and lands them on every
   rival's frontier row in a band within about 2 h: 665 at 06:16; 718, 722, 675, 691, 698, 719, 720, 724 between
   07:13 and 09:11 on 22 Oct. Each row is a same-Q down move of 0.3-0.9 %. Together they win the band.
5. **Cadence.**
   - 6 rows in 14 min (9 Oct), 7 rows in 14 min (21 Oct), 11 rows in 27 min (22 Oct).
   - Billion-op rows on two trees interleaved at one row per ~17 min.
   - In a series the contested widths go first.
6. **Validation discipline is uniform:**
   - nonces declared before they are run, on 8 corpora;
   - failing sets compared with the unchanged base on shared inputs;
   - the base rebuilt and reproduced to the digit;
   - two independent Linux builds with the same SHA;
   - honest lambda in every note.

   What the BW playbook lacks is **breadth**: a dirty-ancilla catalogue, known-zero lane carries, parity halving of
   counters, gap relocation, and the multi-tree transplant sweep.

## 1. Timeline

Family keys:
- **FHD** = froghop-double (BitWonka 37e1f27 lean -> nasqret 777d182 -> gnuchev K1/K2);
- **FH1** = froghop-one (gnuchev 843/819 on BitWonka froghop-single 8f53dab + froghop-double 4adf9ec; later the
  jackylee 839 line e4263fa);
- **FD** = frogdrop traversal (BitWonka bce82f3);
- **FD770** = bulengerk's R08-R12 frogdrop;
- **PW** = BitWonka's 718 payload walk b98ba94;
- **JL** = jackylee's ring-258 / Scheme G line;
- **BK665** = bulengerk 665 on the jackylee 669/671 lineage.

Status: **F** = still on the frontier in the snapshot; otherwise the author and day of the row that dominated it.

### 9 Oct

| # | time | alias | Q | T | status | family / base (author id, posted) | lever | delta | L |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 09:27 | 799-666b | 799 | 17,340,825 | gopik 18 Oct | FHD / BitWonka 37e1f27 (05:20) | ancilla-free offset adds, no const-1 control | -25,752 | 37 |
| 2 | 09:30 | 795-93e1 | 795 | 37,846,519 | own 21 Oct | FHD same tree, pool 3 | borrowed-qubit forms | +20.48M vs 799 base | 4 |
| 3 | 09:33 | 794-bb7c | 794 | 49,151,603 | own 21 Oct | pool 2 (floor) | same | +31.79M | 5 |
| 4 | 09:36 | 796-a516 | 796 | 29,886,875 | own 21 Oct | pool 4 | same | +12.52M | 3 |
| 5 | 09:39 | 797-1291 | 797 | 23,396,795 | nasqret 19 Oct | pool 5 | same | +6.03M | 2 |
| 6 | 09:42 | 798-dff8 | 798 | 18,707,563 | edi3on 21 Oct | pool 6 | same | +1.34M | 1 |
| 7 | 09:53 | 774-f3e0 | 774 | 196,328,204 | own 12:54 | FD / BitWonka bce82f3 (06:43) | flag-free parked-product add + 68-lane pool | -1 Q, +10,529,460 | 1 |
| 8 | 11:39 | 775-9f81 | 775 | 185,347,856 | own 12:54 | FD / bce82f3 | 1 AND-carry qubit in the map adds | -450,888 | 24 |
| 9 | 12:54 | 774-334b | 774 | 179,740,383 | bulengerk 770, 10 Oct | FD / own 774-f3e0 | AND carries on idle + envelope-zero lanes; dy-consuming product | -16,587,821 vs #7 | 25 |
| 10 | 13:22 | 819-3e7f | 819 | 14,489,348 | own 21 Oct | FH1 / own 843 3f1c7ce5 (12:16) | quotient stack into the register gaps | -24 Q, +1,478,748 | 121 |
| 11 | 20:56 | 775-d2ce | 775 | 169,387,896 | bulengerk 770, 10 Oct | FD / bce82f3 | AND carries in the map and the quotient estimate | -16,410,848 (-8.8 %) | 24 |

### 21 Oct

| # | time | alias | Q | T | status | family / base | lever | delta vs best prior at width | L |
|---|---|---|---|---|---|---|---|---|---|
| 12 | 11:16 | 798-5a00 | 798 | 14,907,699 | edi3on 17:55 | FHD K1 / nasqret 777d182 (19 Oct 04:57) | pi stored as h = pi >> 1, pool 7 | -3,023,772 (edi3on edf6211) | 41 |
| 13 | 11:19 | 796-e883 | 796 | 20,927,071 | own 22 Oct | K1 pool 5 | same | -8,959,804 | 2 |
| 14 | 11:21 | 793-46f4 | 793 | 43,860,835 | own 22 Oct | K1 pool 2 (new floor) | same | -627.4M (odinfree e631a57) | 4 |
| 15 | 11:24 | 797-bcdc | 797 | 16,397,595 | edi3on 20:26 | K1 pool 6 | same | -6,412,672 | 2 |
| 16 | 11:26 | 795-896d | 795 | 26,707,639 | own 22 Oct | K1 pool 4 | same | -11,138,880 | 2 |
| 17 | 11:28 | 794-58db | 794 | 33,891,403 | own 22 Oct | K1 pool 3 | same | -15,260,200 | 3 |
| 18 | 11:30 | 799-7932 | 799 | 13,968,947 | edi3on 15:09 | K1 pool 8 | same | -2,209,902 (nasqret) | 40 |
| 19 | 12:07 | 818-7074 | 818 | 9,786,122 | edi3on 23 Oct (-903) | FH1 / jackylee e4263fa (19 Oct 19:58) | gap stack on the 839 line, scratch 15 -> 18 | -21 Q, +1,189,369 | 21 |

### 22 Oct

| # | time | alias | Q | T | status | family / base | lever | delta | L |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 03:26 | 770-986e | 770 | 114,717,662 | F | FD770 / bulengerk 978d89f (11 Oct 05:06) | Euclid size bound on the reciprocal start | -665,148 (-0.58 %) | 27 |
| 21-31 | 03:47-04:14 | 797-f309 ... 793-f280 | 793-803 | 43,392,691 ... 13,529,763 | F (all 11) | FHD K2 / own K1 rows; pools 9-12 for 800-803 | per-slot P1 prefix choice, one-CX scan updates, held [pi == 0], merged S5 flip | -227k..-468k per row; beats every edi3on row | 1-40 |
| 32 | 06:16 | 665-f341 | 665 | 547,776,628 | bulengerk 660 08:30 | BK665 / bulengerk d181b19 (21 Oct 20:43) | un-probe erasure boxes 503/504 deferred + exact cancel index | -3,206,447 (-0.58 %) | 6 |
| 33 | 07:13 | 718-db69 | 718 | 282,166,624 | F | PW / BitWonka b98ba94 (12 Oct 07:30) | bulengerk R12 trio ported (peephole, fused shift, un-probe erasures) | -2,598,518 | 21 |
| 34 | 07:29 | 722-2edf | 722 | 215,546,810 | F | PW CAP 722 (QSUB 6) | width dial | dominates BitWonka 739 | 48 |
| 35 | 07:43 | 675-f95b | 675 | 389,735,655 | F | JL / jackylee 8d916b4 (20 Oct 00:15) | boxes 503/504 + cancel index + nonce CX(5,30) | -1,964,462 (-0.50 %) | 16 |
| 36 | 08:03 | 691-813b | 691 | 294,578,471 | F | JL / jackylee 13c1e05 (16 Oct) | same | -1,922,247 (-0.65 %) | 7 |
| 37 | 08:22 | 698-b902 | 698 | 290,193,999 | F | JL / jackylee f20716b (13 Oct) | same | -1,418,614 (-0.49 %) | 20 |
| 38 | 08:41 | 719-3666 | 719 | 251,305,962 | F | PW CAP 719 (QSUB 3) | width dial | new lane | 20 |
| 39 | 08:57 | 720-2124 | 720 | 233,791,304 | F | PW CAP 720 (QSUB 4) | width dial | new lane | 19 |
| 40 | 09:11 | 724-9777 | 724 | 205,598,493 | F | PW CAP 724 (QSUB 8) | width dial | dominates BitWonka 739 | 46 |
| 41 | 14:44 | 839-a45b | 839 | 8,569,808 | F | FH1 / jackylee e4263fa | three generic exact post-passes | -26,945 (-0.31 %) | 17 |

Detail for rows 21-31, in submission order:

| Q | T | delta |
|---|---|---|
| 797 | 16,018,751 | -286,116 vs edi3on c079e68 |
| 798 | 14,498,839 | -263,732 vs edi3on 4da3d9c |
| 799 | 13,680,091 | -263,928 vs edi3on 79fd807 |
| 801 | 13,556,627 | -345,120 vs edi3on da6a5ea |
| 803 | 13,529,763 | -332,008 vs edi3on 4ad6e0b |
| 800 | 13,578,339 | -372,232 vs edi3on a4e58de |
| 802 | 13,534,723 | new width |
| 796 | 20,461,391 | -465,680 vs own |
| 795 | 26,339,227 | -368,412 vs own |
| 794 | 33,423,259 | -468,144 vs own |
| 793 | 43,392,691 | -468,144 vs own |

Source: 793-f280:92-104.

On 22 Oct his Pareto sweep also produced two accepted product records, Q1242 x 743,575 and Q1240 x 742,640.

## 2. His left-move methods, precisely

### 2.1 Structural qubit cuts (new; exact; lambda unchanged)

**Q1. Scratch diet: froghop-double pool 7 -> 2 (799 -> 794), 9 Oct.**
- **Register.** Only the per-slot scratch pool shrinks: 772 data qubits (D, V = 2 x 258, dy 256) + 20 bookkeeping
  + pool (799-666b:33-38).
- **Mechanism.** Every use of a clean pool qubit gets an exact replacement that needs none (794-bb7c:23-28;
  799-666b:44-70):
  - decoder prefix levels beyond the pool become multi-controlled X on *borrowed dy* qubits (any state, restored);
  - the offset-register adds become the Takahashi-Tani-Kunihiro in-operand ripple, with the carry-out XORed into the
    top lane through one borrowed dy qubit;
  - counters use free pool qubits for carries, then borrowed MCX, and bit 0 is the carry control (no constant-1 qubit);
  - flag predicates are XOR sums of AND terms, e.g. po = CO ^ CO.A ^ CO.B ^ CO.A.B, so po, z0 and nz are never stored;
  - u -= po becomes four literal-controlled increments (inclusion-exclusion);
  - the depth decrement under CO.!A is done unconditionally and then repaired: wrapped shots are returned by a 0 <-> 31
    swap that is reachable only for them;
  - the turn-scan decoder levels are XOR-held in depth bits 0..3 and p1, which are |0> on every turning shot;
  - masked-ladder cells drop their temp (3-control X on borrowed qubits).
- **Dial.** Each step keeps the base's cheap form when its free-pool threshold is met (4 / 3 / 2 qubits, depending on
  the step) and the borrowed form otherwise (799-666b:68-70). This turns the pool size into a dial.
- **Proof.** Each replacement is the same function. The gate-level traversal is checked against the integer model at
  every slot, plus forward + inverse identity, the fold, and a 64-shot end-to-end run (799-666b:126-128). lambda:
  every failing shot is one BitWonka's 799 also fails on the same inputs, across all 22 failing corpora of the six
  builds (799-666b:105-107).
- **T price per qubit removed** (799-666b:74-81):

  | step | T |
  |---|---|
  | 799 -> 798 | +1,366,738 |
  | 798 -> 797 | +4,689,232 |
  | 797 -> 796 | +6,490,080 |
  | 796 -> 795 | +7,959,644 |
  | 795 -> 794 | +11,305,084 |

  Cumulative: +31.8M, +183 %.
- **Floor.** The carry-in and the running mask are both live through every ladder pass, so pool 2 is the minimum
  (799-666b:132-133).
- **Limit of the trick.** Conditionally clean decoder levels work only where the gate selects shots whose lane values
  are known (799-666b:134-135).

**Q2. frogdrop 775 -> 774, 9 Oct: two binders, two cuts.**
- **The two binders.** Both moments sat at 775 (774-f3e0:23-26, 40-48):
  - the traversal: 706 + pool 69;
  - the parked products: inverse 256 + counter 6 + dy 256 + product 256 + overflow flag 1.
- **(a) Traversal: delete a constant-|0> lane by idle-time re-hosting** (774-f3e0:84-93). The pool's `zero` lane had
  four uses, all re-hosted:
  - the zero-padded compares use `cmpc`, which is |0> and idle at every one of them;
  - the sign-lane comparator borrows the PScr temp;
  - the 9-bit masked swap borrows `cmpc` as its 8th prefix;
  - the switch-flag comparator borrows `bq`.

  The ops are the base's, relabelled; T is the same op for op (45,175,536 per traversal).
- **(b) Products: the flag-free controlled modular add `ctrl_modadd_nf`** (774-f3e0:53-71).
  - Add mod 2^256 (TTK ripple, 3n - 2 Toffoli). Then repair the overflow with two reflections, R_{y-c} followed by
    R_y, where R_a(z) = a - 1 - z. Together they add c on the carry shots and leave the others alone.
  - Each reflection fires on F = ctl & [z < a]. Because R_a preserves F, the conditional involution can be held in a
    *borrowed* qubit g of unknown value: `(g?R) ; g^=F ; (g?R) ; g^=F`.
  - g and the compare helper d are bits i+1 and i+2 of the multiplier register.
  - Assumption: z < p and y >= c (probability about 2^-224 per operand to fail).
  - Proof: exhaustive over five small moduli (314,296 cases), plus 256-bit random and edge operands
    (774-f3e0:73-77).
  - Price: 15,674 T per add against 1,910, i.e. **+10,529,460 T (+5.7 %)** over three product plays
    (774-f3e0:79-80, 104).
  - lambda 0.375 on 8 corpora; the model rate of 0.63 is unchanged. The flag add's 32-lane erase-compare
    approximation is gone from those two products (774-f3e0:108-111).
- **(c) Winning the T back (774-334b, 3 h later).**
  - Gidney logical-AND carries (2 T per lane instead of 3) on qubits that are known |0> at that moment: 9 idle map
    scratch qubits, and Q's lanes [m, 138) above the column's pair-value envelope `smax` (774-334b:56-71).
  - A shot outside the envelope already fails frogdrop's map, so no new error appears.
  - Result: -3,265,296 T per traversal (-7.2 %) (774-334b:73).
- **(d) Consume-on-use product `div1_product`** (774-334b:77-85).
  - Horner over dy, top bit first. Each dy bit is X-measured right after use, and its phase joins the dy fix that
    already exists.
  - The first freed qubit becomes the addend's lane 255; the second becomes the overflow flag of every later add.
  - So 253 of the 255 adds are cheap flag adds: 709,149 T against 4,204,950.
- **Net.** 774 x 179,740,383 dominates 775 x 185,798,744 (774-334b:13-16).
- **Later on the same day.** At 775 he added the same carries to the streaming estimate's compare-and-subtract
  ladders (`cmp_csub_and`, carries on `bq` and Q's bottom lanes below the bl(Y) envelope): -4,102,712 T per traversal,
  -9.1 % (775-d2ce:65-73). bulengerk then carried the line to 770, crediting gnuchev for the measured carry kernel
  (770-986e:93-95).

**Q3. Register into gaps: the gap-resident quotient stack (froghop-one).**
843 -> 819 on 9 Oct (819-3e7f:20-52); 839 -> 818 on 21 Oct (818-7074:23-62).
- **Register.** The 24-qubit quotient-bit stack, which doubled as the DONE counter.
- **Placement.**
  - During DIV, bit d goes into V's gap at V-frame lane b + d, just above the divisor.
  - After the step-end swap V becomes D, and the next up-ramp pops from D's gap, top first.
  - Push and pop are one-hot scans over per-slot lane windows, gated by the push and pop flags.
  - The 818 version (818-7074:34-41) keys the scans on the offset register plus d - 1, and stores bit 0 implicitly.
- **b converts at the turn.** b keeps the dividend's length until the stack empties, so the pop lanes stay fixed
  (819-3e7f:37-41; 818-7074:42-46).
- **DONE counter into dead registers.** It moves into k and the low depth bits, which no DONE shot reads again
  (819-3e7f:44-45; 818-7074:52-54).
- **Census.** An integer model over 1M simulated divisions shows that no division needs more lanes, and that stack
  lanes never reach a cofactor lane (818-7074:39-41).
- **Windows.** Sized from 1M divisions with per-window margins: 2 or 3, 5 for the turn's V probe, 4 for the offset
  register (819-3e7f:50-52; 818-7074:59-62).
- **Price.** About 1.5 M T per traversal pair goes to the gap-stack scans.

  | build | T | gap-stack scans | shorter product carry pool |
  |---|---|---|---|
  | 819 | +1,478,748 (+11.4 %) | +335.3 per slot | +267,620 |
  | 818 | +1,189,369 (+13.8 %) | +500,035 per traversal pair | +220,000 |

  818 scan split: pop ~204k, push ~138k, turn adds ~94k, depth term ~71k (819-3e7f:58-63; 818-7074:66-79).
- **Scratch.** 818 spends 3 of the 21 freed qubits on scratch, keeping the products' inter-traversal carry pool at
  the 34-lane floor of the signed-digit compares (818-7074:57-58).
- **lambda.** 0.25 for both, against 0.5 at 843 and ~0.6 at 839. On 45,120 shared point pairs the new build fails a
  subset of the base's shots: 2 of 3 at 819; 0 of 2 at 818 (819-3e7f:81-88; 818-7074:97-103).

**Q4. Classical-parity halving of a counter: pi -> h = pi >> 1 (froghop-double floor 794 -> 793), 21 Oct.**
- **Observation.** pi starts at 1 and moves +-1 every slot for every shot, so its low bit equals the slot-index parity
  and is a per-slot classical constant pk. Store only h = pi >> 1, in 4 qubits (793-46f4:25-30, 44-47).
- **Knock-on Toffoli cuts** (793-46f4:47-63):
  - [pi == 0] is classically 0 on even slots, so every AND term with A disappears there and every !A literal is
    dropped;
  - on odd slots A is a 4-literal AND instead of 5;
  - the offset adds' bit-0 carries become CNOT or X;
  - window queries skip lanes of the wrong parity;
  - the home rotation of V becomes a relabelling of wires.
- **Check.** The slot-level test asserts h = pi >> 1 and the low bit against parity (793-46f4:123).
- **Price.** None: T falls at every width. At 799 it is -2,209,902 against nasqret; skipping the RT0 swap on even
  slots alone is -739,640 (793-46f4:71-81).
- **Origin.** jackylee's froghop-one 839 already stored pi >> 1; gnuchev ported it to froghop-double
  (793-46f4:150-151).
- **New floor.** With 19 bookkeeping qubits and pool 2: "with 19 bookkeeping qubits 793 is this machine's floor"
  (793-46f4:127-128).

### 2.2 Knob sweeps of an existing tree (width dials)

**POOL_D (froghop-double).** One row per pool size: 9 Oct pools 2-7; 21 Oct pools 2-8; 22 Oct pools 2-12.

The K2 cost of each qubit removed (from the K2 table, 793-f280:76-88):

| step | T |
|---|---|
| 803 -> 802 | +4,960 |
| 802 -> 801 | +21,904 |
| 801 -> 800 | +21,712 |
| 800 -> 799 | +101,752 |
| 799 -> 798 | +818,748 |
| 798 -> 797 | +1,519,912 |
| 797 -> 796 | +4,442,640 |
| 796 -> 795 | +5,877,836 |
| 795 -> 794 | +7,084,032 |
| 794 -> 793 | +9,969,432 |

The dial is flat above pool ~9 and steep below pool 6. Every row was submitted, because each strictly decreases.

**CAP_TABLE (payload walk, 718-769).**
- One constant picks the row: `pub const CAP` in `mod.rs` selects a row of `CAP_TABLE`. Peak = 716 + QSUB + POOLX
  (718-db69:24-28).
- **QSUB.** The width of the stored quotient subset, 2 -> 24, from 718 to 740. Each extra qubit widens the subset;
  the switch replays shrink with ceil(24 / QSUB) (718-db69:29-33).
- **POOLX (1-29) and XB, from 741 to 769.**
  - POOLX lanes extend the map's carry tail and AND bank, the probe and compare helpers, and the payload digit.
  - XB lets the loan-bank ring adds and the reciprocal compares borrow those lanes.
  - XB alone is worth -1.61M at 769 (718-db69:34-37, 69).
- **Emitted T** (718-db69:55-66):

  | width | QSUB / POOLX | emitted T |
  |---|---|---|
  | 718 | QSUB 2 | 285,336,392 |
  | 719 | QSUB 3 | 254,624,228 |
  | 720 | QSUB 4 | 237,169,924 |
  | 722 | QSUB 6 | 219,036,236 |
  | 724 | QSUB 8 | 209,110,462 |
  | 728 | QSUB 12 | 195,704,348 |
  | 740 | QSUB 24 | 179,761,608 |
  | 769 | QSUB 24 + POOLX 29, XB | 174,223,852 |

- **Executed / emitted:** 0.98889 at 718 down to 0.98321 at 724.
- **His own measured rules** (718-db69:94-99):
  - QSUB = 1 costs +86.0M;
  - at equal width a wider subset beats extra pool lanes at every width from 723 to 739;
  - the big steps sit where ceil(24 / QSUB) drops, at 719, 720, 721, 722, 724, 728 and 740.
- He submitted only 718, 719, 720, 722 and 724, the steps that clear the next bar.

### 2.3 Composition: other authors' exact levers transplanted onto their own or rivals' rows

All of these are same-Q down moves. Each one turns into L when the right-hand neighbour is far away.

- **bulengerk R12 trio -> BitWonka 718** (718-db69:38-43, 53-59). The three cuts add up exactly to -2,598,500
  (-0.90 %):

  | cut | emitted T |
  |---|---|
  | exact X / CX / CCX peephole | -1,588,420 |
  | fused region shift (region shift folded into the frame rotation) | -275,752 |
  | sz / sy un-probe erasures | -734,328 |

  The nonce's X X pair sits behind a barrier so it never cancels.
- **Deferred un-probe erasure boxes + exact cancel index -> bulengerk 665, jackylee 675 / 691 / 698**
  (665-f341:21-36; 675-f95b:20-31).
  - The sz (stage 8) and sy un-probes become erasure boxes, tags 503 and 504.
  - In the forward traversals T1 and T3 their lanes are X-measured and the outcomes are kept; the inverse traversals
    T2 and T4 replay the probe and apply the recorded phases.
  - The cancel index drops the 4096-gate horizon: it keeps per-key and per-qubit last reader and writer, and lets AND
    computes enter the window.
  - Split per tree (675-f95b:48-49; 691-813b:48-49; 698-b902:48-49):

    | row | boxes | index |
    |---|---|---|
    | 675 | -1,913,770 | -50,728 |
    | 691 | -1,875,106 | -47,164 |
    | 698 | -1,376,308 | -42,304 |

  - On 665 the boxes alone are worth 0 (a box played locally costs what the un-probe costs). Deferred together with
    the index they give -3,206,348 (665-f341:53-55).
  - Full deferral, rows included, gives phase garbage in every batch on the ring-257 lineage, so he restricted it to
    the two box kinds (665-f341:73-75).
- **A math bound -> bulengerk 770** (770-986e:21-44).
  - The reciprocal division P already skipped leading iterations from the column envelope sz0 + sy0. He uses
    `start_min = max(sz0 + sy0, 254 - qb) + soff`.
  - Proof from the extended-Euclid identity:
    - r_{j-1}|t_j| > p/2 gives bl(r_{j-1}) + bl(t_j) >= 255;
    - q_j < 2^qb gives bl(r_{j-1}) <= bl(r_j) + qb;
    - so bl(r_j) + bl(t_j) >= 255 - qb, and the code uses 254 - qb (one lane of slack).
  - Gain: -665,148 executed, -8.2M ops. The 54,144 shared inputs give an identical failing set (770-986e:74-79).
- **Generic post-passes -> jackylee 839** (839-a45b:23-40), on the finished gate list before the nonce tail:

  | pass | expected T |
  |---|---|
  | odinfree's <=6-atom Boolean tables, to a fixed point | -14,698 |
  | jackylee's 9-atom tables | -1,610 |
  | jackylee's conditional-AND pass, options m / f / s | -10,624 |

  The conditional-AND pass alone would give -22,661.5; the passes overlap. Options u and r (which add measurements)
  were not used.
- **jackylee's pi >> 1 -> froghop-double** (Q4 above).
- **edi3on's P1 prefix split -> generalised** (793-f280:35-46). Per slot he enumerates every split k + (np - k) and
  windows recut to the lanes where each decoder can match. He emits the option with the fewest Toffoli in the up and
  down passes. Gain over edi3on's rule: -26,368 / -20,296 / -14,088 at 797 / 798 / 799 (793-f280:90).
- **nasqret's prefix-CX update -> one-CX refresh in the S3 gated-scan decoders** (793-f280:48-53). When the top
  refreshed level changes only because literal L flipped while its other input A did not, the new level is
  A & !L = (A & L) ^ A. One CX replaces an uncompute plus a recompute. Gain: -227,848 to -468,144 per row.
- **His own gap stack (Q3) -> jackylee's 839** (818-7074).
- **Pool-gated extras** (793-f280:55-67, 130-132):
  - holding [pi == 0] from S4 to S7 needs pool >= 8 (-86,800 from 800 up). Below pool 8 it costs up to +2.63M,
    because the held qubit pushes later steps into their borrowed forms;
  - the merged S5 rt0 flip (two disjoint conditions -> one 3-control flip) needs 8 free qubits in S5;
  - keeping the AND chain live (4b) needs one more qubit: -12,400 / -17,360 at 802 / 803.

### 2.4 What gnuchev does that the BW playbook lacks

| gnuchev practice | BW playbook | gap |
|---|---|---|
| Dirty-ancilla rewrites: borrowed MCX, conditional involution in a borrowed qubit, XOR-of-AND flags, TTK adders, wrap-and-repair (Q1, Q2b) | "lend a provable lane": clean lanes only, proved per shot | borrowing qubits in an *unknown* state, then restoring them |
| Pool-aware emission: every step has a cheap form and a borrowed form, picked by free count (799-666b:68-70); per-slot cheapest option (793-f280:41-46) | refactor equivalence-first, fixed design | turns any scratch pool into a submit-every-width dial |
| Carries on envelope-zero lanes of a data register (774-334b:66-71; 775-d2ce:65-71) | executed-T harvest by measurement | T bought from lanes known |0> *per column*, not per shot |
| Register-level classical facts: counter parity is the slot parity, so a lane is dropped (Q4) | provable lanes, leading one of a normalised value | a schedule-level (all-shot) constant, not a per-value identity |
| Whole-register relocation into gaps, sized by an integer model over 1M divisions (Q3) | "store derived quantities", counter in free top lanes | the same family; gnuchev does it at 24-lane scale with simulated-division windows |
| Transplant sweep: same exact cuts on 4-5 rival trees in about 2 h (section 1, rows 32-41) | port one rival cut onto your tree | multi-tree, band-wide, contested-first |
| Euclid-identity bound to skip iterations (770-986e:34-44) | precision knobs (lambda-raising) | an exact, zero-lambda iteration cut |
| Shared-input failure-set equality against the unchanged base (799-666b:105-107; 770-986e:74-79; 839-a45b:47-50) | predictor set-equal to the replica | a differential gate, cheaper than calibrating a predictor |

## 3. Workflow and tooling

### 3.1 How he picks bases

- **The best public row at the exact width, any author.**
  - nasqret 777d182 at 799;
  - jackylee e4263fa (839), 8d916b4 (675), 13c1e05 (691), f20716b (698);
  - bulengerk 978d89f (770), d181b19 (665);
  - BitWonka b98ba94 (718), bce82f3 (775), 37e1f27 (799).
- **His own previous series**: K1 -> K2; 843 -> 819.
- **Every note names a public base**, and none of the 41 builds from scratch.

### 3.2 Sweep automation and ordering

- **Cadence.** A series goes out about 3 minutes apart; billion-op rows from two tree families are interleaved.
- **Contested-first ordering.**
  - 21 Oct: 798 first (it beats edi3on's 798), then 796 (beats every 797 point), then the new floor 793.
  - 22 Oct: 797, 798, 799, 801, 803 first (each beats an edi3on row), then 800 and 802, then his own 796-793.
  - 22 Oct, PW tree: 718 and 722 first (722 dominates BitWonka's 739), 719 / 720 / 724 after the JL rows.
- **One source per series.** Rows differ only in the dial constant and the nonce (Q719 vs Q718
  diff). Count builds of other rows use env overrides that the official build never reads
  (`FD_CAP / FD_QSUB / FD_POOLX / FD_XB / FD_PEEP / FD_FUSE / FD_HDRERASE`, 718-db69:88-90).

### 3.3 Nonce and lambda handling, by family

| family | nonce knob | how chosen | lambda reporting |
|---|---|---|---|
| FD 774/775 | qubit of the identity X X pair (`NONCE = 4/5`) | 8 corpora on qubits 200..207, declared before any run; ship the base's nonce if it passes | 3-5 / 8 = 0.375-0.625; model 0.63 (774-334b:110-126) |
| FHD | count of X X pairs at the end (`NONCE = 0..3`) | 8 declared corpora, 7201..7208 or 8801..8808; bake the first clean small count, with misses stated (e.g. NONCE = 1 has one failing shot on that stream, 793-f280:112; 803-5cce:114) | per row 0.125-1.375. Pooled K2 55 / 88 = 0.625; K1 36 / 56 = 0.64; 9 Oct 29 / 48 = 0.60 against a model of 0.65, so the per-row spread is sampling noise |
| FHD 799-803 K2 | as above | lambda measured on a functionally identical variant without (3) / (4b) (802-1246:112) | stated as such |
| FH1 819 / 818 | `FH_NONCE` (env, corpora) vs baked `NONCE` | 8 declared corpora, 8191..8198 and 8181..8188 | 0.25; plus 45,120 shared pairs and the 1M-division integer model (819-3e7f:67-88) |
| FH1 839 | 48-bit identity tail, `TAIL_NONCE = 1` (X X pairs on qubit 0 or 1) | effectively unlimited corpora | ~0.28 over 18 corpora (839-a45b:41-43, 53-56) |
| JL 675-698 | CX(5, t) pair | try the inherited target; on failure try others (CX(5,54) fails 2 shots, CX(5,10) 1, ship CX(5,30)) | classical failure model over all 674-697 control-5 targets: 2.59 / 2.63 / 3.30 (675-f95b:67-70) |
| BK665 | CX(5,2), unchanged | the first build evaluated passed | inherited model 2.52 (665-f341:73-76) |
| PW 718-724 | single X X pair position | position where `frogdrop_sched::predict_n` lists no failing shot; 22 of 23 replica-clean; the miss 722@168 means the next position, 706 | ~5.3-5.4; all 72 observed failures were inside the predicate's set (718-db69:73-82; 719-3666:85-87; 722-2edf:86) |
| FD770 | none: adjacent-pair cancellation removes the X X pair | first eval passed | 2 / 10 corpora = ~0.2 (770-986e:71-79) |

### 3.4 Validation stack (every row)

1. Empty-environment build with its ops SHA stated. The final number comes from the trusted `eval_circuit` (small
   streams), or from BitWonka's fasteval as an exact parallel replica (billion-op streams: 665-f341:59; 718-db69:12,
   105).
2. Reproducibility:
   - an independent Linux build gives the same SHA (819-3e7f:103; two builds, 818-7074:117; 839-a45b:72);
   - the base is rebuilt and reproduces its published SHA and executed average (770-986e:78-79; 839-a45b:72-74).
3. Tests (`cargo test`):

   | rows | tests |
   |---|---|
   | 774 / 775 | 22-24 |
   | 819 | 18 |
   | 818 | 53 |
   | FHD | 10-13 |

   Including a gate-level traversal against the integer model at every slot, with every scratch qubit |0> after each
   slot (819-3e7f:105-109; 818-7074:118-124).
4. New kernels are verified exhaustively at small size: the AND-carry add on every lane split up to 12
   (774-334b:62-63), and `ctrl_modadd_nf` over 314,296 cases.
5. Differential lambda against the base on identical inputs (section 2.4, last row).
6. A per-mechanism ablation table in every note (793-f280:76-88; 718-db69:53-67; 665-f341:53-55; 839-a45b:25-31).

### 3.5 Named tools, flags and resources

- **Source names.**
  - Kernels and passes: `cadd_tail_and`, `cmp_csub_and`, `ctrl_modadd_nf`, `div1_product`, `map_stage`, the new
    `cancel_index.rs`, `column_upto`.
  - Predicate: `frogdrop_sched::predict_n`.
  - Constants: `CAP_TABLE` / `pub const CAP`, `POOL_D`.
- **Env flags.**
  - Count builds and streaming: `LOWQ_EXACT_STREAM_PATH` (byte-identical streaming), `FD_*` (above).
  - Corpora and nonce: `FH_NONCE`, `TAIL_NONCE`.
  - Window regeneration: `FH1_SCHED`, `FH1_KEEP`, `FH1_MPB/MPE/MQ/MU/MLV/MP2/BM` (margin knobs).
  - Window-escape listing: `FH1_GAPTAIL`, `FH1_TAIL`, `FH1_JL_SCHED` (819-3e7f:121-123; 818-7074:137-141).
- **Tests.** `frogdrop_cadd_and`, `frogdrop_cmp_csub_and`, `modp_nf_exhaustive_small`, `modp_nf_256`,
  `one_schedule`, `one_gap_tail`, `one_tail`.
- **Resources.** Builds keep the full op list in memory; his notes report 38-85 GB resident for these trees
  (665-f341:81; 675-f95b:75-76; 770-986e:88-89; 774-334b:144).

### 3.6 Models and agents

- All 41 notes attribute only Claude Opus 5.5 / Claude Code (header line 3-4 of each).
- None mentions Codex, GPT, Fable, Astra, sub-agents or parallel sessions for his own work. The GPT models that do
  appear are rivals': nasqret gpt-astra, bulengerk GPT-6, jackylee Codex GPT-6 Sol, edi3on gpt-6.1-sol
  (e.g. 793-f280:150-151; 665-f341:85, 106).

## 4. His stated walls and open ideas

- **frogdrop 774.**
  - Below 774 the parked products bind: 774 with no scratch, and ndy must survive division 2's recompute
    (774-f3e0:155-157).
  - Each flag-free add pays two full-width constant adds, 9,784 of its 15,674 T (774-f3e0:158-159).
  - The 39 carry-tail qubits cannot double as carries; the division-2 recompute cannot consume ndy; no Q lane is known
    clean in the estimate or corrections (774-334b:152-157).
  - Columns 40-125 fill Q, so carries come only from scratch there (775-d2ce:131-136).
  - Rotations (~12 % of T) and decoders do not benefit from extra qubits (775-9f81:117-119).
- **froghop-double.**
  - Floor 794 with 20 bookkeeping qubits, then 793 with 19 (799-666b:132-133; 793-46f4:127-128; 793-f280:133).
  - Conditionally clean lanes fail on the push/pop scan and the ladder windows (799-666b:134-135).
  - The [pi == 0] hold is a loss below pool 8 (793-f280:130).
  - The twelfth pool qubit pays only through (4b) (793-f280:132).
- **froghop-one.**
  - 815-817 blocked by the 34-lane floor of the signed-digit compares between a division's two traversals
    (818-7074:128-129).
  - Margin 2 windows leak 12 per 1M divisions (819-3e7f:113-115).
  - The stack scans cost ~2 x 30 lanes per slot (819-3e7f:116).
- **Payload walk.** QSUB = 1 costs +86M, and the pool lanes lose to subset width (718-db69:94-99). One predicate miss
  is known, 722@168 (719-3666:85-87).
- **Ring-257 lineage.** Full erasure deferral gives phase garbage (665-f341:73-75). Measured-carry rows keep local
  repair (665-f341:29-31).
- **770.** No nonce knob is available while the builder cancels the X X pair (770-986e:71-72).

## 5. Could not determine

- **Unstated op counts.** For the 9 / 21 / 22 Oct FHD rows and the PW CAP rows, ops are not given. They are given for
  819 (58.37M), 818 (48.30M), 839 (42.67M), 770 (821.1M), 665 (1.533B), 675 (1.155B), 691 (0.983B), 698 (1.070B) and
  774-f3e0 (676.5M).
- **Peephole in 718-724.** The change list adds `cancel_index.rs`, but the text describes a window flushed by any
  other op (718-db69:24-25, 38-40). It is unclear whether those rows use the unbounded index.
- **Statistics.** The statistical power of his 8-corpus lambda figures; I pooled them in 3.3.
- **Board after the snapshot.** Any rows after 24 Oct 07:17Z.

## Appendix: alias legend

Each alias is one public submission note, `2026-10-<DD>_Q<Q>_<id8>`, from the ecdsa.fail API.

| alias | DD | id8 | alias | DD | id8 | alias | DD | id8 |
|---|---|---|---|---|---|---|---|---|
| 774-f3e0 | 09 | f3e09a4e | 793-46f4 | 21 | 46f49d12 | 724-9777 | 22 | 977717a7 |
| 774-334b | 09 | 334b290c | 794-58db | 21 | 58dbcaf2 | 770-986e | 22 | 986e3b28 |
| 775-9f81 | 09 | 9f811391 | 795-896d | 21 | 896d81e0 | 793-f280 | 22 | f280e0f8 |
| 775-d2ce | 09 | d2ce8c6e | 796-e883 | 21 | e883ea35 | 794-74e1 | 22 | 74e18c99 |
| 794-bb7c | 09 | bb7c3804 | 797-bcdc | 21 | bcdce55e | 795-e2ae | 22 | e2ae7ea8 |
| 795-93e1 | 09 | 93e11b9d | 798-5a00 | 21 | 5a0052a6 | 796-928b | 22 | 928b9542 |
| 796-a516 | 09 | a51637f6 | 799-7932 | 21 | 79329cac | 797-f309 | 22 | f3094ac3 |
| 797-1291 | 09 | 129115cd | 818-7074 | 21 | 7074cb69 | 798-1418 | 22 | 1418af0f |
| 798-dff8 | 09 | dff84426 | 665-f341 | 22 | f3412a5e | 799-5539 | 22 | 55397324 |
| 799-666b | 09 | 666b952b | 675-f95b | 22 | f95b5d95 | 800-2c41 | 22 | 2c41c508 |
| 819-3e7f | 09 | 3e7f1342 | 691-813b | 22 | 813ba61d | 801-c219 | 22 | c2190d27 |
| | | | 698-b902 | 22 | b902c42d | 802-1246 | 22 | 12469dfa |
| | | | 718-db69 | 22 | db693b9f | 803-5cce | 22 | 5cce3b52 |
| | | | 719-3666 | 22 | 36666b3b | 839-a45b | 22 | a45bcccd |
| | | | 720-2124 | 22 | 2124a8d4 | | | |
| | | | 722-2edf | 22 | 2edf5ae9 | | | |

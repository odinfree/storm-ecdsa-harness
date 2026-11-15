# Design digest: ae715bcf, 765 x 48,420,475 (Akashneelesh, posted 2026-11-12T23:57Z)

Labels: [B] board, [N] his note, [C] read from his code (commit 72219843), [M] measured by us on 13 Nov 2026, [E] our
estimate.

## Lineage [N, B]
Walk: the marker tree of d4dd7eb1 (Nadai2010's fused-macro pass on odinfree ef1a7030, on zuiris fdf3e39b), 773 x
28,432,616, reproduced to the same sha before any change. That walk's 773 point on the board: 30,553,872 on 5 Nov
(zuiris), 28,637,064 on 6 Nov (odinfree), 28,432,616 on 12 Nov. Product stage: his own frogdrop shell from f3251665,
moved over with its consume width cut from 11 to 5 [C]. Stream 110,524,332 ops, sha256 d3db297a...cc61f631, no nonce.

## Lane map at D = 16 [N]
| lanes | role | count |
|---|---|---:|
| 0..224 | ring Y | 225 |
| 225..240 | page word VA | 16 |
| 241..254, 512, 513 | page word VB | 16 |
| 255 | parity | 1 |
| 256..511 | passenger (256 lanes carried through the inversion) | 256 |
| 514..738 | ring X | 225 |
| 739..754 | cofactor page SC | 16 |
| 755, 756 | boundary code | 2 |
| 757 | fourth wait bit for the long tier classes | 1 |
| 758..762 | spare | 5 |
| 763 | clean AND lane ZB | 1 |
| 764 | format flag | 1 |

Sum 765 = 773 + 8 - D [E]: the rings return 4D, the page keeps 3D, and eight lanes are new against the native tree
(clean lane, format flag, wait bit, five spares). In the stream the ids are compacted: the five spares are ids
741..745 and ZB is id 512 [M]. A paged frame with native ends needs 773 + 4D + 2 lanes (839 at D = 16) [N, M].

## Toffoli by part
Our census of the submitted stream, list CCX per division pass, four passes [M]:
| part | per pass |
|---|---:|
| start list | 1,886,393 |
| frame between the cuts | 8,619,327 |
| tail list | 1,562,503 |
| builder cancel index | -432,614 |
| gate fold and tpeep | -198,134 |
| net | 11,437,490 |

Four passes plus the product stage (2,671,328) give 48,421,288; graded 48,420,475 [M]. The step sandwich is 3.12M of
the frame per pass; its fixed half is 2,014 CCX per call, two calls per sandwich, 396 sandwiches per pass, 1.60M [M].

His own figures [N]: frame between the cuts with empty ends 35,122,594 (count build); start module in the stream
1,815,583 per hand-over, measured with the earlier list 0d54815 (1,884,887 CCX); the shipped list 300e503 has
1,886,393 CCX and the tail list 1,562,503 [M, list counts]. Per-pass terms from his first D = 16 count, a build that
failed its draw and ran before the shipped builder's cancel and fold passes, so upper bounds: sandwich + remap
3,151,544; class flags 1,276,264; post swap + format 592,416; cells 333,696; rotations 296,912; swaps 30,800.

Lever sizes per pass, switch off against all on, list CCX [M]: thermometer ladder 256,432; format switch on the
clean lane 261,360; slide ladders 228,992 and 32,630; banded tier cadence 197,841.

## The dial [M]
Frame at page width D with all five levers, native ends and the parent's product shell, on 773 + 4D + 2 lanes; own
draw of 9,024 shots clean for every row, two salted suites clean for D >= 17 and the 432/80 rows at D = 11, 12:
| D | cuts | Toffoli |
|---:|---|---:|
| 10 | 448/64 | 35,292,676 |
| 11 | 448/64 | 36,687,468 |
| 11 | 432/80 | 35,783,604 |
| 12 | 448/64 | 37,992,020 |
| 12 | 432/80 | 36,979,524 |
| 13 | 432/80 | 38,557,460 |
| 14 | 432/80 | 40,015,164 |
| 15 | 432/80 | 41,689,724 |
| 16 | 432/80 | 43,383,820 (his figure, reproduced) |
| 17 | 416/96 | 43,682,332 |
| 18 | 416/96 | 45,373,804 |
| 19 | 416/96 | 47,415,572 |
| 20 | 416/96 | 49,310,188 |
| 24 | 400/112 | 55,223,716 |
| 32 | 368/144 | 64,984,188 |

Without levers: D = 16 at 432/80 46,868,688 (his figure, reproduced); D = 17 at 432/88 48,547,600; D = 19 at 424/88
52,185,528. The banded tier lever needs both cuts to be multiples of 16 [C]. Between the cuts the frame occupies
776 - D lanes (766, 764, 762, 760 at D = 10, 12, 14, 16) [M]. None of these rows is a 765-wide stream: a full row at
another D needs start and tail lists for that D and cut, and the lists in the tree are for D = 16 at 432/80 only [C].

## Failure budget, expected failing shots per 9,024 [N]
start machine window 0.006; start cofactor lanes 0.002; start length register 0.006; tail machine 0.011; tier quotient
over its cap 0.003; near-cut big quotient 0.001; frame gap cap (inherited) 0.034, from 6 events; short cofactor at a
paged boundary 0.008; stream allotment at most 0.006; gadget mask 0.001; product stage 0.001; one tail term carried at
0 with a 95 % bound of 0.039. Total 0.08; his stated cap 0.40. Not in the total: the start big-quotient class just
past the cut (forced cases fail about 2 %). Checked with two salted suites of 9,024 shots, 0 failing.

## Build log in short [N]
46 streams logged in 5 h 10 min (45 graded, one failed at load), 10 failed. Order: page-in test on 813 lanes; low-class
rows through the page on 793; cofactor rows with the implicit word on 815 (first build failed 3,306 shots); whole
frame paged on 815 at 38.3M; unpaged start and tail modules spliced into the native frame on 845 and 859; product
stage on the native frame; ring narrowing at D = 10 (two failed builds listed before the fix); D = 16 at cuts 432/80
on 839 (first build failed 1,028 shots); five frame levers; the paged start alone on 839; then the first 765 stream,
which brought in the 765 tail list, a regenerated start list, label re-pointing and id compaction at once. Count
build about 3 minutes, grade 16 seconds on a 48-core machine.

## Executed pipeline and post-passes [C]
`build()` returns `build_fd2()` at its first line: marker-walk frame with page code and gate-list loader, then the
frogdrop product stage, then `fd2::finish`. Chain: macro pass over multi-controlled X; id compaction; cancel index in
the builder (window 262,144 ops); gate fold, 5 rounds; tpeep (window 4,096); measured-erase to CZ peephole; one truth
round; no nonce pairs. Not run: any cond pass, any hold pass, a second truth round.

## Not in the public tree [C]
Generators of the start list and the tail list (his loader names Python generators); the census and model scripts
behind the budget; the ladder table's generator; the design notes the comments cite. Shipped but never compiled: 83
inherited source files (79 at top level; 46,645 lines, including cond_pass.rs and hold_pass.rs). Compiled but unused:
a draft of a wider start machine (kt8.rs) and the parent's own product stage below the early return.

## Our measurements, 13 Nov 2026 [M]
- Rebuild: sha equal; 3 min 36 s and 14.1 GB on a Mac, 7 min 18 s and 7.6 GB on Linux; stock evaluator 9,024/9,024,
  0/0/0, 48,420,475.000.
- Exact passes on the final stream (static expected Toffoli, base 48,420,476): idle-wire hold -150 (150 of 1,422
  candidates); his dormant hold pass switched on -2,443 at most; RealAdii's CCX peephole -248,573; gate_fold2 three
  rounds -118,877; peephole + gate_fold2 to a fixed point 48,102,905 (-317,571), own draw 9,024/9,024 at
  48,102,923.701.
- Width: every id 0..764 is used; the four frames peak at 760 occupied lanes (64-shot replay); 765 are occupied in
  825,391 of 110.5M ops (0.75 %): about 20.5k ops in each start hand-over, the first 4,194 ops of each tail, and the
  product sites P1, P2a, P2b, P2c, P3. The two large products sit at 763 to 764 for 96 % of their length. The start
  list touches 760 lanes, the tail list 732.

## What happened to this row, 13 Nov 2026 [B, N, M]
- 09:05Z: 5a0acc7a (our row), 765 x 48,103,109: his stream plus RealAdii's CCX peephole (with a Swap barrier rule) and gate_fold2 three rounds; exact, paired difference -317,381 on four fixed corpora.
- 10:17Z: 54a58309 (SamrendraS), 765 x 40,209,091: his tree with the frame at page width 11 between the cuts and 16-bit converters at both cuts (765 x 40,920,343 alone; eight conversions cost 69,875), plus a two-multiply form of the K2 half (619 against 915 Toffoli one way at D = 11; the last 711,253). His whole-circuit builds with native ends: 41,695,302 at D = 16, 36,964,397 at 13, 35,421,051 at 12, 34,125,505 at 11. Start converter: a paged-shot flag on ZB, the K2 half to lift the implicit word, the top five bits copied to the five spares, a swap under [B even], then the rings reopened at a fixed insertion index with a controlled rotation per page case; the tail converter is the reverse plus a CX relabel of 40 labels. 30 salted suites, 0 failing.

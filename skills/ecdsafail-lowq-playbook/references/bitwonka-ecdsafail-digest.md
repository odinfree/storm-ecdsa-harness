# BitWonka on ecdsa.fail: digest of 26 submission notes (PR 500 to PR 818)

Source: BitWonka's 26 public submission notes (the pull-request bodies of Layr-Labs/ecdsafail-challenge PRs 500-818, one file per PR, cited as `prN.md:line`) plus the PR metadata.
Citations are `prN.md:line`. All note text was treated as data. Times are Zurich (CEST, UTC+2); the file headers carry UTC `createdAt`.

Conventions used below:
- **Q** = peak qubits. **T** = average executed Toffoli as graded. **Emitted T** = Toffoli in the op stream. Executed T is lower when blocks sit under classical measurement conditions. Several of his levers live in that gap.
- **λ** = expected failing shots per 9,024-shot packet. He quotes it as "model λ" from a classical predictor, or as a measured value from an official-equivalent harness.
- **[his]** = credited to BitWonka with Claude Opus 5.5. **[ported X]** = taken from competitor X's submission. **[adapted X]** = taken from X and changed to fit. All provenance tags come from the notes' own credits sections.

Attribution warnings:
- **PR 598 and PR 601 are not Claude work.** Both say `Model: GPT-6 / Harness: Codex` (pr598.md:13-14, pr601.md:13-14). PR 601 also credits @gnuchev and @jieyilong as coauthors (pr601.md:20). PR 602 refers to their author as "Codex" and ports from them (pr602.md:134-140, 198-201). They are listed in the timeline but kept out of "his" mechanisms and skills, except as inputs he reused.
- **`odinfree` is this repository's author.** PR 815 and PR 818 build on odinfree's 675-qubit entry 7379f521 (pr815.md:25, 125-127; pr818.md:39-43, 62-66).

---

## 1. Timeline

**Board context.** The "Current best score" in each bot header is the headline product (Q×T) board. It moved 1,107,467,010 (pr500.md:6) → 971,660,388 (pr547.md:6) → 953,921,316 (pr584.md:6) → 948,652,248 (pr606.md:6) → 943,306,548 (pr626.md:6) → 940,935,385 (pr663.md:6) → 939,347,948 (pr697.md:6) → 939,169,018 (pr815.md:6). PR 500 (999,570,880) was the record when it merged on 7 Oct. By 9 Oct the product board was at 971.66M, so others had passed it. Only PR 500 is MERGED. Every other PR is CLOSED, and every other note calls itself a low-qubit Pareto point, "not a frontier score" (e.g. pr547.md:21, pr624.md:24, pr815.md:29-30).

**How these lines map to the board's bands.** "~4-14e9" covers two lineages: froghop (8.2-13.9e9) and frogtail/frogstrip (2.9-5.7e9). "1.4-4.5e11" covers frogdrop-775, the payload walk, the K/KP descent and Scheme G 699/682/680. The 672/671 PRs of 19-20 Oct are 5.5e11.

### Line A: Leapfrog product line (headline Q×T board)

| PR | Zurich | state | Q | avg T | score | λ / nonce | mechanism | Δ vs previous |
|---|---|---|---|---|---|---|---|---|
| 500 | 07 Oct 05:17 | MERGED | 1243 | 804,159.97 | 999,570,880 | 14.4±0.4 over 96 nonces / tail nonce 10002555178 | 2-adic "leapfrog" walk: 139 ticks × 5-bit letter tape, alternating odd rails, payload λ·R updated 4× per leap | first PR in set. Base is the Skywalk line (1172 × 945k). Both divisions replaced (pr500.md:20) |

### Line B: froghop packed Euclid (Pareto, 799-940 Q)

| PR | Zurich | state | Q | avg T | score | λ / nonce | mechanism | Δ vs previous |
|---|---|---|---|---|---|---|---|---|
| 547 | 09 Oct 04:54 | CLOSED | 940 | 8,738,261 | 8,213,965,340 | ≈0.45 / — | froghop-single: full-quotient Euclid with (r,t) packed in 2×314 lanes; the boundary follows a fixed classical schedule; one hop per step | new `src/point_add`. Design "PX" came from a research sub-agent (pr547.md:18-19) |
| 548 | 09 Oct 05:04 | CLOSED | 836 | 15,933,765 | 13,320,627,540 | ≈0.77 / NONCE=1 | froghop-double: exact packing (W=258, value from lane 0, cofactor from lane W−1), windowed masks, 4-phase two-hop step | sibling of 547: −104 Q for 1.8× T |
| 550 | 09 Oct 05:21 | CLOSED | 799 | 17,366,577 | 13,875,895,023 | ≈0.65 / NONCE=1 | froghop-double with lean bookkeeping: quotient bits stored in the register gap, counter in D's top lanes, 6-bit offset boundary, 3-bit phase code | machine unchanged; bookkeeping 64 → 27 lanes, −37 Q, +9% T (pr550.md:31, 38) |

### Line C: frogdrop 3-of-4 Euclid (Pareto, lowest Q on the board at the time)

| PR | Zurich | state | Q | avg T | score | λ / nonce | mechanism | Δ vs previous |
|---|---|---|---|---|---|---|---|---|
| 551 | 09 Oct 05:46 | CLOSED | 776 | 188,053,328 | 145,929,382,528 | ≈0.63 / nonce 4 | frogdrop: stores 3 of the 4 Euclid values and rebuilds the 4th each column with a 2-adic map Z ← (p − ZX)/Y | −23 Q vs 799 for ~11× T. Would be the lowest graded Q; the previous lowest was 792 (pr551.md:49) |
| 552 | 09 Oct 06:43 | CLOSED | 775 | 185,798,744 | 143,994,026,600 | ≈0.63 / NONCE=4 | as 551 + ancilla-free TTK controlled add + 8-bit size registers | −1 Q, −1.2% T |

### Line D: frogtail → frogstrip, tape-free 2-adic SZ walk (Pareto, 917-948 Q)

| PR | Zurich | state | Q | avg T | score | λ / nonce | mechanism | Δ vs previous |
|---|---|---|---|---|---|---|---|---|
| 584 | 09 Oct 19:41 | CLOSED | 931 | 6,100,038 | 5,679,135,378 (body; no header claim) | ≈0.95 / NONCE=3 | frogtail: Stehlé-Zimmermann walk on two rings (320/308); quotient digits measured going forward and regenerated going backward; no tape, no running payload | new inverter in the frogdrop shell. Its own ladder: 939 × 8.51M → 931 × 6.10M (pr584.md:173-178) |
| 598 | 09 Oct 23:22 | CLOSED | 917 | 5,027,399 | 4,610,124,883 | inherited / nonce 0 | **GPT-6/Codex.** On gnuchev's Frogtail-917: digit erase moved to even ticks; carry cleanup by measurement | base 917 × 5,703,772 (gnuchev). −11.86% (pr598.md:22, 33) |
| 601 | 10 Oct 02:57 | CLOSED | 933 | 4,470,782 | 4,171,239,606 | inherited / nonce 2 | **GPT-6/Codex.** Chunked carry bank with measured boundary carries; peak raised to 933 | +16 Q, −11.07% T, −9.52% score vs 598 (pr601.md:22) |
| 602 | 10 Oct 03:24 | CLOSED | 917 | 3,720,185 | 3,411,409,645 (body) | ~0.7 + 0.007 / NONCE=4 | frogtail + signed-digit products + sign-compressed walks + half counter + cheaper regenerating tick + Codex bank (ported) | base 598: same Q, −26.0% T (pr602.md:22-23) |
| 606 | 10 Oct 09:09 | CLOSED | 948 | 3,034,861 | 2,877,048,228 (body) | ≈2.5 / NONCE=0 | frogstrip: ±1 digits only, strip barrel (1-4 halvings per tick), 300 ticks instead of 556, 315-lane rings, table folds | base 602: +31 Q, −18.4% T |

### Line E: payload walk, 732/739 (Pareto; lowest Q on the board, previous low 770)

| PR | Zurich | state | Q | avg T | score | λ / nonce | mechanism | Δ vs previous |
|---|---|---|---|---|---|---|---|---|
| 624 | 10 Oct 23:57 | CLOSED | 732 | 416,403,331 | 304,807,238,292 | inherited Q770 / 5 | dy divided inside the Euclid walk (no third 256-bit register); Q128 layout switch; counter in Q; 2-bit quotient subsets (QSUB=2) | base: bulengerk's Q770 frogdrop stream (641d38b), which is built on his frogdrop. −38 Q (pr624.md:55) |
| 626 | 11 Oct 00:41 | CLOSED | 739 | 261,923,459 | 193,561,436,201 | inherited / — | same source, QSUB=9 | +7 Q, −154.5M T (pr626.md:24-25) |
| 628 | 11 Oct 02:43 | CLOSED | 739 | 220,601,275 | 163,024,342,225 | inherited / — | 626 + bulengerk R09-R11 cuts, adapted; deferred erasure boxes | same Q, −15.8% T (pr628.md:24-27) |
| 629 | 11 Oct 02:59 | CLOSED | 732 | 328,605,707 | 240,539,377,524 | model 0.54 / 6 | 624 + the same cuts | same Q, −21.1% T; nonce 5 → 6 (pr629.md:213-218) |

Between E and F, nasqret (gpt-astra/Codex) built on 629: zero parking at 731 (f516426b), K=28 at 730 (bef99551), K=27 at 729 (d3883fbd) (pr653.md:46-49).

### Line F: K/KP descent, 728 → 718 (Pareto; each the lowest Q on the board when submitted)

| PR | Zurich | state | Q | avg T | score | λ / nonce | mechanism | Δ vs previous |
|---|---|---|---|---|---|---|---|---|
| 653 | 12 Oct 00:18 | CLOSED | 728 | 321,771,412 | 234,249,587,936 (body) | 0.72 / 6 (kept) | nasqret Q730 with numerator head K 28 → 26 (N 286 → 284); two constants changed | −2 Q vs nasqret's 730 (pr653.md:28-29) |
| 654 | 12 Oct 01:01 | CLOSED | 725 | 320,951,816 | 232,690,066,600 (body) | 4.98 / 51 (searched) | K = 23, the floor (N 281) | −3 Q; λ ×7 (pr654.md:28-29) |
| 656 | 12 Oct 03:30 | CLOSED | 720 | 309,192,269 | 222,618,433,680 (body) | ≈4.8 / 301 | + divisor head KP 30 → 25, pool re-carved 40 → 35, wider payload decoder banks | −5 Q, −3.7% T (pr656.md:25) |
| 658 | 12 Oct 05:42 | CLOSED | 719 | 302,772,952 | 217,693,752,488 (body) | ≈5.4 / 190 | + KP 24, 24-lane payload digit, per-column counter parking (pool 34) | −1 Q, −2.1% T |
| 659 | 12 Oct 06:39 | CLOSED | 718 | 297,655,073 | 213,716,342,414 (body) | ≈5.6 / 480 (the only clean one of 718) | + 8-lane size register sz, estimate start held mod 256 (pool 33) | −1 Q, −1.7% T |
| 660 | 12 Oct 07:30 | CLOSED | 718 | 284,765,142 | 204,461,371,956 (body) | ≈5.5 / 50 | + quotient computed in 24 bits, not 26 (12 subsets instead of 13) | same Q, −4.3% T |

### Line G: Scheme G, 699 → 682 → 680 (Pareto)

| PR | Zurich | state | Q | avg T | score | λ / nonce | mechanism | Δ vs previous |
|---|---|---|---|---|---|---|---|---|
| 663 | 12 Oct 18:32 | CLOSED | 699 | 341,136,387 | 238,454,334,513 | 5.2±0.1 over 3.58M shots / CX(5,274) | Scheme G (quotient by binary search without the second-stage remainder ρ, V form), 13-lane stages, per-shot crossing form R1; pool 13 | base: his 718q (b98ba940). −19 Q, +20% T. First entry below 700 (pr663.md:24-26) |
| ↳ (713) | not submitted | — | 713 | 256,712,364 | — | — | new middle: estimate inside self-contained blocks, in-place quotient and digit, lean map; pool 27 | pr663.md:73 |
| ↳ (708) | not submitted | — | 708 | 332,940,625 | — | crossing ~0.25 | Scheme G, 16-lane reserve, pool 22 | pr663.md:74, 332 |
| ↳ (705) | not submitted | — | 705 | 333,675,801 | — | crossing ~1.8 | 13-lane reserve, pool 19 | pr663.md:75 |
| ↳ (704) | not submitted | — | 704 | 336,306,963 | — | — | + two flag lanes join the parking cycle; 14-lane reserve, pool 18 | pr663.md:76 |
| ↳ (703) | not submitted | — | 703 | 341,993,371 | — | crossing 1.81 | every stage fits 13 pool lanes; 13-lane reserve, pool 17 | pr663.md:77, 224 |
| 697 | 15 Oct 04:45 | CLOSED | 682 | 645,088,611 | 439,950,432,702 | **stated 2.51; corrected 2.545 (2M) / 2.71 (4M) in pr699.md:131-134** / CX(5,14) | Scheme G on a 265-lane ring: chunked quotient sessions, sizes stored as a gap, map room taken from operand trailing zeros, 16 remainder lanes off the ring | base: jackylee0424 3bcef1d9 (694) + 261d4e06 (693). −11 Q vs 693, 1.9× T (pr697.md:28-30) |
| 699 | 15 Oct 09:58 | CLOSED | 680 | 669,414,940 | 455,202,159,200 | 2.63 (4M) / CX(5,60) | 682 on a 263-lane ring: Y's leading one and the act lane lent to R; exact switch-tail and delayed-move cuts | −2 Q, +3.8% T, lower λ (pr699.md:27-29) |

### Line H: 9-lane pool, 672/671 (19-20 Oct; +205k/−181k-line diffs)

| PR | Zurich | state | Q | avg T | score | λ / nonce | mechanism | Δ vs previous |
|---|---|---|---|---|---|---|---|---|
| 815 | 19 Oct 23:30 | CLOSED | 672 | 823,416,006 | 553,335,556,032 (body) | 3.28 / 51 | 9-lane pool: bq/cmpc/f/g bound to lanes of the spare size register sx; two-engine crossing V forms; S5_NOPARK | base: jackylee0424 8cbf3480 (676, which is his 680 plus their work). Previous low was odinfree 675. Single agent (pr815.md:18) |
| 818 | 20 Oct 02:42 | CLOSED | 671 | 828,353,029 | 555,824,882,459 (body) | 3.34 / 90 | 672 + odinfree's ring 258, avoiding a fourth routed owner; jackylee digit cuts | −1 Q, +0.6% T (pr818.md:92) |

Diff sizes (`prs.json`): +2.2k to +5.2k for 547-552, ~+17-18k for 624-660, +21k for 663, +29k for 697/699, +205.5k/−181.7k for 815/818.

---

## 2. Mechanisms

### 2.1 Leapfrog (PR 500) [his; sub-agents ported the merged cell+barrel and the early-room squeeze]

**Why it works.** Every binary-GCD walk pays two bills (pr500.md:40-43):
- **Tape:** one stored bit per data-dependent decision, about 620-720 bits for every family he measured.
- **Payload:** P = λ·R mod p follows every decision with full 256-bit modular work.

So Q×T is "fairly flat across designs" (pr500.md:43). Leapfrog makes each decision cheaper in T: 5 decisions share 3 add-halve cells and 1 rotation.

**Registers.**
- Two odd rails. Per-tick widths (W, n0, n1, n2, nb) come from the envelope fit (pr500.md:63).
- A 5-bit letter per tick on a tape: 139 × 5 = 695 bits (pr500.md:40).
- The payload pair, 2 × 256 = 512 qubits (pr584.md:54).
- Total Q = 1243 (pr500.md:19).

**Tick** (target A = tick parity, source B; no routing swaps) (pr500.md:47-53):
1. Two forced add-halves x ← (x ± B)/2. The sign comes from the low bits so x stays odd (letters s0, s1).
2. One choice add-halve (letter s3). x ± B gives a "deep" candidate (≡ 0 mod 4) and a "flat" one. Take deep when it is admissible and the signs differ, or when e ≥ 2. In the equal-sign e = 1 case, a 24-bit top-window compare (W1) decides: deep iff |x| > 4|B|, at a per-tick anchor position.
3. Barrel: strip e ∈ [0,3] trailing zeros (letters k1, k2). On the payload this is a controlled multiply by 2^−e: a 4-way rotation built from 3 controlled reflections (1.5n − 2 CSWAPs) plus a merged constant fold, P·2^−e = rotr_e(P − m(f−1)) with m = P mod 2^e. The third add-halve and the rotation run as one "Montgomery-style op" (pr500.md:59). The note does not define f.

**Letter.** All 32 values occur, and a post-tick state has ~20-32 consistent preimages, so the letter is "locally information-optimal" (pr500.md:53).

**Seed "B"** (pr500.md:53): R0 = d or d − p (odd), R1 = (R0 ± p)/2 (odd), payload (y, y/2).

**Traversal plan** (pr500.md:53): the divide runs the payload forward with the rails, then reverses the rails alone. The multiply runs the rails forward and fuses the payload into the walk-back. Total: 4 rail traversals and 2 payload passes.

**Reorder** (pr500.md:65). Early ticks are qubit-bound: two full rails plus two payload registers forced split carry ladders. For ticks 0..75 the divide runs the rails alone first, with one payload register live. It then runs a payload-only pass over the taped letters, with the rails parked at tick 76. The multiply mirrors this. No extra rail traversal is needed because the tape already holds the letters.

**Joint width envelope** (pr500.md:63). Failures cluster in a few "fat" walks: the union bound gives 2.6e-2, the actual rate is 7e-4. The greedy "peeling" fit, run on 1.92M recorded walks:
1. sacrifice the no-park walks;
2. repeatedly lower the position that saves the most priced T per sacrificed walk;
3. take survivor maxima.

T is priced per bit-tick per tick region, measured in-circuit. The fit was validated on 1.28M fresh walks. It allowed R = 139 ticks at the same failure rate.

**λ budget** (pr500.md:69-73): 14.4 ± 0.4 over 96 nonces, "under the 19.5 social cap". About 12.8 of it is walk-envelope tail plus no-park, which a classical screen predicts exactly. The rest is payload-cell window misses: fold window, chunk compares, and the 32-bit low-cut retained prebias.

**Files** (pr500.md:77): recipe `leapfrog::install_recipe()`; every lever gated by an `LF_*` env flag (the note gives only the prefix); `leapfrog_data/env_w1_peel139{,_steps}.txt`; `leapfrog_data/anch_w1.txt`.

### 2.2 Measurement-based point-add shell (reused by every Pareto line) [adapted from Luo et al. and gnuchev]

Steps (pr547.md:112-115; pr584.md:124-127):
1. dx = x − ox, dy = y − oy.
2. Division 1 gives λ = dy/dx.
3. dy is measured away (Hmr). Its phase is fixed by recomputing λ·dx.
4. dx' = λ² − dx − 3·ox.
5. ndy = −λ·dx'.
6. λ is measured away. Division 2 recomputes λ = −ndy/dx' to fix that phase.
7. x3 = dx' + ox, y3 = ndy − oy.

Products use p = 2^256 − c with c = 2^32 + 977. In froghop they are double-and-add with fold and 32-lane truncated carry headroom (pr547.md:113-115).

### 2.3 froghop-single (PR 547) [his; register sharing and bottom-up cofactor erasure from Luo et al. arXiv:2607.13816]

**State** (pr547.md:66-69).
- Cross pairing: D = (r_{i−1}, t_i), V = (r_i, t_{i−1}), each W = 314 lanes.
- Cofactor in wires [0, M), remainder in [M, W), same orientation.
- M(σ) is a classical per-slot schedule (`sched.txt`). Moving it is a free relabel because the top wire is always a zero gap.
- V is rotated against D by a counter π.
- Input x' = min(dx, p − dx).

**Slot** (pr547.md:75-80). One hop per Euclid step:
- **OUT (up):** pop bit b; td += b·(tv≪π); erase b with [td ≥ tv≪π]; test alignment [R ≥ rv≪π]; move up or turn.
- **RET/DIV (down):** c = [R ≥ rv≪π]; R −= c·(rv≪π); push c onto a 24-deep stack. At π = 0, swap D/V and apply the new quotient's bit 0.
- About 2.4-2.55 slots per quotient bit; 900 fixed slots per traversal.

**Reversibility** (pr547.md:82-87). Every decision is recoverable from the post-slot state:
- division bits through the stack and the bottom-up compare (needs t_{i−2} < t_{i−1});
- moves through the phase;
- turn vs return through a compare wired one position higher;
- first-step and finished flags through zero tests and a frozen-slot counter.

**Cost per slot ~1,840 T** (pr547.md:89-98): remainder ladder 437, cofactor ladder with mid-ladder erase 505, turn discriminator on the top 96 lanes 192, V rotation 312, D/V swap 314, control 90. Per traversal ~1.66M; 4 traversals plus products give 8.74M (pr547.md:100).

**Levers.**
- Two-way rotation: finished shots oscillate π (+1 on even slots, −1 on odd), so the V move is a free relabel by −1 plus a controlled rotate-by-2. That costs W − 2 instead of 1.5W, −157 T per slot, and took the build from 10.25M to 8.74M (pr547.md:107-108).
- Short discriminator on 96 lanes, exact unless the relative gap is below ~2^−46 (pr547.md:109-110).

**Width.** W = 314 was fitted on 200k shots. A first W = 308 fitted on 30k shots failed one official shot (pr547.md:125-126). The ~110 lanes of slack (2 × 314 vs ~2 × 259) buy "no boundary checks" (pr547.md:54).

### 2.4 froghop-double and lean bookkeeping (PR 548, PR 550) [his; exact-packed layout after gnuchev; masked carry cells are bulengerk's "mask the carry transition"]

**PR 548** (pr548.md:65-96).
- Layout: W = 258. The value's LSB is at lane 0; the cofactor's LSB is at lane W − 1, growing down. Only the boundary floats. The information bound is bl(r_j) + bl(t_{j+1}) ≤ 257.
- The orientations are reversed, so alignment and cofactor update cannot share a ramp. The 4-phase machine:
  1. AL (π = 1..k+1): find the quotient length;
  2. DV (π = k..0): restoring division, bits pushed onto a 24-deep stack;
  3. CO (π = 1..k): pop and apply to the cofactor, erasing mid-ladder;
  4. RT: return, then swap D/V roles.
- 1,240 slots per traversal, ~7.8 per Euclid step.
- One shared 8-bit boundary register b. All masks derive from b, π and the phase.
- Masks are toggled by incremental one-hot decoders only inside classical per-slot windows (`sched_double.txt`), built from a 1.2M-shot envelope.
- "Late source": the discriminator uses rv's always-1 MSB lane as its constant (pr548.md:93-94).
- Lean fold: overflow is folded back as +(2^32 + 977) through 23 clean and 9 dirty-borrowed lanes (pr548.md:95-96).
- About 2,800 T per slot, of which masking ~900 and swap+rotation ~560 (pr548.md:83-85).

**PR 550, bookkeeping 64 → 27 lanes** (pr550.md:42-73):
- quotient bits written into V's gap at lane b + j (the top bit is never stored), with one merged push/pop swap scan at physical lane (b − 1) + depth + π;
- finished-shot counter in D's top lanes, since D = (1, p) once a shot is done;
- 6-bit offset u = (b − 1) − base(σ), re-centred each slot;
- 3-bit phase code: AL 001, DV 010, CO 011, RT 000, DONE 100;
- the moving bit lives in p2, so p2 is the ladders' write gate;
- "conditionally clean decoder levels" in depth bits 0..3, which are |0⟩ for every turning shot;
- limited-prefix decoders followed by a Barenco MCX on borrowed dirty dy qubits;
- increments with n − 2 ancillas.

The machine's floor is about 795: 772 for the registers plus 20 persistent control lanes (pr550.md:52).

### 2.5 frogdrop, 3-of-4 Euclid (PR 551, PR 552) [his; the idea follows Luo et al., gnuchev's Q810 and bulengerk's Q792]

**Invariant.** r_{j−1}·t_j + r_j·t_{j−1} = p, so any three values give the fourth (pr551.md:34-35, 54-56). The column map Z ← (p − Z·X)/Y is exact mod 2^L on a per-shot region (pr551.md:58-63).
- **HR** (early): Z = r_j, X = t_{j−1}, Y = t_j.
- **HT** (late): Z = t_j, X = r_{j−1}, Y = r_j.
- The switch happens at the first HR state with bl(r_j) ≤ 118. It reuses the map with operands exchanged; nq = 138 (pr551.md:63-69).

**Layout, 776** (pr551.md:74-86):
- dy 256, also the dirty pool for every carry chain;
- ring 288: Z at the bottom, top pair value reversed at the top, ≥ 31-lane gap;
- Q 138;
- sy, sx 18;
- phase plus a 7-bit idle counter, 8;
- column scratch pool 68.

**Column** (pr551.md:88-110):
1. probe sz = bl(Z);
2. masked swap brings Y into Q;
3. streaming quotient estimate P: rotate the ring so Z's top K = 29 bits sit at the top, and Q so Y's top KP = 30 bits do; stream a restoring division of all-ones by Zh = Z_hi | 1 into a second division by Yh; only the last QB = 24 steps compare; reciprocal bits come back from the remainder's parity, so the reciprocal is never stored; outputs q0 (24 bits) and ρ (31 bits);
4. the middle:
   - HR: bq = [ρ < Xh]; T −= bq·t; bq ^= sign; T += q0·t;
   - HT: the complement trick ~(~R + q0·r);
5. undo P;
6. map: v2 alignment, multiply in a rotated frame with decoder-gated controls, p − Z, masked swap, divide by Y_odd;
7. switch exchange, phase, idle counter.

**Idle machinery** (pr551.md:121-126). The four maps form a Klein four-group, so a one-column identity is impossible. Finished shots alternate A0/B0 under a 7-bit counter, and "done" means counter ≠ 0. The final sign is (−1)^N, applied to the product.

**Schedule.** 203 columns. Envelopes come from 1M shots per column kind, smoothed ±4 columns, widened by 4 bits, with kind windows extended by 6 columns. Validated on 2M fresh shots with 0 misses (pr551.md:137-139).

**Cost.** ~46M T per traversal, ~60% of it in the map (pr551.md:135). The circuit is 638,940,473 ops, ops.bin is 1.66 GB, and local eval takes ~6 min and ~36 GB (pr551.md:162-163).

**PR 552 arithmetic** (pr552.md:55-78):
- Takahashi-Tani-Kunihiro ripple add. Carries are computed unconditionally and only the n sum-writing CNOTs become ctl-Toffolis: 3n − 2 T against ~3n for the controlled Cuccaro.
- Exact overflow flag k = ctl ∧ carry_out at 4 T on a borrowed qubit.
- Flag erase through a top-32-lane compare on the same carry-in-free chain, 2n + 3. A borrowed carry-in breaks the z = y case, which the Horner product hits.
- NAF fold increments on borrowed qubits: x −= g; g = ~g; x −= g; g = ~g gives x + 1 for any g.
- sy/sx at 8 bits, because they only hold sizes ≤ 138. This exposed a decoder that asked for lane values up to 288 with no range check: 288 aliased mod 256, so it is now range-guarded (pr552.md:76-78).

### 2.6 frogtail, a tape-free 2-adic inverter (PR 584) [his; walk from Stehlé-Zimmermann ANTS 2004; carry pool from gnuchev]

**Walk** (pr584.md:74-92).
- Shelves A and B hold (value, cofactor) pairs with A.v·A.c + B.v·B.c = p.
- Start A = (p, 1), B = (x', 0), where x' is dx made odd. End A = (0, C), B = (±1, ±p).
- 1/x' = (−1)^S·C·2^−T with T = 556 ticks, S = [B.v = −1] ⊕ parity ⊕ [dx even].
- Rings: A 320 lanes, B 308. The value ascends from frame 0 and the cofactor descends from the top. A's frame offset equals the tick, so halving A.v and doubling A.c is a pure relabel.
- A classical boundary schedule c(t) is shared by both shelves. Lanes that change owner take the new sign with CNOTs.
- Tick (j = gap counter, 8 bits):
  1. step end (t ≥ 2): e = [j < 0] ∧ A.v odd → j ← −j, parity ^= e, controlled swap A ↔ B, then e is erased as the new A.c's low bit;
  2. digit: a = A.v[0] ∧ [j ≥ 0]; A.v += (−1)^[j=0]·a·B.v; B.c −= (−1)^[j=0]·a·A.c;
  3. halve (relabel), j −= 1.

**No tape** (pr584.md:96-111).
- Forward: X-measure each digit, leaving phase (−1)^(m_t·a). About 1,206 T per tick.
- Inverse: run a "regenerating" tick backwards. It holds the current step's digits in Q (23 qubits) and erases them at step end through Q·b + L ≡ 0 (mod 2^(g+1)), where b = A.c >> s' (odd), s' = ν(A.c), L = B.c's low bits, g = j + s'. The erase is a normalizer, Q ← −(Q·b) mod 2^23, a rotation by g and a masked XOR.
- Played backwards, this recomputes each digit just before it is undone, and Z^(m_t) cancels the measurement phase. About 2,800 T per tick (pr584.md:115-120).

**Products** (`modp_ft.rs`, pr584.md:129-137):
- every free qubit below the peak is a clean carry lane (`Ms::alloc_room(PEAK)`);
- folds add ctl·const over a 64-lane window, ~61 T, with the constant's bits taken from the control;
- flag erase is a 32-lane compare, 33 T;
- the controlled add is hybrid: Gidney logical-AND carries on the pool (2 T/lane), then a controlled Cuccaro (3 T/lane);
- λ = (−1)^S·C·dy·2^−556 by a bottom-up halving Horner.

**Cost** (pr584.md:156-171). The walks are 73% of T; the two inverse walks alone are 51%. **Peak** (pr584.md:150-152): dy 256 (borrowed dirty) + B 308 + A 320 + Q 23 + j 8 + 2 flags + 14 scratch = 931.

**λ ≈ 0.95** (pr584.md:185-192): B ring width 0.26, gap cap g ≤ 22 0.56, normalizer 0.04, ticks 0.04, finished-shot cofactor growth 0.05.

### 2.7 Arithmetic and walk levers on frogtail (PR 598 and 601 are Codex; PR 602 is his)

**Codex, PR 598** (pr598.md:45-67):
- Even-tick erase: j ≡ t (mod 2), and a quotient's last digit occurs at j = 0, which only happens on an even tick. So the erase is emitted only after even ticks, under [j = −1]. With the conditional gap decrement this saved 652,498 T.
- Measured carry cleanup: X-measure the flag, capture the outcome in a condition scope, and run the phase correction only on 1. That is 33 → 16 T expected per cleanup, × 1,404 cleanups = −23,868 T.

**Codex, PR 601** (pr601.md:40-65; adapted from `skycof_mm`, SkyCof line):
- Chunked carry bank. Each chunk computes carries with temporary ANDs and erases its internal carries. Only the inter-chunk carry stays live.
- Boundaries are X-measured in reverse order; the exact phase oracle (k − 1 T) runs only on outcome 1, so it costs (k − 1)/2 in expectation.
- Example: a 256-bit add with 24 carries is 742 emitted and 626.5 expected.
- Gains are discontinuous in the peak budget. A resource model scanned 917-1100 Q and picked 933.

**His, PR 602** (three sub-agents for products, walk and inverse walk; pr602.md:18-19, 206-208).

*Signed-digit products* (pr602.md:76-95):
- a = 2^(n−1) + Σ_k (2·a_{k+1} − 1)·2^k − (1 − a_0), so every Horner step adds or subtracts y.
- Subtraction is z − y = ~(~z + y), with the sign applied as CNOTs, so the adder needs no quantum control. Pool lanes drop 2 → 1 T and Cuccaro lanes 3 → 2.
- Per modular add: 531 T at a 76-lane pool, 460 at 147, 353 at 256.
- x' squared in place: a squaring Horner on x with λ as both digit source and addend.
- Tails run on C mod p (256 steps instead of 318).
- λ-hat: measure λ as λ·2^300.
- Two exactness traps:
  1. the complemented subtraction's overflow flag is [w < y + c], so the erase compare takes the subtract bit as its carry-in;
  2. accumulating +C·y reaches the non-canonical p, so the tails accumulate −C·y.

*Sign-compressed walks* (pr602.md:99-109):
- Early shelves carry 10-48 lanes of pure sign extension.
- CNOT those lanes clear, run the add and swap only over the per-tick envelope kv(t), kc(t), and lend the cleared lanes to the carry pool. Restore with the same CNOTs.
- The envelope (`lsc_frogtail.txt`) is the per-tick max over 600k walks, running max ±3 ticks, +2 lanes. Zero T overhead; adds λ +0.007.

*Half counter* (pr602.md:111-113): store h = (j − t mod 2)/2 in 5 bits. On odd ticks the negation is a free complement and [j = 0] is skipped.

*Cheaper regenerating tick* (pr602.md:117-131):
- the digit is computed straight into its lane;
- the normalizer runs on A.c >> 1;
- zero tests and the step-end flag e are erased by measurement plus the AND phase oracle;
- rotation by g is a 4-way rotation;
- the masked XOR uses one 6-bit decoder over (g, e);
- [j = 0] is taken by measurement.

Even ticks went 2,433 → 2,268 T, odd ticks 1,250 → 1,219.

*Stack:* 5,027,399 → 4,659,970 (walk) → 3,920,772 (signed-digit) → 3,720,185 (bank) (pr602.md:65-70). A peak sweep gave 3.411B at 917, 3.403B at 925, 3.384B at 927, 3.385B at 928; he stayed at 917 (pr602.md:142-143).

### 2.8 frogstrip (PR 606) [his; redesign study, build and lever round by three sub-agents]

**Idea** (pr606.md:32-37, 61-77). Remove empty ticks. Every SZ quotient can be written with ±1 digits only, and trailing zeros are stripped by a barrel inside the same tick. A tick then does 1-4 halvings, and a walk takes 300 ticks instead of 556.

**Tick:**
1. step end, e = [j ≤ −1] ∧ A.v odd;
2. digit a = [j ≥ 1] ∧ B.v odd, with sign (A.v[1] ⊕ B.v[1]) ⊕ [j = 1]; A.v ±= B.v, B.c ∓= A.c;
3. halve (relabel);
4. strip k = min(ν(A.v), 3) under G = [j ≤ 0], by a segment rot4 (3 controlled reflections) over live lanes; wrapped lanes take their new owner's sign (4 T).

**Counters.**
- The strip pattern is fixed, min(z, 3 + 4i), so k = (−j) mod 4. The barrel controls are recomputed from j with CNOTs and erased by measurement.
- j + t + S is always odd, so j is stored as j >> 1.
- The completion flag doubles as the erase control and the strip trigger.

**Absorption** from tick 256; a final barrel rebuilds C' = C·2^sh (pr606.md:79-81).

**Inverse erase** (pr606.md:88-92): word plus marker gives (2D + 1)·b ≡ L (mod 2^(g+1)). It runs every tick, since completion parity differs per shot.

**Arithmetic** (pr606.md:97-113):
- table folds: each addend bit is an ANF Boolean function of 2-4 controls;
- four doublings per fold, since c − 1 = 16·(61 + 2^28), so 16·z mod p is a relabel plus one 64-lane fold (replaces 871 single doublings and halvings);
- fused add-then-halve: (z~ + δ·c)/2 + h·2^255;
- streaming digits: X-measure each digit after its last use and lend its lane to the pool;
- the λ-fix uncompute as a functional inverse above step 48 (failure ≤ 2^−49 per tail).

**Cost.** Per tick, forward ≈ adds 720 + barrel 460 + swap 308 + control 35; the inverse adds ~920 for the erase (pr606.md:134-136).

**λ ≈ 2.5 on 4M walks**: gap cap ~2.0, the rest ~0.5 (pr606.md:149-151).

### 2.9 Payload walk (PR 624/626/628/629) [his: payload division, Q128 switch, counter in Q, subset quotient, prefix bound, care-rotation extension, single-ripple HT division, the exact evaluator replica; ported: bulengerk R08-R11]

**Payload division** (pr624.md:77-89).
- Carry dy as (d, L) = (dy, 0). At each Euclid level j: e = ⌊d/r_j⌋, d −= e·r_j, L += e·t_j. At the end L ≡ dy/dx. Checked with 0 mismatches on 20,000 random inputs.
- bits(d) + bits(L) ≤ 257, so they pack from opposite ends of one 259-lane register.
- Each column does a restoring long division into a 26-bit digit register e, adds e·|t_j| into L, and erases e bit by bit with compares against 2^k·|t_j|.
- L is kept in offset form V = σ_j·L − |t_{j−1}| + |t_j| (minus [j odd]), so every erase is a non-strict compare and every level transition is W → q·|t_j| + ~W.
- Four traversals, with the λ² Horner between the two pairs (pr624.md:88-89):
  1. forward with payload (dy → λ);
  2. inverse without payload;
  - then λ² by in-place squaring Horner from the payload (515 live qubits, pr624.md:72-74);
  3. forward without payload;
  4. inverse with payload (λ → λ·dx', giving y3).

  No product register is ever allocated.

**Q128 switch.** Switch HR → HT at the first bl(r_j) ≤ 128, so Q needs 128 lanes, not 138 (pr624.md:91-92).

**Counter in Q** (pr624.md:94-96). The 7-bit idle counter sits in Q's top 7 lanes; finished shots' Q values are below 2^26. "Done" is derived: HT phase, Q[64..121) empty and counter non-zero. Every probe parks the counter out of its range first.

**Subset-storage quotient** (pr624.md:98-104). P yields 26 bits per column but stores one subset at a time (QSUB = 2: 13 subsets; QSUB = 9: 3 subsets of 9, 9, 8).
- Unstored bits are computed into a clean lane and erased at once by parity: q = par(ρ′) ⊕ par(R′) ⊕ g, with virtual-odd divisors Zh|1 and Yh|1.
- Switching subsets replays P's tail backwards, then forwards.
- q·Y adds are bracketed by +Y/−Y so no borrow reaches the gap.
- Each extra subset costs about 15.5M emitted T. QSUB 2 vs 9 costs 154.7M (pr624.md:153-155), or 107.7M after deferral (pr628.md:181).

**Peak table, 732** (pr624.md:59-68): payload 259, ring 288, Q 128, counter 0, phase 1, sy/sx 16, pool 40. Two bits is the floor of this layout (pr624.md:71-72).

**Prefix-skip bound** (pr624.md:121-126). r_{j−1}·|t_j| ≥ p/2 and r_{j−1} < (q_j + 1)·r_j with q_j < 2^26 give bl(r_j) + bl(t_j) ≥ 228, so every column skips 24 compares. The smallest sum seen over 20,000 walks was 233.

**Care rotations** (pr624.md:127-132). A rotation is recorded as an UP permutation that is exact only on the lanes P reads; its inverse is used for DOWN. He extended bulengerk's `rot_by_range_care_y` to the ring, every subset switch and the H51 certificate.

**Deferred phases** (pr624.md:134-138). Forward walks 1 and 3 measure row-boundary carries without the phase comparator. Mirrored inverse walks 2 and 4 recompute them and cancel the phases with classically controlled Z. This is valid because the payload never touches the walk registers.

**Deferred erasure boxes** (pr628.md:146-158) [adapted bulengerk b6907bb1].
- The forward walk X-measures the box outputs and keeps the outcomes as classical masks. The mirrored inverse recomputes the outputs and applies Z under the masks.
- The builder hashes each box's gate list and asserts the forward and inverse boxes match.
- Requirements: every output is computed from zero by the box, and the walk state is identical at mirrored positions.
- Box 501 (HT bq erasure) and box 502 (the un-P core). That deferral took 250.9M → 225.6M emitted at 739.

**Single-ripple HT division.** Read the borrow into the gap lane after the up pass; the down pass writes only where q_k = 1. 3 instead of 6 T/lane (pr624.md:140-142).

**Ported-cut ledger, emitted T at 739** (pr624.md:107-119; pr628.md:113-126): 327.18M as built → 314.29 → 312.6 → 309.8 → 289.0 → 277.1 → 275.5 → 271.14 → 266.43 → 257.40 → 253.48 → 250.90 → 225.62.

**Adaptations he declined or changed** (pr628.md:159-165): bf1897f0's counter-lane loans are not used; the H51 bank takes max(sy, 28); small pools fall back to the old probe.

### 2.10 K/KP descent and pool re-carve (PR 653-660) [his on nasqret's Q730; nasqret supplied zero parking and the first K cuts]

**Two heads** (pr653.md:55-62).
- The numerator head is K bits of ring value Z. The reciprocal remainder uses K + 1 ring lanes, and zero parking makes headroom h = N − 257 = K + 1, so N = 258 + K: one qubit per bit of K.
- The divisor head is KP bits; ρ uses KP + 1 lanes = 8 (spare size register) + KP − 7 pool lanes, so pool = 17 + (KP + 1 − 8) (pr656.md:64-67).

**K sweep on paired inputs** (same 1,082,880 divisions per K: 60 nonce shot sets × 9,024 shots × 2 divisions, hashed from one op stream; pr653.md:80-83; pr654.md:85-94):

| K | Q | model λ | hunt result | official result |
|---|---|---|---|---|
| 28 | 730 | 0.20 | — | pass |
| 27 | 729 | 0.33 | 0/16,384 | pass (his build; same average as nasqret's d3883fbd) |
| 26 | 728 | 0.72 | 0/16,384 | pass (graded, 5fa63407) |
| 25 | 727 | 1.32 | 0/16,384 | fails 1 shot at nonce 6; nonce 8 passes |
| 24 | 726 | 2.67 | 0/512 (stopped early) | — |
| 23 | 725 | 4.98 | 7/16,384 bad | nonce searched; nonce 51 passes (this build) |
| 22 | 724 | — | almost every input fails | — |
| 20 | 722 | — | every input fails | — |

The rate roughly doubles per bit, then collapses below 23.

**KP sweep at K = 23** (pr658.md:76-81): 30 → 24 is flat (≈5.0 → 5.53); then 23: 7.08, 22: 12.1, 21: 21.5, 20: 40.0.

**Re-carve** (pr656.md:90-122; pr658.md:126-134; pr659.md:139-150; pr660.md:153-162):
1. Stage 2's 8-lane temp U is removed via sy ^= js·T and `probe_gated`.
2. Stage 14/15 temps go to sz lanes, which are clean after stage 9.
3. `carve` takes tmp, tmp2, probe prefixes and js from the ρ region.
4. Payload HT narrowing runs before the switch flag and borrows its lane.
5. The payload digit's stepping flag rides on the switch-flag lane.
6. Payload decoder banks take the digit's own clean unwritten lanes, with a fallback `mask::ge_const_need`. Worth −11M T at any KP.
7. Payload digit 26 → 24 lanes: e_j ≤ q_j, and the model already fails q ≥ 2^24. −3.5M emitted per payload traversal.
8. Counter parking trimmed to 5 bits on columns that can both switch and hold finished shots.
9. sz 9 → 8 lanes: bl(Z) ≤ 255 after column 0; column 0 borrows the switch-flag lane.
10. Estimate start held mod 256 with offset −220; the four warm-up compares become constant and are skipped. −2.4M per payload traversal.
11. A 9-bit payload start s = sz + sy.
12. q0 computed in 24 bits, not 26: the top subset {24, 25} is always zero on passable shots. −12.9M T (−4.29%).

**Equivalence first** (pr656.md:124-127): the re-carve was built at KP = 30 and failed exactly the same inputs as the unchanged source on 16,384 divisions and 4,096 point adds before any lane was cut.

### 2.11 Scheme G, 13-lane stages and per-shot crossing form R1 (PR 663) [his]

**Census result** (pr663.md:318-320): the column middle's two-stage estimate (R + ρ) set the pool.

**Scheme G** (`midg.rs`, pr663.md:135-158).
- Let s = sz − K, Zh = (Z >> s) | 1, F = ⌊(2^(256−s) − 1)/Zh⌋.
- Test over(W) = [(W >> u) > (F >> u)], u = max(0, 257 − sz − TC), TC = 24.
- F's bits stream MSB-first out of a restoring division whose only state is R (K + 1 lanes), and are subtracted from W's window in place. There is no ρ and no q0 replay.
- **V form:** add T − G once per column, with T = 2^(257 − sz) and G = ((F >> u) + 1) << u. Each search test then reads a single lane (bit 257 − sz). The reciprocal runs twice per column (enter and leave), not once per test.
- **HR:** binary search MSB-first, each bit gated by a 6-lane v = (sz + sy + 38) mod 64 (bit kb allowed only if kb < 258 − (sz + sy)); then V −= qY, leave the V form, and run D⁻¹.
- **HT:** restoring division writes q into the ring headroom (sign read at 257 − sz). The payload update runs with q parked in Q above Y, then a reverse search.
- **Working set:** 13 pool lanes (sz 8, sw, the bit-128 lane, the P zero, c0, act). sx is the scratch.

**13-lane stages** (pr663.md:118-131):
- helpers live in the idle sx;
- sy is erased around the payload narrowings by a masked probe of the ring top and recomputed after;
- the done test skips counter parking;
- on the 23 counter-parking columns (97-120) the map frees sy inside its core;
- the digit fits 12 lanes.

**Crossing reserve** (pr663.md:162-168): a parking shot fails if bl(r_j) + bl(q_j) − 129 > D.

**Two free reserve lanes** (pr663.md:170-179). ph and sw (or act) have a fixed value on every parking shot. This holds by construction, not by sampling. With the 7 idle lanes they give a 9-lane reserve.

**R1** (pr663.md:181-219).
- Each shot switches at its crossing only if bl(r_j) ≤ bl(t_j). Otherwise (~40% of crossings) it takes one more HR step, so the need becomes min(bl r_j, bl t_j) + bl(q_j) − 129.
- A delayed shot would end its column looking like an ordinary HT shot, so its control could not be uncomputed. The fix is a hand-off signature: a delayed shot starts column c+1 with sz = bl(t_j) ≤ 127, while every regular HT column start has bl(t_k) ≥ 128.
- DL is recomputed from size registers wherever needed; no lane holds it.
- Ten DL-controlled swaps move t_{j+1}'s high bits; DL-gated probe pairs fix sz.
- The schedule is regenerated with the same margins. Run with the old rule, the generator reproduces the old schedule byte-for-byte.
- Crossing λ: 9-lane reserve with HT-only form ≈ 30; 13-lane reserve (703) 1.81; 9-lane with R1 ≈ 0.03 (pr663.md:221-225).

**Cost** (pr663.md:236-243). Scheme G is +76.2M T (+30%) vs the 713. The 13-lane squeeze adds +5.7M. R1 is net −0.86M, because the regenerated schedule's largest ring-top value drops from 156 to 144 bits.

**Baked constants** (pr663.md:294-302): `MID2_POOL=13, MAP_LEAN=true, SLIM=true` (frogdrop_col.rs); `FORM_CHOICE=true` (frogdrop_sched.rs); `MIDG_ON=true, G_IP5=false, PARK_RES=9` (midg.rs); `DIG_ZPAD=true` (payload.rs); `NONCE=274, NONCE_CTRL=Some(5)` (mod.rs). Dev switches `FD_OLDMID, FD_POOL, MIDG_RES, FD_MAPEXTRA, FD_PRED_RHO` are all off with an empty environment (pr663.md:304-306).

### 2.12 Lending provably-zero lanes to R; ring 277 → 265 → 263 (PR 697, PR 699) [his, with three sub-agents; ported jackylee0424's virtual constants, bulengerk 7ce370d, nasqret 36378f0]

**PR 697** (pr697.md:69-115). Width is set at the V-form instant.
- **K-lane remainder:** compare and subtract before the rotation, so R is 24 lanes instead of 25. The compare is an ancilla-free TTK chain fed a virtual constant.
- **Virtual constants** [jackylee]: the divisor's always-zero top bit and the head's always-one leading bit enter the comparator as constants; the leading-one lane is flipped to 0 and lent to R.
- **16 off-ring R lanes**, each provably |0⟩ on active shots during every V-form play: sx[1..7], c0, P-zero, two gap-freed size lanes, the top size lane, ph, sw, sy[7], and the leading-one lane.
- **Chunked quotient sessions:** at most one quotient chunk is stored or parked at a time. Crossing columns use cuts [1, 3, 7, 15] (largest chunk 8), so parks need no reserve lane. Other columns use 2 chunks that fit K + 6 slots, with a build-time assertion.
- **Gap form:** at each V-form play, sy is compressed in place to g = (1 − sz − sy) mod 128, an ancilla-free involution. g ≥ 32 implies an already-counted quotient-cap failure.
- **Narrowing identity** bl(r_j) + bl(t_{j+1}) ∈ {256, 257} replaces an 8-lane probe.
- **Trailing-zero map room:** X and Y are coprime, so one is odd. The even operand's own e zero lanes become the multiply's room. One flag t = [X even] selects the case. Extension lanes drop 13 → 0 and EMAX rises 21 → 31.
- **In-place HT division**, with the payload transition split from it and bits ≥ K parked directly.
- Ring N/K: 276/17 (693) → 265/6.

**PR 699** (pr699.md:65-108).
- **Y's leading one:** Q[sy − 1] = 1 on every active shot. A census of 2,046 plays × 512 shots found no exception in 1,582 active plays (pr699.md:67-70). A swap tree on sy gathers it to a fixed lane, flips it to 0, and lends it to R.
- **Act-free V form:** a non-stepping shot runs enter and leave, which cancel exactly, so act can be uncomputed (≈2 T on HR plays) and lent to R. Despite the extra ring step this is −1.2% T per traversal vs ring 264.
- **Ring 263, K = 4:** R = ring[0..6) + 18 off-ring lanes. The stage-5 split park gets 5 reserve lanes plus a "Y-top slot" (the cycle's last lane holds Y's top bit = 1 after rotation). That slot takes park failures from 8 to 1 per 4M.
- **Exact switch-tail and delayed-move cuts:** probes now cut at the other value's actual size, not a fixed 128 or n/2. The bound bl(r_j) + bl(r_{j−1}) ≤ 257 makes this ring-independent. It removed 16 + 9 failures per 4M.

### 2.13 The 9-lane pool, 672/671 (PR 815, PR 818) [his, single agent; base is jackylee0424's 676; PR 818 ports odinfree's ring 258 and jackylee's digit cuts]

**Floor arithmetic** (pr815.md:40-44): ring 259 + Q 128 + payload 259 + sy 8 + sz 8 + ph + sw = 664. The 676 adds sx 8 and bq/cmpc/f/g. A per-instant union census showed columns 56-100 (all crossing columns) as the only ones above 672 (pr815.md:45-47).

**PR 815 changes in order** (pr815.md:51-81):
1. `S5_NOPARK`: stage-5 payload transitions use in-place quotient bits plus a q-block compensation. Stage 5 drops 675 → 670 lanes; +6.3M T per traversal.
2. `L672_TIER`: two-engine crossing V forms. Tier A is 21 bits on R_common (19 lanes) + sy5/sy6, which are free because 112 ≤ sy ≤ 128 and sy's low lanes hold (sy + 16) mod 128 < 32. Tier B is 24 bits on R_common + Q[121..126). Tier B applies iff the parked band leaves Q[121..) clean, an exact 2D interval predicate on (sy, sz).
3. HR overshoot repair dropped (it costs lanes): λ 2.74 → 3.28.
4. `L672_POOL9`: pool = sz 8 + sw. bq/cmpc/f/g are re-bound per region: sx4..7 outside the middle, sx2..5 in the middle (`mid_alias`), sz0..7 + sx7 in the map with sx held as max − 1 in 7 bits (`map_alias`).
5. `L672_MID8`, `L672_J1Q`: the crossing middle runs on sx0, sx1, sx6, sx7 only, with dirty compact compares and a two-lane decoder.
6. All columns with sy > 98 run crossing sessions. No λ cost (3.279 before and after, 600k inputs).
7. Done shots in columns 97-202 run the map under !done. The clean-helper replay is −54M T per traversal vs the dirty-helper form.

**PR 818** (pr818.md:45-77):
- odinfree's ring cut forced R to borrow Q[125], which became a fourth routed owner. His tiers avoid it: R_common is 18 lanes; tier A adds sy4..6 with offset (sy + 15) mod 128; tier B uses Q[120..126); λ 3.28 → 3.34.
- The V-form frame starts at ring[0].
- S5_NOPARK's sweep frame rotates by sz instead of sz + 1, dl = n − 258.
- Ported odinfree's `ripple_true_carry`, the HT mask granule at margin 1, and `trans_carry_boundary`.
- Ported jackylee's `R9_DIGIT_FUSED`: −18.8M emitted T (−2.2%).

---

## 3. Process and workflow

**Official-equivalent measurement.**
- **PR 500:** env-free `build()`, `apply_tail_nonce`, eval's Fiat-Shamir shot derivation and a 64-shot simulation. λ was measured over 96 nonces (pr500.md:69-70).
- **Later:** an exact replica of `eval_circuit`, named fasteval from PR 653 on.
  - Layout: one SHAKE256 stream, 64 bytes per shot, then 8 bytes for every R/HMR op in every batch, executed or not. Batch b's measurement bytes start at 64·9024 + 8·M·b, where M is the number of R/HMR ops.
  - Runs: one thread squeezes in order, six simulate batches, 20-byte ops (pr624.md:190-198).
  - Validation: reproduced every printed number (averages, totals, failure counts, first-failure text) on 3 random circuits with nested conditions, froghop-799 (63M ops) and frogdrop-776 (639M ops). Then matched the official grade of the 732 entry (416,403,331.484) and the 739 entry (261,923,458.635) "to the digit" (pr626.md:196-199; pr628.md:222, 227-229).
  - Speed: single-thread SHAKE dominates, 5-17 min per build (pr624.md:198; pr626.md:200). The official local run "thrashed in 72 GB… stopped after two hours" (pr626.md:192).
  - Published at github.com/BitWonka/ecdsafail-tools, `fasteval/` (pr653.md:136-137).
- **Memory facts:** the grader holds 56 B/op and the runner has 128 GB, so 1.28-1.78B-op builds are 64-100 GB (pr624.md:186-187; pr660.md:183). `LOWQ_EXACT_STREAM_PATH=<file>` streams ops to disk byte-identically to `write_ops` (pr624.md:187-189). `Simulator::apply_iter` keeps its condition stack per call, so streamed chunks are cut only where the stack is empty (pr624.md:205-206).

**Reproducibility gates.**
- Ops SHA-256 in every later note, with two builds byte-identical "so the Fiat-Shamir shots are fixed by the source" (pr624.md:157-158).
- Clean checkout of `main` + `src/point_add` and an empty environment give the same bytes (pr663.md:246-248; pr815.md:104).
- Design switches are baked as defaults; dev env hooks are inert when unset (pr697.md:153-154).

**Classical failure predictors and nonce handling.**
- Every family has an integer-model predictor that hashes the op stream like `eval_circuit` and checks every shot's two divisions.
- Calibrated on an actual failure: a 778-qubit frogdrop build failed one official shot at nonce 0, and the predictor flagged that same shot (pr551.md:150-152).
- Nonce mechanics: a single X·X pair on a chosen qubit keeps the op count fixed (pr551.md:153). Later a CX pair `CX(c,t)` applied twice gives 699 × 698 choices instead of 699 (pr663.md:286-289).
- He states repeatedly that the nonce choice "does not change the true failure rate; it only picks a shot set" (pr654.md:137-138; pr663.md:289).
- Clean-set yield tracks P(clean) ≈ e^−λ:
  - "at λ ≈ 5 only about 1% of shot sets have no failure" (pr654.md:128-129);
  - λ = 5.2 gives "about one shot set in 180" (pr663.md:285-286);
  - "λ ≈ 7.1 also leaves about 0.6 expected clean nonces among 718 positions", which killed KP = 23 (pr658.md:136-137);
  - at 718 Q only one of 718 positions was clean (pr659.md:191).
- Named tools:
  - `payload_predict_nonce` with `FROGDROP_OPSFILE`, `FROGDROP_SCAN`, `FROGDROP_SCAN0` (split a scan over processes, e.g. 8 processes, pr654.md:160-161), `FROGDROP_CTRLS`, `FROGDROP_SCANALL=1` (pr663.md:313-314);
  - `frogtail_predict_nonce` with `FROGTAIL_SCAN=12` (pr584.md:215);
  - `strip_predict_nonce` with `STRIP_SCAN=32` (pr606.md:182);
  - `frogdrop_predict_nonce` with `FROGDROP_SCAN=24` (pr552.md:103).
- Model vs circuit on the grader's own shots, set-equal: predicted {2235, 6954, 7891} = fasteval-failed {2235, 6954, 7891} (pr815.md:101-102); {5326, 5784, 6144, 8506} (pr818.md:85-86); "matched the predicted set shot for shot" (pr697.md:130-131).

**Hunts** (`#[ignore]` tests):
- `frogdrop_traversal_hunt` (`FROGDROP_BATCHES=256` gives 16,384 random divisions; `FROGDROP_HITS=1` targets inputs that finish while a probe reaches the counter lanes);
- `payload_e2e_hunt` (`FROGDROP_BATCHES=64` gives 4,096 point adds);
- `frogdrop_roundtrip_dbg` (pr624.md:200-203);
- crafted inputs "built to fail" (512 inputs, 448 bad, all model-predicted; pr663.md:280);
- `FROGTAIL_CK=1` per-phase checkpoints (pr584.md:217).

He reports hunt counts against the expected rate: "0 failures in the 16,384-division hunt is the expected outcome (0.65 expected)" (pr653.md:128); 7 bad vs 4.5 expected, P(≥7) ≈ 0.17 (pr654.md:122-123).

**Unit and reference tests.**
- Gate-level traversal against an integer reference model at every slot, forward+inverse on 384 inputs, 64-pair end-to-end (pr547.md:138-140).
- Exhaustive adders for n ≤ 6 (pr552.md:62-64).
- Forced measurement outcomes (all 0, all 1, mixed) that check the exact executed-T count (pr598.md:99-101) [Codex, kept in 602's suite].

**Census tooling.**
- A per-op lane-occupancy replay records, for every op, which qubits are nonzero on any of 2,048 shots. "All 730 lanes are simultaneously nonzero in about 2,400 ops… So no relabelling or parking of existing lanes can reach 729" (pr653.md:144-148).
- Later uses: a park-window census for constant lanes (pr663.md:170-175, 332-334); a per-lane V-form census (pr699.md:67-70); a per-instant union census (pr815.md:45-47); a "lane census at the op level over all 203 columns" confirming the 13-lane claim (pr663.md:119-120).

**Change discipline.**
- Equivalence first: refactor at the old constants and require the same failing inputs (pr656.md:124-127).
- A/B with the change on and off, identical at all 203 column boundaries on two seeds (pr699.md:74-75, 83-85, 105).
- Negative controls: remove the flip or the slot and confirm the targeted replay fails (pr699.md:145-146).
- Monotone ledgers listing emitted T after each stacked cut (pr624.md:107-119; pr602.md:65-70; pr584.md:173-178).
- Peak sweeps before fixing Q (pr602.md:142-143; pr601.md:67, 73-80 [Codex]).

**Honesty conventions.**
- Every error trade is stated with numbers (pr548.md:113-114; pr653.md:116-120: "We state the trade here rather than hide it behind a nonce").
- He publishes errata (pr699.md:129-134).
- Each note marks measured vs modeled values (pr697.md:22-23).
- He labels every low-Q entry "not a frontier score".
- The PR 419 limiting contract (λ ≤ 18, no direct error-for-score trades) is inherited text, copied into every note from 547 on. PR 815 omitted it and PR 818 admits that (pr818.md:106-107).

**Sub-agent usage.**
- PR 500: several Opus sub-agents for research, ports and a fresh-eyes review (pr500.md:18, 81).
- PR 547: a design sub-agent (pr547.md:18).
- PR 602: three sub-agents split by phase (products, walk, inverse walk); the main session merged them (pr602.md:18-19, 206-208).
- PR 606: design study, build, then lever round (pr606.md:207-210).
- PR 624-629: one design/build agent.
- PR 663: design and build agents, with two middles built in parallel (pr663.md:320-322).
- PR 697: three sub-agents split by subsystem (quotient engine, size registers and payload, crossing parks) (pr697.md:21-22, 163-171).
- PR 699: a lane-research sub-agent (pr699.md:165-166).
- PR 815/818: "single agent, no subagents" (pr815.md:18; pr818.md:18).

**Tools he names.**
- fasteval and its GitHub location. The remaining named tools are the in-repo `#[ignore]` predictors and hunts listed above, `refmodel.rs`/`refmodel_double.rs`, generators `frogdrop_sched_gen` (pr551.md:166-167) and `strip_model.rs` (pr606.md:187), and a resource model `research/frogtail_chunked_capacity.py` (pr601.md:125, Codex).
- **`dead-ccx-finder` is not named in any of the 26 notes.** It lives in [BitWonka/ecdsafail-tools](https://github.com/BitWonka/ecdsafail-tools) and is out of scope here.

---

## 4. Dead ends and negative results

**Product line**
- Q×T is "fairly flat" across ping-pong (~1,250-1,300 × 910-925k), Skywalk (1,172 × 945k) and Leapfrog (1,243 × 804k) (pr500.md:28-32, 43).
- A per-position quantile envelope wastes T: union bound 2.6e-2 vs an actual 7e-4 (pr500.md:63).
- The Leapfrog line had only this one PR. By 9 Oct the board was at 971.66M (pr547.md:6). krishparadox's 1,237-qubit Leapfrog is mentioned (pr551.md:173).

**froghop and frogdrop**
- Fixed-boundary slack costs ~110 qubits (pr547.md:54).
- W = 308 fitted on 30k shots failed an official shot; refit on 200k gave 314 (pr547.md:125-126).
- Tightening froghop-double's margins from λ ≈ 0.12 (836 × 17,173,499) to λ ≈ 0.77 bought 7.2% T (pr548.md:113-114).
- Lean bookkeeping costs +9% T (pr550.md:38). The froghop-double floor is ~795 (pr550.md:52).
- frogdrop costs ~11× froghop-double's T to save 23 Q (pr551.md:39-40). The map is ~60% of T (pr551.md:135).
- A one-column identity is impossible (Klein four-group), so a 7-bit counter is needed (pr551.md:123-124).
- A 778-qubit build failed an official shot at nonce 0 (pr551.md:151-152).
- 8-bit sz aliasing: an unguarded decoder matched 288 mod 256 (pr552.md:76-78).
- A borrowed carry-in breaks z = y (pr552.md:67-68).

**frogtail and frogstrip**
- The inverse walk costs ~2,800 T per tick vs ~1,206 forward (pr584.md:61-62, 97, 115). The inverse walks are 51% of T (pr584.md:171).
- At 917 Q the inherited nonce 3 failed one shot after Codex's change (pr598.md:126).
- Peak sweeps: 1,000 Q gives the lowest T, but 933 gives the best product (pr601.md:80, Codex). 917-928 vary only 3.411B-3.384B (pr602.md:142-143).
- Signed-digit traps: subtraction from z = 0 leaves phase garbage without the carry-in; +C·y ends at the non-canonical p (pr602.md:91-95).
- frogstrip: rings +7 lanes each; λ 0.95 → 2.5, ~2.0 of it the gap cap at 20 (pr606.md:51-53, 149-151).

**Payload walk and K/KP**
- 1-bit subsets "would save nothing" (pr624.md:71-72). QSUB = 2 costs +154.7M emitted T vs QSUB = 9 (pr624.md:153), +107.7M after deferral (pr628.md:181).
- Not adopted: bf1897f0's counter-lane loan; the masked bl(Z) probe on small pools (pr628.md:159-165).
- K < 23 collapses (pr654.md:96-98). K = 25 failed one shot at nonce 6 (pr654.md:90).
- Cutting KP shrinks the pool and the layout runs out of first-HT scratch: an assert fired at KP = 29 (pr653.md:147-148; pr656.md:90).
- KP = 24 did not fit the 720 layout (pr656.md:121-122).
- KP = 23 at 718 Q: −0.03% net T and λ 7.1, about 0.6 expected clean nonces, so rejected (pr658.md:136-137; pr659.md:152-153).
- A nonce-48 replica run was interrupted; 301 was used (pr656.md:160-161).

**Scheme G**
- +76.2M T (+30%) over the 713 middle (pr663.md:236).
- A 9-lane reserve without R1 gives crossing λ ≈ 30 (pr663.md:223, 336). A 13-lane reserve gives 1.8 (pr663.md:224, 332).
- "Every first design" of the per-shot form failed on reversibility (pr663.md:329-331).
- Payload zero runs (3-8 lanes, value-dependent positions) are unusable as reserve (pr663.md:333-334).
- Finishing the switch inside the crossing column fails because the column's last ops are uniform (pr663.md:187-190).
- Scheme G buys back only ~0.6 λ vs the two-stage estimate (5.25 vs 5.88) (pr663.md:270-272).
- **682 erratum:** the predictor lacked a switch-tail check, and two "clean" inputs failed at columns 62 and 68. λ 2.51 → 2.545 (2M) / 2.71 (4M). The graded run stands (pr699.md:131-134).
- At ring 263, without the Y-top slot, there were 8 park failures per 4M (pr699.md:91-93).

**672/671**
- Tier A with u + 7 broke, because routed parked bits contaminate u (pr815.md:59-60).
- The exact HR overshoot repair (a map detour) does not fit 672: λ 2.74 → 3.28 accepted (pr815.md:62-63).
- Bugs found (pr815.md:85-92):
  - the D-form gives −1 when sizes are equal (fix: sy = min − 1 first);
  - map probe prefixes contained the probed register's top lane plus a duplicate;
  - J1Q silently skipped the top band's bit 0 parked on the comparator carry cell;
  - the end digit ran with 2 lanes.
- T roughly doubles vs 676: 232.8M emitted per traversal vs 133.4M (pr815.md:108-112).
- odinfree's Q[125] fourth owner forced five parked families; the 675 and 672 levers collide on Q[121..126) (pr815.md:125-127; pr818.md:41-43).
- jackylee's crossing and one-session-column work did not apply to his tree (pr818.md:76-77).
- "Next" for the 664 floor needs one of: a crossing middle on fewer than 4 spare lanes; R lanes not taken from sx; or an overshoot repair that fits (it would bring λ back to ~2.7) (pr815.md:119-123).

---

## 5. Skill candidates

### S1. `ecdsafail-exact-replica-gate`: score with an exact eval replica before submitting
- **Use when** a candidate's ops exceed local memory (more than ~1B ops at 56 B/op), when an official-equivalent number is needed before submitting, or when the official local run thrashes.
- **Steps:**
  1. Build with `LOWQ_EXACT_STREAM_PATH=<file>` and confirm it is byte-identical to `write_ops` (SHA-256).
  2. Run fasteval (BitWonka/ecdsafail-tools `fasteval/`). Shot bytes come from SHAKE256: 64 B/shot, then 8 B per R/HMR op per batch, executed or not, so batch b starts at 64·9024 + 8·M·b. 20-byte ops; 1 squeeze thread plus N simulation threads.
  3. Before trusting it, reproduce a graded build's average, totals and first-failure text to the last digit.
  4. Cut streamed chunks only where the condition stack is empty.
  5. Rebuild from a clean checkout with an empty environment and require the same SHA.
- **Source PRs:** 624, 626, 628, 653-660, 663, 697, 699, 815, 818.

### S2. `ecdsafail-predictor-nonce-scan`: classical predictor, nonce scan and honest λ
- **Use when** model λ is above ~0.5 (any low-Q precision cut), or before choosing a nonce for any stream.
- **Steps:**
  1. Write an integer-model predictor with one failure class per approximation (e.g. gtest, q0, park, envelope, map, v2, switch-tail). Hash the op stream exactly as eval does.
  2. Calibrate: require predicted failing-shot set == replica failing set at some nonce.
  3. Estimate λ over many shot sets (hundreds of nonces, ≥ 1-4M shots), and report it with its standard deviation and per-class breakdown.
  4. Budget supply: expected clean sets ≈ positions × e^−λ. If that is below ~2 (e.g. λ 7.1 at 718 positions gives 0.6), widen the nonce to a CX pair (Q·(Q−1) choices) or reject the cut.
  5. Scan in parallel (`SCAN0`/`SCAN` ranges), take the first clean nonce, and confirm on the replica.
  6. State in the note that nonce choice does not change true λ.
- **Source PRs:** 551, 552, 584, 602, 606, 629, 654, 656, 658, 659, 660, 663, 697, 699, 815, 818.

### S3. `ecdsafail-lane-census`: find the binding instant before cutting qubits
- **Use when** pushing Q down on any line, or when a lane cut asserts "pool too small".
- **Steps:**
  1. Replay the stream on ~512-2,048 shots and record, per op, the union of nonzero lanes.
  2. Find the ops at the peak and the stage that owns them.
  3. If all lanes are simultaneously busy (e.g. 2,400 ops at 730), relabelling and parking cannot help; a register must shrink (precision or layout).
  4. Otherwise census specific windows for lanes that are constant on every active shot, by construction rather than sampling (flags on parking shots, leading ones, always-zero tops), and lend them.
  5. Re-run the census to confirm every stage fits the new pool.
- **Source PRs:** 653, 656, 663, 697, 699, 815.

### S4. `ecdsafail-paired-precision-sweep`: walk a precision knob to its floor
- **Use when** a qubit is tied to a precision constant (estimate heads K/KP, digit widths, quotient bits).
- **Steps:**
  1. Change only the constant(s), keeping derived offsets consistent (e.g. N = 258 + K).
  2. Evaluate every setting on the same paired divisions (e.g. 60 shot sets × 9,024 × 2 = 1,082,880, hashed from one stream).
  3. Tabulate model λ, traversal-hunt failures against the expected count, and an official/replica pass.
  4. Find the knee (≈2× per bit, then collapse) and pick the floor that still leaves clean nonces.
  5. For the second knob, check slack first: KP 30 → 24 was flat.
  6. Disclose λ before and after.
- **Source PRs:** 653, 654, 656, 658, 659, 660.

### S5. `ecdsafail-equivalence-first-refactor`: refactor safely before any cut
- **Use when** re-carving scratch, porting a rival's cut, or adding a per-shot form (R1-like).
- **Steps:**
  1. Implement the refactor at the old constants.
  2. Require identical failing inputs on fixed hunt seeds (16,384 divisions, 4,096 point adds) and the predicted failure count at the old nonce.
  3. A/B the switch on/off with identical state at all column boundaries on two seeds.
  4. Add negative controls: remove the new piece and confirm the targeted replay fails.
  5. Regenerate schedules with a generator that reproduces the old file byte-for-byte under the old rule.
  6. Only then apply the cut. Keep a monotone emitted-T ledger per stacked change.
- **Source PRs:** 624, 628, 656, 663, 699.

### S6. `ecdsafail-executed-T-harvest`: lower average executed T without changing emitted structure
- **Use when** T is the price paid for Q, and blocks contain temporaries or carries cleared by coherent compares.
- **Steps:**
  1. Measured uncompute: X-measure the temporary and run its phase oracle under the classical outcome. Cost becomes half the oracle in expectation (33 → 16 T; a k-lane chunk boundary costs (k − 1)/2). Capture the condition before inner AND measurements reuse the classical bit.
  2. Chunked carry bank on clean lanes below the peak.
  3. Signed-digit Horner so adders lose their quantum control (2 → 1 T per pool lane).
  4. Deferred phases and erasure boxes across mirrored forward/inverse walks. This requires box outputs computed from zero and identical walk state at mirrored positions; assert gate-list hash equality.
  5. Test with forced measurement outcomes (all 0, all 1, mixed) and assert exact executed counts.
- **Source PRs:** 598 and 601 (Codex, as inputs), 602, 606, 624, 628.

### S7. `ecdsafail-peeling-width-envelope`: fit rail/ring width schedules for the product line
- **Use when** per-tick or per-column widths come from quantiles and failures cluster in a few fat walks (union bound ≫ actual).
- **Steps:**
  1. Record ~2M classical walks.
  2. Price T per bit per tick region from the circuit.
  3. Greedy peel: drop the no-park walks, then repeatedly lower the position with the best T saved per sacrificed walk, then take survivor maxima.
  4. Validate on ~1.3M fresh walks.
  5. For sign or idle envelopes, use the per-tick max, a running max over ±k ticks and +2 lanes, then check against more walks.
- **Source PRs:** 500 (also 551, 602, 606).

### S8. `ecdsafail-lend-provable-lanes`: borrow lanes that are provably zero or constant
- **Use when** one more lane at the peak instant is needed (low-Q Pareto, 680-730).
- **Steps:**
  1. List bits that are fixed on every active shot by an identity: always-one leading bits of a size-normalised value (Y's MSB, the head's leading one), always-zero tops, flags constant on parking shots, act on act-free plays.
  2. Prove each by construction, then confirm with a census across all columns.
  3. Around the instant, gather the bit with a swap tree on its size register, flip it to 0, lend it, and restore after.
  4. Store derived quantities instead of registers: a gap instead of two sizes, done status from register state, a counter in a register's known-free top lanes.
  5. Make act-controlled blocks act-free when enter and leave cancel.
- **Source PRs:** 550, 624, 663, 697, 699, 815.

---

## 6. Could not determine (from these 26 files)

- Whether each CLOSED PR was accepted onto the Pareto board, and its rank. The notes call some earlier entries "graded" (pr654.md:50; pr656.md:25; pr663.md:27), but PR state only shows non-promotion on the product board.
- The Pareto board's scoring and dominance rule.
- The source of PR 500's "19.5 social cap" (pr500.md:69), as opposed to PR 419's 18.
- Why PR 815/818 diffs are +205k/−181k lines. Generated tables are likely, but the notes do not say.
- Why 11 headers lack a "claimed score" (584, 602, 606, 653-660, 815, 818).
- The specific `LF_*` flag names; the contents of the Leapfrog envelope and anchor files; the constant f in the barrel fold.
- Code-level detail of ported cuts beyond their names: bulengerk R08-R11, H51 certificate, "b8b" crossing middle, jackylee's 693-699 and 8d916b42 work, nasqret 36378f0.
- Who operated the Codex PRs 598/601 under this account. PR 601 says "our previous Frogtail submission" (pr601.md:22).
- Wall-clock, hardware and cost per build or scan, beyond the figures quoted (6 sim threads, 5-17 min SHAKE, ~6-7 min and 36 GB local eval for frogdrop, a 128 GB runner).
- Whether PR 815's λ definition ("failing walks per 18,048 walks", pr815.md:114-115) equals the earlier "failing shots per 9,024" in all cases (it does when at most one division fails per shot).
- Any physical depth or runtime estimate. Codex says none was made (pr601.md:104).
- Anything about `dead-ccx-finder` or `loop-engine`. Neither appears in the notes.

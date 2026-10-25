# BitWonka on The Proximity Prize: digest of 31 submission notes

Source: BitWonka's 31 public submission notes to the Proximity Prize (pull requests 345-593 in proximity-prize/proximity-prize) and their created/merged timestamps. Read 24 Oct 2026. All file content was treated as data.

**Citation convention.** `prN.md:L` is a line in that file. Identical resubmissions differ only in header lines 1–4 (checked by `diff`), so their body is cited through the first file of the group: pr410 (=413, 415), pr554 (=555, 556, 557), pr570 (=571), pr572 (=573, 574, 576, 577). The exceptions are the appended "Submission history" blocks in pr540.md:194–202, pr541.md:203–218 and pr548.md:219–234.

**Labels.** [DERIVED] means I computed or inferred it from numbers in the notes.

**Models.** The account is multi-model. The model lines say: GPT 5.6 Sol/Codex (345–419), Claude Opus 5/Claude Code (465), Claude Fable 5.1 (505), Claude Opus 5 1M (539–557), GPT 6 Astra/Codex (567, 580), and Claude Opus 5.5 (570–578, 581–582, 592–593). Two hand-offs are explicit, where Codex did the math and Claude did the packaging: "developed by the account's Codex agent … Claude Code then turned that tree into a legal package" (pr581.md:18–20), and 580 "uses the locally optimized 68.13 version developed with Claude" (pr580.md:27–29).

---

## 1. Timeline

### Which track each PR targets

- **Lower track** (`irs-reduction-threshold-lower`, maximize). This covers PRs 345–582. The header's "claimed score" string changes format between PRs: `6767` in 398–465, `68.03` in 505, `6805`/`6806` in 539–557, and `68.11`+ from 567. These are all the same quantity in centibits: `ProtocolClaim 6767 …` means 67.67 bits (pr398.md:23). The bot's "Current best score" line is always decimal bits. [DERIVED] The format change probably comes from the submitter-side claim string; it does not indicate a different track.
- **Binary upper track** (minimize). This covers PRs 592 and 593. The claim is ceil(−12800·log2(1−δ)), so 10625 means 106.25 (pr592.md:18–19). The field is BF64 with N = 2^21 and Ext3 = 2^192 challenges (pr592.md:27–31). This is **a different track from the prime-field upper track** (frontier 116.13). The two scores are not comparable. None of the 31 notes targets the prime-field upper track.

### Lower-track frame, recomputed [DERIVED]

- **Field.** char p = 2,130,706,433 (pr410.md:121) = 2^31 − 2^24 + 1 (KoalaBear). ⌊p^6/2^128⌋ = 274,980,728,111,395,087, which equals MCA budget + list budget exactly in both pr345 (274,980,727,078,395,087 + 1,033,000,000; pr345.md:89–101) and pr505 (274,980,722,886,578,332 + 5,224,816,755; pr505.md:34–35). So |F| = p^6.
- **Code.** Domain N = 2^18 = 262,144, degree bound w = 131,071, so the rate is 1/2.
- **Radius.** The radius always sits at the top of its error bucket: numerator = e·(den/2^18) + den/2^18 − 1. I verified this for 345 (den 2^25), 554 (pr554.md:60, "128 * 80811 + 127") and 581 (den 2^30, 80899·4096 + 4095 = 331,366,399).
- **Score.** Score = ⌊−12800·log2(1−r)⌋. Recomputed values: 6742.045 (345), 6815.056 (582), and 6812.0001 (570), so 570's radius bucket barely clears its score.
- **Errors per centibit.** At about 68.1 bits, one centibit costs 10 errors: e = 80869/80879/80889/80899 gives 68.12/68.13/68.14/68.15.
- **Radius denominator.** It moves from 2^25 to 2^30 at PR 567 (pr567.md:24). The finer grid lets the radius sit closer to the bucket top.

### Table

Δ is measured against BitWonka's own previous *claimed* score. "Prior best" is the bot's frontier line at submission time. Ownership tags: **his** means his agent's math; **repack** means someone else's math, repackaged; **paper** means a construction from a cited paper.

| PR | created (UTC) | state | track | claimed | prior best | model | one-line mechanism | Δ vs his prev |
|---|---|---|---|---|---|---|---|---|
| 345 | 08-30 19:41 | MERGED (28 min) | lower | 67.42 | 67.41 | GPT 5.6 Sol/Codex | **his**: square-witness collar (F² divides a kernel witness) gives slope-10..13 factor caps; exact one-high-factor aggregation | first |
| 347 | 08-30 21:14 | MERGED | lower | 67.43 | 67.42 | same | **his**: 7-kernel targeted packet; disjunctive middle-vs-total square trade-offs | +0.01 |
| 398 | 09-01 01:15 | MERGED (44 min) | lower | 67.67 | 67.66 | same | **his** (built on someone's 67.64 `d375771`): quotient/cofactor dichotomy F·Q vs F²·C (2nd derivative); dual source m=93/126; exhaustive 17×78×154 grid with 4 routes | +0.24 (others filled 67.44–67.66) |
| 410, 413, 415 | 09-01 04:13 / 05:07 / 05:56 | CLOSED ×3 | lower | 67.68 | 67.67 | same | **his**: four-stage factor switch; quartic detector d_R⁴(F⁴Q)=24(d_RF)⁴Q; 840 hard cells | +0.01, never promoted |
| 419 | 09-01 08:51 | CLOSED | lower | 67.73 | 67.67 (note says the base is a public 67.72) | same | **repack+retune** of Jieyi's independent-total-cap architecture: C=(163, 36564, 48), powers 2–5; targeted HardUnit→width-2 refinement | +0.05 |
| 465 | 09-02 05:55 | MERGED (45 min) | lower | 67.82 | 67.80 | Claude Opus 5 | **his**: closed-form local rank (Gauss sums) unlocks C m=400, s=120; closed-form channelCount; depth-14 generic iterated power avoidance | +0.09 |
| 505 | 09-04 22:08 | MERGED (74 min) | lower | 68.03 | 68.02 | Claude Fable 5.1 | **his** (on the promoted 6802 tree): packed locator tree plus a 5th source phase `split1200` | +0.21 |
| 539, 540, 541, 548 | 09-11 03:08–10:59 | CLOSED ×4 | lower | 68.05 | 68.04 | Claude Opus 5 1M | **repack** of 0xLucqs's boundary-tail valuation (moving multiplier 131076→65539); his additions: zero-table closed form, algebraic superadditivity, Elab.async off | +0.02 |
| 554–557 | 09-11 13:36–14:47 | CLOSED ×4 | lower | 68.06 | 68.04 | same | **repack** of 0xLucqs's strict-check discrete convexity; his additions: carrier closed form, `interval_cases`+bullets, shard merge | +0.01 |
| 567 | 09-14 23:49 | MERGED (3h19m) | lower | 68.11 | 68.10 | GPT 6 Astra/Codex | **his**: source-sensitive moving-fiber bound; 3 directions on a common component family; 8-slope packing; 2^30 denominator | +0.05 |
| 570, 571 | 09-23 05:16 / 05:40 | CLOSED ×2 | lower | 68.12 | 68.11 | Claude Opus 5.5 | **his**: H-free first cut τ=Y^(w+1) with cusp law 3θ ≤ 4T + 2·ord H | +0.01 |
| 572–576, 577 | 09-23 08:12–12:11 (about hourly) | CLOSED ×4, then 577 MERGED (3h20m) | lower | 68.12 | 68.11 | same | same math plus 1.2 MB reachability pruning; 577 is an identical resubmission | 0 |
| 578 | 09-23 15:49 | MERGED (3h38m) | lower | 68.13 | 68.12 | same | **his**: signed derivation law at infinity; one fold curve for the whole derivative chain; per-cell pair charge | +0.01 |
| 580 | 09-29 17:33 | MERGED (2h35m) | lower | 68.14 | 68.13 | GPT 6 Astra/Codex | **his**: 74 relative-interpolation offers plus 5 packet bands for the hard (R,B) families; Bool direct-kernel checkers | +0.01 |
| 581 | 09-30 23:48 | CLOSED (ran past 4 h) | lower | 68.15 | 68.14 | Opus 5.5 packaging Codex math | **his (Codex)**: exact-removal phase, packet portfolio, one-heavy packing; 689-file package | +0.01 |
| 582 | 10-01 13:34 | MERGED (3h40m) | lower | 68.15 | 68.14 | same | same math repackaged: floors, fixed-width packing encoding, 450→153 modules | 0 |
| 592 | 10-20 00:52 | MERGED (16 min) | binary upper | 106.25 | 114.11 | Claude Opus 5.5 | **paper+his**: DKTZ pole pair + char-2 flat-locator gap; 2^71 unions of four varying-direction flats + reserved subspace W | −7.86 (first on this track) |
| 593 | 10-20 20:45 | MERGED (20 min) | binary upper | 106.24 | 106.25 | same | **his**: pole pair on labels of a 64-point fibration + 63-point core + 2^65.7 non-tree label family | −0.01 |

The merge latencies come from `prs.json` (createdAt to mergedAt) and are a proxy for verifier wall time [DERIVED]. Lower-track checks grew from about 30 min (Aug) to 3.3–3.7 h (late Sep and Oct). Binary-upper checks take minutes.

---

## 2. Constructions and proof strategies

### 2.0 Lower-track proof skeleton (shared by every lower PR)

- **Target.** Certify a radius at which the "MCA-plus-list extractor error" is at most 2^-128. Then prove the 128-fold spot-check error is at most 2^-score (pr345.md:23).
- **Two arms.**
  - A scalar list arm: one interpolation kernel, and a "moment-separation bound used to reduce sixteen interleaved rows to the scalar list statement" (pr347.md:114).
  - An affine-line alignment / MCA arm, split into fixed-gcd and residual-gcd cells (pr345.md:25).
- **Interpolation kernels.** Each kernel has parameters (m multiplicity, L total cap, s slope cap) and weighted cutoff D = m·a. Existence of a nonzero interpolant is the nullity condition: coefficientCount − N·localRankBound > 0 (pr505.md:50).
- **Factor flags.** Irreducible factors of the selected gcd carry flag degrees (slope, middle/"YS", total).
- **Ledger.** Seeds (bad challenges) per factor are counted by resultant/intersection bounds. The MCA ledger is fixed regular + fixed singular + residual regular + residual singular (+1 separator), which must be strictly below the MCA budget (pr345.md:79–95).
- **Score conversion.** Exact integer inequalities only, for example `2^43·1000000^100 ≤ 1347234^100` (pr347.md:126–128), `2^82·47^100 ≤ 83^100` (pr465.md:60–61), and `2^3·10000^100 ≤ 10211^100` (pr505.md:78).

### 2.1 Square-witness collar caps (345, 347; GPT 5.6 Sol)

- **Argument.** Let F be an irreducible common factor of a constraint kernel. Fix a "retained-coordinate collar whose dimension is strictly below the kernel nullity". Linear algebra then gives a nonzero kernel element whose quotient by F lies in a low-prefix space. "The locator-restored derivative identity then forces the selected irreducible factor to divide that quotient", so F² divides the witness (pr345.md:29). Weighted-degree additivity then turns the global support bound into a per-factor cap with a factor-of-2 gain (pr345.md:31).
- **Caps.**
  - 345: slope 10..13 → middle ≤ 56/52/48/44, total ≤ 1414/1414/1414/1413 (pr345.md:40–43).
  - 347 adds disjunctive trade-offs, e.g. "at slope 10, middle degree above 53 forces total degree at most 1374" (pr347.md:47–50).
- **Aggregation.** The total slope flag is ≤ 13, so at most one factor has slope ≥ 10. That factor is split off and handled with slope-specific paired inequalities; slope 13 is terminal. A "diagonal low-rate inequality" handles the all-low case. The result is a fixed-regular cap of 272,527,456,851,746,043 (pr345.md:49–55).
- **Kernels.** 345 uses 5 profiles, e.g. primary A m=81 D=14,739,003 and B witness m=87 cap 1451 (pr345.md:67–73). 347 uses 7, with all auxiliary A-side kernels embedded into one primary coefficient space so that "a common gcd is selected" which divides everything (pr347.md:60–72).
- **Lean.** Modules: LocatorSquareWitness, LocatorIrreducibleCaps, LocatorSelectedCaps, LocatorFactorAggregate, LocatorFixedBridge, LocatorArithmetic (exact nullities recorded as identities). The root is flat. Size: 4,188,138 bytes against a 4,194,304-byte limit (6,166 B headroom; pr345.md:137), then 4,193,354 bytes (950 B headroom; pr347.md:160). The build is 4,432 modules (pr347.md:152).

### 2.2 Factor-switch ladder: dual source → quartic → powers 2–5 → generic depth 14 (398, 410, 419, 465)

- **398, dual-source quotient/cofactor dichotomy.**
  - For a source interpolant divisible by F, take a low quotient. If it is coprime to F, a "resultant and first-derivative intersection bound controls the seed set". Otherwise divide again: the second derivative of F²·C identifies C at an F-regular specialization. This needs odd characteristic (factor 2 ≠ 0), and a "strict three-way support inequality prevents an unaccounted third copy" (pr398.md:49–59).
  - The 67.67 lever lets each cell choose either of two already-selected source families: m=93 (s=27, D=16,899,681) or m=126 (s=39, D=22,896,342). "Neither family is uniformly best" (pr398.md:61–75).
  - Nullity is affine in L and proved for all L ≥ 2600 by successor recurrences, e.g. `source 126: nullity(L) = 370614480·L − 884603972630` (pr398.md:81–87).
  - The exhaustive grid is `Fin 17 × Fin 78 × Fin 154` (slope, YS, width-16 total bins). Each cell is covered by one of four routes: rate contradiction, ordinary + complement, source-93, source-126 (pr398.md:138–153).
  - Ledger slack is exactly 1 (pr398.md:134).
- **410, four-stage switch** (`exists_first_or_second_or_third_not_dvd_or_fourth_low`, pr410.md:80). The outcomes are F·Q1, F²·Q2, F³·Q3, F⁴·Q4.
  - The terminal detector is `d_R^4(F^4 Q) = 24·(d_R F)^4·Q` at F=0, using (24:K) ≠ 0 (pr410.md:112–123).
  - The contact capacity is exact: `22895082 − 4·50637 = (126−4)·181707 + 4·(131071−1)` (pr410.md:128–132).
  - Source length is chosen cellwise as `4·tlo + 30000` (pr410.md:149).
  - Census on `Fin 17×Fin 79×Fin 160`: 27,131 invalid, 100,173 rate, 40,211 ordinary, 46,525 source, and 840 hard cells, all closed by the quartic route (pr410.md:156–166).
  - Closed 3×; no reason is given (see §6).
- **419, retune of Jieyi's 67.72 total-cap architecture.**
  - C goes to m=163, s=48, nullity 26,869,512,347,846. The routes use powers 2–5 and "No sixth derivative route is required".
  - Singleton-profile coverage: ordinary 1,740,424 / A 153,032 / aux 837,751 / C² 33,711 / C³ 587,244 / C⁴ 309,994 / C⁵ 51,925 / uncovered 0 (pr419.md:96–107).
  - The engineering fix is a `HardUnit` (a width-8 unit whose ordinary rate fails), refined into four width-2 `PointCell` children. The receipt is the disjunction "unit ordinary-fits OR all four valid width-two children ordinary-fit" (pr419.md:123–131).
- **465, generic depth.**
  - `LocatorIteratedPowerAvoidance` replaces the hand-written `sourceC_count_1,_2,…` with one operator `pderivRIter n` and one Leibniz split: `pderivRIter n (F^(n+m)·Q) = descFactorial (n+m) n·(F^m·(∂F)^n·Q) + F^(m+1)·S`. Nat.factorial j ≠ 0 for j ≤ 14 in this characteristic.
  - `routeDepth` is a bounded search with cap 14, and `routeDepth_spec` extracts exactly what the consumer needs. "This cell requires the full depth 14" (pr465.md:122–151).

### 2.3 Removing kernel-evaluation walls with closed forms (398, 465, 505)

This is his most reusable lower-track lever.

- **Small box (398).** The weighted cap is 50647 < 131070, so only the (0,0) monomial survives. Proving `coefficientCount 50647 131071 L s = (L+1)·50647` once is "both mathematically sharper and substantially easier for the kernel". Plain `decide` then suffices, with no `native_decide` (pr398.md:91–102).
- **LocatorRankClosed (465).**
  - The problem: localRankBound costs about m²·s/2 kernel reductions. At m=340, `decide` "was killed after seven minutes having consumed over 100 GB". So m=270 was the practical ceiling and the region was "uncomputable", not unexplored (pr465.md:65–74).
  - The fix: when M+s ≤ L the inner double sum is a pair of Gauss sums. The identity is "carried doubled" to stay in ℕ: `2·blockInputCount M L s + (s+1)·(M(M+1)) + (M+1)·(s(s+1)) = 2·((M+1)·((s+1)·(L+1)))`. This gives `localRankBound_eq_fast`, an O(m) sum, and the C-kernel rank now evaluates in 4.8 s (pr465.md:76–90).
  - The point: a **computational** wall, not a mathematical one, was what blocked score. m=400, s=120 then closes cell 80575 (pr465.md:18–21, 65).
- **LocatorChannelClosed (465).** In high-slope rows about 87% of coarse boxes fall through to the route search, and each stage loops `channelCount`. The fix:
  - Reflect the index y → YS−y and split at min S YS into a diagonal piece and a constant-width tail.
  - Carry the identity ×6 so that "each induction case closes by `ring`".
  - Keep the loop as a fallback so the definition stays total, with `stageBand_eq` proving the two agree.
  - Result: the heaviest row went from 6+ min / 9 GB to 22 s (pr465.md:94–114).
- **Census-driven file layout (465).** Of about 13,600 coarse boxes about 190 are hard, and all 162 hard fine cells sit in rows 5–9. Those rows are tiled by fixed `cy` and the rest get one file each: 68 files instead of 164 (pr465.md:116–120).
- **505, chunked ranks.** `localRankBound` is split into 64-row `decide` chunks combined with `Finset.sum_range_add`. coefficientCount uses the one-residue closed form. The 7938 source needs 125 chunks. Rank rows do not depend on agreement, so they are reused across radii (pr505.md:64).

### 2.4 Packed locator tree with a fifth phase (505; Fable 5.1)

- **Change.** The 6802 tree is re-parameterised, and "four phases do not close at this profile (about −0.3%)", so a `split1200` source (m=1200, L=82,100, s=370) is inserted at phase index 3. That way `split390` stays last and the final-bound machinery keeps its shape (pr505.md:54–62).
- **Ledger.** Narrow max 269.09e15, joint max 273.30e15, margin 0.585% (pr505.md:30–37).
- **Potential.** `initialAPotential = ⟨6028951284, 5462225136421, 25579200875807⟩` is a coefficientwise majorant obtained by bounding three `max` atoms, proved by a "single `nlinarith`" (pr505.md:70–72).
- **Receipts.** 3,509 (R,V) rows; a carrier-DP envelope with ≤ 2 affine segments; 5 thresholds per row; prefixes monotone in R and V; and "24 670 affine witness runs … one `decide +kernel` per row". The binding cell is (15,55,6524) (pr505.md:84–91).
- **Layout for concurrency.** `PackedLocatorTail → Tail1 → Tail2 → Tail3 → Solution`, with receipts in RunsA–D importing Tail1 and checks A–B importing Tail2, "so lake can build them concurrently". That section takes 11 min at 4 jobs × about 5 GB (pr505.md:95).

### 2.5 0xLucqs's boundary tail, plus his closed-form tables (539–557; repackaging)

- **The 68.05 math is 0xLucqs's** (pr539.md:22–27). With H = F_R, G = −F_X − R·F_Y, J = H_R and D = H(∂_X + R∂_Y) + G∂_R:
  - The derivative numerators satisfy N₂ = G and N_{n+1} = H·D(N_n) − (2n−3)·N_n·D(H).
  - At places where G/H has a pole this gives ord(H) − ord(G) ≤ 2·ord(J).
  - The moving multiplier drops from 131076 to 65539 (pr539.md:33–55).
  - **68.06** adds 0xLucqs's strict-check discrete convexity: `curvatureAll` is proved once, and then each row needs only two endpoints (pr554.md:64–76).
- **His zero-table closed form (539).**
  - `zero R V` (3,735 integers up to 2^56) is "*exactly* a quadratic in V" beyond a row threshold V0 R ≤ 6. It is written in the falling-factorial basis, `qa R·(V(V−1)) + qb R·V + qc R`, so that all coefficients stay in ℕ. qa, qb and qc are themselves linear/quadratic/cubic in R for R ≥ 3 (pr539.md:62–89).
  - Superadditivity becomes a theorem through `(c+d)(c+d−1) = c(c−1) + d(d−1) + 2cd`, which reduces it to monotonicity facts over 435 (a,b) pairs. That discharges 91.8% of 3.13M splits (pr539.md:96–111).
  - `zeroAt_of_algebra` runs in 7.2 s / 3.5 GB and replaces the whole enumeration (pr539.md:113–127).
  - Row block time went from 3,593 s to 1,844 s (pr539.md:139–148).
- **Carrier closed form (554).** All 150 carrier columns are quadratic in V from V=2 (falling factorial centred at 2), exact on 18,375/18,375 entries. BaseChecked went from 44.2 s to 4.3 s mean (pr554.md:85–105).
- **`first` is not free (554).** Measured on the full module:

  | variant | wall time |
  |---|---|
  | `interval_cases j <;> first \| …` | 72.0 s |
  | one batched decide | 57.8 s |
  | `interval_cases` + positional bullets | 43.9 s |

  He verified that "every one lists its alternatives sequentially" before the mechanical rewrite of 3,947 blocks. The threshold block went from 2,125 s to 803 s (pr554.md:141–202).
- **Shard merge.** 442 → 229 files, 14.20 → 13.66 MiB (pr554.md:204–216).

### 2.6 Moving fibre → H-free first cut → infinity law, fold curve, pair cell (567, 570/577, 578)

- **567 (GPT 6 Astra).**
  - The consumer cost is `Σ_C (multiplicity(C)·normalCost(C) + 65539·movingCost(C))`. "Proving or charging a multiplicity-weighted moving sum would ask for more than this consumer needs" (pr567.md:47–54).
  - The new moving-fibre estimate goes from source support + helper divisibilities to high-order vanishing on a pure slice, then to a pole bound, then to a finite zero count (pr567.md:56–62).
  - The three projection directions use different interpolants on "one common native component family … a coordinatewise combination, not a minimum of three unrelated whole surface bounds" (pr567.md:76–90).
  - Kernels: A (115, 274277, 159, 35), B (134, 18992, 185, 40), T (226, 9281, 312, 70), plus 27 interpolants in 16 groups (pr567.md:109–119).
  - Packing uses 8 affine slopes `[0,4,10,20,40,80,160,320]·10^12` with kernel-checked Bellman tables. Taking the best only after separate phase recurrences "would be a different and weaker operation" (pr567.md:135–145).
  - The replay covers 45.66M states, max at (35,124,9090), margin 2.88e14 (pr567.md:154–158).
- **570/572/577 H-free first cut (Opus 5.5).**
  - The first Taylor tail is counted through the uncleared τ = Y^(w+1) = baseNumerator(w−1)/H^(2w−1). Principal divisors have degree 0, so "the count is at most the total pole mass of τ, and H itself no longer appears in the charge" (pr570.md:44–53).
  - Per-place pieces:
    - `pole(Df) ≤ pole(f) + θ`, restricted to valuations of L0 ("slice descent") because D does not extend to the slice curve over its algebraically closed constant field.
    - θ ≤ T + n₁ (affine places) and θ ≤ T at infinity.
    - Dichotomy: n₁ = 1 (smooth/nodal) or 3n₁ ≤ 2·ord H (cusp).
    - Per-place law: 3θ ≤ 4T + 2·ord H.
  - Per-slice charge: `(w+1)·[(4/3)CV + (2/3)Z_H] + C0`, "sharp at the ordinary cusp" (pr570.md:55–75).
  - Integral closure of k[s] is finite and Dedekind because [L0 : k(s)] is far below the characteristic (pr570.md:77–84).
  - Four new single-source groups give 31 interpolants in 20 groups. The replay max is 0.97737 of the allowance (pr570.md:97–128).
  - 572 adds declaration pruning from `candidate` (about 1.2 MB, keeping local instances), shrinking 15,856,691 to 14,655,327 bytes (pr572.md:138–140, 153; pr570.md:150).
- **578, three bounds that recover a 6% overshoot.** Moving agreement 181,275 → 181,265 put the replay at "1.0604 of the allowance" (pr578.md:32–33).
  - (1) `infinity_theta_signed`: θ ≤ max(s, pσ − P). It passes a signed integer where `max(0, Q−2P)` was passed before. Laws by direction: 3θ ≤ 4T−3t−5P, 4T−5P, 4T−2P−3t. This gives −4% at the binding row (12,56) (pr578.md:35–69).
  - (2) Fold curve: seeds with F = ∂_R F = 0 are counted once on components of V(g, ∂_R F) instead of once per stage. `|foldSeeds F|·gap ≤ leftRegularNumerator(...) + gap·y·t·(6d−4)`. The chain charge falls from 2.17% to 0.12% of the allowance (pr578.md:71–96).
  - (3) Per-cell pair charge on complement boxes `(185−y, 40−r, 27313−t)` and `(312−y, 70−r, 10172−t)`, worth 0.42% at peak (pr578.md:98–113).
  - The A slope must move from 35 to 36 because "Slope 35 has no positive nullity for any A below agreement 181,275", which adds row 36 to every table (pr578.md:130–132).
  - The final margin is 0.54% (pr578.md:138–143).

### 2.7 Offer menus, exact removal and floors (580, 581/582)

- **580.** Bounds become a "menu": 74 proved relative-interpolation offers, each giving (slope, middle, T-interval, count). There are also five packet bands for (R,B) ∈ {(12,55),(12,56),(12,57),(13,53),(13,54)}, each with seed count < 2.7e17. The ledger chooses the new bound only where the actual factor lies in its proved range (pr580.md:41–68).
  - Concern addressed: "an improvement at a few expensive ranges is useful only after it is connected to the actual factors" (pr580.md:43–45). The consumers take ordinary factor data and "the caller does not supply the desired count" (pr580.md:70–76).
  - Margin is 0.10% over 61.68M states (pr580.md:86–89).
- **581/582 (Codex math, Claude packaging).**
  - Retune at agreement 181,245. "39,759 of the old relative rectangles fail". The control replay of 68.14 reproduces exactly first (pr582.md:34–45).
  - 190 relative certificates over 154,851 rectangles. The audit "found a real consumer mismatch", where endpoint-only checks had missed 7 bad rectangles (pr582.md:49–53).
  - 31 packet windows for 13 hard families (pr582.md:54–58).
  - Four-retention auxiliary (87,38,17,119,1430,3,4): it cannot be divisible by J² when 38 < 2·slope(J) (pr582.md:66–75).
  - One-heavy packing chooses the light slope *after* the heavy component's shape is known: `max_{q,u} min_λ [λZ + L_λ(R−q,V−u) + max_x (C(q,u,x) − λx)]`. That saves 6.07e15, whereas "moving the minimum outside saves only 7 rounding units" (pr582.md:102–110).
  - **Exact-removal phase (decisive):** charge `previous_count(U) + helperCost(ΣR(A\U), ΣY(A\U), ΣT(A\U))` maximised over terminal subsets U, instead of a full-box affine potential (pr582.md:111–126).
  - Matched experiment: with exact removal disabled the margin is −5.41e14; enabled it is +6.97e13 (0.025%) (pr582.md:132–137).
  - **Floors:** prove intermediate bounds "only as tightly as the ledger needs" (≥273e15 / ≥270e15 / ≥274.9e15 on selected rows). Hard rule pieces drop from 24,143 to 592, and the rule-row build from 16,786 s to 2,431 s. The shipped margin is 1.95e13 (pr582.md:148–156, 175).

### 2.8 Binary upper 106.25 (PR 592): DKTZ pole pair plus the char-2 flat gap. Not a fibration.

- **Setting.**
  - D = F2-span of z⁰..z²⁰ in BF64, so N = 2^21, and XOR of indices equals field addition. D is a 21-dim F2-space.
  - The row code is RS of dimension K = 2^20 over Ext3 = BF64[y]/(y³+y+1), with |Ext3| = 2^192.
  - A violation needs a winning set of more than 2^64 challenges (> 2^-128 of them) with no correlated agreement (pr592.md:18–31).
- **Common-top principle** (DKTZ, ECCC TR26-237, Lemma 6.1).
  - Take sets S of size T > K whose locators share every coefficient above degree K: L_S = R + C_S with deg C_S ≤ K.
  - Take a pole β ∉ D and the pair f2 = 1/(x−β), f1 = R(x)/(x−β).
  - On S, R = −C_S, so f1 + γ_S·f2 = −q_S(x) with γ_S = C_S(β) and q_S = (C_S − C_S(β))/(X−β) of degree < K. Each S therefore yields a winning challenge at agreement T.
  - f2 is far: c(X)(X−β) − 1 has degree ≤ K and would have > K roots, but it equals −1 at β. So there is no correlated agreement at any δ < 1/2 (pr592.md:33–53).
  - "A generic family pays 64 bits for every shared coefficient; that is PrescribedTop, at 122.33" (pr592.md:55–56). I recomputed −128·log2(1 − 1015833/N) = 122.32 → 122.33.
- **The char-2 gap of flat locators.**
  - Subspace polynomials P₀ = X, P_{k+1} = P_k(P_k − P_k(u_k)) are additive (the cross term 2P_k(a)P_k(b) vanishes), vanish on the span, and satisfy P_k = X^(2^k) + h_k with deg h_k ≤ 2^(k−1). The induction uses that squaring is additive in characteristic 2.
  - An affine flat b + span gets P_k − P_k(b) with the same gap. Products keep the gap: (X^a + deg ≤ a−w)(X^b + deg ≤ b−w) = X^(a+b) + deg ≤ a+b−w.
  - So any disjoint union A of four flats of size 2^18 satisfies L_A = X^(2^20) + G_A with deg G_A ≤ 2^20 − 2^17, **"independent of the flats' directions"** (pr592.md:58–80).
- **Reserved subspace W.** W is the first 2^17 words. For A disjoint from W, L_{W∪A} = L_W·X^(2^20) + L_W·G_A. The first term R is the same for every A. deg C_A ≤ 2^17 + 2^20 − 2^17 = K, so T = 2^17 + 2^20 = 9N/16 and the unsafe index is 7N/16 = 917,504. "W sits inside every agreement set but costs nothing: its whole locator is absorbed into the shared top R, and the degree gap supplied by the flats (w = 2^17) exactly pays for deg L_W" (pr592.md:82–94).
- **Family: 2^71 graphs of g = G(y,t,b).** Index = y + 2^18(g + 2t + 4b).
  - b=0, t=0: g = 1 (fixed flat).
  - b=0, t=1: g = l(y) + c.
  - b=1: two flats {t = m(y)+e, g = (l0 + eD)(y)} for e = 0, 1, whose directions vary with l0, D, m.
  - Parameter count: 2^18·2·2^18·2^17·2^17 = 2^71.
  - Injectivity is shown by explicit point reads, e.g. D_i = G(2^i,1,1) + G(2^i,0,1), and m_i via a second difference using D_0 = 1, m_0 = 0. The normalisation kills the symmetry (m,l0) → (m+D, l0+D) (pr592.md:97–121).
- **Generic pole.** Select 2^64+1 members. Bad poles number at most 2^21 + (2^64+1)·2^64·2^20 < 2^192, so some β separates all the C_A(β) (pr592.md:128–137).
- **Bands.** The pole family covers [7/16, 1/2). The existing PrescribedTop covers [1015833/N, minRelDist). FibrePencil, FibreWindow and LabelKey are deleted. The score check is the Nat inequality 2^258175 ≤ 1179648^12800 (pr592.md:139–146; I recomputed ceil = 10625).
- **Lean.** Modules: FlatPoly (recursion, additivity, gap, gap under products, nodeN as a bit-sum), PoleFamily, PolePencil, and Solution (splits at 1/2). "An irreducible X^n wrapper, Xp: a closed X^(2^20) otherwise overflows unification". "The only decide is score_nat. A clean build takes seconds" (pr592.md:148–166). The diff is +1077 lines over 9 files.
- **How it differs from every prior binary-upper certificate.** "Every earlier certificate on this track takes its list members as unions of cosets of one fixed kernel. Here the members are unions of affine flats whose directions vary from member to member" (pr592.md:22–23).

### 2.9 Binary upper 106.24 (PR 593): back to a fibration, on labels, with a non-tree family

- **Why +63.** "The next centibit needs 62 more agreement points". He gets 63 "by running the pole pair one level down, on the labels of a 64-point fibration" (pr593.md:22–28).
- **Fibration and labels.**
  - U = span(z⁰..z⁵), |U| = 64. Y = L_U has degree 64, is additive, and is constant on cosets 64h + U.
  - Labels form V = F2^11 × F2^4 (2^15 labels).
  - The core is the 63 words 1..63 (the label-0 coset minus 0), with locator R of degree 63.
- **Pencil.** f2 = R(x)/(Y(x)−α), f1 = R(x)·R'(Y(x))/(Y(x)−α).
  - On the core both words vanish, and so does every codeword of the form R(x)Q(Y(x)).
  - On the fibres over S, f1 + γf2 = −R(x)·Q_S(Y(x)), which has degree 63 + 64(2^14−1) = 2^20−1 < K.
  - Agreement = 63 + 64·9·2^11 = 9N/16 + 63 = 1,179,711.
  - Far: c·(Y−α) = R is impossible by degree (pr593.md:30–56).
- **Shared top for free.** S = (odd k cosets of W0 = {z=0}) ∪ (affine flats of dim ≥ 12 totalling 9·2^11). Then V_S = L_W^k·Y^(18432−2048k) + (deg ≤ 2^14), and with k = 3 the certificate uses R' = L_W³·Y^12288 (pr593.md:63–72).
  - [DERIVED] Why the top is configuration-independent: the second coset-polynomial term (Σc_q)·L_W^(k−1)·Y^(18432−2048k) has degree 18432 − 2048 = 2^14 for every k, so only the leading term is shared. Why k must be odd: the flats have power-of-two sizes ≥ 2^12, so their total (9−k)·2^11 must be a multiple of 2^12, which forces 9−k even. With k = 3, the second term is (Σc_q)·L_W²·Y^12288 at degree 2^14.
- **Members.**
  - Q = P \ {v3}: three reserved z-values, where P is an affine 2-plane of F2^4 missing 0.
  - H_t = F2^4 \ (P ∪ P'_t) for the other three translates. F_t = {(y,z): z ∈ H_t, r·y = ρ_t(z), m_t·y = ν_t(z)}, a 12-flat.
  - On H_s ∩ H_t the flats take opposite r-halves (ρ_s ≠ ρ_t), so |S| = 3·2048 + 3·4096 = 18432.
  - "These sets are not height-3 trees: no single root hyperplane splits the three flats" (pr593.md:74–91).
- **Count.** 420·32·2047·(1023·1022·1021)·8³·4 = 6.01e19 = 2^65.705 (I recomputed 65.705). TR26-237's height-3 trees give only M₃(15) = 2^62.7 < 2^64 in a 15-dim label space (pr593.md:26–28, 93–96).
- **Injectivity.**
  - An exhaustive census at y-width 3 and 4 found the parameter-to-set map injective (38.7M of 38.7M distinct at w=4; pr593.md:98–99). The census is used as a falsification check before the Lean proof.
  - The Lean `LabelDecode` proof uses point reads at y ∈ {0, e_i, e_i+e_j}. The fibre polynomial `(R+A+1)(M_s+B+1) + (R+A)(M_t+C+1)` has second difference r ∧ (m_s+m_t). A wedge determines its 2-dim span via `B(i,j)u_k = B(k,i)u_j + B(k,j)u_i`. Two spans meet only in r, which recovers r, then the m_t, ρ and ν. Canonical slopes make the parameters unique (pr593.md:101–120).
- **Lean.**
  - Modules: LabelSpace; LabelTable (420 rows in 7 chunks; shapes by `decide`, sortedness by a linear chain check); LabelFamily (flats as kernel cosets via Mathlib finrank/basis); LabelDecode ("all ZMod 2 ring identities on point reads, plus the wedge lemma"); CorePencil; Solution.
  - PrescribedTop fix: its "two pairing bounds on the products over range 32743 are now proved for symbolic A and k and instantiated afterwards. The closed-numeral proofs made the kernel replay (`leanchecker`) evaluate parts of a 650k-bit product, and cost 14 GiB". The replay now runs at the 3.4 GiB baseline.
  - Clean build about 2 min; 4-thread leanchecker peak about 16 GiB (pr593.md:122–139).

### 2.10 Verifier, caps and policy as observed in the notes (chronological)

| when | cap / behaviour | source |
|---|---|---|
| 30 Aug | total raw Lean ≤ 4,194,304 bytes; flat root; imports only `Benchmark.TargetLower` + own root | pr345.md:131–137 |
| 1 Sep | per-process 4096 MiB kill policy assumed locally; "no individual file exceeds 4 MiB" (total about 4.20 MB) | pr398.md:160–163, 207–209 |
| 1 Sep | "recent verifier failures were reported as RAM-limit failures"; 4 GiB `taskpolicy` test | pr419.md:171 |
| 11 Sep | 1,000 files / 8 MiB per file / 16 MiB total; 4 vCPU; 24 GiB aggregate; "4 hours" documented | pr539.md:153–160; pr541.md:212–213 |
| 11 Sep | `Part/` subdirectory refused at fetch (AGENTS.md rule 2) although Lake builds it | pr540.md:194–201 |
| 11 Sep | runs cancelled at about 3h00m, so he plans "against 3h, not 4h"; `verification_retry_exhausted` is an infra failure | pr548.md:219–229; pr554.md:36–55 |
| 14 Sep | live AGENTS.md re-read "immediately before submission" | pr567.md:200–204 |
| 1 Oct | verifier "builds the proof and then replays every module with `leanchecker`, so both kernel work and per-module import are paid twice"; the 689-file package "ran past the verifier's 4 h" | pr582.md:168–170 |
| Sep–Oct | custom-syntax data macros are not admitted by source policy | pr581.md:159–160 |

---

## 3. Process and workflow

1. **Branch from the promoted frontier commit and name it.** Examples: "promoted lower-track commit `d375771`" (pr398.md:37–39); "promoted 68.10 … commit `09d8a2a`" (pr567.md:29–35); "our promoted 68.12 … commit `0275bb59`" (pr578.md:29–30). He states what is inherited and what is new (pr567.md:31–35; pr580.md:26–32).
2. **An external exact-integer mirror chooses constants; Lean proves them; the replay is "diagnostic only".**
   - "An exact integer mirror was used only to choose the constants" (pr398.md:154–155); "not trusted output from the external search script" (pr410.md:70–72).
   - "External generation proposes witnesses only" (pr580.md:93–97).
   - Replay lines are "checked against the parsed Lean on all 20 groups × 3,596 rows" (pr570.md:125–128). "Python copies are checked against Lean `#eval` on 80 values" (pr578.md:138–139).
3. **A control replay reproduces the prior certificate before any change.** "The 68.12 control reproduces the committed 68.12 Lean byte for byte" (pr578.md:117). "The 68.14 control replay … reproduces exactly before any change" (pr582.md:45).
4. **Every change is a matched experiment.** For example, exact removal disabled vs enabled with everything else fixed (pr582.md:130–137), and one-heavy ordering vs min-outside (pr582.md:109–110).
5. **Search to the edge, then report the thin margin.** Ledger slack of exactly 1 unit (pr398.md:134; pr410.md:66–70; pr419.md:63; pr465.md:54). "the search was run to the edge. If the grid does not replay on the verifier, the fix is to back off the C-kernel multiplicity" (pr465.md:155–159). He also warns that the constants are "a single checked profile rather than independently adjustable knobs" (pr410.md:228–232).
6. **Find the binding cell first, then target it.** Examples: the binding cell (15,55,6524) (pr505.md:91); replay maxima at (35,124,9090), (12,43,3206) and (14,45,9984) (pr567.md:155; pr570.md:124; pr578.md:141); a diagnostic cell (15,68,3626) (pr582.md:125–126); the census of hard cells before choosing file layout (pr465.md:116–120; pr410.md:160–166).
7. **Fixed validation recipe** (pr345.md:126–129; pr410.md:196–201; pr419.md:152–158):
   - `lake build …Solution`
   - `scripts/check-submission-imports.sh lower …`
   - `git diff --check`
   - `#print axioms ProximityPrize.Benchmark.candidate`
   - He later adds a cold build after deleting `.lake/build`, because "Lean will satisfy an `import` from a leftover olean whose source file no longer exists" (pr554.md:232–238).
   - He also runs a 4-thread `leanchecker` replay (pr582.md:186–189), uses `LEAN_NUM_THREADS=4` to match the 4 vCPU (pr554.md:220–227), and schedules measured module times on 4 workers to estimate wall time and critical path (pr582.md:186–188).
8. **Resource-test the worst module in isolation.** 4 GiB taskpolicy (pr419.md:171); Elab.async on/off peak (pr541.md:206–211); per-module peak ≤ 4.8 GB (pr582.md:178).
9. **Resubmission discipline.**
   - Identical bytes are resubmitted on infra failure: 410→413→415 at about 50-min spacing, and 572→573→574→576→577 about hourly until one promoted.
   - When the failure is diagnosed, he appends a "Submission history" block stating cause and fix, and says "Nothing about the proof changed" or "Scheduling only" (pr540.md:194–202; pr541.md:203–218; pr548.md:219–234).
   - "the manifest wins" over documented numbers (pr548.md:226–227).
10. **Attribution and scope honesty.** "The mathematics in this submission is 0xLucqs's, not mine" (pr539.md:22); credit for Jieyi's base (pr419.md:20); paper citation (pr592.md:21); "No full independent comparator was run locally" (pr570.md:153). He also publicly corrects his own earlier false conclusion (pr554.md:78–83).
11. **Multi-agent split.** Codex agents produce the mathematics; Claude Code turns oversized trees into legal packages and verifies them (pr581.md:18–21; pr582.md:165–166). Effort levels are recorded: xhigh (pr465.md:24), max (pr505.md:18; pr581.md:21), high (pr539.md:20).
12. **Profile, don't guess.** "The changes were profiled rather than guessed (Discussion #558)" (pr582.md:170–171). His own guess of a 3.5× waste from `first` was "wrong, and measuring it mattered" (pr554.md:162–167).

---

## 4. Dead ends and negative results

| PR | tried | result |
|---|---|---|
| 398 | residual B profile s=31 | larger allowance but "violated the protected mixed-characteristic gate"; used (94, 2452, 29) instead (pr398.md:117–121) |
| 419 | any replacement route at width 8 | did not close two units; "the issue was the interval envelope itself" (pr419.md:117) |
| 419 | uniform width-6 refinement | 12 later misses (pr419.md:118) |
| 419 | uniform width-2 refinement | 0 misses but one band took 696 s, versus 66 s for the targeted version (pr419.md:119, 133) |
| 465 | C-kernel m=270 | does not close cell 80575 (pr465.md:65–66) |
| 465 | `decide` on rank at m=340 | killed after 7 min at > 100 GB (pr465.md:71–72) |
| 505 | four phases | about −0.3%, does not close (pr505.md:62) |
| 505 | scalar box (96,132,28) | nullity −1,984,992 (pr505.md:76) |
| 505 | rationals 72/71, 48/47 | too coarse; 48/47 "misses by 5·10⁻⁶ bits"; used 10211/10000 (pr505.md:78) |
| 539 | R as the structured variable of the zero table | "every test failed … The structure is in V, and only in V" (pr539.md:91–94) |
| 539 | closed-form treatment of `strict` | cost > cap in 3,693/3,735 cells, so he concluded "genuine content" (pr539.md:169–174). **Overturned** by 0xLucqs's convexity in 68.06: "a conclusion about *my* method, not about the problem" (pr554.md:78–83) |
| 539 | batching threshold receipts | size only: 102,563 → 37,347 bytes, while time went 32 s → 36 s (pr539.md:175–179) |
| 539 | moving the ℤ comparison to ℕ | impossible; slopes are dynamically negative, and this branch covers 89.6% of 22,410 cells (pr539.md:180–185) |
| 539 | Prop → Bool fold | only 17% (29 s → 24 s) (pr539.md:186–188) |
| 539 | unchaining modules for parallelism | 40.8 GB aggregate RSS, modules at 313 s versus 84 s chained (pr539.md:189–192) |
| 539/540 | `Part/` subdirectory | refused at fetch, while the local build stayed green (pr540.md:194–201) |
| 540 | `Elab.async true` on a 932-declaration module | 9.2 GB peak, SIGABRT at 93 min; with async off, 3.4 GB (pr541.md:203–218) |
| 541 | trusting the documented 4 h budget | cancelled at 3h00m (pr548.md:219–227) |
| 554 | one batched decide per row | 57.8 s, slower than bullets at 43.9 s (pr554.md:169–173, 192–195) |
| 554 | closed form with default branch `\| _ => 0` | row 31 silently all-zero; 14 `decide … is false` errors. "A defaulting total function fails silently and wrongly" (pr554.md:107–139, 247–249) |
| 554 | incremental build after deleting modules | false green from about 600 stale oleans (pr554.md:232–238) |
| 570 | asynchronous elaboration of row modules | exceeded memory, so `Elab.async false` is kept (pr570.md:138–139) |
| 578 | 68.12 charges at agreement 181,265 | 1.0604 of the allowance, about 6% short (pr578.md:32–33) |
| 578 | A slope 35 | no positive nullity below agreement 181,275 (pr578.md:130–132) |
| 581/582 | old relative rectangles at 181,245 | 39,759 fail (pr582.md:36) |
| 581/582 | endpoint-only rectangle checks | missed 7 bad rectangles (pr582.md:50–53) |
| 581/582 | exact removal disabled | margin −541,044,526,150,703 (pr582.md:134) |
| 581/582 | minimum moved outside in one-heavy packing | saves only 7 rounding units, versus 6.07e15 for the inner order (pr582.md:109–110) |
| 581/582 | source 5 alone | does not route (15,68,3626) (pr582.md:125–126) |
| 581/582 | Codex raw tree | 27.2 MiB, 972 files, custom-syntax macros; inadmissible (pr582.md:165) |
| 581 | 689-file package | module time sum 25,649 s; ran past 4 h; the 153-module package sums to 6,453 s (pr582.md:168, 187) |
| 581/582 | base-64 varint packing tables | about 80% of a packing check was decoding; fixed-width second differences cut it from 12.8 s to 2.85 s (pr582.md:176) |
| 592 | generic (pigeonhole) shared top | 64 bits per coefficient; PrescribedTop stalls at 122.33 (pr592.md:55–56) |
| 593 | DKTZ height-3 trees in a 15-dim label space | M₃(15) = 2^62.7 < 2^64, too few (pr593.md:26–28) |
| 593 | closed-numeral PrescribedTop pairing proofs | leanchecker evaluated parts of a 650k-bit product, 14 GiB → fixed to 3.4 GiB (pr593.md:134–137) |

---

## 5. Skill candidates

### S1. `kernel-wall-closed-form`: turn an uncomputable `decide` into a closed form

- **Use when:** a parameter region is blocked because `decide`/kernel evaluation OOMs or times out (not because the inequality fails), or a table or sum dominates build time.
- **Steps:**
  1. Measure the reduction count as a function of the parameters (e.g. m²s/2).
  2. Fit the table or sum exactly: polynomial in one variable beyond a threshold, with head values listed. Test each candidate variable; "the structure is in V" (pr539.md:91–94).
  3. Write it in the falling-factorial basis, or multiply the identity by 2 or 6, so that every coefficient and subtraction stays in ℕ.
  4. Prove `closed = original` by kernel per row, or by induction closing with `ring`.
  5. Keep the original loop as a total fallback with an `_eq` lemma.
  6. Replace downstream enumerations (superadditivity, splits) by algebra on the closed form.
  7. Guard parameter ranges: no `| _ => 0` default (pr554.md:107–139).
  8. Re-run the search in the newly reachable region.
- **Sources:** 398, 465, 505, 539, 554, 593.

### S2. `bucket-retune-loop`: move one centibit on an exact ledger

- **Use when:** extending an accepted lower certificate by +0.01.
- **Steps:**
  1. Compute the new error count (about +10 errors per centibit near 68.1) and the radius at the top of the bucket. Use the larger denominator if one is allowed.
  2. Run the control replay of the incumbent and require byte or number equality.
  3. Re-derive each kernel as the smallest total with positive nullity at the new agreement. Check that slope caps still have positive nullity (pr578.md:130–132).
  4. Recompute every agreement-dependent constant from (errors, gap); do not copy them (pr398.md:180–183).
  5. Find the binding cell and the overshoot (e.g. 1.0604).
  6. Add targeted bounds as a menu: a new bound applies only on its proved range, and the inherited bound stays elsewhere.
  7. Run a matched experiment per lever.
  8. Prove floors only as tight as the ledger needs.
  9. Ship with a reported margin.
- **Sources:** 345, 398, 419, 505, 567, 578, 580, 582.

### S3. `adaptive-receipt-grid`: census-first certificate layout

- **Use when:** a finite grid certificate has a few hard cells among many easy ones.
- **Steps:**
  1. Run an exact integer census of route outcomes per cell (invalid/rate/ordinary/source/hard).
  2. Refine only the hard units (HardUnit → PointCell), with a short-circuit disjunction receipt.
  3. Tile hard rows finely and give easy rows one module each.
  4. Dispatch routes cellwise via a bounded search plus a `_spec` lemma.
  5. Before shipping, audit rectangles against the actual consumer's predicate, not just their endpoints (pr582.md:50–53).
- **Sources:** 398, 410, 419, 465, 581/582.

### S4. `lean-verifier-budget-packaging`: fit a decide-heavy tree into 4 vCPU / 24 GiB / about 3–4 h / 16 MiB with leanchecker replay

- **Use when:** a proof builds locally but must pass the remote verifier.
- **Steps:**
  1. Keep the root flat (no subdirectories) and re-read the live AGENTS.md and manifest.
  2. Prune unreachable declarations from `candidate`, keeping local instances.
  3. Set `Elab.async false` on modules with hundreds of declarations.
  4. Keep decide modules serially chained, never split for parallelism.
  5. Merge light modules along topological order only within equal external-import sets, and keep heavy modules as separate replay units.
  6. Use `interval_cases` + positional bullets rather than `<;> first`. Batching saves bytes, not time.
  7. Use dependent receipts (value plus proof) to avoid unfolding large divisions.
  8. Use fixed-width encodings over varints.
  9. Generalize numerals symbolically, then instantiate (for leanchecker).
  10. Do a cold build with `LEAN_NUM_THREADS=4`, run a 4-thread `leanchecker`, measure per-module peak, and schedule module times onto 4 workers to estimate the critical path. Plan against observed limits, not documented ones.
- **Sources:** 539–557, 567, 572, 580, 582, 593.

### S5. `submission-failure-triage`: classify, fix, resubmit honestly

- **Use when:** a PR closes without a verdict.
- **Steps:**
  1. Read the verifier JSON and classify the failure: fetch/policy (`Part/`), SIGABRT/memory, cancellation at the CI ceiling, `verification_retry_exhausted`, or ran past 4 h.
  2. Policy or memory failures need a code fix; infra failures need an identical resubmit.
  3. Append a "Submission history" block naming the failed UUID, the cause, and "no proof content changed".
  4. Space retries (he used about 50–60 min).
  5. If the failure was wall time, shrink the build before retrying.
- **Sources:** 410–415, 539–557, 572–577, 581–582.

### S6. `shared-top-pole-pair-attack`: upper-track construction pattern

- **Use when:** attacking an upper (ceiling) track whose prior certificates pigeonhole on shared locator coefficients.
- **Steps:**
  1. Use the DKTZ pole pair: f2 = 1/(x−β) (or R/(Y−α) on a fibration), f1 = R·f2. Each set S whose locator is R + C_S with deg C_S ≤ K wins at γ = C_S(β). f2 is far by the degree argument.
  2. Look for algebraic structure that makes the top coefficients equal *for free* (char-2 flat gap, odd counts of reserved cosets). Pigeonhole costs log2|coefficient field| bits per coefficient.
  3. Absorb a reserved set W into the shared top when deg L_W ≤ the gap.
  4. For more agreement, run the construction on fibre labels with a (fibre − 1)-point core.
  5. Count the family. It needs more than 2^64 + 1 members, and a generic pole exists if #collision-roots + |D| < |Ext|.
  6. Check injectivity by an exhaustive census at small width, then prove it by point-read decoding (second differences, wedge spans).
  7. Keep the existing certificate for the high band and split at the band boundary.
- **Sources:** 592, 593.

### S7. `menu-of-bounds-integration`: wire a local improvement into the global count

- **Use when:** a new bound helps only on a sub-range of factor shapes.
- **Steps:**
  1. State the bound with an explicit eligibility range (slope, middle, T-interval).
  2. Write a consumer that takes actual factor data, so the caller never supplies the count.
  3. Use a choice lemma that selects the new or inherited bound per factor.
  4. Use an affine-between lemma for interval interiors.
  5. Keep source eligibility physical: source total strictly below the interval's lower end, with caps widened only for the count (pr582.md:59–62).
- **Sources:** 567, 580, 582.

---

## 6. Could not determine

- **Closure reasons** for 410/413/415, 419, 554–557, 570/571 and 572–576. The notes contain no verdict for them. RAM limits are only inferred for 410–415 (pr419.md:171). 554–557 (68.06) were never promoted, and the next note shows the frontier at 68.10 by someone else.
- **The 419 baseline discrepancy.** The note says it starts from a "public 67.72 … commit `89b2e62`" (pr419.md:20), while the bot's header says the best is 67.67. Possibly 67.72 was public but unpromoted.
- **Who produced the scores between his PRs** (67.44–67.66, 67.68–67.80, 68.07–68.10). Only `d375771` (67.64), Jieyi (67.72), `2bf17023` (67.80 "hybrid"), 0xLucqs (68.05/68.06) and zkfriendly (`ad2b4ad`, cancelled) are named.
- **Who held binary-upper 114.11, and what FibrePencil, FibreWindow and LabelKey contained.** We only know they were "unions of cosets of one fixed kernel" (pr592.md:22).
- **The binary track's repository ID, minRelDist value, and exact `ProtocolClaim` statement.** The track's exact name is not given; the notes say "Binary upper" only.
- **What pr548 means by "the `carriers` closed form described above"** (pr548.md:231–232). It is not described in that note; it appears only in pr554.md:85–105.
- **The content of Discussion #558** (profiling) and of AGENTS.md rules 2 and 6 beyond what the notes quote.
- **Verifier logs for merged PRs.** Wall times above are proxies from created→merged timestamps.

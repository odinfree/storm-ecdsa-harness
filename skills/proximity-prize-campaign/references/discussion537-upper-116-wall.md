# Digest: Proximity Prize Discussion #537, the upper-track 116.13 2.0035-bit gap thread

Source: GitHub Discussion #537 in proximity-prize/proximity-prize, exported to one Markdown file (6,128 lines; opening post plus 39 comments, no nested replies). `L<n>` cites are lines of that export, in comment order. Thread opened 2026-09-11 by BitWonka; last comment 2026-10-24 (GordoAR). Track `irs-reduction-threshold-upper`, frontier 116.13 throughout. Nobody in the thread claims a score.

Comment numbering: C0 is the opening post and C1..C39 are the comments in file order. The thread uses the same numbers itself (yoyo930021 calls hybridnoise's comment C28 at L3890 and lamb356's second comment C26 at L3993). Who wrote what: BitWonka C0,1,4-7,10,13,14,16,19,20,23,29,36; jieyilong C2,3,12,21,22; dtumad C8,9,11,15,17,18; CrystallineButterfly C24; lamb356 C25,26; raresbuhai C27; hybridnoise C28; yoyo930021 C30-35; GordoAR C37-39.

Status tags used below: **PROOF** (written proof, not Lean); **PROOF-cond** (a proof that rests on cited or unverified inputs); **EXH** (exhaustive computation over a stated finite set); **EXACT** (exact distribution, nothing sampled); **SAMPLE**; **TOY** (small field or small domain only); **HEUR** (heuristic or extrapolation). None of the thread's results are Lean-formalised.

Quoting note: the seven questions are paraphrased, not quoted. Their exact wording is at the cited lines.

---

## 0. Verdict in one paragraph

The thread turns the upper-track gap into one precise object: the largest fibre of the key U -> (p_1..p_6(U), prod U) on 136-subsets of mu_256 \ {1} mod p. A win needs a fibre of at least 2^57.93, while the mean is 2^55.93, so the max must be 4.01x the mean. Over six weeks every proposed *mechanism* for a heavy fibre was priced or closed. These include coset and symmetric families, reciprocal locators, second cheap evaluation pins (base field, F_{p^2}, F_{p^3}), resultant keys, label-node words, masks, common-factor degree repair, Mobius and rational folds of every degree in the winning bands, and decomposable folds. The capstone is BitWonka C36 (L6034-6040). For the whole rational-pullback codeword ledger it shows that no w=0 key class of any instance reaches T, with no pigeonhole caveat, and that no w>=1 point gives a pigeonhole-certified win. GordoAR C39 (L6127) checks the shipped `OrbitPencil.lean` and finds it binding at its exact optimum. **What is NOT closed** is the bare heavy-fibre statement for the u=1024, w=6 key. C36 counts top pins at the pigeonhole rate p^w and says outright that it does not address structured pin collisions (L6044-6050). Every exact measurement says the key behaves like a random hash (max/mean - 1 between 1e-36 and 1e-95 on the computable marginals), but there is no theorem. Three gap-closing pin cells were never enumerated. dtumad's F_{p^2} circle census at N=283 was announced as running (L1612, L1637) and never reported. The F_{p^3} Singer cells N=67 and N=469 got only structured and small-order scans (L1151-1152). All three are closed only heuristically (GordoAR C38). A score now needs a mechanism outside the R*Q(X^u) / rational-pullback codeword shapes, or a non-pigeonhole certificate.

---

## 1. The problem as framed

### 1.1 Parameters and the rung ledger (C0, L18-38)

- Source `1b2ca03`. Best 116.13 = unsafe index 122369 (agreement t = N - idx = 139775). To improve, index must be <= 122362 (t >= 139782). Score = -128*log2(1 - idx/2^18), in hundredths, rounded down (GordoAR, L6127). The 116.11 and 116.00 rungs need indices 122355 and 122271 (L6127).
- p = 2130706433 (KoalaBear, p-1 = 2^24*127), N = 2^18, m = k = 2^17, challenge field F = F_{p^6}. Target T = floor(p^6/2^128)+1 = 274,980,728,111,395,088 = 2^57.932108 (L22, L86, L2632).
- Per rung with fibre size u: t = N - idx, core = t mod u, c = (t - core)/u, A = N/u labels, degQ = (m-1-core)/u, hard = (c-1) - (2+degQ). Then value = lgC(A-[core>0], c) - log2 A - hard*log2 p (L25-29).
  - Incumbent: idx 122369, u=512, c=272, A=512, hard=14 gives 61.7980, margin +3.8659 (L31).
  - First improving rung: idx 122362, u=1024, c=136, A=256, hard=6 gives 55.9286, margin **-2.0035 bits = factor 4.0097** (L32-35).
  - Confirmed by jieyilong (4.0096729423, L405), CrystallineButterfly (exact floor 68,579,341,025,511,058 vs 274,980,728,111,395,088, ratio 4.009672942309319, 2.0034845649 bits; L3175-3196) and GordoAR's 3,812-row bigint ledger (L6060).
- **The same deficit buys more than 116.12.** CrystallineButterfly C24 (L3104-3150) takes the full u=1024 fibre geometry: core 1023, deg Q <= 127, 127*1024+1023 = 131071. That gives t = 140287 (idx 121857), which passes the exact check for **115.46** (2^218854 <= 140287^12800) and fails 115.45. Fibre-size table (L3202-3211): u=512 61.80 bits at 139775 (passes); u=1024 55.93 at 140287; u=2048 53.74 at 141311; u=4096 53.40 at 143359.
- **Two currencies for one gap.** At u=512 the challenge count is fine but the rung is 7 agreements short (139775 vs 139782). At u=1024 the agreements are free and the challenge count is short (BitWonka C4, L750-759). jieyilong (L469-476) puts this as a transform: one that adds 7 agreements while keeping 6.8586661% of the 512-key guarantee (4,009,245,024,241,067,461) would also cross. No such transform exists.

### 1.2 The moment-curve fibre-max formulation (C0, L42-68)

- The u=1024 key is S -> (e_1..e_6(S), prod S) on 136-subsets S of the 255 labels mu_256 \ {1}. By Newton's identities (6! is invertible) this is the same as the power sums p_j(S) = sum_{i in S} zeta^{ij}, j=1..6, plus prod S in mu_256. That is a subset sum on the degree-6 moment curve.
- Equivalent forms: weight-136 binary vectors on Z_256 whose Fourier coefficients vanish at frequencies 1..6 (L50-51). Fibre differences are balanced ternary codewords of the GRS code with zeros zeta^1..zeta^6 (L231-233).
- A rung lives or dies on max fibre / mean fibre >= 2^2.0035. Exact handle: N(kappa) = M^-1 * sum_{(a,r)} psi(-<a,kappa>) T(a,r), with M = A*p^6 = 2^193.9321 and T(a,r) = [z^136] prod_{i=1}^{255} (1 + psi(f_a(zeta^i)) eta^{ri} z), where f_a = sum a_j x^j. Sanity checks: T(0,0) = C(255,136) = 2^249.860732; for a=0 and r odd, |T| = 1 exactly (L67-68). About 3 s per character in exact arithmetic (L245).
- dtumad's coding-theory restatement (C9, L1019). Folded by x -> x^512, OrbitPencil is a received pencil r_1 + gamma*r_2 on 511 labels with code RS[511,256] over F_{p^6}, agreement 272 = k'+16, and winning family 2^59. 116.12 is the same problem at agreement k'+17 with a family >= T. The Johnson agreement is about 362, so no known bound forbids it.

### 1.3 The seven questions (C0, L214-243), paraphrased

1. (L214) Is there a coherent family, one whose members share a key by construction, that is not a union of disjoint zero-blocks? Concretely: more than 2^27.98 subsets on one key, or a proof that such a family must decompose.
2. (L218) Is there an equidistribution theorem for subset sums on a degree-k moment curve over F_p? Does max/mean -> 1 as the mean grows?
3. (L222) Can max_a |T(a)| be bounded non-trivially? T(a) is e_136 of 255 roots of unity with degree-<=6 polynomial phases. The r=1 contour bound is hopeless.
4. (L227) Is the largest fibre the right object? Is there an accounting of the winning set at this radius that avoids a fibre maximum?
5. (L231) Is there literature on weight enumerators restricted to binary or ternary vectors in a large-prime-field code with consecutive zeros that beats the C(n,w)/p^k heuristic?
6. (L236) Does anyone have a construction whose winning set is not counted by a pigeonhole?
7. (L240) Can the two halves be bridged, so that a constructed family can be read as a fibre of the moment-curve key?

Added in C1 (L394-401): **Q1'** (a large non-zero-block family must be a characteristic-p accident; can it be described at all?) and **Q8** (does the accidental part equidistribute?).

---

## 2. Answer-state per question

### 2.0 Corrections and withdrawals ledger

| # | Claim | Stated | Corrected by | What survives |
|---|---|---|---|---|
| 1 | The fibration is forced to be a power map (a coset image loses 21 of 23 bits) | BitWonka C1 L318-328 | jieyilong C3 L493-497: a fixed-size product on c*mu_A lies in c^r*mu_A (A values). BitWonka C4 L717-723 withdraws; 200,000 random 17-subsets of a coset give exactly 256 products | The coset is a reparametrisation with no gain. Ritt (C10 L1091-1095): only two descents of mu_N exist, the power map and Dickson x+1/x; Dickson labels are not a group, and the index-127 filter returns nothing for Dickson |
| 2 | One challenge scalar buys exactly one root (gamma_injective) | C1 L299-301 | jieyilong C3 L499 (reciprocal locators force roots at alpha and alpha^-1). BitWonka C4 L725-734 accepts. BitWonka's mechanism alpha^{D-2}=1 was for a different (gamma*Y) pencil; jieyilong C12 L1193-1200 shows no pole condition is needed; accepted C13 L1361-1373 | The mechanism is real but priced at -96.15 bits at u=1024 (C4 L738-744). Legality forces J>=7, so the family is 25 bits short (C10 L1075-1081) |
| 3 | A size-s block kills at most s-1 moments (general frequencies) | C4 L777-784 | jieyilong C12 L1177-1179: {a,-a} kills every odd moment. BitWonka C13 L1332-1359: the general form is false, and his own table (g=2 B=3, g=4 B=5) already violated it | The consecutive-band version stands (the key is a consecutive band). The symmetry ledger is unaffected (215.69/214.34/213.91 vs 249.86; L1351-1353). The off-by-one argument (crossover needs B>=9 vs hard<=8) is **withdrawn** (L1354-1356). The char-0 coset theorem is re-verified (C14 L1455-1475) |
| 4 | max/mean sits below Poisson everywhere | C4 L824-826 | C5 L852-865: false at hard=2 (+6.8%, +10.9%). C6 L906-917 and C7 L941-948: the excess is monotone in the **mean** and is a small-mean artifact (hard=3 at mean 25,000 gives -1.9%) | max/mean -> 1 with growing mean, below Poisson at non-degenerate means |
| 5 | Q5 answered in the negative direction (collision deficit) | C4 L837-844 | C5 L877-880; C10 L1031-1036: Sum N^2 bounds the variance, not the maximum | Open statement narrowed to bounding the largest fibre |
| 6 | dtumad's mean-2^232 run retires the extrapolation caveat | BitWonka C10 L1046-1048 | jieyilong C12 L1183-1187: a quotient mod 127*2^10 leaves a 2^14 kernel; the {0,1,3} in Z/8 example. BitWonka C13 L1377-1386 withdraws; dtumad C15 L1485 withdraws his any-level uniformity claim | Repaired by a full-resolution computation (C17 L1570-1579): max/mean - 1 <= 1.6e-38. Still a single-pin marginal, not the conditioned fibre |
| 7 | F_{p^2} cells N in {6,283,566} are not enumerable | dtumad C11 L1154 | dtumad C15 L1503: 566 (~9 h) and 283 (~31 h) are enumerable; only N=6 (6.3e16 pairs) is not | N=566 closed exhaustively (C17 L1612). **N=283 result never posted** (L1637 is the last mention) |
| 8 | Degree-513 fold: 262143 points vs CZ bound 156352 | dtumad C11 L1163 | dtumad C15 L1505: wrong, it assumed the 511 fibre labels are 512th roots | Replaced by CZ13 Cor. 2 on the off-diagonal collision curve; conditional closure (see 3.7) |
| 9 | Partition census of mu_12 attainers (11/3/3 orbits) | BitWonka C16 L1535-1541 | C19 L1643-1651: the enumerator was incomplete for unequal profiles (1,920 of 207,900 partitions); correct counts 63/23/23 | The bound dim Lambda <= ceil(A/2) is a proof and is unaffected; all attainers are core plus dihedral pair-pencil |
| 10 | gcd/dim dichotomy: no pencil built from locator differences can be repaired by a shared factor | BitWonka C10 L1061-1068, C14 L1422-1453 (stated as a screen, A<=32) | jieyilong C21 L1829-1875: in an actual-prime counterexample, 3 of a 10-member fibre share Y-beta with span dim 2 and 3 distinct challenges | The counterexample forces gamma in K, so this mechanism has a p-challenge cap. Whole-fibre gcd = 1 still holds |
| 11 | Six-pin reciprocal family is 6.00 bits over T and fails only on degree (excess 1024) | BitWonka C10 L1052-1055, reading jieyilong C3 L565-567 | BitWonka, same comment L1075-1081: J=6 gives deg Q = 257 (illegal); the legal J=7 gives 2^32.94, -24.99 bits | Degree repair needs a shared factor; see row 10 |
| 12 | A label node costs about 1 bit | hybridnoise C28 L3479 | yoyo C30 Thm 2(c)/2'(c) L3979, L4010: a label node is a forced value pin or a hyperplane in b-space, never a free bit | Applies to all label words inside the template once row 14 is taken into account |
| 13 | The balanced deficiency profile is optimal (fold rows) | yoyo C32 L5392-5394 | yoyo C33 L5772-5776: false (216 of 2,348 small instances); support-2 at fixed (n,s) is also false | Conjecture S* (unproved), later made unnecessary by C36 |
| 14 | Words with 2L > N' are open | yoyo C30 L3909, L4051 | yoyo C34 L5812-5827: the set is empty at real parameters (L <= 63 for N'=126) | Theorems 1/2/2' cover every label word |
| 15 | Fold-family threshold n >= 72 (F4: 144) | yoyo C31 draft | Fable referee, C31 L4377-4385: optimal s=34 gives n >= 69 (F4: 138) | -- |
| 16 | GordoAR's exact enumeration of N=283/566 | C38 first version | Self-corrected inside C38 (L6102): the censuses used cosets of order h, so they closed the already-closed cells N = 7,528,998 / 3,764,499 / 2,509,666 | 283 and 566 are conditional-only in GordoAR's account; dtumad had already closed 566 exhaustively |
| 17 | Antipodal (p_1,p_3) family clears the mean by +0.0905 bits | GordoAR C37 L6062 | GordoAR wave-5, same comment L6085: the parity contact is not free; surplus becomes -0.9095 | Closed (toy evidence plus extrapolation) |
| 18 | BitWonka's no-winning-parameters region statement for folds | C29 L3869-3871 | BitWonka C36 L5997-6003: three gaps (equal-fibre shortcut invalid for mixed profiles; cap d <= 8710 not necessary; reliance on key-group inputs) | Replaced by the key-free recount (3.7) |
| 19 | d4.c diagnostics (dtumad's additive gist) | dtumad C18 artifacts | jieyilong C21 L1909-1916: the first-half log adds N(0) wrongly; a u128 capacity check overflows (needs 143 bits) | No end-to-end count error; the real-prime per-bin extrema are not independently reproduced |
| 20 | The monomial control's 56 states, read as a new field-independent family | construction line, C1 L336-351 | BitWonka C1 L356-367 himself: it is C(8,3), the coset family in other coordinates | Field-independence is the char-0 rigidity, not a new mechanism |

### 2.1 Q1 / Q1' (coherent family not built from zero-blocks)

- **Characteristic 0: answered NO, PROOF.** BitWonka C1 (L261-287). Over Q, p_j(S)=0 for j=1..6 holds iff S is a union of mu_8-cosets. Proof: Phi_256*Phi_128*Phi_64 = (x^128+1)(x^64+1)(x^32+1) telescopes to the coset indicator, so the zero-key char-0 fibre is exactly C(31,17) = 2^27.98. Consequence: about 2^55.93 of every fibre consists of characteristic-p accidents (L282-287). Verified at seven (A,hard) points (L278-280) and re-verified after the block-theorem retraction (C14 L1466-1473).
- **Upgraded to the whole pinned window, PROOF.** dtumad C11 (L1158-1161). At A=139782 the window contains P_s(T) for s in [1,7686], which is a complete residue system mod 2^12. Exact flatness off 512Z holds iff T delta T0 is a union of mu_512-cosets. Any non-coset family needs mod-p accidents at >= 15 further frequencies, about 31 bits each. Cofactors are an exact wash (L1160).
- **Mod-p local rigidity, PROOF with exact arithmetic.** jieyilong C22 (L2641-2733). For ternary v at N=64 (moments 1..6) and N=128 (moments 1..14), the vanishing forces period 8. The proof combines resultant divisibility by p^h with a Parseval/AM-GM norm bound, checked case by case (7 and 15 cases). Local fibre caps: 70; with the product pin 10; punctured 5; a four-cell Cartesian product <= 5000. It does **not** cover globally coupled families (L2653).
- **Block structures: PROOF.** BitWonka C16 (L1527-1533): dim Lambda <= ceil(A/2) for every partition and every choice of block functions. Unequal blocks arise only from the core (C19 L1651).
- **Char-p positives (all far below T):** an antipodal family of 2^118 selectors gives an existential fibre >= ceil(2^118/p^3) = 34,353,314 (C3 L505-509). Modular trades exchange 48/52/36 roots; a raw-integer-key fibre >= 3,337,745,696 (C3 L678). The portable char-0 class maximum with the product is 8,287,155 (C3 L503). There are no 7- or 8-root signed trace trades at KoalaBear (EXH over 84,010,500 records, C12 L1204-1216; independently rerun by dtumad C15 L1491-1499). GordoAR finds no example in 3,812 rows (L6076).
- **Q1' (can an accidental family be described):** unanswered.

### 2.2 Q2 and Q8 (equidistribution)

- **No theorem.** Every exact measurement points toward max/mean -> 1:
  - BitWonka EXACT histograms (C4-C7): at A=40, p=41 (hard 1/2/3, means 4.2e7 / 1.0e6 / 25,000) max/mean = 1.0000 / 1.0011 / 1.0147, all below Poisson (L941-945).
  - dtumad, real prime, hard=1 additive marginal, mean 2^218.87: max/mean - 1 = +2.383682e-36, which is 3e3 times below the Poisson reference (C17 L1583-1594). The mu_512 pool, mean 2^473.6, gives +2.475979e-95 (C18 L1620-1629).
  - Joint (p_1,p_2, label-sum) fibres at A=256 for p'=257 and 769 show only the label-sum parity term C(127,68)/C(255,136) = 5.332043e-39 (C17 L1598-1608).
  - Full-resolution multiplicative pin <= 1.585e-38 (C17 L1572-1577).
  - GordoAR toys on (p_1,p_3) fibres: 1.004-1.028 at means 3,289-3,797 (L6065).
- **Why measurements cannot settle it** (BitWonka C16 L1547). One 4x-mean fibre contributes 2^115.7 to Sum N^2 out of 2^305.7, and 2^230 to the fourth moment out of 2^307. A 2^-20 fraction of characters can carry the needed Fourier mass. So no moment, marginal or character sample can see it.
- **A random-hash caveat that cuts the other way:** size-5 vanishing sums of 256th roots, predicted at 4.05 per prime, occur 0 times across 7 primes, because the sums are nonzero algebraic integers (C4 L805-809).
- dtumad's stated position: he would not spend more search on the accidental family without a proof (L1167).

### 2.3 Q3 (non-trivial bound on max_a |T(a)|)

- **Open, not attacked after C0.** The only content is in C0: the triangle-inequality bound is vacuous. 720 sampled characters give log2|T| mean 30.96, sd 10.21, max 74.05, a bound of 2^11.19 against the 2^2.0035 needed, missing by 9.18 bits. A 24-sample pilot was 0.6 bits off (SAMPLE, L156-161). |T(a)| <= C always, with equality impossible for a != 0 (PROOF, L166-168).
- dtumad's exact hard=1 transforms (C17) compute the one-coordinate analogue exactly but bound no max_a.

### 2.4 Q4 (accounting without a fibre max)

- **Inside the R*Q(X^u) template: NO, PROOF.** hybridnoise C28 (L3454-3462) reduces a rung to the list size of one label word G in W = span(Y^1..Y^{A/2+1}). yoyo C30 Lemma 0 (L4035-4040) proves #winning gamma <= L(G), with no partial fibres and no extra factor A. Theorem 2(d)/(f) (L3980-3984) proves that for the pencil word the accepted sets are exactly one kappa-fibre (set equality, no dedup collapse).
- **Counting gammas instead of keys is strictly worse** (TOY at p=17, 97, 193, 257): gamma-fibres refine key-fibres, and equal-key fibres split on the free cubic coefficient (86/86, 2/2, 1383/1383) (GordoAR C37 L6070, L6078).
- **Key-free bound (PROOF):** swap lemma |class| <= #good_{s-1}/s, which needs no label structure (BitWonka C36 L6007-6017).
- **Partial escapes, all closed:**
  - Full MCA is not universally a fixed-word list. Challenge-to-codeword injectivity fails: 15 winners share the zero codeword (jieyilong C3 L618-627).
  - Any target-size family needs decoded-message affine dimension >= 9. At r=8 the bound is 176,301,312,604,155,999 < T (PROOF, jieyilong C22 L2760-2782). The driving quantity is A-k+1 = 8711, the same small-support rigidity under which a changed message must lose >= 8711 old agreements (C3 L680).
  - No real Johnson radius exists beyond n/2, so two-word geometry is mandatory (GordoAR L6072).

### 2.5 Q5 (binary/ternary weight enumerators)

- **Open; no literature reference produced.** BitWonka measured a collision deficit: Sum N^2 / random-hash = 0.9989, 0.9971, 1.0000 (EXACT TOY, C4 L831-835). He then retracted it as an answer, because it constrains variance and not the maximum (rows 4 and 5 of the ledger). dtumad's real-prime hard=1 Var/mean is 2.79e-7 against a Poisson reference of 1 (L1589). The statement still standing is: bound the largest fibre, not the collision count (L880, L1036).

### 2.6 Q6 (construction not counted by pigeonhole)

- **None.** Constructed families:
  - C0 (L97-102): 65 (F193, a characteristic artifact, L121-131), 55 (KoalaBear, n=32), 21 (F257), 4 lifted to idx 120833.
  - jieyilong's table (C3 L515-521): 8,239,666,916 = 2^32.94 reciprocal locators at 140,287 agreements; 565,722,720 mu_32 complements; 100,947; 2 (overlapping patches at 147,456).
  - Masks: 22 (C22 L2784-2818), then 1,712 (C23 L2958-2971).
- No construction exists within 2^25 of T at an improving agreement.
- GordoAR: every route ends in a pigeonhole (L6079). A polynomial-parameter family (gamma(x), c(x)) with more than 15 winners needs degree >= 8711*p/131073, about 2^27.1 (BitWonka C29 L3877).

### 2.7 Q7 (bridge construction and counting)

- **Bridged inside the template, PROOF.**
  - The monomial control (56 states, flat across primes 97..769) *is* the C(8,3) coset family (BitWonka C1 L336-367).
  - yoyo Thm 2(d)/(f): the pencil word's list *equals* one kappa-fibre. The C28 toy gives 109 accepted = 109 fibre = 109 codewords (L4003, L4063).
  - yoyo C34 extends the cover to all label words.
- **Construction-side compatibility test:** BitWonka's joint-source recovery criterion (C20 L1654-1821) decides whether several root sets serve distinct challenges on one source. It is a criterion, not a fibre reading.
- Outside the template: open.

---
## 3. Techniques and results catalogue

Each entry gives the statement, the numbers, who and when, and the status tag.

### 3.1 Coset structure and rigidity

- **Coset (zero-block) family and its price.** BitWonka, C0, 11 Sep, L181-210. At A=256, hard=6, a union of 17 of the 31 usable mu_8-cosets has p_1..p_6 = 0. There are C(31,17) = 2^27.98 of them, and the largest single fibre is 2^22.98. Going from A to A/8 loses 221.88 bits of entropy (36.98 per condition) and saves 185.93 bits of field cost (30.99 = log2 p per condition). **Coherence of this shape costs 36.98 bits per condition and buys 30.99.** Minimality was first shown by exhausting C(32,8) = 10,518,300 subsets (EXH), with an A=128 positive control (15 zero-blocks, all cosets, found by an MITM over 10,334,625 4-subset sums). It was later proved in char 0 (C1, PROOF).
- **Symmetry ledger, one rule for all symmetric families.** BitWonka, C4, L786-800, corrected in C13. A symmetry of order g beats the mean iff B*log2 p > lgC(A-1,c) - lgC(A/g-1, c/g).
  - g=2: -34.17 bits; g=4: -35.52; g=8: -35.95.
  - EXH over all 1,524 nontrivial symmetries of Z_A at six parameter points: the best reaches 0.21x the mean, and the ratio falls 50x as the mean grows (L797-798).
  - This single rule prices coset, inversion-pair, subfield-descent and the rank-3 monomial families.
- **Rank axis** (C1 L371-387). Rank-r projective state spaces cap at |PG(r-1,p)|. Rank 3 has capacity p^2+p+1 = 2^61.98, margin +4.0453, but the only known rank-3 family is a block family with 56 states. Swept block-family maximum over every rung: 22.98 bits vs 57.93. This is a capacity, not a construction.
- **Cyclotomic-norm rigidity mod p** (jieyilong C22, 13 Sep): PROOF; see 2.1.
- **Priced consequences of the window theorem** (dtumad C11 L1163).
  - Killing a single label-frequency orbit inside a coset union costs -69 to -83 bits.
  - The moving-core cell (core 1542 = 1023 + a full mu_512 fibre + 7 points, u = 135, A = 139782 exactly) is -2.91 bits, worse than the -2.00 incumbent u=1024 cell. This is a named near-rung that is easy to rediscover.
  - A denominator root at a label just removes that fibre. Mixed-radix coset unions collapse to the finest subgroup, because the subgroup lattice of Z/2^18 is a chain.
  - Fixed-centre lists at A >= 139782 are -56 to -80 bits at every fold.
- **Condition degeneracy is a plateau** (BitWonka C10 L1099-1122). Codewords lie in every condition's kernel, so rank is capped at N-k. In TOY runs, fibre and random families both saturate after 3-4 supports (fibre at rank 6, random at rank 7). This matches dtumad's zero Grassmann tangent dimension and the hill-climb that never leaves 1 over 12 restarts and 520 evaluations (C0 L140-142). Generic non-fibre rank-1 supports number C(n,a)/p^(D-1) with D = 8703. Toy check: about 85 at D=2 and zero at D=3 (L1129-1133).

### 3.2 Only one cheap key: evaluation-pin and resultant censuses

- **All rho in F_p, both characters (index 2 and index 127), cosets included.** dtumad C8, 11 Sep, L970-982. EXH at M=256 and M=512: the only hit is rho=0, the product key. Survivor decay matches random exactly: index 2 gives 1065353093 -> 266334823 -> 16641575 -> 1, and index 127 gives 16777215 -> 1027 -> 1. Runtime about 30 s per M on 24 cores. BitWonka's earlier 127th-power filter (C1 L308-316: 16,777,216 -> 132,634 -> 1,079 -> 11 -> 1) was incomplete; dtumad's scan replaces it.
- **Generated subgroups at real p** (lamb356 C26, 16 Sep, L3326-3350). |H_0| = 128 (7 bits); every other rho tried has |H_rho| = p-1 (all zeta^s for s=0..127, and 80 of 80 random rho), so EXH on zeta^s and SAMPLE on random rho. Products of j distinct generators from a 64-block have no collisions: |P_2..P_5| = 2016 / 41,663 / 635,245 / 7,609,493 = C(64,j). Proof that rho != 0 never gives a mu-coset generator set (L3266-3273, plus EXH at three small (q,F)).
- **Conditioned on product phase** (raresbuhai C27, 23 Sep, L3375-3393). For A = 128/256/512 with selector sizes 68/136/272, there are pair swaps whose V_U(1)-ratios have full order p-1 (897828945, 2067659621, 168615078). A common filler exists at every residue, so within each product class the ratio group is all of F_p^x. EXH plus PROOF. This rules out an index-16/32 discount on V_U(1). It does not bound image size or uniformity.
- **Twisted F_p pins** (C29 L3878): only rho=0, even allowing a mu_256 character twist.
- **Resultant coset keys of degree d** (dtumad C8 L1002, gist L1513). The cost would be 31(d-1) + log2|S|; one coset-valued quadratic with |S| <= 2^28 would close the rung. EXH ranges: d=2 up to |S| = 2^17 (3.4e10 systems per pool), d=3 up to 2^11, d=4 up to 2^9, d=5 for |S| in {64,127,128}. Only monomials X^d appear, i.e. functions of the product key. Over C this is a theorem (Fourier support); mod p it would take an accident of probability about 2^-5000.
- **Extension-field pins** (dtumad C11, 11 Sep, L1144-1154; C15; C17).
  - A pin at rho in F_{p^2} \ K replaces two K-pins (62 bits). Admissible cells are N | p+1 = 2*3*283*1254833, with ledger values N=6 +0.58, 283 +6.1, 1698 +8.7, >= 1254833 +18. GordoAR verified these equal lg2 N - 2 (max deviation 0.26, L6100).
  - F_{p^3} Singer cells N in {7, 67, 469} (+0.8 / +4.1 / +6.9). These were **not** enumerated exhaustively. Only structured rho scans (histograms uniform to three decimals) and all 18.1e6 small-order beta in F_{p^3} were checked (L1151-1152). Under GordoAR's hypothesis (H) the expectations are 2^-620 / 2^-1448 / 2^-2161 (L6115, HEUR). N=67 and N=469 would each exceed the 2.0035-bit gap.
  - EXH closed: N in {1254833, 2509666, 3764499, 7528998}; N = 1698 (7.9e11 pairs) and 849 (3.1e12); all norm-type t in K (indices 2, 4, 127); all beta in mu_{p+1} for argument types 3, 283, 1254833; 15.5e6 and 18.1e6 small-order beta in F_{p^2} and F_{p^3}; N = 566 (7.09e12 pairs, 0 hits, max coverage 13 of 255; C17 L1612).
  - Survivor counts match uniform to three digits. A planted-pool control recovers the planted map.
  - Not enumerated: N=6 (6.3e16 pairs, worth only +0.58) and **N=283** (run announced, never reported).
  - BitWonka TOY (C16 L1562): cells exist only at N=2 and A <= 16; count p*A*2^-(A/2-1); extrapolated expectation 2^-88 at real scale.
  - GordoAR **pair lemma** (C38 L6106-6109, PROOF; full enumeration at p=101 and 257): rho -> w_rho(y1)/w_rho(y2) maps F_{p^2} \ F_p onto mu_{p+1} \ {1} with exactly p-1 preimages each, so pair coincidence is exactly about 1/N for every pair type.
  - Under the hypothesis (H) that no higher-order coincidence exists, E = 2^-594.9 at N=6 and 2^-2006.8 at N=283 (HEUR).
  - Faithful-scale test at p = 228097 (256 | p-1, 283 | p+1): 645,124 candidates per cell, 25.9M in total, zero full passes, order-3/4/5 joint rates 1.0034x / 1.0047x / 1.020x (EXH at the analogue prime, L6123).
  - Weil (2N*sqrt(p), about 2.6e7) and Burgess-type bounds (about 3.4e3) both exceed 255, so they exclude nothing (L6119).
- **Base-field-valued pencils** give |W| <= p (C16 L1554, PROOF). Spending gamma on a Galois orbit forces gamma in c*F_p^x, so at most p winners (hybridnoise L3485, PROOF). Subfield descent costs (d-k) units and buys (d/k - 1): -61.98 bits or a cap at p (C4 L761-771). BitWonka warns he once computed a false +28.99-bit win here.
- **Architecture of OrbitPencil traced to source** (BitWonka C1 L291-301). `productKey U = (sum b.val) % 512` is used only in `deltaV_eval_zero`, which puts the root X into the pencil. Dropping it raises hard by 1: pay 30.99 bits to save 8. The key is therefore a net gain of about 23 bits.

### 3.3 Exact fibre statistics

- **FFT and MITM histograms** (BitWonka C4-C7, 11 Sep). The key (p_1..p_h mod p, label-sum mod A) lives in Z_p^h x Z_A, so the full histogram can be computed exactly by group-convolution FFT (hard <= 2) or by MITM over label halves with `bincount` (hard = 3). Choosing small p with A | p-1 decouples the mean from hard (A=40, p=41, C(39,20) = 6.9e10 subsets into 2.76e6 bins). The method caps out near A=48. Tables at L816-822, L859-865, L896-899, L941-945.
- **Multiplicative pin, full resolution, real prime** (dtumad C17 L1570-1579, EXACT). Character transforms E(a) = e_136 in F_q for five NTT primes q = 1 mod p-1; inverse NTT of length 2^24*127; Garner CRT up to C(255,136). Mean 2^218.87. max/mean - 1 is +1.098563e-38 (random rho), +7.030943e-39 (zeta_{2^24}) and +1.585375e-38 (zeta_127*zeta_{2^24}). At least 99.99999% of the variance is the quadratic-character mode. Validated against brute force at p'=769 and bit-for-bit against the mod-130048 tables.
- **Additive hard=1 at real prime** (C17 L1583-1594; C18 L1620-1629, EXACT). mu_256 pool: max at kappa = 67698650, min -2.398130e-36, Var/mean 2.787316e-07. mu_512 pool: max at kappa = -1 (the complement map gives N_272(-1) = N_239(0); not investigated). Gists at L1633-1634. jieyilong's independent audit (C21 L1901-1916) matched every toy bin and 69 manifest hashes and found two d4.c diagnostic bugs with no count error. **Real per-bin data were not independently reproduced.**
- **Joint key at real pool size, small p'** (C17 L1598-1608, EXACT, small characteristic only): h <= 2 with the sum, and (p_1,p_2,p_3) without the sum.
- **Exact product marginal** (jieyilong C2 L409-431, PROOF plus a DP check). N_max = [C(255,136) + C(127,68) + 2C(63,34) + 4C(31,17)]/256 at r = 4 mod 8. There are 7 distinct marginal counts and the relative bias is 5.3320430157e-39. ceil(N_max/p^6) equals the mean guarantee 68,579,341,025,511,059, so choosing the product class first gains nothing.
- **Low-degree image equations** (jieyilong C2 L437-462, PROOF). If W + B <= 136 (weighted moment degree plus degree in z), no nonzero F(s_1..s_6, z) vanishes on all 136-subsets. For moment-only F, Pr[F = 0] <= W/137.

### 3.4 Pricing identities and ledgers

- **Pricing the fibre family** (lamb356 C25, 16 Sep, L3232-3258, PROOF of an accounting identity). Split the conditions as m - D - 2 = T (pinned leading coefficients, log2 p each) + (d-1) (root conditions, priced at their value set). Then m = D + d + 1 + T and A = w + (T + d + 1)*f. Calibration: d=2, T=14, f=512 gives A = 139775, m = 272.
  - rho=0 costs log2 F; every rho != 0 costs about 31 bits (C26).
  - **A mask is a root condition at rho = Y_c != 0, so it costs log2 p per f agreements, the same exchange rate as a pin** (L3271-3279).
  - Best corner reaching radius 140632: f=2048, d=2, T=2 gives A = 141311 and class 2^53.74, 4.19 bits short (18.2x).
  - With d=3 the corner needs a rho with |{V_U(rho)}| <= 2^27.5 (11.3x). That would land idx 120833 at 114.10 (written `B = 11410`) and would refute the lower track's 115.00 target as a side effect (L3281-3300).
  - Tip: never put exact bigint binomials inside a search loop; 68,000 calls to C(131071,k) stall for minutes (L3303).
- **Cost map and asymptotic limit** (hybridnoise C28, 23 Sep, L3464-3488). Acceptance amounts to 7 Hankel functionals m_i(V) = sum_j V_j s_{j+i} of the complement locator (127 numbers s_0..s_126 at u=1024). Kronecker nodes price as: infinity 31 bits each, 0 (phase) 8 bits, other rho >= 31 bits, label about 1 bit (the last later refuted, ledger row 12).
  - The asymptotic stall of any subset-indexed template is H(rho) = log2(p)*(rho - 1/2), rho* = 0.532173, about idx 122,638 = 116.48 bits.
  - 116.13 sits past that limit only because of a fixed bonus: +62 (two free roots) - 9 (phase) - 4.8 (Stirling) = +48.2, plus 13.6 from the per-label term, giving 61.8.
  - **hybridnoise's conclusion: a single additional condition at u=1024 that is free, or costs at most 29 bits, would suffice** (L3486).
  - The fixed-word-list route (`HalfRadiusCollision.lean`) is about 54 bits worse than the pencil (L3488).
- **Two prior-campaign leads closed at real scale** (dtumad C8 L986, C9 L1012-1014).
  - (a) The six-value coefficient-257 fibre. A 518-point core reaches exactly 139782 *if* some 14-key/product class larger than 6.82*Theta (Theta = 587929506547794519) has coefficient 257 = -e_15 taking <= 6 values; <= 7 values is provably insufficient. The EXH census of all 131072 affine maps of Z/512 that force p_15 gives at most 2^40.87 symmetric selectors (17 bits below T), and antipodal families give 2^24.94 per class. Under the accident model the expected number of qualifying classes is below 2^(-1.67e19).
  - (b) The s=128 quartic generalised-Pade chart (fibre 2048, 68 fibres, core 518) is exactly the (M=2048, t=4) rung: 2 K-pins plus the product key retain 15073406664870633, which is -4.189 bits.
- **Rung ledger and binding probe** (GordoAR C37 L6060, C39 L6127). 3,812 rows over u in [128,16384] in exact bigint arithmetic: zero winning rungs. #eval probes on live Lean definitions: `OrbitPencil.lean:796` `hagree` binds at u=122369 with deficit exactly 1/8/64 at offsets -1/-8/-64. T_card = 139775 = 273*512 - 1, and row degree 131071 = rowDim - 1 exactly. Edits do not exist at 512-granularity. **The template is at its exact optimum; a beat needs >= 2 fibres per signature.**
- **Antipodal two-pin family** (GordoAR C37 L6062-6092, TOY plus PROOF pieces).
  - The (p_1,p_3) family clears on the mean by +0.0905, but the legal contact count is 127 against a quotient at 130.
  - Product parity rho^2 = -1 buys one contact (130 -> 129) but costs a full parity bit at the real mean. Both parities occur in 66049/66049 fibres at mean 16, so the surplus is -0.9095.
  - On (p_1,p_3)-fibres, delta e_1..e_4 vanish identically (Newton; 900/900 pairs at real p). So degree 127 is reachable iff delta p_5 = 0, a (p_1,p_3,p_5) class at -30.9 bits; delta p_5 was never zero in 25,351 exact pairs (|S| = 5..13).
  - The mu_4-coset route clears the count by +2.56 bits but fails the contact gate by -2.35 bits.
  - Also: odd moments are independent on mu_256 (E1), and the f_2 slack of 8192 is worthless because the agreement set is shared (L6072).

### 3.5 List structure (label-word) results

- **The pencil word is optimal on toys** (hybridnoise C28, TOY/EXH over slices). About 36M words over 2-D slices, including all 105 coordinate planes through the pencil word G = Y^c + g0.
  - A=32, p=769, c=19: pencil L = 5811 vs best other about 2370.
  - A=32, p=193, c=20: pencil 109 vs 108.
  - Raw counts collapse under dedup, the largest from 888,041 subsets to 12 codewords (L3494-3501).
  - The toys have 3 conditions, not 7.
- **yoyo's list-structure theorems** (C30, 25 Sep; PROOF-cond, citing the Heinig-Rost / Iohvidov Hankel-kernel theorem with a sketch).
  - Deflate the root 1 with s'_m = s_{m+1} - s_m, N' = A-1-w, e' = A-1-c.
  - Thm 1 (rank <= k): complete collapse, L(G) = 1.
  - Thm 2 (rank k+1, where the pencil lives: Lambda = X*Z^k, L = 8 at the real rung): accepted sets equal one kappa-fibre exactly, a label root is forced into U with a pinned value, and L(G) = #accepted when Z | Lambda.
  - Thm 2' (rank k+1+t): always k conditions on kappa(U). A label node is a hyperplane b(sigma,1) = 0. Dedup collapses by at most C(c+t,c); referee counterexamples at p=73, A=24 (253 -> 205) and p=97, A=16 (9 -> 1) (L4012-4015).
  - Lemma 0: the template reduction (2.4).
  - Real-rung parameters A=256, c=136, w=129, k=7, e'=119, N'=126; **w=129 and k=7 are extrapolated from the formalised u=512 case** (L4002).
  - Checked by three independent code bases on toys up to A=32; the C28 toy was rerun over 84,672,315 DFS leaves giving 109.
  - C34 later shows 2L <= N' always holds at real parameters, so the theorems cover every label word.
- **The pure list door is shut** (BitWonka C13 L1390-1401, TOY). Maximising |list(g)| over words g gives surplus over pigeonhole from +3.70 down to -0.51, monotone in the mean; at the largest mean the best list is 30% below pigeonhole. Collapse, not counting, binds: random g has support:codeword ratio 0.64-0.75, and hill-climbing on supports reaches 8008 supports on one codeword.

### 3.6 Construction-side mechanisms

- **jieyilong's constructions** (C3, 11 Sep, L515-567). Counts and caveats are given in 2.6.
  - Cubic-subfield collision budget: B(N) = 256C(N,2) - 511C(a,2) - r*a, with loss <= 1,910,340,051 at N = 2^59+1. That yields 576,460,750,393,083,438 distinct challenges at 139,775 agreements, still 7 agreements short.
  - The mu_32 all-complement separation proof needs no enumeration (L533-542).
  - Fixed-even trace-part conditional construction: 140,799 agreements, needs 274,980,728,361,535,374 selectors in one family, and that family is missing (L571-594).
  - Common-mask rounding theorem: probability >= 0.43002503295 of gaining a fibre. 639,452,841,229,043,320 directed vertices would suffice. Exclusion holds for every fixed difference with <= 61 outer roots (bound 141,394,850,705,352,846 < T at s=61) (L598-612).
  - Incidence bound floor((m-a+1)C(m,d)/C(a,d)). The mu_64 stride-4096 class maximum is C(64,32)/17 = 107,801,420,055,446,502 < T (L631-645).
- **Reciprocal locators** (jieyilong C3 L546-567; priced by BitWonka C4, C10). 136 inversion pairs plus {-1} in mu_512 give Y^8 | Delta, the second root comes free at alpha^-1, there are 140,287 agreements, and ceil(C(255,136)/p^7) = 8,239,666,916. Reciprocity is 28.86 bits worse than the plain pencil: entropy halves (-254.78) while pins halve (+216.92) (L1088-1090). The J=6 version (2^63.93) has deg Q = 257, which is illegal.
- **gcd/dim dichotomy and its counterexample.** BitWonka C10/C14 (TOY, 27 points, A <= 32): dim(span) >= 2 implies gcd = 1, and dim = 1 implies full degree. Reproduction traps (L1070-1073): small samples inflate gcds, and stripping trailing zeros destroys the Y-power, so track the Y-adic valuation explicitly. jieyilong C21 (EXH over C(16,8) = 12,870 subsets, PROOF by explicit certificate): zeta = 148625052 of order 16, M(Y) = Y^2 - 1959434487Y + 1619648401; a selected 3-member subfamily with gcd Y-beta, span dim 2, gammas 0 / 115541457 / 144827143, rescalable into mu_512 \ {1} by r = 170455089. Its limit: beta = alpha^p forces gamma in K (p-cap) (L1875). Scripts with SHA-256 at L1927 and L2054.
- **Joint-source recovery criterion** (BitWonka C20, 12 Sep; algebra independently re-derived by jieyilong C21 L1877-1899).
  - Quartic guarded model: H = <699882112> (|H| = 128), D = X^4 - 1, 68-subsets of 124 allowed roots, source commit `224323f0`.
  - Necessary test det(P_j,Q_j,P_k,Q_k) = 0. Then four shared invariants A0..A3 plus a 2-unknown linear system in (s,r). Singular systems leave an affine source line. gamma = -u/u^p is injective on PG(2,K).
  - Toy p=257: 209 of 210 pairs recover the source.
  - Actual-root bank: 51 shapes, 757 rotations, 286,146 pairs. 285,156 fail the determinant; the 990 proportional-row pairs are inconsistent. **No compatible pair** (EXH on the bank only).
  - Sage filter at L1789-1817.
  - Implementation must enforce kappa not in H, v != 0 and s,r != 0. The N_l correction -(X^{72-l} mod D) is essential (L1886-1888).
- **Leading jets freeze the compiler** (jieyilong C22 §2 L2736-2758, PROOF; 37,525 finite checks). Locators sharing their top ell coefficients have identical division quotients, so the residual lies on one fixed projective line, giving at most max(p+1, #poles) directions. Fixing all four leading coefficients of the degree-68 source restricts it to <= p+1; the degree-272/top-14 family has the same issue. **Vary the leading jets** in joint-source search.
- **Deterministic masks: 22, then 1,712** (jieyilong C22 §4 L2784-2914; BitWonka C23 L2917-3096; EXH plus scripts).
  - Original bank: 405 eight-subsets S of {1..15} with sum = 4 mod 16, V_S(Y) = (Y+1)A_S(Y^2) of degree 17 on mu_32, alpha^3 + alpha + 4 = 0, Y = X^8192, D = V219 - V73, flips at fibres 0/14/5/10/13 of sizes 8192/3108/1036/518/1036. Result: 22 distinct challenges at 139,782-150,046 agreements, witness degree <= 106,496, far-direction cap 139,263. Affine span 7 gives a bound of 5,858,641,064,542,080 < T.
  - BitWonka's version releases the next-coefficient pin (all 17-subsets of mu_32 \ {1} with V_U(0) = g^8, deg Q <= 14). The MITM finds 2,202 eligible candidates. Published mask: 1,627; new mask (flips 8192/4096/1012/2048/518): **1,712**, affine dimension 15, agreements 139,782-149,504, witness degree <= 114,688.
  - **The jump comes from one extra outer degree (13 -> 14). The mask-only gain is 5.22%. Restoring the pin returns 22 winners**, and the 512-label frontier has no spare degree (L2973-2981).
- **Overlapping local patches** (jieyilong C3 L614): a 405-member mu_32 key family admits a two-site patch keeping 2 challenges at 147,456 agreements. Another construction gives 15 winners on the same zero codeword (L622).
- **Pole-direction pencils folded by x^u** (C29 L3876, PROOF): |W| <= C(L,k)/C(c,k), which is 2^55.54 at u = 4096.

### 3.7 Rational folds and Corvaja-Zannier

- **Mobius census** (dtumad C8 L987-999, EXH plus PROOF). Maps with m(mu_M) inside mu_N: only x -> zeta*x and x -> zeta/x, for N up to 8192 (5.50e11 candidates at the top). Normalised with m(1) = 1, the census reaches the full domain N = 2^18 for both sources, leaving only the identity and 1/x. An algebraic proof covers N <= 8192 from mu_512 and N <= 2048 from mu_256. raresbuhai (L3436-3440) gives a short proof that every Mobius permutation of mu_{2^18} is dihedral, and that the semilinear stabiliser of a pole has at most 2 elements, not 4. He also proves that two distinct challenges cannot win on the same qualifying agreement set for one violating affine instance (L3442).
- **Degree-513 fold** (dtumad C15 L1505, PROOF-cond). CZ13 Cor. 2 is applied to the off-diagonal curve g(x) = g(y) on mu_{2^18}^2. Every bidegree (s,s), 1 <= s <= 512, fails, with minimum margins 18006564492279800 and 557723012038654. A toric component would need a deck group of order 513 in PGL(2,p), impossible since gcd(513, p(p^2-1)) = 3. The closure is conditional on the bridges listed in the earlier campaign's `Tiny513*Gate` Lean files (branch `codex/upper-transfer-6732`).
- **Winning fold bands** (BitWonka C29, 24 Sep, L3809-3833). For a fold h = A/B of degree d with codewords R*B^(s-3-w)*q_U(A/B), a win at idx 122362 needs (3+w)d - Sum(d - f_lambda) >= 8711 and C(n,s)/(m p^w) >= T. That gives 16 bands: w=0 at d = 2904-3855 (n = 90 -> 69), w=1 at 2178-2621, ..., w=14 at 513-514, w=15 at 484-485. No power of 2 lies in any band, which is why x^u stops at 122369.
- **Local CZ Prop. 2 without the p-condition** (C29 L3837-3855, PROOF; about 1e8 test cases with closest ratio 0.994). One place with |E|k + he < p and he < |E| replaces the global resultant step. Corollary: for d <= 3777, collisions on mu_N^2 number at most 8.56e8, so no fold has 70 fibres of >= 3707 points. That stopped at w=0, d in [2904,3244], where the bound is 4.1% too weak. Dihedral g(x^512 + x^-512) with g cubic has <= 3 complete fibres, against about 72 needed.
- **Decomposable folds** (yoyo C31-C35, 25-26 Sep; EXH/SAMPLE plus PROOF-cond).
  - d=3072 census of families F1-F4 (C31). F1 (g o x^1024) EXH: max k = 3 over 5,461 representatives (257 s on 18 cores). F4/F2/F3 by sampling with full verification: max k = 3, miss probability <= 8.7e-6 for F4 and 2.06e-4 for F2/F3.
  - CZ composite table (C32): 7 rows closed after C34, (3072,10/9/8), (3200,7/6), (3232,5/4). Ratios B/L_true: (3072,10) 0.90747, (3072,9) 0.97332, (3072,8) 0.99610 with L_true = 9064, (3232,4) closed by Rust branch-and-bound with B = 2743529 (C34 L5829-5861).
  - Conjecture S* and lemma U_3 were unproved (C33, C35).
  - All of this is **superseded by C36** below.
- **Sharper CZ (22') and the key-free recount** (BitWonka C36, 30 Sep).
  - (22'): G <= (h deg v + k deg u)/n + (n-1)/2*chi - ((n-k)T_v + k T_u)/n. It replaces CZ's crude bound (12) with the exact divisor bookkeeping, gaining a factor 3^(1/3) (constant 2.38 vs 3.43). PROOF; 0 violations in about 3.8e11 exact instances; sharp on u = x^m, v = (x-r)^-(p-1), where G = m and (22') gives m + 1/3. An independent referee re-derived it (L5952-5984).
  - The w=0 pair-bound fraction drops from 0.809 to 0.565 at d=2904, where 0.775 is needed, so the window closes with a 27% margin for every h, composite or not. This makes S* and U_3 unnecessary (L5986-5994).
  - Swap lemma: |class| <= #good_{s-1}/s.
  - Power-of-2 degrees (d/u in {1,2}) are counted exactly. The one case the swap lemma does not close at once is the u=1024 rung at w=6. Complements must share core mass, so they form an intersecting family, and EKR / Ahlswede-Khachatrian applies: worst case 0.91 bits below T (L6019-6026). This is the ledger's closest point to T. **It is an upper bound on what the ledger can certify at the pigeonhole rate p^6, not a measured class and not a bound on the heaviest single fibre**, so it does not shrink the 2.0035-bit gap.
  - A monotone Chernoff bound handles large w, certified at w_d = max(30, ceil(8711/d) - 3).
  - Result at thresholds idx 122362 and 122368: w=0 on d in [2904,131071] is unconditional for any instance of this shape; 1 <= w <= 29 and w >= 30 are closed at the pigeonhole rate (worst -3.3 bits). Thinnest margins of 3e-6 bits were re-verified in 60-digit arithmetic (L6034-6046).
  - Scope (L6044-6050): the rational-pullback codeword ledger only; for w >= 1 the pins are counted at p^w.

### 3.8 Adjacent mathematics imported (jieyilong C3 §8-10, L651-697), compressed

- Cubic function-field norms (Leem-Jacobson-Scheidler): a census of 245 centres gave at most 35 messages at nine agreements, with no amplifying operation.
- Doliwa / Odesskii refactorisation: invertibility at counted nodes fails on the actual domain.
- Huang-Landsberg rank-4 templates: max_gamma rank(A + B T_gamma) = min(6, dim(im A + im B)) gives a fixed containing image.
- Sheekey-Van de Voorde rank-metric: collapses on the prime-field domain.
- Corvaja-Zannier Thm 2: a non-monomial Mobius map sends <= 19,505 domain points back into the domain.
- Juskevicius-Semetulskis: Frobenius rank <= 3 for 58-generator Boolean families.
- Li-Shagrithaya list recovery: 13^16 messages, but <= 149,441,834 matches per word.
- Crites-Stewart receiver averaging: M is about 2^-8582, so the certificate guarantees 1.
- Diamond-Gruen: needs radius >= n/2.
- Genus cancels from divisor counting (L666).
- All are scoped negatives.

---
## 4. Bottom line for someone attacking 116.13 today

### 4.1 Closed routes and how strongly

| Route | Closure | Strength |
|---|---|---|
| Re-tuning the x^u fibre template (any u, core, c, w) | GordoAR 3,812-row exact ledger with zero winners (L6060); `OrbitPencil.lean:796` binds exactly (L6127); C29 band table: no power of 2 in any band | Exact arithmetic plus Lean #eval probes. **Strong** for pigeonhole-certified rungs |
| Any rational pullback fold h = A/B in the winning bands (codewords R*B^(s-3-w)*q_U(A/B)) | BitWonka C36: w=0 unconditional for every instance of the shape; w >= 1 at pigeonhole rate (L6034-6040) | PROOF plus exact computation, one referee pass, not Lean. **Strong** within the ledger |
| Mobius / dihedral folds, degree-513 fold, decomposable G o x^(2^a) | C8 EXH to N=2^18; C15 CZ13 Cor. 2 (conditional bridges); yoyo C31-35, superseded by C36 | EXH plus PROOF-cond |
| Second cheap K-rational pin (evaluation, resultant, twisted, conditioned on phase) | C8, C26, C27, C29 | EXH at real p over all rho; resultants over stated degree and subgroup ranges only |
| Extension-field pins: F_{p^2} N >= 849 and N = 566, all small-order beta | C11, C17 | EXH |
| Extension-field pins F_{p^2} N = 283 (+6.1 bits) and F_{p^3} Singer N = 67 / 469 (+4.1 / +6.9), each enough to close the gap | **Not closed by enumeration.** dtumad's N=283 run was never reported, and the Singer cells got only structured and small-order scans. GordoAR's closure is conditional: pair lemma, hypothesis (H), and for N=283 a faithful-scale analogue with 0 hits in 25.9M | HEUR / SAMPLE |
| Coset, symmetric and reciprocal families; subfield descent; rank-3 block family | C0, C4, C10, C13 ledgers: 34-36 bits short; reciprocal -28.86 vs plain; legal J >= 7 gives 2^32.94 | PROOF plus EXH over 1,524 symmetries |
| Label-node or alternative-word substitution inside R*Q(X^u) | yoyo Thms 1/2/2' plus C34; hybridnoise toys | PROOF-cond (cites the Hankel kernel theorem) |
| Masks as a multiplier | lamb356: a mask is priced like a pin (log2 p per f agreements); C23: 5.22% mask-only, 22 at tight degree | Argument plus EXH on banks |
| Shared-factor degree repair | Whole-fibre gcd = 1 (screen at A <= 32); selected-subfamily repair exists but forces gamma in K, so <= p challenges | TOY plus PROOF of the p-cap |
| Affine decoding / low-dimensional message families | Need affine dimension >= 9 (C22 PROOF); F_p-affine rules have span <= 6 | PROOF |
| Antipodal (p_1,p_3) two-pin family | -0.9095 after parity; degree 127 needs delta p_5 = 0 at -30.9 bits | TOY plus Newton PROOF plus extrapolation |
| Fixed-word list route; base-field pencils; Galois-orbit gamma | ~54 bits worse; |W| <= p | PROOF |
| Moment, marginal and character-sample evidence for a heavy fibre | All flat to 1e-36 to 1e-95 | EXACT, but **cannot see a single heavy fibre** (C16 L1547) |

### 4.2 What remains open

1. **The bare heavy-fibre question.** Does U -> (p_1..p_6(U), prod U) on 136-subsets of mu_256 \ {1} mod p have a fibre >= 2^57.93 (C16 L1549; C17 L1614)? There is no proof either way and no search handle at real scale. A 4.01x fibre at u=1024 gives up to 115.46. lamb356's u=2048 corner would need an 11.3x deviation for 114.10. Every proposed mechanism has been priced, and C36's w >= 1 closure counts pins at p^w, so it does not touch this question.
2. **Unenumerated gap-closing pin cells.** First, the N=283 F_{p^2} circle cell: 2.8e13 conjugate-reduced pairs at m = 7528998, about 31 h on dtumad's box (L1503, L1612, L1637). Second, the F_{p^3} Singer cells N=67 (+4.1) and N=469 (+6.9), which only had structured scans (L1151-1152); no enumeration cost is stated for them. GordoAR (L6102) argues the h-coset formulation reduces to a discrete log of a fractional-linear function and is hard; he makes no attempt.
3. **Codeword shapes outside the R*Q(X^u) / rational-pullback ledger**, non-pencil g_2, and certificates that are neither pigeonhole nor low-degree algebraic families (C29 L3880-3884; C30 (iii) L3911; C36 L6044-6050; yoyo's caveats L4044).
4. **Structured collisions among the top pins.** C36 counts them at p^w and does not address non-pigeonhole certificates for w >= 1 (L6050). hybridnoise: one more free condition, or one costing <= 29 bits, at u=1024 is enough (L3486). The thread never found one.
5. **Joint-source recovery with varying leading jets.** The target is three new actual-field root sets on one source with three distinct directions (C20 L1821), and the jets must vary (C22 §2). Even if this works, the family must reach 2^57.93 with affine dimension >= 9 (C22 §3).
6. **Antipodal line:** pin p_5 for less than a full base-field symbol, or prove (p_1,p_3,p_5) classes never far exceed 2^27 (GordoAR L6090-6092).
7. **Lower-track cross-link:** the lower-track thread #568 is referenced (L3796). lamb356's u=2048 corner, if realisable, would refute the lower 115.00 target (L3296).

### 4.3 Most promising direction, as the thread itself says

There is no consensus ranking, and none should be read in.
- dtumad: would not spend more search on the accidental family without a proof (L1167).
- GordoAR: a beat needs at least two fibres per signature, meaning a new mechanism and not a template refit (L6127).
- The only stated quantitative small ask left is hybridnoise's: one condition costing <= 29 bits at u=1024.
- The concrete computations left undone that could close the gap by themselves are dtumad's N=283 census (+6.1 bits) and exhaustive F_{p^3} Singer-cell censuses at N=67 and N=469 (+4.1 and +6.9 bits).

### 4.4 Binary tracks and BitWonka's 106.25

**The thread says nothing about them.** There are zero mentions of binary-reduction-upper/lower, 106.25, or a non-fibration construction (grep of the whole file; the word binary appears only in the 0/1-vector sense). Outside the thread, from header lines only of sibling files in the same directory:
- `pr592.md` (merged 2026-10-20): BitWonka's binary-upper 106.25 at unsafe index 917504 = 7N/16, up from 114.11, built on a pole pair the PR attributes to Dao, Kominers, Thaler and Zheng.
- `pr593.md` (merged 2026-10-20): 106.24 at unsafe index 917441.

These were not digested here.

---

## 5. Reusable research procedures (candidates for a campaign skill)

**Screens and controls**
- **Two-prime screen.** Run any candidate at two primes an order of magnitude apart and treat anything that moves as an artifact (C0 L133-136). Example: the 65-state family has rank saving 2/16 at p=193 and 0/16 at KoalaBear and six other primes (ideal norm 2^18*193^2).
- The converse also holds: **field-independence signals char-0 rigidity, usually a coset family in disguise** (C1 §3).
- **Check the root-of-unity generator against every prime divisor of the order**, e.g. `all(pow(z, order//q, p) != 1 for q in primefactors(order))`. The bug that tests only z^(order/2) != 1 struck three times and produced fake heavy fibres: N(0) = 1414 at three primes, and Var/mean 2172843 with max/mean 480 (L170-174, L954-961).
- **Positive and negative controls on every census:**
  - A=128 coset recovery (L196-197).
  - Planted-pool recovery in the F_{p^2} census (L1148).
  - The <x^3,1> orbit and a planted Dickson pencil for fold censuses (L4441-4460).
  - Mutated states for the joint-source checker (L2522-2530).
  - cap = L-1 / cap = L for branch-and-bound (L5850).
- **Sanity identities:** T(0,0) = C(255,136); |T| = 1 for a=0 and r odd (L67-68); totals Sum_kappa N = C(n,k) exactly (dtumad, everywhere).

**Exact enumeration methods**
- **Decouple the mean from hard:** pick small p with A | p-1 so that bins = p^hard*A stay small while C(A-1,c) is large (L936-938).
- MITM over label halves with `bincount` for exact joint histograms (L891-893). Use FFT over Z_p^h x Z_A when the grid fits.
- **DP mod several 61-bit primes plus CRT**, with totals checked against the binomial (L984). **Length-(p-1) NTT of multiplicative characters with 5-10 CRT primes** for full-resolution pins (L1570). Rader / length-(p-1) cyclic correlation for the additive DFT (L1583).
- Discrete logs are cheap because p-1 = 2^24*127 is smooth (Pohlig-Hellman; L3326).
- **Sampling with full verification:** sample members per bucket, verify any >= 2-member bucket exactly over all labels, and report miss(f,K) = P[Bin(K-1,f) <= 1] (L4397-4420).
- **Moment recurrence for DFS over complements:** m_i(V(Y-z)) = m_{i+1}(V) - z*m_i(V), so V is never formed (L3503-3505). One slice of 141M subsets took 1.08 s on 11 threads.
- Exact branch-and-bound over deficiency count vectors with staircase, squeeze, Cantelli and tilt bounds, re-verified with exact BigUint DP (L5833-5861).
- Store certificates as exact-integer `assert` scripts (jieyilong's style: L1930-2048, L2820-2912).

**Pitfalls they hit**
- Small pilots mislead when the verdict hangs on a standard deviation: a 24-sample pilot was 0.6 bits off (L160-161).
- Small samples inflate gcds. Stripping trailing zeros destroys the Y-power, so track valuations (L1070-1073).
- Never put exact bigint binomials in a search loop; screen with log-gamma and compute exact values only at the corners (L3303).
- An incomplete enumerator for unequal block profiles (L1643).
- u128 overflow in capacity checks (L1912).
- A formal state that has the right coefficients but zero roots in H validates the algebra, not the construction (L1897).
- Labelling errors between N and the coset order h (L6102).
- Double precision in #good is acceptable only with a stated slack (L5524-5527).

**Verification culture**
- Before posting, have a second agent re-implement the computation independently, with different early-exit orders, a CRT-free DP, or fraction-free elimination (dtumad L1004, L1566).
- Use an adversarial referee pass on every proof note. Fable 5.1 caught the threshold error (72 -> 69), the t >= 1 dedup overclaim, the F1 algebraic family and the Cantelli bug (L3913, L4496, L5537, L5849).
- Every comment opens by stating that no score or 116.12 certificate is claimed, and every negative is scoped to the method that produced it. Retract publicly and promptly; the thread contains about 20 corrections (ledger 2.0).
- Ship artifacts: MIT gists with `MANIFEST.sha256` (L1509-1517), source SHA-256 in the comment (L1230, L1927, L2054, L2176), and exact reproduction commands with expected outputs.
- Probe live Lean definitions with `#eval` to locate the binding obligation, for example `OrbitPencil.lean:796` `hagree` (L6127). Read the submission source before treating a ledger term as a cost; the `productKey` term turned out to be a +23-bit gain (L291-301).

**Tooling seen in the thread**
- Sage (joint_root_filter.sage).
- Pure-Python exact checkers.
- C with OpenMP (slice.c) and pthreads (census.c).
- Node.js (yoyo: pencil.mjs, lib.mjs, exact.mjs, bnb.mjs).
- Rust with rayon (B&B).
- Montgomery or __int128 mulmod.

**Model attributions (as each author stated them)**
- dtumad: Claude Fable 5.1 for computation, Opus 5 for write-ups (L1022, L1169).
- hybridnoise: Claude Opus 5.5 (L3450).
- yoyo930021: Opus 5.5 for proofs and code, Fable 5.1 as adversarial referee, Sonnet 5 for toys and implementation (L3915, L4496, L5537).
- GordoAR: qwen3.8-flash-next plus deepseek-v4.1-flash via the Hermes Agent harness (L6094, L6121).
- BitWonka, jieyilong, CrystallineButterfly, lamb356 and raresbuhai give no model line.
- dtumad also mentions an earlier autonomous campaign (Aug 28 - Sep 6, run with GPT 5.6 Sol / Codex) whose Lean artifacts were partly lost (L1008).

---

## 6. Could not determine

1. **The outcome of dtumad's N=283 F_{p^2} circle census.** It was announced as running at L1612 and L1637 and never reported (+6.14 bits). The F_{p^3} Singer cells N=67 and N=469 (+4.1 and +6.9) also lack an exhaustive closure (L1151-1152). These are the only gap-closing pin cells left without one.
2. Whether the heaviest u=1024 key fibre exceeds 2^57.93. Nobody proves or disproves it; C36 does not bound it for w >= 1 (pigeonhole rate).
3. Whether (22') is already in print. BitWonka asks for pointers; Zannier 2012 fn. 12 and Pasten-Wang 2017 are the nearest precedents (L5970-5975). yoyo did not re-derive CZ05 Prop. 2.2 (L5520-5522). The local-CZ form (C29) is self-refereed only.
4. Whether the gcd/dim dichotomy holds at A=256. It was screened only at A <= 32, and BitWonka says the reciprocal-repair closure fails if it fails there (L1450-1453). jieyilong's counterexample is for selected subfamilies with a p-cap.
5. Whether S* / U_3 are true. They are unproved but moot after C36.
6. dtumad's real-prime per-bin extrema and their uniqueness: only aggregate consistency was audited (L1916). yoyo's a=3, n >= 70 runs were not re-run by the referee (L5902). jieyilong's KoalaBear trade census was not rerun by its author (L1214), though dtumad reran it.
7. The meaning of `B = 11410` (lamb356) and `B = 11612` (GordoAR). Inferred as the score in hundredths (114.10 at idx 120833; 116.12 at t = 139782), not stated.
8. Whether the C36 key-free recount and the (22') window closure were independently reproduced. BitWonka says scripts and logs are available on request (L6050); one referee pass covered (22').
9. Whether w=129 and k=7 at u=1024 match the Lean template. yoyo extrapolates them from the formalised u=512 case (L4002).
10. The artifact archive of dtumad's earlier Aug-Sep campaign (Lean files partly lost, L1008; branch `codex/upper-transfer-6732` named at L1505).
11. Anything about the binary tracks or BitWonka's 106.25 binary-upper construction. Absent from this thread; see 4.4.
12. The content of gists and attached artifacts (not fetched). All gist claims above are as stated in the comments.

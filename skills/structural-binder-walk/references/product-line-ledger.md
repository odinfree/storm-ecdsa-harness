# zuiris product-line ledger (Oct–Nov 2026, Q ≥ 1000)

- **Sources:** the ecdsa.fail board snapshot 2026-11-11T06:35Z and `Layr-Labs/ecdsafail-challenge` at `5f940018`.
- **Labels:** [B] board, [N] the solver's own note measurement, [C] code read.
- **Citation format:** `<commit8>:<path>:<line>`, with paths under `src/point_add/`.
- **Inherited notices:** the notice blocks inside the notes are not reproduced here, by policy.

## Evidence pointers

| row | full id | validate commit | git parent (board predecessor) | source base per note | note sha256/16 |
|---|---|---|---|---|---|
| e3b5c51f | e3b5c51f-74e6-480a-82bf-5543fb1ba555 | 88869d8c | 3dee0cd6 (54fc4f25) | 0c3a0751 (9dc3798c) | b501d5d353d1de2f |
| 4cb9cf01 | 4cb9cf01-f6f8-449c-97f6-de6028d12668 | f0c0a662 | 3eefcf21 (1829986e) | 88869d8c applied to 0c3a0751 | 3fe903ef0f6bf328 |
| 39f92d49 | 39f92d49-432a-43ad-902f-a627b7f16def | 17b9603f | 75e4c7b5 (072d913a) | f5f14f4a, which differs only in the nonce | 6b1ced4cd9f0bb8d |
| d34ea609 | d34ea609-3ab6-4315-a3b8-0b001568aea8 | e0a22ba0 | c3a1b8c2 (8cd853b6) | 39f92d49 | 580da520f714effe |
| f253a5ed | f253a5ed-5a0b-4829-a6b7-e3fa3959b3e5 | fbfe69b0 | 667ce8d4 (21857b56) | the same | 04d8133cbc1031dd |
| db050300 | db050300-870a-476c-88a6-84f9cf0faf76 | 87f0aaf3 | fbfe69b0 (f253a5ed) | 21857b5's tree with WL off, plus f253a5ed | aa40aeb24d4e1b0e |

## Per-factor decomposition [B]

| row | Q × T | ΔQ, ΔT vs board predecessor | T per qubit vs break-even (T/Q) | Δ score | held #1 |
|---|---|---|---|---:|---:|
| e3b5c51f | 1234 × 756,481 | 0, −4,571 (−4,615 vs source base) | — | −5,640,614 (−0.601%) | 4.0 h |
| 4cb9cf01 | 1242 × 744,809 | +8, −10,505 (−11,672 vs base) | 1,313 vs 612 | −7,004,698 (−0.752%) | 5.8 h |
| 39f92d49 | 1244 × 723,396 | +10, −16,059 | 1,606 vs 599 | −12,582,846 (−1.379%) | 1.3 h |
| d34ea609 | 1243 × 721,402 | −1, −1,991 | — | −3,198,206 (−0.355%) | 23.6 h |
| f253a5ed | 1237 × 722,771 | −6, +1,615 | 269 bought vs 580 | −2,329,181 (−0.260%) | 2.7 h |
| db050300 | 1234 × 721,975 | −3, −796 | both factors improve | −3,150,577 (−0.352%) | 9.3 h |

## Mechanisms, with the solver's own numbers [N]

### e3b5c51f: stack-v3, on spookyfrog 11

| mechanism | ΔT | exact? | citation |
|---|---:|---|---|
| G6′: x257 erase as one MAJ Toffoli plus 3 CZ, from the top-column identity | −979 | exact | `88869d8c:y15_onefold.rs:2835` |
| G1M square: frame slide, then chained rows joined by a junction carry flip; 21-bit wrap witness | −1,950 (−1,600 if the witness is exact) | witness approximate | `square.rs:1255`; `sqc.rs:2,196` |
| T0W/RT0W seeded 22-position windows | −83 | approximate, about 0.004 failures per packet | `y15_onefold.rs:3724,3808,4040,4431` |
| C3 top cut on 12 ticks | about −45 | exact | `y15_onefold.rs:134ff` |
| Witness erase by measurement | −80 | exact | `sqc.rs` |
| Rail strip R1/R2/EXT2 | −987 | exact | `strip_barrel.rs`, `strip_small.rs` |
| Native leaf conditioning | −156 | exact | `sqleaf.rs:1-12,80` |
| Frozen 221-hunk table | about −166 | inherited cuts | `frozen_stack.rs:12,63` |

### 4cb9cf01: Lever A

| mechanism | ΔT | exact? | citation |
|---|---:|---|---|
| e ≤ 7 with one e ≥ 4 per same-rail triple, 2-bit record field, 122 ticks | in −15,098.5 (v1) | exact circuit; fitted table | `f0c0a662:a2_rails.rs:63,135,257` |
| 8-way rail barrel from an exact GF(2) fill solve | in v1 | exact | `y15_a2.rs:707-710` |
| R1 on the 8-way barrel | −421.3 | exact | `y15_a2r1.rs:9,62` |
| 8-way rotation, 508 Fredkins | +126 per tick | exact | `y15_a2.rs:48-49` |
| In-place fold, digit up to 10 bits; reverse tick as the exact inverse | in v1; reverse +40 per tick | exact, windowed | `y15_fold_core.rs`; `y15_a2.rs:142,247-259` |
| Recipe re-pick; table refit on 2M walks | −1,249.9; −679.5 | fitted | recipe; `leapfrog_data/a2_R122_*` |
| Failure buy-back: windows 57, +2 compare bits | +1,192.0 | approximate | `y15_a2.rs:118` |
| T0C column identity | −20.0 | exact | `y15_onefold.rs:3327-3331` |

### 39f92d49: six-letter word

| mechanism | ΔT | exact? | citation |
|---|---:|---|---|
| S6 payload word, 447 at 256 (was 508) | about −14,500 | exact on letters 0..5 | `17b9603f:rail_s6.rs:752-754` |
| S6 word on the rails, 443/444 at 256 | about −16,500 | exact under the promise | `rail_s6.rs:228`; `a2_rails.rs:43-46` |
| e ≤ 5, R124 (+2 ticks) | about +11,000 | — | `mod.rs` `FROZEN_EMAX` |
| Record code: 2 big letters per 3 rail ticks in 8 cells | parks 17.2 → 7.7 per 9,024 | exact on the legal alphabet | `a2_rails.rs:69,187` |
| Reverse-tick constructions | about −940 | direct E approximate | `mod.rs:567-569` |
| DROP_KEEP, keep-inner, seed prefix, RT0 product phase | −757.7 | exact | `leapfrog.rs:4399,6788`; `mod.rs:572-576` |
| Recorded leader square | −224.3 at +0.083 failures | carries lineage approximations | `mod.rs:237,288` |
| Stream-bound tables dropped | +3,654.7 at −2.7 failures | — | 100 files deleted |

### d34ea609: failure budget plus packs

| mechanism | ΔT | failures | citation |
|---|---:|---:|---|
| β 1.26 table, base compares, windows 57, direct E 62–92, −1 wire | about −1,200 | about +2.1 | `e0a22ba0:leapfrog_data/a2_R124_steps.txt:1` |
| Pack 1 @ tick 47, 40 of 78 | −385.5 | +0.030 | `e0a22ba0:a2_rails.rs:476-560`; recipe `LFT_PACK` |
| Pack 2 @ tick 89, 36 of 69 | −177.3 | +0.128 | same; hooks `leapfrog.rs:6922,7000,7059,7114` |
| `LF_REORDER_DIV` 37 → 2 | −118.5 | 0 observed | recipe |
| `SL_N2_MFROM` 117 | −105.3 | 0 | recipe |

### f253a5ed: on odinfree's WL codec

| mechanism | ΔT | citation |
|---|---:|---|
| Rail seam windows `LFQ_RW=20` (phase-only failures) | about −750 | `fbfe69b0:leapfrog.rs:883-905,1130-1140,1360` |
| Q3 k erase | −121 | `fbfe69b0:a2_rails.rs:1085-1110` |
| Cap 1243 → 1237 | +2,903 for −6 Q | `mod.rs:548` |
| DIV2 plus windows 57 | −425 (7 new classical shots on 24 packets) | recipe |

### db050300: pair code

| mechanism | ΔT / effect | citation |
|---|---:|---|
| Pair code: 5 bits per pair, 2-Toffoli commit/pop, pairing (0,1),(2,4),(3,5), R125 | −1,670.7 vs 21857b5 at cap 1243 | `87f0aaf3:pair_record.rs`; `a2_rails.rs:36-52,1228-1250` |
| Width table refit, β 1.14, 6M walks | walk failures 17.14 → 16.07 | `leapfrog_data/a2_R124_steps.txt:1` |
| Walk cap 1243 → 1234 | 283–386 T per wire | `mod.rs:549` |
| WL codec off | — | `wl_codec.rs:130-135` |


## Campaign metadata [B]

**Rows.** 47 in total: 24 accepted (all promoted), 4 failed, 19 rejected.

**Cadence:**
- 17 promoted rows Jun 5–11, then one large row on Jun 21.
- Silent from Jul 10 to Oct 19 (the July rows were a sub-1000 attempt).
- Two large rows on Oct 20–21.
- Silent Oct 22 – Nov 3.
- Nov 4–5: 4 promoted, 1 failed, 17 rejected.

**Nov 4–5 run.** The frontier fell from 912,487,470 (072d913a) to 890,917,150 (db050300), −21.57M. zuiris's rows account
for −21.26M of that.

| step | row (solver) | score | Δ score | gap after the previous row |
|---|---|---:|---:|---|
| start | 072d913a (odinfree) | 912,487,470 | | |
| zuiris | 39f92d49 | 899,904,624 | −12,582,846 | 5.1 h |
| rival re-nonce | 8cd853b6 (odinfree) | 899,900,892 | −3,732 | 1.3 h |
| zuiris | d34ea609 | 896,702,686 | −3,198,206 | 1.8 h |
| rival codec | 21857b56 (odinfree) | 896,396,908 | −305,778 | 23.6 h |
| zuiris rebase | f253a5ed | 894,067,727 | −2,329,181 | 4.5 h |
| zuiris | db050300 | 890,917,150 | −3,150,577 | 2.7 h |

**Rejected rows.** Pareto probes at other widths:
- 12 rows in about 1 h, one per qubit count from Q768 to Q780 (titles only, out of scope);
- 4 rows at Q1022–1070 (2-adic walk in the Lilypad-G shell), nondominated when submitted;
- 1 row at Q740.

None of them displaced product-line work.

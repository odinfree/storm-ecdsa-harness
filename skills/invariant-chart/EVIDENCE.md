# Evidence: invariant-chart

Sources and conventions as in beachhead-ratchet/EVIDENCE.md ([V] = read in his source, in a scratch clone of his commits).

| chart | evidence |
|---|---|
| residue chart mod 4 (Q795 -> Q794, c4c2c938 / 84233955, +38% T) | report-leftmoves row Q794: Work1 = 257 + 2 markers, `q794_lifecycle.rs:15, :111` [V]; the algebra (t r + u v + q t v = p, p = 3 mod 4) is his statement |
| residue chart mod 8 (Q794 -> Q793, 52694f13 / 76de23d8, +44%) | report-leftmoves row Q793: Work1 = 256 + 3, assertion over [256, 257, 258], `q793_lifecycle_r03.rs:15, :111`, `q793_loans.rs:2` [V] |
| sum-domain code E = Y - 1, S = Z + Y - 226, 16 -> 12 owners, 4,096 words valid | report-source "E/S registers": `sum_size.rs:3-7, 33-47` [V]; report-leftmoves row Q660 |
| Q666 five-bit code on 231 <= Z + Y <= 257: the inherited domain at completed post-stage-2 boundaries (notes.md:10821), not proven for every input | report-descent770 Q666: `shared_size.rs:1-16` @2248d26e [V] |
| predicates as MAJ-carry tapes with costed comments (20 CCX, 18 CCX) | report-source: `direct_size_predicates.rs:30-34, :42-44` [V] |
| one-hole payload: PRE omits hole 257 - bl(t); POST normalizes P[bl(r)] and omits it; PH lent as logical P[258] through digit/transition, returned before phase/activity readers | report-source "Proved-zero lanes": `d461761e:src/point_add/payload/splice258.rs:3-11, :22`, `direct_payload.rs:9-11` [V] |
| virtual odd-divisor bit and zero-prefix decoder (Q770 4f55785a) | report-source pattern 7: `virtual_odd.rs:1-18`, `head_product_care.rs:1-20`, `frogdrop.rs:1034-1078` [V]; report-leftmoves row Q770 |
| lockstep tie cut: pool constant 21 -> 19 -> 18 -> 17 (a cut of 2, then 1, then 1) with 2/3/4 consumed multiplier bits; three left moves in about six hours | report-leftmoves rows Q772/771/770 (`frogdrop_col.rs:87-89`, `pointadd_frogdrop.rs:339`, field_consume_second/third/fourth.rs) [V] |
| capsule harness: forward-then-inverse replay, phase check, omitted rails asserted untouched | report-source pattern 8: `q793_t10_full_check_v13.rs` [V] (capsules not shipped) |
| baked admission: BAKED_KNOBS, SOURCE_AND_COST_ADMITTED: bool = true | report-source "Knob selection" and "Stale headers": `mod.rs:101-141`, `direct_traversal.rs:34`, `splice258.rs:25` [V] |

Limits: the mod-4 and mod-8 algebra was not re-derived; absolute pool lane counts are not verified (only the constant
deltas); nothing was rebuilt.

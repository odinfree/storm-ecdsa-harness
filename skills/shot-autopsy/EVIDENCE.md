# Evidence: shot-autopsy

Sources and conventions as in beachhead-ratchet/EVIDENCE.md.

| claim | evidence |
|---|---|
| nonce inherited literally every time: 4 (frogdrop), CX(5,274), CX(5,24), CX(5,387), CX(5,2) | report-ops "Nonce": notes.md:9008, 10607, 10676, 10637, 10835; `de464c21:src/point_add/mod.rs:94-96` NONCE=2, NONCE_CTRL=Some(5) [V] |
| any stream edit changes the validation population; the base's nonce certifies nothing | report-ops "Nonce": ed89218e notes.md:1776-1779; June 61451098 notes.md:26-34 (dead gates appeared inactive on 512 sampled shots; the modified stream failed after reseeding, notes.md:34) |
| failing shots repaired, kept as regressions: Q772 7926; Q770 614, 5732, 7689; Q660 63, 4543, 5284; set 256 -> 320 cases | report-leftmoves "Validation"; report-descent770 "Entry" and pattern 2: notes.md:9483-9598, 10063-10067, 10076 |
| pay precision, never trade error: head 24 -> 25 (fa250a1d notes.md:10833), crossing head 32 / QB30 (d181b19f notes.md:10902), window 32 -> 33 (e58ee040 notes.md:10970); "spends no error budget to reduce score" (13ba6c73 notes.md:9012) | report-ops "Lambda and the limiting contract" |
| 45-minute runner wall: benchmark.yml timeout-minutes 45; timeouts at 2.25, 2.21, 2.23, 2.06 B ops; landed at 2.03, 1.90, 1.94 B | report-leftmoves pattern 4 [V benchmark.yml]; report-descent792 "Origin" |
| op diet techniques: XOR-cube tables, template cache, bulk append, per-step cancellation, ESOP metadata; global_cancel window 4,096 | report-leftmoves pattern 4; report-source "Byte-identical rebuilds" (`builder.rs:174, 260-280`) [V] |
| pins: CANDIDATE_OPS = 1_902_227_679, CANDIDATE_TOFFOLI = 1_124_860_100, peak == 793, < 128 GB asserted at build end | report-source: `q793_lifecycle_r03.rs:209-210`, `trailmix_port/mod.rs:4404-4411` [V] |
| note as a record: exact sum / 9,024, emitted vs executed, parent id + commit, three SHA256s, negative claims | report-ops "Note template, evidence style" |

Limits: his root-cause method is stated in notes, not reproducible from the tree (native suites and capsules are not
shipped); the exact remote op wall varies (2.035 B passed, 2.055 B failed).

| exact transformations on an inherited approximate circuit (not exact lanes) | notes.md:9008-9012 (approximations retained), 10065 (universal arithmetic disclaimed), 11018 (historical modeled lambda 2.52 kept) |

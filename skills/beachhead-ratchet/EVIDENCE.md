# Evidence: beachhead-ratchet

Source data: an ecdsa.fail API snapshot of 25 Oct 2026 (81 bulengerk submissions, 74 validated; 9 left moves and 61
down moves at submission time, computed against the frontier as it stood). Every claim rests on his public submission
notes: "notes.md:N" is line N of his 81 notes concatenated in submission order (fetch them with `ecdsafail
submissions`), and submission ids identify each row. The `report-*` names refer to our working reports, which are not
published. Most rows also give the public note line or submission id they rest on; the rest summarize his notes
as a whole. [V] = checked in his source code;
otherwise his own statement.

| claim | evidence |
|---|---|
| Q770 beachhead: 774 -> 772 -> 771 -> 770 at +20.4%, +10.8%, +22.2%; 186.6M -> 304,134,670 (+63%); stated target 300,000,000 T with an explicitly permitted overrun of 1.37822% | report-descent770 "Entry"; notes.md:9080, 9234, 9405, 9410-9414; rows c9089985, b2b994fd, 4f55785a |
| 13 down rows to 115,382,810 (-62%) in ~31 h; 62% of the cut recovered the purchase overhead; half the cut in the first three rows (11.6 h) | report-descent770 "Why so fast" 1; submissions.json |
| Q792: landed +31% (959.7M -> 1,257.8M); 38 rows in all (37 reductions after the landing row) to 574,285,626 (-54.3%) | report-leftmoves table; report-descent792 scope and row table |
| Q794 / Q793 landed at +38% / +44%, then 5c42a5be -17.5% at +2.7 h | report-leftmoves table and pattern 6 |
| misses consistent with no frontier re-read: 13ba6c73 (Q774) and 38e6918e (Q695) landed after a better rival row | submission timestamps on the board |
| invoice model within ~100 T: 196,250,688 vs 196,250,710 measured | report-descent770 pattern 3; notes.md:10019 |
| gates: ">= 5% below that parent's executed cost" (d181b19f notes.md:10888); "10 x new_sum <= 9 x baseline_sum" (9a8bbcae notes.md:11034); the user's "strict four-percent threshold" on the final Q792 row (notes.md:8847-8850; the penultimate reduction was 3.51%); ">= 5%" (notes.md:9739) vs strictly "> 5%" (notes.md:10021) on Q770 rows | report-ops "Cadence"; report-descent792 cadence D |
| Q770 carry-row ladder (5-9% per multi-change row, not per isolated kernel): row_add.rs:55, frogdrop.rs:1456, row_add.rs:223, signed_batch.rs:4 | report-descent770 pattern 5 [V] |
| 13-line diff for -9.63% (d8e2a8d4) because overlays keep call signatures | report-descent770 rows; notes.md:9941 |
| pins in source: CANDIDATE_TOFFOLI 670139450 -> 656602578 in q792_lifecycle_r01.rs | report-descent792 "Ordering" [V] |
| submit-while-validating on a frozen parent; "score did not improve" as the correctness proxy (22 notes) | report-ops "Cadence and pipeline", "Bases and credit" |
| re-absorb: nasqret's 39227bab = his row-10 tree + 8 edited files; row 11 re-imported 5 byte-identical, beat nasqret by 4.1% within 5 h | report-descent792 "Keeping the leftmost point" [V] |
| left Q792 for gnuchev's frogdrop tree the same day the 776-774 band opened (9 Oct) | report-descent792; notes.md:8970-8974 |

Limits: lambda of his rows is not exposed by the board; the percent gates may be the user's or the model's choice; the
per-lever split inside multi-change rows is his own invoice.

- Left moves that raised T: seven of nine (Q665 and Q660 lowered T: report-leftmoves rows Q665, Q660). Observed increases about +11% to +122%.

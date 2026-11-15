# Determinism map: <benchmark>, evaluator commit <sha>

Fill one row per random draw the evaluator makes, in the order it makes them. The map is complete when the last
section can be answered for any unit of work.

## Seed

| item | value | file:line |
|---|---|---|
| Hash or generator | <e.g. SHAKE256, one stream> | |
| Domain tag absorbed first | | |
| What is absorbed (artefact bytes, length, salt, external seed) | | |
| Serialisation of one record as absorbed | | |

## Draws

| # | draw | source stream | order | bytes per draw | amount depends on execution? | offset formula | file:line |
|---|---|---|---|---|---|---|---|
| 1 | test inputs | | first | | no | 0 .. | |
| 2 | <e.g. measurement outcomes> | | per batch, per op, in op order | | yes / no | | |
| 3 | | | | | | | |

## Unit of work

| item | value |
|---|---|
| Unit (sample, batch of samples, transaction, proof) | |
| Samples per unit, and size of the last partial unit | |
| Offset of unit b's randomness | |
| State carried from unit b to unit b+1 (must be none for parallel units) | |

## Verdict

- [ ] Every draw has an offset that does not depend on what executed. An exact parallel replica is available.
- [ ] At least one draw depends on execution: <which>. Exact parallel replica not available; serial compact replica
      or calibrated proxy instead.

## Files whose change invalidates the replica

| file | last change (commit, date) |
|---|---|
| | |

## Golden logs

| artefact (hash or submission id) | judge value | replica value | replica code version | date |
|---|---|---|---|---|
| | | | | |

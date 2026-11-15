# Schnitzmässer (whittling knife)

Technical id: `mk_bcuts.sh`, generalized as `port-hunks.sh`.

Carries a set of cuts from the tree they were written for onto a different frame, keeps the hunks that still
apply, and reports the ones that do not. We used it when a batch of exact adder cuts, written against one
764-wide tree, had to be priced on the newer frame our 763, 762 and 761 rows were built on: five of seven
hunks applied, one was replaced by a hand port, one had no counterpart because the new frame had its own
lever at that line.

## Run

```bash
bash port-hunks.sh trees/row762 trees/row762_cuts cuts.patch 0 src/point_add/mod.rs
bash ../erbsezaehler/cnt.sh trees/row762_cuts row762_cuts      # price it
```

Output: what `patch` reports per file and hunk, the summary line `hunks: 5 applied, 2 rejected of 7`, the new
tree, and `<dst>.rejects/` with `patch.log` and the rejected hunks.

The script runs `patch` with no fuzz (`-F0`). With the default fuzz, Apple's `patch` 2.0 accepted a hunk in our
test whose removed line did not match the file, and replaced the line anyway. Set `FUZZ=2` only if you then
read every applied hunk. The campaign's own script ran `patch` with its default fuzz; its output was used for
pricing only.

## Limits

The tool prices a port. A hunk that applies textually can still be wrong on the new frame: the surrounding
invariant may have changed. On the campaign the ported cuts came out under the threshold we had set for a row of its own and were
parked without a gate. Before any ported hunk ships, it goes through the same paired gate as a new lever, and the author of
the cut is credited in the note.

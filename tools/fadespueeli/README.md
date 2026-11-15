# Fadespüeli (thread spool)

Technical ids: `align.py`, `gl.py`.

Tools for gate lists: long, fixed sequences of X, CX and CCX gates that a circuit ships as data and replays,
in the zstd-compressed `GLV1` format in which the public rows of Akashneelesh's Q765 line ship their end
machines.

- `gl.py stat <list.glz> [TOP]` prints sizes, gate kinds, the highest lane, untouched lanes, and for the
  eight widths below `TOP` how many gates touch a lane at or above that width, with first and last index.
  That last table says at a glance what stands between a list and a narrower row.
- `gl.py replay <ref.glz> <new.glz> <shots> <seed> [NL]` runs two lists on the same random inputs, bit-sliced
  over `<shots>` shots, and reports on how many shots any lane differs.
- `align.py OLD.glz NEW.glz [K] [MIN]` finds the runs of NEW that occur verbatim in OLD, by exact K-gate
  windows. We used it to find where a block we had registered in one list (a measured-erase region) sits in
  the list of a neighbouring width.

```bash
python3 gl.py stat start_763.glz 765
python3 align.py start_763.glz start_762.glz 48 2000
python3 gl.py replay start_ref.glz start_new.glz 4096 1
```

Output of `align.py`: one line per matched segment of at least MIN gates (`new [a, b) = old [c, d)  n gates,
m CCX`) and a totals line.

## Limits

`replay` compares values only: it has no phase tracking and no measurement semantics, and its input layout
is fixed in the code. A clean replay is necessary. Only the evaluator decides. `align.py`
hashes exact windows, so one changed gate splits a segment. Needs `python3` and the `zstd` binary.

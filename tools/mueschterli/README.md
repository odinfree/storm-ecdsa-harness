# Müschterli (little sample)

Technical id: `mk_fv3.py` (and its siblings `mk_b763.py`, `mk_ctl.py`), generalized as `recipe.py`.

Makes a probe tree from a source tree and a recipe file. Each lane of the campaign needed a handful of trees
that differ from a base in a few constants and data files: the row candidate, the same tree with one lever
off, a control. Each tree was made by a short script of exact text replacements that asserted every pattern
occurred exactly once. This is that script with the tree-specific content taken out and put into a JSON file.

## Run

```bash
python3 recipe.py trees/base trees/probe_a example-recipe.json NONCE=85 LEVER_X=false
bash ../erbsezaehler/cnt.sh trees/probe_a probe_a
```

Output: the new tree at DST, and a manifest line (`sha256  path`) for every file the recipe touched. Keep
the manifest with the measurement: it is what binds a number to the tree that produced it.

## Why not sed

A replacement that matches nothing leaves the base tree under the probe's name. A replacement that matches
twice edits a place nobody looked at. Either way the number that comes back is believed. The recipe stops
instead, and names the edit and the count.

## Limits

Text edits only; the recipe does not know Rust. A control tree needs its own target directory or a fresh
build (see Erbsezähler). The campaign's own recipes are not included: they encode list offsets and hashes of
specific rows and are of no use on another tree.

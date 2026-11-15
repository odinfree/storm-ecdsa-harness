# Erbsezähler (pea counter)

Technical ids: `cnt.sh`, `qcount.rs`.

A count-only build of an ecdsa.fail tree. It answers "what does this edit do to the Toffoli count and the
width" in under a minute and about 2 GB, where the full build of a low-Q row takes tens of gigabytes. We ran
it dozens of times per lane to price levers before spending a cloud runtime on a gate.

`qcount.rs` is a 33-line independent width check: it reads an `ops.bin` and counts distinct qubit ids
without using the evaluator's loader. A width claim holds when the evaluator's qubit count, `distinct_q` and
`max_id + 1` all agree.

## Inputs and outputs

`cnt.sh <tree-dir> <name> [VAR=value ...]`; environment in the script header. Output directory
`$OUT/cnt_<name>/`: `cargo.log`, `build.out`, `build.err`, `rc`, `bc.sha` (sha256 of the built binary),
`pre.sha` (sha256 of the stream), `qcount.txt`. It prints the binary hash, the exit code, peak memory, the
matching build-log lines, the stream hash and the qcount line.

```bash
bash cnt.sh trees/control ctl
bash cnt.sh trees/candidate cand LEVER_X=0     # with one development override in the builder's environment
diff out/cnt_ctl/bc.sha out/cnt_cand/bc.sha && echo "SAME BINARY: this is not a comparison"
```

## The mistake this script carries a guard for

Twice in two days a shared cargo target directory made two different trees run one binary.

- 13 Nov 2026: three trees were counted one after another into one target directory. The work copies kept
  their old file times (`rsync -a`), cargo saw nothing newer than its last build, and all three runs
  executed the first binary.
- 14 Nov 2026: a patched tree and its unpatched control were built into one target directory. The control
  run executed the patched binary. Both counts came out identical to the digit (136,170,862), and we told
  the lane that wrote the cut that it was a no-op on our tree. They doubted the control. Rebuilt with
  separate target directories, the unpatched tree gave 140,259,176: the cut was worth 4,088,314 Toffoli.

So: one target directory per name is the default; every source file is touched after the copy; and the
script prints the sha256 of the binary it ran. Two runs that should differ and show the same binary hash are
the same program. Identical streams from a patched and an unpatched tree are evidence of a build fault
before they are evidence of a no-op. The `rust-archive-build-binding` skill has the full discipline.

## Limits

A count is not a gate: it runs no shots and says nothing about correctness. This generic form of `cnt.sh` was
syntax-checked and not rerun on a tree; the campaign ran the version with our paths in it. `STREAM_VAR` must name a
streaming switch that your tree has; with `STREAM_VAR=none` the script runs the tree's normal,
full-memory build. Needs `cargo` with the tree's pinned toolchain, `rsync`, `shasum`.

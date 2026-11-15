# Brotofe (bread oven)

Technical ids: `zjob.sh` (the batch runner, here `vm-batch.sh`) and `zk.sh` (the per-row script, described
below and not included).

Bakes a tray of rows on a rented VM. `vm-batch.sh` installs the toolchain, runs one per-row script for every
line of a spec file with `xargs -P`, packs the results every two minutes, and writes a summary.

## Run

```bash
colab-lane -n ladder-a -g A100 -m -t 150 -u base.tgz -u row.sh -u vm-batch.sh -u spec.txt \
  -d /content/batch-out.tgz -- 'ROW=/content/row.sh PAR=1 bash /content/vm-batch.sh; cat /content/out/SUMMARY.txt'
```

Output on the VM: `out/<job>/RESULT` and logs per row, `out/SUMMARY.txt`, `batch-out.tgz`, `DONE`.

## The per-row pipeline we ran (stage A, then stage B)

Our rows were one tree with one constant K changed (K extra always-zero wires for an exact hold pass), so
the row script was specific to that tree. Its shape carries over:

- **Stage A, find a clean nonce cheaply.** Build once at the default nonce. Check the width with qcount and
  stop on a mismatch. Scan every nonce target with the tree's own classical predictor on the finished stream
  (no rebuild), then for at most four predicted-clean targets: retarget the stream, hash it, and score it
  with the exact evaluator on the grader's shots. Write `RESULT` = target, candidate sha256, average.
- **Stage B, prove the source builds that stream.** Bake the chosen nonce into the source, build the official
  way under an empty environment, and require the sha256 to equal stage A's candidate. Then qcount and the
  exact evaluator again. Only a `SHA_MATCH` row is packaged.
- Every stage writes the hashes of the binaries it ran and the exact evaluator command line, and deletes the
  stream when done: a VM disk fills after three or four rows of a billion ops.

The split matters because a nonce scan on a finished stream costs minutes, while each official-style build
of such a row cost us about 50 GB of RAM and most of an hour.

## Limits

Size `PAR` by memory: twelve cores still fit only one 50 GB build. The two-minute pack is what saves a batch when the runtime hits its time
limit: on the campaign most jobs ran under `-t 150` or less, and one gate probably ran out of its 90 minutes
before its last stage. We syntax-checked this generic runner and did not rerun it on a VM. A row script must be idempotent per job directory. `xargs -L1` splits a spec line on spaces: no spaces
inside an argument.

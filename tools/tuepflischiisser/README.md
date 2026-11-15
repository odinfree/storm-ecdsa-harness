# Tüpflischiisser (nitpicker; literally the one who dots every i, said less politely)

Technical ids: `verify-server.sh`, `vq-put.sh`.

A second verifier that does not trust the builder. It runs on a rented high-memory VM, takes finished rows
from a queue and, for each one, rebuilds the circuit from the row's source archive the way the official
grader does (`cargo build --release --locked`, then `build_circuit` under an empty environment), compares
the sha256 of the resulting `ops.bin` with the one the builder claimed, counts qubit ids independently, and
scores that same file with fasteval on the grader's own shots. A row goes to submission only when the hash
matches to the last digit and the shots are clean.

## Inputs

Queue files in `/content/q/` on the VM (`/content` is the Colab VM's working directory), per row:
`row<W>.tree.tgz`, `row<W>.sha`, `row<W>.ready` (uploaded last). `/content/fe.tgz` must hold `fasteval.rs`
and `qcount.rs`. `fasteval.rs` is BitWonka's tool (github.com/BitWonka/ecdsafail-tools, no licence file, so
it is not bundled here; fetch it yourself). `qcount.rs` is in `tools/erbsezaehler`.

Environment: `IDLE_MIN` (leave after this many idle minutes, default 45), `FE_THREADS`, `TC` (Rust toolchain,
default 1.93.0), `SHOW_CONSTS`, `GREP_LINES`. A file `/content/q/STOP` ends the server when the queue is empty.

## Outputs

One line per event on stdout: `VERIFY W=.. sha=.. MATCH|MISMATCH`, `QCOUNT W=..`, `FEVAL W=.. failing=..
avg_toffoli=..`, `ROWFAIL W=..`. Logs per row under `/content/vres/w<W>/`, packed into
`/content/verify-results.tgz` after every row.

## Run

```bash
tar czf fe.tgz fasteval.rs qcount.rs
colab-lane -n verify1 -g A100 -m -t 480 -u fe.tgz -u verify-server.sh -d /content/verify-results.tgz -- 'bash /content/verify-server.sh'
VQ_SESSION=verify1 VQ_CONFIG=/path/to/state bash vq-put.sh 742 row742.tree.tgz <sha256>
```

## Sizing, as measured in November 2026

The official-style build of a 740-wide row peaked near 53 GB, fasteval near 23 GB. The server never runs two
evaluations at once and refuses to start below 75 GB RAM. One build is in flight while the previous row's
evaluation finishes.

## Limits

fasteval is an exact replica of the official evaluator, checked by differential tests, but the official
grader is still the only authority. The server's line formats are parsed by Notizbüechli-style note writers;
change them in both places. Not rerun in this generic form.

# Wätterfrosch (weather frog)

Technical ids: `board-refresh.sh`, `board-age.sh`.

A weather frog sits in a jar and climbs the ladder when the weather turns. This one reads the whole ecdsa.fail
board every ten minutes and keeps a six-column snapshot that other scripts and agents can read without
touching the platform: qubits, Toffoli, status, user, id, creation time. It leaves the note text out, so a
lane cannot copy another solver's note into its own by accident.

## Inputs and outputs

`board-refresh.sh <outdir> [seconds]` loops forever and writes `board-latest.tsv`, `board-latest.time`,
`board-latest.json`, `board-latest.err` and `board-latest.heartbeat` into `<outdir>`.
`board-age.sh <outdir> [max_seconds]` exits 0 only when the last good read is fresh.

## Run

```bash
nohup bash board-refresh.sh work/ 600 > /dev/null 2>&1 &
bash board-age.sh work/ 1800 && awk -F'\t' '$1 <= 763' work/board-latest.tsv | sort -t$'\t' -k2,2n | head -3
```

## The frog can freeze

During the campaign the refresher stopped at 10:02 UTC on 14 Nov and nobody noticed for eleven hours: the
snapshot file was still there and still looked like a board. This version adds three things: a time limit on
each read, a heartbeat file written every cycle whether or not the read worked,
and `board-age.sh`. A fresh heartbeat with an old `board-latest.time` means the reads are failing; an old
heartbeat means the loop is dead. Use Äugli for a one-off read of your own when the frog lags.

Needs the `ecdsafail` CLI signed in, and `python3`.

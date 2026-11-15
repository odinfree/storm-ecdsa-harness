# Äugli (little eye)

Technical id: `board-own.sh`.

One read of the ecdsa.fail board, on demand, into a lane's own folder. Same six columns as Wätterfrosch's
snapshot, no note text, the raw JSON deleted after the read. A lane uses it when the shared refresher lags
or has frozen, and before it writes a bar into a note.

```bash
bash board-own.sh mylane/ && head -3 mylane/board-own.tsv
```

Exit 1 when the read fails, 3 when it parses to fewer than `MIN_ROWS` (default 100) graded rows; in both
cases the previous snapshot stays. Needs the `ecdsafail` CLI signed in, and `python3`.

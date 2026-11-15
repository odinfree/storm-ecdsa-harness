# Gwüssesbiss (pang of conscience)

Technical id: `macgate2.sh`.

The full gate for one candidate row on a workstation, for the nights when no cloud runtime can be had. It is
the pang of conscience before a submission: everything the official grader will do, plus what it will not.

1. Build the candidate the official way (`env -i`) at the first nonce in the list; record the sha256 of
   `ops.bin` and the independent qubit count.
2. Score it with fasteval on the grader's own shots. If any shot fails, change the nonce constant, rebuild,
   try the next nonce.
3. On a clean draw: run the stock `eval_circuit` on the same file, then eight salted suites (fresh inputs,
   to estimate the true failure rate).
4. Build the parent row once and run candidate and parent on identical salted inputs, listing the failing
   shots of each. A shot that fails only in the candidate is a defect to explain before submitting.

## Inputs and outputs

`macgate2.sh <tree> <outdir> ["nonce order"]`; environment in the script header (`FE_SRC`, `PARENT_TREE`,
`PAIRED`, `NONCE_FILE`, `NONCE_CONST`, `HEAVY_LOCK`, memory limits). Output: `<outdir>/GATE.txt` (one `GATE`
line per step), `<outdir>/logs/`, the picked tree as `tree_pick.tgz`, and the clean `ops.bin`. Exit codes:
2 cargo, 3 build, 4 no clean draw.

```bash
FE_SRC=$HOME/fe PARENT_TREE=trees/parent bash macgate2.sh trees/cand gate763 "1 0 2"
grep -E 'pick=|stock|PAIRED' gate763/GATE.txt
```

## Memory guards

The script was written the day a 48 GB machine went down three times under ten to sixteen parallel
full-memory builds. It therefore takes a machine-wide lock for every heavy step,
waits until free memory is at least `MIN_FREE` percent and no other process exceeds `MAX_OTHER_KB`, kills
its own build above `KILL_RSS_KB`, and kills it when system free memory falls under 15 percent. A lock whose
holder has died is removed. The cached parent build is tied to one parent tree (`PARDIR/PARENT`).

## Limits

- macOS only as written (`memory_pressure`, `time -l`, `sed -i ''`).
- fasteval and the paired evaluator are not bundled: fasteval is BitWonka's tool without a licence file, and
  our paired evaluator links against the tree's own simulator. Any evaluator that runs both streams on the
  same salted inputs and lists failing shots serves; `PAIRED=0` stops after the salted suites.
- Salted results are estimates, never official scores.
- Not rerun in this generic form.

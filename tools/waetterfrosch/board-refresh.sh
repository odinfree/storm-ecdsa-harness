#!/bin/bash
# Wätterfrosch (board-refresh.sh): keep a small, note-free snapshot of the ecdsa.fail board current.
#
#   board-refresh.sh <outdir> [seconds=600]
#
# Writes <outdir>/board-latest.tsv (one graded row per line: qubits, toffoli, status, user, id, created; NO note text),
# <outdir>/board-latest.time (UTC time of the last GOOD read) and <outdir>/board-latest.json (the full read, overwritten).
# Readers use the .tsv: the JSON carries other solvers' note text, which must not be copied into your own notes.
# A read that fails, or returns fewer than MIN_ROWS graded rows (default 100), leaves the previous snapshot in place,
# so ALWAYS check the age of board-latest.time before trusting the snapshot (see board-age.sh).
R=$(mkdir -p "${1:?outdir}" && cd "$1" && pwd) || exit 1; P=${2:-600}
cd "${TMPDIR:-/tmp}" || exit 1
while :; do
  # a hung CLI call must not stop the loop: bound every read (perl alarm works on stock macOS and Linux)
  if perl -e 'alarm shift; exec @ARGV' "${READ_TIMEOUT:-300}" ecdsafail submissions --all --json > "$R/board-latest.json.tmp" 2> "$R/board-latest.err"; then
    if MIN_ROWS=${MIN_ROWS:-100} python3 -I - "$R/board-latest.json.tmp" > "$R/board-latest.tsv.tmp" <<'PY'
import json, os, sys
d = json.load(open(sys.argv[1])); rows = d['submissions'] if isinstance(d, dict) else d
out = []
for r in rows:
    m = r.get('officialMetrics') or {}
    if m.get('qubits') is None or m.get('toffoli') is None: continue
    out.append((m['qubits'], m['toffoli'], r.get('status', ''), r.get('solverUsername', ''), r['id'], r.get('createdAt', '')))
if len(out) < int(os.environ['MIN_ROWS']): sys.exit(3)
out.sort()
print('qubits\ttoffoli\tstatus\tuser\tid\tcreated')
for o in out: print('\t'.join(str(x) for x in o))
PY
    then
      mv "$R/board-latest.json.tmp" "$R/board-latest.json"; mv "$R/board-latest.tsv.tmp" "$R/board-latest.tsv"; date -u +%FT%TZ > "$R/board-latest.time"
    fi
  fi
  date -u +%FT%TZ > "$R/board-latest.heartbeat"
  sleep "$P"
done

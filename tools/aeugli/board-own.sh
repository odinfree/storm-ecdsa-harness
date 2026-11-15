#!/bin/bash
# Äugli (board-own.sh): one read-only board read into <outdir>/board-own.tsv and board-own.time
# (same columns as Wätterfrosch's snapshot; the full JSON, with other solvers' note text, is deleted).
#   board-own.sh <outdir>
Z=$(mkdir -p "${1:?outdir}" && cd "$1" && pwd) || exit 1; cd "${TMPDIR:-/tmp}" || exit 1
ecdsafail submissions --all --json > "$Z/.board.json.tmp" 2> "$Z/.board.err" || { echo "read failed"; exit 1; }
MIN_ROWS=${MIN_ROWS:-100} python3 -I - "$Z/.board.json.tmp" > "$Z/board-own.tsv.tmp" <<'PY' || { echo "read too small or unparsable"; exit 3; }
import json, os, sys
d = json.load(open(sys.argv[1])); rows = d['submissions'] if isinstance(d, dict) else d
out = []
for r in rows:
    m = r.get('officialMetrics') or {}
    if m.get('qubits') is None or m.get('toffoli') is None: continue
    out.append((m['qubits'], m['toffoli'], r.get('status', ''), r.get('solverUsername', ''), r['id'], r.get('createdAt', '')))
if len(out) < int(os.environ['MIN_ROWS']): sys.exit(3)
out.sort(); print('qubits\ttoffoli\tstatus\tuser\tid\tcreated')
for o in out: print('\t'.join(str(x) for x in o))
PY
mv "$Z/board-own.tsv.tmp" "$Z/board-own.tsv"; date -u +%FT%TZ > "$Z/board-own.time"; rm -f "$Z/.board.json.tmp"
echo "board read at $(cat "$Z/board-own.time"): $(($(wc -l < "$Z/board-own.tsv") - 1)) graded rows"

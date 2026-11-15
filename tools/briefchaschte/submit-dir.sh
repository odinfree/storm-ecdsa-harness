#!/bin/bash
# Briefchaschte (submit-dir.sh): submit one prepared row package to ecdsa.fail, or refuse and say why.
#
#   submit-dir.sh <pkgdir> <W> <account-label> <expected-username>
#
# <pkgdir> holds: NOTE-<W>.md, deps-<W>.json, CLAIM (toffoli=<int> / sha=<ops sha256> / dev=<dev commit>),
#   approved (note=<sha256> deps=<sha256> commit=<sha1> tree=<git tree> model=<model line>), verified-sha,
#   row.commit, row.repo (path of the git checkout to submit from), MODEL (one line), optional row.branch
#   (default row<W>) and HARNESS (one line, default "Claude Code").
# environment:
#   ACCOUNTS_DIR   required: one subdirectory per account label holding that account's saved CLI login
#                  (it becomes YUKON_CONFIG_DIR). A file NOTE_SENTENCE there, when present, must occur in the note.
#   CLAIM_MAILBOX  shared claims file for the Türhüeter gate; IGNORE_CLAIMS=1 skips the gate
#   DRYRUN=1       run every guard, then stop before the submit
# Run the real submit under a lock shared by all lanes, for example: flock -n "$SUBMIT_LOCK" submit-dir.sh ...
set -euo pipefail
die() { echo "REFUSED: $*" >&2; exit 1; }
HERE=$(cd "$(dirname "$0")" && pwd)
D=${1:-}; W=${2:-}; A=${3:-}; WANT=${4:-}
case "$W" in ''|*[!0-9]*) die "width must be a positive integer" ;; esac
[ -d "$D" ] || die "no package dir"
D=$(cd "$D" && pwd)
[ -n "$A" ] && [ -n "$WANT" ] || die "usage: submit-dir.sh <pkgdir> <W> <account-label> <expected-username>"
NOTE=$D/NOTE-${W}.md; DEPS=$D/deps-${W}.json
[ -s "$D/MODEL" ] || die "missing MODEL file (one line: the --model credit, naming every model that contributed)"
MODEL=$(head -1 "$D/MODEL"); BR=$(cat "$D/row.branch" 2>/dev/null || echo "row$W")
for f in "$NOTE" "$DEPS" "$D/row.commit" "$D/verified-sha" "$D/CLAIM" "$D/approved"; do [ -f "$f" ] || die "missing $f"; done
grep -qx "model=$MODEL" "$D/approved" || die "MODEL differs from the approved revision"
# never inherit another session's credentials or endpoint
unset ECDSAFAIL_API_TOKEN YUKON_API_TOKEN ECDSAFAIL_API_URL YUKON_API_URL ECDSAFAIL_BENCHMARK_REF
export YUKON_CONFIG_DIR="${ACCOUNTS_DIR:?set ACCOUNTS_DIR}/$A"
[ -d "$YUKON_CONFIG_DIR" ] || die "no saved login for account label $A"
if [ "${IGNORE_CLAIMS:-0}" != 1 ]; then
  python3 "${CLAIM_GATE:-$HERE/../tuerhueter/claim-gate.py}" "$WANT" >&2 || die "another lane holds an open CLAIM on $WANT (or the mailbox is unreadable); wait for its SUBMITTED"
fi
MYT=$(sed -n 's/^toffoli=//p' "$D/CLAIM"); SHA=$(sed -n 's/^sha=//p' "$D/CLAIM")
case "$MYT" in ''|*[!0-9]*) die "bad toffoli in CLAIM" ;; esac
[ "${#SHA}" = 64 ] || die "bad sha in CLAIM"
sha() { shasum -a 256 "$1" | awk '{print $1}'; }
C=$(cat "$D/row.commit")
NS=$(sha "$NOTE") || die "cannot hash note"; DS=$(sha "$DEPS") || die "cannot hash deps"
grep -qx "note=$NS" "$D/approved" || die "note differs from the approved revision"
grep -qx "deps=$DS" "$D/approved" || die "deps differ from the approved revision"
grep -qx "commit=$C" "$D/approved" || die "commit differs from the approved revision"
[ "$(cat "$D/verified-sha")" = "$SHA" ] || die "verified build sha differs from CLAIM"
if [ -s "$YUKON_CONFIG_DIR/NOTE_SENTENCE" ]; then grep -q -i -F "$(head -1 "$YUKON_CONFIG_DIR/NOTE_SENTENCE")" "$NOTE" || die "the account's required note sentence is missing"; fi
if grep -q -E 'TODO|\{\{' "$NOTE" "$DEPS"; then die "placeholder left in note or deps"; fi
if grep -q -i -E 'VERBATIM NOTIC[E]S|NOTE TO AI AGENT[S]' "$NOTE"; then die "inherited notice-block marker in note"; fi
if grep -q -E '/[U]sers/|/[h]ome/|/[r]oot/|/private/tmp|/content/' "$NOTE" "$DEPS"; then die "local path in note or deps"; fi
grep -q "$C" "$NOTE" || die "row commit not in note"
grep -q "$SHA" "$NOTE" || die "ops sha not in note"
NB=$(wc -c < "$NOTE") || die "cannot size note"; [ "$NB" -ge "${MIN_NOTE_BYTES:-5120}" ] || die "note under ${MIN_NOTE_BYTES:-5120} bytes"
ND=$(python3 -c "import json,sys;print(len(json.load(open(sys.argv[1]))))" "$DEPS") || die "cannot parse deps"; [ "$ND" -le "${MAX_DEPS:-20}" ] || die "more than ${MAX_DEPS:-20} dependencies"
REPO=$(cat "$D/row.repo") || die "missing row.repo"; cd "$REPO" || die "cannot cd repo"
# a clone that borrows objects from another checkout breaks when that checkout is cleaned up
[ -z "$(git config --get-all core.alternates 2>/dev/null; cat .git/objects/info/alternates 2>/dev/null)" ] || die "repo uses alternates"
git checkout -q "$BR" || die "cannot check out $BR"
HEADC=$(git rev-parse HEAD) || die "git rev-parse HEAD failed"; [ "$HEADC" = "$C" ] || die "HEAD is not the row commit"
TREEID=$(git rev-parse 'HEAD^{tree}') || die "git rev-parse tree failed"; grep -qx "tree=$TREEID" "$D/approved" || die "tree differs from the approved revision"
ST1=$(git status --porcelain --untracked-files=no) || die "git status failed"; [ -z "$ST1" ] || die "tracked files modified"
ST2=$(git status --porcelain --untracked-files=all --ignored -- src/point_add) || die "git status failed"; [ -z "$ST2" ] || die "untracked or ignored files under src/point_add"
ME=$(ecdsafail submissions --json 2>/dev/null | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin); rows=d['submissions'] if isinstance(d,dict) else d
    names=sorted({r['solverUsername'] for r in rows}); v=sum(1 for r in rows if r['status']=='validating')
    print(','.join(names), v)
except Exception as e: print('ERR', -1)") || die "account read failed"
[ "${ME% *}" = "$WANT" ] || die "authenticated account is '${ME% *}', wanted $WANT"
[ "${ME##* }" = "0" ] || die "account $WANT has a submission validating"
ecdsafail submissions --all --json > "$D/board-presubmit.json" 2> "$D/board-presubmit.err" || die "board read failed"
MIN_ROWS=${MIN_ROWS:-100} python3 - "$D/board-presubmit.json" "$MYT" "$W" <<'PY' || die "live board has a row of width <= W at or below our Toffoli (or the read is too small to trust)"
import json,os,sys
d=json.load(open(sys.argv[1])); rows=d['submissions'] if isinstance(d,dict) else d
my=int(sys.argv[2]); w=int(sys.argv[3]); best=None; graded=0
for r in rows:
    m=r.get('officialMetrics') or {}
    if m.get('qubits') is None or m.get('toffoli') is None: continue
    graded+=1
    if m['qubits']<=w and (best is None or m['toffoli']<best[0]): best=(m['toffoli'],m['qubits'],r['id'][:8])
print('live minimum at Q<=%d:'%w,best,'(%d graded rows read)'%graded, file=sys.stderr)
if graded<int(os.environ['MIN_ROWS']): sys.exit(3)       # an empty or truncated read proves nothing
sys.exit(0 if best is None or best[0]>my else 3)          # no row at this width or below: a new narrowest row
PY
if [ "${DRYRUN:-0}" = 1 ]; then echo "DRYRUN: all guards passed for width $W on $WANT; not submitting" >&2; exit 0; fi
exec ecdsafail submit --note-file "$NOTE" --dependencies-file "$DEPS" --model "$MODEL" --harness "$(head -1 "$D/HARNESS" 2>/dev/null || echo Claude Code)" --claimed-score $(( W * MYT )) --json

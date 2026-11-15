#!/bin/bash
# Pöschtler (submit-wait.sh): wait for a free account with no open claim, bind the approval, dry-run, post a CLAIM,
# submit under the shared lock, then wait for the grade.
#
#   submit-wait.sh <pkgdir> <W> <label>
#
# environment:
#   ACCOUNTS       required: space-separated "label:username" pairs, tried in order (e.g. "main:TeamA second:TeamB")
#   ACCOUNTS_DIR   required: see Briefchaschte (one saved CLI login per label; optional NOTE_SENTENCE per label,
#                  inserted before the note's first later heading when that account is used)
#   CLAIM_MAILBOX  claims file read by the gate; MAILBOX_POST: command that posts stdin as one line (optional)
#   CLAIM_SELF     your tag in the mailbox (default "me")
#   SUBMIT_LOCK    lock file shared by every lane that submits (default $ACCOUNTS_DIR/submit.lock); needs flock
#   STATE_LOG      file that gets one line per submit and grade (optional)
#   KEEP_APPROVED=1  do not write <pkgdir>/approved and do not touch the note: use the approval somebody else wrote.
#                  By default this script writes the approval itself, so STARTING IT IS THE APPROVAL.
# The package must already hold NOTE-<W>.md, deps-<W>.json, CLAIM, verified-sha, row.commit, row.tree, row.repo, MODEL.
set -u
D=$(cd "${1:?pkgdir}" && pwd) || exit 1; W=${2:?width}; LABEL=${3:?label}
HERE=$(cd "$(dirname "$0")" && pwd); T=${SUBMIT_DIR:-$HERE/../briefchaschte/submit-dir.sh}
: "${ACCOUNTS:?set ACCOUNTS}" "${ACCOUNTS_DIR:?set ACCOUNTS_DIR}"
LOCK=${SUBMIT_LOCK:-$ACCOUNTS_DIR/submit.lock}; ME=${CLAIM_SELF:-me}
post() { if [ -n "${MAILBOX_POST:-}" ]; then printf '%s\n' "$1" | $MAILBOX_POST >/dev/null 2>&1; fi; }
logline() { [ -n "${STATE_LOG:-}" ] && echo "- $(date -u +%FT%TZ) $1" >> "$STATE_LOG"; return 0; }
val() { YUKON_CONFIG_DIR=$ACCOUNTS_DIR/$1 ecdsafail submissions --json 2>/dev/null | python3 -c "
import sys,json
try:
  d=json.load(sys.stdin);rows=d['submissions'] if isinstance(d,dict) else d;print(sum(r['status']=='validating' for r in rows))
except Exception: print(-1)"; }
ID=
for ROUND in $(seq 1 30); do ACC=; NAME=
  for i in $(seq 1 90); do
    for pair in $ACCOUNTS; do a=${pair%%:*}; [ "$(val "$a")" = 0 ] && { ACC=$a; NAME=${pair#*:}; break; }; done
    [ -n "$ACC" ] && break; sleep 60; done
  [ -n "$ACC" ] || { echo "no free account"; exit 2; }
  S=$ACCOUNTS_DIR/$ACC/NOTE_SENTENCE
  if [ "${KEEP_APPROVED:-0}" != 1 ] && [ -s "$S" ] && ! grep -q -i -F "$(head -1 "$S")" "$D/NOTE-$W.md"; then
    python3 - "$D/NOTE-$W.md" "$S" <<'PY'
import sys
p=sys.argv[1]; lines=open(p).read().split('\n'); sent=open(sys.argv[2]).readline().strip()
i=next((k for k,l in enumerate(lines) if l.startswith('#') and k>0), len(lines))
lines.insert(i, sent+'\n'); open(p,'w').write('\n'.join(lines))
PY
  fi
  if grep -q -E '/[U]sers/|/[h]ome/|/content/|VERBATI[M]|NOTE TO A[I]|TODO|\{\{' "$D/NOTE-$W.md" "$D/deps-$W.json"; then echo hygiene-fail; exit 3; fi
  [ "${KEEP_APPROVED:-0}" = 1 ] || printf 'note=%s\ndeps=%s\ncommit=%s\ntree=%s\nmodel=%s\n' "$(shasum -a 256 "$D/NOTE-$W.md"|cut -c1-64)" "$(shasum -a 256 "$D/deps-$W.json"|cut -c1-64)" \
    "$(cat "$D/row.commit")" "$(cat "$D/row.tree")" "$(head -1 "$D/MODEL")" > "$D/approved"
  if ! DRYRUN=1 bash "$T" "$D" "$W" "$ACC" "$NAME" 2> "$D/dryrun-stderr.txt"; then cat "$D/dryrun-stderr.txt"
    if grep -q "open CLAIM" "$D/dryrun-stderr.txt"; then sleep 240; continue; fi
    echo "dryrun refused"; exit 4; fi
  TOF=$(sed -n 's/^toffoli=//p' "$D/CLAIM")
  post "$ME: CLAIM $W x $TOF ($LABEL) on $NAME, submitting now"
  for j in $(seq 1 20); do
    flock -n "$LOCK" bash "$T" "$D" "$W" "$ACC" "$NAME" > "$D/submit-response.json" 2> "$D/submit-stderr.txt"
    [ -s "$D/submit-stderr.txt" ] && break; sleep 30; done
  ID=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['submission']['id'])" "$D/submit-response.json" 2>/dev/null)
  if [ -z "$ID" ]; then echo "no id (round $ROUND)"; tail -2 "$D/submit-stderr.txt"
    if grep -q '"conflict"' "$D/submit-stderr.txt" "$D/submit-response.json" 2>/dev/null; then
      post "$ME: $W not submitted on $NAME (conflict, row in flight); claim released, retrying when free"; sleep 180; continue; fi
    post "$ME: $W not submitted on $NAME; claim released"; exit 5; fi
  break
done
[ -n "$ID" ] || exit 6
echo "$ID" > "$D/submission.id"; echo "SUBMITTED $ID on $NAME"
logline "SUBMITTED $W ($LABEL): $ID, $NAME, $W x $TOF, commit $(cat "$D/row.commit")"
post "$ME: SUBMITTED $W $ID on $NAME ($LABEL)"
r=
for i in $(seq 1 120); do r=$(YUKON_CONFIG_DIR=$ACCOUNTS_DIR/$ACC ecdsafail submissions --json 2>/dev/null | python3 -c "
import sys,json
d=json.load(sys.stdin); rows=d['submissions'] if isinstance(d,dict) else d
for r in rows:
  if r['id']==sys.argv[1]: print(r['status'], r.get('officialMetrics'), r.get('rejectionReason'))" "$ID"); case "$r" in validating*|queued*|'') sleep 60;; *) break;; esac; done
echo "GRADE: $r"; logline "$W ($ID) graded: $r"; post "$ME: $W $ID graded: $r"

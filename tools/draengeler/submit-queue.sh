#!/bin/bash
# Drängeler (submit-queue.sh): submit a list of READY row packages in order, one at a time, each through every gate.
#
#   submit-queue.sh <pkgroot> W1 W2 ...        packages are <pkgroot>/w<W>/, each with a READY file
#
# environment: ACCOUNTS, ACCOUNTS_DIR, CLAIM_MAILBOX, MAILBOX_POST, CLAIM_SELF, SUBMIT_LOCK, STATE_LOG as in Pöschtler;
#   KEEP_APPROVED=1  use the approval file somebody else wrote instead of writing it here (see Pöschtler)
#   PREPARE   optional command run as "$PREPARE <W> <username>" before each row (regenerate the note for that
#             account from a fresh board read, sync the submission branch); a non-zero exit skips the row.
# A row whose account is claimed by another lane, or whose dry run is refused, goes to the end of the queue.
set -u
R=$(cd "${1:?pkgroot}" && pwd) || exit 1; shift
HERE=$(cd "$(dirname "$0")" && pwd); T=${SUBMIT_DIR:-$HERE/../briefchaschte/submit-dir.sh}; G=${CLAIM_GATE:-$HERE/../tuerhueter/claim-gate.py}
: "${ACCOUNTS:?set ACCOUNTS}" "${ACCOUNTS_DIR:?set ACCOUNTS_DIR}"
LOG=$R/submit-queue.log; LOCK=${SUBMIT_LOCK:-$ACCOUNTS_DIR/submit.lock}; ME=${CLAIM_SELF:-me}
say() { echo "[sq $(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }
post() { if [ -n "${MAILBOX_POST:-}" ]; then printf '%s\n' "$1" | $MAILBOX_POST >/dev/null 2>&1; fi; }
validating() { YUKON_CONFIG_DIR=$ACCOUNTS_DIR/$1 ecdsafail submissions --json 2>/dev/null | python3 -c "
import sys,json
try:
    d=json.load(sys.stdin); rows=d['submissions'] if isinstance(d,dict) else d
    print(sum(1 for r in rows if r['status']=='validating'))
except Exception: print(-1)"; }
TRIES=0
while [ $# -gt 0 ]; do
  W=$1; shift; D=$R/w$W; TRIES=$((TRIES+1)); [ "$TRIES" -le "${MAX_TRIES:-200}" ] || { say "too many requeues, stop"; exit 3; }
  [ -f "$D/READY" ] || { say "W=$W not READY, skipped"; continue; }
  ACC=; NAME=
  for t in $(seq 1 120); do
    for pair in $ACCOUNTS; do a=${pair%%:*}; [ "$(validating "$a")" = 0 ] && { ACC=$a; NAME=${pair#*:}; break; }; done
    [ -n "$ACC" ] && break; sleep 60; done
  [ -n "$ACC" ] || { say "W=$W no free account after 2 h, stop"; exit 2; }
  if [ -n "${PREPARE:-}" ]; then $PREPARE "$W" "$NAME" >> "$LOG" 2>&1 || { say "W=$W prepare failed, skipped"; continue; }; fi
  if grep -q -E '/[U]sers/|/[h]ome/|/content/|VERBATI[M]|NOTE TO A[I]|TODO|\{\{' "$D/NOTE-$W.md" "$D/deps-$W.json"; then say "W=$W hygiene check failed, skipped"; continue; fi
  [ "${KEEP_APPROVED:-0}" = 1 ] || printf 'note=%s\ndeps=%s\ncommit=%s\ntree=%s\nmodel=%s\n' "$(shasum -a 256 "$D/NOTE-$W.md"|cut -c1-64)" "$(shasum -a 256 "$D/deps-$W.json"|cut -c1-64)" \
    "$(cat "$D/row.commit")" "$(cat "$D/row.tree")" "$(head -1 "$D/MODEL")" > "$D/approved"
  # the gate comes BEFORE our own CLAIM line: a queue that only looks at the account takes other lanes' slots
  if ! python3 "$G" "$NAME" >> "$LOG" 2>&1; then say "W=$W $NAME held by another lane's CLAIM, requeued"; sleep 240; set -- "$@" "$W"; continue; fi
  DRYRUN=1 bash "$T" "$D" "$W" "$ACC" "$NAME" >> "$LOG" 2>&1 || { say "W=$W DRYRUN refused, requeued at the end"; sleep 240; set -- "$@" "$W"; continue; }
  post "$ME: CLAIM $W x $(sed -n 's/^toffoli=//p' "$D/CLAIM") on $NAME, submitting now"
  for j in $(seq 1 20); do
    flock -n "$LOCK" bash "$T" "$D" "$W" "$ACC" "$NAME" > "$D/submit-response.json" 2> "$D/submit-stderr.txt"
    [ -s "$D/submit-stderr.txt" ] && break; sleep 30; done
  ID=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['submission']['id'])" "$D/submit-response.json" 2>/dev/null)
  if [ -n "$ID" ]; then echo "$ID" > "$D/submission.id"; say "W=$W SUBMITTED $ID on $NAME"; post "$ME: SUBMITTED $W $ID on $NAME"
    [ -n "${STATE_LOG:-}" ] && echo "- $(date -u +%FT%TZ) SUBMITTED $W: $ID, $NAME" >> "$STATE_LOG"
    sleep 90  # let the account list show the row as validating
  else say "W=$W submit gave no id; check the account before retrying"; tail -3 "$D/submit-stderr.txt" >> "$LOG"; post "$ME: $W not submitted on $NAME; claim released"; fi
done
say "queue done"

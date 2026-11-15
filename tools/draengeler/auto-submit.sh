#!/bin/bash
# Drängeler (auto-submit.sh): every 5 minutes, find packages under <pkgroot> that are READY and have no submission.id,
# and run submit-queue.sh on them, narrowest first. Stops when <pkgroot>/STOP exists or after MAX_HOURS (default 16).
#   auto-submit.sh <pkgroot>
R=$(cd "${1:?pkgroot}" && pwd) || exit 1; HERE=$(cd "$(dirname "$0")" && pwd)
END=$(( $(date +%s) + ${MAX_HOURS:-16}*3600 ))
while [ ! -f "$R/STOP" ] && [ "$(date +%s)" -lt "$END" ]; do
  if ! pgrep -f "submit-queue.sh $R" >/dev/null; then
    TODO=$(for d in "$R"/w[0-9]*; do W=${d##*/w}; [ -f "$d/READY" ] && [ ! -s "$d/submission.id" ] && echo "$W"; done | sort -n | tr '\n' ' ')
    if [ -n "$TODO" ]; then echo "[auto $(date -u +%H:%M:%S)] queue: $TODO" >> "$R/auto-submit.log"; bash "$HERE/submit-queue.sh" "$R" $TODO; fi
  fi
  sleep 300
done
echo "[auto $(date -u +%H:%M:%S)] exit" >> "$R/auto-submit.log"

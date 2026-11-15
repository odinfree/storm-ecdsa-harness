#!/bin/bash
# Hartnäckler (retry-launch.sh): try to launch a cloud job again and again until it is up or a deadline passes.
#
#   retry-launch.sh <rundir> <interval_seconds> <deadline: UTC yyyymmddHHMM, or 0 for none> -- <launch command...>
#
# The launch command must write its log to <rundir>/lane.log; the job counts as up when that log contains
# SUCCESS_PATTERN (default "launched (detached)", the line colab-lane prints). <rundir> is emptied before each try.
# ANNOUNCE (optional): a command run before each try, for one line in the team channel
# ("launch attempt for <what>, retry every N min until <deadline>").
# A refused launch allocates nothing and costs nothing, so retrying is safe; a launch that half-succeeded is not:
# check the provider's session list before you start a second loop for the same job.
set -u
RUN=${1:?rundir}; EVERY=${2:?interval}; UNTIL=${3:?deadline}; shift 3; [ "${1:-}" = "--" ] && shift
PAT=${SUCCESS_PATTERN:-launched (detached)}; n=0
while [ "$UNTIL" = 0 ] || [ "$(date -u +%Y%m%d%H%M)" -lt "$UNTIL" ]; do
  n=$((n+1)); [ -n "${ANNOUNCE:-}" ] && $ANNOUNCE >/dev/null 2>&1
  rm -rf "$RUN"; mkdir -p "$RUN"; "$@" > "$RUN/launch.log" 2>&1; sleep "${SETTLE:-75}"
  if grep -q -F "$PAT" "$RUN/lane.log" 2>/dev/null; then echo "LAUNCHED $(date -u +%H:%MZ) after $n tries"; exit 0; fi
  echo "not launched $(date -u +%H:%MZ) (try $n)"; sleep "$EVERY"
done
echo "STOPPED at deadline, no launch"; exit 1

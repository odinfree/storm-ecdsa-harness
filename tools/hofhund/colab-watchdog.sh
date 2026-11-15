#!/bin/bash
# Hofhund (colab-watchdog.sh): kill hung `colab` CLI calls of one session until its supervisor exits.
#
#   colab-watchdog.sh <session-name> <supervisor-pid> [max_call_seconds=150]
#
# A `colab exec` call can print "Connection was lost" and then hang at exit. A supervisor without its own call
# timeout then never polls again and never reaches its time limit, so the runtime bills without limit. This
# watchdog kills any exec or sessions call for <session-name> that is older than max_call_seconds.
# It matches the per-session state file name "colab-<session-name>" in the command line, as colab-lane creates it.
name=${1:?session name}; wp=${2:?supervisor pid}; max=${3:-150}
while kill -0 "$wp" 2>/dev/null; do
  for p in $(pgrep -f "colab --auth=oauth2 --config .*colab-$name([.-][A-Za-z0-9]+)?(\.json)? (exec|sessions)"); do
    # macOS ps has no etimes: parse etime ([[dd-]hh:]mm:ss)
    e=$(ps -o etime= -p "$p" 2>/dev/null | tr -d ' ' | awk -F'[-:]' '{n=NF; s=$n+60*$(n-1); if(n>=3)s+=3600*$(n-2); if(n>=4)s+=86400*$(n-3); print s}')
    if [ -n "$e" ] && [ "$e" -gt "$max" ]; then echo "[watchdog $(date -u +%H:%M:%S)] killing hung colab call pid $p (${e}s)"; kill "$p" 2>/dev/null; fi
  done
  sleep 20
done
echo "[watchdog $(date -u +%H:%M:%S)] supervisor $wp gone, exiting"

#!/bin/bash
# Hofhund (colab-detached.sh): start colab-lane in its OWN session with nohup, so the death of the calling agent
# session cannot kill the supervisor before it has downloaded the results and stopped the runtime.
#
#   colab-detached.sh <workdir> <logfile> -- <colab-lane args...>
#
# Refuses unless the colab-lane arguments include -t MINUTES. Writes <logfile>.pid and, when the supervisor
# exits, <logfile>.rc. COLAB_LANE names the supervisor (default: colab-lane on PATH).
set -u
wd=${1:?workdir}; log=${2:?logfile}; shift 2; [ "${1:-}" = "--" ] && shift
case " $* " in *" -t "*) ;; *) echo "refused: pass -t MINUTES to colab-lane" >&2; exit 2;; esac
cd "$wd" || exit 1
nohup python3 -c 'import os,sys,subprocess
os.setsid()
rc = subprocess.call(sys.argv[2:])
open(sys.argv[1] + ".rc", "w").write(str(rc) + "\n")' "$log" "${COLAB_LANE:-colab-lane}" "$@" > "$log" 2>&1 < /dev/null &
echo $! > "$log.pid"; echo "started pid $(cat "$log.pid") log $log"

#!/bin/bash
# Brotofe (vm-batch.sh): run a batch of per-row jobs in parallel ON a rented VM, with results that survive the VM.
#
#   SPEC=/content/spec.txt PAR=3 ROW=/content/row.sh bash vm-batch.sh
#
# /content is the Colab VM's working directory; set C to use another folder.
#   SPEC  text file, one job per line: the arguments for ROW (for example "A 17" or "B 17 85 <sha256>")
#   ROW   your per-row script; it must write its outcome as ONE line to $C/out/<job-dir>/RESULT and may write logs beside it
#   PAR   jobs in parallel (size it by memory: one official-style build of a low-Q row is tens of GB)
#   TC    Rust toolchain to install (default 1.93.0; empty to skip Rust)
# While jobs run, $C/out is packed into $C/batch-out.tgz every 2 minutes (atomically), so a download at any moment,
# including after a time limit killed the job, gets every row that had finished. At the end: $C/out/SUMMARY.txt
# (one line per RESULT), a final pack, and $C/DONE.
C=${C:-/content}; cd "$C" || exit 1
export PATH=$HOME/.cargo/bin:$PATH; PAR=${PAR:-3}; SPEC=${SPEC:-$C/spec.txt}; ROW=${ROW:?set ROW}; TC=${TC-1.93.0}
[ -x /usr/bin/time ] || { apt-get update -qq; apt-get install -y -qq time; } > "$C/apt.log" 2>&1
if [ -n "$TC" ]; then
  command -v gcc >/dev/null || { apt-get update -qq && apt-get install -y -qq build-essential; } >> "$C/apt.log" 2>&1
  command -v cargo >/dev/null || curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal -q > "$C/rustup.log" 2>&1
  rustup toolchain install "$TC" --profile minimal >> "$C/rustup.log" 2>&1 || { echo "toolchain $TC install failed"; exit 10; }
fi
mkdir -p out; exec > >(tee -a out/job.log) 2>&1
echo "[batch $(date -u +%H:%M:%S)] PAR=$PAR jobs=$(grep -c . "$SPEC") host $(uname -srm) cpus=$(nproc) $(free -g | awk '/Mem:/{print "ram_gb="$2" avail_gb="$7}') $(df -h "$C" | tail -1)"
( while :; do sleep 120; tar czf "$C/batch-out.tmp.tgz" -C "$C" out 2>/dev/null && mv "$C/batch-out.tmp.tgz" "$C/batch-out.tgz"; done ) &
TARPID=$!
grep . "$SPEC" | xargs -P "$PAR" -L1 bash "$ROW"
for f in $(find out -name RESULT | sort); do echo "$f: $(cat "$f")"; done | tee out/SUMMARY.txt
kill $TARPID 2>/dev/null; tar czf "$C/batch-out.tgz" -C "$C" out; echo done > "$C/DONE"

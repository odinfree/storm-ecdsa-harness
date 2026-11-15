#!/bin/bash
# Tüpflischiisser (verify-server.sh): a second verifier for finished rows. Runs ON a Colab VM with >= 80 GB RAM
# (the high-memory A100 shape had 12 vCPU and 83 GB in November 2026). /content is the Colab VM's working directory.
# Needs /content/fe.tgz holding fasteval.rs and qcount.rs (fasteval: BitWonka/ecdsafail-tools; qcount: tools/erbsezaehler).
# Queue: /content/q/row<W>.tree.tgz (git archive of the row's dev commit, no .git), row<W>.sha (expected ops.bin sha256), row<W>.ready (uploaded LAST).
# Per row, in arrival order:
#   cargo build --release --locked (shared target dir), build_circuit under `env -i` (official-style, about 52.6 GB peak), sha256 against the
#   expected one, qcount, then fasteval (grader shots, no salt, about 23 GB) on THAT build's own ops.bin, in the background while the next row builds.
# One line per event on stdout (colab-lane streams it to the caller):  VERIFY W=.. / QCOUNT W=.. / FEVAL W=.. / ROWFAIL W=..
# Ends when /content/q/STOP exists and nothing is pending, or after IDLE_MIN minutes without work. Logs: /content/vres/w<W>/ -> /content/verify-results.tgz
set -u
cd /content || exit 1
IDLE_MIN=${IDLE_MIN:-45}; FE_THREADS=${FE_THREADS:-8}; TC=${TC:-1.93.0}
# optional: SHOW_CONSTS = extended regex of source constants to echo per row; GREP_LINES = build-log lines to keep
mkdir -p /content/q /content/vres /content/fe
say() { echo "[vs $(date -u +%H:%M:%S)] $*"; }
finish() { tar czf /content/verify-results.tgz -C /content vres 2>/dev/null; say "server exit $1"; exit "$1"; }
say "host: $(nproc) cpus, $(awk '/MemTotal/{printf "%.1f GiB", $2/1048576}' /proc/meminfo), disk $(df -h /content | awk 'END{print $4}') free"
MEMG=$(awk '/MemTotal/{printf "%d", $2/1048576}' /proc/meminfo)
[ "$MEMG" -ge 75 ] || { say "FATAL: only $MEMG GiB RAM, the official-style build needs about 53"; finish 20; }
[ -x /usr/bin/time ] || { apt-get update -qq; apt-get install -y -qq time; } > /content/apt.log 2>&1
command -v gcc >/dev/null || apt-get install -y -qq build-essential >> /content/apt.log 2>&1
[ -x /usr/bin/time ] || { say "FATAL: /usr/bin/time missing"; tail -5 /content/apt.log; finish 10; }
if ! command -v cargo >/dev/null; then curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal -q > /content/rustup.log 2>&1; fi
export PATH=$HOME/.cargo/bin:$PATH
cargo --version || finish 10
rustup toolchain install "$TC" --profile minimal >> /content/rustup.log 2>&1 || { say "FATAL: toolchain $TC install failed"; tail -5 /content/rustup.log; finish 10; }
rustup toolchain list | grep -q "$TC" || { say "FATAL: toolchain $TC not installed"; finish 10; }
tar xzf /content/fe.tgz -C /content/fe || { say "FATAL: fe.tgz"; finish 11; }
export CARGO_TARGET_DIR=/content/target
say "READY: waiting for rows in /content/q"

FE_PID=
fe_bg() { # fe_bg W : fasteval on the row's own official-style ops.bin; prints the FEVAL lines; deletes ops.bin
  local W=$1 D=/content/v$1 L=/content/vres/w$1
  echo "[vs $(date -u +%H:%M:%S)] FEINFO W=$W cmd=FE_THREADS=$FE_THREADS $D/bin/fasteval $D/run/ops.bin bin_sha=$(sha256sum "$D/bin/fasteval" | cut -d' ' -f1) FE_SALT=${FE_SALT:-unset} env_FE=$(env | grep '^FE_' | tr '\n' ' ')"
  ( cd "$D" && FE_THREADS=$FE_THREADS /usr/bin/time -v -o "$L/fe.time" "$D/bin/fasteval" "$D/run/ops.bin" > "$L/fe.out" 2> "$L/fe.err"; rc=$?
    echo "rc=$rc" > "$L/fe.rc"
    Q=$(awk '/^  qubits  /{print $3; exit}' "$L/fe.out"); CL=$(awk -F: '/classical mismatches/{gsub(/ /,"",$2); print $2}' "$L/fe.out")
    PH=$(awk -F: '/phase-garbage batches/{gsub(/ /,"",$2); print $2}' "$L/fe.out"); AN=$(awk -F: '/ancilla-garbage batches/{gsub(/ /,"",$2); print $2}' "$L/fe.out")
    FS=$(awk -F: '/failing shots/{gsub(/ /,"",$2); print $2}' "$L/fe.out"); AV=$(awk -F: '/avg executed Toffoli/{gsub(/ /,"",$2); print $2}' "$L/fe.out")
    TS=$(awk -F: '/tested shots/{gsub(/ /,"",$2); print $2}' "$L/fe.out")
    RSS=$(awk -F': ' '/Maximum resident/{print $2}' "$L/fe.time"); WALL=$(awk '/wall time/{print $3}' "$L/fe.out")
    echo "[vs $(date -u +%H:%M:%S)] FEVAL W=$W rc=$rc qubits=${Q:-?} shots=${TS:-?} classical=${CL:-?} phase=${PH:-?} ancilla=${AN:-?} failing=${FS:-?} avg_toffoli=${AV:-?} wall=${WALL:-?} maxrss_kb=${RSS:-?}"
    grep -E 'all [0-9]+ shots OK|FAIL|mismatch at|first failing' "$L/fe.out" | head -3 | sed "s/^/[vs] FEVAL W=$W | /"
    rm -f "$D/run/ops.bin"; touch "/content/q/row$W.fedone" ) &
  FE_PID=$!
}

do_row() { # do_row W
  local W=$1 D=/content/v$1 L=/content/vres/w$1 EXP SHA BRC T0 WALL RSS SZ
  rm -rf "$D" "$L"; mkdir -p "$D/tree" "$D/run" "$D/bin" "$L"
  EXP=$(tr -d ' \n' < "/content/q/row$W.sha")
  tar xzf "/content/q/row$W.tree.tgz" -C "$D/tree" || { say "ROWFAIL W=$W untar"; return 1; }
  [ -f "$D/tree/Cargo.toml" ] || { say "ROWFAIL W=$W no Cargo.toml"; return 1; }
  grep -q "$TC" "$D/tree/rust-toolchain" 2>/dev/null || say "note: W=$W rust-toolchain file does not name $TC: $(tr '\n' ' ' < "$D/tree/rust-toolchain" 2>/dev/null)"
  say "ROW W=$W expect ${EXP}${SHOW_CONSTS:+ ; consts: $(grep -rhoE "$SHOW_CONSTS" "$D/tree/src/point_add" | tr '\n' ' ')}"
  cp /content/fe/fasteval.rs /content/fe/qcount.rs "$D/tree/src/bin/"
  ( cd "$D/tree" && cargo build --release --locked --bin build_circuit --bin fasteval --bin qcount ) > "$L/cargo.log" 2>&1 || { say "ROWFAIL W=$W cargo build"; tail -15 "$L/cargo.log"; return 1; }
  cp /content/target/release/build_circuit /content/target/release/fasteval /content/target/release/qcount "$D/bin/" || { say "ROWFAIL W=$W copy bins"; return 1; }
  say "W=$W build_circuit under env -i"
  T0=$(date +%s)
  ( cd "$D/run" && /usr/bin/time -v -o "$L/build.time" env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$D/run" "$D/bin/build_circuit" ) > "$L/build.out" 2> "$L/build.err"
  BRC=$?; WALL=$(( $(date +%s) - T0 )); RSS=$(awk -F': ' '/Maximum resident/{print $2}' "$L/build.time")
  grep -E "${GREP_LINES:-POSTPASS|HOLD|cap}" "$L/build.err" | cut -c1-300 > "$L/build.lines"; sed "s/^/[vs] W=$W | /" "$L/build.lines"
  if [ $BRC -ne 0 ] || [ ! -s "$D/run/ops.bin" ]; then say "ROWFAIL W=$W build_circuit rc=$BRC wall=${WALL}s maxrss_kb=${RSS:-?}"; tail -8 "$L/build.err" | cut -c1-300; rm -f "$D/run/ops.bin"; return 1; fi
  SHA=$(sha256sum "$D/run/ops.bin" | cut -d' ' -f1); SZ=$(stat -c %s "$D/run/ops.bin"); echo "$SHA" > "$L/ops.sha256"; echo "$SZ" > "$L/ops.size"
  if [ "$SHA" = "$EXP" ]; then echo MATCH > "$L/SHA_MATCH"; say "VERIFY W=$W sha=$SHA MATCH size=$SZ build_wall=${WALL}s maxrss_kb=${RSS:-?}"
  else echo "MISMATCH want $EXP" > "$L/SHA_MISMATCH"; say "VERIFY W=$W sha=$SHA MISMATCH expect=$EXP size=$SZ build_wall=${WALL}s maxrss_kb=${RSS:-?}"; fi
  "$D/bin/qcount" "$D/run/ops.bin" > "$L/qcount.txt" 2>&1; say "QCOUNT W=$W $(tr '\n' ' ' < "$L/qcount.txt")"
  # never two evaluations at once (2 x 23 GB next to a 53 GB build would not fit)
  if [ -n "$FE_PID" ]; then wait "$FE_PID" 2>/dev/null; fi
  fe_bg "$W"
  return 0
}

LAST=$(date +%s)
while :; do
  NEXT=
  for f in $(ls -tr /content/q/*.ready 2>/dev/null); do
    w=$(basename "$f" .ready); w=${w#row}
    [ -f "/content/q/row$w.done" ] && continue
    [ -f "/content/q/row$w.tree.tgz" ] && [ -f "/content/q/row$w.sha" ] || continue
    NEXT=$w; break
  done
  if [ -n "$NEXT" ]; then
    do_row "$NEXT"; echo "rc=$?" > "/content/q/row$NEXT.done"; LAST=$(date +%s)
    tar czf /content/verify-results.tgz -C /content vres 2>/dev/null
    continue
  fi
  FE_RUNNING=0; [ -n "$FE_PID" ] && kill -0 "$FE_PID" 2>/dev/null && FE_RUNNING=1
  [ "$FE_RUNNING" = 1 ] && LAST=$(date +%s)
  if [ "$FE_RUNNING" = 0 ]; then
    [ -f /content/q/STOP ] && { say "STOP file seen, queue empty"; finish 0; }
    [ $(( $(date +%s) - LAST )) -gt $(( IDLE_MIN * 60 )) ] && { say "idle for more than $IDLE_MIN min, leaving"; finish 0; }
  fi
  sleep 20
done

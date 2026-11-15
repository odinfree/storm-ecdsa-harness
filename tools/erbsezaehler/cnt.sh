#!/bin/bash
# Erbsezähler (cnt.sh): count-only build of an ecdsa.fail tree. Small memory, under a minute on a streamed tree,
# so it can run on a laptop next to other work.
#
#   cnt.sh <tree-dir> <name> [VAR=value ...]        extra assignments go to the builder's (otherwise empty) environment
#
# Copies <tree-dir> to a work copy (the tree is never edited), adds qcount.rs, builds build_circuit + qcount,
# runs build_circuit under `env -i` with the tree's stream-to-file variable set, prints the lines matching
# GREP_LINES from the build log, and runs qcount on the stream (independent distinct-qubit-id count).
# Everything lands in $OUT/cnt_<name>/ (OUT defaults to ./out). The stream is deleted unless KEEPPRE=1.
#
# environment:
#   STREAM_VAR     name of the tree's own variable that makes build_circuit write its pre-post-pass stream to a file
#                  instead of holding it in memory (default LOWQ_EXACT_STREAM_PATH; low-Q trees of the frogdrop
#                  lineage have it). STREAM_VAR=none runs the tree's normal build and counts ./ops.bin instead.
#   GREP_LINES     extended regex of build-log lines to print (default: panicked|compaction|STREAM)
#   SHARED_TARGET  a cargo target dir shared between names. Default is one target dir PER NAME. Read the README
#                  before you share one: this is how a control build reused the candidate's binary.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
TREE=$(cd "${1:?tree}" && pwd) || exit 2; N=${2:?name}; shift 2
case "$N" in ""|*[!A-Za-z0-9._-]*) echo "name must be letters, digits, dot, dash, underscore" >&2; exit 2;; esac
ROOT=$(mkdir -p "${OUT:-./out}" && cd "${OUT:-./out}" && pwd); O=$ROOT/cnt_$N; rm -rf "$O"; mkdir -p "$O/work" "$O/run"
SV=${STREAM_VAR:-LOWQ_EXACT_STREAM_PATH}; TD=${SHARED_TARGET:-$O/target}
export PATH=$HOME/.cargo/bin:$PATH
rsync -a --exclude target --exclude .git --exclude 'ops*.bin' "$TREE"/ "$O/work"/
# rsync -a keeps old mtimes, and cargo decides by mtime whether to rebuild. With a shared target dir, a second
# tree whose files are OLDER than the last build is silently skipped and the previous binary is reused.
find "$O/work" -type f \( -name "*.rs" -o -name "*.toml" -o -name "*.glz" -o -name "*.txt" \) -exec touch {} +
mkdir -p "$O/work/src/bin"; cp "$HERE/qcount.rs" "$O/work/src/bin/"
( cd "$O/work" && CARGO_TARGET_DIR=$TD CARGO_BUILD_JOBS=${JOBS:-4} nice -n 10 cargo build --release --locked ${CARGO_FLAGS:-} --bin build_circuit --bin qcount > "$O/cargo.log" 2>&1 ) \
  || { echo "[$N] CARGO FAIL"; tail -15 "$O/cargo.log"; exit 2; }
cp "$TD/release/build_circuit" "$O/bc"; cp "$TD/release/qcount" "$O/qcount"
echo "[$N] build_circuit sha256 $(shasum -a 256 "$O/bc" | cut -d' ' -f1)" | tee "$O/bc.sha"
if [ "$SV" = none ]; then S="$O/run/ops.bin"; SETV=(); else S="$O/run/pre.bin"; SETV=("$SV=$S"); fi
TIMEV=-l; /usr/bin/time -l true >/dev/null 2>&1 || TIMEV=-v
( cd "$O/run" && env -i HOME="$HOME" PATH=/usr/bin:/bin ${SETV[@]+"${SETV[@]}"} "$@" nice -n 10 /usr/bin/time $TIMEV "$O/bc" > "$O/build.out" 2> "$O/build.err"; echo $? > "$O/rc" )
echo "[$N] rc=$(cat "$O/rc") $(grep -E 'maximum resident set size|Maximum resident set size' "$O/build.err" | tr -s ' ' | head -1)"
grep -E "${GREP_LINES:-panicked|compaction|STREAM}" "$O/build.err" | cut -c1-260
if [ -s "$S" ]; then
  echo "[$N] stream sha256 $(shasum -a 256 "$S" | cut -d' ' -f1)" | tee "$O/pre.sha"
  echo "[$N] qcount(stream): $("$O/qcount" "$S")" | tee "$O/qcount.txt"
  [ "${KEEPPRE:-0}" = 1 ] || rm -f "$S"
fi
rm -rf "$O/work"
exit "$(cat "$O/rc")"

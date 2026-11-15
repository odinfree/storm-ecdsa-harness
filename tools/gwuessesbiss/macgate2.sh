#!/bin/bash
# Gwüssesbiss (macgate2.sh): the full gate for one candidate tree on a workstation, ONE heavy process at a time.
#
#   macgate2.sh <tree> <outdir> [nonce order, default "1 0 2"]
#
# Order: candidate official-style build (env -i) at each nonce in turn -> sha256 + qcount -> fasteval on the grader's
# shots -> (dirty: next nonce) -> stock eval_circuit -> 8 salted suites -> parent build -> PAIRED salted runs 1-8
# (candidate and parent on identical inputs; lists the failing shots of each). GATE lines go to <outdir>/GATE.txt.
#
# environment:
#   FE_SRC        required: folder with fasteval.rs, qcount.rs and (for the paired part) seval_pair.rs, copied into
#                 each work tree's src/bin. fasteval: BitWonka/ecdsafail-tools. qcount: tools/erbsezaehler.
#                 seval_pair: any evaluator with the interface "seval_pair OPS SHOTS SALT THREADS" that prints
#                 "SEVAL RESULT ..." and "SEVAL FAIL ..." lines on stderr; without it set PAIRED=0.
#   PARENT_TREE   the parent row's tree (required unless PAIRED=0); PARDIR caches its build (default <outdir>/../gate-parent)
#   NONCE_FILE / NONCE_CONST   file and constant name of the nonce (default src/point_add/mod.rs / NONCE)
#   HEAVY_LOCK    lock directory shared by everything heavy on this machine (default ${TMPDIR:-/tmp}/heavy.lockdir)
#   MIN_FREE (50), MAX_OTHER_KB (4194304), KILL_RSS_KB (25165824): the memory limits below
# macOS only as written: it reads `memory_pressure`, uses `time -l` and `sed -i ''`.
set -u
TREE=$(cd "${1:?tree}" && pwd); mkdir -p "${2:?outdir}"; O=$(cd "$2" && pwd); NONCES=${3:-"1 0 2"}; L=$O/logs; mkdir -p $L $O/fe; cp "${FE_SRC:?set FE_SRC}"/*.rs $O/fe/
PAIRED=${PAIRED:-1}; PAR=${PARDIR:-$O/../gate-parent}; PTREE=${PARENT_TREE:-}; NF=${NONCE_FILE:-src/point_add/mod.rs}; NC=${NONCE_CONST:-NONCE}
[ "$PAIRED" = 0 ] || [ -d "$PTREE" ] || { echo "set PARENT_TREE or PAIRED=0" >&2; exit 2; }
MIN_FREE=${MIN_FREE:-50}; MAX_OTHER_KB=${MAX_OTHER_KB:-4194304}; KILL_RSS_KB=${KILL_RSS_KB:-25165824}
export PATH=$HOME/.cargo/bin:$PATH
LK=${HEAVY_LOCK:-${TMPDIR:-/tmp}/heavy.lockdir}
say() { echo "GATE $(date -u +%H:%M:%S) $*" | tee -a $O/GATE.txt; }
memok() { local f; for i in $(seq 1 120); do f=$(memory_pressure | tail -1 | grep -o '[0-9]*%' | tr -d %); [ "${f:-0}" -gt 40 ] && return 0; say "free ${f}% <= 40: waiting"; sleep 30; done; return 1; }
heavyok() { # limits before a heavy step: free memory >= MIN_FREE % AND no other process above MAX_OTHER_KB
  local f big; for i in $(seq 1 240); do
    f=$(memory_pressure | tail -1 | grep -o '[0-9]*%' | tr -d %); big=$(ps -axo rss=,pid=,comm= | awk -v m=$MAX_OTHER_KB '$1 > m {printf "%s(%.1fGB) ", $2, $1/1048576}')
    if [ "${f:-0}" -ge "$MIN_FREE" ] && [ -z "$big" ]; then return 0; fi
    [ $((i % 10)) = 1 ] && say "heavy step waits: free ${f}% (need >= $MIN_FREE), large processes: ${big:-none}"; sleep 30; done; return 1; }
lock_take() { mkdir -p "$(dirname $LK)"; until mkdir "$LK" 2>/dev/null; do local h; h=$(cat $LK/pid 2>/dev/null)
    # a holder that died without cleaning up (crash, kill -9) must not block the machine forever
    if [ -n "$h" ] && ! kill -0 "$h" 2>/dev/null; then say "heavy lock of dead pid $h removed"; rm -rf "$LK"; continue; fi
    say "heavy lock held by ${h:-?}: waiting"; sleep 30; done; echo $$ > "$LK/pid"; }
lock_free() { if [ "$(cat "$LK/pid" 2>/dev/null)" = "$$" ]; then rm -rf "$LK"; fi; }
trap lock_free EXIT INT TERM
guarded() { # guarded <name> <dir> cmd...: run under env -i in <dir>, kill above KILL_RSS_KB, or when the system runs out of memory
  local n=$1 d=$2; shift 2; mkdir -p $d
  ( cd $d && exec /usr/bin/time -l -o $L/$n.time env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR=$d "$@" > $L/$n.out 2> $L/$n.err ) & local tp=$!
  ( while kill -0 $tp 2>/dev/null; do
      for p in $(pgrep -P $tp) $(pgrep -P $(pgrep -P $tp | head -1) 2>/dev/null); do
        r=$(ps -o rss= -p $p 2>/dev/null | tr -d ' '); if [ "${r:-0}" -gt "$KILL_RSS_KB" ]; then echo "GATE GUARD KILL $n pid $p rss_kb $r (> $KILL_RSS_KB)" >> $O/GATE.txt; kill -9 $p; fi
        if [ "${r:-0}" -gt 4194304 ]; then f=$(memory_pressure | tail -1 | grep -o '[0-9]*%' | tr -d %); if [ "${f:-100}" -lt 15 ]; then echo "GATE SYSTEM GUARD KILL $n pid $p: system free ${f}% < 15" >> $O/GATE.txt; kill -9 $p; fi; fi
      done; sleep 3; done ) & local gp=$!
  wait $tp; local rc=$?; kill $gp 2>/dev/null; return $rc
}
prep() { # prep <tree> <name>: work copy + cargo build with the analysis bins
  local w=$O/work_$2; rm -rf $w; mkdir -p $w; rsync -a --exclude target --exclude .git "$1"/ $w/
  find $w -type f \( -name "*.rs" -o -name "*.toml" -o -name "*.glz" \) -exec touch {} +
  mkdir -p $w/src/bin; cp $O/fe/*.rs $w/src/bin/
  local sp=; [ -f $O/fe/seval_pair.rs ] && sp="--bin seval_pair"
  ( cd $w && CARGO_TARGET_DIR=$O/target_$2 CARGO_BUILD_JOBS=6 nice -n 10 cargo build --release --locked ${CARGO_FLAGS:-} --bin build_circuit --bin eval_circuit --bin fasteval --bin qcount $sp ) > $L/cargo_$2.log 2>&1 || { say "CARGO FAIL $2"; tail -5 $L/cargo_$2.log; return 1; }
}
build() { # build <name> <bindir> -> $O/<name>/ops.bin
  heavyok || { say "limits never met for $1"; return 1; }; lock_take
  guarded build_$1 $O/$1 nice -n 10 $2/build_circuit; local rc=$?; lock_free
  say "build $1 rc=$rc sha256 $(shasum -a 256 $O/$1/ops.bin 2>/dev/null | cut -d' ' -f1) $($2/qcount $O/$1/ops.bin 2>/dev/null) rss_mb=$(awk '/maximum resident set size/{printf "%.0f", $1/1048576}' $L/build_$1.time) wall_s=$(awk '/ real /{print $1}' $L/build_$1.time)"
  return $rc
}
fe() { # fe <name> <ops> [salt]
  rm -f $L/$1.log $L/$1.err   # a log left by an earlier run in the same outdir must never read as this run's result
  memok || { say "memory never freed for $1"; return 1; }; if [ -n "${3:-}" ]; then FE_SALT=$3 FE_THREADS=8 nice -n 10 $CB/fasteval $2 > $L/$1.log 2> $L/$1.err; else FE_THREADS=8 nice -n 10 $CB/fasteval $2 > $L/$1.log 2> $L/$1.err; fi
  say "$1: $(grep -hE 'qubits|avg executed Toffoli|classical mismatches|phase-garbage|ancilla-garbage|failing shots|shots OK' $L/$1.log | tr -s ' ' | tr '\n' ';' | cut -c1-420)"
}
say "start; tree $TREE; nonces $NONCES; $(memory_pressure | tail -1)"
prep $TREE cand || exit 2
CB=$O/target_cand/release; PICK=
CONSTN=$(grep -o "^pub const $NC: usize = [0-9]*" $O/work_cand/$NF | grep -o "[0-9]*$")
[ -n "$CONSTN" ] || { say "no line 'pub const $NC: usize = <n>' in $NF: set NONCE_FILE / NONCE_CONST"; exit 2; }
for n in $NONCES; do
  if [ $n != $CONSTN ] || [ -f $O/.edited ]; then touch $O/.edited
    sed -i '' "s/^pub const $NC: usize = [0-9]*;/pub const $NC: usize = $n;/" $O/work_cand/$NF
    ( cd $O/work_cand && CARGO_TARGET_DIR=$O/target_cand CARGO_BUILD_JOBS=6 nice -n 10 cargo build --release --locked ${CARGO_FLAGS:-} --bin build_circuit ) > $L/cargo_cand_n$n.log 2>&1 || { say "CARGO FAIL nonce $n"; exit 2; }
  fi
  say "nonce $n: $(grep -n "^pub const $NC" $O/work_cand/$NF)"
  build c$n $CB || { say "build c$n failed: $(tail -2 $L/build_c$n.err | tr '\n' ' ' | cut -c1-300)"; exit 3; }
  fe fe0_c$n $O/c$n/ops.bin
  if grep -qE 'all [0-9,]+ shots OK' $L/fe0_c$n.log; then PICK=c$n; break; fi
  rm -f $O/c$n/ops.bin
done
say "pick=${PICK:-NONE}"
[ -n "$PICK" ] || { say "no clean draw among nonces $NONCES"; exit 4; }
( cd $O/work_cand && COPYFILE_DISABLE=1 tar czf $O/tree_pick.tgz --exclude target --exclude 'src/bin/fasteval.rs' --exclude 'src/bin/qcount.rs' --exclude 'src/bin/seval_pair.rs' --exclude 'src/bin/gensynth.rs' . )
OPS=$O/$PICK/ops.bin
heavyok || { say "limits never met for the stock evaluator"; exit 3; }; lock_take; mkdir -p $O/stock; ( cd $O/stock && ln -sf $OPS ops.bin && nice -n 10 /usr/bin/time -l -o $L/stock.time $CB/eval_circuit > $L/stock.out 2> $L/stock.err; echo $? > $L/stock.rc ); lock_free
say "stock rc=$(cat $L/stock.rc): $(grep -hiE 'qubits|toffoli|shots|score' $L/stock.out | tr -s ' ' | tr '\n' ';' | cut -c1-420)"
for s in 1 2 3 4 5 6 7 8; do fe fe_salt$s $OPS $s; done
[ "$PAIRED" = 0 ] && { say "DONE pick=$PICK (paired part skipped; candidate ops.bin kept at $OPS)"; exit 0; }
# the cached parent stream belongs to ONE parent tree
if [ -f $PAR/PARENT ] && [ "$(cat $PAR/PARENT)" != "$(cd $PTREE && pwd)" ]; then say "PARDIR $PAR holds another parent ($(cat $PAR/PARENT)): use a PARDIR per parent"; exit 2; fi
if [ ! -s $PAR/par/ops.bin ]; then
  mkdir -p $PAR; (cd $PTREE && pwd) > $PAR/PARENT
  ( O=$PAR; L=$PAR/logs; mkdir -p $L $O/fe; cp "$FE_SRC"/*.rs $O/fe/; prep $PTREE par && build par $O/target_par/release ) || { say "parent build failed"; exit 3; }
fi
say "parent stream $PAR/par/ops.bin sha256 $(shasum -a 256 $PAR/par/ops.bin | cut -d' ' -f1)"
for s in 1 2 3 4 5 6 7 8; do
  memok || { say "memory never freed for the paired run, salt $s"; exit 3; }
  nice -n 10 $CB/seval_pair $OPS 9024 $s 8 > /dev/null 2> $L/seval_cand_s$s.err
  nice -n 10 $CB/seval_pair $PAR/par/ops.bin 9024 $s 8 > /dev/null 2> $L/seval_par_s$s.err
  for w in cand par; do say "PAIRED salt $s $w: $(grep -h 'SEVAL RESULT' $L/seval_${w}_s$s.err | grep -o 'classical.*avg_executed_T=[0-9.]*') | $(grep -h 'SEVAL FAIL' $L/seval_${w}_s$s.err | tr '\n' ';' | cut -c1-600)"; done
done
say "DONE pick=$PICK (candidate ops.bin kept at $OPS)"

#!/usr/bin/env bash
# Run Kimi Code CLI (Moonshot K3) headless as a worker.
#   kimi.sh <role> <prompt-file> <out-file> [workdir]
#   env: KIMI_MODEL (alias from `kimi provider list`, default kimi-code/k3-256k)
# NOTE: needs a valid OAuth login: run `kimi` once interactively and sign in. Until then this fails with
#       "The provided authorization grant is invalid".
set -euo pipefail
ROLE="${1:?role}"; PROMPT="${2:?prompt file}"; OUT="${3:?out file}"; WORKDIR="${4:-$PWD}"
MODEL="${KIMI_MODEL:-kimi-code/k3-256k}"
PRE="$(dirname "$0")/preamble-$ROLE.md"
mkdir -p "$(dirname "$OUT")"
full="$( { [[ -f "$PRE" ]] && cat "$PRE" && echo; cat "$PROMPT"; } )"
start=$(date +%s)
mode=()
[[ "$ROLE" == builder ]] && mode=(--auto)
( cd "$WORKDIR" && kimi -p "$full" -m "$MODEL" --output-format text "${mode[@]}" ) > "$OUT" 2> "$OUT.stderr" || rc=$?
rc=${rc:-0}
echo "kimi[$ROLE,$MODEL] rc=$rc $(( $(date +%s) - start ))s -> $OUT"
exit $rc

#!/usr/bin/env bash
# Run OpenAI Codex (gpt-6-astra) headless as a worker. Max reasoning effort by default.
#
#   codex.sh <role> <prompt-file> <out-file> [workdir] [sandbox]
#     role     advisor | auditor | builder | reviewer   (sets default sandbox + preamble)
#     sandbox  read-only | workspace-write | danger-full-access  (default: by role)
#   env: CODEX_BIN (default codex on PATH), CODEX_MODEL (default gpt-6-astra), CODEX_EFFORT (default max), CODEX_SCHEMA (json schema file)
#
# Output: final assistant message written to <out-file>; JSON-lines event log next to it (<out-file>.events.ndjson).
set -euo pipefail
ROLE="${1:?role}"; PROMPT="${2:?prompt file}"; OUT="${3:?out file}"; WORKDIR="${4:-$PWD}"; SANDBOX="${5:-}"
CODEX="${CODEX_BIN:-codex}"
MODEL="${CODEX_MODEL:-gpt-6-astra}"; EFFORT="${CODEX_EFFORT:-max}"
case "$ROLE" in
  builder)  : "${SANDBOX:=workspace-write}" ;;
  *)        : "${SANDBOX:=read-only}" ;;
esac
PRE="$(dirname "$0")/preamble-$ROLE.md"
mkdir -p "$(dirname "$OUT")"
tmp="$(mktemp)"; { [[ -f "$PRE" ]] && cat "$PRE" && echo; cat "$PROMPT"; } > "$tmp"
args=( exec --skip-git-repo-check -C "$(cygpath -w "$WORKDIR" 2>/dev/null || echo "$WORKDIR")" -m "$MODEL" -s "$SANDBOX" \
       -c "model_reasoning_effort=\"$EFFORT\"" -c 'approval_policy="never"' -c 'model_verbosity="medium"' \
       --json -o "$(cygpath -w "$OUT" 2>/dev/null || echo "$OUT")" )
[[ -n "${CODEX_SCHEMA:-}" ]] && args+=( --output-schema "$(cygpath -w "$CODEX_SCHEMA")" )
start=$(date +%s)
"$CODEX" "${args[@]}" - < "$tmp" > "$OUT.events.ndjson" 2>&1 || rc=$?
rc=${rc:-0}; rm -f "$tmp"
echo "codex[$ROLE,$MODEL,$EFFORT,$SANDBOX] rc=$rc $(( $(date +%s) - start ))s -> $OUT"
exit $rc

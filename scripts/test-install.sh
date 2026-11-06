#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL="$ROOT/install.sh"
SAMPLE="$(find "$ROOT/skills" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort | head -1)"
[ -n "$SAMPLE" ] || { echo "no directory skills found" >&2; exit 1; }

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

fail=0
check() {
  local name="$1"
  shift
  if "$@"; then
    printf 'PASS %s\n' "$name"
  else
    printf 'FAIL %s\n' "$name" >&2
    fail=$((fail + 1))
  fi
}

# Default profile: Hermes is installed only when its skills directory exists.
default_home="$tmp/default-home"
mkdir -p "$default_home/.hermes/skills"
HOME="$default_home" env -u HERMES_HOME bash "$INSTALL" >/dev/null
check "default Hermes profile receives skills" test -L "$default_home/.hermes/skills/$SAMPLE"
check "Claude remains supported" test -L "$default_home/.claude/skills/$SAMPLE"
check "Codex remains supported" test -L "$default_home/.codex/skills/$SAMPLE"

# Named profile: HERMES_HOME wins and the default profile is not polluted.
named_home="$tmp/named-home"
named_profile="$tmp/named-profile"
mkdir -p "$named_home/.hermes/skills" "$named_profile/skills"
HOME="$named_home" HERMES_HOME="$named_profile" bash "$INSTALL" >/dev/null
check "named Hermes profile receives skills" test -L "$named_profile/skills/$SAMPLE"
check "named install does not pollute default Hermes" test ! -e "$named_home/.hermes/skills/$SAMPLE"

# Existing entries are authoritative and a second run is a no-op.
preserve_home="$tmp/preserve-home"
mkdir -p "$preserve_home/.hermes/skills/$SAMPLE"
printf 'keep\n' > "$preserve_home/.hermes/skills/$SAMPLE/marker"
HOME="$preserve_home" env -u HERMES_HOME bash "$INSTALL" >/dev/null
before="$(find "$preserve_home" -type l -printf '%p -> %l\n' | sort)"
HOME="$preserve_home" env -u HERMES_HOME bash "$INSTALL" >/dev/null
after="$(find "$preserve_home" -type l -printf '%p -> %l\n' | sort)"
check "existing Hermes entry is preserved" test -f "$preserve_home/.hermes/skills/$SAMPLE/marker"
check "installer is idempotent" test "$before" = "$after"

printf 'install_test: PASS=%d FAIL=%d\n' "$((7 - fail))" "$fail"
exit "$((fail != 0))"

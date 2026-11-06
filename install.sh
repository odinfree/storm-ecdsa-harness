#!/usr/bin/env bash
# Link every skill in skills/ into the agent skill directories on this machine.
# Targets: Claude and Codex, plus Agents and the active Hermes profile when present.
# An existing entry with the same name is never replaced.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
targets=("$HOME/.claude/skills" "$HOME/.codex/skills")
[ -d "$HOME/.agents/skills" ] && targets+=("$HOME/.agents/skills")
hermes_home="${HERMES_HOME:-$HOME/.hermes}"
[ -d "$hermes_home/skills" ] && targets+=("$hermes_home/skills")
for target in "${targets[@]}"; do
  mkdir -p "$target"
  for dir in "$here"/skills/*/; do
    name="$(basename "$dir")"
    if [ -e "$target/$name" ] || [ -L "$target/$name" ]; then
      echo "skip   $target/$name (already exists)"
    else
      ln -s "${dir%/}" "$target/$name" && echo "linked $target/$name"
    fi
  done
done

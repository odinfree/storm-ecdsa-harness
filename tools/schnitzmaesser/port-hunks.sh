#!/bin/bash
# Schnitzmässer (port-hunks.sh): carry the hunks of a patch that still apply onto another tree, and say which did not.
#
#   port-hunks.sh <src-tree> <dst-tree> <patch-file> [strip=0] [file-in-tree]
#
# Copies <src-tree> to <dst-tree> (replaced; target/ and .git excluded), applies the patch with `patch -p<strip> -f`
# (to [file-in-tree] when given, for a patch made against a differently named tree), and prints one line per hunk:
# applied or FAILED (as far as the local `patch` reports per hunk), then a summary. Rejected hunks are saved in <dst-tree>.rejects/ and removed from the
# tree, so the tree builds with exactly the hunks reported as applied. Exit 0 when at least one hunk applied.
# The result is a COUNT-ONLY probe tree: a hunk that applies textually is not thereby correct on the new frame.
set -u
SRC=${1:?src}; DST=${2:?dst}; P=$(cd "$(dirname "${3:?patch}")" && pwd)/$(basename "$3"); STRIP=${4:-0}; FILE=${5:-}
rsync -a --checksum --delete --exclude target --exclude .git "$SRC"/ "$DST"/
REJ=$(cd "$(dirname "$DST")" && pwd)/$(basename "$DST").rejects; rm -rf "$REJ"; mkdir -p "$REJ"
# -F0: no fuzz. With the default fuzz, Apple's patch 2.0 "applied" a hunk in our test whose removed line did not match.
( cd "$DST" && patch -p"$STRIP" -f -F"${FUZZ:-0}" $FILE < "$P" ) > "$REJ/patch.log" 2>&1
grep -E '^Hunk #[0-9]+ (succeeded|FAILED)|^patching file|^[0-9]+ out of [0-9]+ hunks? ' "$REJ/patch.log"
( cd "$DST" && find . -name '*.rej' | while read -r f; do mkdir -p "$REJ/$(dirname "$f")"; mv "$f" "$REJ/$f"; done; find . -name '*.orig' -delete )
TOTAL=$(grep -c '^@@' "$P"); FAILED=$(awk '/^[0-9]+ out of [0-9]+ hunks? /{n+=$1} END{print n+0}' "$REJ/patch.log")
echo "hunks: $((TOTAL - FAILED)) applied, $FAILED rejected of $TOTAL (rejects in $REJ)"
[ "$((TOTAL - FAILED))" -gt 0 ]

#!/bin/bash
# Tüpflischiisser (vq-put.sh): enqueue one row on a running verify-server.
#
#   vq-put.sh <W> <tree.tgz> <expected ops.bin sha256>
#
# environment: VQ_SESSION (the Colab session name of the verifier), VQ_CONFIG (that session's colab CLI state file,
# as printed by the supervisor that started it), VQ_DIR (local queue folder, default ./vq).
# The tree archive is `git archive` of the row's commit (no .git). The .ready file is uploaded LAST: the server
# only picks a row up when all three files are there.
set -u
W=${1:?width}; T=${2:?tree.tgz}; S=${3:?sha}
name=${VQ_SESSION:?set VQ_SESSION}; cfg=${VQ_CONFIG:?set VQ_CONFIG}; VQ=${VQ_DIR:-./vq}
[ -f "$cfg" ] || { echo "no session state file ($cfg)" >&2; exit 3; }
echo "$S" | grep -q -E '^[0-9a-f]{64}$' || { echo "bad sha" >&2; exit 2; }
[ -s "$T" ] || { echo "no tree archive $T" >&2; exit 2; }
tar tzf "$T" 2>/dev/null | grep -q -E '^(\./)?Cargo.toml$' || { echo "tree archive has no top-level Cargo.toml" >&2; exit 2; }
d=$VQ/put/w$W; mkdir -p "$d"
cp "$T" "$d/row$W.tree.tgz"; echo "$S" > "$d/row$W.sha"; date -u +%FT%TZ > "$d/row$W.ready"
up() { # up <file>: upload with a 180 s limit, three tries
  local f=$1 try
  for try in 1 2 3; do
    if perl -e 'alarm shift; exec @ARGV' 180 colab --auth=oauth2 --config "$cfg" upload -s "$name" "$d/$f" "/content/q/$f" </dev/null >> "$d/upload.log" 2>&1; then return 0; fi
    sleep 15
  done
  return 1
}
for f in "row$W.tree.tgz" "row$W.sha" "row$W.ready"; do
  up "$f" || { echo "upload of $f failed (see $d/upload.log)" >&2; exit 4; }
done
echo "enqueued row $W on $name at $(date -u +%FT%TZ)" | tee -a "$VQ/put.log"

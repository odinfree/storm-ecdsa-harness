#!/usr/bin/env python3
"""Müschterli (recipe.py): make a probe tree from a source tree and a recipe, with every edit applied exactly once.

usage: recipe.py SRC DST RECIPE.json [NAME=value ...]

RECIPE.json:
{
  "copy":   [["from/file", "dst/relative/path"], ...],        optional; "from" is relative to the recipe's folder
  "remove": ["dst/relative/path", ...],                         optional
  "edits":  {"src/point_add/mod.rs": [["old text", "new text"], ...], ...}
}
Every "old text" must occur EXACTLY ONCE in its file, else the run stops and names the edit. {NAME} in any string is
replaced by the value given on the command line; an unknown {NAME} stops the run.

Why exactly once: a constant renamed upstream, a line that moved, or a second copy of a snippet turns a silent
`sed` into a no-op or a double edit, and the probe tree then measures something other than what its name says.
DST is replaced (rsync --delete, target/ and .git excluded). Prints a manifest: every file touched with its sha256.
"""
import hashlib, json, os, shutil, subprocess, sys

def main():
    if len(sys.argv) < 4: sys.exit(__doc__)
    src, dst, rp = sys.argv[1], sys.argv[2], sys.argv[3]
    params = dict(a.split('=', 1) for a in sys.argv[4:])
    def fill(s):
        try: return s.format(**params) if params or '{' in s else s
        except (KeyError, IndexError, ValueError) as e: sys.exit(f'recipe: unfilled or malformed placeholder in {s[:60]!r}: {e}')
    recipe = json.load(open(rp)); base = os.path.dirname(os.path.abspath(rp))
    # --checksum: size and mtime can coincide between a base file and its edited copy made in the same second
    subprocess.run(['rsync', '-a', '--checksum', '--delete', '--exclude', 'target', '--exclude', '.git', src.rstrip('/') + '/', dst.rstrip('/') + '/'], check=True)
    touched = []
    for a, b in recipe.get('copy', []):
        p = os.path.join(dst, fill(b)); os.makedirs(os.path.dirname(p), exist_ok=True); shutil.copy(os.path.join(base, fill(a)), p); touched.append(fill(b))
    for b in recipe.get('remove', []):
        os.remove(os.path.join(dst, fill(b))); print('removed', fill(b))
    for rel, reps in recipe.get('edits', {}).items():
        p = os.path.join(dst, fill(rel)); s = open(p).read()
        for k, (old, new) in enumerate(reps):
            old, new = fill(old), fill(new); c = s.count(old)
            if c != 1: sys.exit(f'recipe: edit {k} of {rel} matches {c} times, need exactly 1: {old[:70]!r}')
            s = s.replace(old, new)
        open(p, 'w').write(s); touched.append(fill(rel))
    for rel in touched:
        print(hashlib.sha256(open(os.path.join(dst, rel), 'rb').read()).hexdigest(), rel)
    print('made', dst)

if __name__ == '__main__':
    main()

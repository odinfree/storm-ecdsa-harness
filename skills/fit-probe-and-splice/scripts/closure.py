#!/usr/bin/env python3
"""closure.py: copy a source file and every file it references, transitively, into a destination.

Usage:
  closure.py <entry-file> <dest> [--root DIR] [--pattern REGEX ...] [--dry-run]
  closure.py --selftest

References followed (paths are relative to the referencing file unless noted):
  Rust     #[path = "f.rs"] mod m;     include!("f")   include_str!("f")   include_bytes!("f")
           mod m;  (m.rs or m/mod.rs next to the file; for a non-mod.rs file also <stem>/m.rs)
  C, C++   #include "f"
  other    each --pattern REGEX whose group 1 is a relative path
A referenced directory is copied whole. Only text sources are parsed; data files are
copied as they are. Line and block comments are ignored.

Files keep their path relative to --root (default: the common parent of the closure).
The manifest (sha256, bytes, path) goes to stdout; record it with the port.
Exit code 1 when a reference cannot be resolved or lies outside --root: the list is
printed, because each such item is something the module reads from its home tree.
"""
import argparse
import hashlib
import os
import re
import shutil
import sys

TEXT_EXT = {".rs", ".c", ".h", ".cc", ".cpp", ".hpp", ".inc", ".in"}
INCLUDE = re.compile(r'\b(?:include|include_str|include_bytes)!\s*\(\s*"([^"]+)"\s*\)')
C_INCLUDE = re.compile(r'^\s*#\s*include\s+"([^"]+)"', re.M)
MOD = re.compile(r'((?:#\[[^\]]*\]\s*)*)(?:pub(?:\([^)]*\))?\s+)?mod\s+([A-Za-z_][A-Za-z0-9_]*)\s*;')
PATH_ATTR = re.compile(r'#\[\s*path\s*=\s*"([^"]+)"\s*\]')


def strip_comments(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"(?<!:)//[^\n]*", "", text)


def references(path, patterns):
    """Yield (candidate paths in order of preference, label) for each reference in one file."""
    if os.path.splitext(path)[1] not in TEXT_EXT:
        return
    try:
        with open(path, encoding="utf-8") as f:
            text = strip_comments(f.read())
    except UnicodeDecodeError:
        return
    here = os.path.dirname(path)
    for m in INCLUDE.finditer(text):
        yield [os.path.join(here, m.group(1))], m.group(0)
    for m in C_INCLUDE.finditer(text):
        yield [os.path.join(here, m.group(1))], m.group(0).strip()
    for rx in patterns:
        for m in rx.finditer(text):
            yield [os.path.join(here, m.group(1))], m.group(0)
    if path.endswith(".rs"):
        stem = os.path.splitext(os.path.basename(path))[0]
        for m in MOD.finditer(text):
            attr = PATH_ATTR.search(m.group(1))
            name = m.group(2)
            if attr:
                yield [os.path.join(here, attr.group(1))], "#[path] mod %s" % name
                continue
            dirs = [here] if stem in ("mod", "lib", "main") else [os.path.join(here, stem), here]
            cands = []
            for d in dirs:
                cands += [os.path.join(d, name + ".rs"), os.path.join(d, name, "mod.rs")]
            yield cands, "mod %s;" % name


def closure(entry, patterns):
    entry = os.path.realpath(entry)
    files, unresolved, queue = [], [], [entry]
    seen = {entry}
    while queue:
        path = queue.pop(0)
        files.append(path)
        for cands, label in references(path, patterns):
            hit = next((os.path.realpath(c) for c in cands if os.path.exists(c)), None)
            if hit is None:
                unresolved.append((path, label))
                continue
            found = [hit]
            if os.path.isdir(hit):
                found = sorted(os.path.join(dp, fn) for dp, _, fns in os.walk(hit) for fn in fns)
            for f in found:
                if f not in seen:
                    seen.add(f)
                    queue.append(f)
    return files, unresolved


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_closure(entry, dest, root=None, patterns=(), dry_run=False, out=sys.stdout, err=sys.stderr):
    files, unresolved = closure(entry, patterns)
    root = os.path.realpath(root) if root else os.path.commonpath([os.path.dirname(f) for f in files])
    outside = [f for f in files if os.path.commonpath([root, f]) != root]
    total = 0
    for f in sorted(files):
        if f in outside:
            continue
        rel = os.path.relpath(f, root)
        size = os.path.getsize(f)
        total += size
        out.write("%s\t%d\t%s\n" % (sha256(f), size, rel))
        if not dry_run:
            target = os.path.join(dest, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copyfile(f, target)
    err.write("%d files, %d bytes, root %s%s\n" % (len(files) - len(outside), total, root, " (dry run)" if dry_run else ""))
    for path, label in unresolved:
        err.write("UNRESOLVED in %s: %s\n" % (os.path.relpath(path, root), label))
    for f in outside:
        err.write("OUTSIDE ROOT, not copied: %s\n" % f)
    return 1 if unresolved or outside else 0


def selftest():
    import io
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        src, dst = os.path.join(d, "donor", "src"), os.path.join(d, "dst")
        tree = {
            "port/mod.rs": '#[path = "../lf/core.rs"]\nmod core;\nmod helper;\npub mod deep;\n'
                           '// mod commented_out;\n/* include!("nope.rs") */\n'
                           'const T: &str = include_str!("data/table.txt");\n'
                           'const B: &[u8] = include_bytes!("data/blob.bin");\ninclude!("gen.in");\n',
            "port/helper.rs": "mod inner;\nfn h() {}\n",
            "port/helper/inner.rs": "fn i() {}\n",
            "port/deep/mod.rs": 'include!("../shared.inc");\n',
            "port/shared.inc": '#include "c/defs.h"\n',
            "port/c/defs.h": "#define N 1\n",
            "port/gen.in": "fn g() {}\n",
            "port/data/table.txt": "1 2 3\n",
            "lf/core.rs": "fn c() {}\n",
            "unrelated.rs": "fn u() {}\n",
        }
        for rel, text in tree.items():
            p = os.path.join(src, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as f:
                f.write(text)
        with open(os.path.join(src, "port/data/blob.bin"), "wb") as f:
            f.write(bytes(range(256)))
        entry = os.path.join(src, "port/mod.rs")
        buf = io.StringIO()
        rc = copy_closure(entry, dst, out=buf, err=io.StringIO())
        copied = sorted(os.path.relpath(os.path.join(dp, fn), dst) for dp, _, fns in os.walk(dst) for fn in fns)
        want = sorted(k for k in list(tree) + ["port/data/blob.bin"] if k != "unrelated.rs")
        assert rc == 0, "complete tree must resolve"
        assert copied == want, (copied, want)
        for rel in copied:
            assert sha256(os.path.join(dst, rel)) == sha256(os.path.join(src, rel)), rel
        print("[1/3] %d files copied byte for byte; #[path], mod, nested mod, include!, include_str!, include_bytes!, #include followed" % len(copied))
        print("      unrelated.rs and commented-out references left alone")
        with open(os.path.join(src, "port/helper.rs"), "a") as f:
            f.write('mod missing;\nconst P: &str = include_str!("../../outside.txt");\n')
        with open(os.path.join(d, "donor", "outside.txt"), "w") as f:
            f.write("home-tree global\n")
        err = io.StringIO()
        rc = copy_closure(entry, os.path.join(d, "dst2"), root=src, out=io.StringIO(), err=err)
        assert rc == 1, "a missing module and a file outside the root must give exit 1"
        assert "UNRESOLVED in port/helper.rs: mod missing;" in err.getvalue(), err.getvalue()
        assert "OUTSIDE ROOT, not copied" in err.getvalue() and "outside.txt" in err.getvalue()
        assert not os.path.exists(os.path.join(d, "dst2", "outside.txt"))
        print("[2/3] negative case: missing module and outside-root file reported, exit 1")
        rc = copy_closure(entry, os.path.join(d, "dst3"), root=os.path.join(d, "donor"), dry_run=True, out=io.StringIO(), err=io.StringIO())
        assert rc == 1 and not os.path.exists(os.path.join(d, "dst3")), "dry run must not write"
        print("[3/3] dry run writes nothing")
    print("closure selftest: PASS")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("entry", nargs="?")
    p.add_argument("dest", nargs="?")
    p.add_argument("--root")
    p.add_argument("--pattern", action="append", default=[])
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not (a.entry and a.dest):
        print(__doc__)
        return 2
    return copy_closure(a.entry, a.dest, a.root, [re.compile(x) for x in a.pattern], a.dry_run)


if __name__ == "__main__":
    sys.exit(main())

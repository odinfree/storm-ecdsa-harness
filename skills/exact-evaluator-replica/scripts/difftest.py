#!/usr/bin/env python3
"""difftest.py: differential test of a replica against the official judge on random artefacts.

Usage:
  difftest.py --gen 'CMD {out} {n} {seed}' --judge 'CMD {artefact}' --replica 'CMD {artefact}'
              --field LABEL [--field LABEL ...]
              [--side-file PATH --side-col COL=LABEL ...] [--n N] [--keep DIR] SEED [SEED ...]
  difftest.py --selftest

For each seed it generates one artefact, runs both programs on it in a fresh work
directory, and compares fields as exact strings. A field's value is the last
whitespace-separated token of the first output line that contains LABEL. A field
that is missing on both sides counts as a mismatch.

--side-file names a file the judge appends a result row to (relative paths are taken
in the work directory, absolute paths are snapshotted and restored afterwards).
--side-col 3=LABEL takes the judge's value for LABEL from tab-separated column 3 of
that file's last row instead of the judge's stdout. Use it for averages a judge
records only there when the artefact fails.

A non-zero exit of the judge or the replica is not an error: random artefacts fail.
Exit code: 0 and "all seeds match" when every field matches on every seed; 1 on any
mismatch; 2 on a usage or generator error.
"""
import argparse
import os
import shlex
import shutil
import subprocess
import sys
import tempfile


def run(template, cwd, **kw):
    cmd = [part.format(**kw) for part in shlex.split(template)]
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout


def field(text, label):
    for line in text.splitlines():
        if label in line and line.split():
            return line.split()[-1]
    return None


def difftest(a):
    side_cols = {}
    for item in a.side_col:
        col, _, label = item.partition("=")
        side_cols[label] = int(col)
    labels = list(a.field) + [l for l in side_cols if l not in a.field]
    if not labels:
        print("no --field given", file=sys.stderr)
        return 2
    work = a.keep or tempfile.mkdtemp(prefix="difftest-")
    os.makedirs(work, exist_ok=True)
    backup = None
    if a.side_file and os.path.isabs(a.side_file) and os.path.exists(a.side_file):
        backup = os.path.join(work, "side-file.bak")
        shutil.copy2(a.side_file, backup)
    failed = False
    try:
        for seed in a.seeds:
            d = os.path.join(work, "s%s" % seed)
            os.makedirs(d, exist_ok=True)
            art = os.path.join(d, "artefact")
            rc, out = run(a.gen, d, out=art, n=a.n, seed=seed)
            if rc != 0 or not os.path.exists(art):
                print("seed %s: generator failed\n%s" % (seed, out), file=sys.stderr)
                return 2
            _, jout = run(a.judge, d, artefact=art)
            _, rout = run(a.replica, d, artefact=art)
            row = []
            if a.side_file:
                sf = a.side_file if os.path.isabs(a.side_file) else os.path.join(d, a.side_file)
                if os.path.exists(sf):
                    with open(sf) as f:
                        rows = [ln for ln in f.read().splitlines() if ln]
                    row = rows[-1].split("\t") if rows else []
            diffs, shown = [], []
            for label in labels:
                if label in side_cols:
                    c = side_cols[label]
                    jv = row[c - 1] if 0 < c <= len(row) else None
                else:
                    jv = field(jout, label)
                rv = field(rout, label)
                shown.append("%s=%s" % (label, rv))
                if jv is None or rv is None or jv != rv:
                    diffs.append("  %-28s judge=%s replica=%s" % (label, jv, rv))
            if diffs:
                failed = True
                print("seed %s: MISMATCH" % seed)
                print("\n".join(diffs))
            else:
                print("seed %s: MATCH  (%s)" % (seed, ", ".join(shown)))
    finally:
        if a.side_file and os.path.isabs(a.side_file):
            if backup:
                shutil.copy2(backup, a.side_file)
            elif os.path.exists(a.side_file):
                os.remove(a.side_file)
        if not a.keep:
            shutil.rmtree(work, ignore_errors=True)
    if failed:
        print("MISMATCH found", file=sys.stderr)
        return 1
    print("all seeds match")
    return 0


def parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--gen")
    p.add_argument("--judge")
    p.add_argument("--replica")
    p.add_argument("--field", action="append", default=[])
    p.add_argument("--side-file")
    p.add_argument("--side-col", action="append", default=[])
    p.add_argument("--n", default="20000")
    p.add_argument("--keep")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("seeds", nargs="*")
    return p


def selftest():
    here = os.path.dirname(os.path.abspath(__file__))
    py = shlex.quote(sys.executable)
    toy, gen = shlex.quote(os.path.join(here, "toy_bench.py")), shlex.quote(os.path.join(here, "gensynth.py"))
    base = ["--gen", "%s %s {out} {n} {seed} --require-coverage" % (py, gen),
            "--judge", "%s %s judge {artefact}" % (py, toy),
            "--field", "tested samples", "--field", "wrong outputs", "--field", "dirty-scratch batches",
            "--side-file", "results.tsv",
            "--side-col", "1=avg executed charged", "--side-col", "2=avg executed free",
            "--side-col", "3=wires", "--side-col", "4=emitted ops", "--n", "3000"]
    seeds = ["11", "22", "33"]
    print("[1/4] exact replica against the toy judge, random artefacts")
    rc = difftest(parser().parse_args(base + ["--replica", "%s %s replica {artefact}" % (py, toy)] + seeds))
    assert rc == 0, "exact replica must match"
    for k, what in ((1, "conditioned measuring ops skip their read (stream misalignment)"),
                    (2, "charge counted only when the controls are set")):
        print("[%d/4] negative control: replica with injected defect %d, %s" % (k + 1, k, what))
        rc = difftest(parser().parse_args(base + ["--replica", "%s %s replica {artefact} --bug %d" % (py, toy, k)] + seeds))
        assert rc == 1, "defect %d must be reported as a mismatch" % k
    print("[4/4] absolute side file is restored after the run")
    with tempfile.TemporaryDirectory() as d:
        side = os.path.join(d, "results.tsv")
        with open(side, "w") as f:
            f.write("keep\tme\n")
        wrap = os.path.join(d, "judge_here.py")       # a judge that always writes into d
        with open(wrap, "w") as f:
            f.write("import os, subprocess, sys\nos.chdir(%r)\n"
                    "sys.exit(subprocess.call([sys.executable, %r, 'judge', sys.argv[1]]))\n"
                    % (d, os.path.join(here, "toy_bench.py")))
        args = list(base)
        args[args.index("--judge") + 1] = "%s %s {artefact}" % (py, shlex.quote(wrap))
        args[args.index("--side-file") + 1] = side
        rc = difftest(parser().parse_args(args + ["--replica", "%s %s replica {artefact}" % (py, toy), "11"]))
        with open(side) as f:
            assert rc == 0 and f.read() == "keep\tme\n", "side file must be restored"
    print("difftest selftest: PASS (match on exact replica, mismatch on both defects, side file restored)")
    return 0


def main():
    a = parser().parse_args()
    if a.selftest:
        return selftest()
    if not (a.gen and a.judge and a.replica and a.seeds):
        print(__doc__)
        return 2
    return difftest(a)


if __name__ == "__main__":
    sys.exit(main())

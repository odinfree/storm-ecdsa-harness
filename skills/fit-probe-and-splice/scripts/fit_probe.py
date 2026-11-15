#!/usr/bin/env python3
"""fit_probe.py: build one module alone at a list of caps (or pool sizes) and tabulate the result.

Usage:
  fit_probe.py --cmd 'BUILD COMMAND with {cap}' --caps 825,830,840:852:4 [--label NAME]
               [--peak-re REGEX] [--cost-re REGEX] [--room N] [--cliff FRACTION] [--tsv FILE]
  fit_probe.py --selftest

For every value in --caps (comma list; a:b:step ranges allowed, b inclusive) it runs
the command with {cap} replaced and reads two numbers from its output:
  peak   first group of --peak-re   (default: peak[ =:]+(\\d+))
  cost   first group of --cost-re   (default: cost[ =:]+([0-9.]+))
A non-zero exit is "does not build"; the last output line is kept as the reason.

--room N    dry-build sizing: report the largest probed value whose measured peak is
            at most N. Use it with the pool size as the swept value and N = cap minus
            live resources at the call site.
--cliff F   flag adjacent values where cost rises by more than fraction F (default 0.2)
            going down; test the adapter on both sides of each flagged pair.
Exit code: 0 when at least one value builds (and, with --room, one fits); 1 otherwise.
"""
import argparse
import re
import shlex
import subprocess
import sys


def parse_caps(text):
    out = []
    for part in text.split(","):
        if ":" in part:
            p = [int(x) for x in part.split(":")]
            out += list(range(p[0], p[1] + 1, p[2] if len(p) > 2 else 1))
        elif part:
            out.append(int(part))
    return out


def probe(cmd, caps, peak_re, cost_re):
    rows = []
    for cap in caps:
        p = subprocess.run([x.format(cap=cap) for x in shlex.split(cmd)],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        lines = [ln for ln in p.stdout.splitlines() if ln.strip()]
        pk, co = re.search(peak_re, p.stdout), re.search(cost_re, p.stdout)
        if p.returncode != 0:
            rows.append((cap, False, None, None, lines[-1].strip() if lines else "exit %d" % p.returncode))
        else:
            rows.append((cap, True, int(pk.group(1)) if pk else None, float(co.group(1)) if co else None, ""))
    return rows


def report(rows, label, room, cliff, tsv=None, out=sys.stdout):
    out.write("%-14s %8s %-15s %8s %14s  %s\n" % ("block", "cap", "result", "peak", "cost", "note"))
    for cap, ok, pk, co, why in rows:
        out.write("%-14s %8d %-15s %8s %14s  %s\n" % (
            label, cap, "builds" if ok else "does not build", "-" if pk is None else pk,
            "-" if co is None else ("%.1f" % co), why))
    built = sorted((r for r in rows if r[1] and r[3] is not None), key=lambda r: r[0])
    for lo, hi in zip(built, built[1:]):
        if lo[3] > hi[3] * (1 + cliff):
            out.write("cliff: cost %.1f at %d vs %.1f at %d; test both sides\n" % (lo[3], lo[0], hi[3], hi[0]))
    if tsv:
        with open(tsv, "w") as f:
            f.write("block\tcap\tbuilds\tpeak\tcost\tnote\n")
            for cap, ok, pk, co, why in rows:
                f.write("%s\t%d\t%s\t%s\t%s\t%s\n" % (label, cap, "yes" if ok else "no",
                                                      "" if pk is None else pk, "" if co is None else co, why))
    pick = None
    if room is not None:
        fits = [r for r in rows if r[1] and r[2] is not None and r[2] <= room]
        if fits:
            pick = max(fits, key=lambda r: r[0])
            out.write("largest value whose measured peak fits room %d: %d (peak %d, cost %s)\n" %
                      (room, pick[0], pick[2], "-" if pick[3] is None else "%.1f" % pick[3]))
        else:
            out.write("no probed value fits room %d\n" % room)
    ok = any(r[1] for r in rows) and (room is None or pick is not None)
    return (0 if ok else 1), pick


def selftest():
    import io
    import os
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        toy = os.path.join(d, "toy_build.py")
        with open(toy, "w") as f:      # a module that needs 40 units, is costly below 47, and peaks at pool + 3
            f.write("import sys\npool = int(sys.argv[1])\n"
                    "if pool < 40:\n    print('error: constant fold must fit its remaining room'); sys.exit(1)\n"
                    "print('built: peak=%d cost=%.1f' % (pool + 3, (89480.0 if pool < 47 else 59580.5) - pool))\n")
        cmd = "%s %s {cap}" % (shlex.quote(sys.executable), shlex.quote(toy))
        rows = probe(cmd, parse_caps("36,38,44:48,55"), r"peak[ =:]+(\d+)", r"cost[ =:]+([0-9.]+)")
        buf = io.StringIO()
        rc, pick = report(rows, "toy-square", 50, 0.2, os.path.join(d, "fit.tsv"), buf)
        sys.stdout.write(buf.getvalue())
        text = buf.getvalue()
        assert rc == 0 and pick[0] == 47, pick
        assert text.count("does not build") == 2 and "must fit its remaining room" in text
        assert "cliff: cost 89434.0 at 46 vs 59533.5 at 47" in text
        with open(os.path.join(d, "fit.tsv")) as f:
            assert len(f.read().splitlines()) == 9
        print("[1/2] table, cliff between 46 and 47, and dry-build pick (47 under room 50) are right")
        rc, pick = report(probe(cmd, [30, 36], r"peak[ =:]+(\d+)", r"cost[ =:]+([0-9.]+)"), "toy-square", None, 0.2, None, io.StringIO())
        rc2, _ = report(rows, "toy-square", 40, 0.2, None, io.StringIO())
        assert rc == 1 and rc2 == 1
        print("[2/2] negative cases: nothing builds, and nothing fits room 40, both give exit 1")
    print("fit_probe selftest: PASS")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cmd")
    p.add_argument("--caps")
    p.add_argument("--label", default="module")
    p.add_argument("--peak-re", default=r"peak[ =:]+(\d+)")
    p.add_argument("--cost-re", default=r"cost[ =:]+([0-9.]+)")
    p.add_argument("--room", type=int)
    p.add_argument("--cliff", type=float, default=0.2)
    p.add_argument("--tsv")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not (a.cmd and a.caps):
        print(__doc__)
        return 2
    rc, _ = report(probe(a.cmd, parse_caps(a.caps), a.peak_re, a.cost_re), a.label, a.room, a.cliff, a.tsv)
    return rc


if __name__ == "__main__":
    sys.exit(main())

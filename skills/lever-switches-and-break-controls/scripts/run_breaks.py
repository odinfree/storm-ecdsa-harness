#!/usr/bin/env python3
"""run_breaks.py: run every numbered break control of one lever and report which the test catches.

Usage:
  run_breaks.py --name NAME --max N [--state FILE] [--expect REGEX] [--accept]
                [--strict] [--timeout SEC] -- TEST COMMAND ...
  run_breaks.py --selftest

It runs TEST COMMAND once with NAME_BREAK unset; that run must pass, otherwise a
failing control proves nothing (exit 2). Then for n = 1..N it sets NAME_BREAK=n in
the environment and runs the command again.

  caught       the command failed (and its output matched --expect, when given)
  NOT CAUGHT   the command passed: the test cannot see this obligation. Disclose the
               control as not claimed, or strengthen the test, or raise the scale.
  other fail   the command failed without matching --expect (a build error, a crash
               in another test). It does not count as caught.

--state FILE keeps the last result per control (TSV). A control recorded as caught
that now passes is a REGRESSION: exit 1, and the record stays "caught" until you
re-run with --accept. --strict also exits 1 when any control is not caught.
Exit codes: 0 no regression; 1 regression (or --strict and a gap); 2 baseline failed
or usage error.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys


def run(cmd, env, timeout):
    try:
        p = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout)
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired as e:
        return 124, (e.stdout or "") + "\n[timeout]"


def load_state(path):
    state = {}
    if path and os.path.exists(path):
        with open(path) as f:
            for line in f:
                p = line.rstrip("\n").split("\t")
                if len(p) >= 2 and p[0] != "control":
                    state[p[0]] = p[1]
    return state


def run_breaks(a):
    if a.cmd and a.cmd[0] == "--":
        a.cmd = a.cmd[1:]
    if not (a.name and a.max and a.cmd):
        print(__doc__)
        return 2
    var = a.name + "_BREAK"
    env = {k: v for k, v in os.environ.items() if k != var}
    rc, _ = run(a.cmd, env, a.timeout)
    if rc != 0:
        print("baseline run (no %s) FAILED with exit %d: fix the test before running controls" % (var, rc))
        return 2
    print("baseline run (no %s): pass" % var)
    state = load_state(a.state)
    results, regress, gaps = {}, [], []
    print("%-18s %-11s %s" % ("control", "result", "previous"))
    for n in range(1, a.max + 1):
        key = "%s=%d" % (var, n)
        e = dict(env)
        e[var] = str(n)
        rc, out = run(a.cmd, e, a.timeout)
        if rc == 0:
            res = "NOT CAUGHT"
        elif a.expect and not re.search(a.expect, out):
            res = "other fail"
        else:
            res = "caught"
        prev = state.get(key, "-")
        note = prev
        if prev == "caught" and res != "caught":
            regress.append(key)
            note = "caught  <-- REGRESSION"
        if res != "caught":
            gaps.append(key)
        results[key] = res
        print("%-18s %-11s %s" % (key, res, note))
    caught = sum(1 for r in results.values() if r == "caught")
    print("%d of %d controls caught" % (caught, a.max))
    if gaps:
        print("not claimed unless fixed: %s" % ", ".join(gaps))
    if a.state:
        merged = dict(state)
        for key, res in results.items():
            if key in regress and not a.accept:
                continue                      # keep "caught" so the regression keeps failing
            merged[key] = res
        with open(a.state, "w") as f:
            f.write("control\tresult\tdate\n")
            today = datetime.date.today().isoformat()
            for key in sorted(merged, key=lambda k: (k.split("=")[0], int(k.split("=")[1]))):
                f.write("%s\t%s\t%s\n" % (key, merged[key], today))
    if regress and not a.accept:
        print("REGRESSION: previously caught, now passing: %s" % ", ".join(regress))
        return 1
    if a.strict and gaps:
        return 1
    return 0


def parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name")
    p.add_argument("--max", type=int)
    p.add_argument("--state")
    p.add_argument("--expect")
    p.add_argument("--accept", action="store_true")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--timeout", type=float, default=None)
    p.add_argument("--selftest", action="store_true")
    p.add_argument("cmd", nargs=argparse.REMAINDER)
    return p


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        test = os.path.join(d, "toy_test.py")
        state = os.path.join(d, "breaks.tsv")

        def write(caught, baseline_ok=True):
            with open(test, "w") as f:
                f.write("import os, sys\nb = os.environ.get('SP_BREAK')\n"
                        "if b is None: sys.exit(%d)\n"
                        "if b == '5': print('error: build failed'); sys.exit(101)\n"
                        "if b in %r: print('assertion failed: frame flip'); sys.exit(1)\n"
                        "sys.exit(0)\n" % (0 if baseline_ok else 1, caught))

        base = ["--name", "SP", "--max", "5", "--state", state, "--expect", "assertion failed", "--", sys.executable, test]
        print("[1/4] controls 1-3 caught, 4 is a blind spot, 5 fails for another reason")
        write(("1", "2", "3"))
        assert run_breaks(parser().parse_args(base)) == 0
        st = load_state(state)
        assert st == {"SP_BREAK=1": "caught", "SP_BREAK=2": "caught", "SP_BREAK=3": "caught",
                      "SP_BREAK=4": "NOT CAUGHT", "SP_BREAK=5": "other fail"}, st
        print("[2/4] --strict turns the blind spot into a failing exit")
        assert run_breaks(parser().parse_args(["--strict"] + base)) == 1
        print("[3/4] negative case: control 2 stops failing, must be reported as a regression")
        write(("1", "3"))
        assert run_breaks(parser().parse_args(base)) == 1
        assert load_state(state)["SP_BREAK=2"] == "caught", "record must stay caught until accepted"
        assert run_breaks(parser().parse_args(base)) == 1, "regression must persist"
        assert run_breaks(parser().parse_args(["--accept"] + base)) == 0
        assert load_state(state)["SP_BREAK=2"] == "NOT CAUGHT"
        print("[4/4] negative case: failing baseline stops the run")
        write(("1", "2", "3"), baseline_ok=False)
        assert run_breaks(parser().parse_args(base)) == 2
    print("run_breaks selftest: PASS")
    return 0


def main():
    a = parser().parse_args()
    if a.selftest:
        return selftest()
    return run_breaks(a)


if __name__ == "__main__":
    sys.exit(main())

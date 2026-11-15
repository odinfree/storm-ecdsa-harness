#!/usr/bin/env python3
"""diag.py: one reference model used as rate estimator, table generator, replayer and seed scanner.

Usage:
  diag.py rate      --n N [--seed S] [--table FILE] [--per-artefact K]
  diag.py envelope  --n N --out FILE [--seed S] [--margin M]
  diag.py envelope  --n N --check FILE [--seed S] [--margin M]     regenerate and compare
  diag.py replay    --artefact PATH [--table FILE]
  diag.py scan      --artefact PATH --start C --want K [--limit L] [--table FILE]
  diag.py blindspot --model FILE --replica FILE      one "seed index" pair per line in each file
  diag.py --selftest
  Add --model-file my_model.py to any command to use your model instead of the toy one.

A model file is a Python module with:
  CLASSES                      list of failure-class names
  STREAM_BYTES                 bytes of seed stream needed for one artefact's inputs
  sample_input(rng)            one random input (rng is random.Random)
  spec(inp)                    the integer specification's result
  run(inp, table)              layout model: (result, None) or (None, failure_class)
  trace(inp)                   per-step values the table must bound (for the envelope)
  split(artefact_bytes)        (prefix_bytes, tail_bytes): the tail is what a seed candidate changes
  tail(candidate)              tail bytes for integer candidate
  seed_hasher()                a fresh hashlib XOF with the judge's domain tag absorbed
  inputs(stream_bytes)         the judge's inputs for one artefact, in order

The built-in toy model: Euclid's algorithm on two 24-bit numbers, run in fixed slots
with a per-slot bound on the quotient's bit length. Its integer specification is
math.gcd. Failure classes: "slots" (the walk needs more slots than the table has)
and "window" (a quotient is wider than its slot's bound).
"""
import argparse
import hashlib
import importlib.util
import math
import random
import sys


class ToyModel:
    CLASSES = ["slots", "window"]
    PER_ARTEFACT = 64
    STREAM_BYTES = 6 * 64

    @staticmethod
    def sample_input(rng):
        return rng.randrange(1, 1 << 24), rng.randrange(1, 1 << 24)

    @staticmethod
    def spec(inp):
        return math.gcd(*inp)

    @staticmethod
    def trace(inp):
        a, b = inp
        out = []
        while b:
            out.append((a // b).bit_length())
            a, b = b, a % b
        return out

    @staticmethod
    def run(inp, table):
        a, b = inp
        for bound in table:
            if b == 0:
                return a, None
            if (a // b).bit_length() > bound:
                return None, "window"
            a, b = b, a % b
        return (a, None) if b == 0 else (None, "slots")

    @staticmethod
    def split(data):
        return data[:-8], data[-8:]

    @staticmethod
    def tail(candidate):
        return candidate.to_bytes(8, "little")

    @staticmethod
    def seed_hasher():
        h = hashlib.shake_256()
        h.update(b"toy-diag-v1")
        return h

    @staticmethod
    def inputs(stream):
        f = lambda i: (int.from_bytes(stream[i:i + 3], "little") or 1)
        return [(f(6 * k), f(6 * k + 3)) for k in range(len(stream) // 6)]


def load_model(path):
    if not path:
        return ToyModel
    spec = importlib.util.spec_from_file_location("user_model", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_table(path):
    with open(path) as f:
        return [int(x) for x in f.read().split()]


def make_envelope(model, n, seed, margin):
    rng = random.Random("envelope:%d" % seed)   # its own stream: a table is never scored on its fitting sample
    table = []
    for _ in range(n):
        for i, v in enumerate(model.trace(model.sample_input(rng))):
            if i == len(table):
                table.append(v)
            elif v > table[i]:
                table[i] = v
    return [v + margin for v in table]


def rate(model, table, n, seed):
    """Failure count per class on n fresh inputs; also checks the model against the specification."""
    rng = random.Random("rate:%d" % seed)
    counts = {c: 0 for c in model.CLASSES}
    for _ in range(n):
        inp = model.sample_input(rng)
        res, cls = model.run(inp, table)
        if cls is None:
            if res != model.spec(inp):
                raise AssertionError("model disagrees with the specification on %r" % (inp,))
        else:
            counts[cls] += 1
    return counts


def report_rate(counts, n, per_artefact):
    total = sum(counts.values())
    se = lambda k: math.sqrt(max(k, 1)) / n          # Poisson standard error; 1 event floor
    print("%-10s %8s %12s %12s %s" % ("class", "fails", "rate", "std err", "per artefact (%d inputs)" % per_artefact))
    for c, k in list(counts.items()) + [("total", total)]:
        print("%-10s %8d %12.3e %12.3e %.3f +- %.3f" % (c, k, k / n, se(k), per_artefact * k / n, per_artefact * se(k)))


def artefact_failures(model, table, hasher_with_prefix, tail, first_only):
    """Indices and classes of failing inputs for one artefact; stops at the first when first_only."""
    h = hasher_with_prefix.copy()                  # the prefix was absorbed once; only the tail is fed here
    h.update(tail)
    fails = []
    for i, inp in enumerate(model.inputs(h.digest(model.STREAM_BYTES))):
        _, cls = model.run(inp, table)
        if cls is not None:
            fails.append((i, cls))
            if first_only:
                break
    return fails


def prefix_hasher(model, prefix):
    h = model.seed_hasher()
    h.update(prefix)
    return h


def replay(model, table, data):
    prefix, tail = model.split(data)
    return artefact_failures(model, table, prefix_hasher(model, prefix), tail, False)


def scan(model, table, data, start, want, limit):
    prefix, _ = model.split(data)
    base = prefix_hasher(model, prefix)
    clean, c = [], start
    while len(clean) < want and c < start + limit:
        if not artefact_failures(model, table, base, model.tail(c), True):
            clean.append(c)
        c += 1
    return clean, c - start


def blindspot(model_pairs, replica_pairs, seeds):
    both = model_pairs & replica_pairs
    return {"predicted and observed": len(both), "observed, not predicted": len(replica_pairs - model_pairs),
            "predicted, not observed": len(model_pairs - replica_pairs), "seeds": seeds}


def read_pairs(path):
    with open(path) as f:
        rows = [tuple(ln.split()[:2]) for ln in f if ln.strip() and not ln.startswith("#")]
    return set(rows), len({r[0] for r in rows})


def selftest():
    import os
    import tempfile
    m = ToyModel
    print("[1/6] envelope: regenerating from the same seed reproduces the table")
    table = make_envelope(m, 20000, 1, 0)
    assert table == make_envelope(m, 20000, 1, 0)
    print("      %d slots, bounds %s..." % (len(table), table[:8]))
    print("[2/6] rate: model equals the integer specification on every passing input")
    counts = rate(m, table, 200000, 1)
    assert sum(counts.values()) > 0, "same default seed for envelope and rate must still draw fresh inputs"
    report_rate(counts, 200000, m.PER_ARTEFACT)
    print("[3/6] negative case: a table fitted on too few samples fails more often")
    small = make_envelope(m, 300, 1, 0)
    c_small = rate(m, small, 200000, 1)
    assert sum(c_small.values()) > 5 * max(1, sum(counts.values())), (c_small, counts)
    print("      fitted on 300: %d fails; fitted on 20000: %d fails (same 200000 inputs)" %
          (sum(c_small.values()), sum(counts.values())))
    print("[4/6] scan with prefix-hash reuse equals a scan that re-hashes the whole artefact")
    prefix = bytes(range(256)) * 400                       # stands for a 100 kB artefact body
    data = prefix + m.tail(0)
    clean, tried = scan(m, small, data, 1, 3, 100000)
    naive = []
    c = 1
    while len(naive) < 3:
        h = m.seed_hasher()
        h.update(prefix + m.tail(c))
        if all(m.run(i, small)[1] is None for i in m.inputs(h.digest(m.STREAM_BYTES))):
            naive.append(c)
        c += 1
    assert clean == naive, (clean, naive)
    print("      first 3 clean candidates %s in %d tried" % (clean, tried))
    print("[5/6] replay: a clean candidate has no failing input; a dirty one names index and class")
    assert replay(m, small, prefix + m.tail(clean[0])) == []
    dirty = next(c for c in range(1, clean[-1]) if c not in clean)
    fails = replay(m, small, prefix + m.tail(dirty))
    assert fails and fails[0][1] in m.CLASSES
    print("      candidate %d: failing inputs %s" % (dirty, fails))
    print("[6/6] blindspot and envelope --check")
    b = blindspot({("1", "7"), ("2", "9")}, {("1", "7"), ("2", "40"), ("3", "5")}, 3)
    assert b["observed, not predicted"] == 2 and b["predicted and observed"] == 1
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "env.txt")
        assert main(["envelope", "--n", "2000", "--out", p]) == 0
        assert main(["envelope", "--n", "2000", "--check", p]) == 0
        with open(p, "a") as f:
            f.write("99\n")                               # a hand edit
        assert main(["envelope", "--n", "2000", "--check", p]) == 1, "an edited table must be reported"
    print("diag selftest: PASS")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", nargs="?", choices=["rate", "envelope", "replay", "scan", "blindspot"])
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--model-file")
    p.add_argument("--n", type=int, default=200000)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--margin", type=int, default=0)
    p.add_argument("--table")
    p.add_argument("--out")
    p.add_argument("--check")
    p.add_argument("--per-artefact", type=int)
    p.add_argument("--artefact")
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--want", type=int, default=1)
    p.add_argument("--limit", type=int, default=1000000)
    p.add_argument("--model")
    p.add_argument("--replica")
    a = p.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.cmd:
        print(__doc__)
        return 2
    model = load_model(a.model_file)
    if a.cmd == "blindspot":
        (mp, _), (rp, seeds) = read_pairs(a.model), read_pairs(a.replica)
        b = blindspot(mp, rp, seeds)
        for k in ("predicted and observed", "observed, not predicted", "predicted, not observed"):
            print("%-26s %6d  (%.3f per seed)" % (k, b[k], b[k] / max(1, seeds)))
        total = b["predicted and observed"] + b["observed, not predicted"]
        print("blind spot share of observed failures: %.1f%%" % (100.0 * b["observed, not predicted"] / max(1, total)))
        return 0
    if a.cmd == "envelope":
        table = make_envelope(model, a.n, a.seed, a.margin)
        text = "".join("%d\n" % v for v in table)
        if a.check:
            with open(a.check) as f:
                same = f.read() == text
            print("envelope %s the committed table %s" % ("reproduces" if same else "DIFFERS from", a.check))
            return 0 if same else 1
        with open(a.out, "w") as f:
            f.write(text)
        print("wrote %d bounds from %d samples (seed %d, margin %d) to %s" % (len(table), a.n, a.seed, a.margin, a.out))
        return 0
    table = read_table(a.table) if a.table else make_envelope(model, 20000, 1, 0)
    if a.cmd == "rate":
        report_rate(rate(model, table, a.n, a.seed), a.n, a.per_artefact or getattr(model, "PER_ARTEFACT", 1))
        return 0
    with open(a.artefact, "rb") as f:
        data = f.read()
    if a.cmd == "replay":
        fails = replay(model, table, data)
        for i, cls in fails:
            print("input %d fails: %s" % (i, cls))
        print("%d failing inputs predicted" % len(fails))
        return 0 if not fails else 1
    clean, tried = scan(model, table, data, a.start, a.want, a.limit)
    print("clean candidates: %s (%d tried from %d)" % (" ".join(map(str, clean)) or "none", tried, a.start))
    return 0 if len(clean) >= a.want else 1


if __name__ == "__main__":
    sys.exit(main())

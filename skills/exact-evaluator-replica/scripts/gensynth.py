#!/usr/bin/env python3
"""gensynth.py: write a random artefact for differential testing of a replica against its judge.

Usage:
  gensynth.py <out> <n_ops> <seed> [--spec spec.json] [--require-coverage]
  gensynth.py --print-spec        print the built-in spec (the toy_bench.py format) as a starting point
  gensynth.py --selftest

The artefact is random, so it fails the judge on every sample. That is intended: the
differential test compares accounting and stream alignment, not correctness.

Coverage it aims for, and reports on stderr:
  every op kind; every kind both with and without a condition; nested condition blocks;
  closing a block at depth 0 (accepted by many judges as a no-op); measuring ops inside
  a condition (own condition or an enclosing block).
With --require-coverage the exit code is 1 when any of these is missing.

Spec (JSON): {"magic": first line or null, "wires": N, "bits": N, "max_depth": D,
"cond_prob": p, "kinds": [{"name", "weight", "operands": ["wire"|"bit", ...],
"cond": true|false, "role": "plain"|"measure"|"push"|"pop"}]}.
Wire operands of one op are distinct. Output is one text line per op:
NAME operands cond ("-" for none). For a binary judge format, replace encode().
"""
import hashlib
import json
import random
import sys

TOY_SPEC = {
    "magic": "TOYOPS 1", "wires": 48, "bits": 24, "max_depth": 4, "cond_prob": 0.3,
    "kinds": [
        {"name": "CCX", "weight": 30, "operands": ["wire", "wire", "wire"], "cond": True, "role": "plain"},
        {"name": "CX", "weight": 20, "operands": ["wire", "wire"], "cond": True, "role": "plain"},
        {"name": "X", "weight": 8, "operands": ["wire"], "cond": True, "role": "plain"},
        {"name": "MR", "weight": 8, "operands": ["wire", "bit"], "cond": True, "role": "measure"},
        {"name": "R", "weight": 4, "operands": ["wire"], "cond": True, "role": "measure"},
        {"name": "S0", "weight": 3, "operands": ["bit"], "cond": True, "role": "plain"},
        {"name": "S1", "weight": 3, "operands": ["bit"], "cond": True, "role": "plain"},
        {"name": "INV", "weight": 3, "operands": ["bit"], "cond": True, "role": "plain"},
        {"name": "PUSH", "weight": 6, "operands": ["bit"], "cond": False, "role": "push"},
        {"name": "POP", "weight": 7, "operands": [], "cond": False, "role": "pop"},
    ],
}


def encode(name, operands, cond):
    """One op as bytes. Replace this function to emit a judge's binary record."""
    return ("%s %s %s\n" % (name, " ".join(map(str, operands)), "-" if cond is None else cond)).replace("  ", " ").encode()


def generate(spec, n_ops, seed):
    rng = random.Random(seed)
    kinds = spec["kinds"]
    weights = [k["weight"] for k in kinds]
    cov = {"kinds": {k["name"]: 0 for k in kinds}, "conditioned": {k["name"]: 0 for k in kinds if k["cond"]},
           "unconditioned": {k["name"]: 0 for k in kinds if k["cond"]},
           "max_depth": 0, "pop_at_depth_0": 0, "measure_under_condition": 0}
    out, depth, count = [], 0, 0
    if spec.get("magic"):
        out.append((spec["magic"] + "\n").encode())
    while count < n_ops:
        k = rng.choices(kinds, weights)[0]
        if k["role"] == "push" and depth >= spec["max_depth"]:
            continue
        wires = rng.sample(range(spec["wires"]), sum(1 for o in k["operands"] if o == "wire"))
        ops = [wires.pop() if o == "wire" else rng.randrange(spec["bits"]) for o in k["operands"]]
        cond = rng.randrange(spec["bits"]) if k["cond"] and rng.random() < spec["cond_prob"] else None
        if k["cond"]:
            cov["conditioned" if cond is not None else "unconditioned"][k["name"]] += 1
        if k["role"] == "measure" and (cond is not None or depth > 0):
            cov["measure_under_condition"] += 1
        if k["role"] == "push":
            depth += 1
            cov["max_depth"] = max(cov["max_depth"], depth)
        elif k["role"] == "pop":
            if depth == 0:
                cov["pop_at_depth_0"] += 1
            depth = max(0, depth - 1)
        cov["kinds"][k["name"]] += 1
        out.append(encode(k["name"], ops, cond))
        count += 1
    return b"".join(out), cov


def missing(cov):
    gaps = [n for n, c in cov["kinds"].items() if c == 0]
    gaps += ["%s conditioned" % n for n, c in cov["conditioned"].items() if c == 0]
    gaps += ["%s unconditioned" % n for n, c in cov["unconditioned"].items() if c == 0]
    if cov["max_depth"] < 2:
        gaps.append("nested condition blocks")
    if cov["pop_at_depth_0"] == 0:
        gaps.append("block close at depth 0")
    if cov["measure_under_condition"] == 0:
        gaps.append("measuring op under a condition")
    return gaps


def selftest():
    data, cov = generate(TOY_SPEC, 5000, 11)
    again, _ = generate(TOY_SPEC, 5000, 11)
    other, _ = generate(TOY_SPEC, 5000, 12)
    assert data == again, "same seed must give the same bytes"
    assert data != other, "different seeds must differ"
    assert data.count(b"\n") == 5001
    assert missing(cov) == [], missing(cov)
    _, small = generate(TOY_SPEC, 3, 11)
    gaps = missing(small)
    assert gaps, "a 3-op artefact cannot cover every case"
    print("gensynth selftest: 5000 ops, sha256 %s" % hashlib.sha256(data).hexdigest()[:16])
    print("  coverage complete: max depth %d, %d closes at depth 0, %d measuring ops under a condition" %
          (cov["max_depth"], cov["pop_at_depth_0"], cov["measure_under_condition"]))
    print("  negative case: 3 ops leave %d coverage gaps, reported as a failure" % len(gaps))
    print("gensynth selftest: PASS")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--print-spec" in argv:
        print(json.dumps(TOY_SPEC, indent=1))
        return 0
    args = [a for a in argv[1:] if not a.startswith("--")]
    spec = TOY_SPEC
    if "--spec" in argv:
        path = argv[argv.index("--spec") + 1]
        args.remove(path)
        with open(path) as f:
            spec = json.load(f)
    if len(args) != 3:
        print(__doc__)
        return 2
    data, cov = generate(spec, int(args[1]), int(args[2]))
    with open(args[0], "wb") as f:
        f.write(data)
    gaps = missing(cov)
    sys.stderr.write("wrote %s ops, sha256 %s, coverage gaps: %s\n" %
                     (args[1], hashlib.sha256(data).hexdigest()[:16], ", ".join(gaps) or "none"))
    return 1 if gaps and "--require-coverage" in argv else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

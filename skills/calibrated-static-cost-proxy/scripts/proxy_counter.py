#!/usr/bin/env python3
"""proxy_counter.py: static expected-cost counter for a generator, and a calibration check.

As a library (copy the StaticCost class into the generator, or port its 20 lines):
    cost = StaticCost()
    cost.charge(1, "adder")              # unconditional charged op
    cost.push()                          # enter a block conditioned on a measurement outcome (rate 1/2)
    cost.charge(1, "repair")             # counts 0.5
    cost.push(rate=0.03)                 # a condition measured to fire on 3% of samples
    cost.charge(4, "rare-fix")           # counts 4 * 0.5 * 0.03
    cost.pop(); cost.pop()
    cost.expected, cost.emitted, cost.by_section

As a tool:
  proxy_counter.py check <calibration.tsv> [--lever SIZE]
      Reads rows of artefact, proxy, judge, ... and prints the gap of each. With
      --lever (smallest lever being decided, in judge units) the exit code is 1 when
      the latest gap is not below that size, because the proxy cannot then decide it.
  proxy_counter.py --selftest
"""
import sys


class StaticCost:
    def __init__(self):
        self.expected = 0.0          # proxy for the judged (executed) cost
        self.emitted = 0             # charged ops in the artefact
        self.by_section = {}
        self._weights = [1.0]

    def push(self, rate=0.5):
        self._weights.append(self._weights[-1] * rate)

    def pop(self):
        if len(self._weights) == 1:
            raise ValueError("pop without push")
        self._weights.pop()

    def charge(self, n=1, section="-"):
        w = n * self._weights[-1]
        self.expected += w
        self.emitted += n
        self.by_section[section] = self.by_section.get(section, 0.0) + w


def check(path, lever):
    rows = []
    with open(path) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 3 or line.startswith("#"):
                continue
            try:
                rows.append((p[0], float(p[1]), float(p[2])))
            except ValueError:
                continue                 # header or template row
    if not rows:
        print("no calibration rows in %s" % path)
        return 2
    print("%-16s %16s %16s %12s %9s" % ("artefact", "proxy", "judge", "gap", "relative"))
    for art, proxy, judge in rows:
        print("%-16s %16.3f %16.3f %+12.3f %8.3f%%" % (art[:16], proxy, judge, proxy - judge, 100 * (proxy - judge) / judge))
    art, proxy, judge = rows[-1]
    gap = abs(proxy - judge)
    if lever is None:
        return 0
    if gap < lever:
        print("latest gap %.3f is below the smallest lever %.3f: the proxy can decide it" % (gap, lever))
        return 0
    print("latest gap %.3f is NOT below the smallest lever %.3f: decide with the judge or recalibrate" % (gap, lever))
    return 1


def selftest():
    import math
    import os
    import random
    import tempfile
    rng = random.Random(3)

    def build(depth=0):
        # random block tree: ("op", n, section) | ("block", rate, [children])
        out = []
        for _ in range(rng.randrange(3, 7)):
            if depth < 3 and rng.random() < 0.4:
                out.append(("block", 0.5, build(depth + 1)))
            else:
                out.append(("op", rng.randrange(1, 9), "sec%d" % rng.randrange(3)))
        return out

    def count(tree, cost, rates=None):
        for node in tree:
            if node[0] == "op":
                cost.charge(node[1], node[2])
            else:
                cost.push(node[1] if rates is None else rates)
                count(node[2], cost, rates)
                cost.pop()

    def execute(tree, r):
        total = 0
        for node in tree:
            if node[0] == "op":
                total += node[1]
            elif r.random() < node[1]:
                total += execute(node[2], r)
        return total

    def measure(tree, n=40000):
        r = random.Random(9)
        xs = [execute(tree, r) for _ in range(n)]
        mean = sum(xs) / n
        se = math.sqrt(sum((x - mean) ** 2 for x in xs) / (n - 1) / n)
        return mean, se

    tree = [("block", 0.5, build())] + build()
    cost = StaticCost()
    count(tree, cost)
    mean, se = measure(tree)
    print("[1/4] balanced conditions: proxy %.3f, simulated judge %.3f +- %.3f, emitted %d" % (cost.expected, mean, se, cost.emitted))
    assert abs(cost.expected - mean) < 4 * se
    assert abs(sum(cost.by_section.values()) - cost.expected) < 1e-9, "sections must sum to the total"
    print("[2/4] sections sum to the total: %s" % {k: round(v, 3) for k, v in sorted(cost.by_section.items())})

    rare = [("op", 100, "a"), ("block", 0.05, [("op", 400, "fix")])]
    naive, fitted = StaticCost(), StaticCost()
    count(rare, naive, rates=0.5)
    count(rare, fitted)
    mean, se = measure(rare)
    print("[3/4] negative case, unbalanced condition (fires 5%%): 1/2-weight proxy %.1f vs judge %.1f; measured-rate proxy %.1f" %
          (naive.expected, mean, fitted.expected))
    assert abs(naive.expected - mean) > 20 * se and abs(fitted.expected - mean) < 4 * se

    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "calibration.tsv")
        with open(p, "w") as f:
            f.write("artefact_sha256\tproxy\tjudge\tgap_rel\tdate\tevaluator_commit\tnote\n")
            f.write("aaaa\t5010346\t5007345.518\t\t\t\t\n")
            f.write("bbbb\t4929726.5\t4854904.726\t\t\t\tforeign module spliced\n")
        print("[4/4] check: a 1.5 percent gap cannot decide a 30,000-unit lever")
        assert check(p, 30000.0) == 1
        assert check(p, 100000.0) == 0
    print("proxy_counter selftest: PASS")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if len(argv) >= 3 and argv[1] == "check":
        lever = float(argv[argv.index("--lever") + 1]) if "--lever" in argv else None
        return check(argv[2], lever)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))

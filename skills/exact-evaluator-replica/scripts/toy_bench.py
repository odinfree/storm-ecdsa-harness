#!/usr/bin/env python3
"""toy_bench.py: a miniature benchmark with a slow judge and an exact fast replica.

It is the worked example for the exact-evaluator-replica skill and the fixture that
difftest.py --selftest runs. The judge and the replica share the artefact parser and
nothing else: the judge simulates one sample at a time and reads its randomness from
a cursor; the replica simulates 64 samples per machine word and takes each batch's
randomness from a computed offset, with batches on a thread pool.

Usage:
  toy_bench.py judge   <artefact>                  official-style run; appends a row to ./results.tsv
  toy_bench.py replica <artefact> [--salt S] [--threads N] [--bug K]
  toy_bench.py golden  <out> <seed> [blocks]       write an artefact that passes every sample
  toy_bench.py --selftest

Artefact format (text): first line "TOYOPS 1", then one op per line: KIND operands cond
(cond is a classical bit index or "-"). Kinds: X t | CX c t | CCX a b t | MR q b |
R q | S0 b | S1 b | INV b | PUSH b | POP. PUSH and POP carry "-" as cond; a POP at depth 0 is a no-op.

Determinism map of the toy judge (the fact the replica rests on):
  seed    = SHAKE256("toy-judge-v1" + [salt] + op count + artefact lines)
  inputs  = first 2*T bytes, 2 bytes per sample (T = 200 samples)
  measure = every MR and R op reads 8 bytes per 64-sample batch, executed or not,
            so batch b's bytes sit at offset 2*T + 8*M*b (M = number of MR and R ops)
"""
import hashlib
import os
import sys
from concurrent.futures import ThreadPoolExecutor

T = 200            # samples per run; not a multiple of 64, so the last batch is partial
W = 16             # input width; wires 0..15 input, 16..31 output, 32.. scratch
MEASURING = ("MR", "R")
ARITY = {"X": 1, "CX": 2, "CCX": 3, "MR": 2, "R": 1, "S0": 1, "S1": 1, "INV": 1, "PUSH": 1, "POP": 0}


def load(path):
    with open(path, "rb") as f:
        raw = f.read()
    lines = raw.decode().split("\n")
    if lines[0] != "TOYOPS 1":
        raise SystemExit("load FAILED: bad magic")
    ops = []
    for ln in lines[1:]:
        if not ln:
            continue
        p = ln.split()
        kind = p[0]
        if kind not in ARITY or len(p) != ARITY[kind] + 2:
            raise SystemExit("load FAILED: bad op line %r" % ln)
        args = [int(x) for x in p[1:-1]]
        cond = None if p[-1] == "-" else int(p[-1])
        ops.append((kind, args, cond))
    return ops


def seed_stream(ops, salt, nbytes):
    h = hashlib.shake_256()
    h.update(b"toy-judge-v1")
    if salt is not None:
        h.update(b"salt:" + salt.encode())
    h.update(len(ops).to_bytes(8, "little"))
    for kind, args, cond in ops:
        h.update(("%s %s %s\n" % (kind, " ".join(map(str, args)), "-" if cond is None else cond)).encode())
    return h.digest(nbytes)


def sizes(ops):
    nw, nb, m = 2 * W, 1, 0
    for kind, args, cond in ops:
        if cond is not None:
            nb = max(nb, cond + 1)
        if kind in ("X", "CX", "CCX", "R"):
            nw = max(nw, max(args) + 1)
        elif kind == "MR":
            nw, nb = max(nw, args[0] + 1), max(nb, args[1] + 1)
        elif kind in ("S0", "S1", "INV", "PUSH"):
            nb = max(nb, args[0] + 1)
        if kind in MEASURING:
            m += 1
    return nw, nb, m


# ---------------------------------------------------------------- judge (slow, scalar)
def judge(path):
    ops = load(path)
    nw, nb, m = sizes(ops)
    nbatch = (T + 63) // 64
    stream = seed_stream(ops, None, 2 * T + 8 * m * nbatch)
    cur = 0
    inputs = []
    for _ in range(T):
        inputs.append(int.from_bytes(stream[cur:cur + 2], "little"))
        cur += 2
    wrong = dirty_batches = charged = free = 0
    for b in range(nbatch):
        words = []
        for _ in range(m):          # one read per measuring op, in op order, executed or not
            words.append(int.from_bytes(stream[cur:cur + 8], "little"))
            cur += 8
        batch_dirty = False
        for s in range(min(64, T - 64 * b)):
            x = inputs[64 * b + s]
            q = [0] * nw
            bits = [0] * nb
            for i in range(W):
                q[i] = (x >> i) & 1
            stack = []
            j = 0
            for kind, a, cond in ops:
                ex = all(stack) and (cond is None or bits[cond] == 1)
                if kind == "PUSH":
                    stack.append(bits[a[0]] == 1)
                elif kind == "POP":
                    if stack:
                        stack.pop()
                elif kind == "X":
                    if ex:
                        q[a[0]] ^= 1
                        free += 1
                elif kind == "CX":
                    if ex:
                        q[a[1]] ^= q[a[0]]
                        free += 1
                elif kind == "CCX":
                    if ex:
                        q[a[2]] ^= q[a[0]] & q[a[1]]
                        charged += 1      # charged per executed sample, controls set or not
                elif kind == "MR":
                    r = (words[j] >> s) & 1
                    j += 1
                    if ex:
                        bits[a[1]] = r
                        q[a[0]] = 0
                elif kind == "R":
                    j += 1
                    if ex:
                        q[a[0]] = 0
                elif kind == "S0":
                    if ex:
                        bits[a[0]] = 0
                elif kind == "S1":
                    if ex:
                        bits[a[0]] = 1
                elif kind == "INV":
                    if ex:
                        bits[a[0]] ^= 1
            out = sum(q[W + i] << i for i in range(W))
            if out != (~x & 0xFFFF):
                wrong += 1
            if any(q[2 * W:]):
                batch_dirty = True
        dirty_batches += batch_dirty
    ok = wrong == 0 and dirty_batches == 0
    print("=== toy judge ===")
    print("  tested samples          : %d" % T)
    print("  wrong outputs           : %d" % wrong)
    print("  dirty-scratch batches   : %d" % dirty_batches)
    avg_c, avg_f = "%.3f" % (charged / T), "%.3f" % (free / T)
    with open("results.tsv", "a") as f:     # the only place the averages appear on failure
        f.write("\t".join([avg_c, avg_f, str(nw), str(len(ops)), "OK" if ok else "FAIL"]) + "\n")
    if not ok:
        print("  FAILED")
        return 1
    print("  avg executed charged    : %s" % avg_c)
    print("  avg executed free       : %s" % avg_f)
    print("  wires                   : %d" % nw)
    print("  emitted ops             : %d" % len(ops))
    print("  score                   : %d" % (round(charged / T) * nw))
    return 0


# ---------------------------------------------------------------- replica (bit-sliced, parallel)
def replica(path, salt=None, threads=4, bug=0):
    ops = load(path)
    nw, nb, m = sizes(ops)
    nbatch = (T + 63) // 64
    stream = seed_stream(ops, salt, 2 * T + 8 * m * nbatch)
    inputs = [int.from_bytes(stream[2 * i:2 * i + 2], "little") for i in range(T)]
    # compact ops: classical bit indices shift by one; slot 0 is all ones and stands for "no condition"
    comp = [(k, a, 0 if c is None else c + 1) for k, a, c in ops]

    def batch(b):
        bs = min(64, T - 64 * b)
        mask = (1 << bs) - 1
        base = 2 * T + 8 * m * b            # fixed offset: independent of what executed before
        q = [0] * nw
        bits = [0] * (nb + 1)
        bits[0] = mask
        for s in range(bs):
            x = inputs[64 * b + s]
            for i in range(W):
                if (x >> i) & 1:
                    q[i] |= 1 << s
        stack, live = [], mask
        j = charged = free = 0
        for kind, a, c in comp:
            ex = live & bits[c]
            if kind == "PUSH":
                stack.append(live)
                live &= bits[a[0] + 1]
            elif kind == "POP":
                if stack:
                    live = stack.pop()
            elif kind == "X":
                q[a[0]] ^= ex
                free += bin(ex).count("1")
            elif kind == "CX":
                q[a[1]] ^= q[a[0]] & ex
                free += bin(ex).count("1")
            elif kind == "CCX":
                fire = q[a[0]] & q[a[1]] & ex
                q[a[2]] ^= fire
                charged += bin(fire if bug == 2 else ex).count("1")
            elif kind == "MR":
                if bug == 1 and (c != 0 or stack):
                    continue                 # injected defect: conditioned measuring ops skip their read
                r = int.from_bytes(stream[base + 8 * j:base + 8 * j + 8], "little") & mask
                j += 1
                bits[a[1] + 1] = (bits[a[1] + 1] & ~ex) | (r & ex)
                q[a[0]] &= ~ex
            elif kind == "R":
                if bug == 1 and (c != 0 or stack):
                    continue
                j += 1
                q[a[0]] &= ~ex
            elif kind == "S0":
                bits[a[0] + 1] &= ~ex
            elif kind == "S1":
                bits[a[0] + 1] |= ex
            elif kind == "INV":
                bits[a[0] + 1] ^= ex
        wrong = dirty = 0
        for s in range(bs):
            x = inputs[64 * b + s]
            out = sum(((q[W + i] >> s) & 1) << i for i in range(W))
            if out != (~x & 0xFFFF):
                wrong |= 1 << s
        for w in q[2 * W:]:
            dirty |= w
        return wrong, dirty & mask, charged, free

    with ThreadPoolExecutor(max_workers=threads) as pool:
        res = list(pool.map(batch, range(nbatch)))
    wrong = sum(bin(r[0]).count("1") for r in res)
    dirty_batches = sum(1 for r in res if r[1])
    failing = sum(bin(r[0] | r[1]).count("1") for r in res)
    charged, free = sum(r[2] for r in res), sum(r[3] for r in res)
    first = next((64 * b + s for b, r in enumerate(res) for s in range(64) if ((r[0] | r[1]) >> s) & 1), None)
    print("=== toy replica (exact, parallel) ===")
    if salt is not None:
        print("  salt=%s: salted samples, NOT the official score" % salt)
    print("  tested samples          : %d" % T)
    print("  wrong outputs           : %d" % wrong)
    print("  dirty-scratch batches   : %d" % dirty_batches)
    print("  failing samples (any)   : %d" % failing)
    print("  first failing sample    : %s" % ("none" if first is None else first))
    print("  avg executed charged    : %.3f" % (charged / T))
    print("  avg executed free       : %.3f" % (free / T))
    print("  wires                   : %d" % nw)
    print("  emitted ops             : %d" % len(ops))
    print("  score                   : %d" % (round(charged / T) * nw))
    return 0 if failing == 0 else 1


# ---------------------------------------------------------------- golden artefact (passing path)
def golden(out, seed, blocks=40):
    import random
    rng = random.Random(seed)
    lines = ["TOYOPS 1"]
    for i in range(W):
        lines += ["CX %d %d -" % (i, W + i), "X %d -" % (W + i)]
    for k in range(blocks):
        a, b = rng.sample(range(W), 2)
        s, bit = 2 * W + rng.randrange(4), rng.randrange(8)
        # scratch is 0, so MR leaves it 0 and puts a fair random outcome in the bit;
        # the pair of charged ops under that bit computes and uncomputes: clean on every sample
        lines += ["MR %d %d -" % (s, bit), "PUSH %d -" % bit,
                  "CCX %d %d %d -" % (a, b, s), "CCX %d %d %d -" % (a, b, s), "POP -"]
        if k % 5 == 0:
            lines += ["CCX %d %d %d %d" % (a, b, s, bit), "CCX %d %d %d %d" % (a, b, s, bit), "R %d %d" % (s, bit)]
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")


def selftest():
    import contextlib
    import io
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        cwd = os.getcwd()
        os.chdir(d)
        try:
            golden("g.ops", 7)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rj = judge("g.ops")
                rr = replica("g.ops")
            text = buf.getvalue()
            val = lambda label: [ln.split()[-1] for ln in text.splitlines() if label in ln]
            assert rj == 0 and rr == 0, "golden artefact must pass both"
            for label in ("avg executed charged", "avg executed free", "score", "wrong outputs"):
                v = val(label)
                assert len(v) == 2 and v[0] == v[1], (label, v)
            with contextlib.redirect_stdout(io.StringIO()) as b1:
                replica("g.ops", bug=1)
            bad = [ln.split()[-1] for ln in b1.getvalue().splitlines() if "avg executed charged" in ln]
            assert bad != val("avg executed charged")[:1], "the stream-alignment defect must change the count"
            with contextlib.redirect_stdout(io.StringIO()) as b2:
                replica("g.ops", salt="a")
            assert "NOT the official score" in b2.getvalue()
            print("toy_bench selftest: golden artefact passes judge and replica with equal lines")
            print("  avg executed charged judge=%s replica=%s; injected defect gives %s" %
                  (val("avg executed charged")[0], val("avg executed charged")[1], bad[0]))
            print("toy_bench selftest: PASS")
        finally:
            os.chdir(cwd)
    return 0


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) >= 3 and argv[1] == "judge":
        return judge(argv[2])
    if len(argv) >= 3 and argv[1] == "replica":
        opt = {"--salt": None, "--threads": "4", "--bug": "0"}
        rest = argv[3:]
        for i in range(0, len(rest) - 1, 2):
            if rest[i] not in opt:
                raise SystemExit(__doc__)
            opt[rest[i]] = rest[i + 1]
        return replica(argv[2], opt["--salt"], int(opt["--threads"]), int(opt["--bug"]))
    if len(argv) >= 4 and argv[1] == "golden":
        golden(argv[2], int(argv[3]), int(argv[4]) if len(argv) > 4 else 40)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))

#!/usr/bin/env python3
"""gl.py (Fadespüeli): reader for GLV1 gate lists (zstd; header "GLV1", u32 gates, u32 lanes, u32 ccx; then per gate one op byte and
1 to 3 u16 lanes: op 0 = X, 1 = CX, 2 = CCX, 3 / 4 = AND-compute / AND-uncompute markers with CCX value semantics).
  gl.py stat <list.glz> [TOP=765]   sizes, marker counts, max lane, and for the eight widths below TOP the gates touching a lane >= W
  gl.py replay <ref.glz> <new.glz> <shots> <seed> [NL=765]   run both lists on the same random inputs, compare all lanes
The replay input layout (x on lanes 0..254, one flag on 512, a passenger on 256..511; scratch 757..764 expected zero at the end)
is the one our 765-wide paged-walk start lists used. Edit `replay` for another layout. Needs the `zstd` binary.
"""
import hashlib, random, struct, subprocess, sys

def load(path):
    raw = subprocess.run(["zstd", "-dc", path], check=True, capture_output=True).stdout
    assert raw[:4] == b"GLV1"
    n, nl, nccx = struct.unpack_from("<III", raw, 4)
    gates, ops, o = [], bytearray(n), 16
    for i in range(n):
        op = raw[o]; o += 1
        k = min(op, 2) + 1
        gates.append(struct.unpack_from("<%dH" % k, raw, o)); o += 2 * k
        ops[i] = op
    assert o == len(raw)
    return gates, ops, nl, nccx

def stat(path, top=765):
    gates, ops, nl, nccx = load(path)
    b = open(path, "rb").read()
    print("file %s bytes %d sha256 %s sha3 %s" % (path, len(b), hashlib.sha256(b).hexdigest()[:16], hashlib.sha3_256(b).hexdigest()[:16]))
    cnt = [0] * 5
    for op in ops: cnt[op] += 1
    mx = [max(g) for g in gates]
    used = set()
    for g in gates: used.update(g)
    print("gates %d header_lanes %d ccx_header %d | X %d CX %d CCX %d ANDC %d ANDU %d | touched %d max_lane %d untouched<%d %s" % (
        len(gates), nl, nccx, cnt[0], cnt[1], cnt[2], cnt[3], cnt[4], len(used), max(mx), top, [l for l in range(top) if l not in used]))
    for W in range(top - 1, top - 9, -1):
        idx = [i for i, m in enumerate(mx) if m >= W]
        if not idx:
            print("W=%d: 0 gates on lanes >= W" % W); continue
        runs, gap = 1, 20000
        for a, c in zip(idx, idx[1:]):
            if c - a > gap: runs += 1
        print("W=%d: %d gates touch a lane >= W; first %d last %d; runs (gap > %d gates) %d; ccx among them %d" % (
            W, len(idx), idx[0], idx[-1], gap, runs, sum(1 for i in idx if ops[i] >= 2)))
    # per-lane first/last for the top lanes
    first, last, c = {}, {}, {}
    for i, g in enumerate(gates):
        for q in g:
            if q >= top - 25:
                first.setdefault(q, i); last[q] = i; c[q] = c.get(q, 0) + 1
    for q in sorted(c): print("lane %d gates %d first %d last %d" % (q, c[q], first[q], last[q]))

def run(path, inp, mask):
    gates, ops, nl, _ = load(path)
    s = list(inp)
    for g in gates:
        if len(g) == 3: s[g[2]] ^= s[g[0]] & s[g[1]]
        elif len(g) == 2: s[g[1]] ^= s[g[0]]
        else: s[g[0]] ^= mask
    return s, len(gates)

def replay(ref, new, n, seed, NL=765):
    rng = random.Random(seed)
    inp = [0] * NL
    for l in list(range(255)) + [512] + list(range(256, 512)): inp[l] = rng.getrandbits(n)
    mask = (1 << n) - 1
    pc = lambda v: bin(v).count("1")
    out = {}
    for name, p in (("ref", ref), ("new", new)):
        s, ng = run(p, inp, mask); out[name] = s
        top = 0
        for l in range(757, 765): top |= s[l]
        pas = 0
        for l in range(256, 512): pas |= s[l] ^ inp[l]
        print("%s %s: %d gates; lanes 757..764 nonzero at end on %d shots; passenger changed on %d shots" % (name, p.split("/")[-1], ng, pc(top), pc(pas)))
    d, per = 0, []
    for l in range(NL):
        x = out["ref"][l] ^ out["new"][l]
        if x: per.append((l, pc(x)))
        d |= x
    print("final states differ on %d of %d shots (seed %d); lanes that differ: %d %s" % (pc(d), n, seed, len(per), per[:40]))

if __name__ == "__main__":
    if sys.argv[1] == "stat": stat(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 765)
    else: replay(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]) if len(sys.argv) > 6 else 765)

#!/usr/bin/env python3
"""rci — Reversible Circuit Invariants.

Executable checkers derived from eprint 2026/2014 (Jo & Lee), "Quantum Discrete
Logarithms on Elliptic Curves with 5n/2+o(n) Logical Qubits and O~(n^2) Toffoli
Gates".  Every subcommand mechanizes one checkable claim from that paper so a
campaign can run it BEFORE spending an evaluation or a submission.

Subcommands
-----------
  census      ops.bin -> op count, kind histogram, Toffoli, peak qubit
  holes       ops.bin -> does any op touch a declared-omitted lane?   (§2.3/§4.1)
  simulate    ops.bin -> X/CX/CCX bit simulation; final non-zero qubits
  inplace     Lemma 5(3) / Fig 6: classify + brute-force verify Ax+By=C
  capacity    §4.1 / Lemma 8 / eq (7): layout sizes and combined-length bounds
  pebble      Lemma 4: uncomputation cost T^2/S + T under an ancilla budget
  exceptional Lemma 12/13: exceptional set of adding a fixed classical point

ops.bin format (from src/bin/eval_circuit.rs):
  magic b"QECCOPSZ" | u64_le op_count | zstd body of op_count * 56-byte records
  record: u32 kind, u32 pad, u64 q_control2, q_control1, q_target,
          c_target, c_condition, r_target      (u64::MAX = absent)

Exit codes: 0 = check passed / command ok, 1 = check FAILED, 2 = usage error.
"""
from __future__ import annotations

import argparse
import json
import math
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

MAGIC = b"QECCOPSZ"
OP_BYTES = 56
NO_QUBIT = (1 << 64) - 1

KIND = {
    0: "Neg", 1: "Register", 2: "AppendToRegister", 3: "BitInvert",
    4: "BitStore0", 5: "BitStore1", 6: "X", 7: "Z", 8: "CX", 9: "CZ",
    10: "Swap", 11: "R", 12: "Hmr", 13: "CCX", 14: "CCZ",
    15: "PushCondition", 16: "PopCondition", 17: "DebugPrint",
}
TOFFOLI_KINDS = {13, 14}          # CCX, CCZ
CLASSICAL_KINDS = {6, 8, 10, 13}  # X, CX, Swap, CCX


# --------------------------------------------------------------------------
# ops.bin
# --------------------------------------------------------------------------
def load_ops(path: str):
    """Yield (kind, c2, c1, tgt) per op. Streams; never holds the whole file."""
    raw = Path(path).read_bytes()
    if raw[:8] != MAGIC:
        raise SystemExit(f"{path}: bad magic {raw[:8]!r}")
    (n,) = struct.unpack_from("<Q", raw, 8)
    body = raw[16:]
    with tempfile.NamedTemporaryFile(suffix=".zst", delete=True) as tf:
        tf.write(body)
        tf.flush()
        out = subprocess.run(["zstd", "-d", "-c", tf.name],
                             capture_output=True)
    if out.returncode != 0:
        raise SystemExit(f"{path}: zstd decode failed: "
                         f"{out.stderr.decode()[:200]}")
    blob = out.stdout
    if len(blob) < n * OP_BYTES:
        raise SystemExit(f"{path}: short body: {len(blob)} < {n * OP_BYTES}")
    for i in range(n):
        kind, _pad, c2, c1, tgt, _ct, _cc, _rt = struct.unpack_from(
            "<IIQQQQQQ", blob, i * OP_BYTES)
        yield kind, c2, c1, tgt


def cmd_census(a):
    counts, toffoli, peak, swaps = {}, 0, -1, 0
    total = 0
    for kind, c2, c1, tgt in load_ops(a.ops):
        total += 1
        name = KIND.get(kind, f"kind{kind}")
        counts[name] = counts.get(name, 0) + 1
        if kind in TOFFOLI_KINDS:
            toffoli += 1
        if kind == 10:
            swaps += 1
        for q in (c2, c1, tgt):
            if q != NO_QUBIT and q > peak:
                peak = q
    res = {
        "ops": total,
        "toffoli": toffoli,
        "peak_qubit_id": peak,
        "qubits_upper_bound": peak + 1,
        "toffoli_fraction": round(toffoli / total, 6) if total else 0.0,
        "kinds": dict(sorted(counts.items(), key=lambda kv: -kv[1])),
    }
    if swaps:
        res["note_swaps"] = f"{swaps} Swap ops counted as 0 Toffoli"
    print(json.dumps(res, indent=2))
    return 0


def cmd_holes(a):
    """A declared-omitted lane must never appear in any op. Sound + cheap:
    an op touching an unallocated physical lane is malformed by construction."""
    watch = {int(x) for x in a.lanes.split(",") if x.strip()}
    hits, first = [], {}
    for i, (kind, c2, c1, tgt) in enumerate(load_ops(a.ops)):
        for slot, q in (("c2", c2), ("c1", c1), ("tgt", tgt)):
            if q in watch and q not in first:
                first[q] = {
                    "op_index": i,
                    "kind": KIND.get(kind, kind),
                    "slot": slot,
                    "t": tgt, "c1": c1, "c2": c2,
                }
                hits.append(q)
    ok = not hits
    print(json.dumps({
        "watch_lanes": sorted(watch),
        "clean": ok,
        "violations": len(hits),
        "first_touch": {str(k): first[k] for k in sorted(first)},
    }, indent=2))
    return 0 if ok else 1


def cmd_simulate(a):
    """Bit simulation. Sound ONLY for X/CX/Swap/CCX streams (the campaign's
    template asserts exactly that, q793_lifecycle_r03.rs:126). Any other kind
    is reported as unsupported rather than silently mis-modelled."""
    setq = {int(x) for x in a.set.split(",") if x.strip()} if a.set else set()
    state, peak, toffoli, unsupported = set(setq), -1, 0, {}
    n = 0
    for kind, c2, c1, tgt in load_ops(a.ops):
        n += 1
        if a.max_ops and n > a.max_ops:
            break
        for q in (c2, c1, tgt):
            if q != NO_QUBIT and q > peak:
                peak = q
        if kind == 6:                                   # X
            state ^= {tgt}
        elif kind == 8:                                 # CX
            if c1 in state:
                state ^= {tgt}
        elif kind == 13:                                # CCX
            toffoli += 1
            if c1 in state and c2 in state:
                state ^= {tgt}
        elif kind == 10:                                # Swap
            a_in, b_in = tgt in state, c1 in state
            if a_in != b_in:
                state ^= {tgt, c1}
        else:
            unsupported[KIND.get(kind, kind)] = \
                unsupported.get(KIND.get(kind, kind), 0) + 1
    print(json.dumps({
        "ops_simulated": min(n, a.max_ops or n),
        "peak_qubit_id": peak,
        "qubits_upper_bound": peak + 1,
        "toffoli_executed": toffoli,
        "final_ones": sorted(state),
        "final_ones_count": len(state),
        "unsupported_kinds": unsupported,
        "sound": not unsupported,
    }, indent=2))
    return 0


# --------------------------------------------------------------------------
# Paper lemmas
# --------------------------------------------------------------------------
def _inv_mod(a, m):
    a %= m
    if a == 0:
        raise ValueError("not invertible")
    return pow(a, -1, m)


def _num(s):
    """Accept 123, 0x1f, 0b1010, 0o17 — field constants are usually hex."""
    return int(s, 0)


def _rotl(x, k, m):
    k %= m
    return ((x << k) | (x >> (m - k))) & ((1 << m) - 1) if k else x & ((1 << m) - 1)


def _rotr(x, k, m):
    k %= m
    return ((x >> k) | (x << (m - k))) & ((1 << m) - 1) if k else x & ((1 << m) - 1)


def cmd_inplace(a):
    """Lemma 5(3) + Fig 6: replacement of x by y under the INTEGER relation
    A*x + B*y = C, with 0 <= x, y < 2^m.

    NOTE the relation is an integer equation, NOT a congruence (eq (12)).  The
    constructed map is a permutation of all 2^m target strings that agrees with
    y on the satisfying pairs.  We build the map from the paper's recipe and
    then brute-force: (a) it must be a bijection of Z_{2^m}; (b) on every
    satisfying integer pair it must return exactly y.  (b) is the check that a
    campaign needs -- a relation that is the wrong shape silently corrupts
    state, and 'exact in-place' rests entirely on this."""
    A, B, C, m = a.A, a.B, a.C, a.m
    if m > a.max_bits:
        raise SystemExit(f"refusing brute force at m={m} (cap {a.max_bits})")
    if A == 0 or B == 0:
        raise SystemExit("A and B must be nonzero (Lemma 5(3))")
    mod = 1 << m
    out = {"A": A, "B": B, "C": C, "m": m, "relation": "integer A*x + B*y = C"}

    def v2(x):
        if x == 0:
            return None
        k = 0
        while x % 2 == 0:
            x //= 2
            k += 1
        return k

    nu = min(v2(A), v2(B))
    if nu is not None and C % (1 << nu) != 0:
        out["case"] = "no_integer_solutions"
        out["note"] = ("2^nu does not divide C, so no integer solutions exist; "
                       "paper: use the identity permutation")
        print(json.dumps(out, indent=2))
        return 0
    if nu:
        A, B, C = A >> nu, B >> nu, C >> nu
        out["reduced"] = {"nu": nu, "A": A, "B": B, "C": C}

    alpha, beta = v2(A), v2(B)
    build = None
    if alpha == 0 and beta == 0:
        out["case"] = "both_odd"
        binv = _inv_mod(B, mod)
        build = lambda x: (binv * (C - A * x)) % mod          # noqa: E731
        out["recipe"] = [f"x <- {binv} * (C - {A} x) mod 2^{m}   (odd slope)"]
    elif beta == 0:                                            # A even, B odd
        a_odd = A >> alpha
        binv = _inv_mod(B, mod)
        y0 = (C * binv) % (1 << alpha)
        d0 = (C - B * y0) >> alpha
        build = lambda x: _rotl((binv * (d0 - a_odd * x)) % mod, alpha, m) ^ y0
        out["case"] = "only_B_odd"
        out["alpha"] = alpha
        out["recipe"] = [
            f"y0 = C*B^-1 mod 2^{alpha} = {y0}",
            f"D0 = (C - B*y0) / 2^{alpha} = {d0}",
            f"x <- B^-1 (D0 - {a_odd} x) mod 2^{m}   (odd slope)",
            f"rotate register LEFT by {alpha}; XOR y0 into low {alpha} bits",
        ]
    else:                                                      # A odd, B even
        b_odd = B >> beta
        x0 = (C * _inv_mod(A, mod)) % (1 << beta)
        d0 = (C - A * x0) >> beta
        binv = _inv_mod(b_odd, mod)
        build = lambda x: (binv * (d0 - A * _rotr(x ^ x0, beta, m))) % mod
        out["case"] = "only_A_odd"
        out["beta"] = beta
        out["recipe"] = [
            f"x0 = C*A^-1 mod 2^{beta} = {x0}",
            f"D0 = (C - A*x0) / 2^{beta} = {d0}",
            f"XOR x0 into low {beta} bits, rotate RIGHT by {beta}",
            f"x <- {binv} * (D0 - A x) mod 2^{m}   (odd slope)",
        ]

    if a.no_verify or build is None:
        print(json.dumps(out, indent=2))
        return 0

    img = [build(x) for x in range(mod)]
    is_bij = len(set(img)) == mod
    sat, agree, bad = 0, 0, []
    for x in range(mod):
        rem = C - A * x
        if rem % B == 0:
            y = rem // B
            if 0 <= y < mod:
                sat += 1
                if build(x) == y:
                    agree += 1
                elif len(bad) < 3:
                    bad.append({"x": x, "want_y": y, "got": build(x)})
    out["check"] = {
        "bijection_on_all_2^m": is_bij,
        "satisfying_pairs": sat,
        "agreeing_pairs": agree,
        "mismatches": bad,
        "exact": bool(is_bij and sat == agree and sat > 0),
    }
    print(json.dumps(out, indent=2))
    return 0 if out["check"]["exact"] else 1


def cmd_capacity(a):
    """§4.1 / §4.2 / eq (7). Sizes and combined-bit-length bounds.

    N_main = n + 8b + 16, N_short = h + 8b + 16, h = floor(n/2)   (eq 7)
    For positive u,v with uv < 2^n:  len(u) + len(v) <= n + 1
    Product bound eq (24):  r't' = cp + eps r't <= (c+1) p
    Exchange bound (paper, after Alg. 2):  cap_b(r) + cap_b(t') < n + 4b + 3
    """
    n, b = a.n, a.b
    h = n // 2
    cap = lambda x: 0 if x == 0 else (x - 1) // b + 1   # cells, rounded to b
    out = {
        "n": n, "b": b, "h": h,
        "N_main_eq7": n + 8 * b + 16,
        "N_short_eq7": h + 8 * b + 16,
        "combined_len_bound_n_plus_1": n + 1,
        "exchange_cap_bound_n_plus_4b_plus_3": n + 4 * b + 3,
    }
    if a.u is not None and a.v is not None:
        u, v = a.u, a.v
        prod = u * v
        out["uv"] = prod
        out["uv_below_2^n"] = prod < (1 << n)
        out["len_u_plus_len_v"] = u.bit_length() + v.bit_length()
        out["combined_bound_holds"] = (
            u.bit_length() + v.bit_length() <= n + 1)
        if prod >= (1 << n):
            out["warning"] = "uv >= 2^n: the n+1 combined bound does NOT apply"
        out["cells_u"] = cap(u)
        out["cells_v"] = cap(v)
    print(json.dumps(out, indent=2))
    return 0


def cmd_pebble(a):
    """Lemma 4: an oblivious program with T ops and S working bits has an exact
    XOR implementation using O(S) ancillas and O(T^2/S + T) Toffoli gates.

    The whole trade is the ratio T/S: pebbling replaces stored working memory
    with recomputation, and the program is recomputed about T/S times.  When a
    working bit is touched ~T/S times, pebbling pays only if T/S is small.
    Reports the verdict so this prices 'recompute instead of store' offline."""
    T, S = a.T, a.S
    if S <= 0 or T <= 0:
        raise SystemExit("T and S must be positive")
    ratio = T / S
    cost = T * ratio + T                      # = T^2/S + T
    viable = ratio <= a.max_blowup
    print(json.dumps({
        "T_ops": T,
        "S_working_bits": S,
        "T_over_S": round(ratio, 3),
        "segments_qseg_ceil_S": math.ceil(ratio),
        "toffoli_qseg_squared_over_S_plus_T": round(cost, 1),
        "toffoli_baseline_store_all": T,
        "blowup_x": round(ratio + 1, 4),
        "viable": viable,
        "verdict": (
            f"PASS: pebbling costs ~{round(ratio + 1, 2)}x the store-all baseline"
            if viable else
            f"KILL: each working bit is reused ~{ratio:,.0f}x, so pebbling "
            f"recomputes the program ~{ratio:,.0f} times "
            f"(~{round(ratio + 1, 1)}x blowup). Pebbling pays only when T/S is "
            f"small; here it is not."),
        "threshold_max_blowup": a.max_blowup,
    }, indent=2))
    return 0 if viable else 1


def cmd_exceptional(a):
    """Lemma 12/13: for fixed Q0=(u,v) on E: y^2 = x^3 + ax + b over F_p, the
    nonexceptional P are those outside {O, Q0, -Q0, -2Q0} (plus two-torsion when
    v=0). The correction is supported on at most 2|E| <= 8 strings.

    Enumerates the canonical encodings and reports the exceptional set size."""
    p, A, B, u, v = a.p, a.a, a.b, a.u, a.v

    def curve_y2(x):
        return (pow(x, 3, p) + A * x + B) % p

    def sqrt_mod(n):
        if n % p == 0:
            return 0
        if pow(n, (p - 1) // 2, p) != 1:
            return None
        if p % 4 == 3:
            return pow(n, (p + 1) // 4, p)
        q, s, z = p - 1, 0, 2
        while q % 2 == 0:
            q //= 2
            s += 1
        while pow(z, (p - 1) // 2, p) != p - 1:
            z += 1
        m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
        while t != 1:
            i, t2 = 0, t
            while t2 != 1:
                t2 = t2 * t2 % p
                i += 1
            bb = pow(c, 1 << (m - i - 1), p)
            m, c = i, bb * bb % p
            t, r = t * c % p, r * bb % p
        return r

    def neg(P):
        if P is None:
            return None
        x, y = P
        return (x, (-y) % p)

    def add(P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        (x1, y1), (x2, y2) = P, Q
        if x1 == x2 and (y1 + y2) % p == 0:
            return None
        if P == Q:
            if y1 == 0:
                return None
            lam = (3 * x1 * x1 + A) * _inv_mod(2 * y1, p) % p
        else:
            lam = (y2 - y1) * _inv_mod((x2 - x1) % p, p) % p
        x3 = (lam * lam - x1 - x2) % p
        return (x3, (lam * (x1 - x3) - y1) % p)

    Q0 = (u, v)
    if curve_y2(u) != (v * v) % p:
        raise SystemExit(f"Q0={(u, v)} is not on the curve mod {p}")
    E = [None, Q0, neg(Q0), add(Q0, Q0), neg(add(Q0, Q0))]
    seen, uniq = set(), []
    for P in E:
        key = "O" if P is None else P
        if key not in seen:
            seen.add(key)
            uniq.append(P)
    out = {
        "p": p, "Q0": [u, v],
        "exceptional_set": ["O" if P is None else list(P) for P in uniq],
        "exceptional_size": len(uniq),
        "lemma13_bound_2E_le_8": len(uniq) <= 8,
        "two_torsion_addend": v == 0,
        "note": ("Lemma 13: Corr is supported on at most 2|E| <= 8 strings via "
                 "disjoint paths/cycles over canonical encodings"),
    }
    print(json.dumps(out, indent=2))
    return 0 if len(uniq) <= 8 else 1


def cmd_diff(a):
    """Compare two op streams. This is the tool for a claim of the form 'this
    change moves Q only' or 'T is byte-identical' -- the campaign makes those
    claims constantly and they are cheap to prove or refute here."""
    A = list(load_ops(a.left))
    B = list(load_ops(a.right))
    ta = sum(1 for k, *_ in A if k in TOFFOLI_KINDS)
    tb = sum(1 for k, *_ in B if k in TOFFOLI_KINDS)
    pa = max((q for _, c2, c1, t in A for q in (c2, c1, t)
              if q != NO_QUBIT), default=-1)
    pb = max((q for _, c2, c1, t in B for q in (c2, c1, t)
              if q != NO_QUBIT), default=-1)
    first = None
    for i, (x, y) in enumerate(zip(A, B)):
        if x != y:
            first = i
            break
    if first is None and len(A) != len(B):
        first = min(len(A), len(B))
    out = {
        "left": {"ops": len(A), "toffoli": ta, "peak_qubit_id": pa},
        "right": {"ops": len(B), "toffoli": tb, "peak_qubit_id": pb},
        "delta_ops": len(B) - len(A),
        "delta_toffoli": tb - ta,
        "delta_peak_qubit_id": pb - pa,
        "identical_stream": A == B,
        "first_difference_op": first,
        "identical_toffoli": ta == tb,
    }
    if first is not None and first < len(A) and first < len(B):
        out["left_op"] = {"kind": KIND.get(A[first][0], A[first][0]),
                          "c2": A[first][1], "c1": A[first][2], "tgt": A[first][3]}
        out["right_op"] = {"kind": KIND.get(B[first][0], B[first][0]),
                           "c2": B[first][1], "c1": B[first][2], "tgt": B[first][3]}
    print(json.dumps(out, indent=2))
    return 0


def cmd_selftest(a):
    """Verify every atom against ground truth. Run this after any edit to rci.py;
    a checker that is itself wrong is worse than no checker."""
    results = []

    def check(name, got, want):
        ok = got == want
        results.append({"check": name, "ok": ok, "got": got, "want": want})
        return ok

    # --- Lemma 5(3): the four cases, each against brute force -------------
    def build_map(A, B, C, m):
        mod = 1 << m

        def v2(x):
            k = 0
            while x and x % 2 == 0:
                x //= 2
                k += 1
            return k
        nu = min(v2(A), v2(B))
        if C % (1 << nu):
            return None
        A, B, C = A >> nu, B >> nu, C >> nu
        if A % 2 and B % 2:
            bi = _inv_mod(B, mod)
            return lambda x: (bi * (C - A * x)) % mod
        if B % 2:
            al = v2(A)
            a_odd, bi = A >> al, _inv_mod(B, mod)
            y0 = (C * bi) % (1 << al)
            d0 = (C - B * y0) >> al
            return lambda x: _rotl((bi * (d0 - a_odd * x)) % mod, al, m) ^ y0
        be = v2(B)
        b_odd, x0 = B >> be, (C * _inv_mod(A, mod)) % (1 << be)
        d0 = (C - A * x0) >> be
        bi = _inv_mod(b_odd, mod)
        return lambda x: (bi * (d0 - A * _rotr(x ^ x0, be, m))) % mod

    for (A, B, C, m) in [(3, 5, 20, 6), (4, 3, 22, 6), (3, 4, 30, 6), (7, 9, 40, 6)]:
        f = build_map(A, B, C, m)
        mod = 1 << m
        bijective = len({f(x) for x in range(mod)}) == mod if f else False
        agree = True
        for x in range(mod):
            rem = C - A * x
            if rem % B == 0 and 0 <= rem // B < mod:
                y = rem // B
                if f is None or f(x) != y:
                    agree = False
        check(f"inplace A={A} B={B} C={C} m={m} exact",
              bool(bijective and agree), True)
    check("inplace 2x+4y=7 m=6 -> no integer solutions",
          build_map(2, 4, 7, 6), None)

    # --- capacity: eq (7) ------------------------------------------------
    check("capacity eq7 N_main n=256 b=8", 256 + 8 * 8 + 16, 336)
    check("capacity eq7 N_short n=256 b=8", 128 + 8 * 8 + 16, 208)

    # --- pebble: Lemma 4 -------------------------------------------------
    T, S = 1000, 100
    check("pebble T^2/S+T at T=1000 S=100", int(T * T / S + T), 11000)

    # --- exceptional: secp256k1 generator, |E| = 5 ------------------------
    GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    import io as _io
    import contextlib
    buf = _io.StringIO()
    with contextlib.redirect_stdout(buf):
        cmd_exceptional(argparse.Namespace(p=P, a=0, b=7, u=GX, v=GY))
    check("exceptional |E| for secp256k1 G", json.loads(buf.getvalue())["exceptional_size"], 5)

    failed = [r for r in results if not r["ok"]]
    print(json.dumps({"passed": len(results) - len(failed), "failed": len(failed),
                      "results": results if a.verbose else failed}, indent=2))
    return 0 if not failed else 1


# --------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(prog="rci", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("census", help="op/Toffoli/peak census of ops.bin")
    c.add_argument("ops")
    c.set_defaults(fn=cmd_census)

    h = sub.add_parser("holes", help="detect ops touching omitted lanes")
    h.add_argument("ops")
    h.add_argument("--lanes", required=True, help="e.g. 255,256,257,258")
    h.set_defaults(fn=cmd_holes)

    s = sub.add_parser("simulate", help="X/CX/Swap/CCX bit simulation")
    s.add_argument("ops")
    s.add_argument("--set", default="", help="qubits to initialise to |1>")
    s.add_argument("--max-ops", type=int, default=0)
    s.set_defaults(fn=cmd_simulate)

    i = sub.add_parser("inplace", help="Lemma 5(3): Ax+By=C replacement")
    i.add_argument("--A", type=_num, required=True)
    i.add_argument("--B", type=_num, required=True)
    i.add_argument("--C", type=_num, required=True)
    i.add_argument("--m", type=int, required=True)
    i.add_argument("--no-verify", action="store_true")
    i.add_argument("--max-bits", type=int, default=12)
    i.set_defaults(fn=cmd_inplace)

    k = sub.add_parser("capacity", help="§4.1/§4.2 layout + length bounds")
    k.add_argument("--n", type=int, required=True)
    k.add_argument("--b", type=_num, default=1)
    k.add_argument("--u", type=_num)
    k.add_argument("--v", type=_num)
    k.set_defaults(fn=cmd_capacity)

    pb = sub.add_parser("pebble", help="Lemma 4: T^2/S + T cost + viability")
    pb.add_argument("--T", type=int, required=True)
    pb.add_argument("--S", type=int, required=True)
    pb.add_argument("--max-blowup", type=float, default=4.0,
                    help="T/S above which pebbling is declared a KILL (default 4)")
    pb.set_defaults(fn=cmd_pebble)

    e = sub.add_parser("exceptional", help="Lemma 12/13 exceptional set")
    e.add_argument("--p", type=_num, required=True)
    e.add_argument("--a", type=_num, required=True)
    e.add_argument("--b", type=_num, required=True)
    e.add_argument("--u", type=_num, required=True)
    e.add_argument("--v", type=_num, required=True)
    e.set_defaults(fn=cmd_exceptional)

    d = sub.add_parser("diff", help="compare two ops streams")
    d.add_argument("left")
    d.add_argument("right")
    d.set_defaults(fn=cmd_diff)

    st = sub.add_parser("selftest", help="verify every atom against ground truth")
    st.add_argument("--verbose", action="store_true")
    st.set_defaults(fn=cmd_selftest)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())

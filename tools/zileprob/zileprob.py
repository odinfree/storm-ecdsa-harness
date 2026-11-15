#!/usr/bin/env python3
"""Zileprob: exhaustive 16-wire model of one multi-class digit slot (lead "Vorzeichezile": signed, non-restoring rows).
Run: python3 zileprob.py   (about 10 s, no arguments, prints the table in out_zileprob.txt)
Geometry taken from the row emitter of the frame we built our 763 row on (Akashneelesh's public row 8396ec91 and the
lineage its note credits) and its big-slot call site: row k pairs target wire a with operand wire a + k
(public), the operand's own position depends on the class e, wires below the class's start hold other data (g),
row k is active for classes e > k (trailing rows inactive), one mask literal gates the low wires.
Reference = restoring rows (3 CCX per plain wire). Candidates = signed (offset) rows.
Every case: class e in 0..K, divisor s, remainder-in t < s*2^e, garbage g < 2^e. Integer + bit level, mod 2^W."""
import itertools, sys
W, K, NS, L = 16, 4, 5, 1
MASK = (1 << W) - 1
def cases():
    for e in range(K + 1):
        for s in range(1, 1 << NS):
            for t in range(s << e):
                for g in range(1 << e):
                    yield e, s, t, g
def operand(e, s, g, k):                # raw operand of row k on the target's wires (public pairing)
    sx = (s << (e + L - 1)) | g
    return sx >> (k + L)
def start(e, k): return e - 1 - k if k < e else None
def ref(e, s, t):                       # restoring rows: digits (msb first) and remainder
    d = []
    for k in range(e):
        o = s << (e - 1 - k)
        b = 1 if t >= o else 0
        t -= b * o; d.append(b)
    return t, d
def addsub(t, o, sub, st, mask_carry, mask_sum):
    """bit-level t (+/-) o on W wires. st = first masked-in wire (None: mask never on).
    mask_carry: carries only run on wires >= st. mask_sum: sum XOR only on wires >= st."""
    if sub: o = ~o & MASK
    c = 1 if sub else 0
    out = 0
    for i in range(W):
        ti, oi = (t >> i) & 1, (o >> i) & 1
        on = st is not None and i >= st
        if mask_carry and not on:
            ci = 0; oi_eff = oi; carry_live = False
        else:
            ci = c; carry_live = True
        if on and mask_carry and i == st: ci = 1 if sub else 0
        if (not mask_sum) or on:
            si = ti ^ oi ^ ci
        else:
            si = ti
        if carry_live or (on and mask_carry):
            c = (ti & oi) | (ti & ci) | (oi & ci)
        out |= si << i
    return out
def run(form, e, s, t, g):
    """returns final target value (signed two's complement on W wires) after K rows"""
    neg = 0                              # sign of the running remainder (0: next row subtracts)
    T = t
    for k in range(K):
        o = operand(e, s, g, k); st = start(e, k); act = k < e
        if form == "A_unmasked_natural":         # 2 CCX everywhere, trailing rows continue by remainder sign
            T = addsub(T, o, not neg, 0, False, False)
        elif form == "B_unmasked_forced":        # 2 CCX everywhere, trailing rows forced: first +, then -
            if act: sub = not neg
            else: sub = (k != e) if e > 0 else (k != 0)
            if e == 0 and k == 0: sub = False
            T = addsub(T, o, sub, 0, False, False)
        elif form == "C_maskcarry_plainsum":     # carry masked (as today), sum XOR without its third Toffoli
            if act: T = addsub(T, o, not neg, st, True, False)
            else:   T = addsub(T, o, True, None, True, False)
        elif form == "D_masked_actctl":          # mask and activity kept on the sum: 3 CCX per wire (control form)
            if act: T = addsub(T, o, not neg, st, True, True)
        neg = (T >> (W - 1)) & 1
    return T
def main():
    forms = ["A_unmasked_natural", "B_unmasked_forced", "C_maskcarry_plainsum", "D_masked_actctl"]
    n = 0
    bad = {f: 0 for f in forms}; badg0 = {f: 0 for f in forms}; ng0 = 0
    fix1 = {f: 0 for f in forms}        # exact after ONE correction add of the class's own unit operand when negative
    spread = {f: {} for f in forms}     # (e, s, g) -> set of (T_final - r) seen over t
    for e, s, t, g in cases():
        n += 1; ng0 += (g == 0)
        r, d = ref(e, s, t)
        for f in forms:
            T = run(f, e, s, t, g)
            ok = (T == r)
            Tc = (T + s) & MASK if (T >> (W - 1)) & 1 else T      # ideal correction (class-dependent row!)
            okc = (Tc == r)
            if not ok: bad[f] += 1
            if not okc: fix1[f] += 1
            if g == 0 and not okc: badg0[f] += 1
            spread[f].setdefault((e, s, g), set()).add((T - r) & MASK)
    print(f"cases {n} (W={W} wires, K={K} rows, classes 0..{K}, s < 2^{NS}); g = 0 subset {ng0}")
    for f in forms:
        sp = spread[f]; k1 = sum(1 for v in sp.values() if len(v) <= 2); mx = max(len(v) for v in sp.values())
        print(f"{f:22} raw mismatches {bad[f]:7}  after ideal sign correction {fix1[f]:7}  "
              f"(g=0 only: {badg0[f]:7})  (e,s,g) classes with <=2 offsets {k1}/{len(sp)}, max offsets {mx}")
    # per class for the forms of interest
    for f in forms[:3]:
        per = {}
        for e, s, t, g in cases():
            r, _ = ref(e, s, t); T = run(f, e, s, t, g)
            Tc = (T + s) & MASK if (T >> (W - 1)) & 1 else T
            a = per.setdefault(e, [0, 0]); a[0] += 1; a[1] += (Tc != r)
        print(f, "per class (cases, wrong after correction):", {e: tuple(v) for e, v in per.items()})
    print("CCX per plain wire per row: restoring 3; forms A, B 2; form C 2 on the sum-unmasked wires; form D 3.")
    # positive control: with every row active and no foreign data below the operand, the signed row IS exact
    n = wrong = 0
    for e, s, t, g in cases():
        if e != K or g != 0: continue
        r, _ = ref(e, s, t); T = run("A_unmasked_natural", e, s, t, g)
        Tc = (T + s) & MASK if (T >> (W - 1)) & 1 else T
        n += 1; wrong += (Tc != r)
    print(f"positive control: class K (all rows active), g=0, form A: {n} cases, wrong {wrong}")
if __name__ == "__main__":
    main()

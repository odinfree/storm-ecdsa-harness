#!/usr/bin/env python3
"""align.py OLD.glz NEW.glz [K=48] [MIN=2000] (Fadespüeli): map runs of NEW onto OLD by exact K-gate windows.
Markers (ops 3/4) compare equal to plain CCX. Prints matched segments >= MIN gates and totals with CCX."""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import gl
A, _, _, _ = gl.load(sys.argv[1]); B, _, _, _ = gl.load(sys.argv[2])
K = int(sys.argv[3]) if len(sys.argv) > 3 else 48
MIN = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
idx = {}
for i in range(0, len(A) - K + 1):
    h = hash(tuple(A[i:i + K]))
    if h not in idx: idx[h] = i
segs, j = [], 0
while j <= len(B) - K:
    i = idx.get(hash(tuple(B[j:j + K])))
    if i is None or A[i:i + K] != B[j:j + K]: j += 1; continue
    a, b = i, j
    while a < len(A) and b < len(B) and A[a] == B[b]: a += 1; b += 1
    segs.append((j, b, i, a)); j = b
ccx = lambda g, lo, hi: sum(1 for x in g[lo:hi] if len(x) == 3)
tot = totc = 0
for (j0, j1, i0, i1) in segs:
    c = ccx(B, j0, j1)
    if j1 - j0 >= MIN: print("new [%d, %d) = old [%d, %d)  %d gates, %d CCX" % (j0, j1, i0, i1, j1 - j0, c))
    tot += j1 - j0; totc += c
print("matched new gates %d of %d (CCX %d of %d); old has %d gates (CCX %d); segments %d" % (tot, len(B), totc, ccx(B, 0, len(B)), len(A), ccx(A, 0, len(A)), len(segs)))

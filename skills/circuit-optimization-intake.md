# Skill: Circuit Optimization Intake

Use when turning an idea, paper lever, public frontier lesson, or failed route
into a ranked set of ECDSA circuit experiments.

## Goal

Create several score-eligible, falsifiable route packets before spending GPU
time. The GPU should confirm a viable circuit theory, not replace one.

## Intake Order

1. `frontier-lock`.
2. `benchmark-frontier-archaeology` or a source-backed paper card.
3. `peak-qubit-reduction` and/or `toffoli-reduction`.
4. `reversible-circuit-validation`.
5. `island-hunting-bakeoff`.
6. `route-compute-gate`.

## Protocol

1. Freeze the base:
   public frontier, source hash, q, Toffoli, score, validator, and known
   binder owners.
2. Generate a slate of distinct routes. Vary mechanisms, not only one knob by
   one notch.
3. For each route, state the theory:
   live-range change, codec, carry/borrow change, measured cleanup, replay,
   pseudo-Mersenne fold, square segment, or validation/tooling improvement.
4. Name the expected metric movement:
   q, emitted Toffoli, average-executed Toffoli, score, and depth risk.
5. Name the first falsifier:
   clean rebuild, peak trace, source/candidate hash diff, toy self-test,
   random differential, failing-shot overlap, or short density pilot.
6. Reject routes that cannot beat the current frontier even under their own
   estimates.
7. For dirty routes, diagnose and repair before hunting. Record the invariant
   being violated and the smallest mechanism to patch.
8. Promote only a short ranked slate into equal-size pilot scans.

## Route Packet

```text
Optimization intake:
- Base frontier:
- Source hash:
- Route name:
- Mechanism:
- Expected q:
- Expected emitted Toffoli:
- Expected avg-executed Toffoli:
- Expected score:
- Binder affected:
- Correctness risk:
- First falsifier:
- Repair plan if dirty:
- Next gate:
```

## Ranking

Prefer routes with:

- score margin against the current frontier;
- direct contact with a measured binder or hot spot;
- one understandable mechanism;
- explicit `cls/pha/anc` obligation;
- a cheap falsifier;
- a nearby repair if the first version is dirty.

Demote routes that depend on stale knobs, unchanged off-peak phases, copied
nonces, cache-only measurements, private artifacts, or unbounded "try harder"
search.

## Kill Gate

No compute request follows from intake alone. A route must pass frontier lock,
score gate, validator plan, owner, budget, and stop condition before
`route-compute-gate` can open.

## Public Boundary

Keep packets source-bound and public-safe. Do not include private mailbox
history, raw logs, endpoints, keys, account data, unreleased diffs, full
candidate lists, or private paths.

## Credit

Adapted from ECDSA circuit-optimization workflow discipline, reduced to a
public route-intake gate for this harness.

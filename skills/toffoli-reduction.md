# Skill: Toffoli Reduction

Use when a route aims to reduce emitted Toffoli, average executed Toffoli,
T-count, or non-Clifford hot spots without losing the q factor or correctness.

## Goal

Classify the hot spot, choose the count-cut primitive that fits it, and
re-measure both score factors before any route is promoted.

## Metric Split

State the metric first:

- `emitted`: every CCX/T in the circuit counts;
- `average-executed`: gates are weighted by benchmark-shot execution.

Conditional replay can improve average-executed cost while leaving emitted
hardware cost unchanged. Report both when possible.

## Protocol

1. Refresh the current frontier and candidate base.
2. Measure q, emitted Toffoli, average-executed Toffoli, score, and source
   hashes from a clean rebuild.
3. Identify the hot spot by phase or op family.
4. Classify the hot spot:
   carry-uncompute, recomputed scratch, data-controlled arithmetic, majority,
   redundant cleanup, full materialization, repeated stage, or off-peak knob.
5. Pick a move that matches the class:
   vent, conditional replay, fused fold, measured cleanup, ancilla-free
   majority, skip-proven cleanup, streamed materialization, or off-peak
   loosening.
6. Price the move:
   Toffoli saved, qubits added, depth impact, phase risk, and score delta.
7. Re-measure both q and Toffoli after the change. A Toffoli win that raises
   peak q can lose the product.
8. Run `reversible-circuit-validation` for any measurement, cleanup, aliasing,
   or conditional replay edit.

## Hot-Spot Packet

```text
Toffoli reduction:
- Source hash:
- Candidate hash:
- Metric type:
- q before/after:
- emitted Toffoli before/after:
- avg-executed Toffoli before/after:
- Hot spot:
- Move:
- Depth risk:
- cls/pha/anc:
- Decision:
```

## Kill Gate

Do not promote a count cut when it only changes a stale cache, hides emitted
cost behind average-executed language, conditions live data instead of
measurable scratch, skips cleanup without a proof, or reports value correctness
without phase and ancilla checks.

## Public Boundary

Use public metrics and bounded route packets. Do not include private run logs,
candidate dumps, hostnames, endpoints, account data, keys, or unreleased
nonces.

## Credit

Adapted from public Toffoli/T-count optimization discipline for reversible
arithmetic and `ecdsa.fail` route triage.

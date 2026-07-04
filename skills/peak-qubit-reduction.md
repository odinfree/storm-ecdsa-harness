# Skill: Peak Qubit Reduction

Use when a route aims to reduce `peak_qubits` by changing live ranges,
allocation, transcript representation, clean-pool reuse, dirty borrowing, or
co-binder schedules.

## Goal

Reduce the measured peak live set without creating a larger Toffoli penalty or
dirty `cls/pha/anc` behavior than the score can tolerate.

## Core Rule

Peak qubits are a maximum over time. Lowering a register that is not live at
the measured binder does not lower width. First find the binder, then attack
what is actually alive there.

## Protocol

1. Refresh the current frontier and score model.
2. Force a clean measurement of the candidate base. Record peak q, Toffoli,
   score, source hash, candidate hash, and build-cache evidence.
3. Trace the peak owner. Name every phase that reaches the maximum, not only
   the first line printed.
4. Inventory the live set at each binder:
   essential data, scratch, transcript/log, passenger, alias candidate,
   truncatable lane, or borrowed host.
5. Build a co-binder ledger. If several phases tie, require a compatible local
   cut for each before expecting the global peak to move.
6. Price each proposed cut:
   qubits saved, Toffoli added or removed, depth risk, validation risk, and
   whether the route remains below the current frontier score.
7. Prefer moves whose target is live at the binder:
   passenger relocation, live-range hole, codec/streamed transcript,
   clean-pool reuse, dirty borrow with restore proof, suffix carry parking, or
   per-step schedule.
8. Validate value, phase, and ancilla behavior before any island search.
9. Re-trace after every local win. The next binder is the next target.

## Plateau Ledger

```text
Peak qubit ledger:
- Current q:
- Score model:
- Binder owners:
- Live-set suspects:
- Local reductions:
- Co-binders still at peak:
- Gate/depth cost:
- Validation status:
- Combined package:
- Decision:
```

## Binary-Failure Warning

Structural width cuts are usually value-exact or broken. Do not treat a dirty
width edit like a graded truncation that can be solved by more nonce scanning.
Validate the edit first, then hunt only if the route is theoretically viable.

## Kill Gate

Do not scale a width route when it targets an off-peak register, lacks a
live-set ledger, relies on one local cut while other co-binders still pin the
peak, exceeds the q/Toffoli exchange rate without an explicit reason, or has
nonzero `pha/anc` that is not localized.

## Public Boundary

Keep output to source hashes, metric summaries, invariant names, and public
route packets. Do not publish private traces, full op streams, host data,
unreleased candidates, keys, endpoints, or private paths.

## Credit

Adapted from public peak-live and co-binder workflow discipline for reversible
ECDSA circuit optimization.

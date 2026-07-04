# Skill: Benchmark Frontier Archaeology

Use when a public `ecdsa.fail` frontier moves and a worker needs to extract the
actual transferable lesson before proposing a route.

## Goal

Turn adjacent public submissions into a mechanism ledger:

- what changed;
- which metric moved;
- whether the lever transfers;
- which binder became the next target.

This is an intake card. It does not authorize compute, claims, or submit work.

## Source Order

1. Fresh public frontier and accepted-submission list.
2. Adjacent accepted source commits or public diffs.
3. Public submission notes.
4. Locally reproduced metrics from a clean tree.
5. Fixture-safe route history.

## Protocol

1. Refresh the public frontier first. Record submission id, source hash, q,
   Toffoli, and score.
2. Walk every accepted intermediate between the last understood point and the
   new frontier. Diff adjacent pairs only.
3. Scope diffs to submitted/editable paths. Ignore generated files, local
   instrumentation, private notes, and harness noise.
4. For each adjacent pair, isolate the smallest plausible lever:
   knob, structural schedule, transcript codec, carry/borrow lifetime,
   square segment, cleanup rule, nonce/island artifact, or validator change.
5. Re-measure q and Toffoli from a clean rebuild before attributing a delta.
   If exact score arithmetic does not reconcile, stop and resolve the
   measurement.
6. Decompose the score movement by factor:
   q delta, Toffoli delta, score delta, and exchange rate.
7. Track binder migration. Name the phase that bound before the change and the
   phase that binds after the change.
8. Classify the lever:
   `transferable`, `artifact`, `tooling`, `validation`, or `unknown`.
9. Emit one route-intake row per lever and hand it to the relevant next card.

## Transfer Test

A lever transfers when it is a mechanism that can be rebuilt on a fresh base:

- source or CFG change with a measured q/Toffoli effect;
- codec or schedule with a self-test obligation;
- live-range or cleanup move with a named invariant;
- Toffoli move whose emitted/executed metric is understood.

A lever does not transfer directly when it is a hunted nonce, stale state file,
cached build artifact, fitted constant, or private run artifact. Re-hunt those
against the new route.

## Output

```text
Frontier archaeology:
- Current frontier:
- Adjacent pair:
- Lever:
- Metric movement:
- Binder before:
- Binder after:
- Transfer class:
- Evidence:
- Next card:
- Kill gate:
```

## Kill Gate

Do not promote a frontier lesson if it comes from a non-adjacent endpoint diff,
unreconciled score arithmetic, stale `ops.bin`, a copied nonce, or an
unverified public note.

## Follow-On Routing

- Width lever: `peak-qubit-reduction`.
- Count lever: `toffoli-reduction`.
- Dirty or correctness-risk lever: `reversible-circuit-validation`.
- Several possible routes: `circuit-optimization-intake` then
  `island-hunting-bakeoff`.
- Submit language: `validation-submit-gate`.

## Public Boundary

Use public submissions and fixture-safe notes only. Do not include private
mailbox history, raw scan logs, endpoints, keys, account data, unreleased
diffs, or nonce assignments.

## Credit

Adapted from public benchmark archaeology workflow discipline for visible
frontier histories. This repo card is a public-safe summary.

# Skill: Reversible Circuit Validation

Use when a candidate circuit route changes arithmetic, allocation, cleanup,
measurement, aliasing, transcript codecs, or any op stream that can affect
correctness.

## Goal

Validate the route across the three independent channels:

- `cls`: classical output value;
- `pha`: relative phase;
- `anc`: ancilla cleanliness and disentanglement.

A route is not clean because its output bits look correct. It is clean only
when the required channels are verified for the intended use.

## Protocol

1. State the required channel set. For coherent reversible use, require
   `cls`, `pha`, and `anc`.
2. Record source hash, candidate hash, CFG/defaults, validator binary hash,
   and test seed.
3. Run differential tests against a trusted reference on random inputs, not
   only on the benchmark shot set.
4. Run forward-inverse identity checks when available. `U^-1 U` should recover
   the full input state, including clean scratch and phase.
5. Report failures as separate `cls/pha/anc` counts. Never collapse them into
   one pass/fail line.
6. Classify failures as designed approximation, validator/tooling issue, or
   real bug. If the route relies on a fixed-shot island, keep that distinction
   explicit.
7. Localize unexpected failures to the first broken operation or section using
   bisection, per-section counters, failing-shot dumps, or invariant checks.
8. Patch the smallest responsible mechanism and rerun all channels, not only
   the channel that failed.

## Per-Channel Zero Screen

For island-hunt routes, sample a batch of GCD-clean candidates and ask whether
each channel reaches zero somewhere:

```text
cls hits 0: <yes/no>
pha hits 0: <yes/no>
anc hits 0: <yes/no>
```

If a channel never reaches zero over a sufficient sample, treat it as a
structural floor until disproven. More nonce scanning is not the first fix;
repair the mechanism that owns that channel.

## Validation Packet

```text
Reversible validation:
- Source hash:
- Candidate hash:
- CFG/defaults:
- Validator:
- Test set:
- Random differential:
- Forward-inverse:
- cls/pha/anc:
- Designed-hard explanation:
- First broken section:
- Decision:
```

## Kill Gate

Do not call a route clean when validation is value-only, fast-reject-only,
missing `pha/anc`, run on a stale binary, run against a different CFG, or based
on a single lucky candidate.

## Public Boundary

Report hashes, metrics, failure classes, and fixture-safe summaries. Do not
publish private logs, unreleased nonces, raw candidate dumps, hostnames,
endpoints, account data, or private paths.

## Credit

Adapted from reversible-circuit `cls/pha/anc` validation discipline and
public-safe ECDSA frontier workflow patterns.

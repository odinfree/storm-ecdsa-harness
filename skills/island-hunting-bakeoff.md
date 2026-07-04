# Skill: Island Hunting Bakeoff

Use when several score-eligible routes survive intake and a worker needs to
choose which one deserves GPU range before a large island hunt.

## Goal

Run equal-size pilots, compare huntability, and commit compute only to a route
with score edge, density, and reachable `0/0/0` evidence.

## Preflight

Before this card:

- `frontier-lock` refreshed the current target;
- `circuit-optimization-intake` produced route packets;
- each route has measured or estimated q/Toffoli/score below the frontier;
- validator and CFG/source hashes are recorded.

## Protocol

1. Select a small slate of genuinely different routes.
2. Assign the same pilot size to each route. Keep ranges bounded and
   non-overlapping.
3. For each pilot, record:
   nonces scanned, GCD-clean candidates, candidates/Mnonce, node/range health,
   and validator status.
4. Validate the GCD-clean candidates as a batch. A single best near miss is not
   enough to rank a route.
5. Build the `cls/pha/anc` distribution:
   best triple, median severity, low-severity tail, repeated fingerprints, and
   whether each channel reaches zero somewhere.
6. Reject stale validator output. Cross-check local and remote validation when
   remote validation is used.
7. Rank routes qualitatively from independent signals:
   score margin, density, per-channel zero reachability, low residuals, diverse
   fingerprints, range stability, and plausible binder contact.
8. Hunt the top route first. Hold or close the others with explicit failure
   classes.

## Bakeoff Table

```text
Island bakeoff:
- Frontier:
- Pilot size:
- Route | score | density | best cls/pha/anc | zero channels | status
- Winner:
- Fallback:
- Closed routes:
- Next range:
- Stop rule:
```

## Stop Rules

Demote or close a route when:

- estimated or measured score no longer beats the frontier;
- candidate density is starved versus healthy baselines;
- one channel never reaches zero over a sufficient sample;
- early candidates share the same high dirty fingerprint;
- no low-severity tail appears after enough validated candidates;
- validator source/CFG/binary does not match the route;
- a node/range anomaly cannot be explained.

## Continue Rules

Continue only when:

- score still has margin;
- density is healthy or yellow with real near misses;
- each channel can hit zero somewhere;
- dirty fingerprints vary;
- validation is reproducible;
- the next range has a bounded budget and stop condition.

## Kill Gate

Do not start a large hunt from one route, one nonce, one unvalidated triple,
fast-reject-only output, stale SOTA, or a route whose clean island is blocked by
a structural channel floor.

## Public Boundary

Report summary metrics, hashes, route names, and decisions. Do not publish raw
nonce assignments, private logs, endpoints, hostnames, account data, keys, or
unreleased candidate dumps.

## Credit

Adapted from public island-hunting triage and route bakeoff discipline for
`ecdsa.fail` candidates.

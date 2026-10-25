# Mission order template

Use only the sections needed, but never omit authority, bounds, decision rights,
or the terminal evidence condition.

```markdown
# Mission Command <ID> — <single result>

Issued: <timestamp and timezone>
Activity: <authorized activity>
Submit: <OPEN or CLOSED from live policy>

## Commander's intent

Purpose: <why now>
Key task: <one concrete deliverable>
End state: <observable terminal condition>

## Authoritative binding

- Repository/worktree: <absolute path>
- Commit: <full hash>
- Tree: <full hash when relevant>
- Route/source: <path and hash>
- Input artifacts: <absolute path and SHA256 for each>
- Live gates: <dispatch, readiness, inventory, submit, timestamp>

## Phase order

- Ball owner: <one role>
- Supporting roles: <parked or distinct later gate>
- Bound: <time, count, numeric interval, builds, and/or files>
- Allowed resources: <exact list>
- Required result: <evidence and verdict>
- First falsifier: <cheapest decisive check>

## Decision rights

Owner may: <reversible in-scope decisions>
Owner may not: <scope expansion and external-state actions>
Escalate on: <conflict, admit, missing authority, or stop trigger>

## Admission and rejection

ADMIT only if: <all correctness, provenance, accounting, and resource gates>
HARD_NACK if: <decisive candidate-specific witness>
Do not classify as HARD_NACK: <timeout, ambiguity, missing evidence>

## Closeout

- Verdict: <ADMIT, COMPLETE, HARD_NACK, or qualified BLOCKED>
- Evidence: <path and SHA256>
- Quantified result: <counts/deltas/peak>
- Scope proof: <diff/status/read-only evidence>
- Actions not taken: <provider/GPU/network/range/submit/etc.>
- Next authorized action: <one phase or STOP>
```

## Compact mailbox form

Adapt to the local line and byte limits:

```text
verdict=<...> submit=<...>; mission=<ID> complete within <bound>.
family_or_result=<exact object>.
binding=<commit/tree/input hashes>.
evidence=<decisive counts and witness>.
delta=<q/CCX/CCZ/time/etc.>.
artifact=<path> sha256=<hash>.
next=<authorized phase or STOP>.
actions_not_taken=<external or forbidden actions>.
```

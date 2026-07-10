# Skill: Diagnose, Test, Verify

Use when work is stuck, an explanation has not been checked, a handoff is
premature, or a completion claim needs proof. The method works across software,
operations, research, analysis, writing, and business development.

## What This Skill Does

1. **Diagnose:** read the direct evidence, reconstruct what happened, and find
   the assumption shared by the failed attempts.
2. **Test:** run the smallest safe check that can distinguish between plausible
   explanations.
3. **Verify:** run the check that proves the requested outcome, then report only
   what that check supports.

The goal is forward progress with evidence. Investigation stays proportional to
the task and inside the user's scope and permissions.

## Trigger

Use this skill when any of these are true:

- the same approach has failed twice,
- the agent keeps changing parameters or wording without changing the idea,
- tooling, data, another team, or the environment is blamed before inspection,
- a user or human handoff is requested before available evidence is checked,
- a plan has stalled without a bounded next check,
- a result is called complete without a test, source, acceptance check, or
  observable outcome,
- the user explicitly asks for a systematic diagnosis or verification pass.

Skip it for a routine first attempt, a known fix already running, or a wait that
depends on an external event. If progress requires a business decision,
access, approval, or other user-only input, inspect the available evidence and
ask for the missing input directly. Request access through an approved channel;
do not ask the user to paste a secret into chat.

## Mode Selector

- **Quick pass:** one unclear assumption or one missing completion check. Read
  the direct evidence, run one bounded test, and verify the result.
- **Full pass:** repeated failures, conflicting evidence, several plausible
  causes, or a handoff that needs an auditable record. Run the full protocol.
- **Critique pass:** an artifact exists and quality is the main issue. Run the
  critique-and-improvement loop, then verify the revised artifact.

## Full Protocol

1. **Define the outcome.** State the requested result and what would prove it.
   If the acceptance check is missing, infer a safe one when the task is
   low-risk. Ask when the choice would change the result or commitment.
2. **Read the direct evidence.** Inspect the actual error, source, data,
   document, conversation, current system state, or acceptance criteria. Use a
   summary only when the original is unavailable.
3. **Reconstruct the attempts.** Record what was tried, what happened, and the
   assumption the attempts shared.
4. **Check the assumption.** Verify current versions, dates, paths, inputs,
   dependencies, permissions, owners, constraints, and source freshness. Check
   the caller, upstream input, downstream consumer, or opposite interpretation
   when the current explanation may be wrong.
5. **Choose the next test.** When the cause is unclear, form at least two
   plausible explanations that require different tests. Choose the smallest
   safe test that separates them and produces useful information whether it
   passes or fails. Define pass, fail, and stop conditions before running it.
6. **Run the test.** Record the result as a fact, inference, eliminated
   explanation, open question, or blocker. If the result is inconclusive, change
   the method or test a different hypothesis. Do not repeat an eliminated
   approach without new evidence.
7. **Check adjacent impact.** After a fix or decision, check the affected area
   for the same failure pattern and inspect relevant upstream or downstream
   effects. Keep this check proportional and inside the original task.
8. **Verify and decide.** Run the completion check. Proceed, revise, pause, stop,
   or request the exact decision or permission needed next.

## Stop Conditions

Stop the loop when any of these are true:

- the requested outcome passes its verification gate,
- the test eliminates the current approach and no supported variant remains,
- the next safe action requires a user decision, access, approval, or external
  event,
- another check would not change the decision,
- the next check would exceed the task's authorized time, cost, or risk.

Difficulty alone is not a stop condition. A failed parameter tweak is not a
reason to hand the task back before testing a different explanation.

## Evidence Labels

- **Fact:** observed directly or supported by a cited source or completed
  check.
- **Inference:** an interpretation supported by facts but not directly
  observed.
- **Hypothesis:** a testable explanation that still needs a check.
- **Unknown:** missing information with no justified conclusion.
- **Blocker:** a specific missing decision, required access, approval, or external
  event that prevents the next safe action.

Never promote an inference or hypothesis to fact because it sounds plausible.
Every blocker must name the action it prevents and what clears it.

## Work-Type Guide

| Work type | Diagnose from | Useful tests | Verification |
| --- | --- | --- | --- |
| Software and data | Full error, relevant source and callers, tests, runtime versions, inputs, safe logs | Minimal reproduction, focused test, type or schema check, build, dependency comparison | Focused regression passes, followed by the appropriate package or integration gate |
| Operations and tooling | Current status, config, runbook, dependency state, recent change, rollback path | Read-only health check, config diff, dry run, isolated restart when authorized | Intended state is observed; rollback or monitoring is recorded when a change was made |
| Research and analysis | Current authoritative sources, publication dates, raw data, calculation, contradictory evidence | Source comparison, recalculation, alternate query, assumption sensitivity check | Sources are traceable, calculations are reproducible, and uncertainty is stated |
| Writing and communication | Source brief, audience, desired action, factual claims, constraints, acceptance criteria | Critique before rewrite, source check, reader-path review, claim-boundary check | Revised artifact passes the stated criteria without invented facts |
| Business development and strategy | Authorized account or market sources, meeting notes, decision owner, offer, constraints, prior commitments | Verify account facts, compare explanations, test decision logic, draft a bounded next step | Facts and inferences are separated; recommendation names its inputs, owner, and authorized next action |

For BD work, never invent customer interest, pipeline status, pricing approval,
partner intent, or internal alignment. Drafting a message does not authorize
sending it.

## Critique And Improvement Loop

Use this loop for code, documents, analyses, plans, and messages:

1. Critique the artifact against explicit criteria.
2. Cite each concrete problem with a line, behavior, source, or missing check.
3. Rank the problems by consequence and choose the smallest useful fixes.
4. Revise after the critique is complete.
5. Rerun the relevant test and verification gate.
6. Repeat only when the new pass finds a substantive issue. Stop when another
   pass would be cosmetic or requires a human choice.

## Safety And Authority Boundary

- Stay inside the user's task, systems, data, and permissions.
- Do not disclose secrets, personal data, private customer information, or
  confidential company material beyond its authorized context.
- Do not send messages, contact prospects, change production, spend money,
  publish, merge, or make commitments unless the user authorized that action.
- Use authoritative sources for legal, financial, security, employment, and
  other high-stakes claims. Keep uncertainty visible.
- Never bypass approvals, access controls, safety checks, or company policy to
  keep the loop moving.

## Working Record

Maintain a concise record of observable evidence and decisions. Do not expose
hidden chain-of-thought or speculative internal reasoning.

```text
Diagnose, Test, Verify:
- Outcome and proof:
- Direct evidence:
- Attempts and shared assumption:
- Diagnosis:
- Test and stop condition:
- Result:
- Adjacent impact and verification:
- Decision or blocker:
```

Use the record in a handoff or after repeated failures. For ordinary responses,
lead with the outcome, the check that passed, and any remaining risk or next
action.

When complete, report the outcome, the verification that passed, and residual
risk. When blocked, report the verified facts, eliminated explanations,
smallest remaining uncertainty, exact input or authority required, and the safe
next action after the blocker clears.

## Verification Gate

Do not claim more than the completed check proves.

- Code needs the relevant test, build, or runtime check.
- Research needs traceable, current sources or an explicit inference label.
- Analysis needs reproducible inputs and calculations.
- Writing needs checked facts and stated acceptance criteria.
- BD work needs facts, inferences, decision owners, and authorized actions kept
  separate.
- Operational work needs the intended state observed, with rollback or
  monitoring named when required.

When full verification is unavailable, name the missing check and narrow the
claim. A precise handoff is valid when it preserves evidence and identifies the
smallest next decision.

## Example Calls

```text
Use diagnose-test-verify on this build failure. Two patches have failed.
Use diagnose-test-verify before calling this research memo verified.
Use diagnose-test-verify on this account brief and separate facts from assumptions.
```

## Examples

Software:

```text
Outcome and proof: restore the import and pass the affected package test.
Direct evidence: the stack trace shows the caller passed a null value.
Diagnosis: the parser assumption is weak; the caller boundary is unverified.
Test: reproduce with one fixture at the caller boundary.
Result: the fixture confirms the caller creates the null value.
Decision: fix the caller and add the fixture as a regression test.
Verification: focused regression and affected package tests pass.
```

BD:

```text
Outcome and proof: produce a source-backed account brief ready for internal review.
Fact: the meeting note records interest in a technical follow-up.
Inference: the account may be evaluating a pilot.
Unknown: budget, decision owner, and timing.
Test: inspect the authorized account record and draft clarification questions.
Result: the account record confirms the follow-up and contains no pilot stage.
Decision: state the follow-up as fact and keep pilot interest unknown.
Verification: the brief cites both sources and is ready for internal review.
Boundary: do not contact the account until sending is approved.
```

## Related Skills

- Use `pip-discipline` for ECDSA-specific public route coordination.
- Use `tony-rci-audit` for a dedicated critique-before-rewrite audit.

## Provenance

Adapted from the systematic diagnosis and completion-evidence method in the
English PIP edition of `tanweai/pua`:

- Source: `https://github.com/tanweai/pua`
- Audited commit: `f16769945d42bdb568fc956d53f2c9f347d66ae2`
- Audited source file: `codex/pua-en/SKILL.md`
- Audited SHA-256:
  `9ac522d2f80655853a4445a5ef0824ffdc139d737030494beb16ccbc1104f98a`

This task-scoped card keeps the diagnosis, alternative-hypothesis, bounded-test,
and verification method. It excludes performance threats, competitive pressure,
telemetry, feedback upload, remote prompt loading, and ECDSA-specific routing.
It does not grant new permissions or make the agent always-on.

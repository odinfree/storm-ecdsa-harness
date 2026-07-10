# Skill: Evidence-First Agent Recovery

Use when an AI agent is stuck, repeats the same approach, hands work back too
early, relies on an unverified assumption, or claims completion without proof.
This skill applies to software, operations, research, analysis, writing, and
business development work.

## Source And Scope

Adapted from the evidence and recovery method in the English PIP edition of
`tanweai/pua`:

- Source: `https://github.com/tanweai/pua`
- Audited commit: `f16769945d42bdb568fc956d53f2c9f347d66ae2`
- Audited source file: `codex/pua-en/SKILL.md`
- Audited SHA-256:
  `9ac522d2f80655853a4445a5ef0824ffdc139d737030494beb16ccbc1104f98a`

This version keeps the systematic recovery method and removes performance
threats, competitive pressure, telemetry, feedback upload, remote prompt
loading, and ECDSA-specific routing. It is a task-scoped prompt card. It does
not grant new permissions or make the agent always-on.

## Core Rule

Convert uncertainty into evidence before repeating work, escalating a claim,
or asking someone else to take over.

Investigation must stay proportional to the task. Exhaust relevant, safe,
in-scope checks. Stop when another check would add little information, require
new authority, or create an external commitment.

## Skill Selector

- Use this skill when work has stalled or a completion claim lacks evidence.
- Use `tony-rci-audit` when an artifact exists and the main job is to critique
  and improve it.
- Use `pip-discipline` for ECDSA-specific public route coordination.

When both recovery and artifact revision are needed, run this skill first to
establish the evidence and completion gate. Then use the critique loop on the
artifact.

## Trigger

Activate this skill when any of these are true:

- the same approach has failed twice,
- the agent is changing parameters or wording without changing the underlying
  idea,
- the agent blames tooling, data, another team, or the environment before
  checking,
- a handoff or request for user action arrives before available evidence has
  been inspected,
- a completion claim lacks a test, source, acceptance check, or observable
  result,
- the plan is broad but has no bounded next check,
- the user explicitly asks for evidence-first recovery or a systematic reset.

Do not activate for a routine first attempt, a known fix already in progress,
or a wait that depends on an external event. If the missing input is a business
decision, credential, approval, or other user-only information, inspect what is
available and ask for that input directly.

## Safety And Authority Boundary

- Stay inside the user's task, systems, data, and permissions.
- Do not disclose secrets, personal data, private customer information, or
  confidential company material beyond its authorized context.
- Do not send messages, contact prospects, change production, spend money,
  publish, merge, or make commitments unless the user authorized that action.
- Treat legal, financial, security, employment, and other high-stakes claims as
  source-sensitive. Use authoritative evidence and keep uncertainty visible.
- Never bypass an approval, access control, safety check, or organizational
  policy to keep the loop moving.

## Recovery Protocol

Use the fast path for a small stall: define the outcome, inspect the direct
evidence, run one bounded check, and verify the result. Use the full protocol
after repeated failures, when several assumptions may be wrong, or when a
handoff needs an auditable record.

1. **Define the outcome.** State the requested result and the evidence that
   would count as complete.
2. **Reconstruct the loop.** List the attempts already made, their results, and
   the assumption they shared.
3. **Read the primary evidence.** Inspect the actual error, source file, data,
   document, conversation, system state, or acceptance criteria. Do not rely on
   a summary when the original is available.
4. **Verify current conditions.** Check the relevant version, date, path,
   dependency, owner, input shape, permissions, constraints, and source
   freshness.
5. **Challenge the shared assumption.** Ask what would be true if the current
   explanation were wrong. Check the caller, upstream input, downstream
   consumer, alternative source, or opposite interpretation.
6. **Create materially different hypotheses.** When the cause remains unclear,
   produce at least two plausible explanations that require different checks.
   If direct evidence already supports one cause, test it instead of inventing
   alternatives. Do not submit several parameter variations as separate
   hypotheses.
7. **Choose the smallest informative check.** Prefer the check with the best
   information gain for its time, cost, and risk. Define its pass, fail, and
   stop conditions before running it.
8. **Execute within scope.** Run the safe check. Record the result as a verified
   fact, eliminated hypothesis, or remaining uncertainty.
9. **Close the loop.** Decide whether to proceed, revise, park, stop, or request
   a specific decision or permission. Do not repeat a killed approach without
   new evidence.
10. **Verify the outcome.** Run the completion check that fits the work. Report
    the evidence and any residual risk.

## Evidence Labels

Use these labels in the working record and handoff:

- **Verified fact:** observed directly or supported by a cited source or check.
- **Inference:** an interpretation supported by facts but not directly
  observed.
- **Hypothesis:** a testable explanation that still needs a check.
- **Unknown:** missing information with no justified conclusion yet.
- **Blocker:** a specific missing decision, access class, approval, or external
  event that prevents the next safe action.

Never promote an inference or hypothesis to a verified fact because it sounds
plausible. Every blocker must name what becomes possible once it clears.

## Work-Type Selector

Use the row that matches the task. Combine rows only when the work genuinely
crosses domains.

| Work type | Primary evidence | Useful bounded checks | Completion proof |
| --- | --- | --- | --- |
| Software and data | Full error, relevant source and call sites, tests, runtime versions, inputs, logs safe to inspect | Minimal reproduction, focused test, type or schema check, build, dependency comparison | Passing focused test plus the appropriate broader build or test gate |
| Operations and tooling | Current status, config, runbook, dependency state, recent change, rollback path | Read-only health check, config diff, dry run, isolated restart when authorized | Intended state observed; rollback or monitoring recorded when a change was made |
| Research and analysis | Best available authoritative sources, publication dates, raw data, calculation, contradictory evidence | Source comparison, recalculation, alternate query, assumption sensitivity check | Traceable sources, reproducible calculation, and uncertainty stated |
| Writing and communication | Source brief, audience, desired action, factual claims, constraints, acceptance criteria | Critique before rewrite, source check, reader-path review, claim-boundary check | Revised artifact passes the stated criteria without invented facts |
| Business development and strategy | Account or market source, meeting notes, decision owner, offer, constraints, prior commitments | Verify the account fact, compare explanations, draft a bounded next step, test the decision logic | Recommendation or artifact cites its inputs, separates fact from inference, and names the owner or next decision |

For BD work, never invent customer interest, pipeline status, pricing approval,
partner intent, or internal alignment. Drafting an outreach message does not
authorize sending it.

## Example Calls

```text
Use evidence-first-recovery on this build failure. We have tried two patches.
Use evidence-first-recovery before calling this research memo verified.
Use evidence-first-recovery on this account brief and separate facts from BD assumptions.
```

## Compact Examples

Software recovery:

```text
Outcome: restore the failing import and pass the focused test.
Shared assumption: the parser is dropping the field.
Verified fact: the stack trace shows the caller passed a null value.
Next bounded check: reproduce with one fixture at the caller boundary.
Completion proof: focused regression test and the affected package test pass.
```

BD recovery:

```text
Outcome: produce a shareable account brief.
Verified fact: the meeting note records interest in a technical follow-up.
Inference: the account may be evaluating a pilot.
Unknown: budget, decision owner, and timing.
Next bounded check: inspect the authorized account record and draft clarification questions.
Authority boundary: do not contact the account until sending is approved.
```

## Critique And Improvement Loop

Use this sub-loop when the output is an artifact such as code, a document, an
analysis, a plan, or a message:

1. Critique the current artifact against explicit criteria. Identify concrete
   issues and cite the relevant line, behavior, source, or missing check.
2. Rank issues by consequence. Fix the smallest set that can change the
   outcome.
3. Revise only after the critique is complete.
4. Rerun the relevant evidence and completion checks.
5. Repeat only if the new pass finds a substantive issue. Stop when another
   loop would be cosmetic or requires a human choice.

## Working Record

Maintain a concise evidence ledger while investigating. Record observable
facts, sources, checks, results, uncertainties, and decisions. Do not expose
hidden chain-of-thought or speculative internal reasoning. Surface the ledger
when coordinating across people or agents, after several failed attempts, or
when a handoff is needed.

```text
Evidence-first recovery:
- Outcome and completion proof:
- Attempts and results:
- Shared assumption:
- Primary evidence inspected:
- Verified facts:
- Inferences:
- Open uncertainties:
- Alternative hypotheses:
- Next bounded check:
- Pass, fail, and stop conditions:
- Permission or safety boundary:
```

## Response Contract

Lead with the result, current evidence, and next action. Keep process detail
brief unless the user asks for it or needs it to review a decision.

If the task is complete, report:

- the outcome,
- the check that passed,
- any remaining risk or follow-up.

If the task is blocked, report:

- verified facts,
- eliminated explanations,
- the smallest remaining uncertainty,
- the exact decision, access class, approval, user input, or external event
  required, without asking the user to paste a secret into an unsafe channel,
- the safest next action once the blocker clears.

## Completion Gate

Do not claim more than the completed check proves.

- Code is not fixed until the relevant test, build, or runtime check passes.
- Research is not verified until the claim is traceable to current,
  authoritative evidence or clearly labeled as inference.
- Analysis is not complete until the calculation or reasoning can be
  reproduced from its inputs.
- Writing is not ready until factual claims and acceptance criteria have been
  checked.
- BD work is not ready until facts, inferences, decision owners, and authorized
  next actions are separated.
- Operational work is not complete until the intended state is observed and
  any required rollback or monitoring step is named.

When full verification is impossible, state the missing check and narrow the
claim. A precise handoff is a valid outcome when it preserves evidence and
identifies the smallest next decision.

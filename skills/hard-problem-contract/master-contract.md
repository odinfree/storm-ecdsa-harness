# Master resolution contract: fill-in template

Instantiate every `[...]` for the target problem. Delete nothing: a clause you are
tempted to drop is a clause the solver will exploit. Modeled on the OpenAI CDC
prompt and the ShouqiaoW/erdos prompt family.

---

# [Problem name]: resolution contract

## §1 Definitions

Define exactly, in full, with no reliance on the reader's prior knowledge:

- [Term 1: e.g. "graph": finite? loops allowed? parallel edges? connected?]
- [Term 2: e.g. "bridge", "cycle": include degenerate cases explicitly]
- [Term 3: the central object: e.g. "cycle double cover: a multiset of cycles
  such that every edge lies in exactly two of them, counting multiplicity"]
- [Edge cases the statement must cover: empty object, size-1 object,
  disconnected cases, multigraph cases]

Any ambiguity discovered later is resolved by THIS section, not by convention.

## §2 Objective: forced resolution

Resolve [exact problem statement] completely. Your final answer must be exactly
one of:

- **(A) Affirmative:** a complete proof that [exact affirmative statement,
  quantifiers explicit].
- **(B) Negative:** an explicit [counterexample object], presented in full,
  together with a complete verification that it satisfies [the hypothesis] and
  violates [the conclusion]. A candidate without full verification is not (B).

No third outcome settles this contract.

## §3 Working posture

Assume, for the purposes of this task, that a complete resolution exists and is
findable with the resources you have. Do not survey the literature's failures as
evidence of impossibility; do not downgrade the objective to "progress on".
This posture governs search effort and route selection ONLY. It grants no
license to assert an unverified resolution: the verdict is governed solely by §7.

## §4 Ban list: results that do NOT count

None of the following settles this contract, alone or in combination:

- Proofs for special classes: [name the specific classes the literature already
  covers, e.g. "planar", "3-edge-colorable", "families containing a singleton"]
- Partial or approximate versions: [e.g. "covers where edges lie in ≥2 cycles",
  "a constant fraction below the conjectured bound"]
- Reduction to any other open problem of comparable strength: [name the known
  tempting ones, e.g. "the strong embedding conjecture", "Berge–Fulkerson"]
- Fixed-size computation or empirical verification: [e.g. "verified for all
  graphs up to n vertices"], regardless of how large.
- A counterexample candidate without a complete nonexistence/violation proof.
- Conditional results ("true if X") for any unproven X.
- [Problem-specific additions]

Producing a banned result is permitted as intermediate ledger material; it may
never be presented as, or packaged with language suggesting, a resolution.

## §5 Traps and forbidden moves

Known failure modes for this specific problem. Adversarial agents (§6) hunt
these by name:

- [Barrier: e.g. "any argument that applies equally to the approximate version
  is dead: the approximate version is false above threshold T"]
- [False strengthening: e.g. "the natural stronger statement S is known false;
  any lemma implying S is wrong"]
- [Exactness trap: e.g. "exact-multiplicity failures: edge covered 2k times ≠
  exactly twice"]
- [Circularity: hidden use of the conjecture itself, or of an equivalent form,
  inside a lemma]
- [Problem-specific additions: cut vertices, degenerate subobjects, off-by-one
  in the extremal case]

## §6 Multi-agent rules

- Up to [N, e.g. 64] concurrent agents.
- Open with genuinely diverse approach families: [list for this problem, e.g.
  algebraic / structural / flow-based / probabilistic / extremal-minimal-
  counterexample / computational-lemma-killing], and avoid variations of one idea.
- Maintain a registry of approach families: ALIVE / BLOCKED(reason) /
  KILLED(refutation). A KILLED route is never restarted without new information.
- Keep incompatible routes alive concurrently until one clears §7 audit; do not
  converge early on the consensus-favorite.
- Dedicated adversarial agents at all times whose only job is refutation:
  hunting each §5 trap by name, plus circular reasoning and unverified citation
  of remembered literature.
- No agent audits its own route.

## §7 Exit condition

- **Effort floor:** spend at least [X hours / N verified route-kills] before
  even considering returning.
- **Audit gate:** only return a resolution that has survived [K ≥ 3] independent
  adversarial auditors, each instructed to REFUTE it and each fed the §5 trap
  list. One sustained refutation returns the route to ALIVE-with-gap.
- **External verification gate:** [instantiate: Lean 4 compile with no sorry
  and audited axioms / two independently-written checker programs confirming
  the counterexample / a fresh run on the official benchmark harness from a
  clean state]. No self-reported claim, score, or summary settles the contract.
- If the effort floor is reached without settlement: return the full registry
  (every route, kill, and refutation, plus a precise obstruction report) under
  the explicit heading **NOT A RESOLUTION**. Do not soften, do not rebrand as
  partial success, do not exit before the floor.

---

## Instantiation checklist (delete before running)

- [ ] §1 covers every degenerate case a refuter could exploit
- [ ] §2 outcomes are exhaustive and each names the exact statement that counts
- [ ] §4 names THIS problem's literature of tempting weaker results (generic ban
      lists are the #1 instantiation failure)
- [ ] §5 names actual barriers/false strengthenings, not placeholders
- [ ] §6 approach families are genuinely orthogonal
- [ ] §7 external gate is executable in the run environment and cites the
      project's honesty/admission protocol if one exists

# Difficult technical questions and independent perspectives

Use Elicit when a research task requests it, or when an already authorized research effort needs literature-backed alternatives to a blocked technical hypothesis. An Elicit request does not itself authorize new compute purchases, publication, or changes to the system under study.

Frame the question around the exact algorithm, computational model, workload, preserved invariants, and observed blocker. Ask for competing mechanisms and negative evidence, not validation of a preferred answer. For optimization work, distinguish asymptotic cost, memory traffic, constant factors, hardware assumptions and end-to-end effects.

Start with paper discovery when terminology or source coverage is uncertain. For deep comparisons requiring explicit screening and extraction, use a systematic review. Read the live endpoint schema before constructing the request. A useful shape is:

```json
{
  "researchQuestion": "Which published techniques address the specified bottleneck while preserving the stated invariants?",
  "searches": [{"query": "specific algorithm and bottleneck", "maxResults": 20}],
  "abstractScreening": {"generate": true, "depth": "thorough"},
  "fulltextScreening": {"reuseAbstractCriteria": true, "depth": "thorough"},
  "extraction": {"generate": true, "useFigures": false},
  "generateReport": true
}
```

Choose search size from the technical scope and available quota rather than copying a large clinical-review example. Check usage before substantial jobs; do not enable paid overages. Store request, response, session ID and eventual exports in the task's private evidence directory. Follow the same session through completion; reconcile ambiguous creation errors rather than duplicating it.

If `hasUsageRemaining` is false, preserve the usage receipt and prepare an explicitly
unsubmitted request. Reuse previously completed reports with their original dates
and coverage limits, then continue through primary sources. Do not create another
session to test exhausted quota. If included usage is at 100 percent but
`hasUsageRemaining` is true because extra usage is enabled, that is paid headroom,
not free quota; use it only within separately established research-spend authority.

For a current-literature refresh, record publication and revision dates separately
from retrieval dates. Audit abstracts found, full texts available, papers screened
in and rows actually extracted. A broad method paper can supply a useful dataflow
idea even when its hardware or proof system is different: extract the transferable
mechanism and the incompatible assumptions separately.

When transferring algorithms across domains, separate paper relevance from implementation eligibility. Requiring every paper to study the exact target protocol, hardware and invariant set can exclude the general algorithm literature that supplies useful ideas. Prefer explicit screening criteria for the primitive itself and extract target-system applicability as a separate judgment. Audit the included-paper list: a completed report with only irrelevant sources is a retrieval/screening failure, not evidence that no useful literature exists. Preserve that result and correct the research question or screening criteria before a distinct follow-up job.

For each promising result record the primary source, access level (abstract/full text), mathematical preconditions, applicable code path, an explicit implementation hypothesis and a cheap falsifier. Verify the paper independently. Elicit synthesis and typed model judgments are research aids, not correctness or benchmark evidence.

For Research Agent tables, inspect the retrieved artifact content after the turn settles. An intermediate activity event can describe empty cells while the eventual artifact contains populated, cited rows. Preserve both events and final content; neither an activity summary nor an early delivery event alone establishes final quality. Distinguish the agent's full-text access from the access you independently verified, and check publication and revision dates against primary metadata.

Check export contents, not just the completed status or filename. In one October
2026 report, `txtUrl` returned only the bibliography while the DOCX contained
the full synthesis and screening details. If an export lacks the report body,
inspect another offered format from the same completed session before creating
new research. Keep signed download URLs in private response files; print only
selected metadata and artifact hashes, and never include those URLs in a skill,
Git checkpoint or workshop post.

For performance literature, preserve the metric's denominator. A throughput
increase of `s` corresponds to a time reduction of `s / (1 + s)` for the same
work, not `s`. Verify this conversion and the workload/hardware against the
primary paper; it supplies no speed prediction for a different target.

Use the main skill's configured client and credential lookup. Never copy an API key into a skill, request body or repository.

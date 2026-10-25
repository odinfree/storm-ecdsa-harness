---
seed:
max_depth: 3
max_breadth: 3
notes_per_run: 1
continuous: false
digest: Findings.md
status: active
tags:
  - research-loop/config
---

# 🔧 Research Loop — Config

> [!note] How this works
> Each research cycle reads this file, takes the next topic from
> [[Queue]], researches it using the **Research method** below, writes a note in
> `Research/`, and appends follow-up questions back to [[Queue]] — so the loop
> feeds itself. The caps below stop it from sprawling forever.

## Settings — edit the frontmatter above

- **seed** — the starting question/topic, quoted (`seed: "..."`). Set this before the first
  run (or pass it inline: `research-loop cycle <loop-name> your topic here`).
- **max_depth** — how many generations of follow-ups to chase (`0` = seed only).
- **max_breadth** — max follow-up questions generated per note.
- **notes_per_run** — questions researched per cycle, each by a parallel subagent.
- **continuous** — `false` (default): **bounded** — stop when the queue drains (good for a
  one-off / finite run). `true`: **never stop** — generate fresh directions toward the
  goal (drive with `/loop`; stop via `paused`).
- **digest** — filename of the rolling summary the loop maintains each cycle (the one note
  you read to follow progress). Rename per domain (e.g. `Movements.md`, `Levers.md`); how
  to structure its contents is up to this loop's Research method.
- **status** — `active` or `paused`. Set `paused` to stop the loop cleanly.

## Research method

Find 4-8 reputable, recent sources with WebSearch (prefer primary sources), extract clean
text with `defuddle parse <url> --md` (kepano's defuddle CLI), then synthesize. Cite every
source.

## Method examples (not part of the method)

Replace the **Research method** section above with your own; it does not have to be web
search. Available tools are listed in the research-loop skill. Examples:

- "Papers only: use the elicit-research skill (`/search/papers`), then read the best hits."
- "Read and analyze the files under `<path to a knowledge repo>`; no web."
- "Reason from first principles only, no external sources."
- "Run `scan.py` in this folder each cycle and analyze what changed."

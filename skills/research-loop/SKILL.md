---
name: research-loop
description: "Run a self-expanding research loop. Each cycle sends parallel researcher agents after open questions, each writes one linked Markdown note, and their follow-up questions refill the queue. Use to start a loop on a seed question, run a cycle, run a tool-assisted monitor cycle, or report loop status. Adapted from BitWonka's loop-engine (MIT)."
license: MIT (adapted from BitWonka/loop-engine; see LICENSE)
---

# Research loop

Usage: `research-loop <new|cycle|run|status> [loop-name] [seed...]` (Claude Code:
`/research-loop ...`; Codex: `$research-loop ...`). With no op, run `status`.

Converted from BitWonka's [loop-engine](https://github.com/BitWonka/loop-engine) commands
(`/research-new`, `/research-cycle`, `/run-loop`, `/research-status`, commit 8c133a7, MIT;
see `LICENSE`) and adapted to a local setup with Claude Code and Codex.

## Where loops live

A **loop** is one folder, and optionally its own Obsidian vault:

- A loop that serves a campaign lives in that campaign's knowledge repo, at
  `<repo>/loops/<loop-name>`, so its notes are committed with the lane's journal.
- Any other loop lives under `LOOPS="${RESEARCH_LOOPS_ROOT:-$HOME/research-loops}"`.

```
<loop>/
├── Engine/Config.md   # seed, caps, status (frontmatter); the Research method section
├── Engine/Queue.md    # `- [ ] [d=N] question (parent:: [[Note]])` items
├── Engine/Log.md      # one table row per researched topic
├── Engine/Map.md      # `- [[Title]] · d<n> · <date>` index of notes
├── Findings.md        # the digest: the one file a human reads
└── Research/          # one note per researched question
```

Below, `<loop>` is that folder: for a loop name, `<repo>/loops/<name>` in the campaign repo you
are working in when it exists, else `$LOOPS/<name>`. `<scratch>` is
`${TMPDIR:-/tmp}/research-loop/<loop-name>` (create it with `mkdir -p`; it is disposable), the
only place for downloads and other working files. Take timestamps from
`date "+%Y-%m-%d %H:%M"` (set `TZ` once per machine); dates are `+%Y-%m-%d`. Obsidian
is optional; read and write the files directly. Each loop gets its own vault, so a personal
vault stays untouched.

## Research methods available here

The **Research method** section of `Engine/Config.md` names one method; follow it, with any
instructions the user gives for this run taking precedence. These are the tools a
method can use:

| Method | Tool |
|---|---|
| Web pages | Find pages with web search (Claude Code: `WebSearch`, loaded via ToolSearch `select:WebSearch` when deferred; Codex: its built-in search). Read them with `defuddle parse <url> --md` (kepano's [defuddle](https://github.com/kepano/defuddle) CLI, MIT). Use WebFetch or `curl -sL` for `.md`, raw, JSON and PDF URLs, and the built-in browser for signed-in pages |
| GitHub repos | `gh api repos/<owner>/<repo>/contents/<path>` or a shallow clone into `<scratch>`; `gh` is authenticated, the anonymous API is rate-limited |
| Papers | the `elicit-research` skill: `python3 <elicit-research>/scripts/elicit.py POST /search/papers --body req.json --out resp.json`. It reads `~/.config/elicit/api-key`. Check `GET /usage` before a large job |
| Local code or a knowledge repo | read-only reads of the named folder; `git log`/`git show` for history |
| First principles | reason with no external sources, then self-question to deepen |
| Typed triage | the jev-second-perspective skill (TypeSafe Jev) to rank a long queue or citation-check the digest against the notes |

Keys stay where they already live (`~/.config/<service>/`, mode 600) or in the loop's own
`.env` inside the loop folder. Notes, logs, digests and reports carry no keys or tokens.

## `new`: scaffold a loop

1. Pick `<loop>` per "Where loops live". If it exists, say so, point at `cycle`, and stop.
   With no name, ask for one (kebab-case; it is also the vault name).
2. Copy the template from this skill's base directory:
   `mkdir -p "$(dirname "<loop>")" && cp -R "<skill-dir>/assets/template" "<loop>"`.
3. When a seed was given, set it in `Engine/Config.md` frontmatter as a double-quoted
   string (escape `"` and `\`) and add it to `Engine/Queue.md` under `## Queue` as
   `- [ ] [d=0] <seed> (parent:: seed)`.
4. When the user described how to research, replace the body of the **Research method**
   section with their description; otherwise keep the default web method.
5. Only when the user wants Obsidian: `open -a Obsidian "<loop>"`.
6. Report the path, seed and method, and how to run it: one cycle with `research-loop
   cycle <loop-name>`; continuously with `/loop /research-loop cycle <loop-name>` in
   Claude Code. Codex has no `/loop`: each invocation runs one cycle.

## `cycle`: one queue-expanding cycle

Do exactly one cycle, then stop; under `/loop` it is re-invoked.

1. **Load config.** Read `Engine/Config.md`: `seed`, `notes_per_run` (default 1),
   `max_depth` (default 3), `max_breadth` (default 3), `continuous` (default false), `digest` (default
   `Findings.md`), `status`, and the **Research method** section (the section only; the
   "Method examples" section after it is editing help). `status: paused` → print
   `⏸ paused` and stop. A seed passed in the arguments replaces the configured one: write
   it to the frontmatter and queue it as in `new` step 3.
2. **Build the worklist** of up to `notes_per_run` items, taken top-down from the lines
   under `## Queue` in `Engine/Queue.md` that start with `- [ ]`:
   - Mark pending items deeper than `max_depth` as skipped: `- [-]`.
   - When the queue holds no items at all, add the seed as `- [ ] [d=0] <seed> (parent:: seed)`.
     The first cycle therefore researches the seed alone; later cycles fill up from its
     follow-ups.
   - Still short, with `continuous: true`: skim `Map.md` and the notes, then add fresh
     `[d=0]` directions toward the seed that existing notes do not cover.
   - Still empty, with `continuous: false`: print
     `✅ research complete: queue drained; stop the /loop` and stop.
   Done when the worklist holds the items this cycle will research.
3. **Fan out**, one researcher per worklist item. In Claude Code, launch them in a single
   message as `general-purpose` Agent subagents (so they can Write). In Codex, or anywhere
   without a subagent tool, research the items yourself one after another. Each researcher
   gets the loop path, the Research method, its one question with its depth, the other
   worklist questions of this cycle (to avoid overlapping them), and these instructions:
   - When a note in `Research/` already covers the question well, write nothing and return
     `skipped: [[<that note>]]`.
   - Research it per the method and cite every source. A method with no external sources
     writes `1. none (first principles)` under Sources. Downloads and working files go to
     `<scratch>` only, and notes never link into it.
   - Write exactly one note, `<loop>/Research/<title>.md`, in the shape below. Choose a
     title without `? : / \ # | [ ] ^`, so the file name, the `title:` line and every
     `[[link]]` are identical. If the Write tool refuses the file, write it with a shell
     heredoc. Touch no other file in the loop and no external repository.
   - Return the note title and at most `max_breadth` follow-up questions.

   ```markdown
   ---
   title: "<clear, specific title; equals the file name>"
   created: <TZ=Europe/Zurich date "+%Y-%m-%d %H:%M">
   tags: [research, depth/<n>]
   depth: <n>
   parent: "<[[Parent Note]], or seed for a d=0 question>"
   status: complete
   ---
   # <title>
   > [!summary] TL;DR
   > 2-4 sentences.
   ## Key findings
   - ...with inline source refs; mark each as measured, cited or inferred
   ## Details
   ## Open questions
   - <the follow-ups it raises>
   ## Sources
   1. [title](url or DOI): note (abstract-only or full text)
   ## Related
   - [[Parent Note]] / siblings
   ```
4. **Collect and refill**, as the orchestrator, serially (you alone write the Engine files
   and the digest, so researchers never race on them). For every returned result:
   - a skip: mark its item `- [-]` and move on;
   - mark its item `[x]` in `Queue.md`;
   - append its follow-ups as `- [ ] [d=<depth+1>] <question> (parent:: [[<title>]])` when
     `depth+1` ≤ `max_depth`, deduplicated against existing notes and queue items; deeper
     follow-ups go to the digest's Open questions instead;
   - append `- [[<title>]] · d<depth> · <date>` to `Map.md`;
   - append `| <n> | <timestamp now> | <depth> | <question, with | replaced by /> | [[<title>]] | <k> queued |`
     to `Log.md`, numbering rows from 1.
   Done when every written note appears in `Map.md` and `Log.md`.
5. **Rewrite the digest** (`digest`, default `Findings.md`, shipped in the template): a
   ranked, deduplicated living summary that folds in this cycle's notes, drops stale items
   and links the `[[notes]]`. Follow the digest structure the Research method names;
   otherwise a ranked "Key findings" list plus "Open questions". Skimmable in about 30
   seconds. When the top finding is about to drive a decision (kill a route, spend money,
   submit), have Claude Fable try to refute it first (Claude Code: an Agent call with
   `model: fable`; Codex: the send-to-claude-fable skill) and record the verdict in the
   digest.
6. **Report** in 3-5 lines: the loop, notes written this cycle, follow-ups queued, total
   notes, and whether it continues on the next tick or is complete.

When a cycle runs inside a subagent, Claude Code's Write tool can refuse loop files as
"report files"; update them with Edit, or write them with a shell heredoc. They are loop
state, not reports.

## `run`: one tool-assisted cycle

For loops whose Research method names a private data tool kept in the loop folder (for
example `<loop>/scan.py`: a leaderboard fetch and diff, an API poll). The tool supplies cheap
raw data; the analysis is yours.

1. Read `Engine/Config.md`; `status: paused` → print `⏸ paused` and stop.
2. Follow the Research method literally. Typically run the helper from the loop folder with
   its own env, so only its compact digest enters your context:
   `(cd "<loop>" || exit 1; set -a; if [ -f .env ]; then . ./.env; fi; set +a; python3 scan.py)`.
3. Find the signal (the largest changes, anything new; ignore noise), research the items no
   note in `Research/` covers yet, and write analytical notes with `[[wikilinks]]` plus any
   thesis or index file the method names. Interpret the data; a pasted digest is not a note.
4. Append a heartbeat row to `Engine/Log.md`.
5. Report in 3-5 lines: the key moves, what you researched and concluded, the notes written.

Keep it running with `/loop 15m /research-loop run <loop-name>` in Claude Code.

## `status`: overview of all loops

Read from disk. Loops are the folders under `$LOOPS` plus any `loops/*` folder in the
campaign repo you are working in. For each loop read `Config.md` frontmatter; count the lines
under `## Queue` in `Queue.md` that start with `- [ ]` (pending), `- [x]` (done) and `- [-]`
(skipped); count the `.md` notes in `Research/`; take the deepest `depth:` among them; and
take the When of the last `Log.md` row.

- No loop name: one table
  `| Loop | Status | Notes | Pending | Done | Skipped | Deepest/max | Last activity | Seed |`,
  with Deepest `-` when there are no notes and the seed without its quotes.
- With a loop name: its seed, the caps (`max_depth`, `max_breadth`, `notes_per_run`,
  `continuous`), a method summary, the pending items with depths, and the last few log rows.
- No loops: say so and suggest `research-loop new <name> <seed>`.

## Running loops

A loop occupies the session it runs in. Run each one in a background agent or its own
session so the main session stays responsive; loops are independent, so several can run at
once. Pause one with `status: paused` in its `Config.md`, or by stopping its `/loop`.

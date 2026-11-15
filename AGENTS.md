# Agent instructions for this repository

This repository is the public home of the Storm skill collection: agent skills for long optimization campaigns on open benchmarks (ecdsa.fail quantum circuits, the Proximity Prize at better.codes, Kaggle packing contests). Each skill is a folder under `skills/` with a `SKILL.md`; a few single-file skills live directly at `skills/*.md`. Campaign tools live under `tools/`, one folder each.

## Conventions

- Skill format: YAML frontmatter (`name`, `description`, `whenToUse`) plus a Markdown body. Prefer the directory form (`skills/<name>/SKILL.md`); supporting files live beside the SKILL.md.
- Attribution: when a skill builds on someone's public work, its README table row and `CREDITS.md` entry must name the source and licence. Never remove an attribution line.
- Tool format: `tools/<name>/` with a `README.md` giving the Swiss name, the technical id, what the tool does, inputs and outputs, how to run it, and its limits. Paths, accounts and hosts come from arguments or environment variables, never from the file. Bundle no third-party code; point to upstream.
- Names: every skill, tool, script and note has a Swiss German name beside its technical id, recorded once in `NAMES.md`. A skill's folder name and frontmatter `name` stay the technical id; the Swiss name goes in the SKILL.md title as `<Swiss name> (<id>)`. Tool folders use the ASCII spelling of the Swiss name. Names are funny, never a slur, never sexual, never aimed at a person or a team; a skill built on a person's work is named after its mechanism.
- `install.sh` symlinks every skill into `~/.claude/skills`, `~/.codex/skills`, and `~/.agents/skills` when present. It must stay idempotent and never replace an existing skill.
- Skills are prompt configuration that agents execute. Treat pull requests like code: review the instructions a skill adds, not just its prose.

## Working rules for agents

- Match the existing style: imperative, compact, no marketing language.
- Keep each frontmatter `description` accurate — that line is what makes agents load the skill.
- Benchmark or score claims in any skill or note must name the evaluator and the date.
- Run `scripts/redaction-check.sh` and `python3 scripts/names-check.py` before committing; both must pass. Never commit secrets, session logs, wire files, absolute home paths, or private hostnames.

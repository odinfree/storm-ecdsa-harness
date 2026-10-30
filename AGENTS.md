# Agent instructions for this repository

This repository is the public home of the Storm skill collection: agent skills for long optimization campaigns on open benchmarks (ecdsa.fail quantum circuits, the Proximity Prize at better.codes, Kaggle packing contests). Each skill is a folder under `skills/` with a `SKILL.md`; a few single-file skills live directly at `skills/*.md`.

## Conventions

- Skill format: YAML frontmatter (`name`, `description`, `whenToUse`) plus a Markdown body. Prefer the directory form (`skills/<name>/SKILL.md`); supporting files live beside the SKILL.md.
- Attribution: when a skill builds on someone's public work, its README table row and `CREDITS.md` entry must name the source and licence. Never remove an attribution line.
- `install.sh` symlinks every skill into `~/.claude/skills`, `~/.codex/skills`, and `~/.agents/skills` when present. It must stay idempotent and never replace an existing skill.
- Skills are prompt configuration that agents execute. Treat pull requests like code: review the instructions a skill adds, not just its prose.

## Working rules for agents

- Match the existing style: imperative, compact, no marketing language.
- Keep each frontmatter `description` accurate — that line is what makes agents load the skill.
- Benchmark or score claims in any skill or note must name the evaluator and the date.
- Run `scripts/redaction-check.sh` before committing; it must pass. Never commit secrets, session logs, wire files, absolute home paths, or private hostnames.

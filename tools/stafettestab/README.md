# Stafettestab (relay baton)

Technical ids: `codex.sh`, `kimi.sh`, `groq.py`, `preamble-*.md`.

A small bridge that lets one orchestrating agent hand a prompt file to another vendor's model and get the
answer back as a file. Each worker takes a role (advisor, auditor, builder, reviewer), prepends that role's
preamble to the prompt, runs the model headless, and writes the final message to the output file.

| file | runs | needs |
|---|---|---|
| `codex.sh` | OpenAI Codex CLI, read-only sandbox unless the role is builder | `codex` signed in; `CODEX_BIN`, `CODEX_MODEL`, `CODEX_EFFORT` |
| `kimi.sh` | Kimi Code CLI | `kimi` signed in; `KIMI_MODEL` |
| `groq.py` | any chat model on Groq's OpenAI-compatible API | the Groq key in the process environment, injected by your secret manager |

```bash
bash codex.sh auditor prompts/audit-hold-pass.md out/audit-hold-pass.md /path/to/checkout
bash kimi.sh advisor prompts/next-lever.md out/next-lever.md
```

Output: the answer in `<out-file>`; `codex.sh` also writes a JSON-lines event log beside it and prints one
status line (`codex[role,model,effort,sandbox] rc=0 412s -> out.md`).

## Roles

The four preambles are the contract. The auditor must verify before asserting, quote file and line, and end
with "what I could not verify" and "top 3 fixes". The builder may edit only `src/point_add/` and reports
hypothesis, change, result, next. The reviewer ends with MERGE, FIX FIRST or REJECT. Edit them for your
project; the builder's file list is ecdsa.fail's.

## Limits

These are October 2026 scripts. Model names and CLI flags change; check `codex exec --help` and
`kimi --help` before relying on them. No key is stored or printed by any of them. A second model's answer is
a review. Measure before you act on it (see the `cross-model-review-gate` skill).

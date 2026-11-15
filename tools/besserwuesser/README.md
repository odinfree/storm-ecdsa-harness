# Besserwüsser (know-it-all)

Technical id: `carbon-advisor`.

Asks a model from another vendor for a second opinion, from the terminal. One bounded, self-contained request
goes in, one verdict comes out. It calls Google's Antigravity CLI (`agy`) in print mode with Gemini 4 Carbon,
or with Gemini 4 Argon when `--argon` is given.

We use it for the review that a model from the author's own vendor cannot give: before a row is submitted,
before a route is declared dead, when many hours of work rest on one assumption. Frame the request as an
attack ("refute this or tell me what I missed"), make it self-contained with absolute paths, and ask for
file:line citations and a list of what the reviewer could not determine.

## Run

```bash
carbon-advisor 'Refute: the hold pass is exact when ... Read /abs/path/holdx.rs. Cite file:line.'
carbon-advisor --argon --effort high --timeout 1200s < packet.txt
```

Options: `--effort low|medium|high`, `--argon`, `--model <id from agy models>`, `--output-format text|json`,
`--timeout`. Output: the model's answer on stdout.

## Limits

- It needs `agy` installed and signed in by a person. No key is read or passed.
- The prompt asks for read-only and nothing enforces it. Run it from a directory where an unwanted edit would be visible in
  `git status`.
- What we measured in November 2026: Argon was the better reader of code (audits, censuses, itemisation);
  Carbon was better at attacking one specific claim. Check a sample of any model's counts yourself.
- The receipt format for such reviews is in the `cross-model-review-gate` skill.

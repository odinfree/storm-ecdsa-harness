# Notizbüechli (little notebook)

Technical id: `zmknote.py`, generalized as `notizbuechli.py`.

Writes one row's submission package: the public note, the dependency list, the `CLAIM` file and the verified
hash. Every number in the note comes from a values file that a script fills from result files, and the tool
refuses to write a note with a hole in it.

We needed it for a ladder of up to seventeen rows that differed in one constant. Every note written by hand
is a chance to quote a neighbouring row's hash.

## What it refuses

A missing value; a `{{PLACEHOLDER}}` left in the text; a local path; an inherited notice-block marker; a
`TODO`; a note under 5 KiB; a commit or ops hash that is not in the note text; more than 20 dependencies; a
dependency without rationale or evidence; a verified sha (from an independent rebuild) that differs from the
one in the values; and, with `--board`, a snapshot older than half an hour or a Toffoli count that is not
strictly below the lowest count on the board at that width or narrower.

## Run

```bash
python3 notizbuechli.py --pkg ladder/w757 --width 757 --template NOTE.tmpl --values res/K17/values.json \
        --deps deps.json --verified-sha res/K17/B/ops.sha256 --board work/board-latest.tsv --evidence res/K17 --ready
python3 notizbuechli.py --pkg ladder/w757 --width 757 --template NOTE.tmpl --values res/K17/values.json \
        --deps deps.json --verified-sha res/K17/B/ops.sha256 --board work/board-latest.tsv --check
```

Output: `NOTE-<W>.md`, `deps-<W>.json`, `CLAIM`, `verified-sha`, `MODEL`, `evidence/`, and with `--ready` a
`READY` file. `--check` regenerates everything and compares it byte for byte with the package, so a note
edited by hand after generation is caught before Briefchaschte binds it.

`NOTE.example.tmpl` shows the placeholder style. It is a skeleton. Write the failure-rate and
credit sections in your own words for your own lineage.

## Limits

The tool checks form. It cannot know that `values.json` was read from the right run; bind that
with hashes (the note must contain the ops sha256 that the verifier reproduced). The campaign version also
cross-checked stage results against each other (the retargeted candidate's hash against the rebuilt row's,
the evaluator's qubit count against the width); keep such checks in the script that writes `values.json`.

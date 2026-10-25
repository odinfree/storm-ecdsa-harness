# Receipt and review contract

## Required source binding

The capture receipt must bind:

- the repository path, resolved predecessor and accepted commit;
- the two commit trees and their authored metadata;
- the editable submission directory;
- score, exact rational radius, and `Solution.lean` proof root at both commits;
- proof-root blobs, direct imports, changed files, and Git numstat;
- the score-history adjacency check;
- the exact public-note bytes when a note is available.

The receipt is contaminated incumbent archaeology. Keep `classification` unchanged.

## Review fields

The helper emits an unfilled `transfer_review`. Complete it only after reading the changed source:

- `claimed_mechanism`: one falsifiable sentence;
- `supporting_anchors`: changed file and line or hunk anchors;
- `inherited_dependencies`: unchanged providers on which the gain depends;
- `accompanying_churn`: edits not required by the claimed lever;
- `falsifier`: an executable comparison on both accepted states;
- `transfer_verdict`: `TRANSFERABLE`, `SOURCE-BOUND`, `FALSIFIED`, or `UNRESOLVED`;
- `target_tree_rebase`: the exact destination commit, or `NOT_ATTEMPTED`.

## Fail-closed cases

Stop and repair the source record when:

- the live accepted commit differs from the newer commit;
- the accepted predecessor is inferred only from commit time or subject text;
- another score-changing commit is present between the selected refs;
- the benchmark contract changes between the pair;
- the note describes a different submission or cannot be byte-bound;
- the claimed lever is absent from the changed proof dependency path.

An endpoint diff across several promotions answers a different question. Capture every adjacent pair separately.


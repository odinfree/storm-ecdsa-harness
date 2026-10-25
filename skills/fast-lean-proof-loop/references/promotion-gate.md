# Promotion gate

Incremental compilation answers whether the changed dependency closure builds against the current cache. It does not establish acceptance.

Before promoting a better.codes Lean candidate, record and pass every project-required gate, including:

1. authoritative worktree, Git head, dirty-state scope, pinned Lean version, and ArkLib revision;
2. exact official `Solution.lean` target build after the final edit;
3. repository-wide build or evaluator build required by the benchmark policy;
4. `sorry`, `admit`, placeholder, forbidden import, and source-size checks;
5. `#print axioms` or the repository axiom checker for the submitted theorem and its load-bearing providers;
6. independent exact replay or falsifier for the claimed arithmetic or construction;
7. refreshed live frontier and separate official evaluator receipt when authorized.

A passing language server, one affected target, an existing `.olean`, or a successful `#check` batch cannot replace these gates. If final-gate output disagrees with the incremental receipt, classify the incremental result as stale or incomplete and repair the dependency model before continuing.


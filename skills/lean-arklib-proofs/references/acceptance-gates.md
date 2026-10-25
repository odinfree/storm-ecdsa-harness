# Lean and ArkLib acceptance gates

Apply the gates required by the target project and record each command and result.

## Source gate

- Search the relevant source and generated artifacts for `sorry`, `admit`, placeholders, and unauthorized axioms.
- Check imports and namespaces so the theorem uses the intended ArkLib definitions.
- Inspect theorem assumptions and compare them with the original claim.

## Build gate

- Build the exact declared target from the authoritative worktree.
- Record Lean version, package lock, ArkLib commit, repository commit, and build command.
- Remove or bypass caches only when the project procedure requires it; never destroy unrelated user work.

## Trust gate

- Run `#print axioms` or the project's stronger dependency audit on every exported load-bearing theorem.
- Treat classical axioms or approved project axioms according to the repository policy; list them instead of silently assuming acceptance.
- Run any repository-specific checker that validates imports, declarations, or forbidden constructs.

## External gate

- Run the official evaluator or packaging checker when the target requires one.
- Preserve its exact output and identify the source commit it evaluated.
- Recheck any live threshold or acceptance rule immediately before promotion or submission.

The final receipt should separate statement review, successful compilation, trust audit, repository checker, and external evaluator. None substitutes for the others.

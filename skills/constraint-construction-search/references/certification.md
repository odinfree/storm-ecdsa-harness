# Certification boundaries

## Satisfiable or feasible

Extract the complete witness and check it against the original mathematical definition in separate exact code. Preserve both artifacts and hashes.

## Unsatisfiable or infeasible

Prefer a solver certificate with an independently checked proof format when available. Otherwise use a second faithful encoding and solver, exhaustive coverage for a finite domain, or formal proof. A solver status line alone is evidence, not a transferable proof.

## Optimal

Verify the candidate objective independently and separately certify that no better solution exists. Record incumbent, bound, gap, tolerances, and termination reason. Time-limit termination with a strong incumbent is not proved optimality.

## Receipt

Record the mathematical specification, encoding map, model hash, solver and version, full parameters, seed, limits, status, witness or certificate hash, independent verifier command, and remaining proof obligation.

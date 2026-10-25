# Exact algebra routing

Choose the narrowest system that represents the object faithfully and exposes a second route for checking it.

| Mathematical job | Default route | Independent or specialist route | Check before trusting |
|---|---|---|---|
| Broad finite-field, polynomial, or coding exploration | SageMath | GAP/GUAVA, Singular, or Magma | Which backend Sage invoked |
| Ideals, elimination, Groebner bases, algebraic geometry | OSCAR or Singular | The other system, `msolve`, or Magma | Monomial order, coefficient field, saturation, radical assumptions |
| Finite groups, automorphisms, equivalence, coding constructions | GAP/GUAVA | SageMath or Magma | Representation, permutation action, coordinate convention |
| Algebraic number fields, ideals, units, class groups | Hecke or PARI/GP | The other system, SageMath, or Magma | Defining polynomial, embedding, precision, conditional algorithms |
| Named Magma database or specialist algorithm | Magma | Best available open implementation | Licence, database version, algorithm flags |

## Independence test

Two replays are independent only to the degree their decisive paths differ. Record:

- front end and version;
- backend libraries used for the decisive operation;
- whether input was regenerated independently;
- whether the second route checks the semantic claim or merely parses the first route's output.

If both routes call the same backend, label the second run a reproducibility check, not an independent check.

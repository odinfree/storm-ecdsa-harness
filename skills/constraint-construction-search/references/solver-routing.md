# Solver routing

| Structure | Default | Key risk |
|---|---|---|
| Boolean clauses with XOR/parity | CryptoMiniSat | Losing native XOR structure during conversion |
| Bit-precise or symbolic logical relations | Z3 | Confusing bit-vector wraparound with mathematical integers |
| Bounded combinatorial integer model | OR-Tools CP-SAT | Unstated bounds or scale conversions |
| Linear mixed-integer optimization | Gurobi | Tolerances, weak big-M constants, and status interpretation |

Use the simplest faithful representation. A second formulation is especially valuable when an infeasibility or optimality result is load-bearing, but shared preprocessing or generated constraints must be recorded before calling it independent.

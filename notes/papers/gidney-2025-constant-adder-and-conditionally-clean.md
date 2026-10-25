# Gidney 2025 constant adder; Khattar-Gidney 2024 conditionally clean ancillae; Fedoriaka 2025; Häner-Roetteler-Svore 2016 dirty-ancilla primitives

- **Citations / URLs:** Gidney, A Classical-Quantum Adder with Constant Workspace and Linear Gates, arXiv:2507.23079 (2025) https://arxiv.org/abs/2507.23079 ; Khattar & Gidney, Rise of conditionally clean ancillae, arXiv:2407.17966 (2024) https://arxiv.org/abs/2407.17966 ; Fedoriaka, New Circuit for Quantum Adder by Constant, arXiv:2501.07060 (2025); Häner, Roetteler, Svore, Factoring using 2n+2 qubits, arXiv:1611.07995 (2016).

## Key results
- Gidney 2025: in-place +constant with 3 clean ancilla at 4n +- O(1) Toffoli (Adder A), or 2 clean + n-2 dirty at 3n (Adder B); controlling it costs no Toffoli and no workspace; carries are "Z-redundant" (recomputable from the complemented sum), vented by X-measurement and fixed later by carry-xors conjugated by classically-controlled Z.
- Khattar-Gidney: n-controlled X 2n-3 Toffoli with 1 clean ancilla (4n-8 with 1 dirty); incrementer 3n with log* n (~5) clean ancilla; LessThanConst 3n with log* n clean; conditionally clean ancillae cannot be measurement-uncomputed (~2x).
- Fedoriaka: +constant with n-3 ancilla, n-3 AND pairs + 1 Toffoli; controlled n-2 ANDs + n-1 Toffoli.
- HRS 2016: dirty-ancilla incrementer 4n-2, CARRY (compare with constant) 4n-6 with n-1 dirty, constant adder 8n log n with 1 dirty.

## Concrete trick
Trade Toffoli for workspace: constant-workspace streaming ripples with vented carries; conditionally clean ancillae (after AND(a,b) -> t, inside the t=1 branch a and b are known-1 and usable as scratch).

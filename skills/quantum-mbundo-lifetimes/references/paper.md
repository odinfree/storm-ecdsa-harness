# Source and transfer

[MBUndo v1](https://arxiv.org/html/2611.02345v1), sections 2.1–2.3, 3–4 and 8.
The compiler reconstructs logical ancilla lifetimes and replaces eligible unitary cleanup with measurement and conditional phase correction. Interval MBU treats each ancilla's last-use boundary separately, avoiding the unsound assumption that all uncompute gates form an isolated contiguous block. The paper evaluates T cost; a target evaluator can price these transformations differently.

Application hypothesis: omitted lifetime opportunities in a current division could change both cleanup cost and storage pressure. Applicability and savings require source-level analysis and emitted-circuit validation.

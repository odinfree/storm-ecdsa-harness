# Implementation routing

| Measured need | Prefer | Avoid until measured |
|---|---|---|
| High-throughput exact arithmetic kernel | FLINT in C/C++ | Reimplementing arithmetic primitives |
| Exact arithmetic with algebraic composition | Nemo in Julia | Dropping into C for non-hot code |
| Memory layout, SIMD-friendly scans, mature native libraries | C++ | Complex templates before a reference path exists |
| Strong ownership, safe concurrency, standalone binaries | Rust | Unsafe code without a benchmarked reason |
| Rapid specialization and parallel orchestration | Julia | Type-unstable inner loops and unbounded allocations |

Before selecting a route, record wall time, CPU time, peak memory, allocation or cache evidence when available, and the fraction of time in the intended hot path. A rewrite justified only by intuition is not yet an engineering result.

Shared native backends reduce independence. A Nemo result checked by another FLINT wrapper may reproduce the same kernel rather than independently verify it.

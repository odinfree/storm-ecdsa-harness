# Gidney 2019 (blog): Spooky pebble games and irreversible uncomputation; Kornerup, Sadun, Soloveichik: Tight Bounds on the Spooky Pebble Game

- **Citations / URLs:** https://algassert.com/post/1905 (2019); arXiv:2110.08973 (Quantum 2025). https://arxiv.org/abs/2110.08973

## Key result
Ghost pebbles via X-basis measurement with deferred phase fixups. Line graph of n steps: reversible pebbling needs Theta(log n) pebbles at Theta(n^1.58) time; spooky: 3 pebbles at quadratic time, Theta(log n) pebbles at Theta(n log n), ghosted midpoint Theta(n^1.32). General: a time-T space-S classical computation runs with O(T/eps) gates and O(T^eps S^(1-eps)) qubits, tight on a line.

## Concrete trick
Measure out a value whose only remaining role is to be uncomputed; fix the (-1)^f kickback later with a cheap phase circuit; checkpoint and recompute segments instead of storing every intermediate.

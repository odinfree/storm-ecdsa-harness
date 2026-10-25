# Gidney 2019: Asymptotically Efficient Quantum Karatsuba Multiplication; Parent, Roetteler, Mosca 2017: Reversible circuits for Karatsuba-based integer multiplication

- **Citations / URLs:** arXiv:1904.07356 (2019) https://arxiv.org/abs/1904.07356 ; arXiv:1706.03419 (2017).

## Key result
Karatsuba with recursive calls that add directly into output sub-registers: O(n^lg 3) Toffoli with O(n) space (vs O(n^1.427) space before); crossover against schoolbook at a few tens of bits per leaf; intermediate products never materialised, so nothing needs uncomputing beyond the leaves.

## Concrete trick
Accumulate each recursive product into the right slice of the output with signed adds (build-apply-unbuild), so A, B, C never co-live.

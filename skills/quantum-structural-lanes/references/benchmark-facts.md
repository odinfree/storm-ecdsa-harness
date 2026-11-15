# ECDSA benchmark facts

Verify these against the active evaluator/API each session. These describe the inspected benchmark, not every quantum score.

- **Q** is the emitted wire extent (maximum qubit ID + 1); a smaller allocator live count does not itself lower Q. Reused lifetimes and every tied peak matter.
- **T** on the board is rounded mean **executed** Toffoli cost. Static/emitted counts include branches not taken; `CCZ` also incurs Toffoli cost. Depth and paper T-gate counts are different metrics.
- **Hmr** records an independent random coin, contributes `qubit & coin` to phase and clears the target. It does not reveal the target's computational bit. The simulator tracks `Neg`, so discarding physical global phase can still fail this harness.
- The stock panel checks classical outputs, phase and ancilla on 9,024 shots. Preserve per-channel failures and their identities. A clean official packet is finite evidence, not an exactness proof.
- Any operation-stream change changes the Fiat–Shamir inputs. A shared seed alone does not establish same-input pairing; use explicit corpora and track measurement roles.
- Define lambda as expected failing shots per panel, specifying the failure union. With rare approximately independent failures, clean-packet probability is approximately `exp(-lambda)`, so independent nonce trials cost approximately `exp(lambda)` on average. Correlation, selection and uncertainty can invalidate this estimate; a nonce does not repair fixed-input failures.
- `WALK_STOP` and profiler counts price a change. They do not establish traversal correctness or official executed cost.

## Frontier and cliffs
For candidate width `q`, the ceiling is `C(q) = min(T_i : Q_i <= q)` over officially scored, valid rows. A width improvement needs `Tnew < C(q)`. Do not compare only to the old row at q. Keep scalar-product leadership separate.

In the inspected scalar API, rows rejected **only** for `score did not improve current best` can be valid Pareto points. Require official metrics/score; exclude failed, cancelled and correctness-rejected rows. Recheck this mapping if the API changes.

One-line snapshot calculation, from the installed skills directory (no network calls):

```sh
python3 quantum-record-mining/scripts/frontier_mine.py board.json --q 825 --out frontier.json
```

For an integer scored parent `(Q,T)`, a one-qubit cut improves its product only when added T is strictly below `T/(Q-1)`. The maximum integer addition is `(Q*T-1)//(Q-1)-T`. This product budget differs from `C(Q-1)-T`; crossing a valuable Pareto cliff can worsen the parent's product. Price both objectives explicitly.

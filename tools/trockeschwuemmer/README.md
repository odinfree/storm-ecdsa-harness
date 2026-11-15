# Trockeschwümmer (dry swimmer)

Technical id: `walksim` (`walksim2.js`, `hd_divstep.js`, `ambig.js`, `costmodel.js`).

Practises the stroke on dry land: classical simulators of the modular-inversion walks behind ecdsa.fail
circuits, on the secp256k1 prime with BigInt arithmetic. They answer how many steps, halvings and transcript
bits a walk rule needs, before anyone writes a gate.

- `walksim2.js "<rule>" [n]`: statistics over n random inputs for one walk rule: adds, halvings, ticks and
  tape bits (mean, p99, max). Rules include the ping-pong walk, Leapfrog variants (M forced steps, strip
  cap), plus-minus and Stein with exact or truncated comparison. The rule names are the keys of the `rules`
  table in the file.
- `hd_divstep.js`: termination statistics of the half-delta divstep and NAF weights of K-step transition
  matrices.
- `ambig.js`: the share of divsteps whose branch cannot be reconstructed from the successor state, which is
  the number of bits a transcript must keep.
- `costmodel.js`: a Toffoli-per-step cost model for batched (jump-K) divstep updates against the elementary
  walk.

```bash
node walksim2.js "leapfrog M=2 cap3 (HEAD)" 1000
node costmodel.js
```

Needs Node 18 or later. Output: one line per rule or table row on stdout.

## Limits

These are counting models from October 2026. They use `Math.random`, so runs do not repeat exactly. Their
gate prices are the simple ones written at the top of each file, and no real tree was censused for them. Use them to
rank walk rules, then measure the winner with a count build. "HEAD" in a rule name meant the public Leapfrog
record tree of that month.

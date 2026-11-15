# Inert-op screen: specification

Read this before implementing the screen (steps 1 to 6 of the skill). It is written against a generic op model.
Map your benchmark's ops onto the roles below first.

## 1. Op roles

| role | meaning | example in a reversible-circuit benchmark |
|---|---|---|
| charged | counted by the judge once per sample that executes it | doubly controlled gate |
| free | changes state, not counted (or counted in a term you ignore) | single-control and uncontrolled gates |
| measure-write | writes a random outcome into a classical bit | basis measurement with reset |
| measure-only | consumes outcome randomness, writes no classical bit that is read | reset with a phase-only draw |
| store | writes a constant into a classical bit | store 0, store 1 |
| invert | flips a classical bit | bit invert |
| push / pop | open and close a block conditioned on a classical bit | condition stack |

Every op may carry its own condition bit. An op **executes** on a sample when all enclosing block conditions and its
own condition are 1 there.

## 2. Fire mask

State is bit-sliced: one machine word per wire holds 64 samples. For a charged op with controls `c1, c2` and
execution mask `ex`:

```
fire = ex & state[c1] & state[c2]
acc[op_index] |= fire          # per-op accumulator, one bit is enough: acc[op_index] |= (fire != 0)
```

The judge charges `popcount(ex)` for this op. When `fire` is zero on every screened sample, the op was charged and
did nothing. After all seeds: `inert = { i : charged(i) and acc[i] == 0 and not excluded(i) }`.

The set is an intersection over seeds. More seeds can only shrink it.

## 3. Exact mode

Reproduce the judge's execution, including its measurement outcomes.

- Derive the seed stream as the judge does. Generate the inputs.
- Outcome randomness: the judge reads a fixed number of bytes per measuring op per batch, in batch-outer, op-inner
  order. Global index of the word for (measuring op j, batch b) is `b*H + j`, with H the number of measuring ops.
- Read one batch's H words in a single call and scatter them into an op-major buffer `rng[j*nb + b]` (nb = number of
  batches), so the transposed loop of section 5 reads each op's words contiguously.
- Consume all H words per batch to keep the stream aligned. Store only the words of measure-write ops; a
  measure-only op's outcome never reaches a condition, so its word is read and discarded. That halves the buffer in
  the worked example.

Cost in the worked example: about 13 minutes for 9 million inputs on 16 cores.

## 4. Fast mode and the taint pass

**Claim used.** Forcing every measurement outcome to 0 is a valid execution: a measurement-based uncompute corrects
on a random bit, and the outcome-0 branch needs no correction. Wire state therefore evolves correctly with no
outcome randomness at all. Check that this claim holds for your benchmark's measurement semantics before using the
mode.

**What it gets wrong.** An op that runs under a condition that depends on a measurement outcome fires on about half
the samples in reality and on none under forced zeros. Such ops must never enter the inert set.

**Taint pass** (one linear pass over the op list, before any simulation):

```
tainted[bit] = false for all bits
stack = []            # one boolean per open block: was its condition tainted
tdepth = 0            # number of open blocks with a tainted condition
for i, op in ops:
    cc = op.condition                      # may be none
    rng_dep = tdepth > 0 or (cc is not none and tainted[cc])
    case op.role:
      charged:        if rng_dep: exclude[i] = true
      push:           t = cc is not none and tainted[cc]; stack.push(t); if t: tdepth += 1
      pop:            if stack not empty: if stack.pop(): tdepth -= 1      # a pop at depth 0 is a no-op
      measure-write:  tainted[op.target_bit] = true
      store:          tainted[op.target_bit] = not (tdepth == 0 and cc is none)
      invert:         tainted[op.target_bit] = tainted[op.target_bit] or rng_dep
```

Properties:

- A bit becomes tainted when a measurement writes it and stays tainted until an unconditional store.
- A store under any condition leaves the bit tainted. This is conservative: the store may not execute.
- The pass is static and conservative. It can exclude ops that are in fact inert; it must not admit one that
  depends on an outcome. The fast set is therefore a subset of the exact set on the same seeds. Test that.

Cost in the worked example: about 7 minutes for the same 9 million inputs, with a slightly smaller set.

## 5. Memory layout for scale

- **Transposed loop.** Outer loop over ops, inner loop over the batches of one seed, on a wire-major state
  `q[wire*nb + b]`. The op list is streamed once per seed, not once per batch, and the per-wire state stays in
  cache. In the worked example the op list was 568 MB and the state 1,156 wires.
- **Condition-bit compaction.** Pass 1 over the ops marks every classical bit that is ever read as a condition
  (own condition or push). Remap those to a dense index and skip writes to every other bit.
- **Seeds in parallel.** One accumulator per worker; OR-merge at the end.
- **Seed derivation with prefix reuse.** When seeds differ only in a suffix of the artefact (a nonce tail), absorb
  the fixed prefix into the hash once, copy the hasher per seed and feed only the tail.

## 6. Index list format and binding

```
# stream_sha256 <hash of the exact op stream the indices refer to>
# screened_inputs <count>   mode <exact|fast>   seeds <description>
<op index>
<op index>
...
```

The loader in the generator must:

1. compute the hash of the stream it is about to filter and compare it with `stream_sha256`; on a mismatch, stop
   with an error (never skip silently);
2. apply the list after every other post-pass, since indices refer to the final stream;
3. be compiled in for the official build (no environment read), with a development switch to disable it;
4. print how many ops it removed.

## 7. Validation protocol

| step | action | pass criterion |
|---|---|---|
| a | Run fast and exact on the same small seed set. | fast set is a subset of exact set |
| b | Self-check on a tiny artefact with a planted inert op, a planted half-firing conditioned op, and a planted always-firing op. | exactly the planted inert op is reported in both modes; the conditioned op is excluded in fast mode |
| c | Double the screened inputs until the set size is unchanged. | last doubling changes nothing |
| d | Build with the drop enabled. Score with the judge or an exact replica on several seeds that were not screened. | average cost down by about the number of dropped ops; failure density about equal to the pre-drop baseline |
| e | Find a passing seed on the dropped stream; run the official judge on it. | all checks pass |
| f | After any generator edit. | list rejected by its hash; re-screen |

Criterion d is the one that detects an over-aggressive drop: extra failures on unscreened seeds mean ops in the set
do fire outside the screened support.

## 8. From list to rules

1. Tag each emitted op with its generator site during the build (a site id in a side table, not in the stream).
2. Histogram the inert set by site. Large families first.
3. For each family, read the site and state the invariant that makes the op inert. If none can be stated, leave
   the family out.
4. Implement the skip at the site behind a switch with break controls (see the
   `lever-switches-and-break-controls` skill).
5. Validate each rule alone on every channel the judge checks; keep only the rules that pass all of them.
6. Remove the list and its loader. Report: ops removed by rules, ops the list removed that the rules do not, and
   the resulting cost against the list-based build.

In the worked example the rule-based row is 1153 x 1,367,698 and the list-based row before it 1156 x 1,366,238. The
two rows differ in other changes as well, so their difference is not a clean measure of what the rules fail to
recover; measure that on one tree with the list on and off.

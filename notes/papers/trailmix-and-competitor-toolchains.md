# Trail of Bits TrailMix and competitor toolchains (reference circuits, evaluator replicas, nonce screens)

- **Sources:** https://github.com/trailofbits/trailmix (kmx circuits, notes/OVERVIEW.md, kmx_circuit_summaries.md); https://github.com/BitWonka/ecdsafail-tools ; https://github.com/jieyilong/ecdsafail_gpu_toolkit ; MonitSharma/elliptic_curve_dsa (1,595 commits; docs/research-plan.md, experiments/*/STATUS.md, agents/{toffoli,product,qubits}); Eigen Labs blog "From a Hidden Quantum Circuit to Open Autoresearch" https://www.eigenlabs.org/blog/open-autoresearch-the-ecdsa-fail-story/

## Key results
- TrailMix: five reference circuits: low-qubit 1,173 Q x 2.48M T (Schrottenloher dialog), jump-lowqubit 1,169 x 2.09M, jump-lowtof 1,412 x 1.90M ("venting": +240 Q for measure-and-fixup uncompute), shrunken-PZ divstep state machine 1,050 x 32.3M (two inversions per addition via slope invariance); ghost/spooky-pebble API so a coordinate and lambda are never simultaneously live; 64-shot parallel simulator; time-travel debugger; phase-correctness gate. Independent confirmation that a naive reversible divstep (no branch recovery) is > 10x worse in T than record-and-replay.
- BitWonka tools: dead-ccx-finder (bit-sliced screen for CCX whose control is 0 on every input; 9M inputs in ~13 min on 16 cores); fasteval (evaluator replica, 1.24B-op circuit in ~3 min / 33 GB vs 69 GB official; FE_SALT for true failure rate on fresh shots).
- GPU toolkit: bit-exact GPU port of the classical GCD pre-filter, ~13.6k nonces/s on an RTX 5090; PR #718: 14M nonces in 3 min, 17 survivors, 1 clean.
- Eigen Labs blog: Google's withheld points (1,175 x 2.7M; 1,425 x 2.1M) were matched by the crowd in ~8 h and passed in ~72 h; organisers publish no circuit-level write-ups beyond the paper and PR notes.

## Concrete tricks
Separate exact gate removal (static screens) from nonce re-sampling; paired CRN lambda estimation; evaluator replica with salted shots for honest failure rates; time-travel debugging of reversible IR.

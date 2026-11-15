# Adapter contract and templates

Read this before writing the adapter (step 3 of the skill) and its gate test (step 4).

Vocabulary: the **donor** is the tree the module comes from. The **caller** is your tree. A **builder** is the
object that allocates wires and classical ids and collects ops. **Stand-ins** are registers allocated in a private
donor builder that play the role of the caller's registers during the private build.

## 1. The seven parts of an adapter call

Signature: `call(caller_builder, kind, registers..., cap)`.

| # | part | why | assertion that guards it |
|---|---|---|---|
| 1 | `room = cap - caller.live` | The module may use only what the caller has left at this site. | `room >= module_minimum(kind)`, with a message naming the site. |
| 2 | Dry build: for pool sizes from large to small, build the module in a throwaway donor builder and read its measured peak above the stand-ins; keep the largest pool whose peak is at most `room`. | A reservation rule is an estimate; the measured peak is a fact. One unit of pessimism can push a call under a cost cliff. | `measured_peak(pool) <= room`; log `site, room, pool, peak, cost`. |
| 3 | Private build: fresh donor builder, allocate stand-ins, set the module's cap through the module's own mechanism (a parameter, a thread-local, a stubbed constant) to stand-ins plus pool, then call the module unchanged. | The module runs exactly as in its home tree, so everything its cost and correctness rely on survives. | The private builder's peak equals the dry build's peak for the same pool. |
| 4 | Restore output order: when the module may return a register on relabelled wires, put bit i back on stand-in wire i with free swaps. | The caller's register must keep its wire order. | After restoring, the returned wire list equals the stand-in list. |
| 5 | Rewrite every op: stand-in wires map to the caller's register wires; every other wire the module touched maps to a fresh caller wire; a shared scratch classical id (one both builders use for immediately consumed results) maps to the caller's; every persistent classical id maps to a fresh caller id. | Wires and ids are private namespaces. Persistent ids that collide corrupt later conditions without any crash. | No op in the rewritten list carries a donor id; a sentinel id used for "unmapped" never appears. |
| 6 | Cleanliness: the private builder's live count is back to its base (stand-ins only). | Every non-register wire must be zero before and after, so it can be a fresh caller wire that is freed afterwards. | `private.live == base`. |
| 7 | Append the rewritten ops verbatim with the module's cost to the caller's stream and cost counter, then free the fresh wires. | Verbatim ops keep the donor's measured uncompute and conditioned repairs. | Caller's live count after the call equals its live count before. |

Keep the append primitive tiny (the worked example's `push_foreign(ops, cost)` is eight lines). Everything else
lives in the adapter file so one switch can bypass it.

## 2. Stubs for what the module reads from its home tree

- The cap: set per call by the adapter (part 3).
- Any peak or layout constant of the home tree: stub with the home tree's value and say so in the note.
- Entry points you do not use: replace with a function that fails loudly when called.
- Visibility: making one item public is an acceptable edit; list it.

List every edit. In the worked example the complete list for one port was two path or visibility edits and two
stubs.

## 3. Gate-test contract for the adapter

For every `kind` the adapter supports, on at least 64 random inputs in the module's domain:

1. the result is exact on every input;
2. the input registers are restored;
3. every other wire returns to zero;
4. every side property the judge checks (phase, scratch flags, refund counters) is at its neutral value;
5. the caller's live count is unchanged across the call.

Run the whole test at each pool size in a list that brackets every cost cliff the fit probe flagged, plus one size
well above. Record the list in the note ("passes at pools 44, 45, 46, 47, 48 and 55").

Add break controls for the adapter itself (see the `lever-switches-and-break-controls` skill): 1 = skip the order
restore, 2 = map a persistent id to itself, 3 = do not free the fresh wires. Each must fail this test.

## 4. Fit-probe test skeleton for a compiled tree

Write this in the donor tree. It is a template: replace the three marked calls with the donor's own API.

```rust
// Run: FIT_CAPS="825,830,840,852,870,900,975" cargo test --release fit_probe_<module> -- --nocapture
#[test]
fn fit_probe_module() {
    let caps: Vec<usize> = std::env::var("FIT_CAPS").unwrap_or("825".into())
        .split(',').map(|s| s.trim().parse().unwrap()).collect();
    println!("block\tcap\tresult\tpeak\tcost");
    for cap in caps {
        // catch_unwind turns the module's own "does not fit" panic into a table row
        let r = std::panic::catch_unwind(|| {
            let mut b = Builder::new();                 // <-- donor builder
            set_cap(cap);                               // <-- the module's own cap mechanism
            let regs = alloc_standins(&mut b);
            module_under_test(&mut b, &regs);           // <-- the module, alone
            (b.peak(), b.expected_cost())
        });
        match r {
            Ok((peak, cost)) => println!("module\t{cap}\tbuilds\t{peak}\t{cost:.1}"),
            Err(_) => println!("module\t{cap}\tdoes not build\t-\t-"),
        }
    }
}
```

For a tree in another language, or to drive a build command from outside, use `scripts/fit_probe.py` with a
command that prints `peak=<n> cost=<x>` and exits non-zero when the module does not build.

## 5. Note section for a splice

- Fit-probe table (all rows, including "does not build").
- Files copied (count, total size), manifest hash, every edit.
- Stubs and their values.
- Adapter parts and the pool chosen per call site.
- Gate-test result with the pool sizes tried.
- Switch name and the hash reproduced with it off.
- Inherited approximations with rates, attributed to the module's authors.
- Paired failure-rate table against the base on shared salts.
- Credits per routine: author, tree, commit.

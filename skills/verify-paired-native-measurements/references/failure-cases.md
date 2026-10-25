# Observed failure cases

These cases came from an independently reviewed measurement harness for a paired native benchmark (October 2026). They are source and fixture failures, not native performance results.

1. Initialize a phase with an 1,800 s cap at wall 1000 / monotonic 100, then present wall 1001 / monotonic 2001. A mocked subprocess boundary still ran with a 1,799 s allowance. The correct behavior is to reject the elapsed-budget overrun independently of the wall clock.
2. Preserve a complete passing A/A phase, omit the required screening and confirmation, and coherently rebind archive hashes plus a failure-shaped label. The reader incorrectly returned a completed gate failure. Correctness requires the declared conditional phase graph, not just a valid prefix.
3. Change the warmup's raw GNU-time RSS and matching records to 0 while keeping valid measured rows. The reader incorrectly admitted the experiment. Warmups stay subject to run validity even though their values are excluded from the sample statistic.
4. Perform a genuine archive restoration, then append corruption before the semantic result is published. The CLI incorrectly admitted the restored result with a new, unchecked archive hash. Keep the original record, and test mutation after restore, after semantic validation, and at publication.

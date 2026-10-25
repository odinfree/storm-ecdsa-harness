# A budget spanning two hosts

Use this only when the experiment declares a cap across a controller and a remote
worker. It adds no requirement to ordinary local tests and creates no execution
or provider authority.

Record the controller's monotonic origin before the first operation charged to
the cap. Keep that origin through staging, execution, archive transfer and final
local validation. Record the worker's own monotonic anchor and boot identity
separately. Boot changes invalidate the corresponding anchor.

One conservative mapping is:

`worker_deadline = worker_anchor + total_cap - controller_elapsed_at_anchor_receipt`

The controller elapsed term includes all preparation and the round trip through
receipt of the worker anchor. Since the worker anchor was sampled before receipt,
this charges the uncertainty conservatively. A later worker launch uses that
saved deadline; it does not obtain a fresh full-duration cap. Absolute resource
cutoffs can further shorten the permitted window. The controller independently
checks its original elapsed budget after final readback.

Keep phase caps and total caps distinct. A completed native phase is not a
completed end-to-end experiment when transfer or validation exceeded the declared
total. Preserve late evidence as incomplete, rather than changing the cap or
retrospectively dropping charged preparation.

Useful falsifiers use unrelated clock offsets, delayed anchor receipt, delayed
worker entry, a changed boot, wall-clock rollback and a late collector. A pure
clock fixture checks the budget logic; it does not establish actual Linux
compatibility, process cleanup, proof correctness or performance.

# Cold builds under nested time limits

Treat compilation duration separately from prover performance. A cold reference
build finishing close to its child deadline is evidence that the allowance may
be too small for the remaining roles. A build timeout before the candidate
starts supplies no candidate correctness or speed result.

Size the original run for every required role, tool probe, preparation step and
cleanup reserve. Check the reachable limits together: the caller's per-build
request, compiler helper's accepted maximum, aggregate controller, outer
supervisor and transport. Increasing only the caller's requested duration can
leave a lower limit in force. Preserve one original aggregate deadline; a longer
child allowance must still be bounded by its remaining time. Diagnostic entry
points that are not called by the production route need not be changed merely
because they contain older constants.

Keep the failed run and its actual wait/cleanup records. For a separately
authorized successor, keep source, compiler flags, features and role selection
fixed when the intended repair is only the time allowance. Successful cleanup
closes resource ownership; it does not turn an incomplete compilation into a
successful artifact binding. No fixed number of seconds is prescribed here.

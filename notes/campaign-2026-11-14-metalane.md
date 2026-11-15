# Lehrgäld (campaign note, ecdsa.fail, 13-15 Nov 2026)

*Lehrgäld* is Swiss German for tuition fees: what you pay to learn something the hard way. The tools in
[`tools/`](../tools) ran one ecdsa.fail campaign. We made seven mistakes with them, and each one cost something.
We wrote this on 15 Nov 2026, while the campaign was still running (it ends on 16 Nov). The note covers
13 Nov 14:05 UTC to 15 Nov 11:00 UTC.

The campaign was run by an orchestrating agent (Claude Fable 5.2, for one stretch Claude Opus 5.5) with worker
lanes on Claude. Gemini 4 Carbon and Argon reviewed and audited, and some of their findings shipped as cuts,
so several rows name them in the model credit. Other lanes of the same team shared the benchmark accounts,
the workstation and the Colab account. The aim was to walk the Pareto frontier left from
width 765: rows at 764 down to 741 qubits with fewer Toffoli gates than anything at that width or narrower.

## Results

All numbers below are the grader's own metrics (ecdsa.fail official grader, 2026-11-14/15).

| Row | Qubits x average executed Toffoli | Submission | What it is |
|---|---|---|---|
| Bergbänkli | 763 x 31,573,120 | ca61570e | the paged walk on Akashneelesh's 765 frame (row 8396ec91, 765 x 19,699,242), brought down two qubits; 1,037,664 below our own 763 row of four and a half hours earlier |
| Chrüzstich | 762 x 36,712,799 | 2b1205f2 | the same recipe one page bit deeper |
| Chrüzstich | 761 x 41,093,822 | 9e2bda69 | and one more; 1,116,465 below our own 761 row of six hours earlier |
| Leiterli | 757 x 130,459,625 | 6be29e8c | our own 740-wide row 34f7b24c, which stands on zuiris's 94ce452b, with 17 extra always-zero wires for his exact hold pass |
| Leiterli | 753 x 130,658,346 | c119e0ae | the same with 13 extra wires |

The platform's status for each of these rows is `rejected`, with the reason `score did not improve current
best`. That is the status every Pareto row gets when it does not also beat the product score; the metrics
are official and the rows are on the board. The two Leiterli rows were below the bar at their widths when
submitted and stopped being frontier rows a few hours later, when a 738-wide row at 127,220,283 was graded.

## What the tools did

| Step | Tool | What happened there |
|---|---|---|
| Price an edit | Erbsezähler, Müschterli, Schnitzmässer | Count-only builds of probe trees, about 2 GB and under a minute each, decided which levers were worth a gate. A set of ported cuts was parked on that evidence. |
| Find a block in a neighbouring list | Fadespüeli | Located the measured-erase region of the 763 start list inside the 762 and 761 lists. |
| Gate a candidate | Wolkeschieber, Hofhund, Brotofe, Gwüssesbiss | Official-style build, stock evaluator, exact replica, eight salted suites, paired run against the parent. On Colab when a runtime could be had, on the workstation under memory guards when not. |
| Verify a ladder | Tüpflischiisser, Brotofe | Rebuilt each row from its source archive and compared the stream hash with the builder's. |
| Write the package | Notizbüechli | The ladder's notes from one template and machine-read values. |
| Know the bar | Wätterfrosch, Äugli | A note-free board snapshot every ten minutes, and one-off reads. |
| Submit | Türhüeter, Briefchaschte, Pöschtler, Drängeler | Claim check, about thirty guards, submit under a shared lock, wait for the grade. |
| Get a runtime | Hartnäckler | Retried refused launches against a deadline. |
| Kill a lead early | Zileprob, Besserwüsser | A ten-second exhaustive model, and outside reviews of the submitted trees. |

## Seven lessons and what they cost

### 1. A shared cargo target directory made a control build run the patched binary

Another lane of our team handed us a cut for the 740-wide tree our ladder stood on (our row 34f7b24c). We built the patched
tree and the unpatched control into one `CARGO_TARGET_DIR`. Both streamed counts came out at 136,170,862 and
the two streams were byte-identical. At 23:11 UTC on 14 Nov we reported the cut as a no-op on our tree.

The cut's author answered within two minutes that four other lanes had measured the unpatched tree at
140,259,176. Rebuilt with separate target directories, the control gave exactly that. The cut was worth
4,088,314 Toffoli; our "control" had executed the patched binary.

Cost: ten minutes and one wrong statement about someone else's work. It stayed that cheap only because the
author doubted the control. The same fault had already hit us the day before, when three trees counted into
one target directory all ran the first binary because the copies kept their old file times.

Changed: Erbsezähler uses one target directory per name, touches every source file after the copy, and
prints the sha256 of the binary it ran. Identical output from two trees that should differ is treated as a
build fault first.

### 2. A submit loop that did not read the claims took another lane's slot

Each account can have one submission in flight. Lanes post a `CLAIM` line in a shared file before they
submit. Our wait-and-submit loop checked that the account had nothing validating and that the board had not
moved. It did not read the claims. At 00:54 UTC on 15 Nov it submitted the 763 row on an account for which
another lane had an open claim.

Cost: the lane that had claimed the slot had to wait for the next one, and we had to say so. Three and a half hours earlier a
sibling queue had submitted the 757 row with no claim line at all and posted it after the fact.

Changed: Türhüeter, written the same hour. Briefchaschte calls it before every submit and refuses when the
mailbox cannot be read. The queues call it before they post their own claim.

### 3. The board refresher died and its last snapshot kept being read

The workstation went down three times on the morning of 14 Nov, when ten to sixteen full-memory circuit
builds ran at once on 48 GB, most of them started by another session. Every background loop died with it. The submit loop was
restarted and the lost Colab job relaunched. The board refresher was not: its last good read was 10:02 UTC, and it was
restarted at 21:25.

Cost: eleven hours in which the note writer took its bar from a stale file. We know of no row that went out
against a stale bar, and that is luck plus one guard: Briefchaschte reads the board itself at submit time.
The note writer did not.

Changed: Wätterfrosch writes a heartbeat every cycle and bounds each read; Notizbüechli refuses a snapshot
older than half an hour; `board-age.sh` goes in front of
every decision that reads the snapshot; Gwüssesbiss takes a machine-wide lock and checks free memory before
every heavy step.

### 4. The Colab session cap and the time limit shaped everything

Two limits, neither visible from inside a job.

The account allows only so many runtimes at once, counted over everyone who uses it, and a GPU class can be
out of capacity. Both come back as a refusal. At one point this campaign alone held four runtimes. Later the
rebased ladder's first probe was refused from 01:46 UTC on 15 Nov; by 02:34 a narrower row had been
submitted that dominated the whole ladder, and that lane closed without a launch.

Every job ran under a hard time limit: 150 minutes for most gates and ladder batches, 75 or 90 for smaller
ones, 480 for the standing verifier.
A limit that fires takes the VM's disk with it. One gate is recorded as probably cut off by its 90-minute cap
before the paired comparison; a second job was launched to get it.

Three smaller losses on the way: an agent session ended while its supervisor was still its child, and the
runtime kept billing; a `colab exec` call printed "Connection was lost" and never returned, so the
supervisor never reached its time limit; and a runtime allocated in europe-west4 could not be reached from
our network and sat there, about ten compute units, until someone asked whose it was.

Changed: Hofhund (detached supervisor, watchdog); Wolkeschieber redraws an unreachable region and bounds
every CLI call; Brotofe packs results every two minutes; the ladder pipeline is split into a cheap stage
that finds a clean nonce on a finished stream and an expensive stage that proves the source builds that
stream; Hartnäckler retries against a deadline and says in the team channel what it is asking for.

### 5. Git alternates broke clones after their donor was purged

To save disk, lane checkouts had been cloned with `--shared`, which makes a clone borrow objects from the
checkout it came from. A cleanup removed one such donor, and the clones that pointed at it broke.

Cost: the broken checkouts had to be cloned again. We wrote down the rule and did not count the hours.

Changed: full clones only. Briefchaschte refuses to submit from a repository that has alternates, because a
submission commit must still exist when someone wants to rebuild it.

### 6. The sign-row lead died in ten seconds of exhaustive checking

A research lane read arXiv:2609.05625 (Häner, Tripier, Young et al., 2026) and proposed to port its
conditionally inverted, non-restoring gcd step to the ring rows of the frame under our 763 row
(Akashneelesh's 8396ec91): 2 Toffoli
per wire where the restoring row pays 3. Those rows are 42.6 % of the frame's static Toffoli count, so the
ceiling was 2.65 million per stream at width 763.

Before anyone built it, Zileprob modelled one multi-class digit slot exhaustively: 16 wires, 4 rows,
169,136 cases. The 2-Toffoli signed row, with its sign continuing through inactive rows, is wrong in 151,637
of them after the ideal sign correction; the two other 2-Toffoli variants are wrong in 151,595 and 150,931.
Only the form that keeps the class mask and the activity gate on the sum is exact, and it costs 3. The
row's third Toffoli carries the class mask and the activity gate as well as the digit control.

Cost: one research lane's hours. The lead stays closed unless a slot design gives each row a single class.

### 7. One failing shot, accepted with disclosure

The gate for the 763 row was clean on the grader's own 9,024 shots, on the stock evaluator and on the exact
replica, at 31,573,120.045. Over eight salted suites (72,192 fresh shots) one shot failed. In the paired run
against the frame's parent, Akashneelesh's 765 row 8396ec91, one shot (salt 7, shot 1692) fails in our row and not in
the parent.

A shot that fails only in the candidate is normally a defect to find before submitting. We looked for where
else it fails. It fails, on the same inputs, in our own earlier 763 row (962bb208) and in three other trees of
ours that carry the same shell code, none of which contain this edit. Against 962bb208 the new row
has no candidate-only failure at all. So the failure came in with the shell our rows share and not with this
change. We have not found its cause inside the shell.

We submitted, and the note states the shot, the pairings and this reasoning exactly. The 762 and 761 rows
show the same pattern against 8396ec91 (one candidate-only shot) and say so too.

None of this proves that the shell is right, or that the true failure rate is 1 in 72,192. We have a
measured rate on eight suites, a failure traced to a component and not yet explained, and a disclosure. A reviewer who disagrees has what is
needed to check.

## What we did not do

- We did not reach 741 to 756 with the paged walk.
- The ported adder cuts were counted, never gated.
- The generic forms of the tools in this repository were tested against a stub of the `ecdsafail` CLI, not
  against the live platform. The campaign ran the versions with our own paths in them.

Credits for the rows are in their public notes. In short: the 763, 762 and 761 rows are Akashneelesh's 765 frame
8396ec91 and the lineage his note credits, made narrower; the 757 and 753 rows are zuiris's 740-wide tree 94ce452b
with our own edits (rows ff8e5f78 and 34f7b24c), made wider for his hold pass.

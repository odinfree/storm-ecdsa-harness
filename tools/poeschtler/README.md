# Pöschtler (postman)

Technical id: `submit-wait.sh`.

Delivers one finished row package and waits for the answer. It waits for an account with nothing validating,
binds the approval file to the exact note, dependencies, commit, tree and model line, runs Briefchaschte as a
dry run, posts a `CLAIM` line, submits under the shared lock, records the submission id, then polls until the
row is graded.

## Inputs and outputs

`submit-wait.sh <pkgdir> <W> <label>`; environment in the script header (`ACCOUNTS`, `ACCOUNTS_DIR`,
`CLAIM_MAILBOX`, `MAILBOX_POST`, `CLAIM_SELF`, `SUBMIT_LOCK`, `STATE_LOG`). It writes `approved`,
`dryrun-stderr.txt`, `submit-response.json`, `submit-stderr.txt` and `submission.id` into the package and
prints `SUBMITTED <id> on <account>` and `GRADE: <status> <metrics> <reason>`.

Exit codes: 2 no free account after 90 minutes, 3 hygiene, 4 dry run refused, 5 submit gave no id, 6 gave up.

## Behaviour worth knowing

- By default Pöschtler writes the `approved` file itself, from the package as it is at that moment. Starting it is
  the approval, and Briefchaschte's approval binding then only guards against a change between the dry run and the
  submit. For a real second pair of eyes, have the reviewer write `approved` and run with `KEEP_APPROVED=1`.

- When the dry run is refused because another lane holds an open claim, it waits four minutes and starts over.
  Any other refusal stops it.
- A `conflict` answer (a row already in flight) releases the claim in the mailbox and retries after three
  minutes.
- The grade line prints the status as the platform gives it. On ecdsa.fail a Pareto row that does not improve
  the product score comes back as `rejected` with the reason `score did not improve current best` and with
  official metrics: that is a graded row.

## Run

```bash
export ACCOUNTS="main:TeamAccountA second:TeamAccountB" ACCOUNTS_DIR=$HOME/accounts
export CLAIM_MAILBOX=/path/to/mailbox.txt CLAIM_SELF=mylane MAILBOX_POST="tee -a /path/to/mailbox.txt"
nohup bash submit-wait.sh pkg/w762 762 "paged walk at 762" > pkg/w762/postman.log 2>&1 &
```

Needs `flock`, `ecdsafail`, `python3`, `shasum`. Tested end to end against a stub CLI; not run against the live
platform in this generic form.

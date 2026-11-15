# Drängeler (queue-jumper, reformed)

Technical ids: `submit-queue.sh`, `auto-submit.sh`.

Submits a ladder of finished row packages unattended. `submit-queue.sh` takes the widths in order and, for
each, waits for a free account, runs an optional prepare step, binds the approval, asks Türhüeter, dry-runs
Briefchaschte, posts a `CLAIM` line and submits under the shared lock. `auto-submit.sh` wakes every five
minutes and queues every package that is `READY` and has no `submission.id`, narrowest first.

The name is earned. The first version checked only whether the account had something validating and posted
no claim line: one row got its mailbox line after the fact (14 Nov 2026). A few hours later a sibling
wait-and-submit loop, built the same way, submitted on an account where another lane had posted a claim.
The gate now runs before our own claim line, and a blocked row is requeued.

## Inputs and outputs

`submit-queue.sh <pkgroot> W1 W2 ...` and `auto-submit.sh <pkgroot>`; packages are `<pkgroot>/w<W>/` in the
layout Briefchaschte reads, plus a `READY` file and `row.tree`. Environment as in Pöschtler, plus `PREPARE`
(a per-row hook) and `MAX_HOURS`. Logs: `<pkgroot>/submit-queue.log`, `<pkgroot>/auto-submit.log`; per
package `submit-response.json`, `submit-stderr.txt`, `submission.id`.

## Run

```bash
export ACCOUNTS="main:TeamAccountA second:TeamAccountB" ACCOUNTS_DIR=$HOME/accounts
export CLAIM_MAILBOX=/path/to/mailbox.txt CLAIM_SELF=mylane MAILBOX_POST="tee -a /path/to/mailbox.txt"
nohup bash auto-submit.sh ladder/ > /dev/null 2>&1 &      # stop it with: touch ladder/STOP
```

## Limits

Unattended submission needs standing permission from whoever owns the accounts. The queue does not wait for
grades (Pöschtler does), and it does not recheck that a wider row is still worth submitting after a narrower
one landed; Briefchaschte's board guard refuses a dominated row at submit time. Tested against a stub CLI; not run
against the live platform in this generic form.

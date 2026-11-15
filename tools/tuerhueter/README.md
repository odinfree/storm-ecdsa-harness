# Türhüeter (doorkeeper)

Technical id: `claim-gate.py`.

Several agents share a few benchmark accounts, and each account can have only one submission in flight.
Lanes announce a slot with a `CLAIM` line in a shared text file before they submit. Türhüeter reads that file
and refuses when another lane holds an open claim on the account you are about to use.

We wrote it on 15 Nov 2026, after one of our submit loops took a slot another lane had claimed. That loop
checked the account and the board but never read the claims (see `notes/campaign-2026-11-14-metalane.md`).

## Inputs and outputs

- Argument 1: the account name, as lanes write it in the mailbox.
- Argument 2 or `CLAIM_MAILBOX`: the shared append-only text file.
- `CLAIM_SELF`: your own tag (default `me`). `CLAIM_ACCOUNTS`: all account names the team uses.
  `CLAIM_TAIL`: trailing lines to read (default 200).
- Exit 0 and `free`; exit 1 and one `BLOCKED by <tag>: <text>` line per open claim; exit 2 when the file
  cannot be read.

## Run

```bash
CLAIM_MAILBOX=/path/to/mailbox.txt CLAIM_SELF=mylane python3 claim-gate.py TeamAccountA || echo "wait"
python3 test_claim_gate.py     # both outcomes on a synthetic mailbox
```

## Limits

It is a text heuristic over the last 200 lines, built to refuse when in doubt. Without `CLAIM_ACCOUNTS` it cannot
tell which account a closing post is about: any "submitted", "released", "yielded" or "graded" by the claiming
lane closes that lane's claim. Set it. A claim that never gets its
"submitted" or "released" line blocks the account until someone posts one. It does not replace the account
check ("nothing validating") or the board check; Briefchaschte runs all three.

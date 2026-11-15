# Briefchaschte (letterbox)

Technical id: `submit-dir.sh`.

Submits one prepared row package to ecdsa.fail through the `ecdsafail` CLI, after about thirty guards. Any
failed guard prints `REFUSED: <reason>` and exits 1; nothing is sent. With `DRYRUN=1` it runs every guard
and stops before the submit.

## What it checks

- **Approval binding.** `approved` holds the sha256 of the note and the dependency file, the row commit, its
  git tree and the model line. Any edit after approval refuses. This is worth what the approval is worth: write
  the file after a review, by a reviewer. Pöschtler and Drängeler write it themselves unless told otherwise.
- **Limits.** An account that has never submitted cannot be identified from its submission list and is refused:
  submit its first row by hand.
- **Artifact binding.** `CLAIM` (Toffoli, ops sha256, dev commit) against `verified-sha`; the row commit and
  the ops sha must appear in the note.
- **Note hygiene.** No placeholder, no local path, no inherited notice-block marker, minimum size, at most
  20 dependencies.
- **Checkout.** HEAD is the row commit, no modified tracked files, nothing untracked or ignored under
  `src/point_add`, and the clone does not use git alternates.
- **Account.** The authenticated user is the expected one and has nothing validating; no other lane holds an
  open claim on it (Türhüeter).
- **Board.** A fresh full board read shows no row at width <= W at or below our Toffoli count.

## Inputs

`submit-dir.sh <pkgdir> <W> <account-label> <expected-username>`. The package layout and the environment
variables (`ACCOUNTS_DIR`, `CLAIM_MAILBOX`, `IGNORE_CLAIMS`, `DRYRUN`, `MIN_NOTE_BYTES`, `MAX_DEPS`) are in
the script header. Output: the CLI's JSON response on stdout, the pre-submit board read in the package.

## Run

```bash
export ACCOUNTS_DIR=$HOME/accounts CLAIM_MAILBOX=/path/to/mailbox.txt CLAIM_SELF=mylane
DRYRUN=1 bash submit-dir.sh pkg/w763 763 main TeamAccountA
flock -n "$SUBMIT_LOCK" bash submit-dir.sh pkg/w763 763 main TeamAccountA > pkg/w763/submit-response.json
```

It needs `ecdsafail`, `git`, `python3` and `shasum`. Notizbüechli writes the package; Pöschtler and Drängeler
call this script.

The campaign ran the version with our paths and account names in it. This generic form was tested end to end
against a stub CLI (refusals, claim gate, dry run, submit) and has not been run against the live platform.

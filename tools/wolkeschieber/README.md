# Wolkeschieber (cloud pusher)

Technical id: `colab-lane`.

Runs one job on a Google Colab runtime until it is done, then downloads the results and stops the runtime.
It is a supervisor around Google's `colab` CLI: it validates every flag before anything billable starts,
uploads files, launches the command detached on the VM, polls and streams the log, enforces a hard time
limit, and stops the runtime on every exit path (three tries, then it prints the exact recovery command).

## Inputs and outputs

```
colab-lane [-g GPU] [-m] [-t MAX_MIN] [-p POLL_S] [-n NAME] [-u LOCAL_FILE]... [-d REMOTE_PATH]... -- CMD
```

`-g` G4 (default), H100, A100, L4, T4 or cpu; `-m` high-RAM shape; `-t` hard limit in minutes; `-u` uploads
into `/content/` (the Colab VM's working directory); `-d` downloads into `./colab-out/<name>/` when the job
ends. The log streams to `./colab-out/<name>/stream.log`. Exit codes are in the script header: the job's own
code, 124 for the time limit, 98 for a runtime that is confirmed gone, 130 when interrupted.

## Run

```bash
colab-lane -n gate-763 -g A100 -m -t 150 -u tree.tgz -u job.sh -d /content/result.json -- 'bash /content/job.sh'
```

Always pass `-t`. Start it through Hofhund when the calling session may die before the job ends.

## Limits

- It needs the `colab` CLI signed in by a person; an expired sign-in exits 7 and keeps the runtime.
- macOS specifics: `caffeinate` and an `osascript` notification, both skipped silently elsewhere.
- It redraws a runtime whose proxy host is in europe-west4, because those were unreachable from our network
  in November 2026. Remove that block if your network differs.
- Downloads happen when the job ends. A runtime Colab takes away takes `/content` with it, so print progress
  to stdout.

The `colab-lane` skill in `skills/` holds the operating notes: spend, session rules, checkpointing, failure
semantics.

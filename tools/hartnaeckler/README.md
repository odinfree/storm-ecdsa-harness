# Hartnäckler (stubborn one)

Technical ids: `retry.sh`, `retry2.sh`, `retry3.sh`, merged here into `retry-launch.sh`.

Keeps asking for a cloud runtime until it gets one. Colab answers "Service Unavailable" when a GPU class is
out of capacity, and refuses a new session when the account already has its limit of them running, whoever
started them. Both look the same from the CLI and both clear on their own.

## Run

```bash
bash retry-launch.sh run-s8 900 202611150300 -- bash launch.sh S "17 5" A100 1 spec.txt
```

tries every 15 minutes until 03:00 UTC on 15 Nov 2026. Output: one line per try, then `LAUNCHED ...` (exit 0)
or `STOPPED at deadline, no launch` (exit 1).

## Rules we learned

- Give every loop a deadline. The three campaign versions were: four tries, forever, and until a clock time.
  Only the last one was safe to leave alone.
- One loop per job. Two loops for the same job can both win and start two runtimes.
- Say in the team channel what the loop is asking for, each time (`ANNOUNCE`). A lane that silently polls for
  the last free slot looks, to everyone else, like the reason they cannot get one.
- A refusal costs nothing. A session cap that others are waiting on is a reason to ask in the channel, not
  to shorten the retry interval.

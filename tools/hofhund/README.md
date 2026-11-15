# Hofhund (yard dog)

Technical ids: `colab-detached.sh`, `colab-watchdog.sh`.

Two guards for a paid cloud runtime that an agent session started.

`colab-detached.sh` puts the `colab-lane` supervisor in its own process session. On 13 Nov 2026 an agent
session ended while its supervisor was still a child of it; the supervisor died with it and the runtime
kept billing. The script refuses to start a job without `-t`.

`colab-watchdog.sh` kills `colab` CLI calls that hang. We saw one print "Connection was lost" and then never
return; the supervisor waited on it, stopped polling, and so never reached its own time limit.

## Run

```bash
bash colab-detached.sh run1/ run1/lane.log -- -g G4 -t 150 -n gate-763 -u tree.tgz -d /content/out.tgz -- 'bash /content/job.sh'
nohup bash colab-watchdog.sh gate-763 "$(cat run1/lane.log.pid)" > run1/watchdog.log 2>&1 &
cat run1/lane.log.rc      # appears when the supervisor has exited
```

## Outputs

`<logfile>` (the supervisor's output), `<logfile>.pid`, `<logfile>.rc`; the watchdog prints one line per kill.

## Limits

The current `colab-lane` wraps every CLI call in `timeout`, so the watchdog is the second line of defence.
Keep its limit above the supervisor's own call timeout when the supervisor counts consecutive failed polls:
an earlier supervisor needed three in a row to declare a runtime lost, the watchdog kept resetting that
count, and the supervisor polled a dead runtime for hours. The process match depends on the state-file
naming of `colab-lane`; check it with `pgrep -fl colab` on your machine.

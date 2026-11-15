#!/bin/bash
# board-age.sh <outdir> [max_seconds=1800]: exit 0 when the last good board read is younger than max_seconds, else 1.
# Put it in front of every decision that reads board-latest.tsv.
R=${1:?outdir}; MAX=${2:-1800}
[ -s "$R/board-latest.time" ] || { echo "no snapshot"; exit 1; }
AGE=$(python3 -c "
import datetime,sys
t=datetime.datetime.strptime(open(sys.argv[1]).read().strip(),'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
print(int((datetime.datetime.now(datetime.timezone.utc)-t).total_seconds()))" "$R/board-latest.time") || exit 1
echo "snapshot age ${AGE}s"; [ "$AGE" -le "$MAX" ]

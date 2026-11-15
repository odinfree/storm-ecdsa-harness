"""Find conflicting host requirements within the same enabled baseline-passing use."""
import argparse
import csv
import json
import sys
from pathlib import Path

FIELDS = ("use", "frame", "shot", "enabled", "baseline_ok", "basis", "required")


def audit(stream):
    rows = csv.DictReader(stream, strict=True)
    if rows.fieldnames is None or sorted(rows.fieldnames) != sorted(FIELDS):
        raise ValueError("expected header: " + ",".join(FIELDS))

    widths = {}
    observations = {}
    eligible = 0
    witness = None
    for row in rows:
        where = f"line {rows.line_num}"
        if None in row or any(row[key] is None for key in FIELDS):
            raise ValueError(f"{where}: wrong column count")
        if any(not row[key].strip() for key in ("use", "frame", "shot")):
            raise ValueError(f"{where}: missing use, frame or shot ID")
        if any(row[key] not in {"0", "1"} for key in ("enabled", "baseline_ok", "required")):
            raise ValueError(f"{where}: flags and required bit must be 0 or 1")
        basis = row["basis"]
        if set(basis) - {"0", "1"}:
            raise ValueError(f"{where}: expected an ordered binary projection")
        use = (row["use"], row["frame"])
        if widths.setdefault(use, len(basis)) != len(basis):
            raise ValueError(f"{where}: basis width changed within use/frame")
        if row["enabled"] == "0" or row["baseline_ok"] == "0":
            continue
        eligible += 1
        first_bit, first_shot = observations.setdefault((*use, basis), (row["required"], row["shot"]))
        if first_bit != row["required"]:
            if first_shot == row["shot"]:
                raise ValueError(f"{where}: conflicting records for the same shot and use")
            if witness is None:
                witness = {"use": use[0], "frame": use[1], "basis": basis,
                           "shots": {first_bit: first_shot, row["required"]: row["shot"]}}
    if not eligible:
        raise ValueError("no enabled baseline-passing observations")
    return {"eligible": eligible, "distinct_projections": len(observations), "witness": witness}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()
    try:
        with args.csv_file.open(encoding="utf-8-sig", newline="") as stream:
            report = audit(stream)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(2, f"{error}\n")
    print(json.dumps(report))
    return int(report["witness"] is not None)


if __name__ == "__main__":
    sys.exit(main())

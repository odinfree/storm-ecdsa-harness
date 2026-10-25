#!/usr/bin/env python3
"""Search Lean sources and verify exact names with one pinned Lean process."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import signal
import subprocess
import sys
from typing import Any


SCHEMA = "fast-lean-proof-loop-symbol-check/v1"


class SymbolError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def search_sources(source: pathlib.Path, query: str | None, limit: int) -> list[dict[str, Any]]:
    if query is None:
        return []
    try:
        pattern = re.compile(query)
    except re.error as exc:
        raise SymbolError(f"invalid search regex: {exc}") from exc
    matches: list[dict[str, Any]] = []
    for path in sorted(source.rglob("*.lean")):
        for line_number, line in enumerate(path.read_text().splitlines(), start=1):
            if pattern.search(line):
                matches.append({
                    "path": str(path), "line": line_number, "text": line.strip()[:500],
                })
                if len(matches) >= limit:
                    return matches
    return matches


def run_with_timeout(
    command: list[str], cwd: pathlib.Path, input_text: str, timeout_seconds: int
) -> tuple[int, str, str, bool]:
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(input=input_text, timeout=timeout_seconds)
        return process.returncode, stdout, stderr, False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout, stderr = process.communicate()
        return 124, stdout, stderr, True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=pathlib.Path, required=True)
    parser.add_argument("--source-root", type=pathlib.Path, required=True)
    parser.add_argument("--query")
    parser.add_argument("--import", dest="imports", action="append", default=[])
    parser.add_argument("--name", dest="names", action="append", default=[])
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--lake", default="lake")
    parser.add_argument("--output", type=pathlib.Path)
    try:
        args = parser.parse_args()
        project = args.project_root.expanduser().resolve(strict=True)
        source = args.source_root.expanduser()
        if not source.is_absolute():
            source = project / source
        source = source.resolve(strict=True)
        if source != project and project not in source.parents:
            raise SymbolError("source root must be inside project root")
        if args.limit <= 0:
            raise SymbolError("limit must be positive")
        if args.timeout_seconds <= 0:
            raise SymbolError("timeout-seconds must be positive")
        candidates = search_sources(source, args.query, args.limit)
        receipt: dict[str, Any] = {
            "schema": SCHEMA,
            "project_root": str(project),
            "source_root": str(source.relative_to(project)),
            "query": args.query,
            "search_candidates": candidates,
            "imports": args.imports,
            "requested_names": args.names,
            "verification": "NOT_RUN",
        }
        return_code = 0
        if args.names:
            if not args.imports:
                raise SymbolError("at least one --import is required when verifying names")
            program = "".join(f"import {name}\n" for name in args.imports)
            program += "".join(f"#check {name}\n" for name in args.names)
            return_code, stdout, stderr, timed_out = run_with_timeout(
                [args.lake, "env", "lean", "--stdin"], project, program, args.timeout_seconds
            )
            if timed_out:
                lean_version = "NOT_CHECKED_AFTER_TIMEOUT"
            else:
                try:
                    version = subprocess.run(
                        [args.lake, "env", "lean", "--version"], cwd=project,
                        check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        timeout=min(args.timeout_seconds, 30),
                    )
                    lean_version = version.stdout.strip()
                except subprocess.TimeoutExpired:
                    lean_version = "VERSION_CHECK_TIMEOUT"
            receipt.update({
                "verification": "TIMEOUT" if timed_out else ("PASS" if return_code == 0 else "FAIL"),
                "program_sha256": sha256(program.encode()),
                "returncode": return_code,
                "timeout_seconds": args.timeout_seconds,
                "stdout": stdout,
                "stderr": stderr,
                "lean_version": lean_version,
                "verified_names": args.names if return_code == 0 else [],
            })
        if args.output:
            output = args.output.expanduser().resolve()
            if output.exists():
                raise SymbolError(f"refusing to overwrite existing output: {output}")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(canonical(receipt))
            receipt_path = str(output)
        else:
            receipt_path = None
        print(json.dumps({
            "status": receipt["verification"], "output": receipt_path,
            "candidate_count": len(candidates), "verified_names": receipt.get("verified_names", []),
        }, sort_keys=True))
        return return_code
    except (SymbolError, OSError, UnicodeDecodeError) as exc:
        print(f"Lean symbol check failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Snapshot the exact local import closure of an accepted Lean proof."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from collections import Counter
from fractions import Fraction
from typing import Any


SCHEMA = "accepted-proof-snapshot/v1"


class SnapshotError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def strip_comments(text: str) -> str:
    """Remove Lean line and nested block comments while preserving newlines."""
    out: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(text):
        pair = text[index:index + 2]
        char = text[index]
        if depth:
            if pair == "/-":
                depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
            continue
        if not in_string and pair == "/-":
            depth = 1
            out.extend("  ")
            index += 2
            continue
        if not in_string and pair == "--":
            while index < len(text) and text[index] != "\n":
                out.append(" ")
                index += 1
            continue
        out.append(char)
        if char == '"' and not escaped:
            in_string = not in_string
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
        index += 1
    if depth:
        raise SnapshotError("unterminated Lean block comment")
    return "".join(out)


def imports(text: str) -> list[str]:
    return re.findall(r"^\s*import\s+([^\s]+)", strip_comments(text), flags=re.MULTILINE)


def module_name(project_root: pathlib.Path, path: pathlib.Path) -> str:
    return ".".join(path.relative_to(project_root).with_suffix("").parts)


def git_state(project_root: pathlib.Path) -> dict[str, Any]:
    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(project_root), *args], check=False, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    inside = git("rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return {"is_git_worktree": False, "head": None, "dirty": None}
    head = git("rev-parse", "HEAD")
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    if head.returncode or status.returncode:
        raise SnapshotError("failed to read Git state")
    return {
        "is_git_worktree": True,
        "head": head.stdout.strip(),
        "dirty": bool(status.stdout),
        "status_sha256": sha256(status.stdout.encode()),
    }


def exact_fraction(path: pathlib.Path, label: str) -> Fraction:
    value = path.read_text().strip()
    if not re.fullmatch(r"[0-9]+(?:/[1-9][0-9]*)?", value):
        raise SnapshotError(f"{label} is not an exact non-negative rational: {value!r}")
    return Fraction(value)


def file_record(project_root: pathlib.Path, path: pathlib.Path) -> dict[str, Any]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SnapshotError(f"Lean source is not UTF-8: {path}: {exc}") from exc
    cleaned = strip_comments(text)
    literals = Counter(
        token.replace("_", "")
        for token in re.findall(r"(?<![A-Za-z0-9_])(?:0x[0-9A-Fa-f_]+|[0-9][0-9_]*)(?![A-Za-z0-9_])", cleaned)
    )
    bindings: list[dict[str, Any]] = []
    binding_pattern = re.compile(
        r"^\s*(?:private\s+)?(?:def|abbrev)\s+([A-Za-z_][A-Za-z0-9_']*)[^\n]*?:=\s*([0-9][0-9_]*)\b"
    )
    for line_number, line in enumerate(cleaned.splitlines(), start=1):
        match = binding_pattern.match(line)
        if match:
            bindings.append(
                {"name": match.group(1), "value": int(match.group(2).replace("_", "")), "line": line_number}
            )
    return {
        "path": path.relative_to(project_root).as_posix(),
        "module": module_name(project_root, path),
        "sha256": sha256(raw),
        "bytes": len(raw),
        "line_count": len(text.splitlines()),
        "imports": imports(text),
        "integer_literals": dict(sorted(
            literals.items(),
            key=lambda item: (
                int(item[0], 16) if item[0].lower().startswith("0x") else int(item[0], 10),
                item[0],
            ),
        )),
        "simple_integer_bindings": bindings,
    }


def build_snapshot(project_root: pathlib.Path, entry: pathlib.Path, submission_dir: pathlib.Path) -> dict[str, Any]:
    root = project_root.expanduser().resolve(strict=True)
    entry_abs = (root / entry).resolve(strict=True)
    submission_abs = (root / submission_dir).resolve(strict=True)
    if root not in entry_abs.parents or root not in submission_abs.parents:
        raise SnapshotError("entry and submission directory must stay inside project root")
    source_files = sorted(submission_abs.rglob("*.lean"))
    module_to_path = {module_name(root, path): path for path in source_files}
    entry_module = module_name(root, entry_abs)
    if entry_module not in module_to_path:
        raise SnapshotError("entry is not a Lean file inside the submission directory")
    closure: set[str] = set()
    pending = [entry_module]
    text_cache: dict[str, str] = {}
    while pending:
        module = pending.pop()
        if module in closure:
            continue
        closure.add(module)
        path = module_to_path[module]
        text = text_cache.setdefault(module, path.read_text())
        for dependency in imports(text):
            if dependency in module_to_path and dependency not in closure:
                pending.append(dependency)
    records = [file_record(root, module_to_path[module]) for module in sorted(closure)]
    score = exact_fraction(submission_abs / "score.txt", "score")
    radius = exact_fraction(submission_abs / "radius.txt", "radius")
    if score.denominator != 1:
        raise SnapshotError("score must be an integer number of centibits")
    solution_text = entry_abs.read_text()
    direct_imports = imports(solution_text)
    internal = [name for name in direct_imports if name in module_to_path]
    manifest_material = "".join(f"{item['path']}\0{item['sha256']}\n" for item in records).encode()
    return {
        "schema": SCHEMA,
        "classification": "ACCEPTED_SOURCE_BOUND_EXPLORATION",
        "project_root": str(root),
        "entry": entry_abs.relative_to(root).as_posix(),
        "submission_dir": submission_abs.relative_to(root).as_posix(),
        "git": git_state(root),
        "accepted_score_centibits": score.numerator,
        "accepted_radius": f"{radius.numerator}/{radius.denominator}",
        "proof_root": internal[-1] if internal else "UNKNOWN",
        "direct_imports": direct_imports,
        "closure_file_count": len(records),
        "closure_manifest_sha256": sha256(manifest_material),
        "files": records,
        "warning": "Literal inventory is lexical evidence, not a complete semantic model.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=pathlib.Path, required=True)
    parser.add_argument("--entry", type=pathlib.Path, required=True)
    parser.add_argument("--submission-dir", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    try:
        args = parser.parse_args()
        snapshot = build_snapshot(args.project_root, args.entry, args.submission_dir)
        output = args.output.expanduser().resolve()
        if output.exists():
            raise SnapshotError(f"refusing to overwrite existing snapshot: {output}")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(canonical(snapshot))
        print(json.dumps({
            "status": "PASS", "output": str(output),
            "closure_files": snapshot["closure_file_count"],
            "manifest_sha256": snapshot["closure_manifest_sha256"],
        }, sort_keys=True))
        return 0
    except (SnapshotError, OSError, ValueError) as exc:
        print(f"accepted proof snapshot failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Plan or run dependency-aware incremental Lean builds."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time
from collections import defaultdict
from typing import Any


PLAN_SCHEMA = "fast-lean-proof-loop-plan/v1"
RUN_SCHEMA = "fast-lean-proof-loop-run/v1"


class LoopError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def strip_comments(text: str) -> str:
    result: list[str] = []
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
                result.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                result.extend("  ")
                index += 2
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
            continue
        if not in_string and pair == "/-":
            depth = 1
            result.extend("  ")
            index += 2
            continue
        if not in_string and pair == "--":
            while index < len(text) and text[index] != "\n":
                result.append(" ")
                index += 1
            continue
        result.append(char)
        if char == '"' and not escaped:
            in_string = not in_string
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
        index += 1
    if depth:
        raise LoopError("unterminated Lean block comment")
    return "".join(result)


def parse_imports(text: str) -> list[str]:
    return re.findall(r"^\s*import\s+([^\s]+)", strip_comments(text), flags=re.MULTILINE)


def module_for(project_root: pathlib.Path, path: pathlib.Path) -> str:
    return ".".join(path.relative_to(project_root).with_suffix("").parts)


def resolve_changed(project_root: pathlib.Path, changed: list[pathlib.Path]) -> list[pathlib.Path]:
    result: list[pathlib.Path] = []
    for item in changed:
        candidate = item.expanduser()
        if not candidate.is_absolute():
            candidate = project_root / candidate
        candidate = candidate.resolve(strict=True)
        if project_root not in candidate.parents or candidate.suffix != ".lean":
            raise LoopError(f"changed file must be a Lean file inside project root: {item}")
        result.append(candidate)
    if not result:
        raise LoopError("at least one --changed Lean file is required")
    return sorted(set(result))


def git_state(project_root: pathlib.Path) -> dict[str, Any]:
    def git(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(project_root), *args], check=False, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    inside = git("rev-parse", "--is-inside-work-tree")
    if inside.returncode or inside.stdout.strip() != "true":
        return {"is_git_worktree": False, "head": None, "dirty": None}
    head = git("rev-parse", "HEAD")
    status = git("status", "--porcelain=v1", "--untracked-files=all")
    if head.returncode or status.returncode:
        raise LoopError("failed to inspect Git state")
    return {
        "is_git_worktree": True,
        "head": head.stdout.strip(),
        "dirty": bool(status.stdout),
        "status_sha256": sha256(status.stdout.encode()),
    }


def build_plan(project_root: pathlib.Path, source_root: pathlib.Path, changed: list[pathlib.Path]) -> dict[str, Any]:
    project = project_root.expanduser().resolve(strict=True)
    source = source_root.expanduser()
    if not source.is_absolute():
        source = project / source
    source = source.resolve(strict=True)
    if source != project and project not in source.parents:
        raise LoopError("source root must be inside project root")
    files = sorted(source.rglob("*.lean"))
    if not files:
        raise LoopError(f"no Lean files under source root: {source}")
    module_to_path = {module_for(project, path): path for path in files}
    path_to_module = {path: module for module, path in module_to_path.items()}
    changed_paths = resolve_changed(project, changed)
    missing = [path for path in changed_paths if path not in path_to_module]
    if missing:
        raise LoopError("changed files are outside indexed source root: " + ", ".join(str(path) for path in missing))
    dependencies: dict[str, set[str]] = {}
    manifest: list[dict[str, Any]] = []
    external_imports: set[str] = set()
    for module, path in sorted(module_to_path.items()):
        raw = path.read_bytes()
        names = parse_imports(raw.decode("utf-8"))
        dependencies[module] = {name for name in names if name in module_to_path}
        external_imports.update(name for name in names if name not in module_to_path)
        manifest.append({
            "module": module,
            "path": path.relative_to(project).as_posix(),
            "sha256": sha256(raw),
            "imports": names,
        })
    reverse: dict[str, set[str]] = defaultdict(set)
    for module, deps in dependencies.items():
        for dependency in deps:
            reverse[dependency].add(module)
    affected = {path_to_module[path] for path in changed_paths}
    pending = list(affected)
    while pending:
        dependency = pending.pop()
        for consumer in reverse.get(dependency, set()):
            if consumer not in affected:
                affected.add(consumer)
                pending.append(consumer)
    order: list[str] = []
    temporary: set[str] = set()
    permanent: set[str] = set()

    def visit(module: str) -> None:
        if module in permanent:
            return
        if module in temporary:
            raise LoopError(f"local import cycle detected at {module}")
        temporary.add(module)
        for dependency in sorted(dependencies[module] & affected):
            visit(dependency)
        temporary.remove(module)
        permanent.add(module)
        order.append(module)

    for module in sorted(affected):
        visit(module)
    roots = sorted(module for module in affected if not (reverse.get(module, set()) & affected))
    manifest_material = "".join(f"{item['path']}\0{item['sha256']}\n" for item in manifest).encode()
    return {
        "schema": PLAN_SCHEMA,
        "project_root": str(project),
        "source_root": source.relative_to(project).as_posix(),
        "git": git_state(project),
        "source_manifest_sha256": sha256(manifest_material),
        "indexed_module_count": len(module_to_path),
        "changed_files": [path.relative_to(project).as_posix() for path in changed_paths],
        "changed_modules": sorted(path_to_module[path] for path in changed_paths),
        "affected_modules_dependency_order": order,
        "affected_module_count": len(order),
        "build_targets": roots,
        "external_import_count": len(external_imports),
        "warning": "Generated, conditional, or out-of-root imports require an explicit reviewed build target.",
    }


def write_new(path: pathlib.Path, value: dict[str, Any]) -> pathlib.Path:
    resolved = path.expanduser().resolve()
    if resolved.exists():
        raise LoopError(f"refusing to overwrite existing output: {resolved}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_bytes(canonical(value))
    return resolved


def plan_command(args: argparse.Namespace) -> int:
    plan = build_plan(args.project_root, args.source_root, args.changed)
    output = write_new(args.output, plan)
    print(json.dumps({
        "status": "PASS", "output": str(output),
        "affected_modules": plan["affected_module_count"], "build_targets": plan["build_targets"],
    }, sort_keys=True))
    return 0


def run_command(args: argparse.Namespace) -> int:
    plan = build_plan(args.project_root, args.source_root, args.changed)
    command = [args.lake, "build", *plan["build_targets"]]
    result: dict[str, Any] = {
        "schema": RUN_SCHEMA,
        "status": "DRY_RUN" if args.dry_run else "RUNNING",
        "plan": plan,
        "command": command,
        "dry_run": args.dry_run,
    }
    return_code = 0
    if not args.dry_run:
        start = time.monotonic_ns()
        proc = subprocess.run(
            command, cwd=plan["project_root"], check=False, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        duration_ms = (time.monotonic_ns() - start) // 1_000_000
        result.update({
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "returncode": proc.returncode,
            "duration_ms": duration_ms,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "stdout_sha256": sha256(proc.stdout.encode()),
            "stderr_sha256": sha256(proc.stderr.encode()),
        })
        return_code = proc.returncode
    output = write_new(args.output, result)
    print(json.dumps({"status": result["status"], "output": str(output), "command": command}, sort_keys=True))
    return return_code


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    for name, handler in (("plan", plan_command), ("run", run_command)):
        command = sub.add_parser(name)
        command.add_argument("--project-root", type=pathlib.Path, required=True)
        command.add_argument("--source-root", type=pathlib.Path, required=True)
        command.add_argument("--changed", type=pathlib.Path, action="append", required=True)
        command.add_argument("--output", type=pathlib.Path, required=True)
        if name == "run":
            command.add_argument("--lake", default="lake")
            command.add_argument("--dry-run", action="store_true")
        command.set_defaults(handler=handler)
    return result


def main() -> int:
    try:
        args = parser().parse_args()
        return args.handler(args)
    except (LoopError, OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"fast Lean loop failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

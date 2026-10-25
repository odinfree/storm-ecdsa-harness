#!/usr/bin/env python3
"""Capture and replay a direct-predecessor better.codes proof delta."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from fractions import Fraction
from typing import Any


# Frozen schema name from before the skill was renamed; kept so existing records still validate.
SCHEMA = "better-codes-frontier-archaeology/v1"
DEFAULT_SUBMISSION = "ProximityPrize/SubmissionLower"


class CaptureError(RuntimeError):
    pass


def run_git(repo: pathlib.Path, *args: str, ok: tuple[int, ...] = (0,)) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode not in ok:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise CaptureError(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def resolve_commit(repo: pathlib.Path, ref: str) -> str:
    return run_git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}").strip()


def show_bytes(repo: pathlib.Path, commit: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise CaptureError(
            f"git show {commit}:{path} failed: {proc.stderr.decode(errors='replace').strip()}"
        )
    return proc.stdout


def show_text(repo: pathlib.Path, commit: str, path: str) -> str:
    try:
        return show_bytes(repo, commit, path).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CaptureError(f"expected UTF-8 text at {commit}:{path}: {exc}") from exc


def parse_score(value: str, label: str) -> int:
    stripped = value.strip()
    if not re.fullmatch(r"[0-9]+", stripped):
        raise CaptureError(f"{label} is not a non-negative integer: {stripped!r}")
    return int(stripped)


def parse_radius(value: str, label: str) -> Fraction:
    stripped = value.strip()
    if not re.fullmatch(r"[0-9]+(?:/[1-9][0-9]*)?", stripped):
        raise CaptureError(f"{label} is not an exact non-negative rational: {stripped!r}")
    result = Fraction(stripped)
    if result < 0:
        raise CaptureError(f"{label} is negative")
    return result


def imports(text: str) -> list[str]:
    return re.findall(r"^\s*import\s+([^\s]+)", text, flags=re.MULTILINE)


def proof_root(solution_text: str, submission_module_prefix: str) -> str:
    direct = imports(solution_text)
    internal = [name for name in direct if name.startswith(submission_module_prefix)]
    return internal[-1] if internal else "UNKNOWN"


def commit_metadata(repo: pathlib.Path, commit: str) -> dict[str, str]:
    raw = run_git(
        repo,
        "show",
        "-s",
        "--date=iso-strict",
        "--format=%H%x00%T%x00%aI%x00%cI%x00%an%x00%s",
        commit,
    ).rstrip("\n")
    fields = raw.split("\x00")
    if len(fields) != 6:
        raise CaptureError(f"unexpected commit metadata for {commit}")
    keys = ("commit", "tree", "authored_at", "committed_at", "author", "subject")
    if len(keys) != len(fields):
        raise CaptureError(f"unexpected commit metadata field count for {commit}")
    return dict(zip(keys, fields))


def state_at(repo: pathlib.Path, commit: str, submission_dir: str) -> dict[str, Any]:
    score_path = f"{submission_dir}/score.txt"
    radius_path = f"{submission_dir}/radius.txt"
    solution_path = f"{submission_dir}/Solution.lean"
    solution_bytes = show_bytes(repo, commit, solution_path)
    solution_text = solution_bytes.decode("utf-8")
    module_prefix = submission_dir.replace("/", ".") + "."
    score = parse_score(show_text(repo, commit, score_path), score_path)
    radius = parse_radius(show_text(repo, commit, radius_path), radius_path)
    return {
        "score_centibits": score,
        "score_decimal": f"{score // 100}.{score % 100:02d}",
        "radius": f"{radius.numerator}/{radius.denominator}",
        "radius_numerator": radius.numerator,
        "radius_denominator": radius.denominator,
        "solution_blob": run_git(repo, "rev-parse", f"{commit}:{solution_path}").strip(),
        "solution_sha256": sha256_bytes(solution_bytes),
        "direct_imports": imports(solution_text),
        "proof_root": proof_root(solution_text, module_prefix),
        "submission_tree": run_git(repo, "rev-parse", f"{commit}:{submission_dir}").strip(),
    }


def adjacency(repo: pathlib.Path, older: str, newer: str, score_path: str) -> dict[str, Any]:
    ancestor = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", older, newer],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if ancestor.returncode != 0:
        raise CaptureError("selected predecessor is not an ancestor of the accepted commit")
    commits = [
        line
        for line in run_git(repo, "log", "--format=%H", f"{older}..{newer}", "--", score_path).splitlines()
        if line
    ]
    if commits != [newer]:
        rendered = ", ".join(value[:12] for value in commits) or "none"
        raise CaptureError(
            "selected refs are not adjacent score promotions; "
            f"score-changing commits in range: {rendered}"
        )
    return {
        "ancestor_check": True,
        "score_changing_commits_between": commits,
        "newer_is_next_score_promotion": True,
    }


def changed_files(repo: pathlib.Path, older: str, newer: str, submission_dir: str) -> list[dict[str, Any]]:
    raw = run_git(repo, "diff", "--numstat", "--find-renames", older, newer, "--", submission_dir)
    statuses_raw = run_git(
        repo, "diff", "--name-status", "--find-renames", older, newer, "--", submission_dir
    )
    status_by_path: dict[str, str] = {}
    for line in statuses_raw.splitlines():
        fields = line.split("\t")
        if len(fields) >= 2:
            status = fields[0]
            status_by_path[fields[-1]] = status
    result: list[dict[str, Any]] = []
    for line in raw.splitlines():
        fields = line.split("\t")
        if len(fields) < 3:
            continue
        added, deleted, path = fields[0], fields[1], fields[-1]
        result.append(
            {
                "path": path,
                "status": status_by_path.get(path, "UNKNOWN"),
                "added_lines": None if added == "-" else int(added),
                "deleted_lines": None if deleted == "-" else int(deleted),
            }
        )
    return sorted(result, key=lambda item: item["path"])


def note_binding(path: pathlib.Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    resolved = path.expanduser().resolve(strict=True)
    data = resolved.read_bytes()
    return {
        "path": str(resolved),
        "sha256": sha256_bytes(data),
        "bytes": len(data),
    }


def build_receipt(
    repo: pathlib.Path,
    older_ref: str,
    newer_ref: str,
    submission_dir: str,
    note_file: pathlib.Path | None,
) -> dict[str, Any]:
    repo = repo.expanduser().resolve(strict=True)
    if run_git(repo, "rev-parse", "--is-inside-work-tree").strip() != "true":
        raise CaptureError(f"not a Git worktree: {repo}")
    older = resolve_commit(repo, older_ref)
    newer = resolve_commit(repo, newer_ref)
    if older == newer:
        raise CaptureError("predecessor and accepted commit resolve to the same commit")
    score_path = f"{submission_dir}/score.txt"
    pair_adjacency = adjacency(repo, older, newer, score_path)
    old_state = state_at(repo, older, submission_dir)
    new_state = state_at(repo, newer, submission_dir)
    if new_state["score_centibits"] <= old_state["score_centibits"]:
        raise CaptureError("accepted score did not increase across the selected pair")
    old_radius = Fraction(old_state["radius_numerator"], old_state["radius_denominator"])
    new_radius = Fraction(new_state["radius_numerator"], new_state["radius_denominator"])
    delta_radius = new_radius - old_radius
    benchmark_dir = str(pathlib.PurePosixPath(submission_dir).parent / "Benchmark")
    benchmark_old = run_git(repo, "rev-parse", f"{older}:{benchmark_dir}").strip()
    benchmark_new = run_git(repo, "rev-parse", f"{newer}:{benchmark_dir}").strip()
    if benchmark_old != benchmark_new:
        raise CaptureError(
            "benchmark contract tree changed across the selected promotion; "
            "rebind the benchmark and review the comparison explicitly"
        )
    files = changed_files(repo, older, newer, submission_dir)
    return {
        "schema": SCHEMA,
        "classification": "CONTAMINATED_INCUMBENT_ARCHAEOLOGY",
        "inputs": {
            "repo": str(repo),
            "older_ref": older_ref,
            "newer_ref": newer_ref,
            "submission_dir": submission_dir,
            "note_file": None if note_file is None else str(note_file.expanduser().resolve()),
        },
        "predecessor": {**commit_metadata(repo, older), **old_state},
        "accepted": {**commit_metadata(repo, newer), **new_state},
        "adjacency": pair_adjacency,
        "benchmark_contract": {
            "path": benchmark_dir,
            "predecessor_tree": benchmark_old,
            "accepted_tree": benchmark_new,
            "unchanged": benchmark_old == benchmark_new,
        },
        "delta": {
            "score_centibits": new_state["score_centibits"] - old_state["score_centibits"],
            "radius": f"{delta_radius.numerator}/{delta_radius.denominator}",
            "proof_root_changed": old_state["proof_root"] != new_state["proof_root"],
            "imports_added": sorted(set(new_state["direct_imports"]) - set(old_state["direct_imports"])),
            "imports_removed": sorted(set(old_state["direct_imports"]) - set(new_state["direct_imports"])),
            "changed_files": files,
            "changed_file_count": len(files),
        },
        "public_note": note_binding(note_file),
        "transfer_review": {
            "status": "UNASSESSED",
            "claimed_mechanism": None,
            "supporting_anchors": [],
            "inherited_dependencies": [],
            "accompanying_churn": [],
            "falsifier": None,
            "transfer_verdict": "UNRESOLVED",
            "target_tree_rebase": "NOT_ATTEMPTED",
        },
    }


def write_receipt(path: pathlib.Path, receipt: dict[str, Any]) -> None:
    path = path.expanduser().resolve()
    if path.exists():
        raise CaptureError(f"refusing to overwrite existing receipt: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(receipt))


def capture_command(args: argparse.Namespace) -> int:
    receipt = build_receipt(args.repo, args.older, args.newer, args.submission_dir, args.note_file)
    write_receipt(args.output, receipt)
    print(json.dumps({
        "status": "PASS",
        "receipt": str(args.output.expanduser().resolve()),
        "score_gain_centibits": receipt["delta"]["score_centibits"],
        "proof_root_changed": receipt["delta"]["proof_root_changed"],
        "changed_files": receipt["delta"]["changed_file_count"],
    }, sort_keys=True))
    return 0


def check_command(args: argparse.Namespace) -> int:
    receipt_path = args.receipt.expanduser().resolve(strict=True)
    observed = json.loads(receipt_path.read_text())
    if observed.get("schema") != SCHEMA:
        raise CaptureError(f"unsupported receipt schema: {observed.get('schema')!r}")
    inputs = observed.get("inputs", {})
    rebuilt = build_receipt(
        pathlib.Path(inputs["repo"]),
        observed["predecessor"]["commit"],
        observed["accepted"]["commit"],
        inputs["submission_dir"],
        None if inputs.get("note_file") is None else pathlib.Path(inputs["note_file"]),
    )
    rebuilt["inputs"]["older_ref"] = inputs["older_ref"]
    rebuilt["inputs"]["newer_ref"] = inputs["newer_ref"]
    rebuilt_review = rebuilt.pop("transfer_review")
    observed_immutable = dict(observed)
    observed_review = observed_immutable.pop("transfer_review", None)
    if rebuilt != observed_immutable:
        raise CaptureError("receipt replay differs from recorded bytes")
    if not isinstance(observed_review, dict):
        raise CaptureError("transfer_review must remain an object")
    allowed_review_keys = set(rebuilt_review)
    if set(observed_review) != allowed_review_keys:
        raise CaptureError("transfer_review keys differ from the receipt schema")
    print(json.dumps({
        "status": "PASS",
        "capture_replay": "PASS",
        "review_status": observed_review.get("status"),
        "receipt_sha256": sha256_bytes(receipt_path.read_bytes()),
    }, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    capture = sub.add_parser("capture", help="capture one adjacent accepted score promotion")
    capture.add_argument("--repo", type=pathlib.Path, required=True)
    capture.add_argument("--older", required=True)
    capture.add_argument("--newer", required=True)
    capture.add_argument("--submission-dir", default=DEFAULT_SUBMISSION)
    capture.add_argument("--note-file", type=pathlib.Path)
    capture.add_argument("--output", type=pathlib.Path, required=True)
    capture.set_defaults(handler=capture_command)
    check = sub.add_parser("check", help="replay and byte-check a capture receipt")
    check.add_argument("--receipt", type=pathlib.Path, required=True)
    check.set_defaults(handler=check_command)
    return result


def main() -> int:
    try:
        args = parser().parse_args()
        return args.handler(args)
    except (CaptureError, OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"frontier archaeology failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

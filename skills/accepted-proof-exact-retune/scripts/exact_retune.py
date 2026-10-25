#!/usr/bin/env python3
"""Enumerate a source-bound exact integer retune model and replay its receipt."""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import math
import pathlib
import re
import sys
from typing import Any, Callable


MODEL_SCHEMA = "accepted-proof-exact-retune-model/v1"
SNAPSHOT_SCHEMA = "accepted-proof-snapshot/v1"
RECEIPT_SCHEMA = "accepted-proof-exact-retune-receipt/v1"
MAX_POWER_EXPONENT = 128


class RetuneError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def ceil_div(a: int, b: int) -> int:
    if b == 0:
        raise RetuneError("ceil_div by zero")
    return -((-a) // b)


class ExactEvaluator:
    def __init__(self, values: dict[str, int | bool]):
        self.values = values
        self.functions: dict[str, Callable[..., int]] = {
            "abs": abs,
            "min": min,
            "max": max,
            "ceil_div": ceil_div,
        }

    def evaluate(self, expression: str) -> int | bool:
        try:
            node = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise RetuneError(f"invalid expression {expression!r}: {exc.msg}") from exc
        return self._node(node.body)

    def _node(self, node: ast.AST) -> int | bool:
        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, bool):
                raise RetuneError("only integer and Boolean literals are allowed")
            return node.value
        if isinstance(node, ast.Name):
            if node.id not in self.values:
                raise RetuneError(f"unknown or forward-referenced name: {node.id}")
            return self.values[node.id]
        if isinstance(node, ast.UnaryOp):
            value = self._node(node.operand)
            if isinstance(node.op, ast.Not):
                return not bool(value)
            if type(value) is not int:
                raise RetuneError("numeric unary operator received a Boolean")
            if isinstance(node.op, ast.USub):
                return -value
            if isinstance(node.op, ast.UAdd):
                return value
            raise RetuneError("unsupported unary operator")
        if isinstance(node, ast.BinOp):
            left = self._integer(self._node(node.left))
            right = self._integer(self._node(node.right))
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.FloorDiv):
                if right == 0:
                    raise RetuneError("floor division by zero")
                return left // right
            if isinstance(node.op, ast.Mod):
                if right == 0:
                    raise RetuneError("modulo by zero")
                return left % right
            if isinstance(node.op, ast.Pow):
                if right < 0 or right > MAX_POWER_EXPONENT:
                    raise RetuneError(f"power exponent must be in [0,{MAX_POWER_EXPONENT}]")
                return left ** right
            if isinstance(node.op, ast.Div):
                raise RetuneError("/ is forbidden; use exact integer arithmetic")
            raise RetuneError("unsupported binary operator")
        if isinstance(node, ast.BoolOp):
            values = [bool(self._node(item)) for item in node.values]
            if isinstance(node.op, ast.And):
                return all(values)
            if isinstance(node.op, ast.Or):
                return any(values)
            raise RetuneError("unsupported Boolean operator")
        if isinstance(node, ast.Compare):
            left = self._node(node.left)
            if len(node.ops) != len(node.comparators):
                raise RetuneError("malformed comparison expression")
            for operator, comparator in zip(node.ops, node.comparators):
                right = self._node(comparator)
                if isinstance(operator, ast.Eq):
                    passed = left == right
                elif isinstance(operator, ast.NotEq):
                    passed = left != right
                elif isinstance(operator, ast.Lt):
                    passed = left < right
                elif isinstance(operator, ast.LtE):
                    passed = left <= right
                elif isinstance(operator, ast.Gt):
                    passed = left > right
                elif isinstance(operator, ast.GtE):
                    passed = left >= right
                else:
                    raise RetuneError("unsupported comparison")
                if not passed:
                    return False
                left = right
            return True
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in self.functions:
                raise RetuneError("only abs, min, max, and ceil_div calls are allowed")
            if node.keywords:
                raise RetuneError("keyword arguments are not allowed")
            args = [self._integer(self._node(item)) for item in node.args]
            if not args:
                raise RetuneError("exact helper call requires at least one argument")
            return self.functions[node.func.id](*args)
        raise RetuneError(f"unsupported expression node: {type(node).__name__}")

    @staticmethod
    def _integer(value: int | bool) -> int:
        if type(value) is not int:
            raise RetuneError("integer expression received a Boolean")
        return value


def read_json(path: pathlib.Path) -> tuple[dict[str, Any], pathlib.Path, bytes]:
    resolved = path.expanduser().resolve(strict=True)
    raw = resolved.read_bytes()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RetuneError(f"invalid JSON at {resolved}: {exc}") from exc
    if not isinstance(value, dict):
        raise RetuneError(f"top-level JSON must be an object: {resolved}")
    return value, resolved, raw


def verify_snapshot(snapshot: dict[str, Any]) -> dict[str, tuple[int, str]]:
    if snapshot.get("schema") != SNAPSHOT_SCHEMA:
        raise RetuneError(f"unsupported snapshot schema: {snapshot.get('schema')!r}")
    root = pathlib.Path(snapshot["project_root"]).resolve(strict=True)
    files: dict[str, tuple[int, str]] = {}
    manifest_material: list[str] = []
    for record in snapshot.get("files", []):
        relative = record["path"]
        path = (root / relative).resolve(strict=True)
        if root not in path.parents:
            raise RetuneError(f"snapshot file escapes project root: {relative}")
        actual = sha256(path.read_bytes())
        if actual != record["sha256"]:
            raise RetuneError(f"accepted source drift at {relative}")
        files[relative] = (int(record["line_count"]), actual)
        manifest_material.append(f"{relative}\0{actual}\n")
    manifest = sha256("".join(manifest_material).encode())
    if manifest != snapshot.get("closure_manifest_sha256"):
        raise RetuneError("snapshot closure manifest is internally inconsistent")
    return files


def source_anchor(anchor: Any, files: dict[str, tuple[int, str]], label: str) -> None:
    if not isinstance(anchor, str):
        raise RetuneError(f"{label} requires a file:line source anchor")
    match = re.fullmatch(r"(.+):([1-9][0-9]*)", anchor)
    if not match:
        raise RetuneError(f"invalid source anchor for {label}: {anchor!r}")
    path, line_text = match.groups()
    if path not in files:
        raise RetuneError(f"source anchor for {label} is outside the captured closure: {path}")
    if int(line_text) > files[path][0]:
        raise RetuneError(f"source anchor for {label} exceeds file length: {anchor}")


def validate_model(model: dict[str, Any], snapshot: dict[str, Any], files: dict[str, tuple[int, str]]) -> None:
    if model.get("schema") != MODEL_SCHEMA:
        raise RetuneError(f"unsupported model schema: {model.get('schema')!r}")
    if model.get("direction") not in ("maximize", "minimize"):
        raise RetuneError("direction must be maximize or minimize")
    for key in ("accepted_score_centibits", "required_step_centibits", "max_cases"):
        if type(model.get(key)) is not int or model[key] <= 0:
            raise RetuneError(f"{key} must be a positive integer")
    if model["accepted_score_centibits"] != snapshot.get("accepted_score_centibits"):
        raise RetuneError("model accepted score differs from accepted proof snapshot")
    seen: set[str] = set()
    for section in ("constants", "parameters", "derived"):
        if not isinstance(model.get(section), list):
            raise RetuneError(f"{section} must be a list")
        for item in model[section]:
            name = item.get("name")
            if not isinstance(name, str) or not name.isidentifier() or name in seen:
                raise RetuneError(f"invalid or duplicate model name: {name!r}")
            seen.add(name)
            source_anchor(item.get("source"), files, f"{section}.{name}")
    if not isinstance(model.get("constraints"), list):
        raise RetuneError("constraints must be a list")
    constraint_names: set[str] = set()
    for item in model["constraints"]:
        if not isinstance(item.get("name"), str) or not isinstance(item.get("expr"), str):
            raise RetuneError("every constraint requires name and expr strings")
        if item["name"] in constraint_names:
            raise RetuneError(f"duplicate constraint name: {item['name']}")
        constraint_names.add(item["name"])
        source_anchor(item.get("source"), files, f"constraint.{item.get('name')}")
    objective = model.get("objective")
    if not isinstance(objective, dict) or not isinstance(objective.get("expr"), str):
        raise RetuneError("objective requires an expression")
    source_anchor(objective.get("source"), files, "objective")


def parameter_domain(item: dict[str, Any]) -> list[int]:
    for key in ("baseline", "min", "max", "step"):
        if type(item.get(key)) is not int:
            raise RetuneError(f"parameter {item.get('name')} {key} must be an integer")
    if item["step"] <= 0 or item["min"] > item["max"]:
        raise RetuneError(f"invalid range for parameter {item['name']}")
    if not item["min"] <= item["baseline"] <= item["max"]:
        raise RetuneError(f"baseline lies outside range for parameter {item['name']}")
    values = list(range(item["min"], item["max"] + 1, item["step"]))
    if item["baseline"] not in values:
        raise RetuneError(f"baseline is off-grid for parameter {item['name']}")
    return values


def evaluate_point(model: dict[str, Any], parameters: dict[str, int]) -> tuple[dict[str, int | bool], list[str], int]:
    values: dict[str, int | bool] = {}
    for item in model["constants"]:
        if type(item.get("value")) is not int:
            raise RetuneError(f"constant {item.get('name')} must be an integer")
        values[item["name"]] = item["value"]
    values.update(parameters)
    for item in model["derived"]:
        result = ExactEvaluator(values).evaluate(item.get("expr", ""))
        if type(result) is not int:
            raise RetuneError(f"derived value {item['name']} is not an integer")
        values[item["name"]] = result
    failed: list[str] = []
    for item in model["constraints"]:
        result = ExactEvaluator(values).evaluate(item["expr"])
        if type(result) is not bool:
            raise RetuneError(f"constraint {item['name']} did not evaluate to Boolean")
        if not result:
            failed.append(item["name"])
    objective = ExactEvaluator(values).evaluate(model["objective"]["expr"])
    if type(objective) is not int:
        raise RetuneError("objective did not evaluate to an integer")
    return values, failed, objective


def search(model: dict[str, Any], snapshot: dict[str, Any], spec_path: pathlib.Path, snapshot_path: pathlib.Path, spec_raw: bytes, snapshot_raw: bytes) -> dict[str, Any]:
    files = verify_snapshot(snapshot)
    validate_model(model, snapshot, files)
    domains = [parameter_domain(item) for item in model["parameters"]]
    case_count = math.prod(len(domain) for domain in domains)
    if case_count > model["max_cases"]:
        raise RetuneError(f"declared grid has {case_count} cases, above max_cases={model['max_cases']}")
    names = [item["name"] for item in model["parameters"]]
    baseline = {item["name"]: item["baseline"] for item in model["parameters"]}
    _, baseline_failed, baseline_objective = evaluate_point(model, baseline)
    if baseline_failed:
        raise RetuneError(f"accepted baseline violates constraints: {', '.join(baseline_failed)}")
    if baseline_objective != model["accepted_score_centibits"]:
        raise RetuneError(
            f"baseline objective {baseline_objective} does not equal accepted score {model['accepted_score_centibits']}"
        )
    maximize = model["direction"] == "maximize"
    target = model["accepted_score_centibits"] + (model["required_step_centibits"] if maximize else -model["required_step_centibits"])
    qualifying: list[dict[str, Any]] = []
    constraint_passes = 0
    for values_tuple in itertools.product(*domains):
        if len(names) != len(values_tuple):
            raise RetuneError("internal parameter-domain length mismatch")
        point = dict(zip(names, values_tuple))
        all_values, failed, objective = evaluate_point(model, point)
        if failed:
            continue
        constraint_passes += 1
        crosses = objective >= target if maximize else objective <= target
        if crosses:
            distance = sum(abs(point[name] - baseline[name]) for name in names)
            qualifying.append({
                "parameters": point,
                "derived": {item["name"]: all_values[item["name"]] for item in model["derived"]},
                "objective": objective,
                "l1_parameter_distance": distance,
            })
    if maximize:
        qualifying.sort(key=lambda row: (row["objective"], row["l1_parameter_distance"], tuple(row["parameters"][name] for name in names)))
    else:
        qualifying.sort(key=lambda row: (-row["objective"], row["l1_parameter_distance"], tuple(row["parameters"][name] for name in names)))
    status = "PASS_STRICT_STEP_FOUND" if qualifying else "NO_STRICT_STEP_IN_DECLARED_GRID"
    return {
        "schema": RECEIPT_SCHEMA,
        "classification": "EXACT_EXPLORATION_NOT_ACCEPTED_PROOF",
        "status": status,
        "inputs": {
            "spec_path": str(spec_path),
            "snapshot_path": str(snapshot_path),
            "spec_sha256": sha256(spec_raw),
            "snapshot_sha256": sha256(snapshot_raw),
        },
        "source": {
            "project_root": snapshot["project_root"],
            "git": snapshot["git"],
            "closure_manifest_sha256": snapshot["closure_manifest_sha256"],
            "proof_root": snapshot["proof_root"],
        },
        "search": {
            "direction": model["direction"],
            "accepted_score_centibits": model["accepted_score_centibits"],
            "required_step_centibits": model["required_step_centibits"],
            "strict_target_centibits": target,
            "declared_cases": case_count,
            "constraint_passing_cases": constraint_passes,
            "qualifying_cases": len(qualifying),
            "baseline_parameters": baseline,
            "baseline_objective": baseline_objective,
        },
        "winner": qualifying[0] if qualifying else None,
        "first_qualifying_cells": qualifying[:25],
    }


def run_search(spec: pathlib.Path, snapshot_path: pathlib.Path) -> tuple[dict[str, Any], pathlib.Path, pathlib.Path]:
    model, spec_resolved, spec_raw = read_json(spec)
    snapshot, snapshot_resolved, snapshot_raw = read_json(snapshot_path)
    receipt = search(model, snapshot, spec_resolved, snapshot_resolved, spec_raw, snapshot_raw)
    return receipt, spec_resolved, snapshot_resolved


def search_command(args: argparse.Namespace) -> int:
    receipt, _, _ = run_search(args.spec, args.snapshot)
    output = args.output.expanduser().resolve()
    if output.exists():
        raise RetuneError(f"refusing to overwrite existing receipt: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical(receipt))
    print(json.dumps({"status": receipt["status"], "output": str(output), "winner": receipt["winner"]}, sort_keys=True))
    return 0 if receipt["winner"] is not None else 2


def check_command(args: argparse.Namespace) -> int:
    observed, path, raw = read_json(args.receipt)
    if observed.get("schema") != RECEIPT_SCHEMA:
        raise RetuneError(f"unsupported receipt schema: {observed.get('schema')!r}")
    inputs = observed.get("inputs", {})
    rebuilt, _, _ = run_search(pathlib.Path(inputs["spec_path"]), pathlib.Path(inputs["snapshot_path"]))
    if rebuilt != observed:
        raise RetuneError("retune receipt replay differs from recorded result")
    print(json.dumps({"status": "PASS", "receipt_sha256": sha256(raw)}, sort_keys=True))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    search_parser = sub.add_parser("search")
    search_parser.add_argument("--spec", type=pathlib.Path, required=True)
    search_parser.add_argument("--snapshot", type=pathlib.Path, required=True)
    search_parser.add_argument("--output", type=pathlib.Path, required=True)
    search_parser.set_defaults(handler=search_command)
    check_parser = sub.add_parser("check")
    check_parser.add_argument("--receipt", type=pathlib.Path, required=True)
    check_parser.set_defaults(handler=check_command)
    return result


def main() -> int:
    try:
        args = parser().parse_args()
        return args.handler(args)
    except (RetuneError, OSError, KeyError, ValueError) as exc:
        print(f"exact retune failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

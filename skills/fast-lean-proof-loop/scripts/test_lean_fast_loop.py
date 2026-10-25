#!/usr/bin/env python3

from __future__ import annotations

import json
import pathlib
import subprocess
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).with_name("lean_fast_loop.py")


class LeanFastLoopTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        source = self.root / "Demo"
        source.mkdir()
        (source / "Base.lean").write_text("def base := 1\n")
        (source / "Middle.lean").write_text("import Demo.Base\ndef middle := base\n")
        (source / "Other.lean").write_text("def other := 2\n")
        (source / "Solution.lean").write_text("import Demo.Middle\nimport Demo.Other\ndef solution := middle\n")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def command(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args], check=False, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def test_reverse_import_closure_and_root(self) -> None:
        output = self.root / "plan.json"
        proc = self.command(
            "plan", "--project-root", str(self.root), "--source-root", "Demo",
            "--changed", "Demo/Base.lean", "--output", str(output),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        plan = json.loads(output.read_text())
        self.assertEqual(
            plan["affected_modules_dependency_order"],
            ["Demo.Base", "Demo.Middle", "Demo.Solution"],
        )
        self.assertEqual(plan["build_targets"], ["Demo.Solution"])
        self.assertNotIn("Demo.Other", plan["affected_modules_dependency_order"])

    def test_leaf_change_builds_leaf_and_solution_root(self) -> None:
        output = self.root / "plan.json"
        proc = self.command(
            "plan", "--project-root", str(self.root), "--source-root", "Demo",
            "--changed", "Demo/Other.lean", "--output", str(output),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        plan = json.loads(output.read_text())
        self.assertEqual(plan["affected_modules_dependency_order"], ["Demo.Other", "Demo.Solution"])
        self.assertEqual(plan["build_targets"], ["Demo.Solution"])

    def test_dry_run_records_exact_command(self) -> None:
        output = self.root / "run.json"
        proc = self.command(
            "run", "--project-root", str(self.root), "--source-root", "Demo",
            "--changed", "Demo/Base.lean", "--output", str(output), "--dry-run",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(output.read_text())
        self.assertEqual(result["command"], ["lake", "build", "Demo.Solution"])
        self.assertEqual(result["status"], "DRY_RUN")

    def test_unindexed_change_fails_closed(self) -> None:
        outside = self.root / "Outside.lean"
        outside.write_text("def outside := 0\n")
        output = self.root / "bad.json"
        proc = self.command(
            "plan", "--project-root", str(self.root), "--source-root", "Demo",
            "--changed", "Outside.lean", "--output", str(output),
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("outside indexed source root", proc.stderr)

    def test_project_root_can_be_the_source_root(self) -> None:
        output = self.root / "whole-project-plan.json"
        proc = self.command(
            "plan", "--project-root", str(self.root), "--source-root", ".",
            "--changed", "Demo/Base.lean", "--output", str(output),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        plan = json.loads(output.read_text())
        self.assertEqual(plan["build_targets"], ["Demo.Solution"])


if __name__ == "__main__":
    unittest.main()

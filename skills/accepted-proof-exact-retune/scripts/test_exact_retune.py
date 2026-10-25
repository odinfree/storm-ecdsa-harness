#!/usr/bin/env python3

from __future__ import annotations

import json
import pathlib
import subprocess
import tempfile
import unittest


DIRECTORY = pathlib.Path(__file__).parent
SNAPSHOT = DIRECTORY / "snapshot_accepted_proof.py"
RETUNE = DIRECTORY / "exact_retune.py"


class ExactRetuneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.project = self.root / "project"
        submission = self.project / "ProximityPrize/SubmissionLower"
        submission.mkdir(parents=True)
        (submission / "Solution.lean").write_text(
            "import ProximityPrize.SubmissionLower.Model\n"
            "theorem candidate : True := by trivial\n"
        )
        (submission / "Model.lean").write_text(
            "def n : Nat := 10\n"
            "def acceptedErrors : Nat := 5\n"
            "def scoreWitness : Nat := 100\n"
            "def leadingZeroInventory : Nat := 007\n"
        )
        (submission / "score.txt").write_text("100\n")
        (submission / "radius.txt").write_text("1/2\n")
        self.snapshot = self.root / "snapshot.json"
        proc = self.command(
            SNAPSHOT, "--project-root", str(self.project),
            "--entry", "ProximityPrize/SubmissionLower/Solution.lean",
            "--submission-dir", "ProximityPrize/SubmissionLower",
            "--output", str(self.snapshot),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def command(self, script: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(script), *args], check=False, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def model(self) -> dict:
        anchor = "ProximityPrize/SubmissionLower/Model.lean"
        return {
            "schema": "accepted-proof-exact-retune-model/v1",
            "accepted_score_centibits": 100,
            "required_step_centibits": 1,
            "direction": "maximize",
            "max_cases": 20,
            "constants": [{"name": "n", "value": 10, "source": f"{anchor}:1"}],
            "parameters": [{
                "name": "errors", "baseline": 5, "min": 3, "max": 5, "step": 1,
                "source": f"{anchor}:2",
            }],
            "derived": [{
                "name": "score_cb", "expr": "200 - 20 * errors", "source": f"{anchor}:3",
            }],
            "constraints": [{
                "name": "range", "expr": "0 <= errors and errors <= n", "source": f"{anchor}:2",
            }],
            "objective": {"name": "score", "expr": "score_cb", "source": "ProximityPrize/SubmissionLower/Solution.lean:2"},
        }

    def test_first_strict_cell_and_replay(self) -> None:
        spec = self.root / "model.json"
        spec.write_text(json.dumps(self.model()))
        receipt = self.root / "receipt.json"
        proc = self.command(
            RETUNE, "search", "--spec", str(spec), "--snapshot", str(self.snapshot),
            "--output", str(receipt),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(receipt.read_text())
        self.assertEqual(result["winner"]["parameters"], {"errors": 4})
        self.assertEqual(result["winner"]["objective"], 120)
        replay = self.command(RETUNE, "check", "--receipt", str(receipt))
        self.assertEqual(replay.returncode, 0, replay.stderr)

    def test_float_expression_is_rejected(self) -> None:
        model = self.model()
        model["derived"][0]["expr"] = "200.0 - 20 * errors"
        spec = self.root / "float.json"
        spec.write_text(json.dumps(model))
        receipt = self.root / "bad.json"
        proc = self.command(
            RETUNE, "search", "--spec", str(spec), "--snapshot", str(self.snapshot),
            "--output", str(receipt),
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("only integer", proc.stderr)

    def test_source_drift_breaks_replay(self) -> None:
        spec = self.root / "model.json"
        spec.write_text(json.dumps(self.model()))
        receipt = self.root / "receipt.json"
        proc = self.command(
            RETUNE, "search", "--spec", str(spec), "--snapshot", str(self.snapshot),
            "--output", str(receipt),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        model_file = self.project / "ProximityPrize/SubmissionLower/Model.lean"
        model_file.write_text(model_file.read_text() + "def drift := 1\n")
        replay = self.command(RETUNE, "check", "--receipt", str(receipt))
        self.assertNotEqual(replay.returncode, 0)
        self.assertIn("source drift", replay.stderr)

    def test_wrong_baseline_is_rejected(self) -> None:
        model = self.model()
        model["derived"][0]["expr"] = "201 - 20 * errors"
        spec = self.root / "wrong.json"
        spec.write_text(json.dumps(model))
        receipt = self.root / "bad.json"
        proc = self.command(
            RETUNE, "search", "--spec", str(spec), "--snapshot", str(self.snapshot),
            "--output", str(receipt),
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("baseline objective", proc.stderr)

    def test_duplicate_constraint_names_are_rejected(self) -> None:
        model = self.model()
        model["constraints"].append(dict(model["constraints"][0]))
        spec = self.root / "duplicate.json"
        spec.write_text(json.dumps(model))
        receipt = self.root / "bad.json"
        proc = self.command(
            RETUNE, "search", "--spec", str(spec), "--snapshot", str(self.snapshot),
            "--output", str(receipt),
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("duplicate constraint name", proc.stderr)


if __name__ == "__main__":
    unittest.main()

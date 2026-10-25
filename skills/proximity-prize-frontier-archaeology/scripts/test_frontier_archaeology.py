#!/usr/bin/env python3

from __future__ import annotations

import json
import pathlib
import subprocess
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).with_name("frontier_archaeology.py")
SUBMISSION = pathlib.Path("ProximityPrize/SubmissionLower")


class FrontierArchaeologyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "user.name", "Test")
        (self.repo / "ProximityPrize/Benchmark").mkdir(parents=True)
        (self.repo / "ProximityPrize/Benchmark/TargetLower.lean").write_text("def contract := 1\n")
        (self.repo / SUBMISSION).mkdir(parents=True)
        self.commit_state(100, "1/4", "OldRoot", "old")
        self.first = self.git("rev-parse", "HEAD").stdout.strip()
        self.commit_state(101, "2/5", "NewRoot", "new")
        self.second = self.git("rev-parse", "HEAD").stdout.strip()
        self.commit_state(102, "3/7", "NewestRoot", "newest")
        self.third = self.git("rev-parse", "HEAD").stdout.strip()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def commit_state(self, score: int, radius: str, root: str, message: str) -> None:
        directory = self.repo / SUBMISSION
        (directory / "score.txt").write_text(f"{score}\n")
        (directory / "radius.txt").write_text(f"{radius}\n")
        (directory / "Solution.lean").write_text(
            f"import ProximityPrize.SubmissionLower.{root}\n"
        )
        (directory / f"{root}.lean").write_text(f"def {root.lower()} := {score}\n")
        self.git("add", ".")
        self.git("commit", "-q", "-m", message)

    def command(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT), *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_adjacent_capture_and_replay(self) -> None:
        note = self.root / "note.md"
        note.write_text("changed proof root\n")
        receipt = self.root / "receipt.json"
        proc = self.command(
            "capture", "--repo", str(self.repo), "--older", self.first,
            "--newer", self.second, "--note-file", str(note), "--output", str(receipt),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(receipt.read_text())
        self.assertEqual(data["delta"]["score_centibits"], 1)
        self.assertTrue(data["delta"]["proof_root_changed"])
        self.assertEqual(data["classification"], "CONTAMINATED_INCUMBENT_ARCHAEOLOGY")
        replay = self.command("check", "--receipt", str(receipt))
        self.assertEqual(replay.returncode, 0, replay.stderr)

    def test_endpoint_diff_is_rejected(self) -> None:
        receipt = self.root / "bad.json"
        proc = self.command(
            "capture", "--repo", str(self.repo), "--older", self.first,
            "--newer", self.third, "--output", str(receipt),
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("not adjacent score promotions", proc.stderr)
        self.assertFalse(receipt.exists())

    def test_receipt_detects_note_drift(self) -> None:
        note = self.root / "note.md"
        note.write_text("first\n")
        receipt = self.root / "receipt.json"
        proc = self.command(
            "capture", "--repo", str(self.repo), "--older", self.second,
            "--newer", self.third, "--note-file", str(note), "--output", str(receipt),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        note.write_text("changed\n")
        replay = self.command("check", "--receipt", str(receipt))
        self.assertNotEqual(replay.returncode, 0)

    def test_completed_review_does_not_break_capture_replay(self) -> None:
        receipt = self.root / "receipt.json"
        proc = self.command(
            "capture", "--repo", str(self.repo), "--older", self.second,
            "--newer", self.third, "--output", str(receipt),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(receipt.read_text())
        data["transfer_review"].update({
            "status": "COMPLETE",
            "claimed_mechanism": "The proof root changed.",
            "supporting_anchors": ["ProximityPrize/SubmissionLower/Solution.lean:1"],
            "transfer_verdict": "SOURCE-BOUND",
        })
        receipt.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        replay = self.command("check", "--receipt", str(receipt))
        self.assertEqual(replay.returncode, 0, replay.stderr)

    def test_benchmark_contract_change_is_rejected(self) -> None:
        benchmark = self.repo / "ProximityPrize/Benchmark/TargetLower.lean"
        benchmark.write_text("def contract := 2\n")
        directory = self.repo / SUBMISSION
        (directory / "score.txt").write_text("103\n")
        self.git("add", ".")
        self.git("commit", "-q", "-m", "contract changed")
        fourth = self.git("rev-parse", "HEAD").stdout.strip()
        receipt = self.root / "bad-contract.json"
        proc = self.command(
            "capture", "--repo", str(self.repo), "--older", self.third,
            "--newer", fourth, "--output", str(receipt),
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("benchmark contract tree changed", proc.stderr)
        self.assertFalse(receipt.exists())


if __name__ == "__main__":
    unittest.main()

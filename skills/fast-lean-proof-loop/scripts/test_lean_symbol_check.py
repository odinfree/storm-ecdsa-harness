#!/usr/bin/env python3

from __future__ import annotations

import json
import pathlib
import stat
import subprocess
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).with_name("lean_symbol_check.py")


class LeanSymbolCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        source = self.root / "Demo"
        source.mkdir()
        (source / "Target.lean").write_text("def ExactName := 1\n")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def fake_lake(self, body: str) -> pathlib.Path:
        path = self.root / "fake-lake"
        path.write_text("#!/usr/bin/env python3\n" + body)
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def command(self, lake: pathlib.Path, output: pathlib.Path, timeout: int) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "python3", str(SCRIPT), "--project-root", str(self.root),
                "--source-root", "Demo", "--query", "ExactName",
                "--import", "Demo.Target", "--name", "Demo.ExactName",
                "--lake", str(lake), "--timeout-seconds", str(timeout),
                "--output", str(output),
            ],
            check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

    def test_verified_batch_is_recorded(self) -> None:
        lake = self.fake_lake(
            "import sys\n"
            "if '--version' in sys.argv:\n"
            "    print('Lean test')\n"
            "else:\n"
            "    text=sys.stdin.read()\n"
            "    assert '#check Demo.ExactName' in text\n"
            "    print('Demo.ExactName : Nat')\n"
        )
        output = self.root / "pass.json"
        proc = self.command(lake, output, 3)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        receipt = json.loads(output.read_text())
        self.assertEqual(receipt["verification"], "PASS")
        self.assertEqual(receipt["verified_names"], ["Demo.ExactName"])

    def test_timeout_kills_process_group_and_writes_receipt(self) -> None:
        lake = self.fake_lake("import time\ntime.sleep(30)\n")
        output = self.root / "timeout.json"
        proc = self.command(lake, output, 1)
        self.assertEqual(proc.returncode, 124, proc.stderr)
        receipt = json.loads(output.read_text())
        self.assertEqual(receipt["verification"], "TIMEOUT")
        self.assertEqual(receipt["returncode"], 124)
        self.assertEqual(receipt["verified_names"], [])


if __name__ == "__main__":
    unittest.main()

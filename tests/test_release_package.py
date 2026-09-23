"""Public, standard-library checks for the tagged installable Skill."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
ARCHIVE = ROOT / "release" / f"project-harness-{VERSION}.zip"
REPORT = ROOT / "release" / f"validation-report-{VERSION}.json"


class ReleasePackageTests(unittest.TestCase):
    def test_manifest_matches_repository_and_archive_bytes(self) -> None:
        manifest = (ROOT / "MANIFEST.sha256").read_bytes()
        entries: dict[str, str] = {}
        for line in manifest.decode("utf-8").splitlines():
            digest, relative = line.split("  ", 1)
            self.assertNotIn(relative, entries)
            entries[relative] = digest
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), digest)

        with zipfile.ZipFile(ARCHIVE) as bundle:
            self.assertIsNone(bundle.testzip())
            prefix = "project-harness/"
            self.assertEqual(
                set(bundle.namelist()),
                {prefix + relative for relative in entries} | {prefix + "MANIFEST.sha256"},
            )
            self.assertEqual(bundle.read(prefix + "MANIFEST.sha256"), manifest)
            for relative, digest in entries.items():
                self.assertEqual(hashlib.sha256(bundle.read(prefix + relative)).hexdigest(), digest)

    def test_validation_report_identifies_the_archive(self) -> None:
        report = json.loads(REPORT.read_text(encoding="utf-8"))
        self.assertEqual(report["version"], VERSION)
        self.assertEqual(
            report["package"]["sha256"], hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
        )
        self.assertEqual(
            report["package"]["manifest_sha256"],
            hashlib.sha256((ROOT / "MANIFEST.sha256").read_bytes()).hexdigest(),
        )

    def test_packaged_helper_initializes_and_validates_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temporary = Path(temp_dir)
            with zipfile.ZipFile(ARCHIVE) as bundle:
                bundle.extractall(temporary)
            helper = temporary / "project-harness" / "scripts" / "harness.py"
            workspace = temporary / "workspace"
            workspace.mkdir()
            for arguments in (
                ["init", "--root", str(workspace), "--name", "Smoke", "--skill-version", VERSION],
                ["status", "--root", str(workspace)],
                ["validate", "--root", str(workspace)],
            ):
                result = subprocess.run(
                    [sys.executable, str(helper), *arguments],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            state = json.loads((workspace / ".harness" / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["skill_version"], VERSION)


if __name__ == "__main__":
    unittest.main()

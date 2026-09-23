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
    def run_helper(self, workspace: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "harness.py"), *arguments, "--root", str(workspace)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

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

    def test_new_project_cannot_pass_release_check(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.assertEqual(self.run_helper(root, "init", "--name", "Smoke", "--skill-version", VERSION).returncode, 0)
            result = self.run_helper(root, "release-check")
            self.assertEqual(result.returncode, 1)
            issues = json.loads(result.stderr)["issues"]
            self.assertTrue(any("stage" in issue for issue in issues))
            self.assertTrue(any("requirement" in issue for issue in issues))

    def test_apply_keeps_previous_requirement_contents(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.assertEqual(self.run_helper(root, "init", "--name", "Smoke", "--skill-version", VERSION).returncode, 0)
            state_path = root / ".harness" / "state.json"
            candidate = root / "candidate.json"
            first = json.loads(state_path.read_text(encoding="utf-8"))
            first["requirements"]["active"] = [{"id": "REQ-1", "text": "Original", "required": True}]
            candidate.write_text(json.dumps(first), encoding="utf-8")
            result = self.run_helper(root, "apply", "--candidate", str(candidate), "--expected-revision", "0", "--actor", "test")
            self.assertEqual(result.returncode, 0, result.stderr)
            second = json.loads(state_path.read_text(encoding="utf-8"))
            second["requirements"]["active"][0]["text"] = "Revised"
            candidate.write_text(json.dumps(second), encoding="utf-8")
            result = self.run_helper(root, "apply", "--candidate", str(candidate), "--expected-revision", "1", "--actor", "test")
            self.assertEqual(result.returncode, 0, result.stderr)
            old = json.loads((root / ".harness/history/state-rev-00000001.json").read_text(encoding="utf-8"))
            self.assertEqual(old["requirements"]["active"][0]["text"], "Original")

    def test_apply_rejects_null_capabilities(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.assertEqual(self.run_helper(root, "init", "--name", "Smoke", "--skill-version", VERSION).returncode, 0)
            state_path = root / ".harness" / "state.json"
            candidate = root / "candidate.json"
            invalid = json.loads(state_path.read_text(encoding="utf-8"))
            invalid["capabilities"] = None
            candidate.write_text(json.dumps(invalid), encoding="utf-8")
            result = self.run_helper(root, "apply", "--candidate", str(candidate), "--expected-revision", "0", "--actor", "test")
            self.assertEqual(result.returncode, 1)
            self.assertTrue(any("capabilities" in issue for issue in json.loads(result.stderr)["issues"]))
            self.assertEqual(json.loads(state_path.read_text(encoding="utf-8"))["revision"], 0)


if __name__ == "__main__":
    unittest.main()

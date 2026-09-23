# Project Harness 2.0.4 compatibility matrix

| Environment | Evidence | Status |
| --- | --- | --- |
| Windows 11, Python 3.14.4 | 92 development tests passed with one symlink privilege skip; 6 public package tests passed | Verified within those checks |
| Ubuntu under WSL2, Python 3.14.4 | 92 development tests passed without skips; 6 public package tests passed | Verified in WSL2 |
| Native Linux and macOS | No native-host run for 2.0.4 | Unverified |
| Codex and local models | No 2.0.4 run | Unverified |
| Other Agent Skills hosts | No host-specific run | Unverified |

2.0.4 fixes two correctness bugs in `scripts/harness.py` (`release_issues` ignoring the `required` flag on
failed checks; `_check_issues` only enforcing the check-v2 schema's required fields for `status: passed`,
including a crash on an explicit `requirement_ids: null`), found by an independent review of the installed
2.0.3 skill. A second-pass review found that the first fix's use of `dict.get()` for the nullable
`snapshot_fingerprint`/`executed_at` fields let a record missing both keys pass silently; both keys are now
required to be present (value may still be `null`). `SKILL.md`, `VERSION`, and `MANIFEST.sha256` also
changed accordingly; the description text itself did not change from 2.0.3. Four regression tests cover the
fixes. See the [validation report](validation-report-2.0.4.json).

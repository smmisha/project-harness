# Project Harness 2.0.0 compatibility matrix

| Environment | Evidence | Status |
| --- | --- | --- |
| Windows 11, Python 3.14.4 | 83 deterministic tests passed; 1 symlink test skipped because the required privilege was unavailable | Verified with the stated skip |
| Ubuntu on WSL2, Python 3.14.4 | 83 deterministic tests passed with no skips; atomic replace, lock, Unicode path, path traversal, and symlink probes passed | Verified in WSL2 |
| Native Linux | No native-host run | Unverified |
| macOS | No run | Unverified |
| Codex behavioral use | Earlier beta snapshot evaluations, including the paired holdout | Limited evidence; no confirmed benefit over baseline |
| Claude Code behavioral use | Selected beta snapshot portable scenarios only | Limited evidence; full 2.0.0 compatibility unverified |
| Other Skill hosts | No host-specific run | Unverified |

The 2.0.0 package is a local release candidate. Its archive and deterministic tests are described in [validation-report-2.0.0.json](validation-report-2.0.0.json). Natural prompting did not trigger Skill discovery in the three positive discovery trials, so automatic invocation is not a verified claim.

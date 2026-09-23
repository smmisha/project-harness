# Project Harness 2.0.2 compatibility matrix

| Environment | Evidence | Status |
| --- | --- | --- |
| Windows 11, Python 3.14.4 | 88 development tests passed with one symlink privilege skip; 6 public package tests passed | Verified within those checks |
| Ubuntu under WSL2, Python 3.14.4 | 88 development tests passed without skips; 6 public package tests passed | Verified in WSL2 |
| Native Linux and macOS | No native-host run for 2.0.2 | Unverified |
| Codex and Claude Code behavior | Only earlier beta-snapshot model evaluations | No 2.0.2 behavioral claim |
| Other Agent Skills hosts | No host-specific run | Unverified |

The [validation report](validation-report-2.0.2.json) identifies the exact archive and test evidence. The public package checks are reproducible from the repository; the 88-test development suite depends on internal historical fixtures that were not published.

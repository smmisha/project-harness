# Project Harness 2.0.1 compatibility matrix

| Environment | Evidence | Status |
| --- | --- | --- |
| Windows 11, Python 3.14.4 | 83 development tests passed with one symlink privilege skip; 3 public package tests passed | Verified within those checks |
| Ubuntu under WSL2, Python 3.14.4 | 83 development tests passed without skips, including filesystem probes | Verified in WSL2 |
| Native Linux and macOS | No native-host run for 2.0.1 | Unverified |
| Codex and Claude Code behavior | Only earlier beta-snapshot model evaluations | No 2.0.1 behavioral claim |
| Other Agent Skills hosts | No host-specific run | Unverified |

The [validation report](validation-report-2.0.1.json) identifies the exact archive and test evidence. The public package checks are reproducible from the repository; the 83-test development suite depends on internal historical fixtures that were not published. Natural prompting did not trigger the Skill in the three positive discovery trials on the earlier beta snapshot.

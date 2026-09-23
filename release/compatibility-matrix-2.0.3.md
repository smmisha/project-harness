# Project Harness 2.0.3 compatibility matrix

| Environment | Evidence | Status |
| --- | --- | --- |
| Windows 11, Python 3.14.4 | 88 development tests passed with one symlink privilege skip; 6 public package tests passed | Verified within those checks |
| Ubuntu under WSL2, Python 3.14.4 | 88 development tests passed without skips; 6 public package tests passed | Verified in WSL2 |
| Native Linux and macOS | No native-host run for 2.0.3 | Unverified |
| Claude Code (desktop), Claude Opus 5.5 subagents | Natural-prompt discovery: 3 of 3 project prompts invoked the Skill; 0 of 1 simple question invoked it | Small-sample observation, not a reliability claim |
| Codex and local models | No 2.0.3 run | Unverified |
| Other Agent Skills hosts | No host-specific run | Unverified |

2.0.3 changes only the `description` frontmatter in `SKILL.md` and `VERSION`, with `MANIFEST.sha256` regenerated for them; the other 16 packaged files are byte-identical to 2.0.2. The [validation report](validation-report-2.0.3.json) identifies the exact archive and test evidence.

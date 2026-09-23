# Project Harness 2.0.5 compatibility matrix

| Environment | Evidence | Status |
| --- | --- | --- |
| Windows 11, Python 3.14.4 | 112 development tests passed with one symlink privilege skip; 6 public package tests passed | Verified within those checks |
| Ubuntu under WSL2, Python 3.14.4 | 112 development tests passed without skips; 6 public package tests passed | Verified in WSL2 |
| Native Linux and macOS | No native-host run for 2.0.5 | Unverified |
| Codex and local models | No 2.0.5 run | Unverified |
| Other Agent Skills hosts | No host-specific run | Unverified |

2.0.5 brings `validate_state()` and `_check_issues()` into full compliance with the project's own
`schemas/state-v2.schema.json` and `schemas/check-v2.schema.json`. A field-by-field audit found 12 places
where an input the schema declares invalid was silently accepted (malformed `project_id`/check `id`
patterns; unexpected extra fields on the state object and on individual checks; extra keys on the `checks`
and `operations` containers; untyped state-level `extensions`/`legacy`; missing pattern and `uniqueItems`
enforcement on `requirement_ids`/`task_ids`; missing `minLength`/`uniqueItems` enforcement on
`input_paths`/`evidence_refs`/`invalidated_by`; non-scalar `environment` values; a wrongly-typed check-level
`extensions`). A second-pass review (Codex) also found that list or object values in enum and reference
fields crashed the validator with `TypeError` instead of producing a validation issue; those now report an
issue. 20 regression tests cover these cases. `SKILL.md` is unchanged. See the
[validation report](validation-report-2.0.5.json).

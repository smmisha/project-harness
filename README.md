# Project Harness

Project Harness is a portable Agent Skill for planning, executing, continuing, recovering, verifying, and handing over multi-step projects. This repository contains the installable `2.0.4` Skill and its verified archive.

`2.0.4` fixes two correctness bugs in the optional `scripts/harness.py` helper, found by an independent
review of the installed 2.0.3 skill: `release_issues()` ignored a check's `required` flag entirely, so a
failed required check was invisible to `release-check` whenever another, non-required check covered the
same requirement; and `_check_issues()` only enforced the check-v2 schema's required fields when a check's
status was `passed`, so a bare `{id, status: planned}` record passed validation and an explicit
`requirement_ids: null` crashed with `TypeError` instead of producing a validation message. Both are fixed
and covered by new regression tests; no other source file changed.

## Install

Copy this directory into the Skills location supported by your AI host, preserving `SKILL.md`, `VERSION`, `LICENSE`, `MANIFEST.sha256`, `agents/`, `assets/`, `references/`, `schemas/`, and `scripts/`. Alternatively, extract [`project-harness-2.0.4.zip`](release/project-harness-2.0.4.zip) and copy its `project-harness/` directory. See [`SKILL.md`](SKILL.md) for activation and workflow instructions.

Explicit invocation example:

```text
Use $project-harness to continue this project from its current state to a verified handover.
```

The Skill works without Python. For optional project-local managed state, Python 3.10+ provides a standard-library helper:

```text
python /path/to/project-harness/scripts/harness.py init --root /path/to/project --name "Project name" --skill-version 2.0.4
python /path/to/project-harness/scripts/harness.py status --root /path/to/project
python /path/to/project-harness/scripts/harness.py validate --root /path/to/project
python /path/to/project-harness/scripts/harness.py recover --root /path/to/project
python /path/to/project-harness/scripts/harness.py release-check --root /path/to/project
```

The helper validates declared state and evidence. It does not prove semantic correctness, contact providers, deploy, send notifications, or authorize external actions.

## Evidence and limits

The [`2.0.4` validation report](release/validation-report-2.0.4.json) records archive hashes and deterministic testing: 92 development tests passed on Windows 11 with one expected symlink privilege skip; 92 passed without skips on Ubuntu under WSL2. See the [compatibility matrix](release/compatibility-matrix-2.0.4.md). Native Linux and macOS were not tested.

Earlier beta-snapshot model evaluations did not establish a benefit over baseline. With the 2.0.2 description, natural prompting failed to discover the Skill in all three positive beta trials and in one Claude Code check. 2.0.3 rewrites only the description as trigger-oriented text; in Claude Code with Claude Opus 5.5 subagents it was invoked in 3 of 3 natural project prompts and not invoked for 1 simple question. These are small single-model samples and should not be read as claims of reliable automatic invocation or broad host compatibility.

Licensed under [MIT](LICENSE), Copyright (c) 2026 socialmediamisha.

## Reproduce public package checks

From this repository with Python 3.10 or newer, run:

```text
python -m unittest discover -s tests -v
```

The six [public tests](tests/test_release_package.py) verify the exact `2.0.4` manifest and ZIP bytes, the report hash, a packaged helper init/status/validate cycle, and the three fixed helper regressions. They use only the Python standard library. The 92-test development suite used additional internal historical fixtures and is not included here; its count is recorded as validation evidence, not represented as independently reproducible from this repository.

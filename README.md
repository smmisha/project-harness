# Project Harness

Project Harness is a portable Agent Skill for planning, executing, continuing, recovering, verifying, and handing over multi-step projects. This repository contains the installable `2.0.0` Skill and its verified release archive.

## Install

Copy this directory into the Skills location supported by your AI host, preserving `SKILL.md`, `VERSION`, `LICENSE`, `MANIFEST.sha256`, `agents/`, `assets/`, `references/`, `schemas/`, and `scripts/`. Alternatively, extract [`project-harness-2.0.0.zip`](release/project-harness-2.0.0.zip) and copy its `project-harness/` directory. See [`SKILL.md`](SKILL.md) for activation and workflow instructions.

Explicit invocation example:

```text
Use $project-harness to continue this project from its current state to a verified handover.
```

The Skill works without Python. For optional project-local managed state, Python 3.10+ provides a standard-library helper:

```text
python /path/to/project-harness/scripts/harness.py init --root /path/to/project --name "Project name" --skill-version 2.0.0
python /path/to/project-harness/scripts/harness.py status --root /path/to/project
python /path/to/project-harness/scripts/harness.py validate --root /path/to/project
python /path/to/project-harness/scripts/harness.py recover --root /path/to/project
python /path/to/project-harness/scripts/harness.py release-check --root /path/to/project
```

The helper validates declared state and evidence. It does not prove semantic correctness, contact providers, deploy, send notifications, or authorize external actions.

## Evidence and limits

The [`2.0.0` validation report](release/validation-report-2.0.0.json) records archive hashes and deterministic testing: 83 tests passed on Windows 11 with one expected symlink privilege skip; 83 passed without skips on Ubuntu under WSL2. See the [compatibility matrix](release/compatibility-matrix-2.0.0.md). Native Linux and macOS were not tested.

Earlier beta-snapshot model evaluations did not establish a benefit over baseline. Natural prompting failed to discover the Skill in all three positive trials. These results should not be read as claims of reliable automatic invocation or broad host compatibility.

Licensed under [MIT](LICENSE), Copyright (c) 2026 socialmediamisha.

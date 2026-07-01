# Monad OS v0 Command Spec

Status: Draft  
Stage: v0 implementation planning  
Owner: Monad OS maintainers  
Last updated: 2026-06-29

## Purpose

This document defines the initial command surface for the Monad OS v0 CLI.

Monad OS is an AI-agnostic, cloud-agnostic, database-agnostic SDLC Control Plane and Monorepo Operating System. The v0 CLI is the first local executable interface into that control plane.

The v0 command surface must prove that Monad OS can:

1. Initialize a governed workspace.
2. Read a canonical `workspace.toml` manifest.
3. Inspect repository structure.
4. Build an initial lifecycle graph from local files.
5. Run governance checks.
6. Produce machine-readable evidence.
7. Prepare AI-ready context without requiring any AI provider.
8. Remain useful without hosted SaaS.

## Non-Goals

The v0 CLI is not expected to provide:

- Hosted SaaS synchronization.
- Multi-user RBAC.
- Enterprise policy marketplace.
- Full remote execution.
- Full CI/CD orchestration.
- Autonomous AI code modification.
- Production incident management.
- Deep language-specific build replacement.
- Complete Nx, Buck2, or Pants integration.

Monad OS v0 should wrap, inspect, validate, and govern. It should not attempt to replace native tools.

## Design Principles

The v0 command surface follows these principles:

1. **Local-first by default**  
   Every required v0 command must run locally without a SaaS backend.

2. **Manifest-driven**  
   Commands should prefer `workspace.toml` as the canonical workspace intent source.

3. **Read before write**  
   Most commands should inspect, validate, report, or produce evidence before mutating files.

4. **Human approval by default**  
   Commands that could make risky changes must require explicit flags or confirmation.

5. **Machine-readable outputs**  
   Commands should support structured output formats where practical.

6. **Composable with native tools**  
   Monad OS should orchestrate and govern native tools rather than hiding them.

7. **AI-ready but AI-optional**  
   Commands may prepare context for AI systems, but must not require a specific AI model or vendor.

8. **Evidence-first**  
   Command results should be suitable for audit trails, CI artifacts, and future lifecycle graph ingestion.

## CLI Binary

The v0 binary name is:

```text
monad
```

## Global Command Shape

```text
monad <command> [subcommand] [options]
```

## Global Flags

All commands should eventually support the following common flags where applicable.

```text
--workspace <path>       Path to the workspace root. Defaults to current directory.
--manifest <path>        Path to workspace manifest. Defaults to ./workspace.toml.
--format <format>        Output format: text, json, markdown.
--output <path>          Write command output to a file.
--quiet                  Reduce non-essential terminal output.
--verbose                Increase diagnostic output.
--no-color               Disable colored terminal output.
--dry-run                Show intended action without making changes.
--yes                    Assume yes for safe prompts only.
--help                   Show command help.
```

## Output Formats

The v0 CLI should standardize on these output formats.

| Format     | Purpose                                      |
| ---------- | -------------------------------------------- |
| `text`     | Human-readable terminal output               |
| `json`     | Machine-readable automation output           |
| `markdown` | Documentation, reports, and review artifacts |

Default output format should be `text`.

Commands that produce durable evidence should support `json` and/or `markdown`.

## Exit Codes

| Code | Meaning                                    |
| ---: | ------------------------------------------ |
|  `0` | Success                                    |
|  `1` | General failure                            |
|  `2` | Invalid command usage or invalid arguments |
|  `3` | Workspace or manifest validation failed    |
|  `4` | Policy check failed                        |
|  `5` | Native tool invocation failed              |
|  `6` | Evidence generation failed                 |
|  `7` | Graph generation failed                    |
|  `8` | Unsafe action blocked                      |
|  `9` | Unsupported feature for current workspace  |

## v0 Command Inventory

The v0 command surface is divided into required and stretch commands.

### Required v0 Commands

These commands define the minimum useful Monad OS CLI.

```text
monad help
monad version
monad init
monad doctor
monad workspace inspect
monad workspace validate
monad graph build
monad graph export
monad policy check
monad evidence collect
monad context pack
```

### Stretch v0 Commands

These commands may be implemented in v0 if capacity allows, but should not block the first working release.

```text
monad tool list
monad tool check
monad plan
monad report
monad adr list
monad adr check
```

## Command Specs

---

## `monad help`

Show top-level CLI help.

### Usage

```text
monad help
monad --help
```

### Behavior

* Prints available commands.
* Prints global flags.
* Points users to documentation.
* Exits with code `0`.

### v0 Requirement

Required.

---

## `monad version`

Show CLI version and build metadata.

### Usage

```text
monad version
monad version --format json
```

### Example Text Output

```text
monad 0.1.0
commit: unknown
build: local
```

### Example JSON Output

```json
{
  "name": "monad",
  "version": "0.1.0",
  "commit": "unknown",
  "build": "local"
}
```

### v0 Requirement

Required.

---

## `monad init`

Initialize Monad OS workspace metadata.

### Usage

```text
monad init
monad init --workspace .
monad init --dry-run
```

### Behavior

Creates missing foundation files only when they do not already exist.

The v0 command may create:

```text
workspace.toml
.monad/
.monad/evidence/
.monad/graph/
.monad/context/
```

It must not overwrite existing files unless an explicit future `--force` flag is added.

### Safety Rules

* Must be safe to run more than once.
* Must not delete user files.
* Must not initialize Git automatically unless explicitly requested in a later version.
* Must explain what was created.

### v0 Requirement

Required.

---

## `monad doctor`

Run local workspace health checks.

### Usage

```text
monad doctor
monad doctor --format json
monad doctor --output .monad/evidence/doctor.json --format json
```

### Checks

The v0 doctor should check:

1. Current directory exists.
2. `workspace.toml` exists.
3. `workspace.toml` parses successfully.
4. Required top-level directories are present.
5. Git repository is detected.
6. Working tree status can be read.
7. Known native tools can be detected when configured.
8. `.monad/` state directory is writable or can be created.
9. Documentation index exists.
10. ADR directory exists.

### Example Text Output

```text
Monad OS doctor

Workspace: .
Manifest: workspace.toml

Checks:
  OK  workspace root found
  OK  workspace.toml found
  OK  manifest parsed
  OK  git repository detected
  OK  docs index found
  OK  decisions directory found

Result: passed
```

### Example JSON Output

```json
{
  "command": "doctor",
  "status": "passed",
  "workspace": ".",
  "manifest": "workspace.toml",
  "checks": [
    {
      "id": "workspace.root.exists",
      "status": "passed"
    },
    {
      "id": "manifest.exists",
      "status": "passed"
    }
  ]
}
```

### v0 Requirement

Required.

---

## `monad workspace inspect`

Inspect workspace structure and summarize detected components.

### Usage

```text
monad workspace inspect
monad workspace inspect --format json
monad workspace inspect --format markdown --output .monad/evidence/workspace-inspect.md
```

### Behavior

The command should read the local workspace and report:

* Workspace root.
* Manifest path.
* Top-level directories.
* Detected apps.
* Detected services.
* Detected packages or libraries.
* Detected docs.
* Detected ADRs.
* Detected policy directories.
* Detected scripts.
* Detected infrastructure directories.
* Detected test directories.
* Unknown or unmanaged directories.

### Example Text Output

```text
Workspace inspection

Root: .
Manifest: workspace.toml

Detected:
  docs: 19 files
  decisions: 15 ADRs
  scripts: 1 file

Warnings:
  none
```

### v0 Requirement

Required.

---

## `monad workspace validate`

Validate workspace structure against `workspace.toml` and Monad OS foundation expectations.

### Usage

```text
monad workspace validate
monad workspace validate --format json
```

### Behavior

The command should verify:

1. Manifest exists.
2. Manifest parses.
3. Required workspace metadata exists.
4. Declared directories exist or are explicitly marked as planned.
5. Declared lifecycle domains are recognized.
6. Declared toolchain entries are valid.
7. No required foundation files are missing.
8. No known anti-patterns are present.

### Relationship to `doctor`

`doctor` checks whether the local environment is healthy.

`workspace validate` checks whether the workspace conforms to Monad OS expectations.

### v0 Requirement

Required.

---

## `monad graph build`

Build the initial local lifecycle graph.

### Usage

```text
monad graph build
monad graph build --output .monad/graph/lifecycle-graph.json
monad graph build --format json
```

### Behavior

The command should scan local repository artifacts and produce a graph model containing nodes and edges.

Initial graph sources may include:

* `workspace.toml`
* `README.md`
* `AGENTS.md`
* Documentation files
* ADRs
* Scripts
* Policy files
* Implementation work packages
* Roadmap documents

### Initial Node Types

| Node Type      | Description                        |
| -------------- | ---------------------------------- |
| `workspace`    | The root Monad OS workspace        |
| `document`     | A documentation artifact           |
| `adr`          | Architecture Decision Record       |
| `script`       | Local automation script            |
| `policy`       | Governance or policy artifact      |
| `work_package` | Implementation planning unit       |
| `roadmap`      | Roadmap artifact                   |
| `command`      | CLI command described by this spec |
| `evidence`     | Generated proof or report artifact |

### Initial Edge Types

| Edge Type    | Description                                      |
| ------------ | ------------------------------------------------ |
| `contains`   | Parent artifact contains child artifact          |
| `references` | Artifact references another artifact             |
| `decides`    | ADR decides or constrains an area                |
| `implements` | Work package implements a decision or capability |
| `validates`  | Script or policy validates an artifact           |
| `produces`   | Command produces an artifact                     |
| `governs`    | Policy governs an artifact or action             |

### Example JSON Shape

```json
{
  "graph_version": "0.1",
  "workspace": "monad-os",
  "nodes": [
    {
      "id": "doc:README.md",
      "type": "document",
      "path": "README.md"
    }
  ],
  "edges": [
    {
      "from": "workspace:monad-os",
      "to": "doc:README.md",
      "type": "contains"
    }
  ]
}
```

### v0 Requirement

Required.

---

## `monad graph export`

Export the lifecycle graph in a requested format.

### Usage

```text
monad graph export --format json
monad graph export --format markdown --output .monad/graph/lifecycle-graph.md
```

### Supported v0 Formats

| Format     | Required |
| ---------- | -------- |
| `json`     | Yes      |
| `markdown` | Yes      |
| `dot`      | Stretch  |
| `mermaid`  | Stretch  |

### Behavior

The command should either:

1. Export a previously built graph from `.monad/graph/`, or
2. Build and export the graph if no graph artifact exists.

### v0 Requirement

Required.

---

## `monad policy check`

Run local governance checks.

### Usage

```text
monad policy check
monad policy check --format json
monad policy check --output .monad/evidence/policy-check.json --format json
```

### v0 Policy Categories

The v0 policy engine should start with static repository checks.

| Category      | Example Checks                                     |
| ------------- | -------------------------------------------------- |
| Foundation    | Required files exist                               |
| Documentation | Docs index references required docs                |
| ADRs          | ADR numbering is contiguous                        |
| Scripts       | Required scripts are executable                    |
| Manifest      | `workspace.toml` exists and parses                 |
| Safety        | Risky AI actions require approval language         |
| Evidence      | Evidence output directory exists or can be created |

### Behavior

* Returns exit code `0` if all required policies pass.
* Returns exit code `4` if required policies fail.
* May return warnings without failing if checks are advisory.

### v0 Requirement

Required.

---

## `monad evidence collect`

Collect command outputs and local facts into an evidence bundle.

### Usage

```text
monad evidence collect
monad evidence collect --output .monad/evidence/foundation-evidence.json
monad evidence collect --format markdown --output .monad/evidence/foundation-evidence.md
```

### Evidence Bundle Contents

The v0 evidence bundle should include:

* Timestamp.
* Workspace root.
* Git commit SHA if available.
* Git branch if available.
* Working tree status summary.
* Manifest path.
* Required file check results.
* ADR inventory.
* Documentation inventory.
* Policy check result.
* Doctor result.
* Graph artifact path if available.

### Example JSON Shape

```json
{
  "evidence_version": "0.1",
  "workspace": "monad-os",
  "git": {
    "branch": "main",
    "commit": "unknown",
    "dirty": false
  },
  "results": {
    "doctor": "passed",
    "policy": "passed",
    "graph": "generated"
  }
}
```

### v0 Requirement

Required.

---

## `monad context pack`

Create an AI-ready context package from governed workspace artifacts.

### Usage

```text
monad context pack
monad context pack --output .monad/context/context-pack.md
monad context pack --format json --output .monad/context/context-pack.json
```

### Behavior

The command should assemble a bounded context package from repository artifacts.

Initial included sources:

* `README.md`
* `AGENTS.md`
* `workspace.toml`
* Product charter
* PRD
* Technical product blueprint
* SDLC control plane architecture
* Toolchain strategy
* Agnosticity strategy
* Competitive moat
* Governance principles
* Roadmap
* Work packages
* ADR index
* ADR files

### AI-Agnostic Requirement

The command must not call an AI provider.

It only prepares context that can be handed to a human or any AI system.

### Safety Rules

The command should:

* Respect ignore files when implemented.
* Avoid secrets.
* Include source paths.
* Include token or size estimates when possible.
* Warn when generated context is too large.
* Prefer deterministic ordering.

### v0 Requirement

Required.

---

## `monad tool list`

List configured native tools.

### Usage

```text
monad tool list
monad tool list --format json
```

### Behavior

Reads `workspace.toml` and lists configured or detected tools.

Examples:

* Git
* Rust
* Node.js
* Bun
* Nx
* Buck2
* Pants
* Fumadocs
* Docker
* Terraform
* OpenTofu

### v0 Requirement

Stretch.

---

## `monad tool check`

Check whether configured native tools are installed.

### Usage

```text
monad tool check
monad tool check --format json
```

### Behavior

Reports installed, missing, and version-mismatched tools.

The command should not install tools in v0.

### v0 Requirement

Stretch.

---

## `monad plan`

Generate an implementation or remediation plan from workspace inspection results.

### Usage

```text
monad plan
monad plan --format markdown --output .monad/evidence/plan.md
```

### Behavior

The v0 version should be deterministic and rule-based.

It should not call an AI provider.

Possible plan sources:

* Failed doctor checks.
* Failed policy checks.
* Missing foundation files.
* Missing graph artifacts.
* Missing evidence artifacts.
* Missing documentation references.

### v0 Requirement

Stretch.

---

## `monad report`

Generate a local status report.

### Usage

```text
monad report
monad report --format markdown --output .monad/evidence/status-report.md
```

### Behavior

Combines outputs from:

* `doctor`
* `workspace inspect`
* `workspace validate`
* `policy check`
* `graph build`
* `evidence collect`

### v0 Requirement

Stretch.

---

## `monad adr list`

List ADRs.

### Usage

```text
monad adr list
monad adr list --format json
```

### Behavior

Reports:

* ADR number.
* Title.
* Status.
* Path.
* Date if available.
* Whether numbering is contiguous.

### v0 Requirement

Stretch.

---

## `monad adr check`

Validate ADR conventions.

### Usage

```text
monad adr check
monad adr check --format json
```

### Behavior

Checks:

* ADR filenames are numbered.
* ADR numbers are contiguous.
* ADR titles are present.
* ADR statuses are present.
* ADR index references all ADRs.

### v0 Requirement

Stretch.

## Command-to-Artifact Mapping

| Command                    | Primary Artifact Produced                  |
| -------------------------- | ------------------------------------------ |
| `monad doctor`             | `.monad/evidence/doctor.json`              |
| `monad workspace inspect`  | `.monad/evidence/workspace-inspect.json`   |
| `monad workspace validate` | `.monad/evidence/workspace-validate.json`  |
| `monad graph build`        | `.monad/graph/lifecycle-graph.json`        |
| `monad graph export`       | `.monad/graph/lifecycle-graph.md`          |
| `monad policy check`       | `.monad/evidence/policy-check.json`        |
| `monad evidence collect`   | `.monad/evidence/foundation-evidence.json` |
| `monad context pack`       | `.monad/context/context-pack.md`           |
| `monad report`             | `.monad/evidence/status-report.md`         |

## Command-to-ADR Mapping

| Command Area              | Relevant ADRs |
| ------------------------- | ------------- |
| Control plane purpose     | ADR-0001      |
| CLI implementation        | ADR-0002      |
| Manifest behavior         | ADR-0003      |
| Native tool wrapping      | ADR-0004      |
| Documentation integration | ADR-0005      |
| Agnosticism               | ADR-0006      |
| Nx support                | ADR-0007      |
| Buck2 and Pants support   | ADR-0008      |
| Local-first operation     | ADR-0009      |
| Future SaaS control plane | ADR-0010      |
| Policy packs              | ADR-0011      |
| Packs and plugins         | ADR-0012      |
| Evidence                  | ADR-0013      |
| Lifecycle graph           | ADR-0014      |
| Human approval gates      | ADR-0015      |

## v0 Implementation Order

Recommended implementation order:

1. `monad version`
2. `monad help`
3. `monad init`
4. `monad doctor`
5. `monad workspace inspect`
6. `monad workspace validate`
7. `monad policy check`
8. `monad evidence collect`
9. `monad graph build`
10. `monad graph export`
11. `monad context pack`

This order starts with simple CLI mechanics, then workspace validation, then evidence, then graph generation, then context packaging.

## Acceptance Criteria

The v0 command surface is acceptable when:

1. The CLI builds locally.
2. `monad --help` shows the command groups.
3. `monad version` returns a version.
4. `monad init` is idempotent.
5. `monad doctor` can pass on the repository.
6. `monad workspace inspect` detects the foundation documents and ADRs.
7. `monad workspace validate` checks `workspace.toml`.
8. `monad policy check` validates foundation rules.
9. `monad evidence collect` writes an evidence artifact.
10. `monad graph build` writes a lifecycle graph artifact.
11. `monad graph export` exports graph data.
12. `monad context pack` writes an AI-ready context package without calling an AI provider.
13. Required commands support useful text output.
14. Evidence-producing commands support machine-readable output.
15. Risky mutation is avoided or guarded.

## Open Questions

1. Should `monad graph build` and `monad graph export` be separate commands in v0, or should export be a flag on build?
2. Should `monad evidence collect` automatically invoke other commands, or only collect existing outputs?
3. Should v0 use JSON Schema for command output contracts?
4. Should `workspace.toml` declare enabled command modules?
5. Should policy checks be hardcoded in v0 before policy packs exist?
6. Should context packing support explicit profiles such as `foundation`, `implementation`, and `handoff`?
7. Should `monad doctor` validate external tools only when declared in the manifest?
8. Should ADR checks be part of `policy check` or remain a separate command group?

## Summary

The v0 CLI should be small, local-first, deterministic, and evidence-oriented.

Its job is to turn the current Monad OS foundation repository from a set of documents into an inspectable, validated, graph-ready control-plane workspace.

The first implementation should prioritize correctness, transparent output, and stable contracts over breadth.

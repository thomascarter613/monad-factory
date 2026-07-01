# Monad OS v0 Work Packages

## Status

Draft v0.1

## Date

2026-06-29

## Purpose

This document breaks Monad OS v0 into concrete implementation work packages.

It translates the product charter, PRD, ADRs, and v0-v1-v2 roadmap into actionable engineering work.

The goal of v0 is not to build the entire Monad OS vision.

The goal of v0 is to create the first useful local-first foundation:

```txt
A Rust-based `monad` CLI that can initialize, inspect, and validate a Monad OS workspace locally.
```

---

# 1. v0 Product Goal

v0 should prove that Monad OS can exist as a real local-first product.

A user should be able to run:

```bash
monad init
monad doctor
monad inspect
```

and get a useful governed repository foundation.

---

# 2. v0 Scope

v0 includes:

```txt
Rust CLI workspace
monad binary
basic command structure
workspace.toml model
monad init
monad init --interactive
monad doctor
monad inspect
basic docs generation
basic recommendation output
basic .monad state directory
foundation validation
```

v0 does not include:

```txt
hosted SaaS
Fumadocs app generation
full Nx integration
full graph engine
full policy pack engine
full evidence system
plugin runtime
marketplace
AI provider integration
production deployment
```

---

# 3. v0 Work Package Summary

| ID        | Work Package                | Outcome                                                   |
| --------- | --------------------------- | --------------------------------------------------------- |
| WP-v0-001 | Create Rust Workspace       | Repo contains compilable Rust workspace                   |
| WP-v0-002 | Create CLI Skeleton         | `monad --help` and `monad version` work                   |
| WP-v0-003 | Define Core Domain Model    | Core types exist for workspace, project, docs, and checks |
| WP-v0-004 | Parse `workspace.toml`      | CLI can read and validate manifest                        |
| WP-v0-005 | Implement `monad init`      | CLI can generate a repo foundation                        |
| WP-v0-006 | Implement Interactive Init  | CLI can collect answers and save recommendations          |
| WP-v0-007 | Implement `monad doctor`    | CLI can validate foundation files                         |
| WP-v0-008 | Implement `monad inspect`   | CLI can summarize workspace state                         |
| WP-v0-009 | Generate Foundational Docs  | CLI can generate baseline docs                            |
| WP-v0-010 | Create Local `.monad` State | CLI owns local machine-readable state                     |
| WP-v0-011 | Add Test Coverage           | Core behavior has tests                                   |
| WP-v0-012 | Add Developer Tooling       | Build, test, format, and lint workflow exists             |
| WP-v0-013 | Add CI Baseline             | GitHub Actions validates v0                               |
| WP-v0-014 | Add v0 Release Checklist    | v0 has explicit release gate                              |
| WP-v0-015 | Cut v0 Tag                  | First usable local release exists                         |

---

# 4. WP-v0-001: Create Rust Workspace

## Objective

Create the initial Rust workspace for the Monad OS CLI.

## Rationale

ADR-0002 selected Rust for the CLI core.

The initial workspace should be small and expandable.

## Target Structure

```txt
Cargo.toml
crates/
  monad-cli/
    Cargo.toml
    src/
      main.rs
  monad-core/
    Cargo.toml
    src/
      lib.rs
```

## Tasks

### Task 1: Create Rust workspace files

Create:

```txt
Cargo.toml
crates/monad-cli/Cargo.toml
crates/monad-cli/src/main.rs
crates/monad-core/Cargo.toml
crates/monad-core/src/lib.rs
```

### Task 2: Configure workspace members

Root `Cargo.toml` should declare:

```toml
[workspace]
members = [
  "crates/monad-cli",
  "crates/monad-core"
]
resolver = "2"
```

### Task 3: Add initial dependencies

Recommended initial dependencies:

```txt
clap
anyhow
thiserror
serde
serde_json
toml
```

Possible later dependencies:

```txt
dialoguer
inquire
owo-colors
camino
walkdir
schemars
```

## Acceptance Criteria

This work package is complete when:

```bash
cargo check
```

passes.

And:

```bash
cargo run -p monad-cli
```

runs without crashing.

---

# 5. WP-v0-002: Create CLI Skeleton

## Objective

Create the first `monad` command surface.

## Commands

Initial commands:

```bash
monad --help
monad version
monad init
monad doctor
monad inspect
```

## Tasks

### Task 1: Add Clap command parser

Use `clap` derive or builder API.

### Task 2: Add version command

The command:

```bash
monad version
```

should print:

```txt
monad 0.1.0
```

or the package version.

### Task 3: Add placeholder commands

Before implementation, placeholder commands may print:

```txt
not implemented yet
```

for:

```txt
init
doctor
inspect
```

## Acceptance Criteria

This work package is complete when:

```bash
cargo run -p monad-cli -- --help
cargo run -p monad-cli -- version
```

both work.

---

# 6. WP-v0-003: Define Core Domain Model

## Objective

Create the first domain types in `monad-core`.

## Rationale

Monad OS should not become only a command script.

The core crate should contain reusable logic and domain types.

## Initial Types

Create types for:

```txt
Workspace
WorkspaceIdentity
WorkspacePrinciples
ToolchainDefaults
DocsConfig
InitOptions
DoctorCheck
DoctorResult
InspectionReport
Recommendation
```

## Suggested Module Structure

```txt
crates/monad-core/src/
  lib.rs
  workspace.rs
  manifest.rs
  init.rs
  doctor.rs
  inspect.rs
  recommendation.rs
  fs.rs
```

## Acceptance Criteria

This work package is complete when:

1. Domain types compile.
2. Types are serializable where appropriate.
3. CLI can import `monad-core`.
4. Basic unit tests exist for at least one core module.

---

# 7. WP-v0-004: Parse `workspace.toml`

## Objective

Allow Monad OS to read and validate the root `workspace.toml`.

## Rationale

ADR-0003 selected `workspace.toml` as the canonical manifest.

## Tasks

### Task 1: Define manifest schema

Initial manifest sections:

```toml
[workspace]
name = "monad-os"
stage = "pre-implementation"

[identity]
category = "AI-native SDLC Control Plane"
product = "Monad OS"

[principles]
local_first = true
ai_agnostic = true
cloud_agnostic = true
database_agnostic = true

[docs]
canonical_docs_dir = "docs"
default_docs_frontend = "fumadocs"

[toolchain.defaults]
cli_language = "rust"
package_manager = "bun"
task_backend_default = "nx-under-monad-wrapper"
```

### Task 2: Implement parser

Create function:

```txt
load_workspace_manifest(path) -> WorkspaceManifest
```

### Task 3: Implement validation

Validate:

```txt
workspace.name exists
identity.product exists
docs.canonical_docs_dir exists or is recommended
principles are parseable
```

## Acceptance Criteria

This work package is complete when:

```bash
monad inspect
```

can read `workspace.toml`.

Unit tests should cover:

```txt
valid manifest
missing file
invalid TOML
missing required field
```

---

# 8. WP-v0-005: Implement `monad init`

## Objective

Create the first useful workspace generator.

## Command

```bash
monad init
```

## Behavior

When run in an empty or mostly empty directory, it should create:

```txt
README.md
AGENTS.md
workspace.toml
docs/
docs/00-index.md
docs/product/
docs/product/charter.md
docs/product/prd.md
docs/architecture/
docs/decisions/
docs/decisions/decision-backlog.md
docs/governance/
docs/governance/principles.md
docs/roadmap/
docs/roadmap/initial-implementation-sequence.md
scripts/
scripts/check-foundation.sh
.monad/
.monad/state/
```

## Safety Requirements

`monad init` should not overwrite existing files unless explicitly forced.

Recommended flags:

```bash
monad init --force
monad init --dry-run
```

For v0, `--force` may be deferred.

## Acceptance Criteria

This work package is complete when:

1. `monad init` creates the baseline files.
2. Existing files are not silently overwritten.
3. Generated repo passes `scripts/check-foundation.sh`.
4. Running `monad init` twice is safe.

---

# 9. WP-v0-006: Implement Interactive Init

## Objective

Create the first interactive recommendation flow.

## Command

```bash
monad init --interactive
```

## Rationale

Monad OS should eventually recommend optimal repo structure, tools, policies, and workflows based on user answers.

v0 should start small.

## Questions

Initial wizard questions:

```txt
Workspace name?
Primary use case?
Private or public?
Primary language?
Primary package manager?
Docs frontend?
Task backend?
Local-first only or SaaS-ready?
Use AI features later?
Preferred AI mode?
Cloud target?
Database strategy?
Governance level?
```

## Default Recommendations

For Monad OS itself, defaults are:

```txt
CLI language: Rust
Package manager: Bun
Docs frontend: Fumadocs
Task backend: Nx under Monad wrapper
Local mode: local-first, SaaS-ready
AI mode: no-AI by default, AI-ready later
Cloud strategy: local-first, cloud-portable
Database strategy: capability-based, no local core DB required
Governance: startup-default plus AI-governance-ready
```

## Generated Files

```txt
.monad/answers.yaml
.monad/recommendation.json
```

## Acceptance Criteria

This work package is complete when:

1. `monad init --interactive` asks questions.
2. Defaults are sensible.
3. Answers are saved.
4. Recommendations are saved.
5. Generated repo remains valid.

---

# 10. WP-v0-007: Implement `monad doctor`

## Objective

Create the first validation command.

## Command

```bash
monad doctor
```

## Checks

Initial checks:

```txt
README.md exists
AGENTS.md exists
workspace.toml exists
docs/00-index.md exists
docs/product/charter.md exists
docs/product/prd.md exists
docs/decisions/ exists
docs/decisions/decision-backlog.md exists
docs/governance/principles.md exists
scripts/check-foundation.sh exists
.monad/ exists
```

## Output

Good output:

```txt
Monad Doctor

PASS README.md exists
PASS AGENTS.md exists
PASS workspace.toml exists
PASS docs/00-index.md exists

Foundation status:
  healthy
```

Bad output:

```txt
FAIL docs/product/prd.md missing

Suggested fix:
  monad init
```

## Exit Codes

Recommended:

```txt
0 = healthy
1 = failed checks
2 = invalid command/configuration
```

## Acceptance Criteria

This work package is complete when:

1. `monad doctor` reports pass/fail checks.
2. Missing files cause non-zero exit.
3. Output is readable.
4. Tests cover pass and fail cases.

---

# 11. WP-v0-008: Implement `monad inspect`

## Objective

Summarize the current workspace.

## Command

```bash
monad inspect
```

## Output Should Include

```txt
workspace name
product identity
stage
principles
docs directory
toolchain defaults
detected docs count
detected ADR count
detected implementation docs count
foundation health summary
```

## Example Output

```txt
Monad Workspace

Name:
  monad-os

Product:
  Monad OS

Category:
  AI-native SDLC Control Plane

Principles:
  local-first
  AI-agnostic
  cloud-agnostic
  database-agnostic

Docs:
  docs/

ADRs:
  15 accepted

Status:
  foundation healthy
```

## Acceptance Criteria

This work package is complete when:

1. `monad inspect` reads `workspace.toml`.
2. It summarizes docs and ADRs.
3. It handles missing manifest clearly.
4. It does not require SaaS or network access.

---

# 12. WP-v0-009: Generate Foundational Docs

## Objective

Ensure `monad init` can generate baseline documentation.

## Docs To Generate

```txt
README.md
AGENTS.md
docs/00-index.md
docs/product/charter.md
docs/product/prd.md
docs/architecture/technical-product-blueprint.md
docs/architecture/sdlc-control-plane.md
docs/architecture/toolchain-strategy.md
docs/architecture/agnosticity.md
docs/architecture/competitive-moat.md
docs/decisions/decision-backlog.md
docs/governance/principles.md
docs/roadmap/initial-implementation-sequence.md
```

## Content Requirements

Generated docs should be:

```txt
useful
brief enough for generated defaults
editable
clearly marked as generated starter content where appropriate
```

## Acceptance Criteria

This work package is complete when:

1. `monad init` creates docs.
2. Docs are internally linked from `docs/00-index.md`.
3. Generated docs are suitable for commit.
4. `monad doctor` validates them.

---

# 13. WP-v0-010: Create Local `.monad` State

## Objective

Create the local state directory.

## Directory

```txt
.monad/
```

## Initial Structure

```txt
.monad/
  state/
  answers.yaml
  recommendation.json
```

For non-interactive init, `answers.yaml` may be omitted.

## Future Structure

```txt
.monad/
  graph.json
  projects.json
  context/
  evidence/
  policy-results/
  file-ownership.json
```

## Acceptance Criteria

This work package is complete when:

1. `.monad/` is created by `monad init`.
2. `.monad/state/` exists.
3. Interactive answers can be saved.
4. Recommendations can be saved.
5. Files are deterministic enough to commit or inspect.

---

# 14. WP-v0-011: Add Test Coverage

## Objective

Add basic automated test coverage.

## Test Types

Initial tests:

```txt
unit tests for manifest parsing
unit tests for doctor checks
unit tests for init file planning
unit tests for recommendation defaults
CLI smoke tests
```

## Recommended Test Approach

Use:

```txt
Rust unit tests
temporary directories
assert_cmd later if useful
insta snapshots later if useful
```

## Acceptance Criteria

This work package is complete when:

```bash
cargo test
```

passes.

Minimum coverage expectations:

```txt
manifest parser tested
doctor checks tested
init plan tested
```

---

# 15. WP-v0-012: Add Developer Tooling

## Objective

Create a repeatable developer workflow.

## Commands

Recommended root scripts eventually:

```bash
cargo fmt
cargo clippy --all-targets --all-features -- -D warnings
cargo test
cargo check
```

Optional helper script:

```txt
scripts/dev-check.sh
```

## Create Script

```txt
scripts/dev-check.sh
```

Should run:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test
cargo check
```

## Acceptance Criteria

This work package is complete when:

```bash
./scripts/dev-check.sh
```

passes.

---

# 16. WP-v0-013: Add CI Baseline

## Objective

Add GitHub Actions validation.

## File

```txt
.github/workflows/ci.yml
```

## Jobs

Initial jobs:

```txt
cargo fmt
cargo clippy
cargo test
cargo check
foundation check
```

## Acceptance Criteria

This work package is complete when:

1. CI runs on pull requests.
2. CI runs on pushes to main.
3. CI validates Rust.
4. CI validates foundation docs.
5. CI is documented.

---

# 17. WP-v0-014: Add v0 Release Checklist

## Objective

Define explicit release readiness criteria.

## File

```txt
docs/release/v0-release-checklist.md
```

## Checklist Should Include

```txt
all tests pass
cargo fmt passes
cargo clippy passes
monad init works
monad doctor works
monad inspect works
docs are updated
ADRs are accepted
roadmap is updated
version is set
tag is created
```

## Acceptance Criteria

This work package is complete when:

1. Release checklist exists.
2. Checklist is linked from docs index.
3. v0 cannot be considered complete without passing it.

---

# 18. WP-v0-015: Cut v0 Tag

## Objective

Create the first v0 release marker.

## Commands

When v0 is ready:

```bash
git tag v0.0.0
git push origin v0.0.0
```

or, if using semantic pre-release:

```bash
git tag v0.1.0-alpha.0
git push origin v0.1.0-alpha.0
```

## Recommended Initial Tag

```txt
v0.1.0-alpha.0
```

## Acceptance Criteria

This work package is complete when:

1. v0 release checklist passes.
2. Git tag exists.
3. Release notes exist.
4. Repository can be cloned and validated locally.

---

# 19. Recommended Build Order

Execute work packages in this order:

```txt
WP-v0-001 Create Rust Workspace
WP-v0-002 Create CLI Skeleton
WP-v0-003 Define Core Domain Model
WP-v0-004 Parse workspace.toml
WP-v0-005 Implement monad init
WP-v0-007 Implement monad doctor
WP-v0-008 Implement monad inspect
WP-v0-006 Implement Interactive Init
WP-v0-009 Generate Foundational Docs
WP-v0-010 Create Local .monad State
WP-v0-011 Add Test Coverage
WP-v0-012 Add Developer Tooling
WP-v0-013 Add CI Baseline
WP-v0-014 Add v0 Release Checklist
WP-v0-015 Cut v0 Tag
```

Note that `doctor` can be implemented before the full interactive wizard because it validates generated structure and improves feedback during development.

---

# 20. Definition of Done for v0

v0 is done when all of the following are true:

```txt
Rust workspace compiles.
monad --help works.
monad version works.
monad init works.
monad init --interactive works.
monad doctor works.
monad inspect works.
workspace.toml is parsed.
.monad/ state exists.
recommendation output exists.
foundation docs are generated.
foundation check passes.
tests pass.
developer check script passes.
CI passes.
release checklist exists.
```

---

# 21. v0 Quality Bar

v0 should be:

```txt
small
local-first
deterministic
documented
testable
safe to run
non-destructive by default
easy to understand
easy to commit
```

v0 should not be:

```txt
over-abstracted
SaaS-dependent
provider-dependent
AI-dependent
plugin-heavy
marketplace-focused
enterprise-heavy
```

---

# 22. Current Next Step

The next implementation artifact should be:

```txt
docs/implementation/v0-command-spec.md
```

That document should define the exact CLI command interface for v0 before code is written.


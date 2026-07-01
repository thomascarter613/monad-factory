# Monad OS Roadmap: v0 to v2

## Status

Draft v0.1

## Date

2026-06-29

## Purpose

This roadmap translates the Monad OS product charter, PRD, and initial foundational ADR series into an implementation sequence.

It covers:

- v0
- v0.1
- v0.2
- v1
- v1.5
- v2

The roadmap is intentionally phased.

Monad OS should begin with a useful local-first core, then evolve toward a governed, extensible, SaaS-ready SDLC control plane.

---

# 1. Product Direction

Monad OS is an:

```txt
AI-agnostic SDLC Control Plane
```

and a:

```txt
Monorepo Operating System
```

The long-term product goal is to help software teams govern, understand, generate, validate, evolve, and operate software systems through one lifecycle-aware control plane.

Monad OS should connect:

```txt
strategy
requirements
architecture
documentation
repo structure
code
tasks
policies
evidence
builds
tests
releases
deployments
incidents
AI workflows
```

The local core comes first.

The hosted SaaS control plane comes later.

---

# 2. Roadmap Principles

The roadmap follows these principles.

## 2.1 Local First

The core must work without SaaS.

## 2.2 SaaS Ready

Local artifacts should be structured so they can sync to a hosted control plane later.

## 2.3 AI Agnostic

AI is optional and provider-neutral.

## 2.4 Cloud Agnostic

No cloud provider is mandatory.

## 2.5 Database Agnostic

No database is mandatory for the local core.

## 2.6 Toolchain Composable

Monad wraps native tools instead of replacing every tool.

## 2.7 Graph Native

The lifecycle graph is the core moat.

## 2.8 Evidence Oriented

Important lifecycle actions should eventually produce evidence.

## 2.9 Policy Controlled

Governance should be expressible through policy packs.

## 2.10 Human Governed AI

Risky AI actions require human approval.

---

# 3. Version Overview

```txt
v0:
  Establish the Rust CLI and local workspace foundation.

v0.1:
  Add docs app foundation, baseline tooling, and first practical checks.

v0.2:
  Add generators, project registry, simple graph, policy checks, and evidence basics.

v1:
  Stabilize the local-first product.

v1.5:
  Add extensibility through packs, stronger graph/evidence/policy models, and migration recipes.

v2:
  Introduce hosted SaaS control plane, multi-repo graph, evidence vault, dashboards, integrations, and marketplace.
```

---

# 4. v0: Local Core Foundation

## Goal

Create the first functional local Monad CLI and workspace foundation.

v0 should prove that Monad OS can exist as a local-first product.

## Primary Outcome

A user can initialize, inspect, and validate a Monad OS workspace locally.

## Scope

### CLI Foundation

Create Rust workspace:

```txt
crates/
  monad-cli/
  monad-core/
```

Initial binary:

```bash
monad
```

Initial commands:

```bash
monad --help
monad version
monad init
monad init --interactive
monad doctor
monad inspect
```

### Workspace Manifest

Establish:

```txt
workspace.toml
```

The manifest should include initial sections for:

```txt
workspace identity
principles
toolchain defaults
docs defaults
build strategy
AI strategy
cloud strategy
data strategy
policy strategy
sync strategy
```

### Local Repo Foundation

`monad init` should generate a useful baseline:

```txt
README.md
AGENTS.md
workspace.toml
docs/
docs/product/
docs/architecture/
docs/decisions/
docs/governance/
docs/roadmap/
scripts/
```

### Recommendation Output

`monad init --interactive` should collect answers and generate:

```txt
.monad/answers.yaml
.monad/recommendation.json
```

### Doctor Checks

`monad doctor` should validate the foundation.

Initial checks:

```txt
README.md exists
AGENTS.md exists
workspace.toml exists
docs/ exists
docs/product/charter.md exists or is recommended
docs/product/prd.md exists or is recommended
docs/decisions/ exists
```

### Documentation

Initial docs should explain:

```txt
what Monad OS is
how to initialize a workspace
how workspace.toml works
how ADRs work
how local-first mode works
```

## Explicit Non-Goals

v0 does not need:

```txt
full Fumadocs app
full Nx integration
full policy engine
full evidence engine
full lifecycle graph
hosted SaaS
plugin runtime
marketplace
AI provider integration
```

## v0 Acceptance Criteria

v0 is complete when:

1. `monad --help` works.
2. `monad init` creates a valid workspace.
3. `monad init --interactive` records answers.
4. `monad doctor` validates the generated foundation.
5. `workspace.toml` is parsed.
6. Basic docs are generated.
7. No SaaS account is required.
8. The repo can be committed and re-run deterministically.

---

# 5. v0.1: Practical Tooling and Documentation Foundation

## Goal

Make Monad OS useful for a real local repository with docs, basic tooling, and initial task backend support.

## Primary Outcome

A user can generate a docs-ready, JS/TS-friendly monorepo foundation using Monad.

## Scope

### Fumadocs Foundation

Generate:

```txt
apps/docs/
```

Using Fumadocs as the default documentation frontend.

Canonical docs remain in:

```txt
docs/
```

Rendered docs app lives in:

```txt
apps/docs/
```

### Bun Baseline

Add Bun workspace support.

Files may include:

```txt
package.json
bun.lock
```

### Biome Baseline

Add formatting and linting baseline.

Files may include:

```txt
biome.json
```

### Nx Baseline

Add Nx as the approved initial JS/TS backend under Monad wrapper.

Files may include:

```txt
nx.json
project.json
```

Initial wrapped commands:

```bash
monad run docs:dev
monad run docs:build
monad graph
```

### GitHub Actions Baseline

Generate CI workflow:

```txt
.github/workflows/ci.yml
```

Initial CI jobs:

```txt
format
lint
typecheck
test
doctor
```

### Lefthook Baseline

Generate:

```txt
lefthook.yml
```

Initial hooks:

```txt
format check
lint check
secret scan placeholder
```

### CODEOWNERS

Generate:

```txt
.github/CODEOWNERS
```

### Renovate

Generate:

```txt
renovate.json
```

### Docs Checks

Add:

```bash
monad docs check
```

Checks:

```txt
docs index exists
required product docs exist
required ADR directory exists
no broken obvious relative links where easily detectable
```

## v0.1 Acceptance Criteria

v0.1 is complete when:

1. `monad init --profile js-ts-docs` can generate a JS/TS docs-ready repo.
2. `apps/docs` exists and can run locally.
3. Bun baseline works.
4. Biome baseline works.
5. Nx baseline works for docs tasks.
6. GitHub Actions baseline exists.
7. Lefthook baseline exists.
8. CODEOWNERS exists.
9. Renovate config exists.
10. `monad docs check` runs locally.

---

# 6. v0.2: Generators, Registry, Policy, Evidence, and Graph Basics

## Goal

Move from static repo initialization to repeatable generation and validation.

## Primary Outcome

A user can add apps, packages, and services through Monad, and Monad updates its local model.

## Scope

### Project Registry

Introduce a generated or maintained local registry.

Possible file:

```txt
.monad/projects.json
```

or manifest-backed project declarations in:

```txt
workspace.toml
```

Track:

```txt
project id
project name
project type
path
language
framework
owner
targets
docs path
```

### Generators

Add commands:

```bash
monad add app
monad add package
monad add service
```

Initial generator examples:

```txt
app docs
app web
package typescript-library
service elysia
service fastapi
```

### Generated Docs

Generators should create documentation stubs.

Examples:

```txt
docs/apps/<name>.md
docs/packages/<name>.md
docs/services/<name>.md
```

### Graph Output

Add:

```bash
monad graph --json
monad graph --mermaid
```

Initial graph nodes:

```txt
Workspace
Project
Document
Decision
Policy
Evidence
```

Possible output:

```txt
.monad/graph.json
```

### Simple Policy Checks

Add:

```bash
monad policy check
monad policy list
```

Initial policy scope:

```txt
required files
required directories
required docs
basic protected paths
```

### Evidence Basics

Add simple local evidence output.

Possible directory:

```txt
.monad/evidence/
```

Evidence commands:

```bash
monad evidence list
monad evidence collect --type foundation
```

### AI Context Basics

Add:

```bash
monad ai context
```

Generate:

```txt
.monad/context/repo-map.md
.monad/context/current-state.md
.monad/context/handoff.md
```

No AI provider integration is required.

## v0.2 Acceptance Criteria

v0.2 is complete when:

1. `monad add app` works.
2. `monad add package` works.
3. `monad add service` works for at least one service type.
4. Generated projects are registered.
5. Generated projects have docs.
6. `monad graph --json` produces a useful graph.
7. `monad policy check` runs.
8. `monad evidence collect --type foundation` creates evidence.
9. `monad ai context` creates provider-neutral context files.
10. All generated files are explainable.

---

# 7. v1: Stable Local-First Product

## Goal

Deliver a stable local-first Monad OS release.

## Primary Outcome

A user can use Monad OS as the governing local control plane for a serious monorepo.

## Scope

### Stable CLI Surface

Stabilize commands:

```bash
monad init
monad doctor
monad inspect
monad run
monad affected
monad graph
monad docs check
monad policy check
monad evidence collect
monad ai context
monad add app
monad add package
monad add service
```

### Manifest v1

Stabilize `workspace.toml` schema v1.

Must support:

```txt
workspace identity
projects
toolchain defaults
docs config
AI mode
cloud strategy
data strategy
policy config
sync disabled/local-only config
```

### Documentation v1

Complete docs for:

```txt
getting started
CLI reference
workspace.toml reference
docs architecture
ADR process
generator system
policy basics
evidence basics
AI context basics
tool wrapping
Nx under Monad
local-first mode
```

### Nx Wrapper v1

Support:

```bash
monad run <project>:<target>
monad affected test
monad affected build
```

### Policy v1

Support baseline local policy packs:

```txt
startup-default
ai-governance
```

Policy outputs should be CI-friendly.

### Evidence v1

Support evidence for:

```txt
doctor checks
policy checks
docs checks
build/test command results where feasible
AI context generation
```

### Graph v1

Support graph outputs:

```txt
JSON
Mermaid
DOT optional
Markdown report optional
```

Graph should include:

```txt
workspace
projects
docs
ADRs
policies
evidence
tooling
```

### AI Context v1

Support provider-neutral context packs.

No specific AI provider should be required.

### Security Baseline

Include:

```txt
secret scanning recommendation
protected paths model
AI approval gate docs
dependency update docs
basic supply-chain docs
```

## v1 Acceptance Criteria

v1 is complete when:

1. A new user can create a real local-first monorepo with Monad.
2. CLI commands are documented and stable.
3. Manifest schema is documented.
4. Docs app can be generated.
5. Nx-backed workflows work where selected.
6. App/package/service generators work.
7. Policy checks work locally and in CI.
8. Evidence files are generated locally.
9. AI context files are generated without AI provider lock-in.
10. Graph output is useful and documented.
11. No SaaS account is required.
12. The project is credible as a local-first open-source core.

---

# 8. v1.5: Extensibility, Migration, and Advanced Local Intelligence

## Goal

Evolve Monad OS from a fixed local tool into an extensible local ecosystem.

## Primary Outcome

Users can install and use packs, run richer policy/evidence workflows, and perform migration/modernization recipes.

## Scope

### Pack System

Introduce local declarative packs.

Commands:

```bash
monad pack list
monad pack inspect <pack>
monad pack apply <pack>
```

Pack types:

```txt
app
service
package
docs
policy
workflow
migration
infrastructure
```

### Pack Manifest

Add:

```txt
pack.toml
```

### Pack Locking

Consider:

```txt
monad.lock
```

Track:

```txt
installed packs
pack versions
plugin versions where applicable
generator versions
```

### Migration Recipes

Add migration packs such as:

```txt
polyrepo-to-monorepo
legacy-docs-to-fumadocs
npm-to-bun
ungoverned-repo-to-monad
```

### Advanced Policy

Add:

```txt
waivers
exceptions
policy severity
advisory/warn/fail modes
policy evidence
```

### Advanced Evidence

Add:

```txt
evidence schemas
evidence verification
evidence reports
release evidence bundle prototype
```

### Advanced Graph

Add:

```txt
graph query basics
impact analysis
traceability reports
docs-to-project links
ADR-to-project links
policy-to-evidence links
```

### Plugin Contract Design

Design plugin system, but do not necessarily allow arbitrary third-party executable plugins yet.

Potential plugin types:

```txt
backend adapters
provider adapters
evidence collectors
policy evaluators
integration connectors
```

### Local Reports

Generate reports:

```bash
monad report maturity
monad report evidence
monad report architecture
monad report ai-readiness
```

## v1.5 Acceptance Criteria

v1.5 is complete when:

1. Local packs work.
2. Pack manifests are documented.
3. Policy packs are useful.
4. Evidence reports are useful.
5. Migration recipes can be applied safely.
6. Lifecycle graph supports impact and traceability basics.
7. Plugin contracts are designed.
8. Monad OS is credible for productized consulting workflows.

---

# 9. v2: Hosted SaaS Control Plane

## Goal

Introduce the hosted Monad OS SaaS control plane.

## Primary Outcome

Teams can sync local Monad artifacts to a hosted platform for multi-repo graph, evidence vault, dashboards, policy visibility, integration sync, and marketplace access.

## Scope

### Hosted Control Plane

Build web application and API.

Core SaaS modules:

```txt
organizations
users
teams
repositories
sync
lifecycle graph
evidence vault
policy dashboard
maturity analytics
integration sync
marketplace
```

### Multi-Repo Lifecycle Graph

Support:

```txt
cross-repo graph
historical graph
evidence graph
policy graph
release graph
ownership graph
```

### Evidence Vault

Support:

```txt
evidence ingestion
evidence search
evidence retention
evidence export
control mapping
release evidence bundles
audit packages
```

### Policy Management

Support:

```txt
organization-level policy packs
policy versioning
waivers
exceptions
approval workflows
policy history
```

### Integration Sync

Initial integrations may include:

```txt
GitHub
GitLab
Linear
Jira
Slack
Notion
monday.com
Backstage
CI systems
observability tools
security scanners
```

### Marketplace

Support:

```txt
official packs
verified packs
private packs
organization catalogs
policy packs
migration packs
integration plugins
```

### Enterprise Features

Add:

```txt
SSO
SAML/OIDC
SCIM
RBAC
audit logs
single-tenant deployment
self-hosted deployment
air-gapped mode planning
```

### Hosted AI Governance

Optional future SaaS capabilities:

```txt
AI action dashboard
AI evidence vault
model/provider inventory
approval workflows
AI risk reports
organization AI policies
```

## v2 Acceptance Criteria

v2 is complete when:

1. Local CLI can explicitly sync selected artifacts.
2. Hosted SaaS can ingest repositories.
3. Multi-repo lifecycle graph works.
4. Evidence vault works.
5. Policy dashboard works.
6. Basic maturity analytics exist.
7. Marketplace foundation exists.
8. At least one major integration works.
9. Enterprise access controls are started.
10. SaaS extends local workflows instead of replacing them.

---

# 10. Workstream Breakdown

## Workstream A: CLI Core

Owns:

```txt
Rust workspace
command routing
errors
configuration
terminal UX
interactive wizard
```

## Workstream B: Manifest and Schema

Owns:

```txt
workspace.toml
schema versioning
validation
manifest reference docs
```

## Workstream C: Generators

Owns:

```txt
repo init
apps
packages
services
docs generation
project registry updates
```

## Workstream D: Toolchain Adapters

Owns:

```txt
Nx
Bun
Biome
Lefthook
GitHub Actions
future moon/Buck2/Pants/Dagger/Nix
```

## Workstream E: Docs System

Owns:

```txt
canonical docs
Fumadocs app
docs checks
docs reference
tutorials
```

## Workstream F: Policy

Owns:

```txt
policy packs
policy checks
policy results
waivers
policy evidence
```

## Workstream G: Evidence

Owns:

```txt
evidence schemas
evidence collection
evidence reports
release evidence
future evidence vault sync
```

## Workstream H: Lifecycle Graph

Owns:

```txt
graph model
graph generation
graph outputs
impact analysis
traceability
future hosted graph
```

## Workstream I: AI Context and Governance

Owns:

```txt
AI-agnostic context packs
protected paths
risk classification
approval gates
AI action evidence
```

## Workstream J: Packs and Plugins

Owns:

```txt
pack format
pack commands
plugin contracts
marketplace readiness
```

## Workstream K: SaaS

Owns:

```txt
hosted API
dashboard
sync
multi-tenancy
evidence vault
marketplace
enterprise admin
```

---

# 11. Recommended Implementation Order

The recommended order after the foundational docs is:

```txt
1. Create Rust workspace.
2. Create monad-cli and monad-core crates.
3. Implement monad --help and monad version.
4. Implement workspace.toml parsing.
5. Implement monad init.
6. Implement monad doctor.
7. Implement monad init --interactive.
8. Generate .monad/answers.yaml and .monad/recommendation.json.
9. Add docs generation.
10. Add Fumadocs app generation.
11. Add Bun/Biome baseline.
12. Add Nx baseline.
13. Add monad run wrapper.
14. Add graph JSON output.
15. Add policy check basics.
16. Add evidence basics.
17. Add AI context generation.
18. Add app/package/service generators.
19. Stabilize v1.
20. Add packs.
21. Add advanced graph/evidence/policy.
22. Build SaaS.
```

---

# 12. Release Gates

Each version should pass gates before release.

## v0 Gate

```txt
CLI compiles
basic commands work
init works
doctor works
docs exist
no SaaS required
```

## v0.1 Gate

```txt
docs app works
tooling baseline works
CI baseline works
Nx wrapper basics work
docs check works
```

## v0.2 Gate

```txt
generators work
graph output works
policy check works
evidence output works
AI context output works
```

## v1 Gate

```txt
stable CLI
stable manifest
stable docs
stable generators
stable policy basics
stable evidence basics
stable graph basics
usable local-first product
```

## v1.5 Gate

```txt
packs work
migration recipes work
advanced local reports work
plugin contracts documented
productized service workflows credible
```

## v2 Gate

```txt
hosted sync works
multi-repo graph works
evidence vault works
policy dashboard works
marketplace foundation works
enterprise controls started
```

---

# 13. Strategic Deferrals

Do not build these too early:

```txt
hosted SaaS
full marketplace
arbitrary plugin runtime
full compliance automation
full AI agent execution
full graph database
enterprise self-hosted deployment
air-gapped support
Buck2/Pants implementation
complex policy language
```

These are important, but they should come after the local core proves value.

---

# 14. Current Next Step

The next recommended implementation artifact after this roadmap is:

```txt
docs/implementation/v0-work-packages.md
```

That document should break v0 into concrete work packages, tasks, subtasks, commands, files, and acceptance criteria.

---

# 15. Final Roadmap Statement

Monad OS should progress from:

```txt
local CLI foundation
```

to:

```txt
stable local-first monorepo operating system
```

to:

```txt
extensible policy/evidence/graph platform
```

to:

```txt
hosted SaaS SDLC control plane
```

without sacrificing the foundational principles:

```txt
local-first
AI-agnostic
cloud-agnostic
database-agnostic
toolchain-composable
policy-controlled
evidence-oriented
graph-native
human-governed
```


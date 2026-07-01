---
title: "Monad Factory v1 Maximal Functional Scope and Delivery Plan"
description: "Canonical repo-ready scope and delivery plan for Monad Factory v1 as a maximal functional, polyglot, AI-ready, governance-grade monorepo product-factory platform."
status: "approved"
version: "0.1.0"
created: "2026-07-01"
updated: "2026-07-01"
owner: "Thomas Carter"
canonical: true
source: "Approved planning artifact normalized for maximal functional v1 repository use"
intended_path: "docs/product/v1-maximal-functional-scope-and-delivery-plan.md"
tags:
  - monad-factory
  - monorepo
  - product-factory
  - polyglot
  - maximal-functional-v1
  - ai-memory
  - agentic-development
  - governance
  - policy-as-code
  - platform
  - planning
---

# Monad Factory v1 Maximal Functional Scope and Delivery Plan

## 1. Executive Summary

`monad-factory` is a maximal functional, local-first, polyglot, AI-ready, governance-grade monorepo product-factory platform.

It provides a complete repository foundation, root control plane, first-class polyglot language baselines, local infrastructure, GitHub automation, Docker and container workflows, publishing workflows, policy and governance systems, contract management, template generation, plugin/marketplace foundations, optional AI-assisted development, autonomous agent workflow capabilities, and a full local-first memory/context/handoff system called **Monad Memory**.

The v1 release is not a narrow starter and not a minimal proof of concept. It is the first complete functional release of the Monad Factory platform. It should be usable locally by a solo developer, but it should also establish the architecture, commands, workflows, governance, and extensibility model needed for serious product-factory use across many future products.

The v1 release is intentionally ambitious. Scope control is achieved through implementation sequencing, clear acceptance criteria, and explicit verification gates — not by moving approved capabilities out of v1.

---

## 2. Scope Interpretation

This document supersedes earlier narrow MVP framing.

The approved v1 direction is:

```txt
Everything approved for v1 is core/maximal functional v1 scope.
Nothing in v1 is minimal, experimental, preview-only, scaffold-only, disabled-by-default-only, or post-v1.
```

This means capabilities previously described as stretch, future, preview, or post-v1 are now included in v1 as functional deliverables.

The v1 release may still be local-first and may still allow users to opt out of features they do not need. However, optional user adoption is different from incomplete implementation. A feature may be optional to use, but if it is in v1 scope, it must be functionally implemented.

---

## 3. Product Identity

### 3.1 Name

Repository:

```txt
monad-factory
```

CLI:

```txt
monad
```

### 3.2 Product Category

`monad-factory` is a:

```txt
Polyglot, AI-ready, governance-grade monorepo product-factory platform
```

It is also the seed of a future:

```txt
Monorepo operating system
```

### 3.3 Primary User

The primary v1 user is:

```txt
A solo developer, founder, advanced builder, consultant, platform engineer, AI-assisted developer, or small technical team that wants a serious reusable monorepo platform for many future products.
```

### 3.4 Core Promise

`monad-factory` gives the user a production-minded, maximal functional v1 platform that is:

```txt
local-first
GitHub-ready
Docker-ready
cloud-ready
Kubernetes-ready
AI-ready
AI-optional from the user perspective
polyglot from day one
governance-grade
policy-aware
template-driven
memory-aware
agent-ready
publish-ready
multi-product-ready
multi-repo-ready
organization-ready
structured for reuse across many products
```

---

## 4. v1 Governing Principle

The governing v1 principle is:

```txt
Monad Factory v1 should provide a complete functional product-factory platform surface, while preserving local-first usability and clean separation between required local development and optional advanced operating modes.
```

This means:

1. Users should be able to clone and use the repo locally.
2. Users should be able to run the core local checks without cloud credentials.
3. Users should be able to use the platform without an LLM.
4. Users should also have functional v1 support for AI workflows, memory, agents, daemon mode, vector memory, policy-as-code, deployment, publishing, plugins, marketplace structure, and multi-repo governance.
5. Advanced features may require configuration, credentials, or infrastructure when actually used, but the v1 implementation must be real and documented.

---

## 5. What v1 Will Be

For v1, `monad-factory` will be:

1. A reusable monorepo starter.
2. A polyglot product-factory platform.
3. A local-first development environment.
4. A governed repository skeleton with docs, policies, ADRs, and conventions.
5. A working multi-language reference repo containing:
   - Next.js web app
   - TypeScript API service
   - Rust CLI/core crates
   - Rust API/service example
   - Go API service
   - Python FastAPI service
   - Java service
6. A root-level task orchestration system using `moon`.
7. A root-level toolchain/version management system using `mise`.
8. A JS/TS workspace using `Bun`.
9. A quality baseline using Biome, language-native linters, tests, and CI.
10. A GitHub-ready repository with issue templates, PR templates, CODEOWNERS, workflows, and governance automation.
11. A Docker Compose local infrastructure baseline.
12. A documentation-first platform with YAML frontmatter on meaningful Markdown documents.
13. A Rust-based `monad` CLI as the public control plane.
14. A full optional-to-use but functionally implemented LLM-agnostic memory/context/handoff system called **Monad Memory**.
15. A semantic/vector memory system with SQLite, pgvector, and Qdrant support.
16. A daemon mode for local indexing, repo graph updates, memory maintenance, and context freshness.
17. A policy-as-code foundation with functional policy checks.
18. A full Nx adapter/wrapper for graph, affected detection, and cache integration.
19. A functional template generation system.
20. A plugin system.
21. A marketplace foundation for templates/plugins.
22. Functional AI tool adapters.
23. A functional AI agent workflow engine.
24. MCP integration foundations.
25. Publishing workflows across package ecosystems and containers.
26. Kubernetes, Helm, Terraform/OpenTofu, ArgoCD, Istio, Nomad, and Vault integration paths.
27. Remote cache integration.
28. Multi-repo federation foundations.
29. Organization-level governance foundations.
30. A hosted/self-hosted control-plane architecture and reference implementation foundation.
31. A complete issue/epic/work-packet structure suitable for GitHub issue automation.

---

## 6. What v1 Will Not Mean

Because v1 is maximal functional, the document does not define a broad “will not be” section that excludes approved capabilities.

Instead, v1 has usage boundaries:

1. v1 does not force every user to use AI.
2. v1 does not force every user to use cloud infrastructure.
3. v1 does not force every user to use Kubernetes.
4. v1 does not force every user to use vector memory.
5. v1 does not force every user to use daemon mode.
6. v1 does not force every user to publish public packages.
7. v1 does not force every user to operate a hosted SaaS deployment.
8. v1 does not require every feature to be active in every local checkout.
9. v1 does require every approved capability to be functionally implemented, documented, and verifiable.

---

## 7. v1 Capability Scope

### 7.1 Repository Foundation

The following are core v1 functional deliverables:

- `.gitignore`
- `.editorconfig`
- `.gitattributes`
- `README.md`
- `LICENSE`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `CODEOWNERS`
- `AGENTS.md`
- `workspace.toml`
- root documentation index
- ADR system
- repo policies
- AI policies
- issue templates
- PR template
- GitHub labels model
- GitHub issue automation artifacts

### 7.2 Root Toolchain

Core v1 functional deliverables:

- `mise.toml`
- Bun workspace
- `moon.yml`
- Biome
- Lefthook
- Renovate
- GitHub Actions
- Docker Compose
- Devcontainer
- Nx integration
- remote cache integration
- root check orchestration
- root task graph
- language-native task delegation

### 7.3 Polyglot Runtime and Project Baselines

Core v1 functional deliverables:

- `apps/web` using Next.js
- `services/api-ts`
- `services/api-rust`
- `services/api-go`
- `services/api-python`
- `services/api-java`
- `packages/config`
- `packages/types`
- `packages/testing`
- `packages/ui`
- `packages/sdk-js`
- `crates/monad-cli`
- `crates/monad-core`
- `crates/monad-config`
- `crates/monad-memory`
- `crates/monad-context`
- `crates/monad-agent`
- `crates/monad-policy`
- `crates/monad-nx-adapter`
- `crates/monad-template`
- `crates/monad-plugin`

### 7.4 Local Infrastructure

Core v1 functional deliverables:

- PostgreSQL
- Redis or Valkey
- MinIO
- Mailpit
- OpenTelemetry Collector
- Qdrant
- optional pgvector-enabled PostgreSQL profile
- policy services where applicable
- local service health checks
- documented ports
- deterministic local startup and shutdown

### 7.5 Advanced DevOps and Platform Operations

Core v1 functional deliverables:

- Dockerfiles
- Docker Compose profiles
- container build workflows
- container publishing workflows
- Helm chart starter with functional deployment path
- Kubernetes manifests
- Terraform/OpenTofu starter with functional environment path
- ArgoCD application definitions
- Istio integration path
- Nomad job definitions
- Vault integration path
- cloud deployment workflow structure
- remote cache integration
- production observability stack path
- release pipeline policies

### 7.6 Monad CLI

The v1 CLI must include the following functional command areas:

```bash
monad --help
monad version
monad doctor
monad check
monad graph
monad affected

monad add app
monad add service
monad add package
monad add crate
monad add infra
monad add policy
monad add template

monad memory init
monad memory status
monad memory add
monad memory search
monad memory index
monad memory compact
monad memory verify

monad context pack
monad context verify
monad context explain

monad handoff create
monad handoff latest
monad handoff verify

monad ai export --target generic
monad ai export --target claude
monad ai export --target cursor
monad ai export --target copilot
monad ai export --target aider
monad ai export --target continue
monad ai export --target cline

monad agent plan
monad agent run
monad agent review
monad agent audit

monad daemon start
monad daemon stop
monad daemon status

monad nx init
monad nx graph
monad nx affected
monad nx run

monad policy check
monad policy explain
monad policy test

monad release plan
monad release changelog
monad release package
monad release publish

monad deploy docker
monad deploy compose
monad deploy kubernetes
monad deploy helm
monad deploy terraform
monad deploy nomad

monad plugin list
monad plugin install
monad plugin verify

monad marketplace list
monad marketplace search
monad marketplace install
```

### 7.7 Monad Memory

Core v1 functional deliverables:

- Markdown-first canonical memory files
- session memory
- handoff files
- context pack generation
- generic AI export
- vendor-specific AI exports
- local-only memory mode
- SQLite memory backend
- semantic memory index
- vector memory index
- pgvector support
- Qdrant support
- memory compaction
- memory verification
- memory search
- memory policy checks
- no accidental inclusion of private memory
- no uncontrolled promotion of temporary memory into canonical memory

### 7.8 AI and Agentic Development

Core v1 functional deliverables:

- generic AI instructions
- Claude export
- Cursor export
- Copilot export
- Aider export
- Continue export
- Cline export
- local LLM adapter path
- MCP integration
- agent workflow engine
- human approval gates
- agent audit log
- prompt-injection policy
- tool-use policy
- generated handoffs
- generated context packs
- safe-by-default local execution

### 7.9 Contracts

Core v1 functional deliverables:

- OpenAPI folder
- AsyncAPI folder
- JSON Schema folder
- Protobuf folder
- basic examples
- contract validation commands
- contract documentation
- contract check in CI

### 7.10 Publishing

Core v1 functional deliverables:

- npm package publishing workflow
- Rust crate publishing workflow
- Go binary release workflow
- Python package publishing workflow
- Java/Gradle publishing workflow
- container publishing workflow
- changelog generation
- release planning
- release approval policy
- release verification checks

### 7.11 Templates, Plugins, and Marketplace

Core v1 functional deliverables:

- template manifest format
- app templates
- service templates
- package templates
- crate templates
- infra templates
- docs templates
- plugin manifest format
- plugin loading model
- plugin verification
- marketplace index format
- local marketplace catalog
- install-from-catalog command path
- trust and verification rules

### 7.12 Governance

Core v1 functional deliverables:

- ADR system
- policy documents
- policy-as-code engine
- CODEOWNERS
- dependency policy
- security policy
- release policy
- AI usage policy
- human approval policy
- organization governance model
- multi-repo governance model
- repo health checks
- architecture fitness checks

---

## 8. Final v1 Stack

### 8.1 Root Control Plane

```txt
monad CLI
moon
mise
Bun
Nx
GitHub Actions
Docker Compose
Devcontainer
remote cache
```

### 8.2 TypeScript / JavaScript

```txt
Bun
TypeScript
Next.js
Tailwind
shadcn-style components
Lucide icons
Biome
Bun test or Vitest
Changesets
ElysiaJS or Hono
Drizzle readiness
OpenAPI client generation
```

### 8.3 Rust

```txt
Cargo workspace
clap
serde
tokio
tracing
axum
cargo test
cargo clippy
cargo fmt
cargo-nextest
cargo-audit
cargo-deny
release-plz readiness
```

### 8.4 Go

```txt
Go workspace or module baseline
net/http or Chi
gofmt
go test
go build
golangci-lint
gotestsum
GoReleaser
```

### 8.5 Python

```txt
uv
FastAPI
Pydantic
Ruff
Pyright
pytest
SQLite support
vector backend adapters
```

### 8.6 Java

```txt
Java 21+
Gradle multi-project
Spring Boot or minimal HTTP service
JUnit
Testcontainers
Spotless
JReleaser readiness
```

### 8.7 Infrastructure

```txt
PostgreSQL
pgvector
Redis or Valkey
MinIO
Mailpit
OpenTelemetry Collector
Qdrant
Docker
Docker Compose
Kubernetes
Helm
Terraform/OpenTofu
ArgoCD
Istio
Nomad
Vault
GHCR
```

### 8.8 Governance and Security

```txt
ADRs
CODEOWNERS
Renovate
Lefthook
Biome
gitleaks
Trivy
CodeQL
OpenSSF Scorecard
policy-as-code
OpenAPI
AsyncAPI
JSON Schema
Protobuf
AI safety policies
agent audit logs
```

---

## 9. Recommended v1 Repository Shape

```txt
monad-factory/
  apps/
    web/
    admin/
    docs/
    control-plane/

  services/
    api-ts/
    api-rust/
    api-go/
    api-python/
    api-java/
    auth/
    billing/
    tenant/
    marketplace/
    policy-api/
    memory-api/
    agent-runner/

  packages/
    config/
    types/
    testing/
    ui/
    sdk-js/
    observability/
    contracts/

  crates/
    monad-cli/
    monad-core/
    monad-config/
    monad-memory/
    monad-context/
    monad-agent/
    monad-policy/
    monad-nx-adapter/
    monad-template/
    monad-plugin/
    monad-marketplace/
    monad-deploy/

  contracts/
    openapi/
    asyncapi/
    protobuf/
    json-schema/

  docs/
    00-index.md
    product/
    planning/
    getting-started/
    architecture/
    adr/
    ai/
    memory/
    agents/
    policy/
    deployment/
    publishing/
    tutorials/
    runbooks/
    marketplace/
    federation/
    hosted-control-plane/

  policies/
    repo/
    security/
    ai/
    release/
    dependency/
    architecture/
    agent/
    memory/
    organization/

  templates/
    apps/
    services/
    crates/
    packages/
    infra/
    docs/
    policies/

  plugins/
    examples/
    registry/
    schemas/

  marketplace/
    catalog/
    manifests/
    trust/

  examples/
    minimal/
    fullstack-saas/
    polyglot-services/
    ai-assisted-development/
    policy-governed-repo/
    federated-repos/

  infra/
    compose/
    docker/
    kubernetes/
    helm/
    terraform/
    opentofu/
    argocd/
    istio/
    nomad/
    vault/

  tools/
    scripts/
    checks/
    generators/
    release/
    security/

  tests/
    smoke/
    integration/
    contract/
    e2e/
    policy/
    agent/
    memory/

  .github/
    workflows/
    actions/
    ISSUE_TEMPLATE/
    PULL_REQUEST_TEMPLATE.md

  .devcontainer/

  .monad/
    config.toml
    memory/
      MEMORY.md
      canonical/
        project.md
        architecture.md
        decisions.md
        conventions.md
        commands.md
        glossary.md
        agents.md
        policies.md
      sessions/
        .gitkeep
      handoffs/
        .gitkeep
      context-packs/
        .gitkeep
      indexes/
        .gitkeep
      private/
        .gitignore
```

---

## 10. Monad Memory v1 Scope

### 10.1 What Monad Memory Is

Monad Memory is a local-first, LLM-agnostic, repo-aware memory, context, handoff, and retrieval subsystem for AI-assisted software development.

It helps users preserve and export project context across chat sessions, AI tools, local agents, and development workflows.

### 10.2 What Monad Memory Does in v1

Monad Memory v1 supports:

1. Canonical project memory.
2. Architecture memory.
3. Decision memory.
4. Convention memory.
5. Command memory.
6. Glossary memory.
7. Agent instruction memory.
8. Policy memory.
9. Session memory.
10. Handoff generation.
11. Context pack generation.
12. Generic AI export.
13. Vendor-specific AI exports.
14. SQLite memory backend.
15. Semantic memory index.
16. Vector memory index.
17. pgvector backend support.
18. Qdrant backend support.
19. Memory search.
20. Memory compaction.
21. Memory verification.
22. Memory policy enforcement.
23. Private memory exclusion.
24. Generated memory artifacts.

### 10.3 v1 Memory Commands

```bash
monad memory init
monad memory status
monad memory add
monad memory search
monad memory index
monad memory compact
monad memory verify
monad context pack
monad context verify
monad context explain
monad handoff create
monad handoff latest
monad handoff verify
```

### 10.4 v1 Memory Files

```txt
.monad/memory/MEMORY.md
.monad/memory/canonical/project.md
.monad/memory/canonical/architecture.md
.monad/memory/canonical/decisions.md
.monad/memory/canonical/conventions.md
.monad/memory/canonical/commands.md
.monad/memory/canonical/glossary.md
.monad/memory/canonical/agents.md
.monad/memory/canonical/policies.md
.monad/memory/sessions/
.monad/memory/handoffs/
.monad/memory/context-packs/
.monad/memory/indexes/
.monad/memory/private/
```

---

## 11. Nx v1 Scope

Nx is included in v1 as a full functional adapter behind the `monad` command surface.

The v1 posture is:

```txt
monad is the public interface.
moon is the default root task orchestrator.
Nx is a supported graph/cache/affected-task backend.
Native language tools remain authoritative inside each language ecosystem.
```

### 11.1 v1 Nx Capabilities

- generate or validate `nx.json`
- map `monad` projects to Nx projects
- support Nx graph commands
- support Nx affected commands
- support Nx task caching
- support custom command caching
- keep Nx behind stable `monad` commands
- document when Nx is used
- provide fallback paths when Nx is unavailable

### 11.2 v1 Nx Commands

```bash
monad nx init
monad nx graph
monad nx affected
monad nx run
monad affected
```

---

## 12. GitHub Issue Model

Each work packet should become one GitHub issue.

Each task should become a checklist item.

Each subtask may become either:

1. a nested checklist item, or
2. a child issue if the work becomes large.

### 12.1 Recommended GitHub Labels

```txt
type:epic
type:work-packet
type:task
area:docs
area:tooling
area:cli
area:memory
area:agent
area:policy
area:typescript
area:rust
area:go
area:python
area:java
area:infra
area:ci
area:security
area:contracts
area:templates
area:plugins
area:marketplace
area:release
area:nx
area:deployment
area:federation
area:control-plane
priority:p0
priority:p1
priority:p2
status:ready
status:blocked
status:deferred
status:in-progress
status:review
good-first-issue
```

### 12.2 Recommended Issue Naming Format

```txt
E00: Epic title
WP-E00-001: Work packet title
```

Example:

```txt
WP-E13-001: Create monad CLI workspace and command skeleton
```

---

## 13. Sprint / Batch Plan

The word “sprint” here means an implementation batch, not a required calendar duration.

### Sprint 0 — Scope Lock and Planning

Goal:

```txt
Finalize maximal functional v1 scope, repo doctrine, issue labels, epic list, work packets, and verification gates.
```

Includes:

- E00 Product Scope and Governance
- E01 Documentation Foundation
- E02 Architecture and ADR Foundation

Exit criteria:

- Maximal v1 scope approved.
- ADR list approved.
- Work packets ready for GitHub issue creation.
- Scope document committed to repo.

---

### Sprint 1 — Repository Foundation

Goal:

```txt
Create the initial repo foundation, docs, policies, governance files, and base directory structure.
```

Includes:

- E03 Repository Foundation
- E04 Root Toolchain
- E05 Documentation Governance

Exit criteria:

- Repo initializes cleanly.
- Root docs exist.
- Root config files exist.
- First foundation checks pass.

---

### Sprint 2 — Tooling, CI, and Quality Baseline

Goal:

```txt
Make the repo checkable, buildable, secure, and CI-ready.
```

Includes:

- E06 Root Task Orchestration
- E07 GitHub Automation
- E08 Security and Quality Baseline
- E09 Dependency and Release Governance

Exit criteria:

- Root check commands exist.
- GitHub Actions are present.
- Formatting/lint/test/build workflows exist.
- Security baseline checks exist.

---

### Sprint 3 — Polyglot Baselines

Goal:

```txt
Add fully functional first-class examples for each first-class language.
```

Includes:

- E10 TypeScript and Next.js
- E11 Rust Baseline
- E12 Go Baseline
- E13 Python Baseline
- E14 Java Baseline

Exit criteria:

- Each language has a functional project.
- Each language has build/test/check commands.
- Root orchestration can call all project checks.

---

### Sprint 4 — Monad CLI Core

Goal:

```txt
Add the first complete monad CLI command surface.
```

Includes:

- E15 Monad CLI Core
- E16 Repo Graph and Affected Detection
- E17 Nx Adapter

Exit criteria:

- `monad --help` works.
- `monad version` works.
- `monad doctor` works.
- `monad check` works.
- `monad graph` works.
- `monad affected` works.
- `monad nx` commands work.

---

### Sprint 5 — Monad Memory and Context Continuity

Goal:

```txt
Add local-first memory, semantic/vector indexing, handoffs, context packs, and AI exports.
```

Includes:

- E18 Monad Memory
- E19 Semantic and Vector Memory
- E20 Context Packs and Handoffs
- E21 AI Tool Exports

Exit criteria:

- Memory files exist.
- SQLite memory backend works.
- pgvector/Qdrant backend paths work.
- `monad context pack` works.
- `monad handoff create` works.
- AI exports work.

---

### Sprint 6 — Agentic Development and Daemon

Goal:

```txt
Add daemon mode, safe agent workflow capabilities, and agent governance.
```

Includes:

- E22 Daemon
- E23 Agent Workflow Engine
- E24 Agent Safety and Audit

Exit criteria:

- Daemon commands work.
- Agent planning works.
- Agent execution respects approval gates.
- Agent audit logs are written.

---

### Sprint 7 — Templates, Generation, Plugins, and Marketplace

Goal:

```txt
Add functional template generation, plugin model, and marketplace catalog.
```

Includes:

- E25 Template Generation
- E26 Plugin System
- E27 Marketplace Foundation

Exit criteria:

- `monad add` commands work.
- Plugin install/verify commands work.
- Marketplace catalog commands work.

---

### Sprint 8 — Contracts, Policies, and Governance

Goal:

```txt
Add contract governance, policy-as-code, organization governance, and multi-repo foundations.
```

Includes:

- E28 Contracts and Schemas
- E29 Policy-as-Code
- E30 Organization Governance
- E31 Multi-Repo Federation

Exit criteria:

- Contract checks work.
- Policy checks work.
- Governance docs and commands exist.
- Federation model is functionally represented.

---

### Sprint 9 — Infrastructure, Deployment, and Operations

Goal:

```txt
Add Docker, Kubernetes, Helm, Terraform/OpenTofu, ArgoCD, Istio, Nomad, Vault, and observability workflows.
```

Includes:

- E32 Local Infrastructure
- E33 Container and Publishing Workflows
- E34 Kubernetes and Helm
- E35 Terraform/OpenTofu
- E36 ArgoCD, Istio, Nomad, and Vault
- E37 Observability

Exit criteria:

- Local infra starts.
- Containers build.
- Helm/Kubernetes path works.
- Terraform/OpenTofu path works.
- Operational integrations are documented and verifiable.

---

### Sprint 10 — Hosted Control Plane and Final Review

Goal:

```txt
Add hosted/self-hosted control-plane foundation and complete maximal v1 verification.
```

Includes:

- E38 Hosted/Self-Hosted Control Plane
- E39 Final v1 Review
- E40 GitHub Issue Automation

Exit criteria:

- Control-plane app/service foundation exists.
- Final v1 review passes.
- All work packets are represented as issues or issue-ready artifacts.

---

# 14. Epics, Work Packets, Tasks, and Subtasks

## E00 — Product Scope and Governance

### Objective

Define the maximal functional v1 scope, governance model, and scope control rules.

### User Value

Prevents ambiguity and makes all later implementation automatable.

### WP-E00-001 — Finalize Maximal Functional v1 Scope Document

Labels:

```txt
type:work-packet, area:docs, priority:p0, status:ready
```

Tasks:

- Create `docs/product/v1-maximal-functional-scope-and-delivery-plan.md`.
  - Add YAML frontmatter.
  - Define product identity.
  - Define target user.
  - Define maximal functional v1 scope.
  - Define usage boundaries.
- Add v1 success criteria.
  - Define local-first success.
  - Define GitHub-ready success.
  - Define polyglot success.
  - Define AI-memory success.
  - Define governance success.
  - Define deployment success.
- Add scope-control rules.
  - State that approved v1 capabilities are core functional.
  - State that implementation sequencing does not imply deferral.
  - State that no approved capability is scaffold-only.

Acceptance Criteria:

- Scope document exists.
- Document uses maximal functional v1 framing.
- Document can be used as the reference for GitHub issue generation.

### WP-E00-002 — Define GitHub Issue Taxonomy

Labels:

```txt
type:work-packet, area:docs, priority:p0, status:ready
```

Tasks:

- Define issue label taxonomy.
  - Add type labels.
  - Add area labels.
  - Add priority labels.
  - Add status labels.
- Define issue naming convention.
  - Epic title format.
  - Work packet title format.
  - Task checklist format.
- Create issue template drafts.
  - Epic issue template.
  - Work packet issue template.
  - Bug issue template.
  - ADR proposal issue template.
  - Security issue template.
  - Policy proposal template.

Acceptance Criteria:

- Issue naming convention exists.
- Label list exists.
- Issue templates exist or are documented.
- Work packets are ready to convert into GitHub issues.

---

## E01 — Documentation Foundation

### Objective

Create the documentation structure and standards for the repository.

### User Value

Makes the repository understandable, maintainable, and AI-friendly from day one.

### WP-E01-001 — Create Documentation Skeleton

Labels:

```txt
type:work-packet, area:docs, priority:p0, status:ready
```

Tasks:

- Create `docs/00-index.md`.
  - Add overview.
  - Link to product docs.
  - Link to architecture docs.
  - Link to ADRs.
  - Link to AI docs.
  - Link to memory docs.
  - Link to policy docs.
  - Link to deployment docs.
- Create documentation folders.
  - `docs/product/`
  - `docs/planning/`
  - `docs/architecture/`
  - `docs/adr/`
  - `docs/ai/`
  - `docs/memory/`
  - `docs/agents/`
  - `docs/policy/`
  - `docs/deployment/`
  - `docs/publishing/`
  - `docs/getting-started/`
  - `docs/tutorials/`
  - `docs/runbooks/`
  - `docs/marketplace/`
  - `docs/federation/`
  - `docs/hosted-control-plane/`
- Add README files where useful.
  - Explain purpose of each docs folder.
  - Keep content navigable.

Acceptance Criteria:

- Documentation tree exists.
- `docs/00-index.md` links to major areas.
- All meaningful Markdown files include YAML frontmatter.

### WP-E01-002 — Add Documentation Standards

Labels:

```txt
type:work-packet, area:docs, priority:p0, status:ready
```

Tasks:

- Define Markdown frontmatter schema.
  - Required fields.
  - Optional fields.
  - Canonical document markers.
- Define document naming rules.
- Define decision/document ownership.
- Add docs review checklist.
- Add docs lint/check command.

Acceptance Criteria:

- Documentation standards exist.
- Frontmatter check can be automated.
- New docs have clear expectations.

---

## E02 — Architecture and ADR Foundation

### Objective

Create the architectural decision system and initial decision record set.

### User Value

Preserves reasoning and reduces accidental architecture drift.

### WP-E02-001 — Create ADR System

Labels:

```txt
type:work-packet, area:docs, area:architecture, priority:p0, status:ready
```

Tasks:

- Create `docs/adr/0000-adr-template.md`.
  - Include frontmatter fields.
  - Include status.
  - Include context.
  - Include decision.
  - Include consequences.
  - Include verification.
- Create ADR index.
  - List ADRs.
  - List status.
  - Link to files.
- Add ADR contribution process.
- Add ADR review checklist.

Acceptance Criteria:

- ADR template exists.
- ADR index exists.
- ADR files use frontmatter.

### WP-E02-002 — Create Initial ADRs

Labels:

```txt
type:work-packet, area:architecture, priority:p0, status:ready
```

Tasks:

- Create ADR-0001: Use a maximal functional polyglot product-factory monorepo.
- Create ADR-0002: Use `monad` as public repo control plane.
- Create ADR-0003: Use `mise` for toolchain management.
- Create ADR-0004: Use native language toolchains under root orchestration.
- Create ADR-0005: Use Rust for the `monad` CLI.
- Create ADR-0006: Include LLM-agnostic Monad Memory.
- Create ADR-0007: Keep AI memory local-first, inspectable, and policy-governed.
- Create ADR-0008: Use generated AI tool adapters.
- Create ADR-0009: Include daemon mode.
- Create ADR-0010: Include Nx as graph/cache/affected-task adapter.
- Create ADR-0011: Keep `monad` commands stable when underlying tools change.
- Create ADR-0012: Treat handoffs and context packs as first-class artifacts.
- Create ADR-0013: Include policy-as-code.
- Create ADR-0014: Include template/plugin/marketplace systems.
- Create ADR-0015: Include Kubernetes/cloud/advanced DevOps integration paths.
- Create ADR-0016: Include multi-repo and organization governance foundations.
- Create ADR-0017: Include hosted/self-hosted control-plane architecture.

Acceptance Criteria:

- Initial ADR set exists.
- ADRs match maximal functional v1 scope.
- ADR index references all initial ADRs.

---

## E03 — Repository Foundation

### Objective

Create the initial root repository files and directory structure.

### User Value

Gives users a clean, professional, reusable monorepo platform foundation.

### WP-E03-001 — Create Root Governance Files

Labels:

```txt
type:work-packet, area:docs, priority:p0, status:ready
```

Tasks:

- Create `README.md`.
  - Explain what `monad-factory` is.
  - Explain v1 maximal functional scope.
  - Explain quickstart.
  - Explain project structure.
- Create `LICENSE`.
- Create `SECURITY.md`.
- Create `CONTRIBUTING.md`.
- Create `CODE_OF_CONDUCT.md`.
- Create `CODEOWNERS`.
- Create `AGENTS.md`.
  - Explain AI assistant expectations.
  - Explain that AI use is optional for users.
  - Point to Monad Memory docs.
  - Point to agent safety rules.

Acceptance Criteria:

- Root governance files exist.
- README clearly communicates product purpose.
- AI usage and governance are documented.

### WP-E03-002 — Create Base Directory Structure

Labels:

```txt
type:work-packet, area:docs, priority:p0, status:ready
```

Tasks:

- Create app directories.
- Create service directories.
- Create package directories.
- Create Rust crate directories.
- Create contract directories.
- Create docs directories.
- Create policy directories.
- Create template directories.
- Create plugin and marketplace directories.
- Create infrastructure directories.
- Create test directories.
- Add `.gitkeep` files where needed.
- Document directory purpose.

Acceptance Criteria:

- Base directory tree exists.
- Empty directories contain `.gitkeep` where needed.
- Directory purpose is documented.

---

## E04 — Root Toolchain

### Objective

Install and configure the root development toolchain.

### User Value

Makes local development reproducible across languages.

### WP-E04-001 — Add Tool Version Management with mise

Labels:

```txt
type:work-packet, area:tooling, priority:p0, status:ready
```

Tasks:

- Create `mise.toml`.
  - Pin Bun.
  - Pin Node if needed.
  - Pin Rust.
  - Pin Go.
  - Pin Python.
  - Pin Java.
  - Pin Gradle.
  - Pin Terraform/OpenTofu.
  - Pin auxiliary tools where practical.
- Add setup instructions.
- Add toolchain verification command.

Acceptance Criteria:

- `mise.toml` exists.
- Required tool versions are pinned.
- Setup docs explain how to install tools.

### WP-E04-002 — Add Bun Workspace

Labels:

```txt
type:work-packet, area:typescript, priority:p0, status:ready
```

Tasks:

- Create root `package.json`.
- Add workspace definitions.
- Add root scripts.
- Add package manager field.
- Initialize lockfile.
- Add root TypeScript configuration.
- Add workspace package references.

Acceptance Criteria:

- Bun workspace exists.
- Root package scripts exist.
- Bun install works.

### WP-E04-003 — Add Formatting and Hooks

Labels:

```txt
type:work-packet, area:tooling, priority:p0, status:ready
```

Tasks:

- Add `biome.json`.
- Add `lefthook.yml`.
- Add `.editorconfig`.
- Add `.gitattributes`.
- Add `.gitignore`.
- Add commit/check conventions.

Acceptance Criteria:

- Formatting config exists.
- Git hooks config exists.
- Root ignored files are correct.
- Formatting checks can run.

---

## E05 — Documentation Governance

### Objective

Make docs verifiable and governance-friendly.

### User Value

Ensures repository knowledge stays structured and durable.

### WP-E05-001 — Add Frontmatter Check

Labels:

```txt
type:work-packet, area:docs, priority:p0, status:ready
```

Tasks:

- Create frontmatter validation script.
- Define required frontmatter fields.
- Exclude generated files where appropriate.
- Add check to root task.
- Add check to CI.

Acceptance Criteria:

- Frontmatter check exists.
- CI can run frontmatter check.
- Meaningful docs include frontmatter.

### WP-E05-002 — Add Docs Index Verification

Labels:

```txt
type:work-packet, area:docs, priority:p1, status:ready
```

Tasks:

- Check canonical docs are linked.
- Check ADR index includes ADRs.
- Check product docs are discoverable.
- Check memory docs are discoverable.
- Check policy docs are discoverable.

Acceptance Criteria:

- Documentation navigation can be verified.
- Missing canonical links are reported.

---

## E06 — Root Task Orchestration

### Objective

Make `moon` the default root task orchestrator while preserving native language tools.

### User Value

Provides one command surface for checking many languages and projects.

### WP-E06-001 — Configure moon Workspace

Labels:

```txt
type:work-packet, area:tooling, priority:p0, status:ready
```

Tasks:

- Create `moon.yml`.
- Define root tasks.
- Define task inputs.
- Define task outputs where useful.
- Define project discovery.
- Add root commands:
  - `format`
  - `lint`
  - `test`
  - `build`
  - `check`
  - `doctor`

Acceptance Criteria:

- Root moon checks work.
- Task names are documented.
- Task names are consistent across languages.

### WP-E06-002 — Define Native Tool Delegation

Labels:

```txt
type:work-packet, area:architecture, priority:p0, status:ready
```

Tasks:

- Document orchestration policy.
- Add task mapping docs for TypeScript, Rust, Go, Python, and Java.
- Add ADR consequence notes.
- Add verification examples.

Acceptance Criteria:

- Tool delegation policy exists.
- Every first-class language has documented task mapping.

---

## E07 — GitHub Automation

### Objective

Add GitHub workflows and repository automation files.

### User Value

Makes the repo ready for collaborative development and CI.

### WP-E07-001 — Create Core CI Workflow

Labels:

```txt
type:work-packet, area:ci, priority:p0, status:ready
```

Tasks:

- Create `.github/workflows/ci.yml`.
- Add checkout/setup steps.
- Add tool install steps.
- Run format checks.
- Run lint checks.
- Run type checks.
- Run unit tests.
- Run builds.
- Run docs checks.
- Add caching where safe.

Acceptance Criteria:

- CI workflow exists.
- CI runs root check commands.
- CI does not require secrets for baseline checks.

### WP-E07-002 — Create Issue and PR Templates

Labels:

```txt
type:work-packet, area:ci, priority:p1, status:ready
```

Tasks:

- Create PR template.
- Create bug issue template.
- Create work packet issue template.
- Create ADR proposal template.
- Create policy proposal template.
- Add issue template config.

Acceptance Criteria:

- Templates exist.
- Templates reinforce verification.

---

## E08 — Security and Quality Baseline

### Objective

Add non-invasive security and quality checks.

### User Value

Creates a safer and more trustworthy platform foundation.

### WP-E08-001 — Add Secret and Dependency Safety Checks

Labels:

```txt
type:work-packet, area:security, priority:p0, status:ready
```

Tasks:

- Add gitleaks config/workflow.
- Add dependency review workflow.
- Add `.env.example`.
- Ensure `.env` files are ignored.
- Add security documentation.

Acceptance Criteria:

- Secret scanning baseline exists.
- Environment file rules are documented.
- No real secrets are committed.

### WP-E08-002 — Add CodeQL, Trivy, and Scorecard

Labels:

```txt
type:work-packet, area:security, priority:p1, status:ready
```

Tasks:

- Add CodeQL workflow.
- Add Trivy workflow.
- Add OpenSSF Scorecard workflow.
- Document security check expectations.
- Add local alternatives where practical.

Acceptance Criteria:

- Security workflows exist.
- Security expectations are documented.

---

## E09 — Dependency and Release Governance

### Objective

Add dependency update and release governance foundations.

### User Value

Keeps the repo maintainable and publish-ready.

### WP-E09-001 — Add Renovate

Labels:

```txt
type:work-packet, area:tooling, area:release, priority:p0, status:ready
```

Tasks:

- Create `renovate.json`.
- Configure grouped updates.
- Configure language-specific update rules.
- Document Renovate behavior.

Acceptance Criteria:

- Renovate config exists.
- Dependency update policy is documented.

### WP-E09-002 — Add Release Policy

Labels:

```txt
type:work-packet, area:release, priority:p0, status:ready
```

Tasks:

- Create `policies/release/release-policy.md`.
- Define versioning approach.
- Define changelog approach.
- Define approval rules.
- Define publish rules.
- Define rollback rules.

Acceptance Criteria:

- Release policy exists.
- Publishing expectations are clear.

---

## E10 — TypeScript and Next.js

### Objective

Add the initial Next.js app and TypeScript ecosystem foundation.

### User Value

Provides a familiar web app baseline and TypeScript package/service examples.

### WP-E10-001 — Create Next.js App

Labels:

```txt
type:work-packet, area:typescript, priority:p0, status:ready
```

Tasks:

- Create `apps/web`.
- Add minimal Next.js app.
- Add TypeScript.
- Add Tailwind.
- Add shadcn-style component structure.
- Add Lucide icon example.
- Add homepage.
- Add local scripts.
- Add app README.

Acceptance Criteria:

- Web app builds.
- Web app typechecks.
- Web app has documented commands.

### WP-E10-002 — Create TypeScript API Service

Labels:

```txt
type:work-packet, area:typescript, priority:p0, status:ready
```

Tasks:

- Create `services/api-ts`.
- Add minimal HTTP server.
- Add health endpoint.
- Add TypeScript config.
- Add tests.
- Add build/check tasks.
- Add service README.

Acceptance Criteria:

- TypeScript API starts locally.
- Health endpoint works.
- Test passes.
- Build passes.

### WP-E10-003 — Create Shared TypeScript Packages

Labels:

```txt
type:work-packet, area:typescript, priority:p1, status:ready
```

Tasks:

- Create `packages/config`.
- Create `packages/types`.
- Create `packages/testing`.
- Create `packages/ui`.
- Create `packages/sdk-js`.
- Add READMEs.
- Add build/typecheck tasks.

Acceptance Criteria:

- Packages are recognized by Bun workspace.
- Packages build or typecheck.
- Packages are documented.

---

## E11 — Rust Baseline

### Objective

Add the Rust workspace and core Rust crates.

### User Value

Creates the durable systems-language foundation for the repo control plane.

### WP-E11-001 — Create Cargo Workspace

Labels:

```txt
type:work-packet, area:rust, priority:p0, status:ready
```

Tasks:

- Create root `Cargo.toml`.
- Define workspace members.
- Define shared package metadata.
- Add core crates:
  - `monad-cli`
  - `monad-core`
  - `monad-config`
  - `monad-memory`
  - `monad-context`
  - `monad-agent`
  - `monad-policy`
  - `monad-nx-adapter`
  - `monad-template`
  - `monad-plugin`
- Add basic tests.
- Add Rust tasks.

Acceptance Criteria:

- Cargo workspace builds.
- Rust tests pass.
- Rust formatting and linting commands exist.

### WP-E11-002 — Create Rust API Service

Labels:

```txt
type:work-packet, area:rust, priority:p1, status:ready
```

Tasks:

- Create `services/api-rust`.
- Add minimal Rust HTTP service.
- Add health endpoint.
- Add tests.
- Add moon tasks.
- Add service README.

Acceptance Criteria:

- Rust service builds.
- Rust tests pass.
- Health endpoint exists.

---

## E12 — Go Baseline

### Objective

Add a fully functional Go service.

### User Value

Proves Go is first-class in the monorepo.

### WP-E12-001 — Create Go API Service

Labels:

```txt
type:work-packet, area:go, priority:p0, status:ready
```

Tasks:

- Create `services/api-go`.
- Add `go.mod`.
- Add minimal HTTP server.
- Add health endpoint.
- Add handler tests.
- Add build/test/check tasks.
- Add service README.

Acceptance Criteria:

- Go service builds.
- Go tests pass.
- Health endpoint works.
- Root orchestration can run Go checks.

---

## E13 — Python Baseline

### Objective

Add a fully functional Python FastAPI service.

### User Value

Proves Python/AI-service workflows are first-class.

### WP-E13-001 — Create Python FastAPI Service

Labels:

```txt
type:work-packet, area:python, priority:p0, status:ready
```

Tasks:

- Create `services/api-python`.
- Add `pyproject.toml`.
- Add uv configuration.
- Add FastAPI app.
- Add health endpoint.
- Add pytest tests.
- Add Ruff configuration.
- Add Pyright readiness.
- Add service README.

Acceptance Criteria:

- Python dependencies install with uv.
- FastAPI app starts locally.
- Tests pass.
- Ruff check passes.

---

## E14 — Java Baseline

### Objective

Add a fully functional Java service.

### User Value

Proves Java/JVM workflows are first-class.

### WP-E14-001 — Create Java Service

Labels:

```txt
type:work-packet, area:java, priority:p0, status:ready
```

Tasks:

- Create `services/api-java`.
- Add Gradle project.
- Add Java 21 configuration.
- Add minimal service.
- Add health endpoint if HTTP service.
- Add JUnit tests.
- Add Spotless readiness.
- Add service README.

Acceptance Criteria:

- Java service builds.
- Java tests pass.
- Root orchestration can run Java checks.

---

## E15 — Monad CLI Core

### Objective

Create the core `monad` CLI.

### User Value

Gives the repo a stable command surface.

### WP-E15-001 — Create CLI Skeleton

Labels:

```txt
type:work-packet, area:cli, area:rust, priority:p0, status:ready
```

Tasks:

- Implement `monad --help`.
- Implement `monad version`.
- Add CLI metadata.
- Add command module structure.
- Add tests for command parsing.

Acceptance Criteria:

- `monad --help` works.
- `monad version` works.
- CLI tests pass.

### WP-E15-002 — Implement `monad doctor`

Labels:

```txt
type:work-packet, area:cli, priority:p0, status:ready
```

Tasks:

- Check required files.
- Check required directories.
- Check tool availability.
- Check memory structure.
- Check policy structure.
- Print readable report.
- Return non-zero on failure.

Acceptance Criteria:

- `monad doctor` reports missing requirements.
- `monad doctor` passes on valid repo.
- Output is readable.

### WP-E15-003 — Implement `monad check`

Labels:

```txt
type:work-packet, area:cli, priority:p0, status:ready
```

Tasks:

- Wrap root check command.
- Delegate to moon where appropriate.
- Include policy checks.
- Include docs checks.
- Print command being run.
- Return correct exit code.

Acceptance Criteria:

- `monad check` runs root checks.
- Failures are propagated.
- Command is documented.

---

## E16 — Repo Graph and Affected Detection

### Objective

Add graph and affected-project capabilities.

### User Value

Lets users and AI assistants understand repo shape and target work efficiently.

### WP-E16-001 — Implement `monad graph`

Labels:

```txt
type:work-packet, area:cli, priority:p0, status:ready
```

Tasks:

- Read workspace manifest.
- Detect projects.
- Detect declared relationships.
- Output text graph.
- Output JSON graph.
- Output Mermaid graph.
- Add tests.

Acceptance Criteria:

- `monad graph` runs.
- Graph includes apps, services, packages, crates.
- JSON output is valid.
- Mermaid output is valid.

### WP-E16-002 — Implement `monad affected`

Labels:

```txt
type:work-packet, area:cli, area:nx, priority:p0, status:ready
```

Tasks:

- Detect changed files.
- Map changed files to projects.
- Include dependency-aware affected projects.
- Support Nx-backed mode.
- Support fallback mode.
- Add tests.

Acceptance Criteria:

- `monad affected` reports changed/affected projects.
- Command works with and without Nx.
- Output is machine-readable when requested.

---

## E17 — Nx Adapter

### Objective

Implement full Nx adapter support behind `monad`.

### User Value

Adds graph, affected-task, and caching power without making Nx the public UX.

### WP-E17-001 — Implement Nx Init and Mapping

Labels:

```txt
type:work-packet, area:nx, area:cli, priority:p0, status:ready
```

Tasks:

- Implement `monad nx init`.
- Generate `nx.json`.
- Map projects to Nx projects.
- Document mapping rules.
- Add tests.

Acceptance Criteria:

- Nx can be initialized.
- Project mapping is deterministic.
- Generated files are documented.

### WP-E17-002 — Implement Nx Graph/Affected/Run

Labels:

```txt
type:work-packet, area:nx, area:cli, priority:p0, status:ready
```

Tasks:

- Implement `monad nx graph`.
- Implement `monad nx affected`.
- Implement `monad nx run`.
- Wrap Nx commands safely.
- Preserve `monad` command stability.
- Add fallback behavior.

Acceptance Criteria:

- Nx-backed commands work.
- Failures are clear.
- `monad` remains the public interface.

---

## E18 — Monad Memory

### Objective

Add local-first memory and context continuity.

### User Value

Allows durable AI-assisted development without vendor lock-in.

### WP-E18-001 — Create Memory File Structure

Labels:

```txt
type:work-packet, area:memory, priority:p0, status:ready
```

Tasks:

- Create `.monad/config.toml`.
- Create `.monad/memory/MEMORY.md`.
- Create canonical memory files.
- Create sessions folder.
- Create handoffs folder.
- Create context-packs folder.
- Create indexes folder.
- Create private memory folder.
- Add ignore rules.
- Document memory rules.

Acceptance Criteria:

- Memory structure exists.
- Public canonical memory is safe to commit.
- Private memory is ignored by default.
- Memory docs explain usage.

### WP-E18-002 — Implement Memory Commands

Labels:

```txt
type:work-packet, area:memory, area:cli, priority:p0, status:ready
```

Tasks:

- Implement `monad memory init`.
- Implement `monad memory status`.
- Implement `monad memory add`.
- Implement `monad memory verify`.
- Add tests.

Acceptance Criteria:

- Memory commands work.
- Commands do not leak private memory.
- Commands return clear status.

---

## E19 — Semantic and Vector Memory

### Objective

Add search, indexing, and vector memory backends.

### User Value

Makes Monad Memory usable for retrieval and context rehydration.

### WP-E19-001 — Implement SQLite Memory Backend

Labels:

```txt
type:work-packet, area:memory, priority:p0, status:ready
```

Tasks:

- Define memory record schema.
- Create SQLite backend.
- Add indexing command.
- Add search command.
- Add tests.
- Document storage format.

Acceptance Criteria:

- SQLite backend works.
- Search returns relevant records.
- Index can be rebuilt.

### WP-E19-002 — Implement pgvector and Qdrant Backends

Labels:

```txt
type:work-packet, area:memory, area:infra, priority:p0, status:ready
```

Tasks:

- Add pgvector backend configuration.
- Add Qdrant backend configuration.
- Add local Compose profile.
- Add indexing support.
- Add search support.
- Add tests or smoke checks.
- Document backend selection.

Acceptance Criteria:

- pgvector backend path works.
- Qdrant backend path works.
- Local configuration is documented.
- Vector backend failures are clear.

### WP-E19-003 — Implement Memory Compaction

Labels:

```txt
type:work-packet, area:memory, priority:p1, status:ready
```

Tasks:

- Define compaction rules.
- Implement compaction command.
- Preserve source references.
- Avoid private memory leakage.
- Add tests.

Acceptance Criteria:

- Compaction produces useful summaries.
- Source traceability is preserved.
- Private memory remains protected.

---

## E20 — Context Packs and Handoffs

### Objective

Generate portable AI-ready context artifacts.

### User Value

Lets users continue work across tools and sessions.

### WP-E20-001 — Implement `monad context pack`

Labels:

```txt
type:work-packet, area:memory, area:cli, priority:p0, status:ready
```

Tasks:

- Read canonical memory files.
- Read workspace manifest.
- Include repo structure summary.
- Include important commands.
- Include ADR list.
- Include policy summary.
- Include verification commands.
- Write latest context pack.
- Write timestamped context pack.
- Avoid private files.

Acceptance Criteria:

- Context pack is generated.
- Context pack is Markdown.
- Context pack excludes private memory.
- Context pack is useful when pasted into an LLM.

### WP-E20-002 — Implement `monad handoff create`

Labels:

```txt
type:work-packet, area:memory, area:cli, priority:p0, status:ready
```

Tasks:

- Generate handoff file.
- Include current repo status.
- Include changed files.
- Include verification section.
- Include next recommended steps.
- Write timestamped handoff.
- Update latest handoff pointer.

Acceptance Criteria:

- Handoff file is generated.
- Handoff file is Markdown.
- Handoff excludes private memory by default.
- Handoff is usable for a fresh AI session.

---

## E21 — AI Tool Exports

### Objective

Provide LLM-agnostic and vendor-specific AI assistant exports.

### User Value

Supports AI development without locking the repo to one provider.

### WP-E21-001 — Implement Generic AI Export

Labels:

```txt
type:work-packet, area:memory, area:cli, priority:p0, status:ready
```

Tasks:

- Implement `monad ai export --target generic`.
- Generate generic assistant instructions.
- Include project summary.
- Include rules for safe AI assistance.
- Include commands.
- Include memory locations.
- Include handoff/context pack locations.

Acceptance Criteria:

- Generic AI export works.
- Output is Markdown.
- Export does not require LLM credentials.

### WP-E21-002 — Implement Vendor-Specific AI Exports

Labels:

```txt
type:work-packet, area:memory, area:ai, priority:p0, status:ready
```

Tasks:

- Implement Claude export.
- Implement Cursor export.
- Implement Copilot export.
- Implement Aider export.
- Implement Continue export.
- Implement Cline export.
- Add adapter docs.
- Add tests/snapshots.

Acceptance Criteria:

- Vendor-specific exports generate expected files.
- Generated files preserve Monad source-of-truth rules.
- Exports are documented.

---

## E22 — Daemon

### Objective

Add local daemon mode for indexing, graph updates, memory maintenance, and context freshness.

### User Value

Keeps repo intelligence current during active development.

### WP-E22-001 — Implement Daemon Lifecycle

Labels:

```txt
type:work-packet, area:cli, area:memory, priority:p0, status:ready
```

Tasks:

- Implement `monad daemon start`.
- Implement `monad daemon stop`.
- Implement `monad daemon status`.
- Add pid/status handling.
- Add logs.
- Add tests where practical.

Acceptance Criteria:

- Daemon can start and stop.
- Status is readable.
- Logs are written.

### WP-E22-002 — Implement Daemon Watchers

Labels:

```txt
type:work-packet, area:memory, area:tooling, priority:p0, status:ready
```

Tasks:

- Watch file changes.
- Update graph cache.
- Update memory index.
- Detect stale context packs.
- Detect ADR drift.
- Detect changed package manifests.
- Avoid destructive writes without policy approval.

Acceptance Criteria:

- Watchers detect changes.
- Index and graph refreshes work.
- Safety rules are enforced.

---

## E23 — Agent Workflow Engine

### Objective

Add safe local AI agent workflow capabilities.

### User Value

Allows AI-assisted development while keeping human approval and auditability.

### WP-E23-001 — Implement Agent Planning

Labels:

```txt
type:work-packet, area:agent, area:cli, priority:p0, status:ready
```

Tasks:

- Implement `monad agent plan`.
- Read context pack.
- Read policies.
- Generate structured execution plan.
- Require approval before execution.
- Add tests/snapshots.

Acceptance Criteria:

- Agent plans are generated.
- Plans reference context and policies.
- Execution is not automatic without approval.

### WP-E23-002 — Implement Agent Run and Review

Labels:

```txt
type:work-packet, area:agent, priority:p0, status:ready
```

Tasks:

- Implement `monad agent run`.
- Implement `monad agent review`.
- Enforce approval gates.
- Capture changed files.
- Capture command logs.
- Generate review summary.

Acceptance Criteria:

- Agent run respects policy gates.
- Review output is generated.
- Changes are auditable.

---

## E24 — Agent Safety and Audit

### Objective

Add agent safety policies and audit logs.

### User Value

Makes agentic development transparent and controllable.

### WP-E24-001 — Create Agent Policies

Labels:

```txt
type:work-packet, area:agent, area:policy, priority:p0, status:ready
```

Tasks:

- Create `policies/agent/agent-permissions.md`.
- Create `policies/agent/human-approval-policy.md`.
- Create `policies/ai/prompt-injection-policy.md`.
- Create `policies/ai/tool-use-policy.md`.
- Create policy examples.

Acceptance Criteria:

- Agent policy docs exist.
- Policies are referenced by CLI commands.

### WP-E24-002 — Implement Agent Audit Log

Labels:

```txt
type:work-packet, area:agent, priority:p0, status:ready
```

Tasks:

- Define audit log schema.
- Log agent plans.
- Log approvals.
- Log commands.
- Log file changes.
- Add audit review command.

Acceptance Criteria:

- Agent actions are auditable.
- Audit logs are machine-readable.
- Audit logs are human-readable.

---

## E25 — Template Generation

### Objective

Add functional template generation commands.

### User Value

Turns the repo into a product factory, not just a static starter.

### WP-E25-001 — Define Template Manifest

Labels:

```txt
type:work-packet, area:templates, priority:p0, status:ready
```

Tasks:

- Define template manifest schema.
- Add examples.
- Add validation command.
- Document template variables.
- Document template constraints.

Acceptance Criteria:

- Template manifest format exists.
- Template validation works.

### WP-E25-002 — Implement `monad add` Commands

Labels:

```txt
type:work-packet, area:templates, area:cli, priority:p0, status:ready
```

Tasks:

- Implement `monad add app`.
- Implement `monad add service`.
- Implement `monad add package`.
- Implement `monad add crate`.
- Implement `monad add infra`.
- Implement `monad add policy`.
- Implement dry-run mode.
- Implement overwrite protection.
- Add tests.

Acceptance Criteria:

- Generation commands create expected files.
- Dry-run output is useful.
- Existing files are protected.

---

## E26 — Plugin System

### Objective

Add a functional plugin system.

### User Value

Allows Monad Factory to extend without hardcoding every capability.

### WP-E26-001 — Define Plugin Manifest and Trust Model

Labels:

```txt
type:work-packet, area:plugins, priority:p0, status:ready
```

Tasks:

- Define plugin manifest schema.
- Define plugin capabilities.
- Define trust model.
- Define verification rules.
- Add example plugin.

Acceptance Criteria:

- Plugin manifest format exists.
- Trust rules are documented.
- Example plugin validates.

### WP-E26-002 — Implement Plugin Commands

Labels:

```txt
type:work-packet, area:plugins, area:cli, priority:p0, status:ready
```

Tasks:

- Implement `monad plugin list`.
- Implement `monad plugin install`.
- Implement `monad plugin verify`.
- Add local plugin loading.
- Add tests.

Acceptance Criteria:

- Plugin commands work.
- Plugin verification works.
- Invalid plugins fail clearly.

---

## E27 — Marketplace Foundation

### Objective

Add local marketplace catalog functionality for templates and plugins.

### User Value

Creates the foundation for reusable ecosystem distribution.

### WP-E27-001 — Define Marketplace Catalog

Labels:

```txt
type:work-packet, area:marketplace, priority:p0, status:ready
```

Tasks:

- Define catalog schema.
- Define catalog entry types.
- Define trust metadata.
- Add local catalog examples.
- Add validation command.

Acceptance Criteria:

- Marketplace catalog exists.
- Catalog validates.
- Example entries are documented.

### WP-E27-002 — Implement Marketplace Commands

Labels:

```txt
type:work-packet, area:marketplace, area:cli, priority:p0, status:ready
```

Tasks:

- Implement `monad marketplace list`.
- Implement `monad marketplace search`.
- Implement `monad marketplace install`.
- Enforce trust checks.
- Add tests.

Acceptance Criteria:

- Marketplace commands work.
- Local catalog can be searched.
- Install respects trust rules.

---

## E28 — Contracts and Schemas

### Objective

Add contract-first structure and validation.

### User Value

Makes the monorepo ready for API governance.

### WP-E28-001 — Create Contract Directories

Labels:

```txt
type:work-packet, area:contracts, priority:p0, status:ready
```

Tasks:

- Create `contracts/openapi`.
- Create `contracts/asyncapi`.
- Create `contracts/json-schema`.
- Create `contracts/protobuf`.
- Add examples.
- Add READMEs.

Acceptance Criteria:

- Contract directories exist.
- Examples exist.
- Purpose is documented.

### WP-E28-002 — Implement Contract Checks

Labels:

```txt
type:work-packet, area:contracts, area:ci, priority:p0, status:ready
```

Tasks:

- Add OpenAPI validation.
- Add AsyncAPI validation.
- Add JSON Schema validation.
- Add Protobuf validation path.
- Add CI checks.
- Add docs.

Acceptance Criteria:

- Contract checks run.
- CI includes contract validation.
- Failures are clear.

---

## E29 — Policy-as-Code

### Objective

Add functional policy-as-code checks.

### User Value

Enforces repository, architecture, security, AI, and release rules.

### WP-E29-001 — Define Policy Model

Labels:

```txt
type:work-packet, area:policy, priority:p0, status:ready
```

Tasks:

- Define policy categories.
- Define policy file layout.
- Define policy result schema.
- Add sample policies.
- Add policy docs.

Acceptance Criteria:

- Policy model exists.
- Policy examples exist.

### WP-E29-002 — Implement Policy Commands

Labels:

```txt
type:work-packet, area:policy, area:cli, priority:p0, status:ready
```

Tasks:

- Implement `monad policy check`.
- Implement `monad policy explain`.
- Implement `monad policy test`.
- Add policy checks for docs.
- Add policy checks for memory.
- Add policy checks for agent approval.
- Add tests.

Acceptance Criteria:

- Policy commands work.
- Policy failures are readable.
- CI can run policy checks.

---

## E30 — Organization Governance

### Objective

Add organization-level governance foundations.

### User Value

Makes the platform usable beyond a single local repo.

### WP-E30-001 — Define Organization Governance Model

Labels:

```txt
type:work-packet, area:governance, priority:p0, status:ready
```

Tasks:

- Define organization roles.
- Define repo ownership model.
- Define approval model.
- Define policy inheritance.
- Define control coverage model.
- Add docs.

Acceptance Criteria:

- Organization governance model exists.
- Roles and approval paths are documented.

### WP-E30-002 — Implement Governance Checks

Labels:

```txt
type:work-packet, area:governance, area:policy, priority:p1, status:ready
```

Tasks:

- Check CODEOWNERS presence.
- Check policy presence.
- Check ADR presence.
- Check approval policy.
- Report governance health.

Acceptance Criteria:

- Governance checks run.
- Results are readable.

---

## E31 — Multi-Repo Federation

### Objective

Add multi-repo federation foundations.

### User Value

Allows Monad Factory to reason about multiple repositories laterally.

### WP-E31-001 — Define Federation Manifest

Labels:

```txt
type:work-packet, area:federation, priority:p0, status:ready
```

Tasks:

- Define federation manifest schema.
- Add repo entry model.
- Add trust model.
- Add sync model.
- Add examples.

Acceptance Criteria:

- Federation manifest exists.
- Example validates.

### WP-E31-002 — Implement Federation Commands

Labels:

```txt
type:work-packet, area:federation, area:cli, priority:p0, status:ready
```

Tasks:

- Implement `monad federation status`.
- Implement repo listing.
- Implement federation validation.
- Add tests.

Acceptance Criteria:

- Federation commands work.
- Invalid manifests fail clearly.

---

## E32 — Local Infrastructure

### Objective

Add local services needed by product development and memory/search workflows.

### User Value

Gives users a serious local-first development foundation.

### WP-E32-001 — Create Docker Compose Baseline

Labels:

```txt
type:work-packet, area:infra, priority:p0, status:ready
```

Tasks:

- Create Compose files.
- Add PostgreSQL.
- Add pgvector profile.
- Add Redis or Valkey.
- Add MinIO.
- Add Mailpit.
- Add OpenTelemetry Collector.
- Add Qdrant.
- Add health checks.
- Add docs.

Acceptance Criteria:

- Local infra starts with one command.
- Services have documented ports.
- Health checks work.

### WP-E32-002 — Add Devcontainer

Labels:

```txt
type:work-packet, area:infra, priority:p1, status:ready
```

Tasks:

- Create `.devcontainer/devcontainer.json`.
- Add Dockerfile if needed.
- Install/reference toolchain.
- Document devcontainer usage.

Acceptance Criteria:

- Devcontainer files exist.
- Devcontainer can support local development.

---

## E33 — Container and Publishing Workflows

### Objective

Add container build and publishing workflows.

### User Value

Makes products distributable.

### WP-E33-001 — Add Dockerfiles

Labels:

```txt
type:work-packet, area:infra, priority:p0, status:ready
```

Tasks:

- Add Dockerfiles for apps/services.
- Add build arguments.
- Add health checks.
- Add local build docs.
- Add CI build checks.

Acceptance Criteria:

- Containers build.
- Build process is documented.

### WP-E33-002 — Add Publishing Workflows

Labels:

```txt
type:work-packet, area:release, priority:p0, status:ready
```

Tasks:

- Add npm publishing workflow.
- Add Rust crate publishing workflow.
- Add Go release workflow.
- Add Python package publishing workflow.
- Add Java publishing workflow.
- Add GHCR publishing workflow.
- Add required approval gates.

Acceptance Criteria:

- Publishing workflows exist.
- Workflows are documented.
- Publishing requires proper approval/secrets.

---

## E34 — Kubernetes and Helm

### Objective

Add functional Kubernetes and Helm deployment paths.

### User Value

Makes the platform cloud/Kubernetes-ready.

### WP-E34-001 — Add Kubernetes Manifests

Labels:

```txt
type:work-packet, area:deployment, priority:p0, status:ready
```

Tasks:

- Add base manifests.
- Add app/service manifests.
- Add config/secrets pattern.
- Add namespace pattern.
- Add docs.
- Add validation.

Acceptance Criteria:

- Manifests validate.
- Deployment path is documented.

### WP-E34-002 — Add Helm Charts

Labels:

```txt
type:work-packet, area:deployment, priority:p0, status:ready
```

Tasks:

- Add Helm chart structure.
- Add values files.
- Add templates.
- Add lint command.
- Add docs.

Acceptance Criteria:

- Helm chart lints.
- Values are documented.

---

## E35 — Terraform/OpenTofu

### Objective

Add functional infrastructure-as-code path.

### User Value

Enables reproducible cloud infrastructure setup.

### WP-E35-001 — Add Terraform/OpenTofu Starter

Labels:

```txt
type:work-packet, area:deployment, area:infra, priority:p0, status:ready
```

Tasks:

- Create `infra/terraform` and/or `infra/opentofu`.
- Add module layout.
- Add local/example environment.
- Add variables.
- Add outputs.
- Add validation commands.
- Add docs.

Acceptance Criteria:

- IaC validates.
- Structure is documented.
- No real secrets are committed.

---

## E36 — ArgoCD, Istio, Nomad, and Vault

### Objective

Add advanced deployment and operations integrations.

### User Value

Makes the platform ready for governed, cloud-native operations.

### WP-E36-001 — Add ArgoCD Integration

Labels:

```txt
type:work-packet, area:deployment, priority:p1, status:ready
```

Tasks:

- Add ArgoCD app definitions.
- Add environment model.
- Add docs.
- Add validation.

Acceptance Criteria:

- ArgoCD definitions exist and validate.

### WP-E36-002 — Add Istio Integration

Labels:

```txt
type:work-packet, area:deployment, priority:p1, status:ready
```

Tasks:

- Add Istio gateway/virtual service examples.
- Add mTLS policy path.
- Add docs.
- Add validation.

Acceptance Criteria:

- Istio path is documented and manifests validate.

### WP-E36-003 — Add Nomad Integration

Labels:

```txt
type:work-packet, area:deployment, priority:p1, status:ready
```

Tasks:

- Add Nomad job definitions.
- Add service definitions.
- Add docs.
- Add validation where practical.

Acceptance Criteria:

- Nomad job examples exist and are documented.

### WP-E36-004 — Add Vault Integration

Labels:

```txt
type:work-packet, area:security, area:deployment, priority:p1, status:ready
```

Tasks:

- Add Vault policy examples.
- Add secret reference model.
- Add local docs.
- Add safety warnings.
- Add validation where practical.

Acceptance Criteria:

- Vault integration path exists.
- Secret handling is documented.

---

## E37 — Observability

### Objective

Add observability foundations.

### User Value

Makes services debuggable and production-aware.

### WP-E37-001 — Add OpenTelemetry Baseline

Labels:

```txt
type:work-packet, area:infra, priority:p0, status:ready
```

Tasks:

- Add OpenTelemetry Collector config.
- Add service instrumentation examples.
- Add local docs.
- Add verification commands.

Acceptance Criteria:

- OTel collector config exists.
- Services document instrumentation path.

### WP-E37-002 — Add Observability Stack Path

Labels:

```txt
type:work-packet, area:infra, priority:p1, status:ready
```

Tasks:

- Add Grafana stack or compatible path.
- Add dashboards folder.
- Add logs/traces/metrics docs.
- Add local profile if practical.

Acceptance Criteria:

- Observability stack path exists.
- Dashboards/docs are present.

---

## E38 — Hosted/Self-Hosted Control Plane

### Objective

Add the foundation for a hosted or self-hosted Monad control plane.

### User Value

Creates the pathway from repo starter to platform product.

### WP-E38-001 — Create Control Plane App

Labels:

```txt
type:work-packet, area:control-plane, priority:p0, status:ready
```

Tasks:

- Create `apps/control-plane`.
- Add basic dashboard shell.
- Add repo status view.
- Add memory status view.
- Add policy status view.
- Add docs.

Acceptance Criteria:

- Control plane app builds.
- Basic status views exist.

### WP-E38-002 — Create Control Plane Services

Labels:

```txt
type:work-packet, area:control-plane, priority:p0, status:ready
```

Tasks:

- Add control-plane API service.
- Add policy API path.
- Add memory API path.
- Add marketplace API path.
- Add auth boundary documentation.
- Add tests.

Acceptance Criteria:

- Control plane services build.
- Health checks work.
- APIs are documented.

---

## E39 — Final v1 Review

### Objective

Verify the maximal functional v1 release is coherent, complete, and usable.

### User Value

Ensures the repo is ready for actual use and future evolution.

### WP-E39-001 — Create v1 Review Checklist

Labels:

```txt
type:work-packet, area:docs, priority:p0, status:ready
```

Tasks:

- Create `docs/product/v1-review.md`.
- Add scope checklist.
- Add command checklist.
- Add docs checklist.
- Add CI checklist.
- Add memory checklist.
- Add agent checklist.
- Add policy checklist.
- Add deployment checklist.
- Add publishing checklist.
- Add known limitations.

Acceptance Criteria:

- Review checklist exists.
- Checklist can be used before v1 tag.
- All v1 capabilities are represented.

### WP-E39-002 — Run Final Verification

Labels:

```txt
type:work-packet, area:ci, priority:p0, status:ready
```

Tasks:

- Run local checks.
- Run CI checks.
- Run CLI smoke tests.
- Run memory checks.
- Run policy checks.
- Run contract checks.
- Run generation checks.
- Run deployment validation checks.
- Record results.

Acceptance Criteria:

- Verification results are documented.
- Blocking failures are resolved or explicitly tracked.

---

## E40 — GitHub Issue Automation

### Objective

Convert the plan into issue-ready artifacts.

### User Value

Makes implementation executable and trackable.

### WP-E40-001 — Generate Issue Markdown Files

Labels:

```txt
type:work-packet, area:ci, area:docs, priority:p0, status:ready
```

Tasks:

- Create `.github/issues/`.
- Generate one Markdown issue file per work packet.
- Include labels.
- Include task checklists.
- Include acceptance criteria.
- Include dependencies where known.

Acceptance Criteria:

- Issue files exist.
- Each work packet has an issue file.
- Files are ready for `gh issue create`.

### WP-E40-002 — Generate GitHub Issue Creation Script

Labels:

```txt
type:work-packet, area:ci, priority:p1, status:ready
```

Tasks:

- Create issue creation script.
- Read generated issue files.
- Call `gh issue create`.
- Support dry-run.
- Document usage.

Acceptance Criteria:

- Script exists.
- Dry-run works.
- Issue creation process is documented.

---

# 15. v1 Definition of Done

The v1 release is done when:

1. The repo can be cloned and understood from the README.
2. The root toolchain is documented and reproducible.
3. `mise install` or equivalent setup is documented.
4. Bun workspace exists and works.
5. moon root tasks exist and work.
6. Nx adapter exists and works.
7. Next.js app exists and builds.
8. TypeScript API exists and checks pass.
9. Rust workspace exists and checks pass.
10. Rust API/service exists and checks pass.
11. Go service exists and checks pass.
12. Python FastAPI service exists and checks pass.
13. Java service exists and checks pass.
14. Docker Compose local infrastructure exists and works.
15. PostgreSQL, Redis/Valkey, MinIO, Mailpit, OTel, pgvector profile, and Qdrant profile are documented and usable.
16. GitHub Actions CI exists.
17. Security workflows exist.
18. Documentation frontmatter checks exist.
19. ADR system exists.
20. Policy docs exist.
21. Policy-as-code commands exist and work.
22. `monad` CLI exists.
23. `monad --help` works.
24. `monad version` works.
25. `monad doctor` works.
26. `monad check` works.
27. `monad graph` works.
28. `monad affected` works.
29. `monad nx` commands work.
30. `monad add app` works.
31. `monad add service` works.
32. `monad add package` works.
33. `monad add crate` works.
34. `monad add infra` works.
35. Monad Memory files exist.
36. SQLite memory backend works.
37. pgvector memory backend path works.
38. Qdrant memory backend path works.
39. `monad memory status` works.
40. `monad memory search` works.
41. `monad memory index` works.
42. `monad memory compact` works.
43. `monad context pack` works.
44. `monad handoff create` works.
45. Generic AI export works.
46. Claude export works.
47. Cursor export works.
48. Copilot export works.
49. Aider export works.
50. Continue export works.
51. Cline export works.
52. Daemon mode works.
53. Agent planning works.
54. Agent execution respects approval gates.
55. Agent audit logs work.
56. Template generation works.
57. Plugin system works.
58. Marketplace catalog works.
59. Contract validation works.
60. Publishing workflows exist and are gated.
61. Container build and publish workflows exist.
62. Kubernetes manifests validate.
63. Helm charts lint.
64. Terraform/OpenTofu validates.
65. ArgoCD integration path validates.
66. Istio integration path validates.
67. Nomad job definitions exist and are documented.
68. Vault integration path exists and is documented.
69. Observability path exists.
70. Remote cache integration exists.
71. Organization governance model exists.
72. Multi-repo federation model exists and has functional commands.
73. Hosted/self-hosted control-plane foundation exists and builds.
74. Work packets are represented as GitHub issue-ready artifacts.
75. Final v1 review checklist passes.

---

# 16. Recommended Immediate Next Step

Before implementation, commit this scope document as the canonical product artifact.

Recommended repository path:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```

Recommended first issue creation order:

```txt
WP-E00-001
WP-E00-002
WP-E01-001
WP-E01-002
WP-E02-001
WP-E02-002
WP-E03-001
WP-E03-002
WP-E04-001
WP-E04-002
WP-E04-003
WP-E05-001
WP-E06-001
WP-E07-001
```

After those are created, begin implementation with the foundation commit:

```bash
mkdir monad-factory && cd monad-factory
git init
```

Then create the repository foundation files and commit:

```bash
git add .
git commit -m "chore: initialize monad-factory foundation"
```

---

# 17. Final Scope Statement

`monad-factory` v1 is a maximal functional, local-first, polyglot, AI-ready, governance-grade product-factory monorepo platform.

It includes the complete functional v1 implementation of the `monad` CLI, root orchestration, polyglot project baselines, local infrastructure, GitHub automation, documentation governance, ADRs, contracts, publishing workflows, templates, generation commands, plugin and marketplace systems, Monad Memory, semantic/vector memory backends, AI adapters, autonomous agent workflow capabilities, daemon mode, full Nx adapter integration, policy-as-code, advanced DevOps integrations, cloud/Kubernetes deployment paths, multi-repo governance foundations, organization governance foundations, and hosted/self-hosted control-plane architecture.

The v1 release remains local-first and usable without forcing AI, cloud, Kubernetes, or hosted services on the user. However, those capabilities are included as functional v1 features rather than deferred roadmap items.

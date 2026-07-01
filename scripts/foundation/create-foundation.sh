#!/usr/bin/env bash
set -euo pipefail

echo "Creating Monad Factory foundation..."

# -------------------------------------------------------------------
# Directories
# -------------------------------------------------------------------

mkdir -p \
  apps/web \
  apps/admin \
  apps/docs \
  apps/control-plane \
  services/api-ts \
  services/api-rust \
  services/api-go \
  services/api-python \
  services/api-java \
  services/auth \
  services/billing \
  services/tenant \
  services/marketplace \
  services/policy-api \
  services/memory-api \
  services/agent-runner \
  packages/config \
  packages/types \
  packages/testing \
  packages/ui \
  packages/sdk-js \
  packages/observability \
  packages/contracts \
  crates/monad-cli \
  crates/monad-core \
  crates/monad-config \
  crates/monad-memory \
  crates/monad-context \
  crates/monad-agent \
  crates/monad-policy \
  crates/monad-nx-adapter \
  crates/monad-template \
  crates/monad-plugin \
  crates/monad-marketplace \
  crates/monad-deploy \
  contracts/openapi \
  contracts/asyncapi \
  contracts/protobuf \
  contracts/json-schema \
  docs/product \
  docs/planning \
  docs/getting-started \
  docs/architecture \
  docs/adr \
  docs/ai \
  docs/memory \
  docs/agents \
  docs/policy \
  docs/deployment \
  docs/publishing \
  docs/tutorials \
  docs/runbooks \
  docs/marketplace \
  docs/federation \
  docs/hosted-control-plane \
  policies/repo \
  policies/security \
  policies/ai \
  policies/release \
  policies/dependency \
  policies/architecture \
  policies/agent \
  policies/memory \
  policies/organization \
  templates/apps \
  templates/services \
  templates/crates \
  templates/packages \
  templates/infra \
  templates/docs \
  templates/policies \
  plugins/examples \
  plugins/registry \
  plugins/schemas \
  marketplace/catalog \
  marketplace/manifests \
  marketplace/trust \
  examples/minimal \
  examples/fullstack-saas \
  examples/polyglot-services \
  examples/ai-assisted-development \
  examples/policy-governed-repo \
  examples/federated-repos \
  infra/compose \
  infra/docker \
  infra/kubernetes \
  infra/helm \
  infra/terraform \
  infra/opentofu \
  infra/argocd \
  infra/istio \
  infra/nomad \
  infra/vault \
  tools/scripts \
  tools/checks \
  tools/generators \
  tools/release \
  tools/security \
  tests/smoke \
  tests/integration \
  tests/contract \
  tests/e2e \
  tests/policy \
  tests/agent \
  tests/memory \
  .github/workflows \
  .github/actions \
  .github/ISSUE_TEMPLATE \
  .devcontainer \
  .monad/memory/canonical \
  .monad/memory/sessions \
  .monad/memory/handoffs \
  .monad/memory/context-packs \
  .monad/memory/indexes \
  .monad/memory/private

find apps services packages crates contracts docs policies templates plugins marketplace examples infra tools tests .monad \
  -type d -empty -exec sh -c 'touch "$1/.gitkeep"' _ {} \;

# -------------------------------------------------------------------
# Root files
# -------------------------------------------------------------------

cat > .gitignore <<'GITIGNORE'
# Dependencies
node_modules/
.bun/
.pnpm-store/
.yarn/
vendor/

# Build outputs
dist/
build/
out/
target/
coverage/
.next/
.turbo/
.nx/
.moon/cache/
.moon/temp/

# Environment
.env
.env.*
!.env.example

# Logs
*.log
logs/

# OS/editor
.DS_Store
Thumbs.db
.idea/
.vscode/*
!.vscode/extensions.json
!.vscode/settings.json

# Python
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
.mypy_cache/
.pyright/
*.pyc

# Java/Gradle
.gradle/
*.class

# Go
bin/

# Local monad private/generated state
.monad/memory/private/*
!.monad/memory/private/.gitignore
.monad/memory/indexes/*
!.monad/memory/indexes/.gitkeep
.monad/runtime/
.monad/cache/
GITIGNORE

cat > .editorconfig <<'EDITORCONFIG'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.{go,rs,py,java}]
indent_size = 4

[Makefile]
indent_style = tab
EDITORCONFIG

cat > .gitattributes <<'GITATTRIBUTES'
* text=auto eol=lf

*.sh text eol=lf
*.md text eol=lf
*.toml text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.json text eol=lf

*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.webp binary
*.ico binary
GITATTRIBUTES

cat > LICENSE <<'LICENSE'
MIT License

Copyright (c) 2026 Thomas Carter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files—the "Software"—to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING
FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
LICENSE

cat > README.md <<'README'
---
title: "Monad Factory"
description: "A maximal functional, polyglot, AI-ready, governance-grade monorepo product-factory platform."
status: "approved"
canonical: true
---

# Monad Factory

`monad-factory` is a maximal functional, local-first, polyglot, AI-ready, governance-grade monorepo product-factory platform.

It is designed to help a developer or team create, govern, build, test, release, deploy, and evolve many products from one standardized monorepo foundation.

## Canonical v1 Scope

The canonical v1 planning artifact is:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```

That document is the source of truth for v1 scope, epics, work packets, tasks, subtasks, sprints, acceptance criteria, and Definition of Done.

## Core v1 Direction

Monad Factory v1 includes:

* polyglot monorepo foundation
* Rust-based `monad` CLI
* Next.js web app
* TypeScript, Rust, Go, Python, and Java services
* root orchestration with `moon`
* toolchain management with `mise`
* Bun workspace
* GitHub automation
* Docker local infrastructure
* Kubernetes/cloud deployment paths
* publishing workflows
* contracts and schemas
* ADRs and governance docs
* policy-as-code
* Monad Memory
* AI tool exports
* daemon mode
* agent workflows
* Nx adapter
* template generation
* plugin system
* marketplace foundation
* multi-repo and organization governance
* hosted/self-hosted control-plane foundation

## Local-First Principle

Monad Factory v1 is local-first. Users should be able to work locally without being forced to use AI, cloud, Kubernetes, or hosted services.

Those capabilities are included as v1 functional platform capabilities, but local development remains the starting point.

## Repository Status

Current stage:

```txt
foundation
```

## Initial Commands

After toolchain setup is added, the expected command surface will grow around:

```bash
monad doctor
monad check
monad graph
monad context pack
monad handoff create
```

## Documentation

Start here:

```txt
docs/00-index.md
```

README

## cat > SECURITY.md <<'SECURITY'

title: "Security Policy"
description: "Security reporting and security expectations for Monad Factory."
status: "approved"
canonical: true
---------------

# Security Policy

## Supported Versions

Monad Factory is currently pre-v1. Until v1 is tagged, security support applies to the main development branch.

## Reporting Security Issues

Do not open public issues for sensitive security vulnerabilities.

Use a private disclosure channel once configured. Until then, contact the repository owner directly.

## Security Principles

Monad Factory should be:

* local-first
* auditable
* least-privilege by default
* safe for AI-assisted development
* careful with secrets
* explicit about network access
* explicit about agent permissions

## Secret Handling

Never commit real secrets.

Use:

```txt
.env.example
```

for placeholder configuration only.
SECURITY

## cat > CONTRIBUTING.md <<'CONTRIBUTING'

title: "Contributing Guide"
description: "Contribution expectations for Monad Factory."
status: "approved"
canonical: true
---------------

# Contributing Guide

## Development Model

Monad Factory uses a work-packet-driven development model.

Each meaningful change should map back to:

* the canonical v1 scope document
* an epic
* a work packet
* acceptance criteria
* verification steps

## Commit Expectations

Use clear conventional commits where practical:

```txt
chore: initialize foundation
docs: add adr system
feat: add monad doctor
fix: correct memory status check
```

## Pull Request Expectations

Every PR should include:

* summary
* linked issue or work packet
* files changed
* verification performed
* risks
* follow-up work

## AI Assistance

AI assistance is allowed, but changes must remain human-reviewable, reproducible, and policy-compliant.

See:

```txt
AGENTS.md
docs/ai/
docs/memory/
policies/ai/
policies/agent/
```

CONTRIBUTING

## cat > CODE_OF_CONDUCT.md <<'CODEOFCONDUCT'

title: "Code of Conduct"
description: "Participation expectations for Monad Factory."
status: "approved"
canonical: true
---------------

# Code of Conduct

Monad Factory should be developed with professionalism, clarity, and respect.

Participants are expected to:

* communicate clearly
* assume good intent
* avoid harassment
* keep technical disagreements focused on evidence
* preserve a constructive development environment

Unacceptable behavior includes harassment, abuse, threats, and intentional disruption.
CODEOFCONDUCT

cat > CODEOWNERS <<'CODEOWNERS'

# Default owner

* @thomascarter613

# Canonical planning and governance

/docs/product/ @thomascarter613
/docs/adr/ @thomascarter613
/policies/ @thomascarter613

# CLI and core Rust crates

/crates/ @thomascarter613

# GitHub automation

/.github/ @thomascarter613
CODEOWNERS

## cat > AGENTS.md <<'AGENTS'

title: "AI Agent Instructions"
description: "Repository instructions for AI assistants and agentic workflows."
status: "approved"
canonical: true
---------------

# AI Agent Instructions

This repository may be developed with AI assistance, but AI use is optional.

## Source of Truth

The canonical v1 planning artifact is:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```

AI assistants must treat that document as the source of truth for v1 scope.

## Development Rules

AI assistants should:

1. Prefer explicit, reviewable changes.
2. Preserve local-first usability.
3. Avoid introducing secrets.
4. Avoid unapproved network dependencies.
5. Keep generated files understandable.
6. Link changes back to work packets.
7. Update documentation when behavior changes.
8. Preserve maximal functional v1 scope.
9. Avoid silently downgrading features to scaffold-only or post-v1.
10. Produce verification commands after meaningful changes.

## Memory and Context

Monad Factory includes Monad Memory for context continuity.

Relevant paths:

```txt
.monad/memory/
docs/memory/
docs/ai/
policies/ai/
policies/agent/
```

Private memory must not be committed unless explicitly exported and reviewed.
AGENTS

cat > workspace.toml <<'WORKSPACE'
name = "monad-factory"
version = "0.1.0"
description = "A maximal functional, polyglot, AI-ready, governance-grade monorepo product-factory platform."
license = "MIT"
owner = "Thomas Carter"
canonical_scope = "docs/product/v1-maximal-functional-scope-and-delivery-plan.md"

[workspace]
stage = "foundation"
local_first = true
polyglot = true
ai_ready = true
governance_grade = true
maximal_functional_v1 = true

[cli]
name = "monad"
language = "rust"

[languages]
typescript = true
rust = true
go = true
python = true
java = true

[capabilities]
monad_memory = true
daemon = true
agent_workflows = true
policy_as_code = true
nx_adapter = true
templates = true
plugins = true
marketplace = true
deployment = true
publishing = true
federation = true
control_plane = true
WORKSPACE

cat > .env.example <<'ENVEXAMPLE'

# Monad Factory example environment file.

# Copy to .env for local-only use.

# Never commit real secrets.

MONAD_ENV=local
MONAD_LOG_LEVEL=info

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=monad
POSTGRES_PASSWORD=monad
POSTGRES_DB=monad_factory

REDIS_HOST=localhost
REDIS_PORT=6379

MINIO_ENDPOINT=[http://localhost:9000](http://localhost:9000)
MINIO_ACCESS_KEY=monad
MINIO_SECRET_KEY=monad-secret

QDRANT_URL=[http://localhost:6333](http://localhost:6333)
ENVEXAMPLE

# -------------------------------------------------------------------

# Documentation indexes

# -------------------------------------------------------------------

## cat > docs/00-index.md <<'EOF_DOCS'

title: "Documentation Index"
description: "Top-level documentation index for Monad Factory."
status: "approved"
canonical: true
---------------

# Documentation Index

## Canonical Product Documents

* [v1 Maximal Functional Scope and Delivery Plan](./product/v1-maximal-functional-scope-and-delivery-plan.md)

## Major Documentation Areas

* [Product](./product/00-index.md)
* [Planning](./planning/00-index.md)
* [Architecture](./architecture/00-index.md)
* [ADRs](./adr/00-index.md)
* [AI](./ai/00-index.md)
* [Memory](./memory/00-index.md)
* [Agents](./agents/00-index.md)
* [Policy](./policy/00-index.md)
* [Deployment](./deployment/00-index.md)
* [Publishing](./publishing/00-index.md)
* [Tutorials](./tutorials/00-index.md)
* [Runbooks](./runbooks/00-index.md)
* [Marketplace](./marketplace/00-index.md)
* [Federation](./federation/00-index.md)
* [Hosted Control Plane](./hosted-control-plane/00-index.md)
  EOF_DOCS

for section in product planning architecture ai memory agents policy deployment publishing tutorials runbooks marketplace federation hosted-control-plane; do
title="$(echo "$section" | tr '-' ' ' | sed 's/\b(.)/\u\1/g')"
cat > "docs/$section/00-index.md" <<EOF_SECTION
-----------------------------------------------

title: "$title Documentation"
description: "$title documentation for Monad Factory."
status: "draft"
canonical: false
----------------

# $title

This section contains $title documentation for Monad Factory.

See the canonical v1 scope document:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```
EOF_SECTION
done

# -------------------------------------------------------------------

# ADR system

# -------------------------------------------------------------------

## cat > docs/adr/0000-adr-template.md <<'ADR_TEMPLATE'

title: "ADR-0000: ADR Template"
description: "Template for Architecture Decision Records."
status: "template"
date: "2026-07-01"
canonical: true
---------------

# ADR-0000: ADR Template

## Status

Template

## Context

Describe the context and forces that led to this decision.

## Decision

Describe the decision.

## Consequences

Describe the expected consequences, trade-offs, and follow-up work.

## Verification

Describe how this decision will be verified or enforced.
ADR_TEMPLATE

## cat > docs/adr/00-index.md <<'ADR_INDEX'

title: "ADR Index"
description: "Architecture Decision Record index for Monad Factory."
status: "approved"
canonical: true
---------------

# ADR Index

|       ADR | Title                                                            | Status   |
| --------: | ---------------------------------------------------------------- | -------- |
|      0000 | ADR Template                                                     | Template |
|      0001 | Use a Maximal Functional Polyglot Product-Factory Monorepo       | Accepted |
|      0002 | Use monad as the Public Repo Control Plane                       | Accepted |
|      0003 | Use mise for Toolchain Management                                | Accepted |
|      0004 | Use Native Language Toolchains Under Root Orchestration          | Accepted |
|      0005 | Use Rust for the monad CLI                                       | Accepted |
|      0006 | Include LLM-Agnostic Monad Memory                                | Accepted |
|      0007 | Keep AI Memory Local-First, Inspectable, and Policy-Governed     | Accepted |
|      0008 | Use Generated AI Tool Adapters                                   | Accepted |
|      0009 | Include Daemon Mode                                              | Accepted |
|      0010 | Include Nx as Graph, Cache, and Affected-Task Adapter            | Accepted |
|      0011 | Keep monad Commands Stable When Underlying Tools Change          | Accepted |
|      0012 | Treat Handoffs and Context Packs as First-Class Artifacts        | Accepted |
|      0013 | Include Policy-as-Code                                           | Accepted |
|      0014 | Include Template, Plugin, and Marketplace Systems                | Accepted |
|      0015 | Include Kubernetes, Cloud, and Advanced DevOps Integration Paths | Accepted |
|      0016 | Include Multi-Repo and Organization Governance Foundations       | Accepted |
|      0017 | Include Hosted and Self-Hosted Control Plane Architecture        | Accepted |
| ADR_INDEX |                                                                  |          |

create_adr() {
local num="$1"
local slug="$2"
local title="$3"
local context="$4"
local decision="$5"
local consequences="$6"
local verification="$7"

## cat > "docs/adr/${num}-${slug}.md" <<EOF_ADR

title: "ADR-${num}: ${title}"
description: "Architecture decision for Monad Factory."
status: "accepted"
date: "2026-07-01"
canonical: true
---------------

# ADR-${num}: ${title}

## Status

Accepted

## Context

${context}

## Decision

${decision}

## Consequences

${consequences}

## Verification

${verification}
EOF_ADR
}

create_adr "0001" "use-maximal-functional-polyglot-product-factory-monorepo" 
"Use a Maximal Functional Polyglot Product-Factory Monorepo" 
"Monad Factory is intended to become a reusable product-factory platform for many products, languages, services, tools, policies, AI workflows, and deployment targets." 
"Monad Factory will use a maximal functional polyglot monorepo architecture as the v1 baseline." 
"The repository will be broader than a narrow starter. Scope will be controlled through clear work packets, verification gates, and canonical documentation rather than by deferring approved v1 capabilities." 
"The repository structure, workspace manifest, documentation, and checks must reflect the maximal functional v1 scope."

create_adr "0002" "use-monad-as-public-repo-control-plane" 
"Use monad as the Public Repo Control Plane" 
"Users need a stable command surface even though underlying tools may evolve." 
"The Rust-based `monad` CLI will be the public control plane for repository checks, graphing, generation, memory, policies, agents, deployment, publishing, plugins, marketplace, and federation." 
"Underlying tools can change without changing the user-facing command model." 
"Core workflows must be reachable through `monad` commands."

create_adr "0003" "use-mise-for-toolchain-management" 
"Use mise for Toolchain Management" 
"Monad Factory is polyglot and requires repeatable local tool versions." 
"`mise` will manage project-level versions for Bun, Node, Rust, Go, Python, Java, Gradle, Terraform/OpenTofu, and other tools where practical." 
"Local setup becomes more reproducible and easier to document." 
"`mise.toml` must exist and tool verification must be documented."

create_adr "0004" "use-native-language-toolchains-under-root-orchestration" 
"Use Native Language Toolchains Under Root Orchestration" 
"Each language ecosystem has mature native tooling that should not be replaced unnecessarily." 
"Monad Factory will use root orchestration while preserving native tools: Bun/TypeScript, Cargo/Rust, Go tooling, uv/Python, and Gradle/Java." 
"The platform avoids creating a brittle custom build system while still providing one coordinated command surface." 
"Task definitions must delegate to native tools and remain documented."

create_adr "0005" "use-rust-for-monad-cli" 
"Use Rust for the monad CLI" 
"The CLI is a long-lived systems component that needs speed, portability, reliability, and strong typing." 
"The `monad` CLI will be implemented in Rust." 
"Rust becomes the foundation for repo analysis, graphing, memory indexing, policies, templates, plugins, and local daemon behavior." 
"The Cargo workspace must include `crates/monad-cli` and core supporting crates."

create_adr "0006" "include-llm-agnostic-monad-memory" 
"Include LLM-Agnostic Monad Memory" 
"AI-assisted development requires durable context, handoffs, decisions, conventions, commands, and project memory across sessions and tools." 
"Monad Factory will include Monad Memory as an LLM-agnostic, local-first memory/context/handoff subsystem." 
"Users are not locked to a specific AI provider, but the repository remains AI-ready." 
"Memory files, commands, policies, and docs must exist and be verifiable."

create_adr "0007" "keep-ai-memory-local-first-inspectable-policy-governed" 
"Keep AI Memory Local-First, Inspectable, and Policy-Governed" 
"Memory systems can leak private information or silently alter project knowledge if not governed." 
"Monad Memory will be local-first, inspectable, auditable, and policy-governed." 
"Private memory must be protected, canonical memory must be explicit, and generated memory artifacts must be reviewable." 
"Private memory ignore rules, memory verification, and memory policy checks must exist."

create_adr "0008" "use-generated-ai-tool-adapters" 
"Use Generated AI Tool Adapters" 
"Different AI tools use different instruction files and conventions." 
"Monad Factory will generate AI tool adapter files from Monad source-of-truth memory and policy files." 
"The repo remains vendor-neutral while supporting Claude, Cursor, Copilot, Aider, Continue, Cline, and generic Markdown contexts." 
"`monad ai export` must support generic and vendor-specific targets."

create_adr "0009" "include-daemon-mode" 
"Include Daemon Mode" 
"Repo intelligence is more useful when graphs, indexes, and context freshness can be maintained during active development." 
"Monad Factory v1 will include daemon mode for local indexing, graph updates, memory maintenance, and context freshness." 
"Daemon behavior must be safe, local, auditable, and policy-aware." 
"`monad daemon start`, `monad daemon stop`, and `monad daemon status` must work."

create_adr "0010" "include-nx-as-graph-cache-affected-task-adapter" 
"Include Nx as Graph, Cache, and Affected-Task Adapter" 
"Nx provides useful graph, affected-project, and caching capabilities." 
"Monad Factory will support Nx as an adapter behind the stable `monad` interface." 
"Users get Nx capabilities without making Nx the only public user experience." 
"`monad nx` and `monad affected` commands must work with documented fallback behavior."

create_adr "0011" "keep-monad-commands-stable-when-underlying-tools-change" 
"Keep monad Commands Stable When Underlying Tools Change" 
"Underlying tools may change over time, but user workflows should stay stable." 
"`monad` commands are the stable public contract for the repo." 
"Internal implementation can delegate to moon, Nx, native language tools, or custom Rust logic." 
"User-facing command behavior must be documented and covered by tests."

create_adr "0012" "treat-handoffs-and-context-packs-as-first-class-artifacts" 
"Treat Handoffs and Context Packs as First-Class Artifacts" 
"AI-assisted development often loses continuity between sessions." 
"Handoff files and context packs will be first-class repository artifacts generated by Monad Memory." 
"Developers can resume work across sessions, tools, and models with less context loss." 
"`monad context pack` and `monad handoff create` must generate useful Markdown artifacts."

create_adr "0013" "include-policy-as-code" 
"Include Policy-as-Code" 
"Governance needs executable checks, not only prose documentation." 
"Monad Factory will include policy-as-code commands and policy result models." 
"Policies can govern docs, architecture, memory, agents, releases, dependencies, and repository health." 
"`monad policy check`, `monad policy explain`, and `monad policy test` must work."

create_adr "0014" "include-template-plugin-and-marketplace-systems" 
"Include Template, Plugin, and Marketplace Systems" 
"A product factory must generate and extend product structures repeatably." 
"Monad Factory will include functional template generation, plugin support, and marketplace catalog foundations." 
"Users can add apps, services, packages, crates, infra, policies, plugins, and catalog entries through governed commands." 
"`monad add`, `monad plugin`, and `monad marketplace` commands must work."

create_adr "0015" "include-kubernetes-cloud-and-advanced-devops-integration-paths" 
"Include Kubernetes, Cloud, and Advanced DevOps Integration Paths" 
"Monad Factory should be local-first but ready for serious cloud-native operations." 
"v1 will include Docker, Compose, Kubernetes, Helm, Terraform/OpenTofu, ArgoCD, Istio, Nomad, Vault, observability, and publishing paths." 
"Users can start locally and progress toward governed deployment without changing repository doctrine." 
"Deployment paths must validate or provide clear verification commands."

create_adr "0016" "include-multi-repo-and-organization-governance-foundations" 
"Include Multi-Repo and Organization Governance Foundations" 
"Product factories may eventually govern multiple repositories and organizational standards." 
"Monad Factory v1 will include multi-repo federation and organization governance foundations." 
"The repo can express ownership, policy inheritance, federation manifests, and governance health." 
"Federation and governance commands/docs must exist and be verifiable."

create_adr "0017" "include-hosted-and-self-hosted-control-plane-architecture" 
"Include Hosted and Self-Hosted Control Plane Architecture" 
"Monad Factory is also the seed of a future monorepo operating system and control plane." 
"v1 will include hosted/self-hosted control-plane architecture and foundation implementation." 
"The control plane can evolve from local repo intelligence toward platform operation." 
"Control-plane app/service foundations must build and expose basic status surfaces."

# -------------------------------------------------------------------

# Policies and Monad memory starter files

# -------------------------------------------------------------------

cat > .monad/config.toml <<'MONAD_CONFIG'
[monad]
version = "0.1.0"
repo = "monad-factory"
canonical_scope = "docs/product/v1-maximal-functional-scope-and-delivery-plan.md"

[memory]
enabled = true
root = ".monad/memory"
private_memory_path = ".monad/memory/private"
canonical_path = ".monad/memory/canonical"

[policy]
enabled = true
root = "policies"

[ai]
enabled = true
vendor_neutral = true

[daemon]
enabled = true

[nx]
enabled = true
MONAD_CONFIG

cat > .monad/memory/private/.gitignore <<'PRIVATE_IGNORE'
*
!.gitignore
PRIVATE_IGNORE

## cat > .monad/memory/MEMORY.md <<'MEMORY'

title: "Monad Memory Index"
description: "Top-level memory index for Monad Factory."
status: "approved"
canonical: true
---------------

# Monad Memory

Monad Memory is the repository-aware memory, context, handoff, and retrieval subsystem for Monad Factory.

Canonical memory lives in:

```txt
.monad/memory/canonical/
```

Private memory lives in:

```txt
.monad/memory/private/
```

Private memory is ignored by default.
MEMORY

for name in project architecture decisions conventions commands glossary agents policies; do
title="$(echo "$name" | sed 's/\b(.)/\u\1/g')"
cat > ".monad/memory/canonical/$name.md" <<EOF_MEMORY
-----------------------------------------------------

title: "$title Memory"
description: "Canonical $name memory for Monad Factory."
status: "draft"
canonical: true
---------------

# $title Memory

This file stores canonical $name memory for Monad Factory.

Source of truth:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```
EOF_MEMORY
done

for policy_file in 
policies/repo/repository-policy.md 
policies/security/security-policy.md 
policies/ai/ai-usage-policy.md 
policies/ai/prompt-injection-policy.md 
policies/release/release-policy.md 
policies/dependency/dependency-policy.md 
policies/architecture/architecture-policy.md 
policies/agent/agent-permissions.md 
policies/agent/human-approval-policy.md 
policies/memory/memory-policy.md 
policies/organization/organization-governance-policy.md
do
mkdir -p "$(dirname "$policy_file")"
title="$(basename "$policy_file" .md | tr '-' ' ' | sed 's/\b(.)/\u\1/g')"
cat > "$policy_file" <<EOF_POLICY
---------------------------------

title: "$title"
description: "$title for Monad Factory."
status: "draft"
canonical: false
----------------

# $title

This policy is part of the Monad Factory v1 maximal functional governance baseline.

The canonical v1 scope document is:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```
EOF_POLICY
done

echo "Foundation created."

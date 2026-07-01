from pathlib import Path

ROOT = Path.cwd()

def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + "\n", encoding="utf-8")

def touch(path: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.touch(exist_ok=True)

directories = [
    "apps/web",
    "apps/admin",
    "apps/docs",
    "apps/control-plane",
    "services/api-ts",
    "services/api-rust",
    "services/api-go",
    "services/api-python",
    "services/api-java",
    "services/auth",
    "services/billing",
    "services/tenant",
    "services/marketplace",
    "services/policy-api",
    "services/memory-api",
    "services/agent-runner",
    "packages/config",
    "packages/types",
    "packages/testing",
    "packages/ui",
    "packages/sdk-js",
    "packages/observability",
    "packages/contracts",
    "crates/monad-cli",
    "crates/monad-core",
    "crates/monad-config",
    "crates/monad-memory",
    "crates/monad-context",
    "crates/monad-agent",
    "crates/monad-policy",
    "crates/monad-nx-adapter",
    "crates/monad-template",
    "crates/monad-plugin",
    "crates/monad-marketplace",
    "crates/monad-deploy",
    "contracts/openapi",
    "contracts/asyncapi",
    "contracts/protobuf",
    "contracts/json-schema",
    "docs/product",
    "docs/planning",
    "docs/getting-started",
    "docs/architecture",
    "docs/adr",
    "docs/ai",
    "docs/memory",
    "docs/agents",
    "docs/policy",
    "docs/deployment",
    "docs/publishing",
    "docs/tutorials",
    "docs/runbooks",
    "docs/marketplace",
    "docs/federation",
    "docs/hosted-control-plane",
    "policies/repo",
    "policies/security",
    "policies/ai",
    "policies/release",
    "policies/dependency",
    "policies/architecture",
    "policies/agent",
    "policies/memory",
    "policies/organization",
    "templates/apps",
    "templates/services",
    "templates/crates",
    "templates/packages",
    "templates/infra",
    "templates/docs",
    "templates/policies",
    "plugins/examples",
    "plugins/registry",
    "plugins/schemas",
    "marketplace/catalog",
    "marketplace/manifests",
    "marketplace/trust",
    "examples/minimal",
    "examples/fullstack-saas",
    "examples/polyglot-services",
    "examples/ai-assisted-development",
    "examples/policy-governed-repo",
    "examples/federated-repos",
    "infra/compose",
    "infra/docker",
    "infra/kubernetes",
    "infra/helm",
    "infra/terraform",
    "infra/opentofu",
    "infra/argocd",
    "infra/istio",
    "infra/nomad",
    "infra/vault",
    "tools/scripts",
    "tools/checks",
    "tools/generators",
    "tools/release",
    "tools/security",
    "tests/smoke",
    "tests/integration",
    "tests/contract",
    "tests/e2e",
    "tests/policy",
    "tests/agent",
    "tests/memory",
    ".github/workflows",
    ".github/actions",
    ".github/ISSUE_TEMPLATE",
    ".devcontainer",
    ".monad/memory/canonical",
    ".monad/memory/sessions",
    ".monad/memory/handoffs",
    ".monad/memory/context-packs",
    ".monad/memory/indexes",
    ".monad/memory/private",
]

for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)
    touch(f"{directory}/.gitkeep")

write(".gitignore", """
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
""")

write(".editorconfig", """
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
""")

write(".gitattributes", """
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
""")

write(".env.example", """
MONAD_ENV=local
MONAD_LOG_LEVEL=info

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=monad
POSTGRES_PASSWORD=monad
POSTGRES_DB=monad_factory

REDIS_HOST=localhost
REDIS_PORT=6379

MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=monad
MINIO_SECRET_KEY=monad-secret

QDRANT_URL=http://localhost:6333
""")

write("workspace.toml", """
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
""")

write("README.md", """
---
title: "Monad Factory"
description: "A maximal functional, polyglot, AI-ready, governance-grade monorepo product-factory platform."
status: "approved"
canonical: true
---

# Monad Factory

`monad-factory` is a maximal functional, local-first, polyglot, AI-ready, governance-grade monorepo product-factory platform.

The canonical v1 planning artifact is:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```

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

## Documentation

Start here:

```txt
docs/00-index.md
```

""")

write("SECURITY.md", """

title: "Security Policy"
description: "Security reporting and security expectations for Monad Factory."
status: "approved"
canonical: true
---------------

# Security Policy

Monad Factory is currently pre-v1. Until v1 is tagged, security support applies to the main development branch.

Never commit real secrets. Use `.env.example` for placeholder configuration only.
""")

write("CONTRIBUTING.md", """

title: "Contributing Guide"
description: "Contribution expectations for Monad Factory."
status: "approved"
canonical: true
---------------

# Contributing Guide

Monad Factory uses a work-packet-driven development model.

Every meaningful change should map back to:

* the canonical v1 scope document
* an epic
* a work packet
* acceptance criteria
* verification steps

AI assistance is allowed, but changes must remain human-reviewable, reproducible, and policy-compliant.
""")

write("CODE_OF_CONDUCT.md", """

title: "Code of Conduct"
description: "Participation expectations for Monad Factory."
status: "approved"
canonical: true
---------------

# Code of Conduct

Monad Factory should be developed with professionalism, clarity, and respect.
""")

write("CODEOWNERS", """

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
""")

write("AGENTS.md", """

title: "AI Agent Instructions"
description: "Repository instructions for AI assistants and agentic workflows."
status: "approved"
canonical: true
---------------

# AI Agent Instructions

The canonical v1 planning artifact is:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```

AI assistants must treat that document as the source of truth for v1 scope.

## Rules

AI assistants should:

1. Prefer explicit, reviewable changes.
2. Preserve local-first usability.
3. Avoid introducing secrets.
4. Avoid unapproved network dependencies.
5. Link changes back to work packets.
6. Update documentation when behavior changes.
7. Preserve maximal functional v1 scope.
8. Avoid silently downgrading features to scaffold-only or post-v1.
9. Produce verification commands after meaningful changes.

Private memory must not be committed unless explicitly exported and reviewed.
""")

write("docs/00-index.md", """

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
""")

doc_sections = {
"product": "Product",
"planning": "Planning",
"architecture": "Architecture",
"ai": "AI",
"memory": "Memory",
"agents": "Agents",
"policy": "Policy",
"deployment": "Deployment",
"publishing": "Publishing",
"tutorials": "Tutorials",
"runbooks": "Runbooks",
"marketplace": "Marketplace",
"federation": "Federation",
"hosted-control-plane": "Hosted Control Plane",
}

for path, title in doc_sections.items():
  write(f"docs/{path}/00-index.md", f"""
--------------------------------------

title: "{title} Documentation"
description: "{title} documentation for Monad Factory."
status: "draft"
canonical: false
----------------

# {title}

This section contains {title} documentation for Monad Factory.

Canonical v1 scope:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```

""")

  write("docs/adr/0000-adr-template.md", """

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
""")

  write("docs/adr/00-index.md", """

title: "ADR Index"
description: "Architecture Decision Record index for Monad Factory."
status: "approved"
canonical: true
---------------

# ADR Index

|  ADR | Title                                                            | Status   |
| ---: | ---------------------------------------------------------------- | -------- |
| 0000 | ADR Template                                                     | Template |
| 0001 | Use a Maximal Functional Polyglot Product-Factory Monorepo       | Accepted |
| 0002 | Use monad as the Public Repo Control Plane                       | Accepted |
| 0003 | Use mise for Toolchain Management                                | Accepted |
| 0004 | Use Native Language Toolchains Under Root Orchestration          | Accepted |
| 0005 | Use Rust for the monad CLI                                       | Accepted |
| 0006 | Include LLM-Agnostic Monad Memory                                | Accepted |
| 0007 | Keep AI Memory Local-First, Inspectable, and Policy-Governed     | Accepted |
| 0008 | Use Generated AI Tool Adapters                                   | Accepted |
| 0009 | Include Daemon Mode                                              | Accepted |
| 0010 | Include Nx as Graph, Cache, and Affected-Task Adapter            | Accepted |
| 0011 | Keep monad Commands Stable When Underlying Tools Change          | Accepted |
| 0012 | Treat Handoffs and Context Packs as First-Class Artifacts        | Accepted |
| 0013 | Include Policy-as-Code                                           | Accepted |
| 0014 | Include Template, Plugin, and Marketplace Systems                | Accepted |
| 0015 | Include Kubernetes, Cloud, and Advanced DevOps Integration Paths | Accepted |
| 0016 | Include Multi-Repo and Organization Governance Foundations       | Accepted |
| 0017 | Include Hosted and Self-Hosted Control Plane Architecture        | Accepted |
""")

adrs = [
("0001", "use-maximal-functional-polyglot-product-factory-monorepo", "Use a Maximal Functional Polyglot Product-Factory Monorepo"),
("0002", "use-monad-as-public-repo-control-plane", "Use monad as the Public Repo Control Plane"),
("0003", "use-mise-for-toolchain-management", "Use mise for Toolchain Management"),
("0004", "use-native-language-toolchains-under-root-orchestration", "Use Native Language Toolchains Under Root Orchestration"),
("0005", "use-rust-for-monad-cli", "Use Rust for the monad CLI"),
("0006", "include-llm-agnostic-monad-memory", "Include LLM-Agnostic Monad Memory"),
("0007", "keep-ai-memory-local-first-inspectable-policy-governed", "Keep AI Memory Local-First, Inspectable, and Policy-Governed"),
("0008", "use-generated-ai-tool-adapters", "Use Generated AI Tool Adapters"),
("0009", "include-daemon-mode", "Include Daemon Mode"),
("0010", "include-nx-as-graph-cache-affected-task-adapter", "Include Nx as Graph, Cache, and Affected-Task Adapter"),
("0011", "keep-monad-commands-stable-when-underlying-tools-change", "Keep monad Commands Stable When Underlying Tools Change"),
("0012", "treat-handoffs-and-context-packs-as-first-class-artifacts", "Treat Handoffs and Context Packs as First-Class Artifacts"),
("0013", "include-policy-as-code", "Include Policy-as-Code"),
("0014", "include-template-plugin-and-marketplace-systems", "Include Template, Plugin, and Marketplace Systems"),
("0015", "include-kubernetes-cloud-and-advanced-devops-integration-paths", "Include Kubernetes, Cloud, and Advanced DevOps Integration Paths"),
("0016", "include-multi-repo-and-organization-governance-foundations", "Include Multi-Repo and Organization Governance Foundations"),
("0017", "include-hosted-and-self-hosted-control-plane-architecture", "Include Hosted and Self-Hosted Control Plane Architecture"),
]

for number, slug, title in adrs:
  write(f"docs/adr/{number}-{slug}.md", f"""
------------------------------------------

title: "ADR-{number}: {title}"
description: "Architecture decision for Monad Factory."
status: "accepted"
date: "2026-07-01"
canonical: true
---------------

# ADR-{number}: {title}

## Status

Accepted

## Context

Monad Factory v1 is a maximal functional, polyglot, AI-ready, governance-grade product-factory platform.

## Decision

Monad Factory accepts this decision as part of the v1 platform foundation: **{title}**.

## Consequences

This decision must be reflected in the repository structure, documentation, work packets, verification checks, and future implementation.

## Verification

Verification will be performed through repository checks, documentation review, ADR review, and work-packet acceptance criteria.
""")

  write(".monad/config.toml", """
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
""")

  write(".monad/memory/private/.gitignore", """
*
!.gitignore
""")

  write(".monad/memory/MEMORY.md", """

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
""")

memory_files = [
"project",
"architecture",
"decisions",
"conventions",
"commands",
"glossary",
"agents",
"policies",
]

for name in memory_files:
  title = name.replace("-", " ").replace("_", " ").title()
  write(f".monad/memory/canonical/{name}.md", f"""
------------------------------------------------

title: "{title} Memory"
description: "Canonical {name} memory for Monad Factory."
status: "draft"
canonical: true
---------------

# {title} Memory

This file stores canonical {name} memory for Monad Factory.

Source of truth:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```

""")

policy_files = {
"policies/repo/repository-policy.md": "Repository Policy",
"policies/security/security-policy.md": "Security Policy",
"policies/ai/ai-usage-policy.md": "AI Usage Policy",
"policies/ai/prompt-injection-policy.md": "Prompt Injection Policy",
"policies/release/release-policy.md": "Release Policy",
"policies/dependency/dependency-policy.md": "Dependency Policy",
"policies/architecture/architecture-policy.md": "Architecture Policy",
"policies/agent/agent-permissions.md": "Agent Permissions",
"policies/agent/human-approval-policy.md": "Human Approval Policy",
"policies/memory/memory-policy.md": "Memory Policy",
"policies/organization/organization-governance-policy.md": "Organization Governance Policy",
}

for path, title in policy_files.items():
  write(path, f"""
----------------

title: "{title}"
description: "{title} for Monad Factory."
status: "draft"
canonical: false
----------------

# {title}

This policy is part of the Monad Factory v1 maximal functional governance baseline.

Canonical v1 scope:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```

""")

print("Foundation repair complete.")

# ADR-0012: Use Packs and Plugins for Ecosystem Extensibility

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will use **packs** and **plugins** as the primary mechanisms for ecosystem extensibility.

Packs will package reusable declarative assets such as:

- app templates
- service templates
- package templates
- documentation templates
- policy packs
- workflow recipes
- migration recipes
- modernization recipes
- infrastructure templates
- compliance templates
- AI context templates
- golden path implementations

Plugins will package executable or semi-executable integrations such as:

- tool adapters
- provider adapters
- graph analyzers
- policy evaluators
- evidence collectors
- code generators
- migration engines
- integration sync connectors
- custom commands
- SaaS connectors

The initial local core does not need a full plugin runtime or marketplace.

However, Monad OS should be designed so extensibility is not an afterthought.

---

# 1. Context

Monad OS is intended to become an SDLC control plane and monorepo operating system.

It must support many different repository types, teams, languages, tools, providers, industries, and maturity levels.

Hard-coding every possible workflow into the core would make Monad OS too large, too rigid, and too difficult to evolve.

The system needs an extensibility model that can support:

- official defaults
- community contributions
- enterprise customization
- productized consulting assets
- future marketplace distribution
- industry-specific governance
- migration and modernization recipes
- tool/provider integration adapters

Therefore, Monad OS needs both packs and plugins.

---

# 2. Definitions

## Pack

A pack is a reusable bundle of declarative assets.

Packs are primarily data, templates, configuration, documentation, and recipes.

Examples:

```txt
packs/apps/saas-web
packs/services/fastapi-service
packs/services/elysia-service
packs/data/postgres-drizzle
packs/docs/fumadocs
packs/policies/startup-default
packs/policies/soc2-readiness
packs/workflows/release-evidence
packs/migrations/polyrepo-to-monorepo
```

## Plugin

A plugin is a reusable extension that provides behavior.

Plugins may include executable code, adapters, analyzers, or command extensions.

Examples:

```txt
plugins/task-backend-nx
plugins/build-backend-pants
plugins/build-backend-buck2
plugins/ai-provider-ollama
plugins/cloud-provider-aws
plugins/data-provider-postgres
plugins/integration-github
plugins/evidence-trivy
plugins/policy-opa
```

## Relationship

A pack may depend on plugins.

Example:

```txt
The "multi-tenant-saas" pack may depend on:
  - data-provider-postgres plugin
  - task-backend-nx plugin
  - docs-fumadocs pack
  - policy-startup-default pack
```

---

# 3. Alternatives Considered

## Alternative 1: Put all functionality in the core

Monad OS could implement every generator, integration, policy, backend, template, and workflow directly inside the core CLI.

### Advantages

* Simpler early architecture.
* Easier to reason about at small scale.
* Fewer package/runtime boundaries.
* Easier initial distribution.

### Disadvantages

* Core becomes bloated.
* Harder to support many ecosystems.
* Harder for users to customize.
* Harder for community or enterprise extensions.
* Harder to build a marketplace.
* Harder to support productized consulting workflows.
* Slower core development over time.

### Decision

Rejected.

The core should be powerful but extensible.

---

## Alternative 2: Use only templates, no plugins

Monad OS could support template packs but avoid executable plugins.

### Advantages

* Safer.
* Easier to implement.
* Easier to audit.
* Works well for scaffolding.

### Disadvantages

* Insufficient for tool adapters.
* Insufficient for provider integrations.
* Insufficient for graph analyzers.
* Insufficient for evidence collectors.
* Insufficient for complex migration workflows.
* Insufficient for future SaaS integration sync.

### Decision

Rejected.

Templates are necessary but not sufficient.

---

## Alternative 3: Use only plugins, no packs

Monad OS could make everything a plugin.

### Advantages

* Maximum flexibility.
* Powerful extension model.
* Easier to model all extensions uniformly.

### Disadvantages

* Too much power for simple templates.
* Worse security posture.
* Harder to inspect.
* Harder for non-programmers to author.
* Harder to version declarative governance and recipes.
* Unnecessary complexity for common use cases.

### Decision

Rejected.

Packs and plugins should be separate concepts.

---

## Alternative 4: Use packs for declarative assets and plugins for behavior

Monad OS can use packs for reusable content/configuration/templates and plugins for executable behavior/adapters.

### Advantages

* Clear separation of concerns.
* Safer default extensibility.
* Supports simple and advanced use cases.
* Supports future marketplace.
* Supports enterprise customization.
* Supports productized service delivery.
* Supports local-first operation.
* Supports future hosted control plane.

### Disadvantages

* Requires two extension concepts.
* Requires dependency/version management.
* Requires documentation.
* Requires trust and security model.
* Requires compatibility checks.

### Decision

Accepted.

---

# 4. Rationale

Monad OS needs to become more than one person's hard-coded toolchain.

The long-term value depends on reusable knowledge:

* how to scaffold systems
* how to govern systems
* how to document systems
* how to secure systems
* how to migrate systems
* how to connect tools
* how to collect evidence
* how to operate AI safely

Packs and plugins allow Monad OS to encode this reusable knowledge without making the core unmanageable.

The rule is:

> Core owns the platform model. Packs and plugins extend the platform.

---

# 5. Pack Categories

Monad OS should eventually support several pack categories.

## App Packs

Examples:

```txt
web-app
admin-app
docs-app
mobile-app
desktop-app
console-app
```

## Service Packs

Examples:

```txt
fastapi-service
elysia-service
go-service
rust-service
java-service
worker-service
workflow-service
rag-service
```

## Package Packs

Examples:

```txt
typescript-library
rust-crate
go-module
python-package
ui-package
sdk-package
config-package
testing-package
```

## Data Packs

Examples:

```txt
postgres-drizzle
postgres-prisma
sqlite-local
mongodb
qdrant
clickhouse
redis-valkey
eventstore
```

## Infrastructure Packs

Examples:

```txt
docker-compose-local
devcontainer
kubernetes
helm
terraform
pulumi
cloudflare
nomad
argocd
```

## Documentation Packs

Examples:

```txt
fumadocs
adr-system
prd-system
runbook-system
api-docs
developer-portal
```

## Policy Packs

Examples:

```txt
startup-default
enterprise-default
ai-governance
soc2-readiness
nist-ssdf
slsa
owasp-samm
```

## Workflow Packs

Examples:

```txt
release-evidence
security-baseline
dependency-maintenance
incident-response
architecture-review
ai-assisted-change
```

## Migration Packs

Examples:

```txt
polyrepo-to-monorepo
npm-to-bun
manual-docs-to-fumadocs
legacy-ci-to-dagger
ungoverned-repo-to-monad
```

---

# 6. Plugin Categories

Monad OS should eventually support plugin categories.

## Tool Backend Plugins

Examples:

```txt
nx
moon
turborepo
pants
buck2
dagger
nix
biome
lefthook
```

## Provider Plugins

Examples:

```txt
ai-provider-openai
ai-provider-anthropic
ai-provider-ollama
cloud-provider-aws
cloud-provider-gcp
cloud-provider-cloudflare
data-provider-postgres
data-provider-qdrant
```

## Integration Plugins

Examples:

```txt
github
gitlab
jira
linear
slack
notion
monday
backstage
datadog
grafana
```

## Analysis Plugins

Examples:

```txt
dependency-analyzer
architecture-drift-analyzer
docs-drift-analyzer
risk-analyzer
security-analyzer
cost-analyzer
```

## Evidence Plugins

Examples:

```txt
test-evidence-junit
coverage-evidence
trivy-evidence
syft-sbom
cosign-signature
slsa-provenance
github-actions-evidence
```

---

# 7. Initial Pack Format

The first pack format should be simple and file-based.

Example:

```txt
packs/services/fastapi-service/
  pack.toml
  README.md
  templates/
  docs/
  hooks/
```

Example `pack.toml`:

```toml
[pack]
id = "service-fastapi"
name = "FastAPI Service"
version = "0.1.0"
type = "service-template"

[compatibility]
monad = ">=0.1.0"
languages = ["python"]
requires = []

[templates]
root = "templates"

[outputs]
creates = [
  "services/{{name}}",
  "docs/services/{{name}}.md"
]
```

The initial format should avoid unnecessary complexity.

---

# 8. Initial Plugin Model

The plugin model should be designed carefully because plugins can execute behavior.

The earliest implementation does not need arbitrary executable plugins.

Recommended progression:

## v0/v1

Use built-in adapters only.

Examples:

```txt
built-in nx adapter
built-in docs checker
built-in foundation checker
```

## v1.5

Add declarative packs.

Examples:

```txt
packs/apps/*
packs/services/*
packs/policies/*
```

## v2+

Add controlled plugin runtime.

Potential plugin execution options:

```txt
subprocess plugins
WASM plugins
RPC plugins
containerized plugins
signed native plugins
```

The plugin security model should be designed before arbitrary third-party plugins are allowed.

---

# 9. Marketplace Implications

Packs and plugins create the basis for a future marketplace.

Marketplace assets may include:

* official packs
* community packs
* enterprise packs
* industry packs
* migration packs
* integration plugins
* policy packs
* AI workflow packs
* evidence collectors

The marketplace can support:

* free assets
* paid assets
* verified assets
* private organization assets
* enterprise-approved catalogs

This is a major product moat.

---

# 10. Productized Service Implications

Packs and plugins support consulting/productized service offerings.

Examples:

```txt
"Apply SOC 2 readiness pack"
"Modernize this repo using the governed monorepo pack"
"Convert this docs system to Fumadocs"
"Add AI governance pack"
"Add SLSA-oriented supply-chain pack"
"Generate release evidence workflow"
```

This allows repeatable service delivery.

A consultant can apply a pack, run checks, produce a report, and sell remediation.

---

# 11. Manifest Implications

`workspace.toml` should eventually declare active packs and plugins.

Example:

```toml
[packs]
active = [
  "startup-default",
  "fumadocs",
  "service-fastapi",
  "ai-governance"
]

[plugins]
enabled = [
  "task-backend-nx",
  "docs-fumadocs"
]
```

The manifest should record intent.

Generated state can live in `.monad/`.

---

# 12. Trust and Security Requirements

Packs and plugins require a trust model.

Future trust levels:

```txt
official
verified
community
private
local
untrusted
```

Policy requirements:

* unsigned plugins may be blocked in strict mode
* plugins should declare permissions
* plugins should declare file access needs
* plugins should declare network access needs
* high-risk plugins require approval
* marketplace plugins should be reviewed or signed

This is especially important for enterprise adoption.

---

# 13. File Ownership

Packs may generate files.

Monad should eventually track generated file ownership.

Future file:

```txt
.monad/file-ownership.json
```

Possible ownership categories:

```txt
user-authored
monad-generated
pack-generated
plugin-generated
native-tool-generated
shared
```

This allows safer regeneration and updates.

---

# 14. Versioning Requirements

Packs and plugins should be versioned.

Versioning should support:

* compatibility checks
* upgrades
* lockfiles
* reproducibility
* marketplace publishing
* enterprise approval

Possible future lockfile:

```txt
monad.lock
```

The lockfile may eventually track installed packs/plugins and versions.

---

# 15. Non-Goals

This decision does not mean:

* full plugin runtime is required in v0
* marketplace is required in v0
* arbitrary third-party code should run immediately
* every feature must be a plugin
* the core should be empty
* packs and plugins are the same thing
* policy packs replace all policy engines
* templates replace all generators

This decision establishes the extensibility model.

---

# 16. Initial Scope

## v0

* Document packs/plugins architecture.
* Keep core implementation simple.
* No arbitrary plugin runtime.
* No marketplace.

## v0.1

* Add basic built-in templates.
* Add pack-like internal structure if helpful.

## v0.2

* Add `monad pack list`.
* Add basic local declarative packs.
* Add app/package/service generation from packs.

## v1

* Stabilize local packs.
* Add pack manifest.
* Add pack documentation.
* Add simple pack dependency checks.
* Keep plugins mostly built-in.

## v1.5

* Add plugin contract design.
* Add controlled plugin execution model.
* Add official adapter plugins.
* Add pack/plugin lockfile support.

## v2

* Add hosted marketplace.
* Add verified packs/plugins.
* Add organization-level catalogs.
* Add enterprise approval workflows.

---

# 17. Risks

## Risk: Plugin security issues

Mitigation:

* Do not allow arbitrary executable plugins early.
* Prefer declarative packs first.
* Add permissions and signing later.
* Consider WASM or sandboxed execution.

## Risk: Extension system overcomplicates core

Mitigation:

* Keep v0/v1 simple.
* Start with built-in templates.
* Add formal extensibility only when patterns stabilize.

## Risk: Marketplace distracts from core product

Mitigation:

* Build local core first.
* Treat marketplace as v2+.

## Risk: Pack fragmentation

Mitigation:

* Provide official defaults.
* Use compatibility metadata.
* Provide clear docs and validation.

## Risk: Breaking changes

Mitigation:

* Version pack/plugin schemas.
* Use lockfiles.
* Provide migration tools.

---

# 18. Success Criteria

This decision is successful if:

1. Monad OS can start with built-in defaults.
2. Monad OS can later support reusable packs.
3. Monad OS can later support controlled plugins.
4. Packs can encode templates, policies, workflows, and migrations.
5. Plugins can encode adapters, analyzers, and evidence collectors.
6. The extension model supports a future marketplace.
7. The extension model supports productized services.
8. The core remains focused on lifecycle graph, policy, evidence, recommendations, and orchestration.

---

# 19. Final Decision Statement

Monad OS will use packs and plugins for ecosystem extensibility.

Packs will package reusable declarative assets.

Plugins will package executable behavior and integrations.

The initial implementation may be simple, but the architecture will preserve a path to an extensible ecosystem and future marketplace.


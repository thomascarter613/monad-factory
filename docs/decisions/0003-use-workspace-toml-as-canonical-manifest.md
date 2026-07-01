# ADR-0003: Use `workspace.toml` as the Canonical Manifest

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will use a root-level `workspace.toml` file as the initial canonical manifest for the local workspace.

The manifest will describe the declared intent of the repository, including:

- workspace identity
- product stage
- architectural principles
- toolchain defaults
- documentation configuration
- project registry
- policy configuration
- AI configuration
- cloud strategy
- database capability strategy
- future SaaS synchronization metadata

The manifest is not intended to replace every native tool configuration file.

Instead, it is the **Monad-owned source of intent** from which Monad can validate, generate, coordinate, and explain the repository.

---

# 1. Context

Monad OS needs a stable local source of truth.

The system will eventually coordinate many tools and artifacts, including:

- docs
- apps
- services
- packages
- policies
- AI context
- CI/CD
- project graph
- generated files
- recommendations
- evidence
- release metadata
- cloud/database/provider configuration
- underlying tool backends such as Nx, moon, Dagger, Pants, Buck2, and others

Without a canonical manifest, Monad OS would have to infer too much from scattered files.

That would weaken:

- explainability
- validation
- recommendations
- generation
- AI context
- SaaS synchronization
- policy enforcement
- future migration support

Monad OS therefore needs a declared workspace model.

---

# 2. Alternatives Considered

## Alternative 1: Use `package.json` as the canonical manifest

### Advantages

- Familiar to JavaScript/TypeScript developers.
- Already exists in many repos.
- Works naturally with Bun, pnpm, npm, and Yarn.
- Easy to parse.

### Disadvantages

- Too JavaScript-specific.
- Poor fit for polyglot repositories.
- Weak fit for SDLC objects such as policies, evidence, AI context, cloud/database capabilities, and lifecycle graph metadata.
- Would make Monad OS feel like a JS-only monorepo tool.

### Decision

Rejected.

`package.json` may exist in generated repos, but it should not be the canonical Monad OS manifest.

---

## Alternative 2: Use `monad.toml`

### Advantages

- Product-specific.
- Clear ownership by Monad OS.
- Avoids ambiguity with generic workspace concepts.
- Similar to tool-specific config names used by many developer tools.

### Disadvantages

- Slightly less descriptive of what the file models.
- Could imply that all configuration belongs to Monad itself rather than the broader workspace.
- Less aligned with the idea that the workspace is the primary local system of record.

### Decision

Rejected for now, but reserved as a possible future compatibility alias.

---

## Alternative 3: Use `.monad/workspace.toml`

### Advantages

- Keeps root directory cleaner.
- Clearly groups Monad-specific files under `.monad/`.
- Useful for generated state, cache, indexes, and internal metadata.

### Disadvantages

- Less visible.
- Easier for users to overlook.
- Less convenient as the human-readable root manifest.
- Makes the primary source of workspace intent feel hidden.

### Decision

Rejected for the canonical manifest.

The `.monad/` directory should be used for state, cache, indexes, generated context, recommendations, and internal metadata.

---

## Alternative 4: Use YAML

### Advantages

- Common in infrastructure and CI tooling.
- Good for nested configuration.
- Familiar to many developers.

### Disadvantages

- More footguns around indentation and type ambiguity.
- Less strict and predictable.
- TOML is generally cleaner for human-authored configuration with explicit sections.

### Decision

Rejected for the initial canonical manifest.

YAML may still be used for generated files, CI, policies, answers, and interop.

---

## Alternative 5: Use JSON

### Advantages

- Extremely machine-friendly.
- Easy schema validation.
- Common for generated files.

### Disadvantages

- Poorer human authoring experience.
- Comments are not standard.
- Verbose for configuration.
- Less pleasant for long-lived hand-edited repo manifests.

### Decision

Rejected for the human-authored canonical manifest.

JSON may be used for generated graph, recommendation, evidence, and sync artifacts.

---

## Alternative 6: Use root-level `workspace.toml`

### Advantages

- Human-readable.
- Root-visible.
- Language-agnostic.
- Product-agnostic enough to describe the repository as a whole.
- Easy to parse from Rust.
- Supports structured configuration.
- Good fit for a declarative local source of truth.
- Does not imply JavaScript-only assumptions.
- Works well with generated native tool configs.

### Disadvantages

- New convention.
- May overlap with other tools if they also use `workspace.toml`.
- Requires Monad OS to define and version its own schema.

### Decision

Accepted.

---

# 3. Rationale

`workspace.toml` is the best initial manifest name because Monad OS is fundamentally concerned with the workspace as a governed software system.

The file should not merely describe Monad settings.

It should describe the workspace's declared intent.

This supports the larger product thesis:

> Monad OS owns intent, graph, policy, evidence, and workflow. Native tools provide replaceable execution backends.

The manifest should eventually become the root of:

- graph generation
- repo inspection
- toolchain recommendation
- project registry
- policy validation
- docs validation
- AI context generation
- cloud/database capability mapping
- SaaS synchronization

---

# 4. Consequences

## Positive Consequences

- Monad OS has a clear local source of truth.
- The repo can be inspected predictably.
- Recommendations and generated files can be explained.
- The project graph has a declared foundation.
- AI context can be generated from structured intent.
- Future SaaS sync has a stable local anchor.
- Tooling can remain replaceable.

## Negative Consequences

- Monad OS must define and maintain a manifest schema.
- Users must learn one new file.
- Some configuration will still live in native tool files.
- Care must be taken to avoid duplicating too much native tool configuration.

## Mitigations

- Keep the v0 manifest small.
- Version the manifest schema.
- Generate native tool configs where appropriate.
- Document which fields are canonical versus derived.
- Provide `monad doctor` checks.
- Provide `monad explain workspace`.
- Allow migration commands as the schema evolves.

---

# 5. Manifest Responsibilities

The manifest should eventually describe:

## Workspace Identity

- name
- description
- stage
- repository type
- private/public status
- product identity

## Principles

- AI agnosticism
- cloud agnosticism
- database agnosticism
- local-first behavior
- SaaS readiness
- graph-native design
- policy control
- evidence orientation

## Toolchain Defaults

- package manager
- docs framework
- task backend
- build backend
- CI execution strategy
- reproducibility strategy
- security baseline
- formatter/linter
- test strategy

## Projects

- apps
- services
- packages
- libraries
- tools
- docs
- infrastructure modules
- agents
- policies

## SDLC Metadata

- owners
- risks
- decisions
- docs
- requirements
- evidence
- releases
- deployments

## Provider Strategies

- AI provider strategy
- cloud provider strategy
- database capability strategy
- observability strategy
- feature flag strategy
- secrets strategy

---

# 6. Initial Example

The initial seed manifest may look like:

```toml
[workspace]
name = "monad-os"
stage = "pre-implementation-architecture-and-product-strategy"
description = "AI-agnostic SDLC control plane and monorepo operating system."
private = true

[identity]
category = "AI-native SDLC Control Plane"
product = "Monad OS"
technical_identity = "Monorepo Operating System"
commercial_identity = "Governed software delivery platform for AI-era engineering teams"

[principles]
ai_agnostic = true
cloud_agnostic = true
database_agnostic = true
local_first = true
saas_ready = true
graph_native = true
declarative = true
policy_controlled = true
evidence_oriented = true
toolchain_composable = true

[docs]
default_docs_frontend = "fumadocs"
canonical_docs_dir = "docs"

[toolchain.defaults]
cli_language = "rust"
package_manager = "bun"
docs = "fumadocs"
task_backend_default = "nx-under-monad-wrapper"
polyglot_task_backend_optional = "moon"
ci_execution = "dagger"
strict_reproducibility_optional = "nix"
7. Schema Versioning
The manifest should eventually include a schema version.

Example:

TOML
￼
[monad]
schema_version = "0.1"
Schema versioning is not required in the earliest seed file, but should be added before the CLI begins enforcing strict validation.

8. Interaction With Native Tool Configs
workspace.toml should not eliminate native tool configuration.

Native files may still exist:

package.json

nx.json

turbo.json

moon.yml

biome.json

lefthook.yml

renovate.json

.github/workflows/*.yml

Dockerfile

docker-compose.yml

next.config.*

source.config.ts

Cargo.toml

Monad OS should define which files are:

canonical

generated

user-owned

synchronized

validated

ignored

This distinction should be formalized later.

9. Non-Goals
This decision does not mean:

every native tool config disappears

every field must live in workspace.toml

the manifest schema is final

all project metadata must be manually written

generated state belongs in workspace.toml

Generated state should generally live under:

￼
.monad/
Examples:

￼
.monad/answers.yaml
.monad/recommendation.json
.monad/graph.json
.monad/context/
.monad/cache/
.monad/state/
10. Success Criteria
This decision is successful if:

Users can understand the repository's declared intent by reading workspace.toml.

Monad CLI can parse the manifest.

Monad CLI can validate required fields.

Monad CLI can generate useful recommendations from it.

Monad CLI can build or enrich a project graph from it.

The manifest supports AI, cloud, and database agnosticism.

The manifest supports future SaaS synchronization.

The manifest does not become an unmaintainable dumping ground.

11. Final Decision Statement
Monad OS will use root-level workspace.toml as the initial canonical workspace manifest.

It will represent repository intent, not every implementation detail.

Native tool configuration files remain allowed and expected.


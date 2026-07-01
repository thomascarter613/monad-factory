# ADR-0005: Use Fumadocs for Documentation

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will use **Fumadocs** as the approved default documentation frontend.

The canonical documentation source will remain in:

```txt
docs/

The future rendered documentation application should live in:

apps/docs/

This establishes a two-layer documentation model:

docs/      = canonical repository documentation
apps/docs/ = documentation website/application using Fumadocs

Monad OS will treat documentation as a first-class SDLC artifact.

Documentation will not be optional or secondary. It will be part of the product's architecture, governance, onboarding, AI context, evidence, and future SaaS synchronization model.

1. Context

Monad OS is an SDLC control plane and monorepo operating system.

It requires strong documentation from the beginning because the product depends on:

product strategy
product requirements
architecture decisions
domain models
CLI references
manifest references
governance rules
SDLC process definitions
policy explanations
toolchain explanations
onboarding tutorials
runbooks
evidence explanations
AI usage guidance
future pack/plugin documentation

Without excellent documentation, Monad OS risks becoming too abstract, too complex, or too difficult to adopt.

The documentation system must support both:

human-readable repository docs
future published product documentation
2. Alternatives Considered
Alternative 1: Plain Markdown only

Monad OS could use only plain Markdown files in docs/.

Advantages
Simple.
No framework dependency.
Easy to read in GitHub.
Easy to edit.
Works before any app/tooling exists.
Excellent for early planning.
Disadvantages
Limited navigation.
Limited search.
Limited docs UX.
Harder to present as a polished product.
Less suitable for public documentation.
Less suitable for commercial SaaS/productized service positioning.
Decision

Partially accepted.

Plain Markdown in docs/ remains the canonical source format, but a docs frontend is still needed.

Alternative 2: Docusaurus
Advantages
Mature.
Popular.
Strong documentation site capabilities.
Good plugin ecosystem.
Common in open-source projects.
Disadvantages
Heavier than desired.
React-based but not as aligned with the desired modern app/documentation composition.
May feel separate from the intended application platform direction.
Less attractive as the default for a next-generation productized developer platform.
Decision

Rejected as the default.

Docusaurus may be supported later as an optional docs backend.

Alternative 3: VitePress
Advantages
Simple.
Fast.
Good developer experience.
Strong for technical docs.
Lightweight compared with some alternatives.
Disadvantages
Vue-based, while the intended product UI ecosystem is more likely to be React/TanStack/Fumadocs-oriented.
Less aligned with the planned app ecosystem.
Less flexible for deeply integrated product docs and future SaaS documentation UX.
Decision

Rejected as the default.

VitePress may be supported later as an optional docs backend.

Alternative 4: Astro/Starlight
Advantages
Excellent docs experience.
Strong content-first architecture.
Good performance.
Good fit for documentation-heavy projects.
Disadvantages
Adds a separate framework direction.
Less directly aligned with the intended React-oriented product UI path.
May be better as an optional docs pack than the default.
Decision

Rejected as the default.

Starlight may be supported later as an optional docs backend.

Alternative 5: MkDocs
Advantages
Excellent for Markdown docs.
Simple.
Strong technical documentation ecosystem.
Good Python ecosystem fit.
Disadvantages
Python-based tooling adds another ecosystem early.
Less aligned with the likely TypeScript/React docs and app surface.
Less ideal for deeply integrated future product UI.
Decision

Rejected as the default.

MkDocs may be supported later as an optional docs backend.

Alternative 6: Custom documentation system

Monad OS could build its own documentation renderer.

Advantages
Maximum control.
Could deeply integrate lifecycle graph, evidence, policies, and AI context.
Could become a unique product feature.
Disadvantages
Major scope increase.
Reinvents solved documentation infrastructure.
Delays useful product work.
Distracts from the core lifecycle graph and control-plane moat.
Decision

Rejected.

Monad OS should not build a custom docs renderer initially.

Alternative 7: Fumadocs
Advantages
Modern documentation framework.
Good fit for React-oriented documentation.
Strong fit for polished product docs.
Good fit for MDX-style documentation.
Suitable for a future docs application under apps/docs/.
Aligns with productized SaaS documentation needs.
Can coexist with canonical Markdown documents under docs/.
Disadvantages
Adds framework/tooling dependency.
Requires generated app setup.
May initially pair most naturally with Next.js even if other app stacks are used elsewhere.
Requires care to keep docs/ canonical rather than burying all content inside an app.
Decision

Accepted.

3. Rationale

Monad OS needs documentation to be treated as product infrastructure.

Fumadocs is a good default because it supports a polished, modern documentation experience while still allowing the repository to preserve canonical docs as Markdown/MDX content.

The important distinction is:

Fumadocs is the documentation frontend. The docs/ directory is the canonical documentation source.

This prevents documentation from becoming trapped inside one app implementation.

The docs strategy should support:

local reading in Git
rendered product docs
AI context generation
docs validation
future docs drift detection
future SaaS documentation sync
future pack/plugin docs
generated references
onboarding tutorials
productized service materials
4. Documentation Architecture

The approved documentation architecture is:

docs/
  00-index.md
  product/
  architecture/
  decisions/
  strategy/
  roadmap/
  governance/
  sdlc/
  glossary/
  reference/
  tutorials/
  runbooks/
  policies/
  evidence/

apps/
  docs/
    # future Fumadocs documentation app
Canonical Docs

Canonical docs live in docs/.

These are source-of-truth repository documents.

Examples:

docs/product/charter.md
docs/product/prd.md
docs/architecture/technical-product-blueprint.md
docs/decisions/0001-build-monad-os-as-sdlc-control-plane.md
docs/governance/principles.md
Rendered Docs App

The future Fumadocs app lives in apps/docs/.

Its responsibilities:

render canonical docs
provide navigation
provide search
provide product-grade docs UX
support future public/private documentation publishing
Monad Docs Commands

Monad OS should eventually support:

monad docs dev
monad docs build
monad docs check
monad docs index
monad docs drift
monad docs publish
5. Docs as SDLC Artifacts

Documentation should become part of the lifecycle graph.

Important documentation node types:

ProductCharter
PRD
ADR
RFC
ArchitectureDoc
DomainModel
CLIReference
ManifestReference
GovernanceDoc
PolicyDoc
Runbook
Tutorial
EvidenceGuide
IntegrationGuide
PackDoc
PluginDoc

Important relationships:

Requirement documented_by PRD
Decision documented_by ADR
Service documented_by ServiceDoc
Policy documented_by PolicyDoc
Command documented_by CLIReference
Release documented_by ReleaseNotes
Incident documented_by Postmortem

This enables future commands such as:

monad docs coverage
monad docs drift
monad docs graph
monad explain docs
6. Docs Validation

Monad OS should validate required documentation.

Initial required docs:

README.md
AGENTS.md
docs/00-index.md
docs/product/charter.md
docs/product/prd.md
docs/product/vision.md
docs/product/positioning.md
docs/architecture/technical-product-blueprint.md
docs/architecture/sdlc-control-plane.md
docs/architecture/toolchain-strategy.md
docs/architecture/agnosticity.md
docs/architecture/competitive-moat.md
docs/sdlc/full-sdlc-coverage.md
docs/governance/principles.md
docs/roadmap/initial-implementation-sequence.md
docs/strategy/next-steps.md

Future docs validation may check:

missing ADR index entries
missing PRD links
broken internal links
stale CLI references
stale manifest schema references
services without docs
commands without docs
policies without explanations
generated docs not committed
docs drift from code/config
7. Interaction With Fumadocs

Fumadocs should not become the only way to read the docs.

Users should be able to read docs directly in GitHub, local editors, or the terminal.

Fumadocs should enhance documentation presentation, navigation, and search.

Possible future behavior:

monad docs init

Generates:

apps/docs/
  app/
  content/
  source.config.ts
  package.json

Possible future behavior:

monad docs sync

Maps:

docs/

into the Fumadocs content system.

Possible future behavior:

monad docs check

Validates:

required documents
navigation coverage
broken links
Fumadocs build readiness
8. Generated Documentation

Monad OS should eventually generate or update documentation for:

CLI reference
manifest schema
project graph
package/app/service catalogs
policy packs
evidence model
plugin model
pack model
toolchain wrappers
command examples
onboarding tutorials

Generated documentation should be clearly marked.

Future file ownership tracking may identify:

user-authored
monad-generated
monad-managed
native-tool-generated
9. AI Context Implications

Documentation is one of the most important inputs for AI-agnostic context generation.

Monad OS should use documentation to generate:

.monad/context/repo-map.md
.monad/context/current-state.md
.monad/context/handoff.md
.monad/context/architecture-summary.md
.monad/context/task-pack.md

Documentation should help AI assistants understand:

product goals
architecture principles
constraints
decisions
roadmap
allowed changes
risky areas
current implementation stage
command usage
governance expectations

This reinforces the rule:

AI should operate from durable repo context, not only from ephemeral chat context.

10. Consequences
Positive Consequences
Documentation is treated as product infrastructure.
The repo has strong onboarding from the beginning.
Future SaaS/productized-service documentation becomes easier.
Fumadocs provides a polished docs frontend.
Canonical docs remain readable as Markdown.
AI context generation has high-quality source material.
Governance and ADRs become easier to navigate.
Future docs drift detection becomes possible.
Negative Consequences
Adds documentation framework complexity.
Requires docs app maintenance.
Requires clear distinction between docs/ and apps/docs/.
Requires docs validation to avoid drift.
May require Next.js or another supported runtime for the docs app.
Mitigations
Keep docs/ canonical.
Introduce apps/docs/ after the planning docs are stable.
Keep early docs readable without Fumadocs.
Add monad docs check.
Add docs ownership and generation rules later.
Treat Fumadocs as the default frontend, not a permanent hard lock-in.
11. Non-Goals

This decision does not mean:

all docs must immediately move into a Fumadocs app
plain Markdown is no longer allowed
the Fumadocs app must be built in v0
other documentation backends can never be supported
Monad OS should build a custom documentation renderer
documentation is only for humans and not for AI/context/policy workflows

This decision establishes Fumadocs as the approved default docs frontend.

12. Success Criteria

This decision is successful if:

The repository maintains canonical docs under docs/.
The future apps/docs/ app can render the docs using Fumadocs.
Documentation supports onboarding, architecture, governance, and product strategy.
Documentation becomes part of the lifecycle graph.
Monad can validate documentation coverage.
Monad can generate AI context from documentation.
Docs remain useful even before the rendered docs app exists.
Fumadocs improves product presentation without trapping source-of-truth content.
13. Final Decision Statement

Monad OS will use Fumadocs as the approved default documentation frontend.

The canonical documentation source will remain in docs/.

The future documentation application will live in apps/docs/.


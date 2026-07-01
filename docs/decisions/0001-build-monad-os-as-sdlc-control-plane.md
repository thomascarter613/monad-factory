# ADR-0001: Build Monad OS as an SDLC Control Plane

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will be designed and built as an **AI-agnostic SDLC control plane and monorepo operating system**, not merely as a monorepo starter, task runner, scaffolding tool, or documentation framework.

The core product model will be a governed, queryable, auditable software lifecycle graph that connects:

BusinessGoal
→ ProductOutcome
→ Initiative
→ Epic
→ Feature
→ Requirement
→ ArchitectureDecision
→ Design
→ WorkItem
→ CodeChange
→ PullRequest
→ Review
→ TestEvidence
→ SecurityEvidence
→ BuildArtifact
→ Provenance
→ Release
→ Deployment
→ RuntimeSignal
→ Incident
→ ProblemRecord
→ Learning
→ Improvement
→ NextRequirement

The local-first CLI will be the initial product surface.

The future SaaS offering should extend the local core through synchronization, hosted graph intelligence, evidence vaults, policy packs, dashboards, integrations, and marketplace capabilities.

---

# 1. Context

Modern software delivery is fragmented across many tools and artifacts.

Common examples:

- source code lives in Git
- issues live in GitHub Issues, Jira, Linear, Plane, or similar systems
- documentation lives in Markdown, docs sites, wikis, or scattered files
- architecture decisions live in ADRs, diagrams, chats, or people's heads
- CI/CD lives in workflow files
- security evidence lives in scanners and reports
- release evidence lives in changelogs, CI logs, package registries, or spreadsheets
- runtime behavior lives in observability platforms
- incidents live in incident management systems
- AI development context lives in editor sessions, chat sessions, and temporary prompts

The result is poor traceability across the lifecycle.

Teams struggle to answer questions like:

- Why does this code exist?
- Which requirement does this change satisfy?
- Which ADR governs this architecture?
- Which services are affected by this dependency change?
- Which tests prove this requirement works?
- Which release introduced this behavior?
- Which deployment caused this incident?
- Which controls have evidence?
- Which AI agent or assistant changed this file?
- Which policy allowed or blocked this change?

Monad OS should address this by making the SDLC explicit, declarative, graph-native, policy-controlled, and evidence-oriented.

---

# 2. Alternatives Considered

## Alternative 1: Build a monorepo starter

Monad OS could have been a sophisticated starter repository that generates a strong initial repo structure.

### Advantages

- Easier to build.
- Easier to explain.
- Faster MVP.
- Lower complexity.

### Disadvantages

- Weak moat.
- Limited long-term value.
- Harder to commercialize as SaaS.
- Easier for competitors to copy.
- Does not solve lifecycle traceability.
- Does not address evidence, governance, operations, or AI safety deeply.

### Decision

Rejected as the primary product identity.

Monad OS may include starter functionality, but it should not be only a starter.

---

## Alternative 2: Build a task runner/build tool

Monad OS could have been a replacement for Nx, Turborepo, moon, Bazel, Buck2, Pants, or similar tools.

### Advantages

- Clear developer-tool category.
- Direct technical control.
- Potentially powerful if successful.

### Disadvantages

- Competes directly with mature tools.
- Requires massive engineering investment.
- Risks reinventing solved problems.
- Reduces ability to compose best-of-breed tools.
- Does not naturally cover the whole SDLC.

### Decision

Rejected.

Monad OS should wrap and coordinate native tools rather than unnecessarily replacing them.

---

## Alternative 3: Build an AI coding assistant

Monad OS could have been an AI coding assistant or agent framework.

### Advantages

- Strong market interest.
- Potentially useful quickly.
- Could integrate with current AI coding workflows.

### Disadvantages

- High model-provider churn.
- Risk of AI-provider lock-in.
- Crowded category.
- Hard to differentiate on model capability alone.
- Does not necessarily solve governance, evidence, or traceability.
- AI-only tools can become unsafe without a deterministic control plane.

### Decision

Rejected as the primary identity.

Monad OS should support AI-assisted development, but AI should operate inside a governed SDLC control plane.

---

## Alternative 4: Build an internal developer platform only

Monad OS could have been an internal developer platform similar in spirit to software catalog and golden path systems.

### Advantages

- Enterprise relevance.
- Strong platform engineering alignment.
- Clear use cases around standards and templates.

### Disadvantages

- May start too far from the solo/local-first use case.
- Can become dashboard-first instead of repo-first.
- Risks requiring SaaS or server infrastructure too early.
- Does not necessarily solve local developer workflow.

### Decision

Partially accepted.

Monad OS should eventually support internal developer platform use cases, but the initial product should be local-first and repo-native.

---

## Alternative 5: Build an SDLC control plane

Monad OS can be a local-first, SaaS-ready SDLC control plane that begins with a monorepo operating system and expands into lifecycle graph, governance, evidence, policy, and AI-safe workflows.

### Advantages

- Strongest long-term product thesis.
- Supports local-first adoption.
- Supports future SaaS commercialization.
- Creates a stronger competitive moat.
- Connects code, docs, decisions, policy, evidence, releases, operations, and AI workflows.
- Allows wrapping best-of-breed tools rather than replacing them.
- Creates a foundation for productized services and enterprise offerings.

### Disadvantages

- More complex.
- Requires careful scope control.
- Needs strong product discipline.
- Risk of becoming too abstract too early.

### Decision

Accepted.

---

# 3. Rationale

The SDLC control plane direction provides the best strategic foundation because it turns Monad OS into a category-defining platform rather than a narrowly scoped repo tool.

The most important product insight is:

> The lifecycle graph is the moat.

Most engineering tools understand only one slice of the software lifecycle.

Monad OS should understand the relationships between slices.

This creates future product value around:

- traceability
- architecture governance
- policy enforcement
- release evidence
- compliance readiness
- AI-safe development
- modernization planning
- maturity assessment
- software delivery intelligence
- productized service workflows
- hosted SaaS analytics

The monorepo is the starting point because it provides a concrete local system of record.

The lifecycle graph is the long-term product.

---

# 4. Consequences

## Positive Consequences

Monad OS can become more than a scaffold.

It can support:

- repo initialization
- toolchain recommendation
- project graphing
- SDLC modeling
- policy checks
- evidence collection
- documentation generation
- AI context generation
- release governance
- modernization planning
- SaaS synchronization
- marketplace packs
- enterprise compliance workflows

This creates a stronger long-term product and business model.

## Negative Consequences

The vision is larger and more complex than a normal developer tool.

The project will need strict phase discipline.

The first implementation must avoid trying to build the entire SDLC control plane immediately.

## Required Mitigation

The project must be implemented in layers:

1. Local core.
2. Repo initialization.
3. Manifest.
4. Documentation foundation.
5. Project graph.
6. Toolchain wrapper.
7. Policy checks.
8. Evidence basics.
9. AI-agnostic context.
10. Packs/plugins.
11. Hosted SaaS.

---

# 5. Implementation Implications

This decision implies that Monad OS must eventually include or support:

## Local Core

- `monad` CLI
- `workspace.toml`
- local graph
- local doctor/check commands
- local documentation generation
- local policy checks
- local evidence generation

## SDLC Model

- product goals
- requirements
- designs
- ADRs
- work items
- code changes
- tests
- builds
- artifacts
- releases
- deployments
- incidents
- improvements

## Governance

- ADRs
- RFCs
- risk registers
- policy packs
- CODEOWNERS
- approval gates
- architecture drift checks

## Evidence

- test evidence
- build evidence
- security evidence
- release evidence
- deployment evidence
- AI action evidence
- compliance control evidence

## AI-Safe Workflows

- AI provider abstraction
- no-AI mode
- local AI mode
- bring-your-own-provider mode
- context packs
- action logs
- human approval gates
- policy-bound agent permissions

## SaaS-Ready Architecture

- local artifact formats should be parseable
- local graph should be syncable
- evidence should be exportable
- policies should be versioned
- packs/plugins should be installable
- hosted control plane should extend local core

---

# 6. Non-Goals Introduced by This Decision

This decision does not mean v0 or v1 will include the full system.

The following remain out of scope for the earliest implementation:

- hosted SaaS dashboard
- multi-tenant backend
- full visual graph UI
- full compliance automation
- full marketplace
- full AI agent runtime
- full enterprise SSO
- full remote execution platform
- full incident management platform

They should be designed for, not built immediately.

---

# 7. Success Criteria

This decision is successful if Monad OS can eventually answer questions such as:

- What exists in this repo?
- Why does it exist?
- Who owns it?
- What depends on it?
- Which requirement does it support?
- Which ADR governs it?
- Which policies protect it?
- Which tests cover it?
- Which releases included it?
- Which deployments run it?
- Which incidents involved it?
- Which evidence proves it is safe?
- Which AI context is needed to work on it?
- What should be modernized next?

Near-term success means the local core establishes enough structure to make these future capabilities possible.

---

# 8. Final Decision Statement

Monad OS will be built as an **AI-agnostic, cloud-agnostic, database-agnostic SDLC control plane and monorepo operating system**.

The initial product will be a local-first CLI and repo foundation.

The long-term product will be a governed lifecycle graph with policy, evidence, documentation, AI-safe workflows, and SaaS-ready synchronization.


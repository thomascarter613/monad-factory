# ADR-0007: Support Nx Under the Monad Wrapper

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will support **Nx as an approved underlying task graph and project graph backend**, especially for JavaScript/TypeScript-heavy repositories.

Nx may be used internally while the user-facing workflow remains centered on the `monad` CLI.

Example user-facing commands:

```bash
monad run web:build
monad run web:test
monad affected test
monad graph
monad inspect
```

These may internally delegate to Nx commands such as:

```bash
nx run web:build
nx affected -t test
nx graph
nx show projects
```

Monad OS will not pretend Nx is absent. Instead, Nx will be documented as a replaceable backend.

The intended relationship is:

```txt
Monad = product/control-plane interface
Nx    = optional task/project graph execution backend
```

Monad owns intent, graph enrichment, SDLC lifecycle modeling, policy, evidence, documentation, recommendations, and user-facing workflow.

Nx provides mature task graph, project graph, affected task execution, caching, and plugin ecosystem capabilities.

---

# 1. Context

Monad OS is intended to become an SDLC control plane and monorepo operating system.

It should not build every underlying capability from scratch.

For JavaScript/TypeScript-heavy monorepos, Nx is a mature and powerful option for:

* project graphing
* task graphing
* affected builds/tests
* caching
* inferred tasks
* generators
* plugin integration
* distributed CI workflows through Nx Cloud/Nx Agents where appropriate

Monad OS can benefit from Nx without becoming merely an Nx wrapper.

The product distinction is important.

Nx is primarily a monorepo build/task/project graph tool.

Monad OS is intended to be an SDLC control plane that includes:

* requirements
* decisions
* architecture
* governance
* documentation
* policy
* evidence
* AI-safe context
* release traceability
* future SaaS synchronization

Nx can power a subset of Monad's execution layer.

---

# 2. Alternatives Considered

## Alternative 1: Do not use Nx

Monad OS could avoid Nx entirely and build all project graph and task graph functionality itself.

### Advantages

* Full control.
* No dependency on Nx.
* Less risk of leaky abstraction.
* Easier to claim a completely independent graph implementation.

### Disadvantages

* Slower implementation.
* Reinvents mature functionality.
* Weakens early TypeScript/JavaScript monorepo support.
* Delays affected task execution.
* Delays practical developer value.
* Requires building plugin/tooling integrations from scratch.

### Decision

Rejected.

Monad OS should leverage mature tools where they are strong.

---

## Alternative 2: Make Nx the public product interface

Monad OS could require developers to use Nx directly.

### Advantages

* Less wrapper work.
* Simpler documentation for Nx-specific workflows.
* Full access to Nx ecosystem and conventions.
* Easier integration with existing Nx workspaces.

### Disadvantages

* Monad becomes less distinct.
* User experience becomes Nx-centered, not Monad-centered.
* Harder to support other backends later.
* Harder to preserve AI/cloud/database/toolchain agnosticism.
* Harder to present Monad OS as a broader SDLC control plane.
* Harder to support Buck2, Pants, moon, Dagger, or other backends as peers.

### Decision

Rejected.

Nx should be available under the hood, but Monad should remain the public interface.

---

## Alternative 3: Use Nx as a hidden implementation detail

Monad OS could completely hide Nx from users and avoid documenting it.

### Advantages

* Cleaner illusion of one unified tool.
* Simpler surface-level messaging.
* Users only need to learn Monad commands.

### Disadvantages

* Dishonest or confusing when Nx files/errors appear.
* Harder to troubleshoot.
* Harder to maintain trust.
* Native Nx concepts may leak anyway.
* Developers may need direct Nx access for advanced debugging.
* Generated configuration would be difficult to explain.

### Decision

Rejected.

Monad should abstract Nx, not dishonestly hide it.

---

## Alternative 4: Use Nx as a documented, replaceable backend under Monad

Monad OS can support Nx as an implementation backend while preserving the Monad public interface.

### Advantages

* Uses mature Nx functionality.
* Keeps Monad user experience consistent.
* Preserves future backend optionality.
* Supports TypeScript-heavy monorepos well.
* Allows Monad to focus on higher-level SDLC value.
* Enables progressive migration to or from Nx.
* Supports backend replacement later.

### Disadvantages

* Requires wrapper design.
* Requires mapping Nx concepts into Monad concepts.
* Native Nx errors may leak through.
* Some Nx configuration must be generated/maintained.
* Backend abstraction must avoid becoming too generic too early.

### Decision

Accepted.

---

# 3. Rationale

Nx is a strong default backend for early Monad OS JavaScript/TypeScript workflows because it already solves many monorepo execution problems.

However, Monad OS must not become Nx-only.

The guiding principle is:

> Monad wraps Nx as an execution backend while preserving Monad as the product control plane.

Nx can provide:

* project graph
* task graph
* affected task calculation
* caching
* inferred tasks
* plugin support
* generator support

Monad adds:

* workspace intent
* SDLC lifecycle graph
* requirements/ADR/risk/evidence relationships
* policy model
* evidence model
* documentation structure
* AI-agnostic context
* recommendation engine
* provider-agnostic architecture
* SaaS-ready synchronization

This creates a layered design.

---

# 4. Conceptual Model

The relationship should be:

```txt
workspace.toml
  ↓
Monad workspace model
  ↓
Monad graph enrichment
  ↓
Backend adapter
  ↓
Nx project/task graph
  ↓
Native task execution
```

Monad may read from:

```txt
workspace.toml
package.json
nx.json
project.json
tsconfig.json
docs/
apps/
packages/
services/
```

Monad may generate or validate:

```txt
nx.json
project.json
package.json scripts
.github/workflows/*
.monad/graph.json
.monad/recommendation.json
docs/tooling/nx.md
```

Monad should combine Nx graph data with SDLC metadata that Nx does not natively own.

---

# 5. User Experience

Users should primarily run:

```bash
monad run web:build
monad run web:test
monad affected test
monad graph
monad inspect web
```

Monad may show the native backend when useful:

```txt
Running task through Nx backend:

  nx run web:build
```

If a task fails, Monad should add explanation:

```txt
Task failed: web:build

Backend:
  Nx

Native command:
  nx run web:build

Suggested next steps:
  monad run web:typecheck
  monad inspect web
  monad explain task web:build
```

Users should also be allowed to run Nx directly when needed:

```bash
nx graph
nx show projects
nx run web:build
```

Monad docs should explain when direct Nx usage is safe.

---

# 6. Initial Nx Scope

## v0

No full Nx integration is required.

v0 may simply record that Nx is the selected/recommended backend.

## v0.1

Monad should generate a basic Nx-compatible configuration for JS/TS monorepos.

Potential generated files:

```txt
nx.json
package.json
apps/docs/
apps/web/
packages/*
```

Potential commands:

```bash
monad run <project>:<target>
monad graph
```

## v0.2

Monad should support:

```bash
monad affected test
monad affected build
monad inspect <project>
```

## v1

Monad should support stable Nx-backed workflows:

```bash
monad run <project>:<target>
monad affected <target>
monad graph --json
monad explain task <project>:<target>
monad doctor
```

---

# 7. Backend Adapter Requirements

The Nx backend adapter should eventually support:

```txt
detect()
generate_config()
validate_config()
list_projects()
list_targets(project)
run_target(project, target)
run_affected(target)
get_project_graph()
get_task_graph()
explain_task(project, target)
collect_evidence(command_result)
```

The adapter should not expose raw Nx concepts directly unless necessary.

Monad concepts should remain primary:

```txt
Project
Task
Target
Dependency
AffectedSet
ExecutionResult
Evidence
```

---

# 8. File Ownership

Monad should classify Nx-related files.

## Native Nx Files

```txt
nx.json
project.json
```

## Shared/Native Files

```txt
package.json
tsconfig.json
```

## Monad-Owned Files

```txt
workspace.toml
.monad/recommendation.json
.monad/graph.json
docs/tooling/nx.md
```

Future file ownership tracking should clarify whether a file is:

```txt
user-owned
native-tool-owned
monad-generated
monad-managed
shared
```

---

# 9. Documentation Requirements

Monad OS should eventually create:

```txt
docs/tooling/nx.md
```

This document should explain:

1. Why Nx is used.
2. What Monad uses Nx for.
3. Which files belong to Nx.
4. Which commands Monad wraps.
5. How to run Nx directly.
6. How to troubleshoot Nx errors.
7. How Nx relates to Monad's lifecycle graph.
8. How to replace Nx with another backend later.

---

# 10. Relationship to Other Backends

This decision does not exclude other backends.

Monad OS should still support or plan for:

```txt
moon
Turborepo
Buck2
Pants
Dagger
Nix
Gradle/Develocity
native language tools
```

Recommended positioning:

```txt
Nx:
  Best initial JS/TS project/task graph backend.

moon:
  Optional polyglot task runner.

Buck2:
  Maximum-scale enterprise build backend.

Pants:
  Enterprise backend-heavy/Python-heavy build backend.

Dagger:
  Portable CI execution backend.

Nix:
  Strict reproducibility and environment backend.
```

Monad should be able to recommend different backends depending on repository needs.

---

# 11. Interaction With the Lifecycle Graph

Nx's project graph is not the full Monad lifecycle graph.

Nx graph can answer:

```txt
Which projects depend on which other projects?
Which tasks are affected by a change?
Which build/test targets exist?
```

Monad lifecycle graph should eventually answer:

```txt
Which requirement caused this project to exist?
Which ADR governs this package?
Which risk applies to this service?
Which evidence proves this release?
Which policy protects this path?
Which AI context is relevant to this task?
Which deployment runs this service?
```

Therefore:

> Nx graph is an input to Monad graph, not the whole Monad graph.

---

# 12. Risks

## Risk: Monad becomes too Nx-specific

Mitigation:

* Keep adapter boundaries.
* Keep Monad command names backend-neutral.
* Avoid exposing Nx-only assumptions in `workspace.toml`.
* Document Nx as replaceable.
* Support at least one alternate backend later.

## Risk: Nx errors confuse users

Mitigation:

* Translate errors where possible.
* Show native command.
* Provide troubleshooting docs.
* Preserve raw output for debugging.

## Risk: Wrapper abstraction leaks

Mitigation:

* Be honest about Nx usage.
* Avoid claiming Nx is invisible.
* Provide `monad explain backend nx`.

## Risk: Support matrix grows too quickly

Mitigation:

* Start with Nx for JS/TS.
* Delay broad backend support.
* Add backends based on use cases.

---

# 13. Non-Goals

This decision does not mean:

* Nx is required for every Monad repository.
* Monad is only for Nx workspaces.
* Monad will hide Nx completely.
* Monad will replace all Nx functionality.
* Nx will be the maximum-scale enterprise build backend.
* Nx will be the only project graph input forever.
* Monad cannot later support moon, Buck2, Pants, or another backend.

This decision only establishes Nx as an approved and recommended initial backend for JS/TS-heavy task/project graph workflows.

---

# 14. Success Criteria

This decision is successful if:

1. Monad can initialize a JS/TS-heavy repo with Nx under the hood.
2. Users can run common tasks through `monad`.
3. Nx configuration is understandable and documented.
4. Direct Nx usage remains possible.
5. Monad can enrich Nx graph data with SDLC metadata.
6. Monad can later support other backends without redesign.
7. Monad remains a control plane, not merely an Nx wrapper.

---

# 15. Final Decision Statement

Monad OS will support Nx as an approved underlying backend for JavaScript/TypeScript project graph, task graph, affected execution, and caching workflows.

Nx will be wrapped by Monad, documented honestly, and treated as replaceable.

Monad remains the user-facing SDLC control plane.


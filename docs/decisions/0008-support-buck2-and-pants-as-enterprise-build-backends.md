# ADR-0008: Support Buck2 and Pants as Enterprise Build Backends

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will support **Buck2** and **Pants** as approved future enterprise build backends.

They will not be required for the initial local core.

They will be treated as optional backend adapters for repositories that need stronger enterprise-scale build capabilities than the default local development stack.

The intended positioning is:

```txt
Nx:
  Default early JS/TS task and project graph backend.

moon:
  Optional polyglot task runner.

Dagger:
  Portable CI execution backend.

Nix:
  Optional strict reproducibility and environment backend.

Buck2:
  Maximum-scale enterprise build backend.

Pants:
  Enterprise backend-heavy and Python-heavy build backend.
```

Monad OS will not hard-code one enterprise build system.

Instead, it will expose backend-neutral user commands such as:

```bash
monad build
monad build affected
monad test affected
monad graph
monad explain task
monad evidence collect
```

Internally, these may delegate to Nx, moon, Buck2, Pants, Dagger, native language tools, or future backends depending on workspace configuration.

---

# 1. Context

Monad OS is intended to serve a wide range of users.

Early users may need:

* fast local repo initialization
* Fumadocs documentation
* Bun/Biome/Nx workflows
* simple project graphing
* local-first validation
* interactive recommendations

Future enterprise users may need:

* stronger hermeticity
* larger monorepo scale
* remote execution
* remote caching
* language-aware builds
* reproducible build actions
* enterprise CI performance
* strict dependency declarations
* backend-heavy service builds
* Python-heavy workflows
* polyglot build coordination

Monad OS should be able to grow into these requirements without redesign.

Bazel is a common reference point for maximum-scale hermetic builds and remote execution, but Monad OS should not require Bazel as the only enterprise path.

Buck2 and Pants are approved non-Bazel enterprise backend options.

---

# 2. Alternatives Considered

## Alternative 1: Use Bazel as the only enterprise build backend

### Advantages

* Mature large-scale build system.
* Strong remote execution ecosystem.
* Strong hermetic build model.
* Widely recognized in enterprise-scale build discussions.

### Disadvantages

* Steep learning curve.
* Complex migration path.
* Can be heavy for many teams.
* May conflict with the desire for non-Bazel alternatives.
* Hard-coding Bazel would weaken Monad's toolchain-composable strategy.

### Decision

Rejected as the only enterprise option.

Bazel-compatible concepts may inform the architecture, and Bazel could potentially be supported later, but it will not be the required enterprise backend.

---

## Alternative 2: Use Nx for all build scales

### Advantages

* Excellent JS/TS monorepo experience.
* Strong project graph.
* Strong affected task workflows.
* Strong ecosystem for frontend/backend TypeScript repos.
* Good fit for early Monad OS adoption.

### Disadvantages

* Not the best fit for strict compiler-level hermeticity.
* Not the best fit for all polyglot enterprise build scenarios.
* Does not fully replace large-scale remote execution build systems.
* Weaker fit for some backend-heavy, Python-heavy, or massive polyglot repos.

### Decision

Rejected for maximum enterprise build scenarios.

Nx remains an approved default JS/TS task/project graph backend.

---

## Alternative 3: Build a custom Monad enterprise build system

Monad OS could build its own hermetic build system, remote execution engine, cache protocol, and language rules.

### Advantages

* Maximum control.
* Potentially deep integration with the lifecycle graph.
* Could become a unique technical moat if successful.

### Disadvantages

* Massive scope.
* Very high engineering burden.
* Competes with mature build systems.
* Delays product value.
* Distracts from Monad's real moat: SDLC graph, policy, evidence, and AI-safe workflows.

### Decision

Rejected.

Monad OS should not build a custom enterprise build system initially.

---

## Alternative 4: Support Buck2 and Pants as optional enterprise backends

### Advantages

* Provides serious non-Bazel enterprise paths.
* Preserves backend optionality.
* Supports different enterprise profiles.
* Avoids forcing every repo into one build model.
* Lets Monad recommend based on actual needs.
* Keeps Monad focused on control-plane value.

### Disadvantages

* Requires adapter design.
* Requires more documentation.
* Requires compatibility testing.
* Increases future support matrix.
* Users may need expertise in the selected backend.

### Decision

Accepted.

---

# 3. Rationale

Monad OS should be future-proof for enterprise use without forcing enterprise complexity into v0 or v1.

The right architecture is:

> Simple defaults now, serious enterprise backends later.

Buck2 and Pants provide two strong optional directions:

```txt
Buck2:
  Best fit for maximum-scale, polyglot, remote-execution-oriented enterprise builds.

Pants:
  Best fit for ergonomic enterprise builds, especially backend-heavy and Python-heavy monorepos.
```

Monad OS should expose a consistent control-plane interface while allowing the backend to vary.

The key principle remains:

> Monad owns intent, graph, policy, evidence, and workflow. Build backends execute.

---

# 4. Backend Positioning

## Buck2

Buck2 should be positioned as the maximum-scale enterprise backend.

Use Buck2 when the repository needs:

* very large-scale build orchestration
* strict build graph discipline
* remote execution
* remote caching
* polyglot builds
* high-performance build execution
* explicit build targets
* enterprise-scale build optimization

Buck2 should not be the default for small repos.

## Pants

Pants should be positioned as the ergonomic enterprise backend.

Use Pants when the repository needs:

* backend-heavy monorepo support
* Python-heavy workflows
* polyglot backend builds
* dependency inference
* hermetic process execution
* remote caching/execution
* lower-friction enterprise build adoption than heavier alternatives

Pants should be especially considered for Python, JVM, Go, and backend-service-oriented repositories.

---

# 5. Initial Build Backend Matrix

Monad OS should eventually support a recommendation matrix.

```txt
Small JS/TS app repo:
  Default: Nx
  Alternative: Turborepo

Medium JS/TS monorepo:
  Default: Nx
  Optional: moon

Polyglot local-first repo:
  Default: moon or Monad-native graph with native tools
  Optional: Nx for JS/TS subset

Backend-heavy Python repo:
  Default: Pants

Maximum-scale enterprise polyglot repo:
  Default: Buck2

Portable CI-heavy repo:
  Default: Dagger plus selected task/build backend

Strict reproducibility requirement:
  Add Nix layer

JVM-heavy enterprise repo:
  Consider Gradle/Develocity pack
```

This matrix should be refined by the interactive recommendation engine.

---

# 6. Monad Command Abstraction

User-facing commands should remain backend-neutral.

Examples:

```bash
monad build
monad build affected
monad test affected
monad run api:build
monad graph
monad explain task api:build
monad evidence collect
```

Possible internal translations:

```txt
Nx:
  nx run api:build
  nx affected -t test

Pants:
  pants package ::
  pants test ::

Buck2:
  buck2 build //...
  buck2 test //...

Dagger:
  dagger call build
```

Monad should expose the native command when useful for transparency.

---

# 7. Adapter Requirements

Future enterprise build adapters should support a common conceptual interface.

```txt
BuildBackendAdapter
  id
  name
  detect()
  generate_config()
  validate_config()
  list_targets()
  build(targets)
  test(targets)
  affected(base, head)
  graph()
  explain(target)
  collect_evidence(result)
```

Backend-specific behavior should be isolated.

Monad should normalize outputs into common concepts:

```txt
Project
Target
Task
BuildAction
Artifact
Dependency
AffectedSet
ExecutionResult
Evidence
```

---

# 8. Evidence Requirements

Enterprise build backends should produce or support evidence collection.

Possible evidence:

```txt
build command
backend used
targets built
inputs
outputs
cache status
remote execution status
test results
artifact paths
logs
SBOM references
provenance references
timestamp
commit SHA
```

Future evidence file:

```txt
evidence/builds/<timestamp>-<backend>.json
```

Example normalized evidence:

```json
{
  "evidence_type": "build",
  "backend": "buck2",
  "targets": ["//services/api:api"],
  "status": "passed",
  "commit": "abc123",
  "timestamp": "2026-06-29T00:00:00Z"
}
```

---

# 9. Manifest Implications

`workspace.toml` should eventually support build backend strategy.

Example:

```toml
[build]
strategy = "recommended"
default_backend = "nx"

[build.backends.nx]
enabled = true
scope = ["apps/*", "packages/*"]

[build.backends.pants]
enabled = false
scope = ["services/*"]

[build.backends.buck2]
enabled = false
scope = ["//..."]

[build.enterprise]
maximum_scale_backend = "buck2"
backend_heavy_backend = "pants"
```

The v0 manifest does not need full backend configuration.

It should only preserve the decision direction.

---

# 10. Recommendation Engine Implications

The interactive recommendation engine should ask about:

```txt
repo size
expected project count
primary languages
backend/frontend split
hermeticity requirements
remote execution requirements
CI budget
enterprise requirements
developer familiarity
migration constraints
speed versus simplicity
local-first requirements
```

It should recommend:

```txt
default backend
optional backend
enterprise migration path
reasoning
trade-offs
risk notes
future upgrade point
```

Example recommendation:

```txt
Recommended build strategy:
  Nx under Monad wrapper for v1.

Reason:
  Your repository is expected to be TypeScript-heavy and does not yet require
  strict remote execution or large-scale hermetic builds.

Future enterprise path:
  If the repo grows beyond 100+ projects or requires remote execution,
  evaluate Buck2 or Pants depending on language mix.
```

---

# 11. Relationship to Nix and Dagger

Buck2 and Pants do not replace all other infrastructure.

## Nix

Nix remains useful for:

* reproducible environments
* toolchain pinning
* remote builders/caches
* local/CI parity
* stricter reproducibility mode

## Dagger

Dagger remains useful for:

* portable CI pipelines
* local/CI executable pipelines
* containerized workflow execution
* CI provider abstraction

The future stack may combine them:

```txt
Nix:
  environment reproducibility

Buck2/Pants:
  build/test backend

Dagger:
  CI execution workflow

Monad:
  control plane, graph, policy, evidence, recommendation, user interface
```

---

# 12. Relationship to Nx

Nx remains the approved initial JS/TS task backend.

Buck2 and Pants are not replacements for Nx in early JS/TS-first adoption unless the repo's scale justifies them.

Recommended progression:

```txt
v0/v1:
  Nx under Monad wrapper.

v1.5:
  Optional Pants backend for backend-heavy repos.

v2+:
  Optional Buck2 backend for maximum-scale enterprise repos.
```

Monad should support migration paths rather than forcing early complexity.

---

# 13. Non-Goals

This decision does not mean:

* Buck2 must be implemented in v0
* Pants must be implemented in v0
* Buck2 or Pants must be implemented in v1
* every repo must use Buck2 or Pants
* Nx is deprecated
* Bazel can never be supported
* Monad will build its own remote execution system
* enterprise backends should be forced on small repos

This decision only reserves Buck2 and Pants as approved future enterprise backend paths.

---

# 14. Risks

## Risk: Enterprise backend complexity leaks into simple projects

Mitigation:

* Keep Buck2/Pants optional.
* Use recommendation profiles.
* Do not scaffold enterprise backends unless selected.
* Keep v0/v1 simple.

## Risk: Supporting too many backends becomes unmanageable

Mitigation:

* Define adapter contracts.
* Add backends incrementally.
* Keep default profiles narrow.
* Build compatibility tests.
* Clearly document support levels.

## Risk: Users expect full enterprise backend support too early

Mitigation:

* Document roadmap clearly.
* Mark Buck2/Pants as future enterprise adapters.
* Avoid promising v0/v1 full support.

## Risk: Backend abstraction becomes too generic

Mitigation:

* Start from real use cases.
* Normalize only what Monad needs.
* Allow backend-specific escape hatches.

---

# 15. Success Criteria

This decision is successful if:

1. Monad OS can start simple without blocking enterprise scale later.
2. Buck2 is available as the future maximum-scale backend path.
3. Pants is available as the future backend-heavy/Python-heavy enterprise backend path.
4. The user-facing Monad command model remains backend-neutral.
5. Nx remains useful for early JS/TS workflows.
6. Enterprise backend support can be added without redesigning the product.
7. Build evidence can eventually be normalized across backends.
8. The recommendation engine can explain when to use each backend.

---

# 16. Final Decision Statement

Monad OS will support Buck2 and Pants as approved future enterprise build backends.

Buck2 is the preferred maximum-scale enterprise build path.

Pants is the preferred ergonomic backend-heavy and Python-heavy enterprise build path.

Both remain optional backends under the Monad control plane.


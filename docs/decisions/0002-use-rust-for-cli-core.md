# ADR-0002: Use Rust for the CLI Core

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will use **Rust** as the implementation language for the core local CLI and control-plane kernel.

The primary binary will be exposed as:

```bash
monad
```

The Rust implementation should own the local core responsibilities:

* CLI command routing
* workspace manifest parsing
* recommendation engine
* repository inspection
* project graph construction
* validation and doctor checks
* generator orchestration
* policy check orchestration
* evidence file generation
* tool backend wrapping
* AI-agnostic context generation
* future plugin/pack loading boundaries

Monad OS itself will remain polyglot.

Rust is the core implementation language for the CLI/control plane, not a restriction on generated repositories.

Generated apps, services, packages, templates, and integrations may use TypeScript, JavaScript, Python, Go, Rust, Java, Kotlin, PHP, SQL, Terraform, Pulumi, Helm, Docker, or other appropriate technologies.

---

# 1. Context

Monad OS needs a local-first CLI that can eventually become the trusted entry point for a governed SDLC control plane.

The CLI must be:

* fast
* portable
* reliable
* easy to distribute
* suitable for local-first usage
* capable of parsing structured files
* capable of invoking native tools
* capable of producing machine-readable outputs
* suitable for future extension
* suitable for long-term productization

The CLI will coordinate many underlying tools, including but not limited to:

* Nx
* moon
* Turborepo
* Buck2
* Pants
* Dagger
* Nix
* Bun
* Biome
* Fumadocs
* GitHub Actions
* Renovate
* Trivy
* Gitleaks
* Syft
* Cosign
* OpenTelemetry tooling

The CLI should be stable even if the wrapped tools change.

---

# 2. Alternatives Considered

## Alternative 1: TypeScript/Node.js

### Advantages

* Very fast to build.
* Strong ecosystem.
* Natural fit for JavaScript/TypeScript monorepos.
* Easy integration with Nx, Bun, Fumadocs, and web tooling.
* Easier for many developers to contribute.

### Disadvantages

* Distribution can be more complex.
* Runtime dependency management can become messy.
* Harder to guarantee a single native binary experience.
* Less ideal for a long-lived systems/control-plane tool.
* Startup performance and dependency footprint may become concerns.
* The tool may appear too coupled to the JavaScript ecosystem.

### Decision

Rejected for the core CLI.

TypeScript remains highly appropriate for generated apps, packages, SDKs, web UI, docs tooling, and future SaaS components.

---

## Alternative 2: Go

### Advantages

* Excellent CLI language.
* Simple cross-compilation.
* Strong standard library.
* Good performance.
* Easy deployment.
* Common in cloud/platform tooling.

### Disadvantages

* Less expressive type system than Rust for some internal modeling.
* Weaker fit for certain future local analysis and safety-oriented abstractions.
* Less alignment with the desired “systems-grade local control plane” identity.

### Decision

Rejected for the core CLI, though Go remains a strong option for future services, integration sync workers, graph services, and SaaS backend components.

---

## Alternative 3: Python

### Advantages

* Very fast prototyping.
* Strong AI/data ecosystem.
* Easy scripting.
* Good for recommendation logic and experiments.

### Disadvantages

* Packaging/distribution can be painful.
* Runtime dependency management is not ideal for a universal local CLI.
* Startup and environment consistency may be weaker.
* Less suitable as the trusted kernel of a local-first control plane.

### Decision

Rejected for the core CLI.

Python remains appropriate for AI/RAG/data-oriented services, analyzers, prototypes, and integrations.

---

## Alternative 4: Shell scripts

### Advantages

* Simple.
* Transparent.
* Easy for bootstrapping.
* No compile step.

### Disadvantages

* Poor long-term maintainability.
* Weak cross-platform behavior.
* Harder testing.
* Harder structured data handling.
* Not suitable for a serious product-grade control plane.

### Decision

Rejected.

Shell scripts may be used for simple repo scripts and generated helper commands, but not as the core product implementation.

---

## Alternative 5: Rust

### Advantages

* Produces fast native binaries.
* Strong type system.
* Excellent reliability characteristics.
* Good cross-platform CLI story.
* Strong ecosystem for command-line tools.
* Good fit for parsing, validation, graph modeling, and file operations.
* Strong long-term foundation for a trusted local control-plane kernel.
* Suitable for productized distribution.
* Helps position Monad OS as a serious systems-grade developer tool.

### Disadvantages

* Slower initial development than TypeScript or Python.
* Higher learning curve.
* More boilerplate.
* Some plugin and scripting workflows may require additional design.
* Not as directly integrated into JS/TS tooling as TypeScript.

### Decision

Accepted.

---

# 3. Rationale

Rust is the best fit for the Monad OS local core because the CLI is intended to become the durable control-plane kernel of the product.

Monad OS should feel like serious infrastructure.

The CLI should be stable, fast, reliable, portable, and capable of coordinating many tools without becoming dependent on one runtime ecosystem.

Rust supports that direction.

The decision also reinforces an important product boundary:

> Monad OS is not a JavaScript-only monorepo tool.

Even though Nx, Bun, Fumadocs, and TypeScript may be important early defaults, Monad OS should remain polyglot and enterprise-capable.

Rust helps preserve that identity.

---

# 4. Consequences

## Positive Consequences

* Monad can be distributed as a native binary.
* The CLI can remain independent from Node.js runtime assumptions.
* The local core can become stable and product-grade.
* Manifest parsing, graph building, and validation can be strongly typed.
* The project can support polyglot ecosystems without appearing JS-only.
* Future SaaS sync agents or local daemons can reuse Rust core libraries.

## Negative Consequences

* Initial development may be slower.
* Contributors may need Rust knowledge.
* Some scaffolding tasks may be easier in TypeScript.
* Plugin design will require care.
* Template logic may need a scripting or declarative layer.

## Mitigations

* Keep generated templates language-agnostic.
* Allow packs/templates to include TypeScript, shell, Python, or other files.
* Use Rust for orchestration, not for every generated artifact.
* Use clear crate boundaries.
* Keep command behavior documented.
* Add integration tests around generated repos.
* Consider a future plugin system that allows non-Rust extensions.

---

# 5. Implementation Implications

The repository should eventually include a Rust workspace.

Likely structure:

```txt
crates/
  monad-cli/
  monad-core/
  monad-config/
  monad-graph/
  monad-doctor/
  monad-generate/
  monad-policy/
  monad-evidence/
  monad-ai-context/
```

Initial minimal structure may be:

```txt
crates/
  monad-cli/
  monad-core/
```

Recommended responsibilities:

## `monad-cli`

* command-line interface
* argument parsing
* help text
* output formatting
* command dispatch

## `monad-core`

* workspace model
* manifest parsing
* shared domain types
* repo inspection
* common errors
* filesystem utilities

Future crates may be split out as complexity grows.

---

# 6. CLI Design Requirements

The CLI should support:

```bash
monad --help
monad version
monad init
monad init --interactive
monad doctor
monad inspect
monad recommend
monad graph
monad docs
```

Future commands should support:

```bash
monad add app
monad add package
monad add service
monad run
monad affected
monad policy check
monad evidence collect
monad ai context
```

The CLI should eventually support:

* human-readable output by default
* `--json` output for automation
* useful exit codes
* clear error messages
* explainable recommendations
* dry-run mode for generators
* non-interactive mode for CI or scripting

---

# 7. Non-Goals

This decision does not mean:

* all generated software must be written in Rust
* all plugins must be Rust forever
* all SaaS backend services must be Rust
* TypeScript is disallowed
* Python is disallowed
* Go is disallowed
* Java/Kotlin is disallowed

This decision only establishes Rust as the preferred language for the local CLI core and control-plane kernel.

---

# 8. Success Criteria

This decision is successful if:

1. Monad OS can be installed and run as a reliable local CLI.
2. The CLI can parse `workspace.toml`.
3. The CLI can generate and validate repo foundations.
4. The CLI can wrap underlying tools without becoming tightly coupled to them.
5. The CLI can support polyglot generated repositories.
6. The CLI can evolve toward project graph, policy, evidence, and AI-context functionality.
7. The Rust core remains modular enough to avoid becoming a monolith.

---

# 9. Final Decision Statement

Monad OS will use **Rust** for the local CLI core and control-plane kernel.

The product remains polyglot, toolchain-composable, AI-agnostic, cloud-agnostic, and database-agnostic.

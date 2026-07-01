# ADR-0004: Wrap Native Tools Instead of Replacing Them

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will **wrap, coordinate, validate, and explain native tools** instead of attempting to replace every tool in the software delivery lifecycle.

Monad OS will own:

- product intent
- workspace manifest
- lifecycle graph
- project graph
- recommendation logic
- policy model
- evidence model
- documentation model
- AI context model
- command interface
- workflow orchestration
- generated rationale
- SaaS-ready synchronization model

Underlying tools will provide specialized execution capabilities.

Examples of tools Monad OS may wrap include:

- Nx
- moon
- Turborepo
- Buck2
- Pants
- Dagger
- Nix
- mise
- proto
- Bun
- pnpm
- Biome
- Lefthook
- Knip
- Syncpack
- Fumadocs
- Renovate
- Gitleaks
- Trivy
- Syft
- Grype
- Cosign
- OpenTelemetry tooling
- Terraform
- Pulumi
- Helm
- Docker
- GitHub Actions
- GitLab CI
- Buildkite
- other future adapters

The user-facing interface should remain:

```bash
monad ...

Native tool usage may remain visible in generated configuration and documentation, but the primary developer workflow should be mediated by Monad.

1. Context

Monad OS aims to become an SDLC control plane and monorepo operating system.

That requires coordinating many concerns:

repository initialization
package management
task execution
build orchestration
documentation
testing
policy checks
security scanning
dependency management
evidence generation
release workflows
deployment workflows
observability integration
AI context generation
future SaaS synchronization

Many mature tools already exist for these concerns.

Replacing all of them would create unnecessary scope, risk, and implementation burden.

Monad OS should instead provide a higher-level control plane that composes best-of-breed tools.

2. Alternatives Considered
Alternative 1: Replace all major tools with custom Monad implementations

Monad OS could build its own package manager, task runner, build engine, documentation renderer, policy engine, CI system, security scanner, and deployment engine.

Advantages
Maximum control.
Consistent internal architecture.
Fewer external abstractions.
Potentially simpler user-facing mental model if fully successful.
Disadvantages
Massive implementation scope.
Years of work before practical value.
High risk of inferior reimplementations.
Difficult to keep up with established ecosystems.
Weakens time-to-market.
Distracts from the actual product moat.
Requires competing with many mature tools simultaneously.
Decision

Rejected.

Monad OS should not attempt to replace mature tools unnecessarily.

Alternative 2: Hard-code one best toolchain

Monad OS could select one stack and tightly integrate it.

Example:

Bun
Nx
Fumadocs
GitHub Actions
PostgreSQL
Cloudflare
OpenAI
Docker
Kubernetes
Advantages
Simpler implementation.
Faster early scaffolding.
Easier documentation.
Fewer combinations to support.
Stronger opinionated default experience.
Disadvantages
Vendor/tool lock-in.
Poor fit for enterprise variety.
Weak cloud/database/AI agnosticism.
Harder to support different repo types.
Harder to sell as a broad SDLC platform.
Harder to evolve as technology changes.
Decision

Rejected as the architectural foundation.

Monad OS may recommend strong defaults, but must not permanently hard-code one stack.

Alternative 3: Be only a thin wrapper around one tool

Monad OS could become a nicer CLI facade over Nx, moon, Turborepo, Bazel, Buck2, Pants, or another backend.

Advantages
Easier to implement.
Can leverage a mature backend.
Faster initial value.
Smaller surface area.
Disadvantages
Weak differentiation.
Product becomes dependent on one backend.
Does not support the full SDLC vision.
Harder to justify as a SaaS/productized service.
Limited lifecycle graph and evidence value.
Harder to remain AI/cloud/database agnostic.
Decision

Rejected.

Monad OS may wrap Nx or other tools, but should not be merely a facade over one tool.

Alternative 4: Wrap native tools through a stable Monad control plane

Monad OS can provide a stable control plane that wraps native tools behind a higher-level model.

Advantages
Best balance of ambition and practicality.
Allows fast adoption of mature tools.
Keeps Monad focused on its real moat.
Supports multiple ecosystems.
Enables backend swapping.
Supports local-first and SaaS-ready architecture.
Enables strong defaults without hard lock-in.
Makes the CLI more durable over time.
Disadvantages
Requires adapter design.
Requires careful documentation of what is canonical.
Native tool errors may leak through.
Supporting many backends can increase complexity.
Some abstractions may become leaky.
Decision

Accepted.

3. Rationale

Monad OS should win by owning the connective tissue of the software lifecycle, not by rebuilding every tool.

The product moat is:

governed lifecycle graph + policy + evidence + recommendations + AI-safe context + SaaS-ready synchronization

The product moat is not:

another task runner

or:

another build tool

or:

another docs renderer

or:

another package manager

Therefore, Monad should treat specialized tools as replaceable execution backends.

The local developer experience should be unified through the monad CLI.

The internal implementation should be adapter-based.

4. Architectural Principle

The controlling principle is:

Monad owns intent. Native tools execute.

This means:

workspace.toml         = declared intent
.monad/                = Monad state, graph, recommendations, evidence, context
native tool configs    = execution details
monad CLI              = user-facing workflow
native tools           = specialized backends

Examples:

monad run web:build

May call:

nx run web:build

Or, in another repo:

moon run web:build

Or, in a maximum-scale enterprise repo:

buck2 build //apps/web:build

But the user-facing workflow remains:

monad run web:build
5. Tool Categories

Monad OS should eventually support adapters for multiple categories.

Package Managers

Potential tools:

Bun
pnpm
npm
Yarn
Cargo
Go modules
uv
Poetry
Maven
Gradle
Composer

Monad responsibility:

recommend package manager
validate lockfiles
check dependency consistency
coordinate dependency updates
generate docs/rationale
integrate evidence
Task and Project Graph Backends

Potential tools:

Nx
moon
Turborepo
Lage
custom Monad graph
future adapters

Monad responsibility:

expose unified commands
inspect projects
compute affected operations
combine task graph with SDLC graph
explain task dependencies
produce graph outputs
Enterprise Build Backends

Potential tools:

Buck2
Pants
Bazel-compatible ecosystems where appropriate
Please
Gradle/Develocity
Nix
Earthly
Dagger

Monad responsibility:

recommend backend by context
generate backend configuration
validate build configuration
wrap common build commands
collect build evidence
support backend migration paths
Documentation Tools

Approved default:

Fumadocs

Potential future tools:

Starlight
VitePress
Docusaurus
MkDocs
custom static docs
enterprise docs integrations

Monad responsibility:

define docs structure
generate docs
validate required docs
detect docs drift
prepare docs for AI context
integrate docs into lifecycle graph
CI/CD Tools

Potential tools:

GitHub Actions
GitLab CI
Buildkite
CircleCI
Jenkins
Woodpecker
Drone
Dagger
Tekton
Argo Workflows

Monad responsibility:

generate CI baselines
validate CI coverage
map CI jobs to lifecycle evidence
collect CI evidence
support provider migration
preserve local/CI parity where feasible
Security Tools

Potential tools:

Gitleaks
Trivy
Syft
Grype
Semgrep
OSV Scanner
OpenSSF Scorecard
Cosign
SLSA generators
dependency review tools

Monad responsibility:

recommend baseline
generate configuration
orchestrate scans
collect evidence
map findings to risks and controls
enforce policy gates
Infrastructure Tools

Potential tools:

Docker
Docker Compose
Kubernetes
Helm
Kustomize
Terraform
Pulumi
OpenTofu
Nomad
Argo CD
Crossplane
Cloudflare tooling

Monad responsibility:

model deployment targets
validate environment definitions
generate local-first infrastructure
support cloud-agnostic capability mapping
collect deployment evidence
preserve provider portability
AI Tools and Providers

Potential providers:

local/no-AI
local Ollama
local vLLM
OpenAI-compatible endpoints
Anthropic
Google
Mistral
OpenRouter
enterprise gateways
custom HTTP adapters

Monad responsibility:

generate provider-agnostic context
enforce AI permissions
log AI actions
evaluate AI outputs
support human approval gates
avoid model lock-in
6. Backend Adapter Model

Monad OS should eventually define a backend adapter model.

Conceptual interface:

BackendAdapter
  id
  name
  category
  detect()
  install()
  generate_config()
  validate()
  run()
  explain()
  collect_evidence()

Example categories:

package-manager
task-graph
build-engine
docs
ci
security
policy
cloud
database
ai-provider
observability
release
deployment

This model allows Monad OS to support strong defaults while preserving backend independence.

7. Canonical vs Generated vs Native Files

Monad OS must distinguish file ownership.

Canonical Monad Files

Examples:

workspace.toml
docs/product/charter.md
docs/product/prd.md
docs/decisions/*.md
.monad/answers.yaml
.monad/recommendation.json
.monad/graph.json

These express Monad-owned intent, rationale, graph, and state.

Native Tool Files

Examples:

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
source.config.ts

These configure execution backends.

Generated Files

Some native files may be generated from Monad intent.

Monad should eventually annotate, document, or track generated files so users know how to modify them safely.

Possible future mechanisms:

.monad/generated-files.json
.monad/file-ownership.json
monad explain file <path>
monad regenerate
8. User Experience Requirements

Users should be able to rely on Monad commands first.

Examples:

monad init --interactive
monad doctor
monad recommend
monad graph
monad docs check
monad run web:build
monad affected test
monad security scan
monad evidence collect

But users should not be prevented from using native tools directly.

Examples:

bun install
nx graph
biome check .

Monad should document when direct native tool usage is safe, discouraged, or likely to cause drift.

9. Error Handling Requirements

Because Monad wraps native tools, native tool failures must be translated where possible.

A poor error:

Process exited with code 1.

A better Monad error:

Nx task failed: web:build

Likely cause:
  TypeScript compilation failed in apps/web.

Suggested next commands:
  monad run web:typecheck
  monad explain task web:build

Native command:
  nx run web:build

Monad should preserve raw backend output when needed, but add context and next steps.

10. Documentation Requirements

Each wrapped backend should have documentation describing:

why it is used
what Monad uses it for
what files it owns
what files Monad generates
how to run it through Monad
how to run it directly
how to replace it
known limitations
troubleshooting steps

Example docs:

docs/tooling/nx.md
docs/tooling/fumadocs.md
docs/tooling/bun.md
docs/tooling/biome.md
docs/tooling/dagger.md
docs/tooling/buck2.md
docs/tooling/pants.md
11. Consequences
Positive Consequences
Faster implementation.
Stronger use of mature tools.
Better ecosystem compatibility.
Less reinvention.
More future-proof architecture.
Better enterprise adaptability.
Clearer SaaS/productized service path.
More credible local-first product.
Negative Consequences
More adapter complexity.
More documentation burden.
More compatibility testing.
Potential leaky abstractions.
Potential backend version drift.
Harder support matrix as the product grows.
Mitigations
Start with a small backend set.
Define stable adapter contracts.
Keep default profiles opinionated.
Use progressive disclosure.
Document native tools honestly.
Add backend health checks.
Add compatibility tests.
Add generated file ownership tracking.
Avoid supporting too many backends too early.
12. Initial Backend Scope
v0

The v0 implementation should not wrap many tools.

Initial focus:

local filesystem
Git detection
workspace.toml
docs foundation
foundation checks
recommendation output
v0.1

Introduce first practical backend wrappers:

Bun
Fumadocs
Biome
Nx under Monad wrapper
GitHub Actions generation
Lefthook
Renovate
v1

Stabilize:

Nx wrapper
docs wrapper
policy checks
evidence basics
AI context generation
project graph
Future

Add enterprise/advanced backends:

moon
Dagger
Pants
Buck2
Nix
OpenTelemetry
deployment providers
database providers
AI providers
13. Non-Goals

This decision does not mean:

Monad will hide all native tools completely
users can never run native tools directly
native tool configs disappear
Monad will support every tool immediately
Monad will never build custom capabilities
Monad will avoid deep integrations forever

Monad may build custom capabilities when they are part of its unique value.

Examples of custom Monad-owned capabilities:

lifecycle graph
recommendation engine
evidence model
policy pack model
AI context generation
generated rationale
SaaS sync model
maturity scoring
lifecycle traceability
14. Success Criteria

This decision is successful if:

Monad users can use one primary CLI.
Monad can coordinate mature tools without replacing them.
Monad remains toolchain-composable.
Monad can swap or add backends over time.
Users understand which tools are being used and why.
Native tools remain accessible when needed.
Monad adds value beyond being a thin wrapper.
The lifecycle graph and evidence model remain Monad-owned.
The architecture supports local-first and SaaS-ready use cases.
15. Final Decision Statement

Monad OS will wrap and coordinate native tools instead of replacing them.

Monad OS will own intent, graph, policy, evidence, documentation structure, recommendations, AI context, and workflow.

Native tools will remain replaceable execution backends.


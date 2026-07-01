# ADR-0011: Use Policy Packs for Governance Extensibility

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will use **policy packs** as the primary mechanism for governance extensibility.

Policy packs will allow Monad OS to apply different governance, security, compliance, architecture, documentation, release, evidence, and AI-safety rules depending on the repository's context.

Policy packs should be installable, versioned, explainable, and eventually shareable through a future pack/marketplace system.

Examples of future policy packs:

```txt
startup-default
enterprise-default
open-source-maintainer
internal-platform
agency-client-work
nist-ssdf
slsa
owasp-samm
soc2-readiness
ai-governance
fintech-saas
healthcare-saas
government-adjacent
```

The initial local core does not need a full policy engine.

However, Monad OS should be designed so governance rules are not hard-coded forever.

---

# 1. Context

Monad OS is intended to become an SDLC control plane.

Governance is central to that vision.

The system should eventually validate and guide:

* repository structure
* documentation coverage
* ownership
* architecture decisions
* risk tracking
* security posture
* release evidence
* dependency management
* AI-assisted development
* compliance readiness
* change approval expectations
* environment/deployment controls

Different organizations need different governance rules.

A solo founder does not need the same policy burden as a regulated enterprise.

An open-source library does not need the same controls as a healthcare SaaS product.

A fintech platform does not need the same policies as a personal project.

Therefore, governance must be extensible.

---

# 2. Alternatives Considered

## Alternative 1: Hard-code one governance model

Monad OS could define one fixed set of governance rules.

### Advantages

* Easier initial implementation.
* Easier documentation.
* More predictable behavior.
* Fewer combinations to test.

### Disadvantages

* Too rigid.
* Poor fit for diverse users.
* Either too heavy for small teams or too weak for enterprises.
* Harder to support productized services.
* Harder to support industry-specific needs.
* Harder to create a future marketplace.
* Harder to evolve without breaking users.

### Decision

Rejected.

Monad OS should have strong defaults, but governance must be extensible.

---

## Alternative 2: Make all governance fully custom from the beginning

Monad OS could require each user to define all policies manually.

### Advantages

* Maximum flexibility.
* No assumptions.
* Easy to adapt to unusual environments.

### Disadvantages

* Terrible onboarding.
* Too much work for users.
* Weak product value.
* No reusable governance intelligence.
* Harder to create explainable recommendations.
* Harder to standardize best practices.

### Decision

Rejected.

Monad OS should provide reusable policy packs with strong recommendations.

---

## Alternative 3: Use policy packs

Monad OS can provide default policy packs and allow additional packs to be installed later.

### Advantages

* Strong defaults.
* Extensible governance.
* Better fit for different team sizes and industries.
* Supports productized services.
* Supports future marketplace.
* Supports open-source/community contributions.
* Supports enterprise customization.
* Keeps governance explainable and versioned.

### Disadvantages

* Requires pack format design.
* Requires policy resolution rules.
* Requires versioning.
* Requires conflict handling.
* Requires clear documentation.

### Decision

Accepted.

---

# 3. Rationale

Policy packs are the best way to balance:

```txt
strong defaults
+
custom governance
+
future marketplace
+
enterprise extensibility
+
local-first operation
```

Policy packs also support Monad OS's larger product thesis:

> Monad OS owns lifecycle graph, policy, evidence, and explainable workflow.

Governance should become a reusable asset.

This is commercially important because teams will pay for packaged governance knowledge, such as:

* SOC 2 readiness
* NIST SSDF alignment
* SLSA-oriented supply-chain posture
* AI development governance
* enterprise release gates
* regulated SaaS controls
* internal platform standards

Policy packs also support productized services.

A consultant could apply a pack to a client repo, run checks, generate a gap report, and sell remediation work.

---

# 4. Policy Pack Responsibilities

A policy pack may define rules for:

## Repository Structure

Examples:

* required root files
* required directories
* naming conventions
* forbidden paths
* generated file ownership
* monorepo boundaries

## Documentation

Examples:

* required README
* required AGENTS.md
* required Product Charter
* required PRD
* required ADRs
* required runbooks
* required service docs
* required API docs
* docs index coverage

## Architecture

Examples:

* ADR required for architectural changes
* service boundaries must be declared
* dependency direction rules
* domain ownership rules
* forbidden cross-layer imports
* architecture drift detection

## Security

Examples:

* secret scanning required
* dependency update policy
* SBOM required for releases
* provenance required for artifacts
* security-sensitive paths require approval
* threat model required for high-risk services

## Release

Examples:

* changelog required
* release notes required
* migration plan required
* rollback plan required
* test evidence required
* security evidence required

## AI Safety

Examples:

* AI actions must be logged
* AI edits forbidden in protected paths
* human approval required for risky changes
* context exclusions required
* prompt/context packs must exclude secrets

## Compliance

Examples:

* control evidence required
* policy waivers tracked
* risk register maintained
* audit log exported
* evidence retention rules

---

# 5. Initial Policy Pack Examples

## startup-default

Purpose:

Useful but lightweight governance for solo founders and small teams.

Possible checks:

```txt
README.md exists
AGENTS.md exists
workspace.toml exists
docs/product/charter.md exists
docs/product/prd.md exists
docs/decisions/ exists
basic .gitignore exists
basic governance principles exist
```

## enterprise-default

Purpose:

Stronger governance for serious engineering teams.

Possible checks:

```txt
CODEOWNERS exists
SECURITY.md exists
CONTRIBUTING.md exists
ADR process exists
risk register exists
release process exists
dependency update policy exists
security scanning configured
branch strategy documented
```

## ai-governance

Purpose:

Rules for AI-assisted development.

Possible checks:

```txt
AGENTS.md exists
AI context rules exist
protected paths are declared
AI action logging is enabled
human approval gates are defined
secret/context exclusions exist
```

## soc2-readiness

Purpose:

Prepare repository for SOC 2-style evidence expectations.

Possible checks:

```txt
access control docs exist
change management docs exist
risk register exists
release evidence exists
security evidence exists
incident process exists
audit trail exists
```

## slsa

Purpose:

Improve software supply-chain maturity.

Possible checks:

```txt
build provenance enabled
artifact signing configured
dependency update process exists
SBOM generation configured
CI workflow permissions reviewed
release artifacts traceable
```

---

# 6. Policy Pack Format

The initial policy pack format can be simple.

Future example:

```toml
[pack]
id = "startup-default"
name = "Startup Default"
version = "0.1.0"
category = "governance"

[checks.required_files]
files = [
  "README.md",
  "AGENTS.md",
  "workspace.toml",
  "docs/product/charter.md",
  "docs/product/prd.md"
]

[checks.required_directories]
directories = [
  "docs/decisions",
  "docs/architecture",
  "docs/governance"
]
```

More advanced policy packs may later use:

* TOML
* YAML
* JSON
* Rego/OPA
* custom Rust checks
* Semgrep rules
* file pattern rules
* graph query rules

The pack format should start simple and evolve.

---

# 7. Policy Execution Model

Future command examples:

```bash
monad policy list
monad policy apply startup-default
monad policy apply ai-governance
monad policy check
monad policy explain startup-default
monad policy report
```

Policy check output should be explainable.

Example:

```txt
Policy check failed: required file missing

Policy:
  startup-default.required_files

Missing:
  docs/product/prd.md

Why this matters:
  The PRD defines product requirements and prevents implementation drift.

Suggested fix:
  monad generate product prd
```

---

# 8. Policy Pack Storage

Initial local policy packs may live in:

```txt
policy-packs/
  startup-default/
  enterprise-default/
  ai-governance/
```

or:

```txt
packs/policies/
  startup-default/
  enterprise-default/
  ai-governance/
```

The exact structure can be finalized later.

Current recommendation:

```txt
policy-packs/
```

because policy packs are important enough to deserve a clear top-level location in early architecture docs.

---

# 9. Interaction With `workspace.toml`

`workspace.toml` should eventually declare active policy packs.

Example:

```toml
[policy]
enabled = true
active_packs = [
  "startup-default",
  "ai-governance"
]

[policy.enforcement]
mode = "warn"
```

Future enforcement modes:

```txt
off
warn
fail
strict
ci-only
advisory
```

This allows policies to be introduced progressively.

---

# 10. Interaction With Evidence

Policy checks should produce evidence.

Example future output:

```txt
.monad/evidence/policy/2026-06-29-policy-check.json
```

Example evidence:

```json
{
  "schema_version": "0.1",
  "type": "policy_check",
  "pack": "startup-default",
  "status": "passed",
  "timestamp": "2026-06-29T00:00:00Z"
}
```

This supports future SaaS evidence vault and compliance workflows.

---

# 11. Interaction With Lifecycle Graph

Policy packs should eventually become graph nodes.

Example nodes:

```txt
PolicyPack
PolicyRule
PolicyCheck
PolicyResult
Waiver
Exception
Evidence
Control
```

Example relationships:

```txt
PolicyPack contains PolicyRule
PolicyRule evaluated_as PolicyResult
PolicyResult produces Evidence
PolicyRule maps_to Control
Waiver overrides PolicyRule
```

This makes governance queryable.

---

# 12. Policy Conflict Handling

Future Monad OS must handle conflicts between policy packs.

Example:

```txt
startup-default says docs/product/prd.md is required.
minimal-open-source says docs/product/prd.md is optional.
```

Possible resolution mechanisms:

* priority order
* explicit override
* profile selection
* local waiver
* environment-specific enforcement
* advisory versus strict modes

Conflict handling does not need to be implemented immediately, but the design should anticipate it.

---

# 13. Waivers and Exceptions

Governance must allow controlled exceptions.

Future commands:

```bash
monad policy waive
monad policy exceptions
monad policy explain-waiver
```

A waiver should include:

```txt
policy rule
reason
owner
expiry
approval
evidence link
```

Waivers are important for enterprise realism.

---

# 14. Non-Goals

This decision does not mean:

* a full policy engine must be implemented in v0
* all policies must use OPA/Rego
* all policies must be strict from day one
* every repo must use enterprise policies
* policy packs must be marketplace-ready immediately
* users cannot customize policies
* Monad must replace all existing security/compliance tools

This decision establishes policy packs as the governance extensibility model.

---

# 15. Initial Scope

## v0

v0 may include only hard-coded foundation checks and documentation that describes future policy packs.

## v0.1

Introduce a simple local policy pack format for required files/directories.

## v0.2

Add:

```txt
monad policy check
monad policy list
basic policy results
```

## v1

Stabilize:

```txt
baseline policy packs
policy evidence
workspace.toml policy declaration
policy docs
CI-friendly policy checks
```

## Future

Add:

```txt
OPA/Rego support
Semgrep integration
compliance mapping
waivers
policy marketplace
hosted policy dashboards
organization-wide policy management
```

---

# 16. Risks

## Risk: Policy packs become too complex too early

Mitigation:

Start with simple file/directory/docs checks.

## Risk: Policy system becomes too rigid

Mitigation:

Support advisory/warn/fail modes and future waivers.

## Risk: Too many packs confuse users

Mitigation:

Use interactive recommendations and profiles.

## Risk: Policy packs duplicate external tools

Mitigation:

Wrap and coordinate external tools where appropriate.

## Risk: Governance feels burdensome

Mitigation:

Use progressive disclosure and lightweight defaults for small teams.

---

# 17. Success Criteria

This decision is successful if:

1. Monad OS can start with simple governance checks.
2. Governance can later be extended without rewriting the core.
3. Policy packs can be selected based on user context.
4. Policy results can produce evidence.
5. Policy packs can become future marketplace assets.
6. Enterprise users can customize governance.
7. Small users are not overwhelmed by enterprise policies.
8. Policy packs reinforce Monad's lifecycle graph and evidence model.

---

# 18. Final Decision Statement

Monad OS will use policy packs for governance extensibility.

Policy packs will encode reusable governance, security, compliance, release, documentation, architecture, and AI-safety rules.

The initial implementation may be simple, but the architecture will treat policy packs as a first-class extensibility model.


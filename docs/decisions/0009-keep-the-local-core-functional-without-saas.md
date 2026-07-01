# ADR-0009: Keep the Local Core Functional Without SaaS

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will be designed so the **local core remains fully useful without requiring a hosted SaaS account**.

The local CLI must provide meaningful value by itself.

The future hosted SaaS offering should extend the local core, not replace it.

The initial product surface will be local-first:

```bash
monad ...
```

The local core should support:

* repository initialization
* interactive recommendations
* workspace manifest management
* documentation generation
* repo inspection
* project graph generation
* validation and doctor checks
* policy checks
* evidence generation
* AI-agnostic context generation
* toolchain wrapping
* local reports
* future sync preparation

The future SaaS control plane may add:

* hosted lifecycle graph
* team and organization views
* evidence vault
* dashboards
* policy management
* integration sync
* maturity analytics
* benchmarking
* marketplace
* enterprise administration

But SaaS must not be required for the local CLI to be valuable.

---

# 1. Context

Monad OS is intended to become a local-first and SaaS-ready SDLC control plane.

The product has two strategic needs:

1. Immediate local utility.
2. Future commercial SaaS potential.

If Monad OS requires SaaS too early, it may lose trust, reduce adoption, and limit use in privacy-sensitive, offline, solo-founder, open-source, and enterprise environments.

If Monad OS ignores SaaS entirely, it may limit future business potential.

The correct approach is:

> Local-first core, SaaS-ready architecture.

This means local artifacts should be structured, versioned, parseable, and eventually syncable, but the local workflow should work without a hosted account.

---

# 2. Alternatives Considered

## Alternative 1: SaaS-first product

Monad OS could require users to create a hosted account before using meaningful functionality.

### Advantages

* Easier monetization.
* Centralized data from the beginning.
* Easier hosted analytics.
* Easier team collaboration features.
* Easier marketplace integration later.

### Disadvantages

* Weakens developer trust.
* Blocks offline use.
* Blocks air-gapped use.
* Blocks privacy-sensitive use.
* Adds friction to adoption.
* Makes the product less useful for solo founders and consultants.
* Creates risk before the local core proves value.
* Conflicts with the open-source/local-first adoption strategy.

### Decision

Rejected.

Monad OS should not be SaaS-first.

---

## Alternative 2: Local-only product forever

Monad OS could remain purely local and never build a hosted SaaS layer.

### Advantages

* Maximum privacy.
* Simpler architecture.
* Easier open-source positioning.
* Easier offline and air-gapped use.
* Lower operational burden.

### Disadvantages

* Limits commercial upside.
* Limits team/org collaboration.
* Limits hosted evidence vault opportunities.
* Limits maturity analytics.
* Limits integration sync.
* Limits marketplace possibilities.
* Limits enterprise management features.
* Limits recurring revenue.

### Decision

Rejected.

Monad OS should be local-first, but not local-only forever.

---

## Alternative 3: Local-first core with optional SaaS extension

Monad OS can provide a useful local core and design artifacts so they can later sync to a hosted control plane.

### Advantages

* Strong developer trust.
* Strong adoption path.
* Supports offline and private workflows.
* Supports open-source core.
* Supports future SaaS business model.
* Supports productized services.
* Supports enterprise self-hosting.
* Avoids premature SaaS complexity.
* Preserves optionality.

### Disadvantages

* Requires careful artifact design.
* Requires local/hosted boundary discipline.
* Requires future sync model.
* May delay hosted monetization.
* Some features must be designed twice: local and hosted.

### Decision

Accepted.

---

# 3. Rationale

Monad OS should be trusted developer infrastructure.

Developer infrastructure earns trust when it works locally, produces inspectable files, and does not require users to send sensitive repository metadata to a hosted service before receiving value.

The local-first approach also supports:

* solo founders
* consultants
* open-source users
* private companies
* regulated organizations
* air-gapped environments
* enterprise self-hosting
* productized service workflows

The future SaaS product remains strategically important, but it should be additive.

The rule is:

> SaaS extends the local core. SaaS does not replace the local core.

---

# 4. Local Core Responsibilities

The local core should eventually support the following capabilities.

## Repository Initialization

```bash
monad init
monad init --interactive
```

The CLI should create a useful repo foundation without requiring SaaS.

## Recommendation Engine

```bash
monad recommend
monad recommend --interactive
```

Recommendations should be generated locally from user answers and known rules.

## Workspace Manifest

```txt
workspace.toml
```

The local manifest should be human-readable and parseable.

## Documentation

```bash
monad docs check
monad docs dev
monad docs build
```

Documentation should be readable locally and later renderable with Fumadocs.

## Repo Inspection

```bash
monad inspect
monad graph
```

Monad should inspect local files and produce useful graph information.

## Doctor Checks

```bash
monad doctor
```

Validation should work locally.

## Policy Checks

```bash
monad policy check
```

Policy checks should run locally.

## Evidence Generation

```bash
monad evidence collect
```

Evidence should be generated locally as files.

## AI-Agnostic Context

```bash
monad ai context
```

Context packs should be generated locally and should not require a specific AI provider.

## Tool Wrapping

```bash
monad run web:build
monad affected test
```

Wrapped tool workflows should work locally when the underlying tools are installed.

---

# 5. SaaS Responsibilities

The future hosted SaaS should add capabilities that are difficult or less useful locally.

Potential hosted capabilities:

```txt
multi-repo lifecycle graph
team and organization dashboards
hosted evidence vault
repository maturity scoring
cross-repo policy visibility
integration sync
historical trend analysis
benchmarking
marketplace
team workflows
approval workflows
enterprise access control
hosted AI workflow orchestration
```

The hosted SaaS should ingest local Monad artifacts rather than requiring a completely separate product model.

---

# 6. Local Artifact Strategy

Local artifacts must be structured for future synchronization.

Important artifacts:

```txt
workspace.toml
.monad/answers.yaml
.monad/recommendation.json
.monad/graph.json
.monad/context/
.monad/evidence/
docs/
docs/decisions/
docs/product/
docs/architecture/
docs/governance/
docs/roadmap/
```

Future sync should be able to read these files and construct hosted state.

---

# 7. Sync-Ready Design

Even though SaaS is not built first, the local core should avoid designs that block future sync.

Local artifacts should eventually include:

* schema versions
* stable IDs
* timestamps where appropriate
* source paths
* commit SHAs where appropriate
* evidence metadata
* provider metadata
* policy decision metadata
* graph node IDs
* graph edge types

Example future evidence metadata:

```json
{
  "schema_version": "0.1",
  "id": "evidence.build.2026-06-29.001",
  "type": "build",
  "source": "local-cli",
  "commit": "abc123",
  "created_at": "2026-06-29T00:00:00Z"
}
```

The v0 implementation does not need the full model, but the architecture should leave room for it.

---

# 8. Privacy and Trust Requirements

Local-first design supports trust.

Monad OS should avoid uploading repository data by default.

Future SaaS sync must be:

* explicit
* opt-in
* documented
* configurable
* auditable
* policy-controlled

Users should know:

* what data is collected
* where it is stored
* how it is used
* how to disable sync
* how to delete hosted data
* how to run locally only

---

# 9. Enterprise and Air-Gapped Implications

Keeping the local core functional without SaaS enables future enterprise modes.

Possible future enterprise modes:

```txt
local-only
self-hosted
private cloud
single-tenant SaaS
air-gapped
hybrid sync
```

This is important for:

* regulated industries
* government-adjacent organizations
* finance
* healthcare
* defense-adjacent workflows
* companies with strict IP controls
* companies that cannot send repo metadata to third-party SaaS

---

# 10. Open Source / Commercial Boundary

The local-first decision supports a strong open-source core.

Possible open-source core:

```txt
CLI
workspace manifest
repo initialization
basic graph
basic docs checks
basic policy checks
basic evidence files
AI-agnostic context generation
local reports
```

Possible paid SaaS features:

```txt
hosted lifecycle graph
multi-repo dashboards
team/org management
evidence vault
advanced policy packs
integration sync
maturity scoring
benchmarking
marketplace
enterprise controls
```

This boundary should be refined later.

---

# 11. Implementation Implications

The Rust local core should not assume a network connection.

Commands should be designed to work offline unless explicitly documented otherwise.

Examples:

```bash
monad doctor
monad graph
monad docs check
monad recommend
monad ai context
```

These should not require SaaS.

Commands that use hosted features should be explicit later:

```bash
monad cloud login
monad sync status
monad sync push
monad sync pull
monad evidence upload
```

These should not be part of the earliest local core.

---

# 12. Manifest Implications

`workspace.toml` should eventually support local/SaaS configuration.

Example future fields:

```toml
[monad]
schema_version = "0.1"

[sync]
enabled = false
mode = "local-only"

[privacy]
upload_repo_metadata = false
upload_evidence = false
upload_ai_context = false
```

The v0 seed manifest can remain simpler.

---

# 13. CLI Implications

The CLI should make local-first behavior obvious.

Good examples:

```bash
monad init --interactive
monad doctor
monad graph
monad docs check
```

Future SaaS commands should be clearly separate:

```bash
monad login
monad sync
monad cloud
```

Avoid making basic local commands require authentication.

---

# 14. Non-Goals

This decision does not mean:

* Monad OS will never have SaaS.
* Monad OS will never collect hosted data.
* Monad OS will never support team workflows.
* Monad OS will never support hosted AI workflows.
* Monad OS will never support hosted evidence vaults.
* Monad OS will never monetize.
* Monad OS must open-source every future feature.
* SaaS sync must be implemented in v0 or v1.

This decision only establishes that local functionality must be real and useful without SaaS.

---

# 15. Risks

## Risk: Local core becomes too limited

Mitigation:

* Ensure local commands solve real problems.
* Prioritize init, recommendation, docs, graph, doctor, policy, and evidence basics.
* Avoid making hosted features the only meaningful features.

## Risk: SaaS architecture becomes an afterthought

Mitigation:

* Keep local artifacts structured.
* Add schema versions.
* Preserve stable IDs.
* Design sync paths before implementation hardens.

## Risk: Commercial boundary becomes unclear

Mitigation:

* Define open-source/pro/SaaS/enterprise editions later.
* Keep local core useful.
* Reserve hosted collaboration, evidence vault, analytics, and marketplace for paid offerings.

## Risk: Privacy concerns block adoption

Mitigation:

* Make sync opt-in.
* Document data handling.
* Provide local-only mode.
* Support self-hosted and air-gapped modes later.

---

# 16. Success Criteria

This decision is successful if:

1. Users can initialize and use Monad OS locally without an account.
2. Local docs, graph, checks, and recommendations provide real value.
3. The local core can be used in private/offline environments.
4. Local artifacts are structured enough for future sync.
5. Future SaaS can extend the local core without replacing it.
6. Users trust Monad OS with sensitive repositories.
7. The product can support open-source, SaaS, and enterprise self-hosted paths.

---

# 17. Final Decision Statement

Monad OS will be local-first and SaaS-ready.

The local core must remain functional and valuable without a hosted account.

The future SaaS control plane will extend local workflows through optional synchronization, hosted graph intelligence, evidence vaults, dashboards, integrations, and marketplace capabilities.


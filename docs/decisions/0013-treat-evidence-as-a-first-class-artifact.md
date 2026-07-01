# ADR-0013: Treat Evidence as a First-Class Artifact

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will treat **evidence** as a first-class artifact.

Evidence will not be an afterthought, a temporary CI log, or an external compliance spreadsheet.

Monad OS will model, generate, collect, validate, store, and eventually synchronize evidence related to the software lifecycle.

Evidence may include:

- product evidence
- requirements evidence
- architecture evidence
- decision evidence
- policy evidence
- test evidence
- build evidence
- security evidence
- dependency evidence
- release evidence
- deployment evidence
- incident evidence
- AI action evidence
- compliance control evidence
- operational evidence

The initial local core may only generate simple evidence files.

The long-term architecture should support a local evidence model, a future hosted evidence vault, and enterprise/compliance exports.

---

# 1. Context

Monad OS is intended to become an SDLC control plane and monorepo operating system.

A serious software delivery system must be able to prove what happened.

Important questions include:

- What was changed?
- Why was it changed?
- Who approved it?
- Which requirement did it satisfy?
- Which tests passed?
- Which build produced the artifact?
- Which security checks ran?
- Which release included it?
- Which deployment shipped it?
- Which incident did it cause or fix?
- Which policy allowed or blocked it?
- Which AI assistant or agent contributed to it?
- Which compliance control does it support?

Most teams answer these questions manually by searching through tickets, PRs, CI logs, scanner outputs, spreadsheets, docs, and chat history.

Monad OS should make evidence a normal output of engineering workflows.

---

# 2. Alternatives Considered

## Alternative 1: Ignore evidence until compliance features are built

Monad OS could defer evidence until a future compliance module exists.

### Advantages

- Simpler early implementation.
- Less schema design up front.
- Faster local CLI work.
- Avoids premature enterprise complexity.

### Disadvantages

- Evidence model becomes bolted on later.
- Local artifacts may not be suitable for audit/compliance workflows.
- Release and policy workflows may lack traceability.
- Future SaaS evidence vault becomes harder to add.
- Weakens enterprise moat.
- Weakens productized service value.

### Decision

Rejected.

Evidence should be part of the architecture from the beginning, even if initial implementation is simple.

---

## Alternative 2: Rely on existing tool logs only

Monad OS could rely on CI logs, test reports, scanner outputs, Git history, and deployment logs.

### Advantages

- Avoids duplicating data.
- Uses existing sources.
- Easier initial implementation.
- Less storage responsibility.

### Disadvantages

- Logs are scattered.
- Logs are inconsistent.
- Logs are not normalized.
- Logs may expire.
- Logs are hard to query across lifecycle stages.
- Logs rarely connect requirements, decisions, policies, releases, and incidents.
- External tools do not share one evidence model.

### Decision

Rejected as the complete strategy.

Monad OS may ingest native tool outputs, but it should normalize them into a Monad evidence model.

---

## Alternative 3: Store evidence only in hosted SaaS

Monad OS could make evidence a hosted-only feature.

### Advantages

- Centralized evidence vault.
- Easier dashboards.
- Easier compliance exports.
- Easier team/org features.

### Disadvantages

- Violates local-first principle.
- Blocks private/offline/air-gapped users.
- Reduces trust.
- Makes the local core weaker.
- Forces SaaS before local value is proven.

### Decision

Rejected.

Evidence should exist locally first and optionally sync to SaaS later.

---

## Alternative 4: Treat evidence as a first-class local and syncable artifact

Monad OS can generate local evidence files and design them to sync later.

### Advantages

- Supports local-first operation.
- Supports future SaaS evidence vault.
- Supports auditability.
- Supports compliance readiness.
- Supports release discipline.
- Supports policy packs.
- Supports AI action accountability.
- Supports productized services.
- Strengthens enterprise moat.

### Disadvantages

- Requires schema/versioning design.
- Requires storage conventions.
- Requires lifecycle graph integration.
- Requires careful privacy handling.
- More work than ignoring evidence.

### Decision

Accepted.

---

# 3. Rationale

Evidence is one of the strongest commercial differentiators for Monad OS.

Most developer tools focus on action:

- build
- test
- deploy
- scan
- release

Monad OS should focus on both action and proof:

- what happened
- why it happened
- what produced it
- what approved it
- what verified it
- what controls it satisfies
- what risks remain

This supports:

- enterprise trust
- compliance readiness
- release governance
- incident response
- AI governance
- SaaS evidence vault
- productized consulting services
- lifecycle graph traceability

The governing principle is:

> Important lifecycle events should produce evidence.

---

# 4. Evidence Categories

Monad OS should eventually support multiple evidence categories.

## Product Evidence

Examples:

```txt
product charter
PRD
roadmap
success metrics
personas
jobs to be done
```

## Requirements Evidence

Examples:

```txt
requirements
acceptance criteria
non-functional requirements
traceability records
coverage reports
```

## Architecture Evidence

Examples:

```txt
ADRs
RFCs
architecture diagrams
domain models
dependency maps
architecture drift reports
```

## Policy Evidence

Examples:

```txt
policy check results
policy pack versions
waivers
exceptions
approval records
control mappings
```

## Test Evidence

Examples:

```txt
unit test reports
integration test reports
contract test reports
E2E test reports
coverage reports
performance test results
accessibility test results
mutation test results
```

## Build Evidence

Examples:

```txt
build logs
build target results
cache metadata
artifact paths
build backend
commit SHA
build environment
```

## Security Evidence

Examples:

```txt
secret scan reports
dependency scan reports
container scan reports
SBOMs
provenance
signatures
threat models
security review records
```

## Release Evidence

Examples:

```txt
release plan
release notes
changelog
test summary
security summary
migration plan
rollback plan
approval record
artifact manifest
```

## Deployment Evidence

Examples:

```txt
deployment target
environment
version deployed
deployment timestamp
deployment actor
deployment status
post-deploy checks
rollback status
```

## Incident Evidence

Examples:

```txt
incident report
timeline
root cause
customer impact
corrective actions
preventive actions
postmortem
follow-up tasks
regression tests
```

## AI Action Evidence

Examples:

```txt
AI plan
AI-generated patch summary
files changed
approval record
tool calls
policy decisions
context pack used
human review record
```

## Compliance Evidence

Examples:

```txt
control evidence
control mapping
audit export
evidence retention record
risk acceptance
waiver
exception approval
```

---

# 5. Initial Local Evidence Structure

Early local evidence can live under:

```txt
.monad/evidence/
```

Possible future structure:

```txt
.monad/evidence/
  product/
  requirements/
  architecture/
  policy/
  tests/
  builds/
  security/
  releases/
  deployments/
  incidents/
  ai/
  compliance/
```

The repository may also include human-facing summaries under:

```txt
evidence/
```

or:

```txt
reports/evidence/
```

Recommendation:

```txt
.monad/evidence/      = machine-readable local evidence
reports/evidence/     = generated human-facing evidence reports
docs/evidence/        = documentation explaining evidence model/process
```

The exact structure can be finalized in the evidence model spec.

---

# 6. Evidence Schema Requirements

Evidence should eventually include common metadata.

Possible fields:

```txt
schema_version
id
type
category
title
description
source
source_path
tool
provider
status
created_at
commit_sha
branch
actor
related_nodes
artifacts
privacy_classification
retention_policy
```

Example:

```json
{
  "schema_version": "0.1",
  "id": "evidence.policy.2026-06-29.001",
  "type": "policy_check",
  "category": "policy",
  "title": "Foundation policy check",
  "source": "monad-cli",
  "status": "passed",
  "created_at": "2026-06-29T00:00:00Z",
  "related_nodes": [
    "policy.startup-default"
  ]
}
```

The first implementation may use simpler text or JSON files.

Schema versioning should be added before evidence becomes enforced.

---

# 7. Evidence Commands

Future CLI commands:

```bash
monad evidence collect
monad evidence list
monad evidence inspect <id>
monad evidence verify
monad evidence export
monad evidence report
```

Examples:

```bash
monad evidence collect --type foundation
monad evidence collect --type policy
monad evidence export --format markdown
monad evidence export --framework soc2
monad evidence export --framework nist-ssdf
```

Initial implementation can be much smaller.

For v0/v1, evidence may begin with:

```bash
monad doctor --evidence
monad policy check --evidence
monad recommend --save
```

---

# 8. Evidence and Policy Packs

Policy checks should produce evidence.

Example:

```txt
Policy:
  startup-default.required-docs

Result:
  passed

Evidence:
  .monad/evidence/policy/2026-06-29-startup-default.json
```

Policy packs may define what evidence is required.

Example:

```txt
soc2-readiness requires:
  access control documentation
  change management evidence
  incident response process
  release approval evidence
  security scan evidence
```

This makes policy packs commercially valuable.

---

# 9. Evidence and Lifecycle Graph

Evidence should become part of the lifecycle graph.

Potential graph nodes:

```txt
Evidence
EvidenceBundle
EvidenceSource
Control
PolicyCheck
Build
TestRun
Release
Deployment
Incident
AIAction
```

Potential graph edges:

```txt
Evidence proves Requirement
Evidence supports Control
Evidence produced_by Build
Evidence verifies Release
Evidence generated_by Tool
Evidence reviewed_by Actor
Evidence associated_with Commit
Evidence satisfies PolicyRule
```

This enables future queries:

```bash
monad graph query "what evidence supports release v1.0.0?"
monad evidence for requirement REQ-001
monad evidence for control SOC2-CC8.1
monad evidence for deployment production
```

---

# 10. Evidence and SaaS

The future hosted SaaS control plane should include an evidence vault.

The evidence vault may provide:

* evidence storage
* evidence search
* evidence retention
* evidence export
* control mapping
* release evidence bundles
* audit packages
* team dashboards
* trend analysis
* evidence freshness checks

Local evidence should be designed so it can be synchronized later.

SaaS sync must be opt-in and privacy-aware.

---

# 11. Evidence and AI Governance

AI-assisted development requires evidence.

AI action evidence may include:

```txt
AI provider or mode
model/capability used if available
context pack used
prompt template used
files proposed
files changed
tests run
policy checks run
human approval record
risk classification
```

This does not mean every prompt must be stored forever.

Instead, Monad OS should define evidence appropriate to the risk level.

For high-risk AI actions, evidence must be stronger.

---

# 12. Evidence and Releases

Every mature release should eventually produce a release evidence bundle.

Possible structure:

```txt
.monad/evidence/releases/v1.0.0/
  release-plan.json
  test-summary.json
  security-summary.json
  sbom.json
  provenance.json
  artifact-manifest.json
  approval.json
  rollback-plan.md
```

Human-facing summary:

```txt
reports/evidence/releases/v1.0.0.md
```

This becomes a major enterprise differentiator.

---

# 13. Evidence and Compliance

Monad OS should not claim compliance automatically.

Instead, it should help collect and organize evidence that may support compliance work.

Supported future frameworks may include:

```txt
NIST SSDF
SLSA
OWASP SAMM
SOC 2
ISO 27001
CIS Controls
HIPAA optional
PCI optional
GDPR optional
FedRAMP future
```

Important distinction:

> Monad OS can provide evidence readiness and control mapping; it does not by itself certify compliance.

---

# 14. Privacy and Retention

Evidence may contain sensitive information.

Future evidence model must account for:

* secrets
* customer data
* internal architecture
* vulnerability details
* incident details
* AI prompts/context
* source paths
* user identities
* cloud/provider metadata

Evidence should support:

```txt
privacy classification
retention policy
redaction
local-only mode
sync exclusions
access control in SaaS
```

Raw source code should not be included in evidence unless explicitly configured.

---

# 15. Non-Goals

This decision does not mean:

* full evidence system must be implemented in v0
* compliance automation must be complete in v1
* evidence replaces external systems of record
* Monad guarantees compliance certification
* all logs must be stored forever
* all AI prompts must be stored forever
* all evidence must sync to SaaS
* raw source code must be uploaded
* every command must immediately generate evidence

This decision establishes evidence as a first-class architectural concept.

---

# 16. Initial Scope

## v0

Possible evidence-related functionality:

* document evidence concept
* create `.monad/evidence/` directory
* save recommendation output
* save foundation check output optionally

## v0.1

Add:

* doctor evidence output
* docs check evidence output
* basic policy evidence output

## v0.2

Add:

* evidence list/inspect commands
* simple JSON schema
* evidence report generation

## v1

Add:

* stable evidence basics
* policy evidence
* test/build evidence adapters where feasible
* release evidence bundle prototype
* AI context/action evidence basics

## Future

Add:

* hosted evidence vault
* compliance exports
* control mapping
* evidence retention
* evidence redaction
* enterprise dashboards
* audit packages

---

# 17. Risks

## Risk: Evidence model becomes too complex too early

Mitigation:

Start with simple JSON files and human-readable reports.

## Risk: Evidence storage captures sensitive data

Mitigation:

Use privacy classifications, redaction, local-only defaults, and sync controls.

## Risk: Users misunderstand evidence as compliance certification

Mitigation:

Document that evidence supports compliance work but does not certify compliance.

## Risk: Evidence becomes noisy

Mitigation:

Generate evidence for meaningful lifecycle events, not every trivial command.

## Risk: Evidence duplicates external tools

Mitigation:

Ingest and normalize external outputs instead of replacing tools.

---

# 18. Success Criteria

This decision is successful if:

1. Monad OS treats evidence as part of normal lifecycle workflows.
2. Evidence can be generated locally.
3. Evidence can support policy checks.
4. Evidence can support release discipline.
5. Evidence can support AI action accountability.
6. Evidence can eventually sync to SaaS.
7. Evidence can eventually support compliance exports.
8. Evidence strengthens Monad's enterprise and productized-service value.

---

# 19. Final Decision Statement

Monad OS will treat evidence as a first-class artifact.

Evidence will be generated, collected, normalized, validated, stored locally, and eventually syncable to a hosted evidence vault.

Evidence is central to governance, auditability, compliance readiness, release discipline, AI accountability, and enterprise trust.


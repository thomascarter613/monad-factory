# ADR-0014: Treat Lifecycle Graph as the Core Product Moat

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will treat the **software lifecycle graph** as the core product moat.

The lifecycle graph is the governed, queryable, auditable model that connects software delivery artifacts across the full SDLC.

The graph should eventually connect:

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

The lifecycle graph is not merely a visualization.

It is the product's reasoning layer.

It should power:

- repo inspection
- project graph enrichment
- impact analysis
- AI context generation
- policy checks
- evidence traceability
- release governance
- compliance readiness
- architecture governance
- modernization planning
- SaaS dashboards
- maturity analytics
- productized service workflows

---

# 1. Context

Most software tools understand one slice of the lifecycle.

Examples:

- Git understands commits and branches.
- GitHub understands issues, PRs, checks, and repositories.
- Jira and Linear understand planning work.
- Nx, Turborepo, moon, Buck2, Pants, and Bazel understand build or task graphs.
- CI systems understand pipeline jobs.
- Security tools understand findings.
- Observability platforms understand runtime telemetry.
- Documentation tools understand pages.
- Incident tools understand incidents.
- Compliance systems understand controls and evidence.

Few systems understand the relationships among all of these.

Monad OS should become valuable by connecting these pieces.

The key insight is:

> The code graph is not enough. The SDLC lifecycle graph is the moat.

---

# 2. Alternatives Considered

## Alternative 1: Focus only on repository structure

Monad OS could focus mainly on generating and validating repository structure.

### Advantages

- Easier to build.
- Easier to explain.
- Faster MVP.
- Useful for greenfield projects.

### Disadvantages

- Weak competitive moat.
- Easier to copy.
- Limited SaaS potential.
- Limited enterprise value.
- Does not solve traceability across requirements, decisions, releases, evidence, and incidents.

### Decision

Rejected as the core product moat.

Repository structure remains important, but it is not enough.

---

## Alternative 2: Focus only on task/build graph

Monad OS could focus on build graph and affected task execution.

### Advantages

- Clear developer value.
- Directly improves CI speed.
- Familiar monorepo category.
- Useful for engineering teams.

### Disadvantages

- Competes directly with Nx, Turborepo, moon, Buck2, Pants, Bazel, and similar tools.
- Narrower product category.
- Does not cover requirements, decisions, policy, evidence, releases, incidents, or AI governance.
- Weaker SaaS/productized-service differentiation.

### Decision

Rejected as the core product moat.

Task/build graph data should be an input to the lifecycle graph.

---

## Alternative 3: Focus only on AI workflows

Monad OS could focus primarily on AI context, AI coding workflows, and AI agent orchestration.

### Advantages

- Timely market interest.
- Strong immediate developer interest.
- Potentially high perceived innovation.

### Disadvantages

- Highly dependent on model/provider churn.
- Crowded space.
- Risk of weak governance.
- AI workflows without lifecycle structure are brittle.
- Does not fully solve enterprise traceability or evidence needs.

### Decision

Rejected as the primary moat.

AI should operate through the lifecycle graph, not replace it.

---

## Alternative 4: Focus on evidence/compliance only

Monad OS could become an evidence and compliance automation platform.

### Advantages

- Strong enterprise value.
- Clear monetization potential.
- Strong productized service fit.

### Disadvantages

- May start too far from developer workflows.
- Could become compliance bureaucracy instead of developer infrastructure.
- Less useful for early local-first adoption.
- Evidence without lifecycle graph lacks context.

### Decision

Rejected as the only moat.

Evidence is first-class, but evidence should be connected by the lifecycle graph.

---

## Alternative 5: Treat lifecycle graph as the core moat

Monad OS can model the full SDLC lifecycle graph and use it to connect repo structure, tasks, docs, decisions, policies, evidence, AI workflows, releases, deployments, and incidents.

### Advantages

- Strongest differentiation.
- Supports local and SaaS products.
- Supports enterprise use cases.
- Supports AI-safe workflows.
- Supports compliance readiness.
- Supports modernization services.
- Supports maturity analytics.
- Supports future marketplace and policy packs.
- Harder to copy because graph quality improves with integrations, packs, evidence, and usage.

### Disadvantages

- More complex.
- Requires careful domain modeling.
- Requires phased implementation.
- Requires stable IDs and schemas.
- Requires high-quality documentation.
- Risk of overbuilding if attempted too early.

### Decision

Accepted.

---

# 3. Rationale

The lifecycle graph is the strongest product moat because it connects everything Monad OS is meant to govern.

A normal project graph can answer:

```txt
Which projects depend on this package?
```

A lifecycle graph should answer:

```txt
Why does this package exist?
Which requirement does it support?
Which ADR governs it?
Which risks apply to it?
Which policies protect it?
Which tests verify it?
Which release shipped it?
Which deployment runs it?
Which incidents involved it?
Which AI context is needed to safely modify it?
```

This is much more valuable than a conventional monorepo graph.

The graph turns Monad OS from a tool wrapper into a software delivery intelligence platform.

---

# 4. Lifecycle Graph Node Types

The graph should eventually include many node types.

## Product and Strategy Nodes

```txt
BusinessGoal
ProductOutcome
KPI
Initiative
Roadmap
Milestone
Persona
JobToBeDone
```

## Planning Nodes

```txt
Epic
Feature
Requirement
AcceptanceCriteria
NonFunctionalRequirement
WorkPacket
Task
Subtask
Sprint
Dependency
Blocker
```

## Architecture Nodes

```txt
System
Domain
BoundedContext
Service
App
Package
Library
Module
API
Event
Database
ArchitectureDecision
Design
RFC
Risk
ThreatModel
```

## Implementation Nodes

```txt
Repository
Workspace
Project
File
Directory
Symbol
Function
Class
Interface
CodeChange
Commit
PullRequest
Review
Owner
CodeOwner
```

## Verification Nodes

```txt
TestPlan
TestSuite
UnitTest
IntegrationTest
ContractTest
E2ETest
PerformanceTest
SecurityTest
AccessibilityTest
TestRun
CoverageReport
```

## Security and Governance Nodes

```txt
PolicyPack
PolicyRule
PolicyCheck
PolicyResult
Control
Finding
Vulnerability
Waiver
Exception
Approval
Attestation
```

## Build and Release Nodes

```txt
Build
BuildTarget
BuildAction
Artifact
ContainerImage
Package
SBOM
Provenance
Signature
Release
ReleaseCandidate
ReleasePlan
Changelog
MigrationPlan
RollbackPlan
```

## Deployment and Operations Nodes

```txt
Environment
Deployment
DeploymentTarget
Region
Tenant
FeatureFlag
Secret
Config
ServiceLevelObjective
ServiceLevelIndicator
ErrorBudget
Metric
Log
Trace
Alert
Dashboard
Runbook
```

## Incident and Learning Nodes

```txt
Incident
IncidentTimeline
CustomerImpact
RootCause
CorrectiveAction
PreventiveAction
Postmortem
Learning
Improvement
RegressionTest
```

## AI Nodes

```txt
AIProvider
AIModel
AICapability
AIContextPack
AIPlan
AIAction
AIApproval
AIEvidence
PromptTemplate
AgentPolicy
```

## Evidence Nodes

```txt
Evidence
EvidenceBundle
EvidenceSource
EvidenceReport
ComplianceMapping
AuditExport
```

---

# 5. Lifecycle Graph Edge Types

The graph should eventually support relationships such as:

```txt
depends_on
owned_by
implements
satisfies
documents
decided_by
governed_by
protected_by
tested_by
verified_by
produced_by
released_in
deployed_to
observed_by
triggered
caused_by
mitigated_by
approved_by
blocked_by
waived_by
evidenced_by
uses_provider
generated_by
syncs_to
```

Examples:

```txt
Requirement tested_by TestSuite
Service governed_by PolicyPack
Package decided_by ADR
Release evidenced_by EvidenceBundle
Deployment caused_by Release
Incident caused_by Deployment
CorrectiveAction creates Requirement
AIAction approved_by HumanApproval
```

---

# 6. Initial Graph Scope

The full lifecycle graph should not be implemented immediately.

## v0

Graph may be conceptual and file-backed.

Minimum nodes:

```txt
Workspace
Document
Decision
ProductArtifact
```

Minimum graph behavior:

```bash
monad graph
```

May initially print a simple summary.

## v0.1

Add project-level graph.

Nodes:

```txt
Workspace
App
Package
Service
Tool
Document
Decision
Policy
```

## v0.2

Add generated project registry and relationships.

Nodes:

```txt
Project
Task
Owner
Doc
PolicyCheck
Evidence
```

## v1

Stabilize local graph basics.

Capabilities:

```txt
project graph
docs graph
decision graph
policy/evidence links
AI context graph input
JSON graph output
```

## v2

Hosted SaaS graph.

Capabilities:

```txt
multi-repo graph
historical graph
team/org graph
evidence graph
integration graph
maturity analytics
cross-repo queries
```

---

# 7. Graph Storage Strategy

The earliest implementation can use generated JSON.

Possible local graph artifact:

```txt
.monad/graph.json
```

Future options:

```txt
.monad/graph.json
.monad/graph.sqlite
hosted graph database
hosted relational + graph projection
```

Recommendation:

```txt
v0/v1:
  JSON first.

v1.5:
  Consider SQLite for richer local querying.

v2:
  Hosted graph service.
```

The local graph should be deterministic enough to regenerate from source files where possible.

---

# 8. Graph Query Strategy

Future commands:

```bash
monad graph
monad graph --json
monad graph query "what depends on packages/auth?"
monad graph explain services/billing
monad trace requirement REQ-001
monad impact packages/ui
monad evidence for release v1.0.0
```

Initial graph output can be simple.

Future graph query should support:

* plain-language queries
* structured query language
* JSON output
* Mermaid output
* DOT output
* Markdown reports

---

# 9. Relationship to Nx, Buck2, Pants, and Other Graphs

Native backend graphs are inputs to the Monad lifecycle graph.

Examples:

```txt
Nx project graph
Buck2 build graph
Pants dependency graph
moon project graph
Cargo package graph
Go module graph
TypeScript import graph
OpenAPI dependency graph
Database schema graph
```

Monad should normalize and enrich these graphs.

Important rule:

> Backend graphs describe execution relationships. Monad graph describes lifecycle relationships.

---

# 10. Relationship to AI Context

The lifecycle graph should be a primary source for AI context generation.

Future command:

```bash
monad ai context --for services/billing
```

Should use graph data to include:

* related requirements
* related ADRs
* owners
* dependencies
* tests
* policies
* evidence
* risks
* docs
* protected paths
* recent changes

This prevents AI from acting only on raw code.

---

# 11. Relationship to Evidence

Evidence should be connected to graph nodes.

Examples:

```txt
Evidence proves Requirement
Evidence verifies Release
Evidence supports Control
Evidence generated_by PolicyCheck
Evidence generated_by Build
Evidence generated_by TestRun
```

This enables auditability.

Example future query:

```bash
monad evidence for control SOC2-CC8.1
```

---

# 12. Relationship to Policy

Policy should operate over the graph.

Examples:

```txt
If Service has data_classification = sensitive,
then ThreatModel is required.

If Project type = public-api,
then OpenAPI contract is required.

If Release includes DatabaseMigration,
then RollbackPlan is required.

If AIAction touches protected path,
then HumanApproval is required.
```

Graph-aware policies are much more powerful than file-only checks.

---

# 13. Relationship to SaaS

The hosted SaaS control plane should be built around the lifecycle graph.

SaaS graph features may include:

* multi-repo graph
* historical graph
* graph diff
* evidence graph
* policy graph
* risk graph
* maturity graph
* integration graph
* organization graph

This is one of the strongest long-term SaaS differentiators.

---

# 14. Relationship to Productized Services

The lifecycle graph enables repeatable services.

Examples:

```txt
AI readiness audit
monorepo modernization audit
software supply-chain gap assessment
documentation drift audit
release evidence readiness audit
architecture governance audit
SOC 2 readiness assessment
```

The lifecycle graph can power reports and remediation plans.

This supports the business model.

---

# 15. Manifest Implications

`workspace.toml` should eventually provide declared graph nodes and metadata.

Example:

```toml
[workspace]
name = "monad-os"

[[projects]]
id = "apps.docs"
type = "app"
name = "docs"
owner = "platform"
docs = "docs/apps/docs.md"

[[policies.active]]
id = "startup-default"

[[decisions]]
id = "ADR-0014"
path = "docs/decisions/0014-treat-lifecycle-graph-as-the-core-product-moat.md"
```

The graph should combine declared metadata with discovered metadata.

---

# 16. Non-Goals

This decision does not mean:

* the full lifecycle graph must be implemented in v0
* a graph database is required immediately
* every artifact must be modeled immediately
* graph visualization must be built immediately
* AI must be required for graph queries
* SaaS must be built before local graph
* native build graphs are replaced
* every relationship must be manually declared

This decision establishes the lifecycle graph as the long-term core product moat.

---

# 17. Risks

## Risk: Graph model becomes too complex too early

Mitigation:

Start with small graph slices.

## Risk: Graph requires too much manual metadata

Mitigation:

Combine declared metadata with discovery.

## Risk: Graph becomes stale

Mitigation:

Regenerate where possible and validate with `monad doctor`.

## Risk: Graph queries are hard to implement

Mitigation:

Start with JSON output and simple queries before natural language.

## Risk: Users do not understand graph value

Mitigation:

Expose practical commands like impact analysis, traceability, and evidence queries.

## Risk: SaaS graph becomes disconnected from local graph

Mitigation:

Use syncable local artifacts and stable IDs.

---

# 18. Success Criteria

This decision is successful if:

1. Monad OS has a clear graph-first architecture.
2. Local graph starts simple and evolves.
3. Native tool graphs can feed Monad graph.
4. Documentation, decisions, policies, and evidence become graph nodes.
5. AI context generation improves because of graph data.
6. Policy checks become more powerful because of graph data.
7. SaaS product value centers on hosted lifecycle graph.
8. The lifecycle graph becomes difficult for competitors to replicate.

---

# 19. Final Decision Statement

Monad OS will treat the software lifecycle graph as the core product moat.

The graph will connect code, docs, requirements, decisions, policies, evidence, releases, deployments, incidents, operations, and AI workflows.

The local implementation will begin small, but the long-term product will be graph-native.


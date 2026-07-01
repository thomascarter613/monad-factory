# ADR-0015: Require Human Approval Gates for Risky AI Actions

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will require **human approval gates for risky AI actions**.

AI may assist with planning, explanation, documentation, code generation, testing, review, refactoring, and evidence preparation.

However, AI must not be allowed to perform high-risk actions autonomously without explicit human approval.

High-risk AI actions include changes involving:

- authentication
- authorization
- billing
- payments
- production infrastructure
- secrets
- encryption
- security policies
- compliance controls
- data migrations
- destructive operations
- dependency supply-chain changes
- release approvals
- deployment to production
- protected branches
- sensitive customer/user data
- policy waivers
- evidence deletion
- incident/postmortem modification
- AI permission changes

Monad OS will support AI-assisted workflows, but AI actions must be:

```txt
bounded
policy-controlled
auditable
explainable
reviewable
reversible where possible
```

The core rule is:

> AI may propose. Humans approve high-risk actions.

---

# 1. Context

Monad OS is intended to be AI-agnostic and AI-operable.

It should support AI-assisted software development, including:

* repo explanation
* context generation
* task planning
* code generation
* refactoring proposals
* documentation generation
* test generation
* review assistance
* migration planning
* evidence preparation
* policy explanation
* release note generation

But software development contains high-risk areas.

If AI can freely modify protected code, production infrastructure, billing logic, security rules, compliance evidence, or deployment workflows, the system becomes unsafe and difficult to trust.

Monad OS must therefore include explicit approval gates for risky AI actions.

This is especially important because Monad OS may later be sold as SaaS, productized service tooling, or enterprise software.

---

# 2. Alternatives Considered

## Alternative 1: Allow AI to act freely

Monad OS could allow AI agents to modify files, run commands, approve workflows, deploy, and change policies freely.

### Advantages

* Maximum automation.
* Impressive demos.
* Faster apparent productivity.
* Less friction.

### Disadvantages

* Unsafe.
* Low trust.
* High risk of destructive changes.
* High risk of security incidents.
* High risk of compliance violations.
* High risk of supply-chain compromise.
* Harder enterprise adoption.
* Harder auditability.
* Harder accountability.

### Decision

Rejected.

AI must not have unrestricted authority.

---

## Alternative 2: Forbid AI from making any changes

Monad OS could restrict AI to read-only explanation and context generation.

### Advantages

* Very safe.
* Easy to reason about.
* Low risk.
* Easier compliance posture.

### Disadvantages

* Too limited.
* Weak product differentiation.
* Reduces AI-assisted development value.
* Makes Monad less useful for future AI-native workflows.
* Users will work around the restrictions with external AI tools.

### Decision

Rejected.

AI should be able to assist with meaningful work, but within policy boundaries.

---

## Alternative 3: Allow AI changes only in low-risk areas

Monad OS could permit AI changes in low-risk areas and require approval for high-risk areas.

### Advantages

* Balanced.
* Useful.
* Safer than unrestricted AI.
* Supports productivity.
* Supports governance.
* Supports enterprise trust.
* Supports local-first and SaaS-ready workflows.
* Enables future policy packs and approval systems.

### Disadvantages

* Requires risk classification.
* Requires policy model.
* Requires approval workflow.
* Requires action logging.
* Requires clear UX.
* May slow some workflows.

### Decision

Accepted.

---

# 3. Rationale

Monad OS should be built for serious software systems.

Serious systems need accountability.

AI can be extremely useful, but the value comes from combining AI speed with deterministic governance.

Monad OS should not position AI as an autonomous unbounded developer.

Instead, Monad OS should position AI as a powerful assistant operating inside the lifecycle graph, policy system, evidence system, and human approval workflow.

The key product principle is:

> AI acceleration without governance is risk. AI acceleration with policy, evidence, and human approval is leverage.

---

# 4. Risk Classification

Monad OS should eventually classify AI actions by risk level.

## Low-Risk Actions

Examples:

```txt
summarize docs
generate glossary draft
explain repo structure
create non-authoritative notes
draft README improvements
draft tutorial text
generate local context pack
suggest task breakdown
```

Possible default behavior:

```txt
AI may perform or propose locally.
Human review recommended but not mandatory.
```

## Medium-Risk Actions

Examples:

```txt
modify documentation
generate tests
generate non-critical code
refactor internal utility
add non-production example
create draft ADR
create draft PRD
suggest dependency update
```

Possible default behavior:

```txt
AI may propose patch.
Human review required before commit/merge.
```

## High-Risk Actions

Examples:

```txt
modify authentication
modify authorization
modify billing
modify payment logic
modify secrets handling
modify encryption
modify production infrastructure
modify CI release pipeline
modify data migrations
modify security policies
modify compliance controls
modify protected files
approve release
deploy to production
delete evidence
create policy waiver
```

Possible default behavior:

```txt
AI may plan or draft.
Explicit human approval required before apply.
```

## Critical-Risk Actions

Examples:

```txt
rotate/delete production secrets
destroy infrastructure
delete production data
disable security controls
bypass policy checks
force-push protected branch
approve its own high-risk changes
modify AI permission system
```

Possible default behavior:

```txt
AI cannot perform directly.
Manual human action required.
```

---

# 5. Approval Gate Model

Future Monad OS should support approval gates.

Conceptual approval object:

```json
{
  "schema_version": "0.1",
  "id": "approval.ai.2026-06-29.001",
  "action_id": "ai-action.001",
  "risk_level": "high",
  "status": "approved",
  "approved_by": "human",
  "created_at": "2026-06-29T00:00:00Z",
  "reason": "Approved after review of migration plan and rollback plan."
}
```

Future commands:

```bash
monad ai plan "add billing workflow"
monad ai review-plan .monad/ai/plans/billing.json
monad ai approve .monad/ai/plans/billing.json
monad ai apply .monad/ai/plans/billing.json
```

High-risk workflow:

```txt
AI proposes plan
→ Monad classifies risk
→ Monad checks policy
→ Human reviews
→ Human approves
→ Monad applies or allows action
→ Monad records evidence
```

---

# 6. AI Action Evidence

Risky AI actions should produce evidence.

Possible files:

```txt
.monad/evidence/ai/
  ai-action-2026-06-29-001.json
  ai-approval-2026-06-29-001.json
```

AI evidence should include:

```txt
action id
risk level
requested action
files affected
policies evaluated
approval status
human reviewer
tests run
evidence produced
timestamp
AI provider/mode if known
context pack used
```

This supports auditability and enterprise trust.

---

# 7. AI Permission Model

Monad OS should eventually define AI permissions.

Example future configuration:

```toml
[ai.permissions]
default_mode = "propose-only"

[ai.permissions.paths]
"docs/**" = "draft"
"apps/**" = "propose"
"packages/**" = "propose"
"services/auth/**" = "approval-required"
"services/billing/**" = "approval-required"
"infra/prod/**" = "manual-only"
"policies/**" = "approval-required"
".github/workflows/**" = "approval-required"

[ai.permissions.actions]
deploy_production = "manual-only"
delete_evidence = "manual-only"
create_policy_waiver = "approval-required"
modify_ai_permissions = "manual-only"
```

Permission levels may include:

```txt
read
suggest
draft
propose
apply-low-risk
approval-required
manual-only
forbidden
```

---

# 8. Protected Areas

Monad OS should treat certain areas as protected by default.

Protected areas may include:

```txt
authentication
authorization
billing
payments
security
secrets
production infrastructure
release workflows
data migrations
compliance evidence
policy packs
AI permissions
protected branches
deployment credentials
```

Protected path examples:

```txt
services/auth/**
services/billing/**
infra/prod/**
policies/**
policy-packs/**
.github/workflows/**
.monad/evidence/**
.monad/state/**
```

Protection rules should be configurable through policy packs and workspace settings.

---

# 9. Relationship to Policy Packs

Policy packs should define AI approval requirements.

Example:

```txt
ai-governance policy pack:
  - AI cannot edit secrets.
  - AI cannot deploy to production.
  - AI cannot delete evidence.
  - AI changes to auth require approval.
  - AI changes to billing require approval.
  - AI context packs must exclude .env files.
```

Future policy command:

```bash
monad policy check --scope ai
```

Policy result should indicate whether AI action is allowed, blocked, or approval-required.

---

# 10. Relationship to Lifecycle Graph

AI actions should become lifecycle graph nodes.

Potential nodes:

```txt
AIProvider
AIModel
AIContextPack
AIPlan
AIAction
AIApproval
AIEvidence
HumanReviewer
PolicyDecision
```

Potential relationships:

```txt
AIAction uses AIContextPack
AIAction proposes CodeChange
AIAction evaluated_by PolicyRule
AIAction requires AIApproval
AIApproval approved_by HumanReviewer
AIAction produces AIEvidence
AIAction modifies Project
```

This gives Monad OS traceability over AI-assisted development.

---

# 11. Relationship to SaaS

Future hosted SaaS may provide:

* organization-level AI policies
* approval workflows
* AI action dashboards
* AI evidence vault
* AI risk reports
* model/provider inventory
* policy enforcement history
* human reviewer assignment
* enterprise audit logs

However, local approval gates should remain possible without SaaS.

SaaS should enhance AI governance, not be required for it.

---

# 12. Relationship to AI Agnosticism

Approval gates must be provider-agnostic.

The risk model should not depend on whether the AI provider is:

```txt
OpenAI
Anthropic
Google
Mistral
Ollama
vLLM
OpenRouter
custom endpoint
enterprise gateway
```

The same governance model should apply.

The system should govern AI actions, not just AI vendors.

---

# 13. Human Approval UX

Approval must be clear and explicit.

Bad UX:

```txt
AI applied high-risk changes automatically.
```

Good UX:

```txt
AI proposed high-risk changes.

Risk level:
  High

Reasons:
  - touches services/billing/**
  - adds database migration
  - modifies release workflow

Required approvals:
  - code owner
  - security reviewer
  - human operator

Next:
  monad ai approve .monad/ai/plans/billing-change.json
```

Approval should not be hidden behind vague prompts.

---

# 14. Non-Goals

This decision does not mean:

* AI cannot be used.
* AI can only read files.
* every AI suggestion needs formal approval.
* full AI approval workflow must be implemented in v0.
* SaaS is required for approvals.
* Monad must store all prompts forever.
* Monad must support every AI provider immediately.
* human approval guarantees correctness.
* AI-generated code is automatically safe after approval.

This decision means risky AI actions require explicit human control.

---

# 15. Initial Scope

## v0

Document AI approval principle.

Core commands should work without AI.

No autonomous risky AI actions.

## v0.1

Add AI context generation.

Possible command:

```bash
monad ai context
```

This should be provider-neutral.

## v0.2

Add basic AI action policy model.

Possible output:

```txt
allowed
approval-required
blocked
```

## v1

Add:

```txt
AI context packs
protected path configuration
approval-required classification
AI action evidence basics
human-readable AI policy docs
```

## Future

Add:

```txt
AI plan/apply workflow
AI action ledger
formal approval records
SaaS AI governance dashboard
organization-level AI policies
AI eval harness
model/provider routing
```

---

# 16. Risks

## Risk: Approval gates slow users down

Mitigation:

Only require approval for risky actions. Keep low-risk AI assistance lightweight.

## Risk: Risk classification is wrong

Mitigation:

Use conservative defaults and allow policy customization.

## Risk: Users bypass Monad with external AI tools

Mitigation:

Make Monad context and approval workflow useful enough that users prefer it.

## Risk: Approval creates false confidence

Mitigation:

Approval should require tests, evidence, review, and policy checks where applicable.

## Risk: AI evidence stores sensitive prompts/context

Mitigation:

Store summaries and metadata by default. Make raw prompt/context storage configurable.

## Risk: SaaS AI governance feels intrusive

Mitigation:

Keep local-only mode and make sync opt-in.

---

# 17. Success Criteria

This decision is successful if:

1. Monad OS can support useful AI workflows.
2. Risky AI actions are not applied without human approval.
3. AI action evidence can be generated.
4. AI permissions can be configured.
5. Policy packs can define AI safety rules.
6. Local-first AI governance works without SaaS.
7. Future SaaS can add organization-level AI governance.
8. Enterprise users can trust Monad OS as an AI-safe SDLC control plane.

---

# 18. Final Decision Statement

Monad OS will require human approval gates for risky AI actions.

AI may assist, plan, draft, explain, and propose.

High-risk actions require explicit human approval.

Critical-risk actions may require manual human execution.

AI acceleration must operate inside Monad OS's policy, evidence, lifecycle graph, and approval model.


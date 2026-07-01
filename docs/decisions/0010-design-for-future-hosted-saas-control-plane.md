# ADR-0010: Design for Future Hosted SaaS Control Plane

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will be designed for a future hosted SaaS control plane, while keeping the local core functional without SaaS.

The hosted SaaS offering may eventually provide:

- multi-repository lifecycle graph
- hosted evidence vault
- policy management
- organization and team dashboards
- maturity analytics
- integration synchronization
- marketplace for packs and plugins
- hosted recommendation intelligence
- collaboration workflows
- enterprise administration
- optional AI workflow orchestration
- benchmarking and delivery intelligence

The local core will remain the primary foundation.

The hosted SaaS should extend local workflows by syncing structured local artifacts, not replace the local product model.

---

# 1. Context

Monad OS is intended to begin as a local-first CLI and monorepo operating system.

However, the long-term commercial opportunity includes SaaS and productized services.

A hosted SaaS control plane can provide value that is difficult to provide locally:

- cross-repo visibility
- organization-wide governance
- team dashboards
- historical analytics
- hosted evidence retention
- integration sync
- marketplace distribution
- compliance exports
- maturity scoring
- benchmarking
- enterprise administration

The architecture should preserve this future path without requiring SaaS in v0 or v1.

---

# 2. Alternatives Considered

## Alternative 1: Ignore SaaS until much later

Monad OS could focus entirely on local CLI features and defer all SaaS-related design decisions.

### Advantages

- Simpler early implementation.
- Less risk of premature abstraction.
- Faster local MVP.
- Cleaner open-source positioning.

### Disadvantages

- Local artifacts may become difficult to sync later.
- Object IDs may not be stable.
- Evidence formats may not be suitable for hosted use.
- Hosted graph architecture may require redesign.
- Product/business model may be harder to layer on later.

### Decision

Rejected.

Monad OS should not build SaaS first, but it should be SaaS-ready from the beginning.

---

## Alternative 2: Build SaaS first

Monad OS could begin as a hosted dashboard and require all projects to sync to it.

### Advantages

- Faster monetization path.
- Centralized data model from the beginning.
- Easier analytics.
- Easier team workflows.

### Disadvantages

- Violates local-first trust.
- Adds authentication, tenancy, hosting, billing, security, and operations too early.
- Increases scope before local value is proven.
- Blocks offline/private/air-gapped users.
- Reduces open-source adoption.
- Makes the project too heavy too soon.

### Decision

Rejected.

Local core comes first.

---

## Alternative 3: Design local artifacts to be syncable later

Monad OS can build local-first capabilities while ensuring artifacts are structured enough for future SaaS synchronization.

### Advantages

- Preserves local-first trust.
- Preserves future commercial path.
- Supports open-source core.
- Supports productized services.
- Supports enterprise self-hosted options.
- Avoids premature SaaS implementation.
- Reduces future migration pain.

### Disadvantages

- Requires more discipline in local data design.
- Requires schema versioning earlier.
- Requires stable IDs earlier.
- Requires thinking about privacy and sync boundaries before SaaS exists.

### Decision

Accepted.

---

# 3. Rationale

The ideal strategy is:

> Local-first core, SaaS-ready artifacts.

Monad OS should create valuable local artifacts such as:

- workspace manifest
- recommendation files
- graph files
- evidence files
- context packs
- policy results
- documentation
- ADRs
- PRDs
- roadmap files
- risk records

These artifacts should eventually be ingestible by a hosted control plane.

That allows the product to grow from:

```txt
local CLI
```

to:

```txt
local CLI + hosted graph/evidence/control plane
```

without discarding early work.

---

# 4. Future SaaS Product Scope

The future hosted SaaS control plane may include the following modules.

## 4.1 Repository Inventory

Tracks connected repositories and their Monad metadata.

Potential features:

* repo list
* repo health
* stage/maturity
* toolchain inventory
* docs coverage
* policy status
* evidence status

## 4.2 Lifecycle Graph

Provides hosted graph queries across one or more repositories.

Potential features:

* requirement-to-release traceability
* ADR-to-code relationships
* policy-to-evidence relationships
* service dependency maps
* ownership maps
* incident-to-change relationships

## 4.3 Evidence Vault

Stores and indexes evidence.

Potential evidence types:

* test evidence
* build evidence
* security evidence
* release evidence
* deployment evidence
* policy evidence
* AI action evidence
* compliance control evidence

## 4.4 Policy Management

Allows organizations to manage governance policies.

Potential features:

* policy pack installation
* policy versioning
* exceptions and waivers
* enforcement history
* approval workflows
* compliance mapping

## 4.5 Maturity Analytics

Scores repository and organization maturity.

Potential dimensions:

* documentation maturity
* security posture
* supply-chain posture
* release discipline
* architecture governance
* test coverage
* observability readiness
* AI governance
* SDLC traceability

## 4.6 Integration Sync

Connects with external systems.

Potential integrations:

* GitHub
* GitLab
* Jira
* Linear
* Slack
* Notion
* monday.com
* Backstage
* Datadog
* Grafana
* cloud providers
* vulnerability scanners
* CI systems

## 4.7 Marketplace

Distributes reusable assets.

Potential marketplace items:

* policy packs
* golden path packs
* app templates
* service templates
* migration recipes
* compliance packs
* AI workflow packs
* integration adapters
* documentation packs

## 4.8 Enterprise Administration

Potential features:

* organizations
* teams
* RBAC
* SSO/SAML/OIDC
* SCIM
* audit logs
* single-tenant deployment
* self-hosted mode
* air-gapped mode

---

# 5. Local-to-SaaS Sync Model

The local core should eventually generate syncable artifacts.

Candidate local artifacts:

```txt
workspace.toml
.monad/answers.yaml
.monad/recommendation.json
.monad/graph.json
.monad/evidence/
.monad/context/
.monad/policy-results/
docs/
docs/decisions/
docs/product/
docs/architecture/
docs/governance/
docs/roadmap/
```

Future sync commands may include:

```bash
monad login
monad sync status
monad sync plan
monad sync push
monad sync pull
monad sync disable
```

Sync must be explicit and opt-in.

---

# 6. Artifact Requirements for SaaS Readiness

Local artifacts should eventually include:

* schema version
* stable ID
* artifact type
* source path
* generated timestamp
* commit SHA when applicable
* tool/provider metadata
* privacy classification where applicable
* relationships to other artifacts
* validation status

Example future artifact metadata:

```json
{
  "schema_version": "0.1",
  "id": "adr.0010",
  "type": "architecture_decision",
  "source_path": "docs/decisions/0010-design-for-future-hosted-saas-control-plane.md",
  "status": "accepted",
  "created_at": "2026-06-29",
  "relationships": [
    {
      "type": "supports",
      "target": "product.monad-os"
    }
  ]
}
```

---

# 7. Privacy Requirements

Future SaaS sync must respect repository sensitivity.

Sync should be:

* opt-in
* explicit
* configurable
* auditable
* revocable
* documented

Users should be able to control whether SaaS receives:

* metadata only
* docs
* graph
* evidence
* policy results
* AI context
* code summaries
* raw source code
* no data at all

Raw source upload should not be assumed.

---

# 8. Edition Strategy

Monad OS may eventually have four product forms.

## 8.1 Open-Source Local Core

Likely includes:

* CLI
* init
* docs foundation
* workspace manifest
* basic graph
* basic checks
* basic evidence files
* AI-agnostic context packs

## 8.2 Pro Local/Desktop Edition

Potentially includes:

* visual graph
* richer local analysis
* advanced generators
* local reports
* advanced local AI workflows
* richer recommendation engine

## 8.3 Hosted SaaS Control Plane

Potentially includes:

* multi-repo graph
* evidence vault
* dashboards
* integration sync
* maturity analytics
* marketplace
* team/org management

## 8.4 Enterprise Self-Hosted Edition

Potentially includes:

* single-tenant deployment
* SSO
* SCIM
* private AI routing
* private evidence storage
* custom policy packs
* air-gapped operation
* premium support

---

# 9. Architectural Implications

The system should eventually separate:

```txt
local CLI
local artifact model
sync protocol
hosted API
hosted graph service
hosted evidence service
hosted policy service
hosted integration workers
hosted dashboard
marketplace
```

But v0 and v1 should not build all of these.

The first priority remains local value.

---

# 10. Manifest Implications

Future `workspace.toml` may include:

```toml
[sync]
enabled = false
mode = "local-only"

[sync.saas]
workspace_id = ""
organization_id = ""
endpoint = ""

[privacy]
upload_metadata = false
upload_docs = false
upload_evidence = false
upload_ai_context = false
upload_source = false
```

These fields should not be required in v0.

---

# 11. Non-Goals

This decision does not mean:

* SaaS will be built in v0
* SaaS will be built in v1
* local workflows require login
* repository data is uploaded by default
* raw source code must be synced
* open-source core must include hosted features
* enterprise self-hosting must be solved immediately

This decision only ensures the architecture does not block SaaS later.

---

# 12. Risks

## Risk: SaaS concerns overcomplicate local core

Mitigation:

* Keep v0/v1 focused on local CLI.
* Add only lightweight schema/versioning where useful.
* Avoid implementing sync before local product value exists.

## Risk: Local artifacts are not syncable later

Mitigation:

* Add schema versions.
* Use stable IDs.
* Store structured artifacts.
* Document artifact ownership.

## Risk: Users distrust hosted sync

Mitigation:

* Make sync opt-in.
* Provide local-only mode.
* Provide clear privacy controls.
* Avoid raw source upload by default.

## Risk: Commercial boundary becomes unclear

Mitigation:

* Define editions later.
* Keep local core useful.
* Reserve hosted graph, evidence vault, analytics, teams, and marketplace for SaaS.

---

# 13. Success Criteria

This decision is successful if:

1. The local core remains useful without SaaS.
2. Local artifacts are structured enough to sync later.
3. Hosted SaaS can be added without redesigning local artifacts.
4. Users can opt into or out of sync explicitly.
5. The SaaS model can support teams, evidence, policy, analytics, and marketplace.
6. The architecture supports enterprise self-hosted and air-gapped futures.
7. SaaS extends local workflows rather than replacing them.

---

# 14. Final Decision Statement

Monad OS will be designed for a future hosted SaaS control plane.

The hosted SaaS will extend the local core through optional synchronization, hosted lifecycle graph, evidence vaults, policy management, dashboards, integrations, analytics, and marketplace capabilities.

The local core remains the foundation.


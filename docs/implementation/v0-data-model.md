# Monad OS v0 Data Model

Status: Draft  
Stage: v0 implementation planning  
Owner: Monad OS maintainers  
Last updated: 2026-06-29

## Purpose

This document defines the initial logical data model for Monad OS v0.

Monad OS turns a software organization’s code, docs, decisions, policies, tests, releases, incidents, infrastructure, and AI workflows into one governed, queryable, auditable lifecycle graph.

The v0 data model describes the minimum set of concepts required for the local-first CLI to:

1. Understand a workspace.
2. Read workspace intent from `workspace.toml`.
3. Inspect repository artifacts.
4. Represent lifecycle graph nodes and edges.
5. Run policy checks.
6. Produce evidence.
7. Package AI-ready context.
8. Prepare for future hosted SaaS without requiring it.

## Scope

The v0 data model is a logical model, not a database schema.

It should guide:

- Rust structs.
- JSON output contracts.
- Evidence artifacts.
- Lifecycle graph artifacts.
- Context pack metadata.
- Future database schema design.
- Future API schema design.

## Non-Goals

The v0 data model does not define:

- A hosted SaaS persistence schema.
- Multi-tenant database tables.
- Billing data.
- User accounts.
- Organization RBAC.
- Remote execution state.
- Incident response workflows.
- Full CI/CD pipeline models.
- Full package dependency graph semantics.
- Full semantic code intelligence.

Those belong to later v1 and v2 models.

## Design Principles

### 1. Local-first

Every v0 entity must be representable using local files and local command output.

### 2. Stable identifiers

Entities should have deterministic IDs where possible.

Example:

```text
doc:README.md
adr:0001
command:monad.doctor
policy:foundation.required-files
```

### 3. Evidence-first

Important command results should be serializable as evidence.

### 4. Graph-ready

Most entities should be convertible into lifecycle graph nodes and edges.

### 5. AI-agnostic

The model may support AI context preparation, but must not depend on a specific model, provider, embedding service, or vector database.

### 6. Cloud-agnostic

The model must not assume GitHub, GitLab, AWS, Azure, GCP, Vercel, Netlify, or any hosted system as the only backend.

### 7. Database-agnostic

The model should be portable across file storage, SQLite, PostgreSQL, document stores, graph databases, and future search/vector stores.

### 8. Append-friendly

Evidence and graph artifacts should be easy to append, version, diff, and archive.

## Storage Locations

The v0 local data model should use these conventional locations.

| Location | Purpose |
|---|---|
| `workspace.toml` | Canonical workspace manifest |
| `.monad/` | Local Monad OS runtime state |
| `.monad/evidence/` | Evidence bundles and check outputs |
| `.monad/graph/` | Lifecycle graph artifacts |
| `.monad/context/` | AI-ready context packs |
| `.monad/cache/` | Optional local cache |
| `.monad/tmp/` | Optional temporary command output |

The `.monad/` directory should be treated as generated local state unless a future decision says specific files should be committed.

## Top-Level Model

The v0 model is organized around these core entities.

```text
Workspace
  Manifest
  Artifact[]
  Command[]
  Tool[]
  Policy[]
  CheckResult[]
  EvidenceBundle[]
  LifecycleGraph
  ContextPack[]
```

## Entity Inventory

| Entity | Purpose |
|---|---|
| `Workspace` | Root unit managed by Monad OS |
| `Manifest` | Parsed representation of `workspace.toml` |
| `Artifact` | File or directory known to Monad OS |
| `Document` | Documentation artifact |
| `ADR` | Architecture Decision Record |
| `WorkPackage` | Implementation planning unit |
| `CommandSpec` | Described CLI command |
| `NativeTool` | External tool wrapped or checked by Monad OS |
| `Policy` | Governance rule |
| `PolicyPack` | Group of related policies |
| `CheckResult` | Result of a validation or policy check |
| `EvidenceBundle` | Auditable command result package |
| `LifecycleGraph` | Graph of artifacts, decisions, policies, commands, and evidence |
| `GraphNode` | Node in the lifecycle graph |
| `GraphEdge` | Edge in the lifecycle graph |
| `ContextPack` | AI-ready context bundle |
| `ApprovalGate` | Human approval requirement for risky actions |
| `Finding` | Warning, violation, or recommendation |
| `NativeInvocation` | Recorded native tool execution |
| `Risk` | Tracked risk or unresolved concern |

## `Workspace`

A `Workspace` is the root unit managed by Monad OS.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable workspace ID |
| `name` | string | Human-readable workspace name |
| `root_path` | string | Workspace root path |
| `manifest_path` | string | Path to `workspace.toml` |
| `monad_dir` | string | Path to `.monad/` local state |
| `created_at` | string or null | Creation timestamp if known |
| `updated_at` | string or null | Last update timestamp if known |

### Example

```json
{
  "id": "workspace:monad-os",
  "name": "monad-os",
  "root_path": ".",
  "manifest_path": "workspace.toml",
  "monad_dir": ".monad",
  "created_at": null,
  "updated_at": null
}
```

## `Manifest`

A `Manifest` is the parsed representation of `workspace.toml`.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `path` | string | Manifest path |
| `format` | string | Manifest format, usually `toml` |
| `schema_version` | string | Manifest schema version |
| `workspace_name` | string | Workspace name |
| `raw_hash` | string | Hash of manifest contents |
| `parsed` | boolean | Whether parsing succeeded |
| `errors` | array | Parse or validation errors |

### Example

```json
{
  "path": "workspace.toml",
  "format": "toml",
  "schema_version": "0.1",
  "workspace_name": "monad-os",
  "raw_hash": "sha256:unknown",
  "parsed": true,
  "errors": []
}
```

## `Artifact`

An `Artifact` is any file or directory known to Monad OS.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable artifact ID |
| `path` | string | Repository-relative path |
| `kind` | string | Artifact kind |
| `exists` | boolean | Whether it exists locally |
| `size_bytes` | integer or null | File size if known |
| `hash` | string or null | Content hash if known |
| `modified_at` | string or null | Last modified time if known |

### Artifact Kinds

| Kind | Description |
|---|---|
| `file` | Generic file |
| `directory` | Generic directory |
| `document` | Documentation file |
| `adr` | Architecture Decision Record |
| `manifest` | Workspace manifest |
| `script` | Script or automation file |
| `policy` | Policy artifact |
| `work_package` | Work package document |
| `roadmap` | Roadmap document |
| `command_spec` | Command specification document |
| `evidence` | Evidence artifact |
| `graph` | Graph artifact |
| `context_pack` | Context package |

### Example

```json
{
  "id": "artifact:docs/implementation/v0-command-spec.md",
  "path": "docs/implementation/v0-command-spec.md",
  "kind": "command_spec",
  "exists": true,
  "size_bytes": null,
  "hash": null,
  "modified_at": null
}
```

## `Document`

A `Document` is a human-authored markdown or text artifact.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable document ID |
| `path` | string | Repository-relative path |
| `title` | string | Document title |
| `section` | string | Documentation section |
| `status` | string | Draft, accepted, active, deprecated, etc. |
| `artifact_id` | string | Linked `Artifact` ID |

### Example

```json
{
  "id": "doc:docs/product/prd.md",
  "path": "docs/product/prd.md",
  "title": "Product Requirements Document",
  "section": "product",
  "status": "draft",
  "artifact_id": "artifact:docs/product/prd.md"
}
```

## `ADR`

An `ADR` represents an architecture decision record.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | ADR ID, such as `adr:0001` |
| `number` | integer | ADR number |
| `title` | string | ADR title |
| `status` | string | Proposed, accepted, superseded, etc. |
| `path` | string | ADR file path |
| `date` | string or null | Decision date if known |
| `supersedes` | array | ADRs superseded by this ADR |
| `superseded_by` | string or null | ADR that supersedes this ADR |

### Example

```json
{
  "id": "adr:0001",
  "number": 1,
  "title": "Build Monad OS as an SDLC Control Plane",
  "status": "accepted",
  "path": "docs/decisions/0001-build-monad-os-as-an-sdlc-control-plane.md",
  "date": null,
  "supersedes": [],
  "superseded_by": null
}
```

## `WorkPackage`

A `WorkPackage` represents a bounded unit of implementation planning.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Work package ID |
| `title` | string | Work package title |
| `path` | string | Source document path |
| `status` | string | Planned, active, blocked, complete |
| `phase` | string | v0, v1, v2, etc. |
| `depends_on` | array | Other work package IDs |
| `related_adrs` | array | Related ADR IDs |
| `acceptance_criteria` | array | Acceptance criteria |

### Example

```json
{
  "id": "wp:v0-cli-foundation",
  "title": "Create v0 CLI Foundation",
  "path": "docs/implementation/v0-work-packages.md",
  "status": "planned",
  "phase": "v0",
  "depends_on": [],
  "related_adrs": ["adr:0001", "adr:0002", "adr:0003"],
  "acceptance_criteria": [
    "CLI builds locally",
    "CLI exposes help and version commands"
  ]
}
```

## `CommandSpec`

A `CommandSpec` represents a command described by the v0 command specification.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable command ID |
| `name` | string | Command name |
| `path` | array | Command path segments |
| `status` | string | Required, stretch, deferred |
| `mutates_files` | boolean | Whether command may change files |
| `requires_approval` | boolean | Whether command requires approval |
| `produces` | array | Artifact kinds produced |
| `related_adrs` | array | Related ADR IDs |

### Example

```json
{
  "id": "command:monad.doctor",
  "name": "doctor",
  "path": ["monad", "doctor"],
  "status": "required",
  "mutates_files": false,
  "requires_approval": false,
  "produces": ["evidence"],
  "related_adrs": ["adr:0001", "adr:0013"]
}
```

## `NativeTool`

A `NativeTool` is an external tool Monad OS may detect, validate, wrap, or orchestrate.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable tool ID |
| `name` | string | Tool name |
| `category` | string | Tool category |
| `required` | boolean | Whether required for current workspace |
| `detected` | boolean | Whether found locally |
| `version` | string or null | Detected version |
| `version_requirement` | string or null | Required version constraint |

### Example

```json
{
  "id": "tool:git",
  "name": "git",
  "category": "vcs",
  "required": true,
  "detected": true,
  "version": null,
  "version_requirement": null
}
```

## `PolicyPack`

A `PolicyPack` groups related policies.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Policy pack ID |
| `name` | string | Human-readable name |
| `version` | string | Policy pack version |
| `source` | string | Local, built-in, registry, etc. |
| `policies` | array | Policy IDs |

### Example

```json
{
  "id": "policy_pack:foundation",
  "name": "Foundation Policy Pack",
  "version": "0.1.0",
  "source": "builtin",
  "policies": [
    "policy:foundation.required-files",
    "policy:foundation.required-directories"
  ]
}
```

## `Policy`

A `Policy` is a governance rule.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Policy ID |
| `name` | string | Human-readable policy name |
| `category` | string | Policy category |
| `severity` | string | info, warning, error, critical |
| `enabled` | boolean | Whether policy is enabled |
| `description` | string | Policy description |
| `remediation` | string or null | Suggested fix |

### Example

```json
{
  "id": "policy:foundation.required-files",
  "name": "Required foundation files exist",
  "category": "foundation",
  "severity": "error",
  "enabled": true,
  "description": "Verifies that required Monad OS foundation files exist.",
  "remediation": "Create the missing files or update the foundation policy."
}
```

## `CheckResult`

A `CheckResult` records the result of a validation, doctor, or policy check.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Check result ID |
| `check_id` | string | Check or policy ID |
| `status` | string | passed, failed, warning, skipped |
| `severity` | string | info, warning, error, critical |
| `message` | string | Human-readable message |
| `path` | string or null | Related file path |
| `evidence` | object or null | Supporting data |

### Example

```json
{
  "id": "check_result:foundation.required-files:docs/00-index.md",
  "check_id": "policy:foundation.required-files",
  "status": "passed",
  "severity": "info",
  "message": "Required file exists: docs/00-index.md",
  "path": "docs/00-index.md",
  "evidence": {
    "exists": true
  }
}
```

## `EvidenceBundle`

An `EvidenceBundle` is an auditable package of command results and local facts.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Evidence bundle ID |
| `evidence_version` | string | Evidence schema version |
| `created_at` | string | Creation timestamp |
| `workspace_id` | string | Related workspace ID |
| `command` | string | Command that produced the evidence |
| `git` | object | Git metadata if available |
| `inputs` | array | Input artifact IDs |
| `outputs` | array | Output artifact IDs |
| `results` | array | Check results or findings |
| `summary` | object | Summary status |

### Example

```json
{
  "id": "evidence:doctor:2026-06-29T00:00:00Z",
  "evidence_version": "0.1",
  "created_at": "2026-06-29T00:00:00Z",
  "workspace_id": "workspace:monad-os",
  "command": "monad doctor",
  "git": {
    "branch": "main",
    "commit": "unknown",
    "dirty": false
  },
  "inputs": [
    "artifact:workspace.toml"
  ],
  "outputs": [
    "artifact:.monad/evidence/doctor.json"
  ],
  "results": [],
  "summary": {
    "status": "passed",
    "passed": 10,
    "failed": 0,
    "warnings": 0
  }
}
```

## `LifecycleGraph`

A `LifecycleGraph` represents the connected model of workspace artifacts, decisions, policies, commands, and evidence.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Graph ID |
| `graph_version` | string | Graph schema version |
| `workspace_id` | string | Related workspace ID |
| `created_at` | string | Creation timestamp |
| `nodes` | array | Graph nodes |
| `edges` | array | Graph edges |
| `summary` | object | Node and edge summary |

### Example

```json
{
  "id": "graph:lifecycle:monad-os",
  "graph_version": "0.1",
  "workspace_id": "workspace:monad-os",
  "created_at": "2026-06-29T00:00:00Z",
  "nodes": [],
  "edges": [],
  "summary": {
    "node_count": 0,
    "edge_count": 0
  }
}
```

## `GraphNode`

A `GraphNode` is a typed vertex in the lifecycle graph.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Node ID |
| `type` | string | Node type |
| `label` | string | Human-readable label |
| `path` | string or null | Related path |
| `properties` | object | Additional metadata |

### v0 Node Types

| Type | Description |
|---|---|
| `workspace` | Workspace root |
| `manifest` | Workspace manifest |
| `document` | Documentation artifact |
| `adr` | Architecture decision record |
| `work_package` | Implementation work package |
| `command` | CLI command |
| `policy` | Governance policy |
| `tool` | Native tool |
| `evidence` | Evidence artifact |
| `context_pack` | AI context package |

### Example

```json
{
  "id": "adr:0001",
  "type": "adr",
  "label": "Build Monad OS as an SDLC Control Plane",
  "path": "docs/decisions/0001-build-monad-os-as-an-sdlc-control-plane.md",
  "properties": {
    "status": "accepted"
  }
}
```

## `GraphEdge`

A `GraphEdge` is a typed relationship between graph nodes.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Edge ID |
| `from` | string | Source node ID |
| `to` | string | Target node ID |
| `type` | string | Edge type |
| `properties` | object | Additional metadata |

### v0 Edge Types

| Type | Description |
|---|---|
| `contains` | Parent contains child |
| `references` | Artifact references another artifact |
| `decides` | ADR decides or constrains something |
| `implements` | Work package implements a decision or capability |
| `validates` | Policy or script validates an artifact |
| `produces` | Command produces an artifact |
| `governs` | Policy governs artifact or action |
| `uses` | Command uses tool or artifact |
| `requires_approval_for` | Approval gate guards action |

### Example

```json
{
  "id": "edge:workspace:monad-os:contains:adr:0001",
  "from": "workspace:monad-os",
  "to": "adr:0001",
  "type": "contains",
  "properties": {}
}
```

## `ContextPack`

A `ContextPack` is an AI-ready bundle of curated workspace context.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Context pack ID |
| `context_version` | string | Context pack schema version |
| `created_at` | string | Creation timestamp |
| `workspace_id` | string | Related workspace ID |
| `profile` | string | Context profile |
| `format` | string | markdown, json, etc. |
| `sources` | array | Source artifacts |
| `output_path` | string | Generated context path |
| `size` | object | Size metadata |
| `warnings` | array | Context generation warnings |

### Initial Profiles

| Profile | Purpose |
|---|---|
| `foundation` | Product, architecture, ADR, and roadmap foundation |
| `implementation` | Implementation-oriented context |
| `handoff` | Context for continuing work in another AI or human session |
| `audit` | Evidence and governance-oriented context |

### Example

```json
{
  "id": "context_pack:foundation:2026-06-29T00:00:00Z",
  "context_version": "0.1",
  "created_at": "2026-06-29T00:00:00Z",
  "workspace_id": "workspace:monad-os",
  "profile": "foundation",
  "format": "markdown",
  "sources": [
    {
      "artifact_id": "artifact:README.md",
      "path": "README.md"
    }
  ],
  "output_path": ".monad/context/foundation.md",
  "size": {
    "bytes": null,
    "estimated_tokens": null
  },
  "warnings": []
}
```

## `ApprovalGate`

An `ApprovalGate` represents a human approval requirement.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Approval gate ID |
| `name` | string | Human-readable name |
| `action_type` | string | Type of action being guarded |
| `required` | boolean | Whether approval is required |
| `reason` | string | Why approval is required |
| `related_policy_ids` | array | Related policies |

### Guarded v0 Action Types

| Action Type | Description |
|---|---|
| `file_overwrite` | Overwriting an existing user file |
| `file_delete` | Deleting a file |
| `git_commit` | Creating a commit |
| `git_push` | Pushing to remote |
| `native_tool_mutation` | Invoking a native tool that mutates project state |
| `ai_code_modification` | AI-generated code change |
| `secret_access` | Reading or exposing secret material |

### Example

```json
{
  "id": "approval_gate:ai_code_modification",
  "name": "AI Code Modification Approval",
  "action_type": "ai_code_modification",
  "required": true,
  "reason": "Risky AI actions require explicit human approval.",
  "related_policy_ids": [
    "policy:safety.risky-ai-actions"
  ]
}
```

## `Finding`

A `Finding` is a warning, violation, recommendation, or informational result.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Finding ID |
| `type` | string | info, warning, violation, recommendation |
| `severity` | string | info, warning, error, critical |
| `title` | string | Short title |
| `message` | string | Human-readable detail |
| `path` | string or null | Related path |
| `remediation` | string or null | Suggested fix |

### Example

```json
{
  "id": "finding:docs.index.missing-reference",
  "type": "violation",
  "severity": "error",
  "title": "Documentation index missing reference",
  "message": "docs/00-index.md does not reference docs/implementation/v0-data-model.md.",
  "path": "docs/00-index.md",
  "remediation": "Add the missing document to the index."
}
```

## `NativeInvocation`

A `NativeInvocation` records an external tool command that Monad OS invokes or checks.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Invocation ID |
| `tool_id` | string | Related native tool |
| `command` | array | Command and arguments |
| `cwd` | string | Working directory |
| `started_at` | string | Start timestamp |
| `finished_at` | string or null | Finish timestamp |
| `exit_code` | integer or null | Process exit code |
| `stdout_path` | string or null | Captured stdout path |
| `stderr_path` | string or null | Captured stderr path |

### Example

```json
{
  "id": "native_invocation:git.status:2026-06-29T00:00:00Z",
  "tool_id": "tool:git",
  "command": ["git", "status", "--short"],
  "cwd": ".",
  "started_at": "2026-06-29T00:00:00Z",
  "finished_at": "2026-06-29T00:00:01Z",
  "exit_code": 0,
  "stdout_path": null,
  "stderr_path": null
}
```

## `Risk`

A `Risk` tracks known uncertainty or potential harm.

### Required Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Risk ID |
| `title` | string | Risk title |
| `description` | string | Risk description |
| `severity` | string | low, medium, high, critical |
| `likelihood` | string | low, medium, high |
| `status` | string | open, mitigated, accepted, closed |
| `mitigation` | string or null | Mitigation strategy |
| `related_artifacts` | array | Related artifact IDs |

### Example

```json
{
  "id": "risk:v0-model-overreach",
  "title": "v0 data model overreach",
  "description": "The v0 model may become too broad before the CLI foundation exists.",
  "severity": "medium",
  "likelihood": "medium",
  "status": "open",
  "mitigation": "Keep v0 implementation focused on local files, evidence, graph, and context.",
  "related_artifacts": [
    "artifact:docs/implementation/v0-data-model.md"
  ]
}
```

## ID Conventions

Stable IDs should use this pattern:

```text
<type>:<stable-key>
```

Examples:

| Entity | Example ID |
|---|---|
| Workspace | `workspace:monad-os` |
| Manifest | `manifest:workspace.toml` |
| Artifact | `artifact:docs/00-index.md` |
| Document | `doc:docs/product/prd.md` |
| ADR | `adr:0001` |
| Work package | `wp:v0-cli-foundation` |
| Command | `command:monad.doctor` |
| Tool | `tool:git` |
| Policy | `policy:foundation.required-files` |
| Policy pack | `policy_pack:foundation` |
| Evidence | `evidence:doctor:2026-06-29T00:00:00Z` |
| Graph | `graph:lifecycle:monad-os` |
| Context pack | `context_pack:foundation:2026-06-29T00:00:00Z` |
| Approval gate | `approval_gate:ai_code_modification` |

## Timestamp Conventions

Use RFC 3339 timestamps where possible.

Example:

```text
2026-06-29T00:00:00Z
```

If the timestamp is unknown, use `null` rather than inventing a date.

## Hash Conventions

When content hashes are implemented, use explicit algorithms.

Example:

```text
sha256:<hex>
```

The model should not assume SHA-256 forever, but SHA-256 is the recommended v0 default.

## Status Values

### Generic Status

```text
draft
planned
active
passed
failed
warning
skipped
blocked
complete
deprecated
superseded
unknown
```

### ADR Status

```text
proposed
accepted
deprecated
superseded
rejected
```

### Policy Severity

```text
info
warning
error
critical
```

### Risk Severity

```text
low
medium
high
critical
```

## Command Output Model

Every evidence-producing command should be able to return a common envelope.

### Common Output Envelope

```json
{
  "schema_version": "0.1",
  "command": "monad doctor",
  "status": "passed",
  "workspace_id": "workspace:monad-os",
  "created_at": "2026-06-29T00:00:00Z",
  "data": {},
  "findings": [],
  "evidence_path": null
}
```

### Required Envelope Fields

| Field | Type | Description |
|---|---|---|
| `schema_version` | string | Output schema version |
| `command` | string | Command that produced output |
| `status` | string | passed, failed, warning, etc. |
| `workspace_id` | string | Related workspace |
| `created_at` | string | Output creation timestamp |
| `data` | object | Command-specific payload |
| `findings` | array | Findings |
| `evidence_path` | string or null | Written evidence path |

## Command-to-Entity Mapping

| Command | Reads | Produces |
|---|---|---|
| `monad init` | Workspace path | `Workspace`, local directories |
| `monad doctor` | `Workspace`, `Manifest`, `Artifact` | `CheckResult`, `EvidenceBundle` |
| `monad workspace inspect` | Local files | `Artifact`, `Document`, `ADR`, `WorkPackage` |
| `monad workspace validate` | `Manifest`, `Artifact` | `CheckResult`, `Finding` |
| `monad policy check` | `Policy`, `Artifact` | `CheckResult`, `Finding`, `EvidenceBundle` |
| `monad evidence collect` | Command outputs | `EvidenceBundle` |
| `monad graph build` | `Artifact`, `ADR`, `Policy`, `CommandSpec` | `LifecycleGraph`, `GraphNode`, `GraphEdge` |
| `monad graph export` | `LifecycleGraph` | Graph artifact |
| `monad context pack` | `Document`, `ADR`, `WorkPackage` | `ContextPack` |

## Minimum v0 JSON Artifacts

The v0 CLI should eventually be able to produce these files.

```text
.monad/evidence/doctor.json
.monad/evidence/workspace-inspect.json
.monad/evidence/workspace-validate.json
.monad/evidence/policy-check.json
.monad/evidence/foundation-evidence.json
.monad/graph/lifecycle-graph.json
.monad/context/context-pack.json
```

## Future Persistence Mapping

Although v0 is file-first, the model should map cleanly to future storage systems.

| Future Store | Model Fit |
|---|---|
| Filesystem | JSON and Markdown artifacts |
| SQLite | Local cache and queryable state |
| PostgreSQL | SaaS relational source of truth |
| Graph database | Lifecycle graph traversal |
| Object storage | Evidence and context artifacts |
| Search index | Documentation and artifact search |
| Vector store | Optional semantic retrieval |

No v0 implementation should require any of these systems beyond the local filesystem.

## Validation Rules

### Workspace Validation

A workspace is valid when:

1. Workspace root exists.
2. `workspace.toml` exists.
3. Manifest parses.
4. Required foundation files exist.
5. Required foundation directories exist.
6. ADR directory exists.
7. Documentation index exists.
8. Implementation docs exist.
9. Foundation script exists and is executable.

### Data Model Validation

The v0 data model is valid when:

1. Entity IDs are stable.
2. Entity types are explicit.
3. Required fields are documented.
4. Graph node and edge types are documented.
5. Evidence bundle structure is documented.
6. Context pack structure is documented.
7. Approval gate structure is documented.
8. The model does not assume a SaaS backend.
9. The model does not assume a specific AI provider.
10. The model does not assume a specific database.

## Open Questions

1. Should v0 define JSON Schema files for each entity immediately?
2. Should `.monad/` generated state be ignored by default?
3. Should evidence bundles include full command stdout and stderr or paths to captured output?
4. Should graph IDs include content hashes?
5. Should context packs include token estimates in v0?
6. Should `workspace.toml` declare policy packs before policy-pack loading exists?
7. Should command output schemas be versioned independently from the data model?
8. Should v0 use one combined state file or separate files per command output?

## Acceptance Criteria

This data model is acceptable for v0 when:

1. It defines the minimum logical entities for the CLI.
2. It supports the v0 command specification.
3. It supports local-first operation.
4. It supports evidence generation.
5. It supports lifecycle graph generation.
6. It supports AI-ready context packaging.
7. It supports future SaaS persistence without requiring SaaS now.
8. It remains AI, cloud, and database agnostic.
9. It is simple enough to implement in Rust structs.
10. It is explicit enough to guide JSON output contracts.

## Summary

The Monad OS v0 data model establishes the first formal vocabulary for the system.

The core progression is:

```text
Workspace -> Artifacts -> Checks -> Evidence -> Graph -> Context
```

This model keeps v0 focused on local inspection, validation, evidence, lifecycle graph construction, and AI-ready context preparation while preserving a clean path toward the future hosted control plane.

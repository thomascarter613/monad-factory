# ADR-0006: Design for AI, Cloud, and Database Agnosticism

## Status

Accepted

## Date

2026-06-29

## Decision

Monad OS will be designed to be **AI-agnostic, cloud-agnostic, and database-agnostic**.

Monad OS may recommend strong defaults, but it must not hard-code the product architecture around one:

- AI provider
- model vendor
- cloud provider
- deployment platform
- database engine
- vector store
- observability provider
- secrets provider
- CI/CD provider
- feature flag provider
- infrastructure provider

The system will use capability-based abstractions, provider adapters, and replaceable backend integrations.

This decision is foundational to Monad OS as a future-proof, next-generation SDLC control plane.

---

# 1. Context

Monad OS is intended to become a local-first and SaaS-ready SDLC control plane.

It must support many different software delivery environments:

- solo founder projects
- open-source projects
- startups
- SMB software teams
- enterprise teams
- regulated organizations
- AI-heavy applications
- cloud-native systems
- local-first systems
- air-gapped/private systems
- hybrid infrastructure
- productized consulting/service offerings

A product in this category cannot assume every user wants the same AI provider, cloud, database, or deployment target.

The technology landscape changes quickly.

AI providers change.
Cloud pricing changes.
Database choices change.
Security requirements change.
Compliance requirements change.
Enterprise procurement requirements change.
Local/offline requirements change.

Monad OS should therefore preserve optionality.

---

# 2. Alternatives Considered

## Alternative 1: Choose one opinionated full stack

Monad OS could hard-code a single recommended stack.

Example:

- OpenAI
- AWS
- PostgreSQL
- Qdrant
- GitHub Actions
- Vercel
- Datadog
- Terraform
- Kubernetes

### Advantages

- Simpler implementation.
- Easier documentation.
- Faster initial scaffolding.
- Fewer combinations to test.
- Easier support in the short term.

### Disadvantages

- Creates vendor lock-in.
- Weakens enterprise adoption.
- Weakens local-first adoption.
- Weakens self-hosted adoption.
- Weakens productized service flexibility.
- Makes the product more fragile as technology changes.
- Conflicts with the long-term SDLC control plane vision.

### Decision

Rejected.

Monad OS may recommend defaults, but it must not permanently hard-code one full stack.

---

## Alternative 2: Avoid recommendations entirely

Monad OS could avoid recommending providers or tools and let users configure everything manually.

### Advantages

- Maximum neutrality.
- No risk of appearing biased.
- Maximum flexibility.

### Disadvantages

- Poor developer experience.
- Too much burden on users.
- Weak onboarding.
- Harder for beginners and solo founders.
- Reduces product value.
- Makes interactive setup less useful.

### Decision

Rejected.

Monad OS should be agnostic, but not indecisive.

The product should provide explainable recommendations while preserving the ability to override them.

---

## Alternative 3: Use capability-based abstractions with recommended defaults

Monad OS can model capabilities first, then map those capabilities to provider implementations.

Examples:

- "relational database" may map to PostgreSQL, MySQL, SQLite, or another relational provider.
- "vector database" may map to Qdrant, Weaviate, pgvector, or another provider.
- "AI completion provider" may map to OpenAI, Anthropic, Google, Mistral, local Ollama, vLLM, or a custom endpoint.
- "container deployment" may map to Docker Compose, Kubernetes, Nomad, ECS, Cloud Run, Fly.io, or another platform.

### Advantages

- Strong defaults without hard lock-in.
- Better enterprise fit.
- Better future-proofing.
- Better productized service flexibility.
- Better SaaS/self-hosted path.
- Cleaner architecture.
- Better recommendation engine.
- Better migration support.

### Disadvantages

- More abstraction work.
- More adapter design.
- More testing combinations.
- More documentation burden.
- Risk of over-abstraction if implemented too early.

### Decision

Accepted.

---

# 3. Rationale

The central product thesis is that Monad OS should own:

- intent
- graph
- policy
- evidence
- recommendations
- workflow
- lifecycle traceability
- AI-safe context
- SaaS-ready synchronization

It should not be defined by one provider stack.

Agnostic design supports:

- future-proofing
- commercial flexibility
- enterprise adoption
- local-first operation
- air-gapped/private operation
- productized service delivery
- migration/modernization workflows
- marketplace packs
- policy packs
- long-term differentiation

Monad OS should be opinionated at the recommendation level, but modular at the architecture level.

The rule is:

> Recommend strongly. Couple loosely.

---

# 4. AI-Agnostic Design

Monad OS must support AI as an optional capability.

AI should enhance the system, not be required for the core to function.

## Supported AI Modes

Monad OS should eventually support:

```txt
no-ai
local-only
bring-your-own-key
bring-your-own-endpoint
hosted-provider
enterprise-gateway
air-gapped
multi-provider
```

## Possible AI Providers

Provider adapters may include:

```txt
openai
anthropic
google
mistral
cohere
openrouter
ollama
vllm
lm-studio
custom-openai-compatible
custom-http
enterprise-gateway
```

## AI Capability Types

Monad OS should model AI capabilities, not just providers.

Possible capabilities:

```txt
chat-completion
text-completion
code-completion
embedding
reranking
tool-calling
structured-output
vision
audio
long-context
local-inference
policy-evaluated-action
```

## AI Design Principles

1. Core commands must work without AI.
2. AI providers must be replaceable.
3. AI-generated changes must be policy-bound.
4. AI actions should be logged.
5. High-risk AI actions should require human approval.
6. AI context should be provider-neutral.
7. AI prompts and context packs should not assume one model.
8. Sensitive files should be excluded by policy.
9. Local/offline AI should be supported.
10. SaaS AI features should extend, not replace, local workflows.

## Example Future Configuration

```toml
[ai]
mode = "bring-your-own-endpoint"
default_provider = "local-ollama"
required_for_core = false

[ai.providers.local-ollama]
type = "ollama"
base_url = "http://localhost:11434"
capabilities = ["chat-completion", "embedding"]

[ai.policies]
allow_repo_context = true
allow_file_edits = false
require_approval_for = ["auth", "billing", "security", "infra/prod"]
```

---

# 5. Cloud-Agnostic Design

Monad OS must model cloud and infrastructure through capabilities.

## Cloud Capability Types

Potential capabilities:

```txt
compute
container
function
edge-function
static-site
object-storage
relational-database
document-database
key-value-store
queue
stream
secret-store
dns
cdn
waf
identity
container-registry
observability
logging
metrics
tracing
scheduler
workflow-engine
```

## Possible Cloud/Deployment Providers

Provider adapters may include:

```txt
local
docker-compose
kubernetes
nomad
bare-metal
aws
gcp
azure
cloudflare
digitalocean
hetzner
fly
render
railway
vercel
netlify
heroku-compatible
```

## Cloud Design Principles

1. Local development must remain first-class.
2. Cloud provider selection should be recommendation-driven.
3. Infrastructure should be generated through replaceable adapters.
4. Deployment targets should be capability-mapped.
5. Cloud cost and portability should be considered by the recommendation engine.
6. Multi-cloud and hybrid scenarios should be possible later.
7. Enterprise self-hosting should not be blocked by SaaS assumptions.
8. Cloud-specific features should be isolated behind adapters.

## Example Future Configuration

```toml
[cloud]
strategy = "local-first-cloud-portable"
default_target = "local"

[cloud.capabilities]
compute = ["container"]
object_storage = ["s3-compatible"]
secrets = ["vault-compatible"]
dns = ["cloudflare-compatible"]

[cloud.providers.local]
type = "docker-compose"

[cloud.providers.production]
type = "kubernetes"
iac = "terraform"
gitops = "argocd"
```

---

# 6. Database-Agnostic Design

Monad OS must model data storage through capabilities instead of assuming one database.

## Database Capability Types

Potential capability categories:

```txt
relational
document
key-value
cache
queue
stream
search
vector
graph
time-series
analytics
event-store
object-storage
ledger
embedded
local-dev
```

## Possible Database Providers

Provider adapters may include:

```txt
postgresql
mysql
mariadb
sqlite
mongodb
redis
valkey
dragonfly
qdrant
weaviate
pgvector
opensearch
elasticsearch
clickhouse
duckdb
neo4j
scylladb
cassandra
eventstoredb
kafka
redpanda
minio
s3-compatible
```

## Database Design Principles

1. Strong defaults are allowed.
2. PostgreSQL may be a recommended default, not a hard dependency.
3. Database categories should be capability-based.
4. Generated services should declare data needs.
5. Migration strategies should be provider-aware.
6. Data portability checks should be possible later.
7. Polyglot persistence should be supported when justified.
8. Local development databases should be easy to replace.

## Example Future Configuration

```toml
[data.primary]
capability = "relational"
provider = "postgresql"
orm = "drizzle"

[data.cache]
capability = "cache"
provider = "valkey"

[data.vector]
capability = "vector"
provider = "qdrant"

[data.analytics]
capability = "analytics"
provider = "clickhouse"
```

---

# 7. Provider Adapter Model

Monad OS should eventually define provider adapter contracts.

Conceptual interface:

```txt
ProviderAdapter
  id
  name
  category
  capabilities
  detect()
  recommend()
  generate_config()
  validate()
  explain()
  migrate_from()
  migrate_to()
  collect_evidence()
```

Provider categories may include:

```txt
ai-provider
cloud-provider
database-provider
observability-provider
ci-provider
secrets-provider
feature-flag-provider
deployment-provider
package-registry-provider
artifact-registry-provider
```

This allows Monad OS to preserve a stable product model while supporting changing providers.

---

# 8. Recommendation Engine Implications

The interactive recommendation engine must understand agnosticism.

It should ask users about:

```txt
AI preferences
local-only requirements
cloud provider preferences
cloud avoidance requirements
database preferences
expected scale
compliance needs
budget sensitivity
offline requirements
enterprise constraints
team skillset
existing infrastructure
migration constraints
```

It should produce:

```txt
recommended defaults
allowed alternatives
trade-off explanations
lock-in risks
portability notes
migration paths
future upgrade paths
```

Example recommendation style:

```txt
Recommended relational database: PostgreSQL

Reason:
  Best default for local-first SaaS-oriented systems, strong ecosystem,
  mature tooling, and extension support.

Alternatives:
  SQLite for embedded/local-only systems.
  MySQL/MariaDB for organizations already standardized on it.
  CockroachDB for distributed SQL use cases.
  Cloud-managed equivalents for hosted deployment.

Lock-in risk:
  Low to moderate if SQL and migration discipline are preserved.
```

---

# 9. Manifest Implications

`workspace.toml` should include sections for provider strategy.

Possible sections:

```toml
[ai]
mode = "no-ai"

[cloud]
strategy = "local-first"

[data]
strategy = "capability-based"

[observability]
strategy = "opentelemetry-first"

[secrets]
strategy = "provider-adapter"

[feature_flags]
strategy = "openfeature-compatible"
```

These fields should describe strategy and capability intent, not hard-code every implementation detail.

---

# 10. SaaS Implications

The future hosted Monad SaaS must not assume that every customer uses the same stack.

The SaaS control plane should be able to ingest and reason over repositories using different:

* AI providers
* clouds
* databases
* CI systems
* package managers
* build engines
* deployment targets
* observability tools
* security tools

The SaaS should normalize these through the lifecycle graph, not require uniform infrastructure.

This makes Monad OS more commercially viable.

---

# 11. Plugin and Pack Implications

Agnosticism requires a pack/plugin architecture.

Examples:

```txt
ai-provider-openai
ai-provider-anthropic
ai-provider-ollama
cloud-aws
cloud-gcp
cloud-azure
cloud-cloudflare
data-postgres
data-mongodb
data-qdrant
observability-opentelemetry
ci-github-actions
ci-gitlab
```

Policy packs and golden path packs should be able to declare provider compatibility.

Example:

```toml
[pack]
name = "multi-tenant-saas"
compatible_clouds = ["local", "aws", "gcp", "azure", "kubernetes"]
compatible_relational_databases = ["postgresql", "mysql"]
compatible_ai_modes = ["no-ai", "bring-your-own-key", "enterprise-gateway"]
```

---

# 12. Evidence Implications

Evidence should record provider context without making provider-specific evidence the only supported form.

Example evidence metadata:

```json
{
  "evidence_type": "security_scan",
  "provider": "trivy",
  "target": "container-image",
  "artifact": "services/api",
  "timestamp": "2026-06-29T00:00:00Z"
}
```

Evidence should be normalized into Monad concepts:

```txt
test-evidence
security-evidence
build-evidence
release-evidence
deployment-evidence
policy-evidence
ai-action-evidence
```

This lets Monad support different tools while maintaining one evidence model.

---

# 13. Non-Goals

This decision does not mean:

* Monad OS will support every provider in v0
* Monad OS will support every provider in v1
* all adapters must be implemented immediately
* users must manually configure everything
* defaults are forbidden
* PostgreSQL cannot be recommended
* OpenTelemetry cannot be recommended
* Fumadocs cannot be the default
* Nx cannot be used under the hood
* a hosted SaaS offering cannot provide opinionated integrations

This decision means that the architecture must not make any one provider impossible to replace later.

---

# 14. Consequences

## Positive Consequences

* Better future-proofing.
* Better enterprise fit.
* Better local-first support.
* Better self-hosted support.
* Better air-gapped support.
* Better productized service flexibility.
* Stronger competitive positioning.
* Easier migration/modernization product offerings.
* Reduced exposure to provider churn.
* Supports stronger recommendation engine.

## Negative Consequences

* More architectural complexity.
* More documentation required.
* More adapter contracts required.
* More testing combinations over time.
* Risk of building abstractions before they are needed.
* Initial implementation may be slower if overdone.

## Mitigations

* Use strong defaults for v0/v1.
* Implement only a small number of adapters initially.
* Model capabilities early, but defer full adapter implementation.
* Keep core workflows working without AI/cloud/database integrations.
* Add providers incrementally.
* Document trade-offs clearly.
* Use recommendation profiles rather than endless configuration prompts.

---

# 15. Initial Scope

## v0

v0 should only encode the principle.

It should support:

* `workspace.toml` fields expressing AI/cloud/database strategy
* recommendation output acknowledging provider choices
* no-AI local core
* local-first repo foundation

v0 should not require real provider integrations.

## v1

v1 should support:

* AI-agnostic context files
* provider-neutral docs
* basic provider strategy validation
* local-first default data/cloud assumptions
* optional provider configuration files
* generated rationale for provider choices

## Future

Future versions may support:

* AI provider adapters
* cloud provider adapters
* database provider adapters
* portability checks
* migration plans
* provider cost analysis
* SaaS provider inventory
* enterprise provider policy packs

---

# 16. Success Criteria

This decision is successful if:

1. Monad OS core works without AI.
2. Monad OS does not require one cloud.
3. Monad OS does not require one database.
4. Recommended defaults can be changed.
5. Provider choices are documented.
6. Provider lock-in risks are explainable.
7. Future adapters can be added without redesigning the system.
8. The SaaS architecture can support diverse customer environments.
9. The recommendation engine can explain trade-offs.
10. The lifecycle graph can normalize different provider implementations.

---

# 17. Final Decision Statement

Monad OS will be AI-agnostic, cloud-agnostic, and database-agnostic by design.

It will use capability-based abstractions, provider adapters, and explainable recommendations.

Defaults are allowed.

Hard lock-in is not.


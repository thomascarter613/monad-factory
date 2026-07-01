# Monad OS Documentation Index

Monad OS is an AI-agnostic, cloud-agnostic, database-agnostic SDLC Control Plane and Monorepo Operating System.

This index tracks the current pre-implementation architecture and product strategy foundation.

## Root Files

| File | Purpose |
|---|---|
| [`README.md`](../README.md) | Repository overview |
| [`AGENTS.md`](../AGENTS.md) | AI-agent operating instructions |
| [`workspace.toml`](../workspace.toml) | Canonical workspace manifest |
| [`.editorconfig`](../.editorconfig) | Editor formatting baseline |
| [`.gitignore`](../.gitignore) | Git ignore rules |
| [`scripts/check-foundation.sh`](../scripts/check-foundation.sh) | Foundation verification script |

## Product

| Document | Purpose |
|---|---|
| [`docs/product/charter.md`](product/charter.md) | Product charter |
| [`docs/product/prd.md`](product/prd.md) | Product requirements document |

## Architecture

| Document | Purpose |
|---|---|
| [`docs/architecture/technical-product-blueprint.md`](architecture/technical-product-blueprint.md) | Technical product blueprint |
| [`docs/architecture/sdlc-control-plane.md`](architecture/sdlc-control-plane.md) | SDLC control plane architecture |
| [`docs/architecture/toolchain-strategy.md`](architecture/toolchain-strategy.md) | Toolchain strategy |
| [`docs/architecture/agnosticity.md`](architecture/agnosticity.md) | AI, cloud, and database agnosticism strategy |
| [`docs/architecture/competitive-moat.md`](architecture/competitive-moat.md) | Competitive moat thesis |

## SDLC

| Document | Purpose |
|---|---|
| [`docs/sdlc/full-sdlc-coverage.md`](sdlc/full-sdlc-coverage.md) | Full SDLC coverage model |

## Governance

| Document | Purpose |
|---|---|
| [`docs/governance/principles.md`](governance/principles.md) | Governance principles |

## Strategy

| Document | Purpose |
|---|---|
| [`docs/strategy/next-steps.md`](strategy/next-steps.md) | Recommended next steps |

## Roadmap

| Document | Purpose |
|---|---|
| [`docs/roadmap/initial-implementation-sequence.md`](roadmap/initial-implementation-sequence.md) | Initial implementation sequence |
| [`docs/roadmap/v0-v1-v2-roadmap.md`](roadmap/v0-v1-v2-roadmap.md) | v0, v1, and v2 roadmap |

## Implementation

| Document | Purpose |
|---|---|
| [`docs/implementation/v0-work-packages.md`](implementation/v0-work-packages.md) | v0 implementation work packages |
| [`docs/implementation/v0-command-spec.md`](implementation/v0-command-spec.md) | v0 CLI command specification |
| [`docs/implementation/v0-data-model.md`](implementation/v0-data-model.md) | v0 logical data model |
| [`docs/implementation/v0-lifecycle-graph-schema.md`](implementation/v0-lifecycle-graph-schema.md) | v0 lifecycle graph schema |

## Decisions

| Document | Purpose |
|---|---|
| [`docs/decisions/README.md`](decisions/README.md) | ADR index |
| [`docs/decisions/decision-backlog.md`](decisions/decision-backlog.md) | Future decision backlog |

## Foundational ADRs

| ADR | Decision |
|---|---|
| [`ADR-0001`](decisions/0001-build-monad-os-as-an-sdlc-control-plane.md) | Build Monad OS as an SDLC Control Plane |
| [`ADR-0002`](decisions/0002-use-rust-for-the-cli-core.md) | Use Rust for the CLI Core |
| [`ADR-0003`](decisions/0003-use-workspace-toml-as-the-canonical-manifest.md) | Use `workspace.toml` as the Canonical Manifest |
| [`ADR-0004`](decisions/0004-wrap-native-tools-instead-of-replacing-them.md) | Wrap Native Tools Instead of Replacing Them |
| [`ADR-0005`](decisions/0005-use-fumadocs-for-documentation.md) | Use Fumadocs for Documentation |
| [`ADR-0006`](decisions/0006-design-for-ai-cloud-and-database-agnosticism.md) | Design for AI, Cloud, and Database Agnosticism |
| [`ADR-0007`](decisions/0007-support-nx-under-the-monad-wrapper.md) | Support Nx Under the Monad Wrapper |
| [`ADR-0008`](decisions/0008-support-buck2-and-pants-as-enterprise-build-backends.md) | Support Buck2 and Pants as Enterprise Build Backends |
| [`ADR-0009`](decisions/0009-keep-the-local-core-functional-without-saas.md) | Keep the Local Core Functional Without SaaS |
| [`ADR-0010`](decisions/0010-design-for-future-hosted-saas-control-plane.md) | Design for Future Hosted SaaS Control Plane |
| [`ADR-0011`](decisions/0011-use-policy-packs-for-governance-extensibility.md) | Use Policy Packs for Governance Extensibility |
| [`ADR-0012`](decisions/0012-use-packs-and-plugins-for-ecosystem-extensibility.md) | Use Packs and Plugins for Ecosystem Extensibility |
| [`ADR-0013`](decisions/0013-treat-evidence-as-a-first-class-artifact.md) | Treat Evidence as a First-Class Artifact |
| [`ADR-0014`](decisions/0014-treat-lifecycle-graph-as-the-core-product-moat.md) | Treat Lifecycle Graph as the Core Product Moat |
| [`ADR-0015`](decisions/0015-require-human-approval-gates-for-risky-ai-actions.md) | Require Human Approval Gates for Risky AI Actions |

## Current Foundation Status

The repository currently contains:

- Product foundation
- Architecture foundation
- SDLC control-plane thesis
- Governance principles
- v0-v1-v2 roadmap
- v0 implementation work packages
- v0 command specification
- v0 logical data model
- v0 lifecycle graph schema
- ADR-0001 through ADR-0015
- Foundation verification script

## Recommended Next Artifacts

After the v0 lifecycle graph schema, recommended next artifacts are:

1. `docs/implementation/v0-cli-implementation-plan.md`
2. `docs/implementation/v0-repo-structure.md`
3. `docs/implementation/v0-evidence-schema.md`
4. `docs/implementation/v0-context-pack-spec.md`
5. Initial Rust CLI scaffold

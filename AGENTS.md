# AGENTS.md

This repository is intended to become Monad OS: an AI-agnostic SDLC control plane and monorepo operating system.

AI agents, coding assistants, and automation tools working in this repository should follow these rules.

## Current Stage

The repository is currently in the pre-implementation architecture and product strategy stage.

Do not assume implementation details are finalized unless they appear in formal product, architecture, or decision documents.

## Operating Rules

1. Prefer explicit documentation over implicit assumptions.
2. Preserve architectural intent.
3. Do not remove governance, architecture, roadmap, or strategy documents without a replacement.
4. Favor additive changes during early planning.
5. Record major architectural choices as ADRs once the ADR system is created.
6. Treat AI, cloud, and database agnosticism as non-negotiable architectural principles.
7. Treat Nx, Buck2, Pants, moon, Dagger, Nix, Bun, Fumadocs, and similar tools as replaceable backends or product choices unless explicitly promoted to hard dependencies.
8. Do not introduce vendor lock-in without documenting why.
9. Do not implement SaaS-only assumptions in the local core.
10. Keep local-first operation as a first-class design requirement.

## Preferred Direction

Monad OS should expose a unified `monad` CLI.

Internal tools may be wrapped under the hood. For example, Nx may be used as a task graph/backend while the user-facing interface remains Monad.

## Documentation Expectations

When adding new concepts, update the relevant documentation under `docs/`.

When making a major decision, prepare an ADR under `docs/decisions/` or `docs/adr/` once ADR structure is formalized.


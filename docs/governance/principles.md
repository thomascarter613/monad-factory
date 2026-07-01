# Governance Principles

Monad OS should be built according to these governance principles.

## 1. Explicit over implicit

Important decisions should be recorded.

## 2. Local-first, SaaS-ready

The local core should provide real value without requiring a hosted SaaS account.

The architecture should still be designed so a future hosted control plane can sync with and extend the local core.

## 3. Agnostic by default

Avoid hard dependency on one AI provider, cloud provider, database provider, CI provider, deployment target, or task runner.

## 4. Evidence-oriented

Important lifecycle events should produce evidence.

## 5. Policy-controlled automation

Automation should be powerful but bounded by policy.

## 6. AI assistance is optional

The system should work without AI.

AI should enhance workflows, not become an unavoidable dependency.

## 7. Human approval for high-risk changes

High-risk areas should require human approval.

Examples:

- authentication
- authorization
- billing
- production infrastructure
- secrets
- compliance controls
- data migrations
- security policies


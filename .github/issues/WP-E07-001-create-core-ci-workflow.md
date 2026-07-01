---
title: "WP-E07-001: Create Core CI Workflow"
labels: "type:work-packet,area:ci,priority:p0,status:ready"
---

## Objective

Create the first GitHub Actions CI workflow.

## Tasks

- [ ] Create `.github/workflows/ci.yml`.
- [ ] Add checkout/setup steps.
- [ ] Add tool install steps.
- [ ] Run format checks.
- [ ] Run lint checks.
- [ ] Run type checks.
- [ ] Run unit tests.
- [ ] Run builds.
- [ ] Run docs checks.
- [ ] Add caching where safe.

## Acceptance Criteria

- [ ] CI workflow exists.
- [ ] CI runs root check commands.
- [ ] CI does not require secrets for baseline checks.

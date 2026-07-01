#!/usr/bin/env bash
set -euo pipefail

require_gh() {
  if ! command -v gh >/dev/null 2>&1; then
    echo "Error: GitHub CLI 'gh' is required."
    exit 1
  fi
}

upsert_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  if gh label create "$name" --color "$color" --description "$description" >/dev/null 2>&1; then
    echo "created: $name"
  else
    gh label edit "$name" --color "$color" --description "$description" >/dev/null
    echo "updated: $name"
  fi
}

require_gh

upsert_label "type:epic" "5319E7" "Large body of work containing multiple work packets"
upsert_label "type:work-packet" "1D76DB" "Issue representing one planned work packet"
upsert_label "type:task" "0E8A16" "Implementation task"

upsert_label "area:docs" "0075CA" "Documentation"
upsert_label "area:architecture" "0075CA" "Architecture and ADRs"
upsert_label "area:tooling" "0075CA" "Developer tooling"
upsert_label "area:cli" "0075CA" "monad CLI"
upsert_label "area:memory" "0075CA" "Monad Memory"
upsert_label "area:agent" "0075CA" "Agentic workflows"
upsert_label "area:policy" "0075CA" "Policy and policy-as-code"
upsert_label "area:typescript" "0075CA" "TypeScript and JavaScript"
upsert_label "area:rust" "0075CA" "Rust"
upsert_label "area:go" "0075CA" "Go"
upsert_label "area:python" "0075CA" "Python"
upsert_label "area:java" "0075CA" "Java"
upsert_label "area:infra" "0075CA" "Infrastructure"
upsert_label "area:ci" "0075CA" "CI and GitHub automation"
upsert_label "area:security" "0075CA" "Security"
upsert_label "area:contracts" "0075CA" "Contracts and schemas"
upsert_label "area:templates" "0075CA" "Templates and generation"
upsert_label "area:plugins" "0075CA" "Plugin system"
upsert_label "area:marketplace" "0075CA" "Marketplace catalog"
upsert_label "area:release" "0075CA" "Release and publishing"
upsert_label "area:nx" "0075CA" "Nx adapter"
upsert_label "area:deployment" "0075CA" "Deployment"
upsert_label "area:federation" "0075CA" "Multi-repo federation"
upsert_label "area:control-plane" "0075CA" "Hosted/self-hosted control plane"
upsert_label "area:governance" "0075CA" "Repository and organization governance"

upsert_label "priority:p0" "B60205" "Critical path"
upsert_label "priority:p1" "D93F0B" "Important"
upsert_label "priority:p2" "FBCA04" "Normal priority"

upsert_label "status:ready" "0E8A16" "Ready to work"
upsert_label "status:blocked" "B60205" "Blocked"
upsert_label "status:deferred" "C5DEF5" "Deferred"
upsert_label "status:in-progress" "FBCA04" "In progress"
upsert_label "status:review" "5319E7" "Needs review"

upsert_label "good-first-issue" "7057FF" "Good first contribution"

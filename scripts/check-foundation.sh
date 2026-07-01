#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

pass() {
  echo "OK: $1"
}

required_files=(
  ".gitignore"
  ".editorconfig"
  "README.md"
  "AGENTS.md"
  "workspace.toml"
  "scripts/check-foundation.sh"
  "docs/00-index.md"
  "docs/product/charter.md"
  "docs/product/prd.md"
  "docs/architecture/technical-product-blueprint.md"
  "docs/architecture/sdlc-control-plane.md"
  "docs/architecture/toolchain-strategy.md"
  "docs/architecture/agnosticity.md"
  "docs/architecture/competitive-moat.md"
  "docs/sdlc/full-sdlc-coverage.md"
  "docs/strategy/next-steps.md"
  "docs/governance/principles.md"
  "docs/roadmap/initial-implementation-sequence.md"
  "docs/roadmap/v0-v1-v2-roadmap.md"
  "docs/implementation/v0-work-packages.md"
  "docs/implementation/v0-command-spec.md"
  "docs/implementation/v0-data-model.md"
  "docs/implementation/v0-lifecycle-graph-schema.md"
  "docs/decisions/decision-backlog.md"
  "docs/decisions/README.md"
)

required_dirs=(
  "docs"
  "docs/product"
  "docs/architecture"
  "docs/sdlc"
  "docs/strategy"
  "docs/governance"
  "docs/roadmap"
  "docs/implementation"
  "docs/decisions"
  "scripts"
)

echo "Checking Monad OS foundation..."
echo

for dir in "${required_dirs[@]}"; do
  [[ -d "$dir" ]] || fail "Missing directory: $dir"
  pass "Directory exists: $dir"
done

echo

for file in "${required_files[@]}"; do
  [[ -f "$file" ]] || fail "Missing file: $file"
  [[ -s "$file" ]] || fail "File is empty: $file"
  pass "File exists and is non-empty: $file"
done

echo

[[ -x "scripts/check-foundation.sh" ]] || fail "scripts/check-foundation.sh is not executable"
pass "scripts/check-foundation.sh is executable"

echo

expected_adr_count=15
actual_adr_count="$(find docs/decisions -maxdepth 1 -type f -name '[0-9][0-9][0-9][0-9]-*.md' | wc -l | tr -d ' ')"

[[ "$actual_adr_count" == "$expected_adr_count" ]] || fail "Expected $expected_adr_count ADR files, found $actual_adr_count"
pass "Found $expected_adr_count ADR files"

for i in $(seq 1 "$expected_adr_count"); do
  n="$(printf "%04d" "$i")"
  if ! find docs/decisions -maxdepth 1 -type f -name "${n}-*.md" | grep -q .; then
    fail "Missing ADR number: $n"
  fi
  pass "ADR number exists: $n"
done

echo

grep -q "v0-command-spec.md" docs/00-index.md || fail "docs/00-index.md does not reference v0-command-spec.md"
pass "docs/00-index.md references v0-command-spec.md"

grep -q "v0-data-model.md" docs/00-index.md || fail "docs/00-index.md does not reference v0-data-model.md"
pass "docs/00-index.md references v0-data-model.md"

grep -q "v0-lifecycle-graph-schema.md" docs/00-index.md || fail "docs/00-index.md does not reference v0-lifecycle-graph-schema.md"
pass "docs/00-index.md references v0-lifecycle-graph-schema.md"

grep -q "monad context pack" docs/implementation/v0-command-spec.md || fail "v0 command spec does not define monad context pack"
pass "v0 command spec defines monad context pack"

grep -q "monad graph build" docs/implementation/v0-command-spec.md || fail "v0 command spec does not define monad graph build"
pass "v0 command spec defines monad graph build"

grep -q "monad policy check" docs/implementation/v0-command-spec.md || fail "v0 command spec does not define monad policy check"
pass "v0 command spec defines monad policy check"

grep -q "EvidenceBundle" docs/implementation/v0-data-model.md || fail "v0 data model does not define EvidenceBundle"
pass "v0 data model defines EvidenceBundle"

grep -q "LifecycleGraph" docs/implementation/v0-data-model.md || fail "v0 data model does not define LifecycleGraph"
pass "v0 data model defines LifecycleGraph"

grep -q "ContextPack" docs/implementation/v0-data-model.md || fail "v0 data model does not define ContextPack"
pass "v0 data model defines ContextPack"

grep -q "ApprovalGate" docs/implementation/v0-data-model.md || fail "v0 data model does not define ApprovalGate"
pass "v0 data model defines ApprovalGate"

grep -q "graph_version" docs/implementation/v0-lifecycle-graph-schema.md || fail "v0 lifecycle graph schema does not define graph_version"
pass "v0 lifecycle graph schema defines graph_version"

grep -q "GraphNode" docs/implementation/v0-lifecycle-graph-schema.md || fail "v0 lifecycle graph schema does not define GraphNode"
pass "v0 lifecycle graph schema defines GraphNode"

grep -q "GraphEdge" docs/implementation/v0-lifecycle-graph-schema.md || fail "v0 lifecycle graph schema does not define GraphEdge"
pass "v0 lifecycle graph schema defines GraphEdge"

grep -q "lifecycle-graph.json" docs/implementation/v0-lifecycle-graph-schema.md || fail "v0 lifecycle graph schema does not define lifecycle-graph.json"
pass "v0 lifecycle graph schema defines lifecycle-graph.json"

grep -q "contains" docs/implementation/v0-lifecycle-graph-schema.md || fail "v0 lifecycle graph schema does not define contains edges"
pass "v0 lifecycle graph schema defines contains edges"

grep -q "produces" docs/implementation/v0-lifecycle-graph-schema.md || fail "v0 lifecycle graph schema does not define produces edges"
pass "v0 lifecycle graph schema defines produces edges"

echo
echo "Monad OS foundation check passed."

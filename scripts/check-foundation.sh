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

expected_adr_count=0
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

echo "Monad OS foundation check passed."

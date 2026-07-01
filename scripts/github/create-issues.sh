#!/usr/bin/env bash
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "Error: GitHub CLI 'gh' is required."
  exit 1
fi

DRY_RUN="${DRY_RUN:-0}"

for file in .github/issues/*.md; do
  title="$(sed -n 's/^title: "\(.*\)"$/\1/p' "$file" | head -n 1)"
  labels="$(sed -n 's/^labels: "\(.*\)"$/\1/p' "$file" | head -n 1)"

  body="$(mktemp)"
  awk '
    BEGIN { in_frontmatter=0; seen_frontmatter=0 }
    NR == 1 && $0 == "---" { in_frontmatter=1; seen_frontmatter=1; next }
    in_frontmatter && $0 == "---" { in_frontmatter=0; next }
    !in_frontmatter && seen_frontmatter { print }
  ' "$file" > "$body"

  if [[ -z "$title" ]]; then
    echo "Skipping $file: missing title"
    rm -f "$body"
    continue
  fi

  args=(issue create --title "$title" --body-file "$body")

  if [[ -n "$labels" ]]; then
    IFS=',' read -ra label_array <<< "$labels"
    for raw_label in "${label_array[@]}"; do
      label="$(echo "$raw_label" | xargs)"
      args+=(--label "$label")
    done
  fi

  if [[ "$DRY_RUN" == "1" ]]; then
    echo "DRY RUN: gh ${args[*]}"
  else
    echo "Creating issue: $title"
    gh "${args[@]}"
  fi

  rm -f "$body"
done

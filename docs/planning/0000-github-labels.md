Run this from the root of `monad-factory`.

```bash
mkdir -p .github/issues scripts/github
```

## 1. Create canonical label config

```bash
cat > .github/labels.yml <<'EOF'
labels:
  - name: "type:epic"
    color: "5319E7"
    description: "Large body of work containing multiple work packets"
  - name: "type:work-packet"
    color: "1D76DB"
    description: "Issue representing one planned work packet"
  - name: "type:task"
    color: "0E8A16"
    description: "Implementation task"

  - name: "area:docs"
    color: "0075CA"
    description: "Documentation"
  - name: "area:architecture"
    color: "0075CA"
    description: "Architecture and ADRs"
  - name: "area:tooling"
    color: "0075CA"
    description: "Developer tooling"
  - name: "area:cli"
    color: "0075CA"
    description: "monad CLI"
  - name: "area:memory"
    color: "0075CA"
    description: "Monad Memory"
  - name: "area:agent"
    color: "0075CA"
    description: "Agentic workflows"
  - name: "area:policy"
    color: "0075CA"
    description: "Policy and policy-as-code"
  - name: "area:typescript"
    color: "0075CA"
    description: "TypeScript and JavaScript"
  - name: "area:rust"
    color: "0075CA"
    description: "Rust"
  - name: "area:go"
    color: "0075CA"
    description: "Go"
  - name: "area:python"
    color: "0075CA"
    description: "Python"
  - name: "area:java"
    color: "0075CA"
    description: "Java"
  - name: "area:infra"
    color: "0075CA"
    description: "Infrastructure"
  - name: "area:ci"
    color: "0075CA"
    description: "CI and GitHub automation"
  - name: "area:security"
    color: "0075CA"
    description: "Security"
  - name: "area:contracts"
    color: "0075CA"
    description: "Contracts and schemas"
  - name: "area:templates"
    color: "0075CA"
    description: "Templates and generation"
  - name: "area:plugins"
    color: "0075CA"
    description: "Plugin system"
  - name: "area:marketplace"
    color: "0075CA"
    description: "Marketplace catalog"
  - name: "area:release"
    color: "0075CA"
    description: "Release and publishing"
  - name: "area:nx"
    color: "0075CA"
    description: "Nx adapter"
  - name: "area:deployment"
    color: "0075CA"
    description: "Deployment"
  - name: "area:federation"
    color: "0075CA"
    description: "Multi-repo federation"
  - name: "area:control-plane"
    color: "0075CA"
    description: "Hosted/self-hosted control plane"
  - name: "area:governance"
    color: "0075CA"
    description: "Repository and organization governance"

  - name: "priority:p0"
    color: "B60205"
    description: "Critical path"
  - name: "priority:p1"
    color: "D93F0B"
    description: "Important"
  - name: "priority:p2"
    color: "FBCA04"
    description: "Normal priority"

  - name: "status:ready"
    color: "0E8A16"
    description: "Ready to work"
  - name: "status:blocked"
    color: "B60205"
    description: "Blocked"
  - name: "status:deferred"
    color: "C5DEF5"
    description: "Deferred"
  - name: "status:in-progress"
    color: "FBCA04"
    description: "In progress"
  - name: "status:review"
    color: "5319E7"
    description: "Needs review"

  - name: "good-first-issue"
    color: "7057FF"
    description: "Good first contribution"
EOF
```

## 2. Create label creation script

```bash
cat > scripts/github/create-labels.sh <<'EOF'
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
EOF

chmod +x scripts/github/create-labels.sh
```

## 3. Generate first batch of issue files

This creates the first planning/foundation batch from the canonical v1 scope document.

```bash
cat > scripts/github/generate-initial-issues.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

mkdir -p .github/issues

write_issue() {
  local file="$1"
  local title="$2"
  local labels="$3"
  cat > ".github/issues/$file" <<ISSUE
---
title: "$title"
labels: "$labels"
---

ISSUE
  cat >> ".github/issues/$file"
}

write_issue "WP-E00-001-finalize-maximal-functional-v1-scope-document.md" \
"WP-E00-001: Finalize Maximal Functional v1 Scope Document" \
"type:work-packet,area:docs,priority:p0,status:ready" <<'EOF'
## Objective

Commit and maintain the canonical maximal functional v1 scope document for Monad Factory.

## Tasks

- [ ] Confirm `docs/product/v1-maximal-functional-scope-and-delivery-plan.md` exists.
- [ ] Confirm YAML frontmatter is present.
- [ ] Confirm document uses maximal functional v1 framing.
- [ ] Confirm document defines product identity.
- [ ] Confirm document defines target user.
- [ ] Confirm document defines all core v1 capabilities.
- [ ] Confirm document defines usage boundaries.
- [ ] Confirm document includes v1 Definition of Done.
- [ ] Confirm document includes epics, work packets, tasks, and subtasks.

## Acceptance Criteria

- [ ] Scope document exists at the canonical repo path.
- [ ] Document is marked `status: approved`.
- [ ] Document is marked `canonical: true`.
- [ ] Document can be used as the source for GitHub issue generation.
EOF

write_issue "WP-E00-002-define-github-issue-taxonomy.md" \
"WP-E00-002: Define GitHub Issue Taxonomy" \
"type:work-packet,area:docs,area:ci,priority:p0,status:ready" <<'EOF'
## Objective

Define the GitHub labels, issue naming model, and issue template structure for the v1 implementation plan.

## Tasks

- [ ] Create `.github/labels.yml`.
- [ ] Create label creation script.
- [ ] Define type labels.
- [ ] Define area labels.
- [ ] Define priority labels.
- [ ] Define status labels.
- [ ] Define issue naming convention.
- [ ] Define epic issue format.
- [ ] Define work-packet issue format.
- [ ] Define task checklist format.

## Acceptance Criteria

- [ ] Label taxonomy exists.
- [ ] Label creation script exists.
- [ ] Work-packet issues can be generated consistently.
- [ ] Issue naming convention is documented.
EOF

write_issue "WP-E01-001-create-documentation-skeleton.md" \
"WP-E01-001: Create Documentation Skeleton" \
"type:work-packet,area:docs,priority:p0,status:ready" <<'EOF'
## Objective

Create the repository documentation structure.

## Tasks

- [ ] Create `docs/00-index.md`.
- [ ] Create `docs/product/`.
- [ ] Create `docs/planning/`.
- [ ] Create `docs/architecture/`.
- [ ] Create `docs/adr/`.
- [ ] Create `docs/ai/`.
- [ ] Create `docs/memory/`.
- [ ] Create `docs/agents/`.
- [ ] Create `docs/policy/`.
- [ ] Create `docs/deployment/`.
- [ ] Create `docs/publishing/`.
- [ ] Create `docs/getting-started/`.
- [ ] Create `docs/tutorials/`.
- [ ] Create `docs/runbooks/`.
- [ ] Create `docs/marketplace/`.
- [ ] Create `docs/federation/`.
- [ ] Create `docs/hosted-control-plane/`.
- [ ] Add README files where useful.

## Acceptance Criteria

- [ ] Documentation tree exists.
- [ ] `docs/00-index.md` links to major documentation areas.
- [ ] Meaningful Markdown files use YAML frontmatter.
EOF

write_issue "WP-E01-002-add-documentation-standards.md" \
"WP-E01-002: Add Documentation Standards" \
"type:work-packet,area:docs,priority:p0,status:ready" <<'EOF'
## Objective

Define documentation rules for durable, reviewable, AI-friendly repository knowledge.

## Tasks

- [ ] Define Markdown frontmatter schema.
- [ ] Define required frontmatter fields.
- [ ] Define optional frontmatter fields.
- [ ] Define canonical document markers.
- [ ] Define document naming rules.
- [ ] Define documentation ownership expectations.
- [ ] Add documentation review checklist.
- [ ] Add docs lint/check command plan.

## Acceptance Criteria

- [ ] Documentation standards exist.
- [ ] Frontmatter rules are documented.
- [ ] New docs have clear authoring expectations.
EOF

write_issue "WP-E02-001-create-adr-system.md" \
"WP-E02-001: Create ADR System" \
"type:work-packet,area:docs,area:architecture,priority:p0,status:ready" <<'EOF'
## Objective

Create the Architecture Decision Record system for Monad Factory.

## Tasks

- [ ] Create `docs/adr/0000-adr-template.md`.
- [ ] Include frontmatter fields.
- [ ] Include status section.
- [ ] Include context section.
- [ ] Include decision section.
- [ ] Include consequences section.
- [ ] Include verification section.
- [ ] Create `docs/adr/00-index.md`.
- [ ] Add ADR contribution process.
- [ ] Add ADR review checklist.

## Acceptance Criteria

- [ ] ADR template exists.
- [ ] ADR index exists.
- [ ] ADR files use frontmatter.
- [ ] ADR process is documented.
EOF

write_issue "WP-E02-002-create-initial-adrs.md" \
"WP-E02-002: Create Initial ADRs" \
"type:work-packet,area:architecture,area:docs,priority:p0,status:ready" <<'EOF'
## Objective

Create the initial ADR set for maximal functional v1.

## Tasks

- [ ] ADR-0001: Use a maximal functional polyglot product-factory monorepo.
- [ ] ADR-0002: Use `monad` as public repo control plane.
- [ ] ADR-0003: Use `mise` for toolchain management.
- [ ] ADR-0004: Use native language toolchains under root orchestration.
- [ ] ADR-0005: Use Rust for the `monad` CLI.
- [ ] ADR-0006: Include LLM-agnostic Monad Memory.
- [ ] ADR-0007: Keep AI memory local-first, inspectable, and policy-governed.
- [ ] ADR-0008: Use generated AI tool adapters.
- [ ] ADR-0009: Include daemon mode.
- [ ] ADR-0010: Include Nx as graph/cache/affected-task adapter.
- [ ] ADR-0011: Keep `monad` commands stable when underlying tools change.
- [ ] ADR-0012: Treat handoffs and context packs as first-class artifacts.
- [ ] ADR-0013: Include policy-as-code.
- [ ] ADR-0014: Include template/plugin/marketplace systems.
- [ ] ADR-0015: Include Kubernetes/cloud/advanced DevOps integration paths.
- [ ] ADR-0016: Include multi-repo and organization governance foundations.
- [ ] ADR-0017: Include hosted/self-hosted control-plane architecture.

## Acceptance Criteria

- [ ] Initial ADR set exists.
- [ ] ADRs match maximal functional v1 scope.
- [ ] ADR index references all initial ADRs.
EOF

write_issue "WP-E03-001-create-root-governance-files.md" \
"WP-E03-001: Create Root Governance Files" \
"type:work-packet,area:docs,area:governance,priority:p0,status:ready" <<'EOF'
## Objective

Create the root governance files for the repository.

## Tasks

- [ ] Create `README.md`.
- [ ] Create `LICENSE`.
- [ ] Create `SECURITY.md`.
- [ ] Create `CONTRIBUTING.md`.
- [ ] Create `CODE_OF_CONDUCT.md`.
- [ ] Create `CODEOWNERS`.
- [ ] Create `AGENTS.md`.
- [ ] Explain maximal functional v1 scope in README.
- [ ] Explain AI assistant expectations in `AGENTS.md`.
- [ ] Link to Monad Memory docs.
- [ ] Link to agent safety rules.

## Acceptance Criteria

- [ ] Root governance files exist.
- [ ] README clearly communicates product purpose.
- [ ] AI usage and governance are documented.
EOF

write_issue "WP-E03-002-create-base-directory-structure.md" \
"WP-E03-002: Create Base Directory Structure" \
"type:work-packet,area:docs,area:tooling,priority:p0,status:ready" <<'EOF'
## Objective

Create the base directory structure for the maximal functional v1 platform.

## Tasks

- [ ] Create app directories.
- [ ] Create service directories.
- [ ] Create package directories.
- [ ] Create Rust crate directories.
- [ ] Create contract directories.
- [ ] Create docs directories.
- [ ] Create policy directories.
- [ ] Create template directories.
- [ ] Create plugin directories.
- [ ] Create marketplace directories.
- [ ] Create infrastructure directories.
- [ ] Create test directories.
- [ ] Add `.gitkeep` files where needed.
- [ ] Document directory purpose.

## Acceptance Criteria

- [ ] Base directory tree exists.
- [ ] Empty directories contain `.gitkeep` where needed.
- [ ] Directory purpose is documented.
EOF

write_issue "WP-E04-001-add-tool-version-management-with-mise.md" \
"WP-E04-001: Add Tool Version Management with mise" \
"type:work-packet,area:tooling,priority:p0,status:ready" <<'EOF'
## Objective

Add reproducible project-level tool version management.

## Tasks

- [ ] Create `mise.toml`.
- [ ] Pin Bun.
- [ ] Pin Node if needed.
- [ ] Pin Rust.
- [ ] Pin Go.
- [ ] Pin Python.
- [ ] Pin Java.
- [ ] Pin Gradle.
- [ ] Pin Terraform/OpenTofu.
- [ ] Pin auxiliary tools where practical.
- [ ] Add setup instructions.
- [ ] Add toolchain verification command.

## Acceptance Criteria

- [ ] `mise.toml` exists.
- [ ] Required tool versions are pinned.
- [ ] Setup docs explain how to install tools.
EOF

write_issue "WP-E04-002-add-bun-workspace.md" \
"WP-E04-002: Add Bun Workspace" \
"type:work-packet,area:typescript,area:tooling,priority:p0,status:ready" <<'EOF'
## Objective

Create the root Bun workspace for TypeScript and JavaScript packages.

## Tasks

- [ ] Create root `package.json`.
- [ ] Add workspace definitions.
- [ ] Add root scripts.
- [ ] Add package manager field.
- [ ] Initialize lockfile.
- [ ] Add root TypeScript configuration.
- [ ] Add workspace package references.

## Acceptance Criteria

- [ ] Bun workspace exists.
- [ ] Root package scripts exist.
- [ ] Bun install works.
EOF

write_issue "WP-E04-003-add-formatting-and-hooks.md" \
"WP-E04-003: Add Formatting and Hooks" \
"type:work-packet,area:tooling,priority:p0,status:ready" <<'EOF'
## Objective

Add formatting, Git metadata, and Git hook configuration.

## Tasks

- [ ] Add `biome.json`.
- [ ] Add `lefthook.yml`.
- [ ] Add `.editorconfig`.
- [ ] Add `.gitattributes`.
- [ ] Add `.gitignore`.
- [ ] Add commit/check conventions.

## Acceptance Criteria

- [ ] Formatting config exists.
- [ ] Git hooks config exists.
- [ ] Root ignored files are correct.
- [ ] Formatting checks can run.
EOF

write_issue "WP-E05-001-add-frontmatter-check.md" \
"WP-E05-001: Add Frontmatter Check" \
"type:work-packet,area:docs,priority:p0,status:ready" <<'EOF'
## Objective

Add automated validation for meaningful Markdown document frontmatter.

## Tasks

- [ ] Create frontmatter validation script.
- [ ] Define required frontmatter fields.
- [ ] Exclude generated files where appropriate.
- [ ] Add check to root task.
- [ ] Add check to CI.

## Acceptance Criteria

- [ ] Frontmatter check exists.
- [ ] CI can run frontmatter check.
- [ ] Meaningful docs include frontmatter.
EOF

write_issue "WP-E06-001-configure-moon-workspace.md" \
"WP-E06-001: Configure moon Workspace" \
"type:work-packet,area:tooling,priority:p0,status:ready" <<'EOF'
## Objective

Configure `moon` as the default root task orchestrator.

## Tasks

- [ ] Create `moon.yml`.
- [ ] Define root tasks.
- [ ] Define task inputs.
- [ ] Define task outputs where useful.
- [ ] Define project discovery.
- [ ] Add `format` task.
- [ ] Add `lint` task.
- [ ] Add `test` task.
- [ ] Add `build` task.
- [ ] Add `check` task.
- [ ] Add `doctor` task.

## Acceptance Criteria

- [ ] Root moon checks work.
- [ ] Task names are documented.
- [ ] Task names are consistent across languages.
EOF

write_issue "WP-E07-001-create-core-ci-workflow.md" \
"WP-E07-001: Create Core CI Workflow" \
"type:work-packet,area:ci,priority:p0,status:ready" <<'EOF'
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
EOF

echo "Generated initial issue files in .github/issues/"
EOF

chmod +x scripts/github/generate-initial-issues.sh
./scripts/github/generate-initial-issues.sh
```

## 4. Create issue publishing script

```bash
cat > scripts/github/create-issues.sh <<'EOF'
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
EOF

chmod +x scripts/github/create-issues.sh
```

## 5. Verify files

```bash
find .github scripts/github -maxdepth 3 -type f | sort
```

## 6. Commit

```bash
git add .github/labels.yml .github/issues scripts/github
git commit -m "chore: add github planning automation"
git push
```

## 7. Create labels and issues on GitHub

Make sure you are authenticated:

```bash
gh auth status
```

Create or update labels:

```bash
./scripts/github/create-labels.sh
```

Dry-run issue creation first:

```bash
DRY_RUN=1 ./scripts/github/create-issues.sh
```

Then create the issues:

```bash
./scripts/github/create-issues.sh
```

This gives you the first GitHub issue batch for the canonical v1 plan.

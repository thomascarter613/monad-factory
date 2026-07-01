#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

root = Path.cwd()

required_files = [
    ".github/workflows/ci.yml",
    "package.json",
    "bun.lock",
]

missing = [path for path in required_files if not (root / path).is_file()]
if missing:
    print("Missing required CI files:")
    for path in missing:
        print(f"  - {path}")
    sys.exit(1)

workflow = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8")

required_workflow_fragments = [
    "name: CI",
    "pull_request:",
    "push:",
    "branches:",
    "- main",
    "permissions:",
    "contents: read",
    "concurrency:",
    "runs-on: ubuntu-latest",
    "timeout-minutes: 15",
    "uses: actions/checkout@v5",
    "uses: oven-sh/setup-bun@v2",
    "bun-version: 1.3.14",
    "bun install --frozen-lockfile",
    "bun run check:ci",
    "bun run check:foundation",
    "bun run check:toolchain",
    "bun run check:rust",
        "bun run doctor:ci",
        "bun run typecheck",
    "bun run format:check",
    "bun run moon:version",
    "bun run check",
]

missing_fragments = [
    fragment for fragment in required_workflow_fragments if fragment not in workflow
]

if missing_fragments:
    print("CI workflow is missing required fragments:")
    for fragment in missing_fragments:
        print(f"  - {fragment}")
    sys.exit(1)

package = json.loads((root / "package.json").read_text(encoding="utf-8"))
scripts = package.get("scripts", {})

required_scripts = [
    "check:ci",
    "ci:local",
    "check",
    "check:foundation",
    "check:toolchain",
    "format:check",
    "moon:version",
    "check:rust",
        "doctor:ci",
        "typecheck",
]

missing_scripts = [script for script in required_scripts if script not in scripts]
if missing_scripts:
    print("package.json is missing required CI scripts:")
    for script in missing_scripts:
        print(f"  - {script}")
    sys.exit(1)

print("CI workflow files present and structurally valid")
PY

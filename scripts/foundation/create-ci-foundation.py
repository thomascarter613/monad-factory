from __future__ import annotations

import json
import os
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def clean(content: str) -> str:
    value = textwrap.dedent(content).lstrip()
    if not value.endswith("\n"):
        value += "\n"
    return value


def write_file(relative_path: str, content: str, mode: int | None = None) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean(content), encoding="utf-8")
    if mode is not None:
        os.chmod(path, mode)
    print(f"wrote {relative_path}")


def update_package_json() -> None:
    path = ROOT / "package.json"
    package = json.loads(path.read_text(encoding="utf-8"))

    scripts = package.setdefault("scripts", {})
    scripts["check:ci"] = "bash scripts/check-ci.sh"
    scripts["ci:local"] = "bun run check:ci && bun run check"

    path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    print("updated package.json")


write_file(
    ".github/workflows/ci.yml",
    """
    name: CI

    on:
      pull_request:
      push:
        branches:
          - main

    permissions:
      contents: read

    concurrency:
      group: ${{ github.workflow }}-${{ github.ref }}
      cancel-in-progress: true

    jobs:
      foundation:
        name: Foundation and root toolchain
        runs-on: ubuntu-latest
        timeout-minutes: 15

        steps:
          - name: Checkout repository
            uses: actions/checkout@v5

          - name: Set up Bun
            uses: oven-sh/setup-bun@v2
            with:
              bun-version: 1.3.14

          - name: Print runtime versions
            run: |
              bun --version
              node --version

          - name: Install dependencies
            run: bun install --frozen-lockfile

          - name: Validate CI workflow files
            run: bun run check:ci

          - name: Validate foundation
            run: bun run check:foundation

          - name: Validate root toolchain files
            run: bun run check:toolchain

          - name: TypeScript configuration check
            run: bun run typecheck

          - name: Biome formatting and lint check
            run: bun run format:check

          - name: moon availability check
            run: bun run moon:version

          - name: Aggregate root check
            run: bun run check
    """,
)

write_file(
    "scripts/check-ci.sh",
    """
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
    """,
    mode=0o755,
)

update_package_json()

print("CI foundation generated")

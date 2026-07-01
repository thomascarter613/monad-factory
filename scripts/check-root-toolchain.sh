#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

root = Path.cwd()

required_files = [
    "mise.toml",
    "package.json",
    "tsconfig.base.json",
    "biome.json",
    "lefthook.yml",
    ".moon/workspace.yml",
    ".moon/toolchains.yml",
    "moon.yml",
    "scripts/check-root-toolchain.sh",
    "scripts/check-foundation.sh",
    "docs/product/v1-maximal-functional-scope-and-delivery-plan.md",
]

missing = [path for path in required_files if not (root / path).is_file()]
if missing:
    print("Missing required root toolchain files:")
    for path in missing:
        print(f"  - {path}")
    sys.exit(1)

for path in ["package.json", "tsconfig.base.json", "biome.json"]:
    with (root / path).open("r", encoding="utf-8") as handle:
        json.load(handle)

with (root / "mise.toml").open("rb") as handle:
    tomllib.load(handle)

for path in ["lefthook.yml", ".moon/workspace.yml", ".moon/toolchains.yml", "moon.yml"]:
    content = (root / path).read_text(encoding="utf-8").strip()
    if not content:
        print(f"{path} is empty")
        sys.exit(1)

package = json.loads((root / "package.json").read_text(encoding="utf-8"))

required_scripts = [
    "check",
    "check:foundation",
    "check:toolchain",
    "doctor",
    "format:check",
    "format:write",
    "hooks:install",
    "lint",
    "moon:check",
    "moon:version",
    "typecheck",
]

scripts = package.get("scripts", {})
missing_scripts = [script for script in required_scripts if script not in scripts]
if missing_scripts:
    print("Missing package.json scripts:")
    for script in missing_scripts:
        print(f"  - {script}")
    sys.exit(1)

required_dev_dependencies = [
    "@biomejs/biome",
    "@moonrepo/cli",
    "lefthook",
    "typescript",
]

dev_dependencies = package.get("devDependencies", {})
missing_dev_dependencies = [
    dependency for dependency in required_dev_dependencies if dependency not in dev_dependencies
]
if missing_dev_dependencies:
    print("Missing package.json devDependencies:")
    for dependency in missing_dev_dependencies:
        print(f"  - {dependency}")
    sys.exit(1)

print("root toolchain files present and parseable")
PY

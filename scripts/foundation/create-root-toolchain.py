from __future__ import annotations

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


write_file(
    "mise.toml",
    """
    # Monad Factory root toolchain manifest.
    #
    # This file establishes the root development toolchain for the maximal
    # functional v1 foundation. It does not narrow the approved v1 scope.
    #
    # mise manages the language/runtime versions.
    # Bun manages the root JavaScript/TypeScript workspace.
    # moon provides the repo task/project orchestration layer.

    [tools]
    node = "24.18.0"
    bun = "1.3.14"
    rust = "stable"
    go = "1.24"
    python = "3.13"
    java = "temurin-21"

    [tasks.check]
    description = "Run root validation checks."
    run = "bun run check"

    [tasks.format]
    description = "Check root formatting."
    run = "bun run format:check"

    [tasks.hooks]
    description = "Install repository Git hooks."
    run = "bun run hooks:install"
    """,
)

write_file(
    "package.json",
    """
    {
      "name": "monad-factory",
      "version": "0.0.0",
      "private": true,
      "description": "Maximal functional, local-first, polyglot, AI-ready, governance-grade monorepo product-factory platform.",
      "license": "MIT",
      "type": "module",
      "packageManager": "bun@1.3.14",
      "workspaces": [
        "apps/*",
        "packages/*",
        "services/*",
        "templates/*"
      ],
      "scripts": {
        "check": "bun run check:foundation && bun run check:toolchain && bun run format:check",
        "check:foundation": "bash scripts/check-foundation.sh",
        "check:toolchain": "bash scripts/check-root-toolchain.sh",
        "doctor": "bun run check",
        "format:check": "biome check .",
        "format:write": "biome check --write .",
        "hooks:install": "lefthook install",
        "lint": "biome lint .",
        "moon:check": "moon run repo:check",
        "moon:version": "moon --version",
        "typecheck": "tsc --showConfig --project tsconfig.base.json > /dev/null"
      },
      "devDependencies": {
        "@biomejs/biome": "^2.3.11",
        "@moonrepo/cli": "^2.2.5",
        "lefthook": "^1.13.0",
        "typescript": "^5.9.0"
      },
      "engines": {
        "bun": ">=1.3.14",
        "node": ">=24.18.0"
      }
    }
    """,
)

write_file(
    "tsconfig.base.json",
    """
    {
      "compilerOptions": {
        "allowSyntheticDefaultImports": true,
        "composite": false,
        "declaration": true,
        "declarationMap": true,
        "esModuleInterop": true,
        "exactOptionalPropertyTypes": true,
        "forceConsistentCasingInFileNames": true,
        "isolatedModules": true,
        "lib": [
          "ES2024",
          "DOM",
          "DOM.Iterable"
        ],
        "module": "ESNext",
        "moduleDetection": "force",
        "moduleResolution": "Bundler",
        "noEmit": true,
        "noFallthroughCasesInSwitch": true,
        "noImplicitOverride": true,
        "noImplicitReturns": true,
        "noUncheckedIndexedAccess": true,
        "resolveJsonModule": true,
        "skipLibCheck": true,
        "strict": true,
        "target": "ES2024",
        "verbatimModuleSyntax": true
      },
      "files": []
    }
    """,
)

write_file(
    "biome.json",
    """
    {
      "$schema": "https://biomejs.dev/schemas/2.3.11/schema.json",
      "root": true,
      "vcs": {
        "enabled": true,
        "clientKind": "git",
        "useIgnoreFile": true
      },
      "files": {
        "ignoreUnknown": true,
        "includes": [
          "**/*.{js,cjs,mjs,jsx,ts,tsx,json,jsonc,css,graphql,gql}",
          "!**/.git",
          "!**/.moon/cache",
          "!**/.moon/temp",
          "!**/node_modules",
          "!**/dist",
          "!**/build",
          "!**/coverage",
          "!**/.next",
          "!**/.turbo"
        ]
      },
      "formatter": {
        "enabled": true,
        "formatWithErrors": false,
        "indentStyle": "space",
        "indentWidth": 2,
        "lineWidth": 100
      },
      "linter": {
        "enabled": true,
        "rules": {
          "recommended": true
        }
      },
      "javascript": {
        "formatter": {
          "quoteStyle": "double",
          "semicolons": "always",
          "trailingCommas": "all"
        }
      },
      "json": {
        "formatter": {
          "trailingCommas": "none"
        }
      },
      "assist": {
        "actions": {
          "source": {
            "organizeImports": "on"
          }
        }
      }
    }
    """,
)

write_file(
    "lefthook.yml",
    """
    # Monad Factory Git hooks.
    #
    # Hooks are intentionally conservative at this stage:
    # - root file validation
    # - foundation validation
    # - Biome formatting/lint checks for supported file types
    #
    # Heavier language-specific checks are added as real projects/services are
    # implemented under apps/, packages/, services/, crates/, and infra/.

    pre-commit:
      parallel: false
      commands:
        root-toolchain:
          run: bash scripts/check-root-toolchain.sh
        biome:
          run: bun run format:check

    pre-push:
      parallel: false
      commands:
        foundation:
          run: bun run check:foundation
        root-check:
          run: bun run check:toolchain
    """,
)

write_file(
    ".moon/workspace.yml",
    """
    # Monad Factory moon workspace.
    #
    # The root repository is modeled as the `repo` project so root governance,
    # formatting, validation, and orchestration tasks can be invoked through moon.
    #
    # Product/application/service projects will become real moon projects as
    # they move from directory skeletons to implemented packages.

    projects:
      globs:
        - "apps/*"
        - "packages/*"
        - "services/*"
        - "crates/*"
      sources:
        repo: "."
    """,
)

write_file(
    ".moon/toolchains.yml",
    """
    # Monad Factory moon toolchains.
    #
    # JavaScript and TypeScript are enabled now because the root control plane
    # uses Bun, Biome, Lefthook, and TypeScript config.
    #
    # Rust, Go, Python, and Java implementation toolchain details will be
    # expanded when the corresponding v1 service/crate foundations are created.

    javascript:
      packageManager: "bun"

    typescript: {}

    node: {}

    bun: {}
    """,
)

write_file(
    "moon.yml",
    """
    # Root moon project configuration.
    #
    # Project id: repo
    # Purpose: root governance, validation, and control-plane orchestration.

    id: "repo"

    tags:
      - "root"
      - "governance"
      - "control-plane"
      - "toolchain"

    tasks:
      check:
        command: "bun run check"
        options:
          cache: false

      check-foundation:
        command: "bun run check:foundation"
        options:
          cache: false

      check-toolchain:
        command: "bun run check:toolchain"
        options:
          cache: false

      format:
        command: "bun run format:check"
        options:
          cache: false

      format-write:
        command: "bun run format:write"
        options:
          cache: false

      lint:
        command: "bun run lint"
        options:
          cache: false

      typecheck:
        command: "bun run typecheck"
        options:
          cache: false
    """,
)

write_file(
    "scripts/check-root-toolchain.sh",
    """
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
    """,
    mode=0o755,
)

print("root toolchain foundation generated")

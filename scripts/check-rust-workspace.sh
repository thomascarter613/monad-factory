#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

root = Path.cwd()

required_files = [
    "Cargo.toml",
    "Cargo.lock",
    "rust-toolchain.toml",
    "rustfmt.toml",
    ".cargo/config.toml",
    "crates/monad-core/Cargo.toml",
    "crates/monad-core/src/lib.rs",
    "crates/monad-cli/Cargo.toml",
    "crates/monad-cli/src/main.rs",
]

required_crates = [
    "monad-agent",
    "monad-cli",
    "monad-config",
    "monad-context",
    "monad-core",
    "monad-deploy",
    "monad-marketplace",
    "monad-memory",
    "monad-nx-adapter",
    "monad-plugin",
    "monad-policy",
    "monad-template",
]

missing_files = [path for path in required_files if not (root / path).is_file()]
if missing_files:
    print("Missing required Rust workspace files:")
    for path in missing_files:
        print(f"  - {path}")
    sys.exit(1)

for crate in required_crates:
    crate_root = root / "crates" / crate
    cargo_toml = crate_root / "Cargo.toml"
    if not cargo_toml.is_file():
        print(f"Missing Cargo.toml for crate: {crate}")
        sys.exit(1)

    data = tomllib.loads(cargo_toml.read_text(encoding="utf-8"))
    package_name = data.get("package", {}).get("name")
    if package_name != crate:
        print(f"Crate {crate} has unexpected package name: {package_name}")
        sys.exit(1)

workspace = tomllib.loads((root / "Cargo.toml").read_text(encoding="utf-8"))
members = set(workspace.get("workspace", {}).get("members", []))

expected_members = {f"crates/{crate}" for crate in required_crates}
missing_members = sorted(expected_members - members)

if missing_members:
    print("Cargo workspace is missing members:")
    for member in missing_members:
        print(f"  - {member}")
    sys.exit(1)

print("Rust workspace files present and structurally valid")
PY

cargo fmt --all -- --check
cargo check --workspace --all-targets
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
cargo run -p monad-cli -- help >/dev/null
cargo run -p monad-cli -- version >/dev/null
cargo run -p monad-cli -- info >/dev/null

echo "Rust workspace checks passed"

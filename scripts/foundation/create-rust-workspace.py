from __future__ import annotations

import json
import os
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CRATES = [
    {
        "dir": "monad-core",
        "kind": "lib",
        "package": "monad-core",
        "crate": "monad_core",
        "description": "Core domain primitives and shared runtime contracts for Monad Factory.",
    },
    {
        "dir": "monad-config",
        "kind": "lib",
        "package": "monad-config",
        "crate": "monad_config",
        "description": "Configuration loading, validation, and normalization for Monad Factory.",
    },
    {
        "dir": "monad-context",
        "kind": "lib",
        "package": "monad-context",
        "crate": "monad_context",
        "description": "Context pack, handoff, and AI-tool export primitives for Monad Factory.",
    },
    {
        "dir": "monad-memory",
        "kind": "lib",
        "package": "monad-memory",
        "crate": "monad_memory",
        "description": "Local-first memory abstractions for Monad Memory.",
    },
    {
        "dir": "monad-policy",
        "kind": "lib",
        "package": "monad-policy",
        "crate": "monad_policy",
        "description": "Policy-as-code interfaces and governance checks for Monad Factory.",
    },
    {
        "dir": "monad-template",
        "kind": "lib",
        "package": "monad-template",
        "crate": "monad_template",
        "description": "Template generation primitives for Monad Factory.",
    },
    {
        "dir": "monad-plugin",
        "kind": "lib",
        "package": "monad-plugin",
        "crate": "monad_plugin",
        "description": "Plugin system contracts for Monad Factory.",
    },
    {
        "dir": "monad-deploy",
        "kind": "lib",
        "package": "monad-deploy",
        "crate": "monad_deploy",
        "description": "Deployment integration primitives for Docker, Kubernetes, Nomad, Helm, and OpenTofu paths.",
    },
    {
        "dir": "monad-agent",
        "kind": "lib",
        "package": "monad-agent",
        "crate": "monad_agent",
        "description": "Agent workflow primitives for governed AI-assisted development.",
    },
    {
        "dir": "monad-nx-adapter",
        "kind": "lib",
        "package": "monad-nx-adapter",
        "crate": "monad_nx_adapter",
        "description": "Nx graph, affected-task, and cache adapter primitives for Monad Factory.",
    },
    {
        "dir": "monad-marketplace",
        "kind": "lib",
        "package": "monad-marketplace",
        "crate": "monad_marketplace",
        "description": "Marketplace catalog, manifest, and trust foundation primitives.",
    },
    {
        "dir": "monad-cli",
        "kind": "bin",
        "package": "monad-cli",
        "crate": "monad_cli",
        "description": "Public monad command-line interface.",
    },
]


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


def remove_file(relative_path: str) -> None:
    path = ROOT / relative_path
    if path.exists():
        path.unlink()
        print(f"removed {relative_path}")


def update_package_json() -> None:
    path = ROOT / "package.json"
    package = json.loads(path.read_text(encoding="utf-8"))

    scripts = package.setdefault("scripts", {})

    scripts["check:rust"] = "bash scripts/check-rust-workspace.sh"
    scripts["rust:check"] = "cargo check --workspace --all-targets"
    scripts["rust:fmt"] = "cargo fmt --all"
    scripts["rust:fmt:check"] = "cargo fmt --all -- --check"
    scripts["rust:clippy"] = "cargo clippy --workspace --all-targets -- -D warnings"
    scripts["rust:test"] = "cargo test --workspace --all-targets"
    scripts["monad:help"] = "cargo run -p monad-cli -- help"
    scripts["monad:version"] = "cargo run -p monad-cli -- version"

    scripts["check"] = (
        "bun run check:foundation && "
        "bun run check:toolchain && "
        "bun run check:ci && "
        "bun run check:github-planning && "
        "bun run check:rust && "
        "bun run doctor:ci && "
        "bun run format:check"
    )

    path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    print("updated package.json")


def update_doctor() -> None:
    path = ROOT / "scripts" / "doctor.py"
    text = path.read_text(encoding="utf-8")

    extra_files = [
        '"Cargo.toml",',
        '"Cargo.lock",',
        '"rust-toolchain.toml",',
        '"rustfmt.toml",',
        '".cargo/config.toml",',
        '"scripts/check-rust-workspace.sh",',
    ]

    for item in reversed(extra_files):
        if item not in text:
            text = text.replace(
                '"scripts/github/check-github-planning.py",',
                f'"scripts/github/check-github-planning.py",\n                {item}',
            )

    if '"cargo": ["cargo", "--version"],' not in text:
        text = text.replace(
            '"python3": ["python3", "--version"],',
            '"python3": ["python3", "--version"],\n                "cargo": ["cargo", "--version"],\n                "rustc": ["rustc", "--version"],',
        )

    if '("Rust workspace", ["bash", "scripts/check-rust-workspace.sh"]),' not in text:
        text = text.replace(
            '("GitHub planning", ["python3", "scripts/github/check-github-planning.py"]),',
            '("GitHub planning", ["python3", "scripts/github/check-github-planning.py"]),\n                ("Rust workspace", ["bash", "scripts/check-rust-workspace.sh"]),',
        )

    path.write_text(text, encoding="utf-8")
    print("updated scripts/doctor.py")


def update_ci_workflow() -> None:
    path = ROOT / ".github" / "workflows" / "ci.yml"
    text = path.read_text(encoding="utf-8")

    marker = """      - name: Repository doctor check
        run: bun run doctor:ci
"""

    insertion = """      - name: Set up Rust
        run: rustup toolchain install stable --profile minimal --component rustfmt,clippy

      - name: Rust workspace check
        run: bun run check:rust

"""

    if "bun run check:rust" not in text:
        text = text.replace(marker, insertion + marker)

    path.write_text(text, encoding="utf-8")
    print("updated .github/workflows/ci.yml")


def update_check_ci() -> None:
    path = ROOT / "scripts" / "check-ci.sh"
    text = path.read_text(encoding="utf-8")

    if '"bun run check:rust",' not in text:
        text = text.replace(
            '"bun run doctor:ci",',
            '"bun run check:rust",\n        "bun run doctor:ci",',
        )

    if '"check:rust",' not in text:
        text = text.replace(
            '"doctor:ci",',
            '"check:rust",\n        "doctor:ci",',
        )

    path.write_text(text, encoding="utf-8")
    print("updated scripts/check-ci.sh")


workspace_members = ",\n  ".join(f'"crates/{crate["dir"]}"' for crate in CRATES)

write_file(
    "Cargo.toml",
    f"""
    [workspace]
    members = [
      {workspace_members}
    ]
    resolver = "2"

    [workspace.package]
    version = "0.1.0"
    edition = "2021"
    license = "MIT"
    repository = "https://github.com/thomascarter613/monad-factory"
    rust-version = "1.85"

    [workspace.lints.rust]
    unsafe_code = "forbid"
    missing_docs = "warn"

    [workspace.lints.clippy]
    all = "warn"
    pedantic = "warn"
    nursery = "warn"
    unwrap_used = "warn"
    expect_used = "warn"
    panic = "warn"
    todo = "warn"
    unimplemented = "warn"
    """,
)

write_file(
    "rust-toolchain.toml",
    """
    [toolchain]
    channel = "stable"
    components = ["rustfmt", "clippy"]
    profile = "minimal"
    """,
)

write_file(
    "rustfmt.toml",
    """
    edition = "2021"
    max_width = 100
    newline_style = "Unix"
    use_field_init_shorthand = true
    use_try_shorthand = true
    """,
)

write_file(
    ".cargo/config.toml",
    """
    [alias]
    c = "check --workspace --all-targets"
    t = "test --workspace --all-targets"
    l = "clippy --workspace --all-targets -- -D warnings"
    f = "fmt --all"
    fc = "fmt --all -- --check"
    """,
)

write_file(
    "crates/monad-core/Cargo.toml",
    """
    [package]
    name = "monad-core"
    description = "Core domain primitives and shared runtime contracts for Monad Factory."
    version.workspace = true
    edition.workspace = true
    license.workspace = true
    repository.workspace = true
    rust-version.workspace = true

    [lib]
    name = "monad_core"
    path = "src/lib.rs"

    [lints]
    workspace = true
    """,
)

write_file(
    "crates/monad-core/src/lib.rs",
    """
    //! Core domain primitives and shared runtime contracts for Monad Factory.

    /// Canonical product name.
    pub const PRODUCT_NAME: &str = "Monad Factory";

    /// Canonical public CLI command name.
    pub const CLI_NAME: &str = "monad";

    /// Current implementation phase.
    pub const IMPLEMENTATION_PHASE: &str = "pre-implementation foundation";

    /// Build and product identity exposed by the CLI and future services.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct BuildInfo {
        /// Product name.
        pub product_name: &'static str,

        /// CLI command name.
        pub cli_name: &'static str,

        /// Cargo package version.
        pub version: &'static str,

        /// Current implementation phase.
        pub phase: &'static str,
    }

    /// Return build and product identity for the current crate graph.
    #[must_use]
    pub const fn build_info() -> BuildInfo {
        BuildInfo {
            product_name: PRODUCT_NAME,
            cli_name: CLI_NAME,
            version: env!("CARGO_PKG_VERSION"),
            phase: IMPLEMENTATION_PHASE,
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn build_info_uses_canonical_names() {
            let info = build_info();

            assert_eq!(info.product_name, "Monad Factory");
            assert_eq!(info.cli_name, "monad");
            assert_eq!(info.phase, "pre-implementation foundation");
        }
    }
    """,
)

for crate in CRATES:
    if crate["dir"] in {"monad-core", "monad-cli"}:
        continue

    write_file(
        f"crates/{crate['dir']}/Cargo.toml",
        f"""
        [package]
        name = "{crate['package']}"
        description = "{crate['description']}"
        version.workspace = true
        edition.workspace = true
        license.workspace = true
        repository.workspace = true
        rust-version.workspace = true

        [lib]
        name = "{crate['crate']}"
        path = "src/lib.rs"

        [dependencies]
        monad-core = {{ path = "../monad-core" }}

        [lints]
        workspace = true
        """,
    )

    readable = crate["description"]
    readable_doc = readable.replace("OpenTofu", "`OpenTofu`")

    write_file(
        f"crates/{crate['dir']}/src/lib.rs",
        f"""
        //! {readable_doc}

        /// Return the canonical crate name.
        #[must_use]
        pub const fn crate_name() -> &'static str {{
            "{crate['crate']}"
        }}

        /// Return the canonical public CLI name from the shared core crate.
        #[must_use]
        pub const fn cli_name() -> &'static str {{
            monad_core::CLI_NAME
        }}

        #[cfg(test)]
        mod tests {{
            use super::*;

            #[test]
            fn exposes_canonical_crate_name() {{
                assert_eq!(crate_name(), "{crate['crate']}");
            }}

            #[test]
            fn shares_canonical_cli_name() {{
                assert_eq!(cli_name(), "monad");
            }}
        }}
        """,
    )

write_file(
    "crates/monad-cli/Cargo.toml",
    """
    [package]
    name = "monad-cli"
    description = "Public monad command-line interface."
    version.workspace = true
    edition.workspace = true
    license.workspace = true
    repository.workspace = true
    rust-version.workspace = true

    [[bin]]
    name = "monad"
    path = "src/main.rs"

    [dependencies]
    monad-core = { path = "../monad-core" }

    [lints]
    workspace = true
    """,
)

write_file(
    "crates/monad-cli/src/main.rs",
    """
    //! Public `monad` command-line interface.

    use monad_core::{build_info, CLI_NAME};

    const HELP: &str = "Monad Factory CLI\\n\\nUsage:\\n  monad help\\n  monad version\\n  monad info\\n  monad doctor\\n\\nCommands:\\n  help      Show this help text.\\n  version   Show CLI version.\\n  info      Show product and implementation information.\\n  doctor    Explain how to run the repository doctor.\\n";

    fn main() {
        let args: Vec<String> = std::env::args().skip(1).collect();

        match run(&args) {
            Ok(output) => {
                println!("{output}");
            }
            Err(message) => {
                eprintln!("{message}");
                std::process::exit(2);
            }
        }
    }

    fn run(args: &[String]) -> Result<String, String> {
        let command = args.first().map_or("help", String::as_str);

        match command {
            "help" | "--help" | "-h" => Ok(help_text()),
            "version" | "--version" | "-V" => Ok(version_text()),
            "info" => Ok(info_text()),
            "doctor" => Ok(doctor_text()),
            unknown => Err(format!(
                "unknown command `{unknown}`\\n\\nRun `monad help` for available commands."
            )),
        }
    }

    fn help_text() -> String {
        HELP.to_string()
    }

    fn version_text() -> String {
        let info = build_info();
        format!("{} {}", info.cli_name, info.version)
    }

    fn info_text() -> String {
        let info = build_info();

        format!(
            "product: {}\\ncli: {}\\nversion: {}\\nphase: {}",
            info.product_name, info.cli_name, info.version, info.phase
        )
    }

    fn doctor_text() -> String {
        format!(
            "`{CLI_NAME} doctor` is reserved for the native CLI doctor. For the current repository foundation, run `bun run doctor`."
        )
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        fn args(values: &[&str]) -> Vec<String> {
            values.iter().map(ToString::to_string).collect()
        }

        #[test]
        fn help_is_default() -> Result<(), String> {
            let output = run(&args(&[]))?;

            assert!(output.contains("Monad Factory CLI"));
            assert!(output.contains("monad help"));

            Ok(())
        }

        #[test]
        fn version_uses_canonical_cli_name() -> Result<(), String> {
            let output = run(&args(&["version"]))?;

            assert!(output.starts_with("monad "));

            Ok(())
        }

        #[test]
        fn info_uses_canonical_product_name() -> Result<(), String> {
            let output = run(&args(&["info"]))?;

            assert!(output.contains(monad_core::PRODUCT_NAME));
            assert!(output.contains("phase: pre-implementation foundation"));

            Ok(())
        }

        #[test]
        fn unknown_command_fails() -> Result<(), String> {
            let error = match run(&args(&["nope"])) {
                Ok(output) => {
                    return Err(format!(
                        "unknown command should fail but returned successful output: {output}"
                    ));
                }
                Err(error) => error,
            };

            assert!(error.contains("unknown command"));

            Ok(())
        }
    }
    """,
)

write_file(
    "scripts/check-rust-workspace.sh",
    """
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
    """,
    mode=0o755,
)

remove_file("crates/monad-core/.gitkeep")
remove_file("crates/monad-config/.gitkeep")
remove_file("crates/monad-context/.gitkeep")
remove_file("crates/monad-memory/.gitkeep")
remove_file("crates/monad-policy/.gitkeep")
remove_file("crates/monad-template/.gitkeep")
remove_file("crates/monad-plugin/.gitkeep")
remove_file("crates/monad-deploy/.gitkeep")
remove_file("crates/monad-agent/.gitkeep")
remove_file("crates/monad-nx-adapter/.gitkeep")
remove_file("crates/monad-marketplace/.gitkeep")
remove_file("crates/monad-cli/.gitkeep")

update_package_json()
update_doctor()
update_ci_workflow()
update_check_ci()

print("Rust workspace foundation generated")

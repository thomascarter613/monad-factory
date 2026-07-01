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

    scripts["monad:help"] = "cargo run -p monad-cli -- help"
    scripts["monad:version"] = "cargo run -p monad-cli -- version"
    scripts["monad:info"] = "cargo run -p monad-cli -- info"
    scripts["monad:check"] = "cargo run -p monad-cli -- check all"
    scripts["monad:inspect"] = "cargo run -p monad-cli -- inspect workspace"
    scripts["monad:graph"] = "cargo run -p monad-cli -- graph text"
    scripts["monad:context"] = "cargo run -p monad-cli -- context help"
    scripts["monad:memory"] = "cargo run -p monad-cli -- memory status"

    path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    print("updated package.json")


def update_doctor() -> None:
    path = ROOT / "scripts" / "doctor.py"
    text = path.read_text(encoding="utf-8")

    expected = [
        '"monad:check",',
        '"monad:context",',
        '"monad:graph",',
        '"monad:help",',
        '"monad:info",',
        '"monad:inspect",',
        '"monad:memory",',
        '"monad:version",',
    ]

    for script in reversed(expected):
        if script not in text:
            text = text.replace(
                '"moon:version",',
                f'{script}\n                "moon:version",',
            )

    path.write_text(text, encoding="utf-8")
    print("updated scripts/doctor.py")


def update_rust_check() -> None:
    path = ROOT / "scripts" / "check-rust-workspace.sh"
    text = path.read_text(encoding="utf-8")

    required_files = [
        '"crates/monad-cli/src/cli.rs",',
        '"crates/monad-cli/src/commands/mod.rs",',
        '"crates/monad-cli/src/commands/check.rs",',
        '"crates/monad-cli/src/commands/context.rs",',
        '"crates/monad-cli/src/commands/graph.rs",',
        '"crates/monad-cli/src/commands/info.rs",',
        '"crates/monad-cli/src/commands/inspect.rs",',
        '"crates/monad-cli/src/commands/memory.rs",',
        '"docs/cli/00-index.md",',
        '"docs/cli/command-surface.md",',
    ]

    for required_file in reversed(required_files):
        if required_file not in text:
            text = text.replace(
                '"crates/monad-cli/src/main.rs",',
                f'"crates/monad-cli/src/main.rs",\n        {required_file}',
            )

    command_checks = """
    cargo run -p monad-cli -- check all >/dev/null
    cargo run -p monad-cli -- check foundation >/dev/null
    cargo run -p monad-cli -- inspect workspace >/dev/null
    cargo run -p monad-cli -- inspect scope >/dev/null
    cargo run -p monad-cli -- graph text >/dev/null
    cargo run -p monad-cli -- graph json >/dev/null
    cargo run -p monad-cli -- graph mermaid >/dev/null
    cargo run -p monad-cli -- graph dot >/dev/null
    cargo run -p monad-cli -- context help >/dev/null
    cargo run -p monad-cli -- context pack >/dev/null
    cargo run -p monad-cli -- memory status >/dev/null
    cargo run -p monad-cli -- memory backends >/dev/null
    """

    if "cargo run -p monad-cli -- check all >/dev/null" not in text:
        text = text.replace(
            "cargo run -p monad-cli -- info >/dev/null\n",
            "cargo run -p monad-cli -- info >/dev/null\n" + clean(command_checks) + "\n",
        )

    path.write_text(text, encoding="utf-8")
    print("updated scripts/check-rust-workspace.sh")


write_file(
    "crates/monad-cli/src/main.rs",
    """
    //! Public `monad` command-line interface.

    mod cli;
    mod commands;

    fn main() {
        let args: Vec<String> = std::env::args().skip(1).collect();

        match cli::run(&args) {
            Ok(output) => {
                println!("{output}");
            }
            Err(error) => {
                eprintln!("{error}");
                std::process::exit(2);
            }
        }
    }
    """,
)

write_file(
    "crates/monad-cli/src/cli.rs",
    r'''
    //! CLI argument parsing and dispatch.

    use std::fmt::{Display, Formatter};

    use crate::commands;

    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct CliError {
        message: String,
    }

    impl CliError {
        pub fn new(message: impl Into<String>) -> Self {
            Self {
                message: message.into(),
            }
        }
    }

    impl Display for CliError {
        fn fmt(&self, formatter: &mut Formatter<'_>) -> std::fmt::Result {
            formatter.write_str(&self.message)
        }
    }

    impl std::error::Error for CliError {}

    pub fn run(args: &[String]) -> Result<String, CliError> {
        let Some(command) = args.first() else {
            return Ok(commands::root_help());
        };

        let rest = &args[1..];

        match command.as_str() {
            "help" | "--help" | "-h" => Ok(commands::root_help()),
            "version" | "--version" | "-V" => Ok(commands::info::version_text()),
            "info" => Ok(commands::info::info_text()),
            "doctor" => Ok(commands::info::doctor_text()),
            "check" => commands::check::render(rest).map_err(CliError::new),
            "inspect" => commands::inspect::render(rest).map_err(CliError::new),
            "graph" => commands::graph::render(rest).map_err(CliError::new),
            "context" => commands::context::render(rest).map_err(CliError::new),
            "memory" => commands::memory::render(rest).map_err(CliError::new),
            unknown => Err(CliError::new(format!(
                "unknown command `{unknown}`\n\nRun `monad help` for available commands."
            ))),
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        fn args(values: &[&str]) -> Vec<String> {
            values.iter().map(ToString::to_string).collect()
        }

        fn run_ok(values: &[&str]) -> Result<String, String> {
            run(&args(values)).map_err(|error| error.to_string())
        }

        #[test]
        fn help_is_default() -> Result<(), String> {
            let output = run_ok(&[])?;

            assert!(output.contains("Monad Factory CLI"));
            assert!(output.contains("monad check"));
            assert!(output.contains("monad memory"));

            Ok(())
        }

        #[test]
        fn version_uses_canonical_cli_name() -> Result<(), String> {
            let output = run_ok(&["version"])?;

            assert!(output.starts_with("monad "));

            Ok(())
        }

        #[test]
        fn info_uses_canonical_product_name() -> Result<(), String> {
            let output = run_ok(&["info"])?;

            assert!(output.contains(monad_core::PRODUCT_NAME));
            assert!(output.contains("phase: pre-implementation foundation"));

            Ok(())
        }

        #[test]
        fn command_groups_are_registered() -> Result<(), String> {
            let commands = [
                ["check", "all"],
                ["inspect", "workspace"],
                ["graph", "text"],
                ["context", "help"],
                ["memory", "status"],
            ];

            for command in commands {
                let output = run_ok(&command)?;
                assert!(!output.trim().is_empty());
            }

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
                Err(error) => error.to_string(),
            };

            assert!(error.contains("unknown command"));

            Ok(())
        }
    }
    ''',
)

write_file(
    "crates/monad-cli/src/commands/mod.rs",
    r'''
    //! Command rendering modules for the `monad` CLI.

    pub mod check;
    pub mod context;
    pub mod graph;
    pub mod info;
    pub mod inspect;
    pub mod memory;

    pub fn root_help() -> String {
        [
            "Monad Factory CLI",
            "",
            "Usage:",
            "  monad <command> [arguments]",
            "",
            "Core commands:",
            "  monad help                 Show this help text.",
            "  monad version              Show CLI version.",
            "  monad info                 Show product and implementation information.",
            "  monad doctor               Explain how to run repository doctor checks.",
            "",
            "Foundation command groups:",
            "  monad check [target]       Validate foundation, toolchain, Rust, CI, or all checks.",
            "  monad inspect [target]     Inspect workspace, scope, toolchain, or memory state.",
            "  monad graph [format]       Render the registered graph command surface.",
            "  monad context <command>    Work with context packs, handoffs, and AI exports.",
            "  monad memory [command]     Inspect local-first Monad Memory foundations.",
            "",
            "This command surface is part of core v1 scope. Current outputs are deterministic",
            "foundation responses that anchor the stable CLI shape while the deeper engines are",
            "implemented under the approved v1 maximal functional plan.",
        ]
        .join("\n")
    }

    pub fn unknown_argument(command: &str, value: &str, allowed: &[&str]) -> String {
        format!(
            "unknown argument `{value}` for `monad {command}`\n\nAllowed values: {}",
            allowed.join(", ")
        )
    }
    ''',
)

write_file(
    "crates/monad-cli/src/commands/info.rs",
    r'''
    //! Informational command renderers.

    use monad_core::{build_info, CLI_NAME};

    pub fn version_text() -> String {
        let info = build_info();
        format!("{} {}", info.cli_name, info.version)
    }

    pub fn info_text() -> String {
        let info = build_info();

        [
            format!("product: {}", info.product_name),
            format!("cli: {}", info.cli_name),
            format!("version: {}", info.version),
            format!("phase: {}", info.phase),
            "scope: v1 maximal functional product-factory platform".to_string(),
            "source_of_truth: docs/product/v1-maximal-functional-scope-and-delivery-plan.md"
                .to_string(),
        ]
        .join("\n")
    }

    pub fn doctor_text() -> String {
        format!(
            "`{CLI_NAME} doctor` is reserved for the native CLI doctor command. For the current repository foundation, run `bun run doctor` or `bun run doctor:strict`."
        )
    }
    ''',
)

write_file(
    "crates/monad-cli/src/commands/check.rs",
    r'''
    //! Check command renderer.

    use crate::commands::unknown_argument;

    const TARGETS: &[&str] = &[
        "all",
        "foundation",
        "toolchain",
        "ci",
        "github-planning",
        "rust",
    ];

    pub fn render(args: &[String]) -> Result<String, String> {
        let target = args.first().map_or("all", String::as_str);

        match target {
            "all" => Ok(response("all", "bun run check")),
            "foundation" => Ok(response("foundation", "bun run check:foundation")),
            "toolchain" => Ok(response("toolchain", "bun run check:toolchain")),
            "ci" => Ok(response("ci", "bun run check:ci")),
            "github-planning" => Ok(response(
                "github-planning",
                "bun run check:github-planning",
            )),
            "rust" => Ok(response("rust", "bun run check:rust")),
            "--help" | "-h" | "help" => Ok(help()),
            unknown => Err(unknown_argument("check", unknown, TARGETS)),
        }
    }

    fn response(target: &str, delegated_command: &str) -> String {
        [
            format!("check_target: {target}"),
            format!("delegated_command: {delegated_command}"),
            "status: registered".to_string(),
            "scope: core v1 validation surface".to_string(),
        ]
        .join("\n")
    }

    fn help() -> String {
        [
            "Usage:",
            "  monad check [target]",
            "",
            "Targets:",
            "  all",
            "  foundation",
            "  toolchain",
            "  ci",
            "  github-planning",
            "  rust",
        ]
        .join("\n")
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        fn args(values: &[&str]) -> Vec<String> {
            values.iter().map(ToString::to_string).collect()
        }

        #[test]
        fn defaults_to_all() -> Result<(), String> {
            let output = render(&args(&[]))?;

            assert!(output.contains("check_target: all"));
            assert!(output.contains("bun run check"));

            Ok(())
        }

        #[test]
        fn renders_rust_target() -> Result<(), String> {
            let output = render(&args(&["rust"]))?;

            assert!(output.contains("check_target: rust"));
            assert!(output.contains("bun run check:rust"));

            Ok(())
        }
    }
    ''',
)

write_file(
    "crates/monad-cli/src/commands/inspect.rs",
    r'''
    //! Inspect command renderer.

    use crate::commands::unknown_argument;

    const TARGETS: &[&str] = &["workspace", "scope", "toolchain", "memory"];

    pub fn render(args: &[String]) -> Result<String, String> {
        let target = args.first().map_or("workspace", String::as_str);

        match target {
            "workspace" => Ok(workspace()),
            "scope" => Ok(scope()),
            "toolchain" => Ok(toolchain()),
            "memory" => Ok(memory()),
            "--help" | "-h" | "help" => Ok(help()),
            unknown => Err(unknown_argument("inspect", unknown, TARGETS)),
        }
    }

    fn workspace() -> String {
        [
            "inspect_target: workspace",
            "workspace_manifest: workspace.toml",
            "moon_workspace: .moon/workspace.yml",
            "cargo_workspace: Cargo.toml",
            "status: registered",
        ]
        .join("\n")
    }

    fn scope() -> String {
        [
            "inspect_target: scope",
            "source_of_truth: docs/product/v1-maximal-functional-scope-and-delivery-plan.md",
            "scope_model: v1 maximal functional scope",
            "downgrade_policy: approved v1 capabilities remain core v1 scope",
        ]
        .join("\n")
    }

    fn toolchain() -> String {
        [
            "inspect_target: toolchain",
            "toolchain_manifest: mise.toml",
            "javascript_package_manager: bun",
            "task_orchestrator: moon",
            "rust_workspace: Cargo.toml",
        ]
        .join("\n")
    }

    fn memory() -> String {
        [
            "inspect_target: memory",
            "memory_index: .monad/memory/MEMORY.md",
            "policy: policies/memory/memory-policy.md",
            "planned_backends: sqlite, pgvector, qdrant",
        ]
        .join("\n")
    }

    fn help() -> String {
        [
            "Usage:",
            "  monad inspect [target]",
            "",
            "Targets:",
            "  workspace",
            "  scope",
            "  toolchain",
            "  memory",
        ]
        .join("\n")
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        fn args(values: &[&str]) -> Vec<String> {
            values.iter().map(ToString::to_string).collect()
        }

        #[test]
        fn renders_scope_source_of_truth() -> Result<(), String> {
            let output = render(&args(&["scope"]))?;

            assert!(output.contains("v1 maximal functional scope"));
            assert!(output.contains("source_of_truth"));

            Ok(())
        }
    }
    ''',
)

write_file(
    "crates/monad-cli/src/commands/graph.rs",
    r'''
    //! Graph command renderer.

    use crate::commands::unknown_argument;

    const FORMATS: &[&str] = &["text", "json", "mermaid", "dot"];

    pub fn render(args: &[String]) -> Result<String, String> {
        let format = args.first().map_or("text", String::as_str);

        match format {
            "text" => Ok(text()),
            "json" => Ok(json()),
            "mermaid" => Ok(mermaid()),
            "dot" => Ok(dot()),
            "--help" | "-h" | "help" => Ok(help()),
            unknown => Err(unknown_argument("graph", unknown, FORMATS)),
        }
    }

    fn text() -> String {
        [
            "graph_format: text",
            "nodes:",
            "  - repo",
            "  - apps",
            "  - packages",
            "  - services",
            "  - crates",
            "  - infra",
            "  - policies",
            "  - memory",
            "edges:",
            "  - repo -> apps",
            "  - repo -> packages",
            "  - repo -> services",
            "  - repo -> crates",
            "  - repo -> infra",
            "  - repo -> policies",
            "  - repo -> memory",
        ]
        .join("\n")
    }

    fn json() -> String {
        [
            "{",
            "  \"format\": \"json\",",
            "  \"nodes\": [\"repo\", \"apps\", \"packages\", \"services\", \"crates\", \"infra\", \"policies\", \"memory\"],",
            "  \"edges\": [",
            "    [\"repo\", \"apps\"],",
            "    [\"repo\", \"packages\"],",
            "    [\"repo\", \"services\"],",
            "    [\"repo\", \"crates\"],",
            "    [\"repo\", \"infra\"],",
            "    [\"repo\", \"policies\"],",
            "    [\"repo\", \"memory\"]",
            "  ]",
            "}",
        ]
        .join("\n")
    }

    fn mermaid() -> String {
        [
            "graph TD",
            "  repo[repo]",
            "  apps[apps]",
            "  packages[packages]",
            "  services[services]",
            "  crates[crates]",
            "  infra[infra]",
            "  policies[policies]",
            "  memory[memory]",
            "  repo --> apps",
            "  repo --> packages",
            "  repo --> services",
            "  repo --> crates",
            "  repo --> infra",
            "  repo --> policies",
            "  repo --> memory",
        ]
        .join("\n")
    }

    fn dot() -> String {
        [
            "digraph monad_factory {",
            "  repo -> apps;",
            "  repo -> packages;",
            "  repo -> services;",
            "  repo -> crates;",
            "  repo -> infra;",
            "  repo -> policies;",
            "  repo -> memory;",
            "}",
        ]
        .join("\n")
    }

    fn help() -> String {
        [
            "Usage:",
            "  monad graph [format]",
            "",
            "Formats:",
            "  text",
            "  json",
            "  mermaid",
            "  dot",
        ]
        .join("\n")
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        fn args(values: &[&str]) -> Vec<String> {
            values.iter().map(ToString::to_string).collect()
        }

        #[test]
        fn renders_mermaid() -> Result<(), String> {
            let output = render(&args(&["mermaid"]))?;

            assert!(output.contains("graph TD"));
            assert!(output.contains("repo --> crates"));

            Ok(())
        }

        #[test]
        fn renders_json() -> Result<(), String> {
            let output = render(&args(&["json"]))?;

            assert!(output.contains("\"format\": \"json\""));
            assert!(output.contains("\"nodes\""));

            Ok(())
        }
    }
    ''',
)

write_file(
    "crates/monad-cli/src/commands/context.rs",
    r'''
    //! Context command renderer.

    use crate::commands::unknown_argument;

    const COMMANDS: &[&str] = &["help", "pack", "verify", "handoff", "exports"];

    pub fn render(args: &[String]) -> Result<String, String> {
        let command = args.first().map_or("help", String::as_str);

        match command {
            "help" | "--help" | "-h" => Ok(help()),
            "pack" => Ok(response(
                "pack",
                "context pack creation is a core v1 command surface",
            )),
            "verify" => Ok(response(
                "verify",
                "context pack verification is a core v1 command surface",
            )),
            "handoff" => Ok(response(
                "handoff",
                "cross-session handoff generation is a core v1 command surface",
            )),
            "exports" => Ok(response(
                "exports",
                "AI tool export generation is a core v1 command surface",
            )),
            unknown => Err(unknown_argument("context", unknown, COMMANDS)),
        }
    }

    fn response(command: &str, description: &str) -> String {
        [
            format!("context_command: {command}"),
            format!("description: {description}"),
            "source_of_truth: docs/product/v1-maximal-functional-scope-and-delivery-plan.md"
                .to_string(),
            "status: registered".to_string(),
        ]
        .join("\n")
    }

    fn help() -> String {
        [
            "Usage:",
            "  monad context <command>",
            "",
            "Commands:",
            "  pack",
            "  verify",
            "  handoff",
            "  exports",
        ]
        .join("\n")
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        fn args(values: &[&str]) -> Vec<String> {
            values.iter().map(ToString::to_string).collect()
        }

        #[test]
        fn renders_handoff_command() -> Result<(), String> {
            let output = render(&args(&["handoff"]))?;

            assert!(output.contains("context_command: handoff"));
            assert!(output.contains("core v1"));

            Ok(())
        }
    }
    ''',
)

write_file(
    "crates/monad-cli/src/commands/memory.rs",
    r'''
    //! Memory command renderer.

    use crate::commands::unknown_argument;

    const COMMANDS: &[&str] = &["status", "backends", "policy"];

    pub fn render(args: &[String]) -> Result<String, String> {
        let command = args.first().map_or("status", String::as_str);

        match command {
            "status" => Ok(status()),
            "backends" => Ok(backends()),
            "policy" => Ok(policy()),
            "--help" | "-h" | "help" => Ok(help()),
            unknown => Err(unknown_argument("memory", unknown, COMMANDS)),
        }
    }

    fn status() -> String {
        [
            "memory_status: registered",
            "memory_index: .monad/memory/MEMORY.md",
            "scope: local-first inspectable policy-governed Monad Memory",
            "planned_backends: sqlite, pgvector, qdrant",
        ]
        .join("\n")
    }

    fn backends() -> String {
        [
            "memory_backends:",
            "  - sqlite",
            "  - pgvector",
            "  - qdrant",
            "backend_policy: local-first with optional external retrieval acceleration",
        ]
        .join("\n")
    }

    fn policy() -> String {
        [
            "memory_policy: policies/memory/memory-policy.md",
            "governance: inspectable, policy-governed, LLM-agnostic",
            "scope: core v1 memory foundation",
        ]
        .join("\n")
    }

    fn help() -> String {
        [
            "Usage:",
            "  monad memory [command]",
            "",
            "Commands:",
            "  status",
            "  backends",
            "  policy",
        ]
        .join("\n")
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        fn args(values: &[&str]) -> Vec<String> {
            values.iter().map(ToString::to_string).collect()
        }

        #[test]
        fn renders_backend_plan() -> Result<(), String> {
            let output = render(&args(&["backends"]))?;

            assert!(output.contains("sqlite"));
            assert!(output.contains("pgvector"));
            assert!(output.contains("qdrant"));

            Ok(())
        }
    }
    ''',
)

write_file(
    "docs/cli/00-index.md",
    """
    # CLI Documentation Index

    Monad Factory exposes the public `monad` CLI as the governed repository and product-factory control plane.

    ## Documents

    - [Command Surface](./command-surface.md)
    """,
)

write_file(
    "docs/cli/command-surface.md",
    """
    # Monad CLI Command Surface

    The public CLI command name is:

    ```txt
    monad
    ```

    The first stable command surface includes:

    ```txt
    monad help
    monad version
    monad info
    monad doctor
    monad check [target]
    monad inspect [target]
    monad graph [format]
    monad context <command>
    monad memory [command]
    ```

    This command surface is part of the approved v1 maximal functional scope. The current implementation establishes deterministic foundation responses, test coverage, and stable command grouping while deeper engines are implemented under the canonical v1 delivery plan.

    The canonical v1 source of truth remains:

    ```txt
    docs/product/v1-maximal-functional-scope-and-delivery-plan.md
    ```

    ## Check targets

    ```txt
    all
    foundation
    toolchain
    ci
    github-planning
    rust
    ```

    ## Inspect targets

    ```txt
    workspace
    scope
    toolchain
    memory
    ```

    ## Graph formats

    ```txt
    text
    json
    mermaid
    dot
    ```

    ## Context commands

    ```txt
    pack
    verify
    handoff
    exports
    ```

    ## Memory commands

    ```txt
    status
    backends
    policy
    ```
    """,
)

update_package_json()
update_doctor()
update_rust_check()

print("CLI command surface generated")

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


lib_path = ROOT / "crates/monad-core/src/lib.rs"
lib_text = lib_path.read_text(encoding="utf-8")

if "mod aggregate_check;" not in lib_text:
    if "mod context_foundation;\n" in lib_text:
        lib_text = lib_text.replace(
            "mod context_foundation;\n",
            "mod context_foundation;\nmod aggregate_check;\n",
        )
    elif "mod graph;\n" in lib_text:
        lib_text = lib_text.replace("mod graph;\n", "mod graph;\nmod aggregate_check;\n")
    else:
        raise SystemExit("Could not find module insertion point in crates/monad-core/src/lib.rs")

if "pub use aggregate_check::" not in lib_text:
    export = '''
pub use aggregate_check::{run_all_checks, AggregateCheckItem, AggregateCheckReport};

'''
    if "pub use context_foundation::" in lib_text:
        lib_text = lib_text.replace("pub use context_foundation::", export + "pub use context_foundation::")
    elif "pub use graph::" in lib_text:
        lib_text = lib_text.replace("pub use graph::", export + "pub use graph::")
    else:
        raise SystemExit("Could not find export insertion point in crates/monad-core/src/lib.rs")

lib_path.write_text(lib_text, encoding="utf-8")
print("updated crates/monad-core/src/lib.rs")


write_file(
    "crates/monad-core/src/aggregate_check.rs",
    r'''
    //! Native aggregate check engine for the `monad check all` command.

    use std::path::{Path, PathBuf};

    use crate::{
        build_repository_graph, inspect_context_foundation, run_foundation_check, run_memory_check,
        run_toolchain_check, CheckStatus, WorkspaceInspectionError,
    };

    /// One native aggregate check item.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct AggregateCheckItem {
        /// Stable item name.
        pub name: String,

        /// Check status.
        pub status: CheckStatus,

        /// Human-readable check message.
        pub message: String,
    }

    /// Native aggregate check report.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct AggregateCheckReport {
        /// Workspace root used for the aggregate check.
        pub root: PathBuf,

        /// Overall aggregate status.
        pub status: CheckStatus,

        /// Individual aggregate check items.
        pub items: Vec<AggregateCheckItem>,
    }

    impl AggregateCheckReport {
        /// Count passing check items.
        #[must_use]
        pub fn pass_count(&self) -> usize {
            self.items
                .iter()
                .filter(|item| item.status == CheckStatus::Pass)
                .count()
        }

        /// Count warning check items.
        #[must_use]
        pub fn warn_count(&self) -> usize {
            self.items
                .iter()
                .filter(|item| item.status == CheckStatus::Warn)
                .count()
        }

        /// Count failing check items.
        #[must_use]
        pub fn fail_count(&self) -> usize {
            self.items
                .iter()
                .filter(|item| item.status == CheckStatus::Fail)
                .count()
        }
    }

    /// Run the native aggregate check.
    ///
    /// # Errors
    ///
    /// Returns an error when one of the underlying native inspections or checks fails to run.
    pub fn run_all_checks(root: &Path) -> Result<AggregateCheckReport, WorkspaceInspectionError> {
        let foundation = run_foundation_check(root)?;
        let toolchain = run_toolchain_check(root)?;
        let memory = run_memory_check(root)?;
        let context = inspect_context_foundation(root)?;
        let graph = build_repository_graph(root)?;

        let items = vec![
            aggregate_item(
                "foundation",
                foundation.status,
                format!(
                    "{} pass, {} warn, {} fail",
                    foundation.pass_count(),
                    foundation.warn_count(),
                    foundation.fail_count()
                ),
            ),
            aggregate_item(
                "toolchain",
                toolchain.status,
                format!(
                    "{} pass, {} warn, {} fail",
                    toolchain.pass_count(),
                    toolchain.warn_count(),
                    toolchain.fail_count()
                ),
            ),
            aggregate_item(
                "memory",
                memory.status,
                format!(
                    "{} pass, {} warn, {} fail",
                    memory.pass_count(),
                    memory.warn_count(),
                    memory.fail_count()
                ),
            ),
            aggregate_item(
                "context",
                context.status(),
                format!(
                    "{}/{} context artifacts present",
                    context.present_artifact_count(),
                    context.artifacts.len()
                ),
            ),
            aggregate_item(
                "graph",
                presence_status(graph.is_complete()),
                format!("{}/{} graph nodes present", graph.present_node_count(), graph.nodes.len()),
            ),
        ];

        Ok(AggregateCheckReport {
            root: foundation.root,
            status: summarize_status(&items),
            items,
        })
    }

    fn aggregate_item(
        name: &str,
        status: CheckStatus,
        message: String,
    ) -> AggregateCheckItem {
        AggregateCheckItem {
            name: name.to_string(),
            status,
            message,
        }
    }

    fn summarize_status(items: &[AggregateCheckItem]) -> CheckStatus {
        if items.iter().any(|item| item.status == CheckStatus::Fail) {
            CheckStatus::Fail
        } else if items.iter().any(|item| item.status == CheckStatus::Warn) {
            CheckStatus::Warn
        } else {
            CheckStatus::Pass
        }
    }

    const fn presence_status(present: bool) -> CheckStatus {
        if present {
            CheckStatus::Pass
        } else {
            CheckStatus::Fail
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn summarize_status_passes_when_all_items_pass() {
            let items = vec![
                aggregate_item("one", CheckStatus::Pass, "ok".to_string()),
                aggregate_item("two", CheckStatus::Pass, "ok".to_string()),
            ];

            assert_eq!(summarize_status(&items), CheckStatus::Pass);
        }

        #[test]
        fn summarize_status_fails_when_any_item_fails() {
            let items = vec![
                aggregate_item("one", CheckStatus::Pass, "ok".to_string()),
                aggregate_item("two", CheckStatus::Fail, "bad".to_string()),
            ];

            assert_eq!(summarize_status(&items), CheckStatus::Fail);
        }
    }
    ''',
)


write_file(
    "crates/monad-cli/src/commands/check.rs",
    r'''
    //! Check command renderer.

    use std::path::Path;

    use monad_core::{
        run_all_checks, run_foundation_check, run_memory_check, run_toolchain_check,
        AggregateCheckReport, FoundationCheckReport, MemoryCheckReport, ToolchainCheckReport,
    };

    use crate::commands::unknown_argument;

    const TARGETS: &[&str] = &[
        "all",
        "foundation",
        "toolchain",
        "memory",
        "ci",
        "github-planning",
        "rust",
    ];

    /// Render a check command response.
    pub fn render(args: &[String]) -> Result<String, String> {
        let target = args.first().map_or("all", String::as_str);

        match target {
            "all" => all(),
            "foundation" => foundation(),
            "toolchain" => toolchain(),
            "memory" => memory(),
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

    fn all() -> Result<String, String> {
        let report = run_all_checks(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_all_report(&report))
    }

    fn foundation() -> Result<String, String> {
        let report = run_foundation_check(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_foundation_report(&report))
    }

    fn toolchain() -> Result<String, String> {
        let report = run_toolchain_check(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_toolchain_report(&report))
    }

    fn memory() -> Result<String, String> {
        let report = run_memory_check(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_memory_report(&report))
    }

    fn render_all_report(report: &AggregateCheckReport) -> String {
        let mut lines = vec![
            "check_target: all".to_string(),
            "engine: native".to_string(),
            format!("workspace_root: {}", report.root.display()),
            format!("status: {}", report.status),
            format!("pass_count: {}", report.pass_count()),
            format!("warn_count: {}", report.warn_count()),
            format!("fail_count: {}", report.fail_count()),
            "items:".to_string(),
        ];

        for item in &report.items {
            lines.push(format!(
                "  - {}: {} - {}",
                item.name, item.status, item.message
            ));
        }

        lines.join("\n")
    }

    fn render_foundation_report(report: &FoundationCheckReport) -> String {
        let mut lines = vec![
            "check_target: foundation".to_string(),
            "engine: native".to_string(),
            format!("workspace_root: {}", report.root.display()),
            format!("status: {}", report.status),
            format!("pass_count: {}", report.pass_count()),
            format!("warn_count: {}", report.warn_count()),
            format!("fail_count: {}", report.fail_count()),
            format!(
                "top_level_domains_present: {}/{}",
                report.inspection.present_domain_count(),
                report.inspection.domains.len()
            ),
            format!(
                "foundation_files_present: {}/{}",
                report.inspection.present_foundation_file_count(),
                report.inspection.foundation_files.len()
            ),
            "items:".to_string(),
        ];

        for item in &report.items {
            lines.push(format!(
                "  - {}: {} - {}",
                item.name, item.status, item.message
            ));
        }

        lines.join("\n")
    }

    fn render_toolchain_report(report: &ToolchainCheckReport) -> String {
        let mut lines = vec![
            "check_target: toolchain".to_string(),
            "engine: native".to_string(),
            format!("workspace_root: {}", report.root.display()),
            format!("status: {}", report.status),
            format!("pass_count: {}", report.pass_count()),
            format!("warn_count: {}", report.warn_count()),
            format!("fail_count: {}", report.fail_count()),
            format!(
                "toolchain_files_present: {}/{}",
                report.inspection.present_file_count(),
                report.inspection.files.len()
            ),
            format!(
                "mise_tools_declared: {}/{}",
                report.inspection.declared_tool_count(),
                report.inspection.declared_tools.len()
            ),
            "items:".to_string(),
        ];

        for item in &report.items {
            lines.push(format!(
                "  - {}: {} - {}",
                item.name, item.status, item.message
            ));
        }

        lines.join("\n")
    }

    fn render_memory_report(report: &MemoryCheckReport) -> String {
        let mut lines = vec![
            "check_target: memory".to_string(),
            "engine: native".to_string(),
            format!("workspace_root: {}", report.root.display()),
            format!("status: {}", report.status),
            format!("pass_count: {}", report.pass_count()),
            format!("warn_count: {}", report.warn_count()),
            format!("fail_count: {}", report.fail_count()),
            format!(
                "memory_files_present: {}/{}",
                report.inspection.present_file_count(),
                report.inspection.files.len()
            ),
            format!(
                "memory_backends_registered: {}/{}",
                report.inspection.registered_backend_count(),
                report.inspection.backends.len()
            ),
            "items:".to_string(),
        ];

        for item in &report.items {
            lines.push(format!(
                "  - {}: {} - {}",
                item.name, item.status, item.message
            ));
        }

        lines.join("\n")
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
            "  memory",
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
        fn defaults_to_native_all() -> Result<(), String> {
            let output = render(&args(&[]))?;

            assert!(output.contains("check_target: all"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("items:"));

            Ok(())
        }

        #[test]
        fn renders_rust_target() -> Result<(), String> {
            let output = render(&args(&["rust"]))?;

            assert!(output.contains("check_target: rust"));
            assert!(output.contains("bun run check:rust"));

            Ok(())
        }

        #[test]
        fn renders_native_foundation_check() -> Result<(), String> {
            let output = render(&args(&["foundation"]))?;

            assert!(output.contains("check_target: foundation"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("items:"));

            Ok(())
        }

        #[test]
        fn renders_native_toolchain_check() -> Result<(), String> {
            let output = render(&args(&["toolchain"]))?;

            assert!(output.contains("check_target: toolchain"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("toolchain_files_present:"));
            assert!(output.contains("mise_tools_declared:"));
            assert!(output.contains("items:"));

            Ok(())
        }

        #[test]
        fn renders_native_memory_check() -> Result<(), String> {
            let output = render(&args(&["memory"]))?;

            assert!(output.contains("check_target: memory"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("memory_files_present:"));
            assert!(output.contains("memory_backends_registered:"));
            assert!(output.contains("items:"));

            Ok(())
        }
    }
    ''',
)


write_file(
    "docs/cli/all-check.md",
    """
    # Native Aggregate Check

    `monad check all` runs the native aggregate readiness check.

    Example:

    ```bash
    cargo run -p monad-cli -- check all
    ```

    The aggregate currently includes:

    - native foundation check
    - native toolchain check
    - native memory check
    - native context foundation readiness
    - native repository graph readiness

    This replaces the earlier delegated-only `monad check all` response with a native report while preserving root `bun run check` as the full local/CI validation command.

    This is part of the approved v1 maximal functional CLI, governance, inspection, memory, context, graph, and repository-control scope.
    """,
)

index_path = ROOT / "docs/cli/00-index.md"
index_text = index_path.read_text(encoding="utf-8")
if "Native Aggregate Check" not in index_text:
    index_text = index_text.replace(
        "- [Native Context Command Group](./context-command.md)",
        "- [Native Context Command Group](./context-command.md)\n- [Native Aggregate Check](./all-check.md)",
    )
    index_path.write_text(index_text, encoding="utf-8")
    print("updated docs/cli/00-index.md")

check_path = ROOT / "scripts/check-rust-workspace.sh"
check_text = check_path.read_text(encoding="utf-8")

if '"crates/monad-core/src/aggregate_check.rs",' not in check_text:
    check_text = check_text.replace(
        '"crates/monad-core/src/context_foundation.rs",',
        '"crates/monad-core/src/context_foundation.rs",\n        "crates/monad-core/src/aggregate_check.rs",',
    )

if '"docs/cli/all-check.md",' not in check_text:
    check_text = check_text.replace(
        '"docs/cli/context-command.md",',
        '"docs/cli/context-command.md",\n        "docs/cli/all-check.md",',
    )

check_text = check_text.replace(
    "cargo run -p monad-cli -- check all >/dev/null",
    'cargo run -p monad-cli -- check all | grep "engine: native" >/dev/null',
)

check_path.write_text(check_text, encoding="utf-8")
print("updated scripts/check-rust-workspace.sh")

print("aggregate check engine generated")

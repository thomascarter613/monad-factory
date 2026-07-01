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


core_path = ROOT / "crates/monad-core/src/lib.rs"
core_text = core_path.read_text(encoding="utf-8")

insert_candidates = [
    "\n#[cfg(test)]\nmod tests {\n",
    "\n    #[cfg(test)]\n    mod tests {\n",
]

toolchain_check_engine = r'''
/// One native toolchain check item.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct ToolchainCheckItem {
    /// Stable item name.
    pub name: String,

    /// Check status.
    pub status: CheckStatus,

    /// Human-readable check message.
    pub message: String,
}

/// Native toolchain check report.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct ToolchainCheckReport {
    /// Workspace root used for the check.
    pub root: PathBuf,

    /// Overall check status.
    pub status: CheckStatus,

    /// Individual check items.
    pub items: Vec<ToolchainCheckItem>,

    /// Toolchain inspection used by the check.
    pub inspection: ToolchainInspection,
}

impl ToolchainCheckReport {
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

/// Run the native Monad Factory toolchain check.
///
/// # Errors
///
/// Returns an error when toolchain inspection fails.
pub fn run_toolchain_check(root: &Path) -> Result<ToolchainCheckReport, WorkspaceInspectionError> {
    let inspection = inspect_toolchain(root)?;
    let mut items = Vec::new();

    add_toolchain_file_check(&mut items, &inspection);
    add_mise_tool_check(&mut items, &inspection);
    add_package_manager_check(&mut items, &inspection);
    add_rust_toolchain_check(&mut items, &inspection);
    add_required_toolchain_status_checks(&mut items, &inspection);

    let status = summarize_toolchain_check_status(&items);

    Ok(ToolchainCheckReport {
        root: inspection.root.clone(),
        status,
        items,
        inspection,
    })
}

fn add_toolchain_file_check(
    items: &mut Vec<ToolchainCheckItem>,
    inspection: &ToolchainInspection,
) {
    let missing_files = inspection.missing_file_names();

    items.push(ToolchainCheckItem {
        name: "toolchain-files".to_string(),
        status: presence_status(missing_files.is_empty()),
        message: if missing_files.is_empty() {
            format!(
                "all {} expected toolchain files are present",
                inspection.files.len()
            )
        } else {
            format!("missing toolchain files: {}", missing_files.join(", "))
        },
    });
}

fn add_mise_tool_check(items: &mut Vec<ToolchainCheckItem>, inspection: &ToolchainInspection) {
    let missing_tools = inspection.missing_tool_names();

    items.push(ToolchainCheckItem {
        name: "mise-tools".to_string(),
        status: presence_status(missing_tools.is_empty()),
        message: if missing_tools.is_empty() {
            format!(
                "all {} expected mise tools are declared",
                inspection.declared_tools.len()
            )
        } else {
            format!("missing mise tools: {}", missing_tools.join(", "))
        },
    });
}

fn add_package_manager_check(
    items: &mut Vec<ToolchainCheckItem>,
    inspection: &ToolchainInspection,
) {
    let message = inspection
        .package_manager
        .as_deref()
        .map_or_else(|| "package manager declaration is missing".to_string(), |manager| {
            format!("package manager declared as `{manager}`")
        });

    add_status_check(
        items,
        "package-manager",
        presence_status(inspection.package_manager.is_some()),
        message,
    );
}

fn add_rust_toolchain_check(
    items: &mut Vec<ToolchainCheckItem>,
    inspection: &ToolchainInspection,
) {
    let message = inspection
        .rust_toolchain_channel
        .as_deref()
        .map_or_else(|| "Rust toolchain channel is missing".to_string(), |channel| {
            format!("Rust toolchain channel declared as `{channel}`")
        });

    add_status_check(
        items,
        "rust-toolchain",
        presence_status(inspection.rust_toolchain_channel.is_some()),
        message,
    );
}

fn add_required_toolchain_status_checks(
    items: &mut Vec<ToolchainCheckItem>,
    inspection: &ToolchainInspection,
) {
    let checks = [
        (
            "root-check-script",
            inspection.check_script_status,
            "package.json script `check` is required",
        ),
        (
            "root-toolchain-check-script",
            inspection.toolchain_check_script_status,
            "package.json script `check:toolchain` is required",
        ),
        (
            "rust-check-script",
            inspection.rust_check_script_status,
            "package.json script `check:rust` is required",
        ),
        (
            "moon-workspace",
            inspection.moon_workspace_status,
            ".moon/workspace.yml is required",
        ),
        (
            "moon-toolchains",
            inspection.moon_toolchains_status,
            ".moon/toolchains.yml is required",
        ),
        (
            "cargo-workspace",
            inspection.cargo_workspace_status,
            "Cargo.toml must declare a Cargo workspace",
        ),
    ];

    for (name, status, message) in checks {
        add_status_check(items, name, status, message.to_string());
    }
}

fn summarize_toolchain_check_status(items: &[ToolchainCheckItem]) -> CheckStatus {
    if items.iter().any(|item| item.status == CheckStatus::Fail) {
        CheckStatus::Fail
    } else if items.iter().any(|item| item.status == CheckStatus::Warn) {
        CheckStatus::Warn
    } else {
        CheckStatus::Pass
    }
}

fn add_status_check(
    items: &mut Vec<ToolchainCheckItem>,
    name: &str,
    status: CheckStatus,
    message: String,
) {
    items.push(ToolchainCheckItem {
        name: name.to_string(),
        status,
        message,
    });
}
'''

if "pub struct ToolchainCheckReport" not in core_text:
    insert_before = next((candidate for candidate in insert_candidates if candidate in core_text), None)

    if insert_before is None:
        raise SystemExit(
            "Could not find insertion point in monad-core/src/lib.rs. "
            "Expected a crate-root #[cfg(test)] mod tests block."
        )

    core_text = core_text.replace(insert_before, toolchain_check_engine + insert_before)
    core_path.write_text(core_text, encoding="utf-8")
    print("updated crates/monad-core/src/lib.rs")
else:
    print("crates/monad-core/src/lib.rs already contains toolchain check engine")


write_file(
    "crates/monad-cli/src/commands/check.rs",
    r'''
    //! Check command renderer.

    use std::path::Path;

    use monad_core::{
        run_foundation_check, run_toolchain_check, FoundationCheckReport, ToolchainCheckReport,
    };

    use crate::commands::unknown_argument;

    const TARGETS: &[&str] = &[
        "all",
        "foundation",
        "toolchain",
        "ci",
        "github-planning",
        "rust",
    ];

    /// Render a check command response.
    pub fn render(args: &[String]) -> Result<String, String> {
        let target = args.first().map_or("all", String::as_str);

        match target {
            "all" => Ok(response("all", "bun run check")),
            "foundation" => foundation(),
            "toolchain" => toolchain(),
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

    fn foundation() -> Result<String, String> {
        let report = run_foundation_check(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_foundation_report(&report))
    }

    fn toolchain() -> Result<String, String> {
        let report = run_toolchain_check(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_toolchain_report(&report))
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
    }
    ''',
)

write_file(
    "docs/cli/toolchain-check.md",
    """
    # Native Toolchain Check

    `monad check toolchain` runs a native validation engine over the root development control plane.

    Example:

    ```bash
    cargo run -p monad-cli -- check toolchain
    ```

    Current checks include:

    - expected root toolchain files
    - expected `mise.toml` tool declarations
    - Bun package manager declaration
    - Rust toolchain channel declaration
    - root check script presence
    - root toolchain check script presence
    - Rust check script presence
    - moon workspace/toolchain configuration presence
    - Cargo workspace declaration

    This is part of the approved v1 maximal functional CLI, governance, and root control-plane scope.
    """,
)

index_path = ROOT / "docs/cli/00-index.md"
index_text = index_path.read_text(encoding="utf-8")
if "Native Toolchain Check" not in index_text:
    index_text = index_text.replace(
        "- [Toolchain Inspection](./toolchain-inspection.md)",
        "- [Toolchain Inspection](./toolchain-inspection.md)\n- [Native Toolchain Check](./toolchain-check.md)",
    )
    index_path.write_text(index_text, encoding="utf-8")
    print("updated docs/cli/00-index.md")

check_path = ROOT / "scripts/check-rust-workspace.sh"
check_text = check_path.read_text(encoding="utf-8")

if '"docs/cli/toolchain-check.md",' not in check_text:
    check_text = check_text.replace(
        '"docs/cli/toolchain-inspection.md",',
        '"docs/cli/toolchain-inspection.md",\n        "docs/cli/toolchain-check.md",',
    )

if 'cargo run -p monad-cli -- check toolchain | grep "engine: native" >/dev/null' not in check_text:
    check_text = check_text.replace(
        "cargo run -p monad-cli -- check all >/dev/null",
        'cargo run -p monad-cli -- check all >/dev/null\ncargo run -p monad-cli -- check toolchain | grep "engine: native" >/dev/null',
    )

check_path.write_text(check_text, encoding="utf-8")
print("updated scripts/check-rust-workspace.sh")

print("toolchain check engine generated")

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


insert_before = "\n    #[cfg(test)]\n    mod tests {\n"

toolchain_engine = r'''
    /// Expected root toolchain files for the Monad Factory repository control plane.
    pub const EXPECTED_TOOLCHAIN_FILES: &[&str] = &[
        "mise.toml",
        "package.json",
        "bun.lock",
        "tsconfig.base.json",
        "biome.json",
        "lefthook.yml",
        ".moon/workspace.yml",
        ".moon/toolchains.yml",
        "moon.yml",
        "Cargo.toml",
        "Cargo.lock",
        "rust-toolchain.toml",
        "rustfmt.toml",
        ".cargo/config.toml",
    ];

    /// Expected tool declarations in `mise.toml`.
    pub const EXPECTED_MISE_TOOLS: &[&str] = &["node", "bun", "rust", "go", "python", "java"];

    /// Inspection result for one expected toolchain file.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct ToolchainFile {
        /// File path relative to the repository root.
        pub relative_path: String,

        /// Absolute file path.
        pub path: PathBuf,

        /// Whether the file exists.
        pub exists: bool,
    }

    /// Inspection result for one expected declared tool in `mise.toml`.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct DeclaredTool {
        /// Tool name.
        pub name: String,

        /// Whether the tool is declared.
        pub declared: bool,

        /// Raw configured version or channel, when present.
        pub version: Option<String>,
    }

    /// Root toolchain inspection report.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct ToolchainInspection {
        /// Canonical repository root.
        pub root: PathBuf,

        /// Expected toolchain file inspection results.
        pub files: Vec<ToolchainFile>,

        /// Expected mise tool declarations.
        pub declared_tools: Vec<DeclaredTool>,

        /// Bun package manager value from `package.json`, when present.
        pub package_manager: Option<String>,

        /// Whether package scripts include `check`.
        pub check_script_status: CheckStatus,

        /// Whether package scripts include `check:toolchain`.
        pub toolchain_check_script_status: CheckStatus,

        /// Whether package scripts include `check:rust`.
        pub rust_check_script_status: CheckStatus,

        /// Whether moon workspace configuration exists.
        pub moon_workspace_status: CheckStatus,

        /// Whether moon toolchain configuration exists.
        pub moon_toolchains_status: CheckStatus,

        /// Whether Cargo workspace configuration exists.
        pub cargo_workspace_status: CheckStatus,

        /// Rust toolchain channel from `rust-toolchain.toml`, when present.
        pub rust_toolchain_channel: Option<String>,
    }

    impl ToolchainInspection {
        /// Count present expected toolchain files.
        #[must_use]
        pub fn present_file_count(&self) -> usize {
            self.files.iter().filter(|file| file.exists).count()
        }

        /// Count declared mise tools.
        #[must_use]
        pub fn declared_tool_count(&self) -> usize {
            self.declared_tools
                .iter()
                .filter(|tool| tool.declared)
                .count()
        }

        /// Return missing expected toolchain files.
        #[must_use]
        pub fn missing_file_names(&self) -> Vec<&str> {
            self.files
                .iter()
                .filter(|file| !file.exists)
                .map(|file| file.relative_path.as_str())
                .collect()
        }

        /// Return missing expected mise tool declarations.
        #[must_use]
        pub fn missing_tool_names(&self) -> Vec<&str> {
            self.declared_tools
                .iter()
                .filter(|tool| !tool.declared)
                .map(|tool| tool.name.as_str())
                .collect()
        }

        /// Return whether the root toolchain foundation is complete.
        #[must_use]
        pub fn is_complete(&self) -> bool {
            self.missing_file_names().is_empty()
                && self.missing_tool_names().is_empty()
                && self.package_manager.is_some()
                && self.check_script_status == CheckStatus::Pass
                && self.toolchain_check_script_status == CheckStatus::Pass
                && self.rust_check_script_status == CheckStatus::Pass
                && self.moon_workspace_status == CheckStatus::Pass
                && self.moon_toolchains_status == CheckStatus::Pass
                && self.cargo_workspace_status == CheckStatus::Pass
                && self.rust_toolchain_channel.is_some()
        }
    }

    /// Inspect root toolchain manifests and configuration.
    ///
    /// # Errors
    ///
    /// Returns an error when workspace discovery fails.
    pub fn inspect_toolchain(root: &Path) -> Result<ToolchainInspection, WorkspaceInspectionError> {
        let workspace = inspect_workspace(root)?;
        let root = workspace.root;

        let files = EXPECTED_TOOLCHAIN_FILES
            .iter()
            .map(|relative_path| {
                let path = root.join(relative_path);

                ToolchainFile {
                    relative_path: (*relative_path).to_string(),
                    exists: path.is_file(),
                    path,
                }
            })
            .collect::<Vec<_>>();

        let mise_text = read_optional(root.join("mise.toml"));
        let package_text = read_optional(root.join("package.json"));
        let cargo_text = read_optional(root.join("Cargo.toml"));
        let rust_toolchain_text = read_optional(root.join("rust-toolchain.toml"));

        let declared_tools = EXPECTED_MISE_TOOLS
            .iter()
            .map(|tool| DeclaredTool {
                name: (*tool).to_string(),
                declared: find_toml_assignment(&mise_text, tool).is_some(),
                version: find_toml_assignment(&mise_text, tool),
            })
            .collect::<Vec<_>>();

        let package_manager = find_json_string_value(&package_text, "packageManager");
        let rust_toolchain_channel = find_toml_assignment(&rust_toolchain_text, "channel");

        Ok(ToolchainInspection {
            root: root.clone(),
            files,
            declared_tools,
            package_manager,
            check_script_status: presence_status(package_text.contains("\"check\"")),
            toolchain_check_script_status: presence_status(package_text.contains("\"check:toolchain\"")),
            rust_check_script_status: presence_status(package_text.contains("\"check:rust\"")),
            moon_workspace_status: presence_status(root.join(".moon/workspace.yml").is_file()),
            moon_toolchains_status: presence_status(root.join(".moon/toolchains.yml").is_file()),
            cargo_workspace_status: presence_status(cargo_text.contains("[workspace]")),
            rust_toolchain_channel,
        })
    }

    fn read_optional(path: PathBuf) -> String {
        fs::read_to_string(path).unwrap_or_default()
    }

    fn find_toml_assignment(text: &str, key: &str) -> Option<String> {
        let prefix = format!("{key} =");

        text.lines()
            .map(str::trim)
            .find(|line| line.starts_with(&prefix))
            .and_then(|line| line.split_once('='))
            .map(|(_, value)| clean_manifest_value(value))
            .filter(|value| !value.is_empty())
    }

    fn find_json_string_value(text: &str, key: &str) -> Option<String> {
        let marker = format!("\"{key}\"");

        text.lines()
            .map(str::trim)
            .find(|line| line.starts_with(&marker))
            .and_then(|line| line.split_once(':'))
            .map(|(_, value)| clean_manifest_value(value))
            .filter(|value| !value.is_empty())
    }

    const fn presence_status(present: bool) -> CheckStatus {
    if present {
        CheckStatus::Pass
    } else {
        CheckStatus::Fail
    }
}

fn clean_manifest_value(value: &str) -> String {
        value
            .trim()
            .trim_end_matches(',')
            .trim()
            .trim_matches('"')
            .trim_matches('\'')
            .to_string()
    }
'''

if "pub struct ToolchainInspection" not in core_text:
    insert_before = next((candidate for candidate in insert_candidates if candidate in core_text), None)

    if insert_before is None:
        raise SystemExit(
            "Could not find insertion point in monad-core/src/lib.rs. "
            "Expected a crate-root #[cfg(test)] mod tests block."
        )

    core_text = core_text.replace(insert_before, toolchain_engine + insert_before)
    core_path.write_text(core_text, encoding="utf-8")
    print("updated crates/monad-core/src/lib.rs")
else:
    print("crates/monad-core/src/lib.rs already contains toolchain inspection engine")


write_file(
    "crates/monad-cli/src/commands/inspect.rs",
    r'''
    //! Inspect command renderer.

    use std::path::Path;

    use monad_core::{
        inspect_toolchain, inspect_workspace, ToolchainInspection, WorkspaceInspection,
    };

    use crate::commands::unknown_argument;

    const TARGETS: &[&str] = &["workspace", "scope", "toolchain", "memory"];

    /// Render an inspect command response.
    pub fn render(args: &[String]) -> Result<String, String> {
        let target = args.first().map_or("workspace", String::as_str);

        match target {
            "workspace" => workspace(),
            "scope" => Ok(scope()),
            "toolchain" => toolchain(),
            "memory" => Ok(memory()),
            "--help" | "-h" | "help" => Ok(help()),
            unknown => Err(unknown_argument("inspect", unknown, TARGETS)),
        }
    }

    fn workspace() -> Result<String, String> {
        let inspection = inspect_workspace(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_workspace_inspection(&inspection))
    }

    fn render_workspace_inspection(inspection: &WorkspaceInspection) -> String {
        let missing_domains = inspection.missing_domain_names();
        let missing_files = inspection.missing_foundation_file_names();

        let mut lines = vec![
            "inspect_target: workspace".to_string(),
            format!("workspace_root: {}", inspection.root.display()),
            "workspace_manifest: workspace.toml".to_string(),
            format!(
                "workspace_manifest_loaded: {}",
                inspection.workspace_manifest_loaded
            ),
            format!(
                "workspace_manifest_lines: {}",
                inspection.workspace_manifest_line_count
            ),
            format!(
                "top_level_domains_present: {}/{}",
                inspection.present_domain_count(),
                inspection.domains.len()
            ),
            format!(
                "foundation_files_present: {}/{}",
                inspection.present_foundation_file_count(),
                inspection.foundation_files.len()
            ),
            format!("missing_domains: {}", render_missing_values(&missing_domains)),
            format!("missing_foundation_files: {}", render_missing_values(&missing_files)),
            format!(
                "status: {}",
                if inspection.is_complete() {
                    "complete"
                } else {
                    "incomplete"
                }
            ),
            "domains:".to_string(),
        ];

        for domain in &inspection.domains {
            lines.push(format!(
                "  - {}: {} entries={}",
                domain.name,
                if domain.exists { "present" } else { "missing" },
                domain.entry_count
            ));
        }

        lines.push("foundation_files:".to_string());

        for file in &inspection.foundation_files {
            lines.push(format!(
                "  - {}: {}",
                file.relative_path,
                if file.exists { "present" } else { "missing" }
            ));
        }

        lines.join("\n")
    }

    fn render_missing_values(values: &[&str]) -> String {
        if values.is_empty() {
            "none".to_string()
        } else {
            values.join(", ")
        }
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

    fn toolchain() -> Result<String, String> {
        let inspection = inspect_toolchain(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_toolchain_inspection(&inspection))
    }

    fn render_toolchain_inspection(inspection: &ToolchainInspection) -> String {
        let missing_files = inspection.missing_file_names();
        let missing_tools = inspection.missing_tool_names();

        let mut lines = vec![
            "inspect_target: toolchain".to_string(),
            "engine: native".to_string(),
            format!("workspace_root: {}", inspection.root.display()),
            format!(
                "toolchain_files_present: {}/{}",
                inspection.present_file_count(),
                inspection.files.len()
            ),
            format!(
                "mise_tools_declared: {}/{}",
                inspection.declared_tool_count(),
                inspection.declared_tools.len()
            ),
            format!("missing_toolchain_files: {}", render_missing_values(&missing_files)),
            format!("missing_mise_tools: {}", render_missing_values(&missing_tools)),
            format!(
                "package_manager: {}",
                inspection.package_manager.as_deref().unwrap_or("missing")
            ),
            format!(
                "rust_toolchain_channel: {}",
                inspection
                    .rust_toolchain_channel
                    .as_deref()
                    .unwrap_or("missing")
            ),
            format!("check_script_status: {}", inspection.check_script_status),
            format!(
                "toolchain_check_script_status: {}",
                inspection.toolchain_check_script_status
            ),
            format!("rust_check_script_status: {}", inspection.rust_check_script_status),
            format!("moon_workspace_status: {}", inspection.moon_workspace_status),
            format!("moon_toolchains_status: {}", inspection.moon_toolchains_status),
            format!("cargo_workspace_status: {}", inspection.cargo_workspace_status),
            format!(
                "status: {}",
                if inspection.is_complete() {
                    "complete"
                } else {
                    "incomplete"
                }
            ),
            "declared_tools:".to_string(),
        ];

        for tool in &inspection.declared_tools {
            lines.push(format!(
                "  - {}: {} version={}",
                tool.name,
                if tool.declared { "present" } else { "missing" },
                tool.version.as_deref().unwrap_or("missing")
            ));
        }

        lines.push("toolchain_files:".to_string());

        for file in &inspection.files {
            lines.push(format!(
                "  - {}: {}",
                file.relative_path,
                if file.exists { "present" } else { "missing" }
            ));
        }

        lines.join("\n")
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

        #[test]
        fn renders_real_workspace_inspection() -> Result<(), String> {
            let output = render(&args(&["workspace"]))?;

            assert!(output.contains("workspace_manifest_loaded: true"));
            assert!(output.contains("top_level_domains_present:"));
            assert!(output.contains("foundation_files_present:"));
            assert!(output.contains("domains:"));
            assert!(output.contains("foundation_files:"));

            Ok(())
        }

        #[test]
        fn renders_real_toolchain_inspection() -> Result<(), String> {
            let output = render(&args(&["toolchain"]))?;

            assert!(output.contains("inspect_target: toolchain"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("toolchain_files_present:"));
            assert!(output.contains("mise_tools_declared:"));
            assert!(output.contains("declared_tools:"));

            Ok(())
        }
    }
    ''',
)

write_file(
    "docs/cli/toolchain-inspection.md",
    """
    # Toolchain Inspection

    `monad inspect toolchain` runs a native inspection pass over the root development control plane.

    Example:

    ```bash
    cargo run -p monad-cli -- inspect toolchain
    ```

    The command currently reports:

    - expected root toolchain files
    - expected `mise.toml` tool declarations
    - Bun package manager declaration
    - Rust toolchain channel declaration
    - root check script presence
    - moon workspace/toolchain configuration presence
    - Cargo workspace presence

    This is part of the approved v1 maximal functional CLI and governance scope. It does not replace deeper future validation; it establishes the first native inspection engine for the root toolchain.
    """,
)

index_path = ROOT / "docs/cli/00-index.md"
index_text = index_path.read_text(encoding="utf-8")
if "Toolchain Inspection" not in index_text:
    index_text = index_text.replace(
        "- [Native Foundation Check](./foundation-check.md)",
        "- [Native Foundation Check](./foundation-check.md)\n- [Toolchain Inspection](./toolchain-inspection.md)",
    )
    index_path.write_text(index_text, encoding="utf-8")
    print("updated docs/cli/00-index.md")

check_path = ROOT / "scripts/check-rust-workspace.sh"
check_text = check_path.read_text(encoding="utf-8")

if '"docs/cli/toolchain-inspection.md",' not in check_text:
    check_text = check_text.replace(
        '"docs/cli/foundation-check.md",',
        '"docs/cli/foundation-check.md",\n        "docs/cli/toolchain-inspection.md",',
    )

if 'cargo run -p monad-cli -- inspect toolchain | grep "engine: native" >/dev/null' not in check_text:
    check_text = check_text.replace(
        "cargo run -p monad-cli -- inspect scope >/dev/null",
        'cargo run -p monad-cli -- inspect scope >/dev/null\ncargo run -p monad-cli -- inspect toolchain | grep "engine: native" >/dev/null',
    )

check_path.write_text(check_text, encoding="utf-8")
print("updated scripts/check-rust-workspace.sh")

print("toolchain inspection engine generated")

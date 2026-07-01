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

if "mod memory;" not in lib_text:
    marker = "/// Canonical product name."
    if marker not in lib_text:
        raise SystemExit("Could not find canonical product marker in crates/monad-core/src/lib.rs")

    insertion = '''
mod memory;

pub use memory::{
    inspect_memory, MemoryBackend, MemoryFile, MemoryInspection, EXPECTED_MEMORY_FILES,
    MEMORY_INDEX_PATH, MEMORY_POLICY_PATH, PLANNED_MEMORY_BACKENDS,
};

'''
    lib_text = lib_text.replace(marker, insertion + marker)
    lib_path.write_text(lib_text, encoding="utf-8")
    print("updated crates/monad-core/src/lib.rs")
else:
    print("crates/monad-core/src/lib.rs already declares memory module")


write_file(
    "crates/monad-core/src/memory.rs",
    r'''
    //! Native memory foundation inspection for Monad Factory.

    use std::fs;
    use std::path::{Path, PathBuf};

    use crate::{inspect_workspace, CheckStatus, WorkspaceInspectionError};

    /// Canonical local Monad Memory index path.
    pub const MEMORY_INDEX_PATH: &str = ".monad/memory/MEMORY.md";

    /// Canonical memory governance policy path.
    pub const MEMORY_POLICY_PATH: &str = "policies/memory/memory-policy.md";

    /// Expected files for the current native memory foundation.
    pub const EXPECTED_MEMORY_FILES: &[&str] = &[
        MEMORY_INDEX_PATH,
        MEMORY_POLICY_PATH,
        ".monad/config.toml",
        "docs/memory/00-index.md",
        "docs/product/v1-maximal-functional-scope-and-delivery-plan.md",
    ];

    /// Planned memory backends in approved v1 scope.
    pub const PLANNED_MEMORY_BACKENDS: &[&str] = &["sqlite", "pgvector", "qdrant"];

    /// Inspection result for one memory-related file.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct MemoryFile {
        /// File path relative to the repository root.
        pub relative_path: String,

        /// Absolute file path.
        pub path: PathBuf,

        /// Presence status.
        pub status: CheckStatus,

        /// Number of lines in the file when present.
        pub line_count: usize,
    }

    /// Inspection result for one planned memory backend.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct MemoryBackend {
        /// Backend name.
        pub name: String,

        /// Backend role in the v1 memory architecture.
        pub role: String,

        /// Backend registration status.
        pub status: CheckStatus,
    }

    /// Native memory inspection report.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct MemoryInspection {
        /// Canonical repository root.
        pub root: PathBuf,

        /// Memory foundation files.
        pub files: Vec<MemoryFile>,

        /// Planned memory backends.
        pub backends: Vec<MemoryBackend>,

        /// Status for local-first memory policy language in the memory policy.
        pub local_first_policy_status: CheckStatus,

        /// Status for inspectable memory policy language in the memory policy.
        pub inspectable_policy_status: CheckStatus,

        /// Status for policy-governed memory language in the memory policy.
        pub policy_governed_status: CheckStatus,
    }

    impl MemoryInspection {
        /// Count present memory files.
        #[must_use]
        pub fn present_file_count(&self) -> usize {
            self.files
                .iter()
                .filter(|file| file.status == CheckStatus::Pass)
                .count()
        }

        /// Count registered memory backends.
        #[must_use]
        pub fn registered_backend_count(&self) -> usize {
            self.backends
                .iter()
                .filter(|backend| backend.status == CheckStatus::Pass)
                .count()
        }

        /// Return missing expected memory files.
        #[must_use]
        pub fn missing_file_names(&self) -> Vec<&str> {
            self.files
                .iter()
                .filter(|file| file.status == CheckStatus::Fail)
                .map(|file| file.relative_path.as_str())
                .collect()
        }

        /// Return whether the native memory foundation is complete.
        #[must_use]
        pub fn is_complete(&self) -> bool {
            self.missing_file_names().is_empty()
                && self.local_first_policy_status == CheckStatus::Pass
                && self.inspectable_policy_status == CheckStatus::Pass
                && self.policy_governed_status == CheckStatus::Pass
                && self
                    .backends
                    .iter()
                    .all(|backend| backend.status == CheckStatus::Pass)
        }
    }

    /// Inspect the native Monad Memory foundation.
    ///
    /// # Errors
    ///
    /// Returns an error when workspace discovery fails.
    pub fn inspect_memory(root: &Path) -> Result<MemoryInspection, WorkspaceInspectionError> {
        let workspace = inspect_workspace(root)?;
        let root = workspace.root;

        let files = EXPECTED_MEMORY_FILES
            .iter()
            .map(|relative_path| inspect_memory_file(&root, relative_path))
            .collect::<Vec<_>>();

        let memory_policy_text = read_optional(root.join(MEMORY_POLICY_PATH));
        let memory_index_text = read_optional(root.join(MEMORY_INDEX_PATH));

        let combined_memory_text = format!("{memory_policy_text}\n{memory_index_text}");

        Ok(MemoryInspection {
            root,
            files,
            backends: planned_backends(&combined_memory_text),
            local_first_policy_status: contains_status(&combined_memory_text, "local-first"),
            inspectable_policy_status: contains_status(&combined_memory_text, "inspectable"),
            policy_governed_status: contains_status(&combined_memory_text, "policy-governed"),
        })
    }

    fn inspect_memory_file(root: &Path, relative_path: &str) -> MemoryFile {
        let path = root.join(relative_path);
        let text = read_optional(path.clone());

        MemoryFile {
            relative_path: relative_path.to_string(),
            status: presence_status(path.is_file()),
            line_count: text.lines().count(),
            path,
        }
    }

    fn planned_backends(memory_text: &str) -> Vec<MemoryBackend> {
        PLANNED_MEMORY_BACKENDS
            .iter()
            .map(|backend| MemoryBackend {
                name: (*backend).to_string(),
                role: backend_role(backend).to_string(),
                status: contains_status(memory_text, backend),
            })
            .collect()
    }

    const fn backend_role(backend: &str) -> &'static str {
        match backend.as_bytes() {
            b"sqlite" => "local durable memory store",
            b"pgvector" => "semantic memory inside PostgreSQL",
            b"qdrant" => "external vector retrieval accelerator",
            _ => "planned memory backend",
        }
    }

    fn contains_status(text: &str, needle: &str) -> CheckStatus {
        presence_status(text.to_lowercase().contains(&needle.to_lowercase()))
    }

    const fn presence_status(present: bool) -> CheckStatus {
        if present {
            CheckStatus::Pass
        } else {
            CheckStatus::Fail
        }
    }

    fn read_optional(path: PathBuf) -> String {
        fs::read_to_string(path).unwrap_or_default()
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn backend_roles_are_stable() {
            assert_eq!(backend_role("sqlite"), "local durable memory store");
            assert_eq!(backend_role("pgvector"), "semantic memory inside PostgreSQL");
            assert_eq!(backend_role("qdrant"), "external vector retrieval accelerator");
        }

        #[test]
        fn planned_backend_names_are_registered() {
            let backends = planned_backends("sqlite pgvector qdrant");

            assert_eq!(backends.len(), 3);
            assert!(backends.iter().all(|backend| backend.status == CheckStatus::Pass));
        }
    }
    ''',
)

write_file(
    "crates/monad-cli/src/commands/inspect.rs",
    r'''
    //! Inspect command renderer.

    use std::path::Path;

    use monad_core::{
        inspect_memory, inspect_toolchain, inspect_workspace, MemoryInspection, ToolchainInspection,
        WorkspaceInspection,
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
            "memory" => memory(),
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

    fn memory() -> Result<String, String> {
        let inspection = inspect_memory(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_memory_inspection(&inspection))
    }

    fn render_memory_inspection(inspection: &MemoryInspection) -> String {
        let missing_files = inspection.missing_file_names();

        let mut lines = vec![
            "inspect_target: memory".to_string(),
            "engine: native".to_string(),
            format!("workspace_root: {}", inspection.root.display()),
            format!(
                "memory_files_present: {}/{}",
                inspection.present_file_count(),
                inspection.files.len()
            ),
            format!(
                "memory_backends_registered: {}/{}",
                inspection.registered_backend_count(),
                inspection.backends.len()
            ),
            format!("missing_memory_files: {}", render_missing_values(&missing_files)),
            format!(
                "local_first_policy_status: {}",
                inspection.local_first_policy_status
            ),
            format!(
                "inspectable_policy_status: {}",
                inspection.inspectable_policy_status
            ),
            format!("policy_governed_status: {}", inspection.policy_governed_status),
            format!(
                "status: {}",
                if inspection.is_complete() {
                    "complete"
                } else {
                    "incomplete"
                }
            ),
            "memory_files:".to_string(),
        ];

        for file in &inspection.files {
            lines.push(format!(
                "  - {}: {} lines={}",
                file.relative_path, file.status, file.line_count
            ));
        }

        lines.push("memory_backends:".to_string());

        for backend in &inspection.backends {
            lines.push(format!(
                "  - {}: {} role={}",
                backend.name, backend.status, backend.role
            ));
        }

        lines.join("\n")
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

        #[test]
        fn renders_real_memory_inspection() -> Result<(), String> {
            let output = render(&args(&["memory"]))?;

            assert!(output.contains("inspect_target: memory"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("memory_files_present:"));
            assert!(output.contains("memory_backends_registered:"));
            assert!(output.contains("memory_backends:"));

            Ok(())
        }
    }
    ''',
)

write_file(
    "docs/cli/memory-inspection.md",
    """
    # Memory Inspection

    `monad inspect memory` runs a native inspection pass over the local-first Monad Memory foundation.

    Example:

    ```bash
    cargo run -p monad-cli -- inspect memory
    ```

    Current inspection includes:

    - `.monad/memory/MEMORY.md`
    - `policies/memory/memory-policy.md`
    - `.monad/config.toml`
    - `docs/memory/00-index.md`
    - canonical v1 scope document presence
    - planned memory backend registration for SQLite, pgvector, and Qdrant
    - local-first, inspectable, and policy-governed memory language

    This is part of the approved v1 maximal functional memory, governance, CLI, and AI-readiness scope.
    """,
)

index_path = ROOT / "docs/cli/00-index.md"
index_text = index_path.read_text(encoding="utf-8")
if "Memory Inspection" not in index_text:
    index_text = index_text.replace(
        "- [Native Toolchain Check](./toolchain-check.md)",
        "- [Native Toolchain Check](./toolchain-check.md)\n- [Memory Inspection](./memory-inspection.md)",
    )
    index_path.write_text(index_text, encoding="utf-8")
    print("updated docs/cli/00-index.md")

check_path = ROOT / "scripts/check-rust-workspace.sh"
check_text = check_path.read_text(encoding="utf-8")

if '"crates/monad-core/src/memory.rs",' not in check_text:
    check_text = check_text.replace(
        '"crates/monad-core/src/lib.rs",',
        '"crates/monad-core/src/lib.rs",\n        "crates/monad-core/src/memory.rs",',
    )

if '"docs/cli/memory-inspection.md",' not in check_text:
    check_text = check_text.replace(
        '"docs/cli/toolchain-check.md",',
        '"docs/cli/toolchain-check.md",\n        "docs/cli/memory-inspection.md",',
    )

if 'cargo run -p monad-cli -- inspect memory | grep "engine: native" >/dev/null' not in check_text:
    check_text = check_text.replace(
        "cargo run -p monad-cli -- inspect memory >/dev/null",
        'cargo run -p monad-cli -- inspect memory | grep "engine: native" >/dev/null',
    )

check_path.write_text(check_text, encoding="utf-8")
print("updated scripts/check-rust-workspace.sh")

print("memory inspection engine generated")

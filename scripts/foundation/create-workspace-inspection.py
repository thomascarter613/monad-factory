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
    "crates/monad-core/src/lib.rs",
    r'''
    //! Core domain primitives and shared runtime contracts for Monad Factory.

    use std::error::Error;
    use std::fmt::{Display, Formatter};
    use std::fs;
    use std::path::{Path, PathBuf};

    /// Canonical product name.
    pub const PRODUCT_NAME: &str = "Monad Factory";

    /// Canonical public CLI command name.
    pub const CLI_NAME: &str = "monad";

    /// Current implementation phase.
    pub const IMPLEMENTATION_PHASE: &str = "pre-implementation foundation";

    /// Expected top-level repository domains for the maximal functional v1 foundation.
    pub const EXPECTED_TOP_LEVEL_DOMAINS: &[&str] = &[
        "apps",
        "contracts",
        "crates",
        "docs",
        "examples",
        "infra",
        "marketplace",
        "packages",
        "plugins",
        "policies",
        "scripts",
        "services",
        "templates",
    ];

    /// Expected foundation files that anchor the approved repository baseline.
    pub const EXPECTED_FOUNDATION_FILES: &[&str] = &[
        "workspace.toml",
        "mise.toml",
        "package.json",
        "Cargo.toml",
        "docs/product/v1-maximal-functional-scope-and-delivery-plan.md",
        "docs/adr/00-index.md",
        ".monad/config.toml",
        ".monad/memory/MEMORY.md",
        ".github/workflows/ci.yml",
        "scripts/check-foundation.sh",
        "scripts/check-root-toolchain.sh",
        "scripts/check-rust-workspace.sh",
    ];

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

    /// Inspection result for one expected top-level repository domain.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct WorkspaceDomain {
        /// Domain directory name.
        pub name: String,

        /// Absolute domain path.
        pub path: PathBuf,

        /// Whether the domain directory exists.
        pub exists: bool,

        /// Number of direct entries inside the domain directory.
        pub entry_count: usize,
    }

    /// Inspection result for one expected foundation file.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct WorkspaceFile {
        /// File path relative to the repository root.
        pub relative_path: String,

        /// Absolute file path.
        pub path: PathBuf,

        /// Whether the file exists.
        pub exists: bool,
    }

    /// Inspection result for the repository workspace.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct WorkspaceInspection {
        /// Canonical repository root.
        pub root: PathBuf,

        /// Absolute path to `workspace.toml`.
        pub workspace_manifest: PathBuf,

        /// Whether the workspace manifest was loaded.
        pub workspace_manifest_loaded: bool,

        /// Number of lines in `workspace.toml`.
        pub workspace_manifest_line_count: usize,

        /// Expected top-level domain inspection results.
        pub domains: Vec<WorkspaceDomain>,

        /// Expected foundation file inspection results.
        pub foundation_files: Vec<WorkspaceFile>,
    }

    impl WorkspaceInspection {
        /// Count present top-level domains.
        #[must_use]
        pub fn present_domain_count(&self) -> usize {
            self.domains.iter().filter(|domain| domain.exists).count()
        }

        /// Count present foundation files.
        #[must_use]
        pub fn present_foundation_file_count(&self) -> usize {
            self.foundation_files.iter().filter(|file| file.exists).count()
        }

        /// Return missing top-level domain names.
        #[must_use]
        pub fn missing_domain_names(&self) -> Vec<&str> {
            self.domains
                .iter()
                .filter(|domain| !domain.exists)
                .map(|domain| domain.name.as_str())
                .collect()
        }

        /// Return missing foundation file paths.
        #[must_use]
        pub fn missing_foundation_file_names(&self) -> Vec<&str> {
            self.foundation_files
                .iter()
                .filter(|file| !file.exists)
                .map(|file| file.relative_path.as_str())
                .collect()
        }

        /// Return whether all expected domains and foundation files are present.
        #[must_use]
        pub fn is_complete(&self) -> bool {
            self.missing_domain_names().is_empty() && self.missing_foundation_file_names().is_empty()
        }
    }

    /// Error returned when workspace inspection fails.
    #[derive(Debug)]
    pub struct WorkspaceInspectionError {
        message: String,
        source: Option<std::io::Error>,
    }

    impl WorkspaceInspectionError {
        fn new(message: impl Into<String>) -> Self {
            Self {
                message: message.into(),
                source: None,
            }
        }

        fn with_source(message: impl Into<String>, source: std::io::Error) -> Self {
            Self {
                message: message.into(),
                source: Some(source),
            }
        }
    }

    impl Display for WorkspaceInspectionError {
        fn fmt(&self, formatter: &mut Formatter<'_>) -> std::fmt::Result {
            formatter.write_str(&self.message)
        }
    }

    impl Error for WorkspaceInspectionError {
        fn source(&self) -> Option<&(dyn Error + 'static)> {
            self.source
                .as_ref()
                .map(|source| source as &(dyn Error + 'static))
        }
    }

    /// Inspect a Monad Factory workspace root.
    ///
    /// # Errors
    ///
    /// Returns an error when the root cannot be canonicalized, `workspace.toml`
    /// cannot be read, or a present expected domain cannot be inspected.
    pub fn inspect_workspace(root: &Path) -> Result<WorkspaceInspection, WorkspaceInspectionError> {
        let canonical_start = fs::canonicalize(root).map_err(|source| {
            WorkspaceInspectionError::with_source(
                format!("failed to canonicalize workspace root `{}`", root.display()),
                source,
            )
        })?;

        if !canonical_start.is_dir() {
            return Err(WorkspaceInspectionError::new(format!(
                "workspace root `{}` is not a directory",
                canonical_start.display()
            )));
        }

        let workspace_root = discover_workspace_root(&canonical_start)?;
        let workspace_manifest = workspace_root.join("workspace.toml");

        let manifest_text = fs::read_to_string(&workspace_manifest).map_err(|source| {
            WorkspaceInspectionError::with_source(
                format!(
                    "failed to read workspace manifest `{}`",
                    workspace_manifest.display()
                ),
                source,
            )
        })?;

        let domains = EXPECTED_TOP_LEVEL_DOMAINS
            .iter()
            .map(|domain| inspect_domain(&workspace_root, domain))
            .collect::<Result<Vec<_>, _>>()?;

        let foundation_files = EXPECTED_FOUNDATION_FILES
            .iter()
            .map(|relative_path| inspect_foundation_file(&workspace_root, relative_path))
            .collect();

        Ok(WorkspaceInspection {
            root: workspace_root,
            workspace_manifest,
            workspace_manifest_loaded: true,
            workspace_manifest_line_count: manifest_text.lines().count(),
            domains,
            foundation_files,
        })
    }

    fn discover_workspace_root(start: &Path) -> Result<PathBuf, WorkspaceInspectionError> {
        for candidate in start.ancestors() {
            let workspace_manifest = candidate.join("workspace.toml");
            let canonical_scope = candidate
                .join("docs")
                .join("product")
                .join("v1-maximal-functional-scope-and-delivery-plan.md");

            if workspace_manifest.is_file() && canonical_scope.is_file() {
                return Ok(candidate.to_path_buf());
            }
        }

        Err(WorkspaceInspectionError::new(format!(
            "failed to discover Monad Factory workspace root from `{}`",
            start.display()
        )))
    }

    fn inspect_domain(
        root: &Path,
        name: &str,
    ) -> Result<WorkspaceDomain, WorkspaceInspectionError> {
        let path = root.join(name);
        let exists = path.is_dir();

        let entry_count = if exists {
            count_directory_entries(&path)?
        } else {
            0
        };

        Ok(WorkspaceDomain {
            name: name.to_string(),
            path,
            exists,
            entry_count,
        })
    }

    fn inspect_foundation_file(root: &Path, relative_path: &str) -> WorkspaceFile {
        let path = root.join(relative_path);

        WorkspaceFile {
            relative_path: relative_path.to_string(),
            exists: path.is_file(),
            path,
        }
    }

    fn count_directory_entries(path: &Path) -> Result<usize, WorkspaceInspectionError> {
        let read_dir = fs::read_dir(path).map_err(|source| {
            WorkspaceInspectionError::with_source(
                format!("failed to inspect directory `{}`", path.display()),
                source,
            )
        })?;

        read_dir
            .map(|entry| entry.map(|_| 1usize))
            .try_fold(0usize, |total, count| {
                count.map(|value| total + value).map_err(|source| {
                    WorkspaceInspectionError::with_source(
                        format!("failed to read entry in `{}`", path.display()),
                        source,
                    )
                })
            })
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        fn test_workspace(name: &str) -> Result<PathBuf, Box<dyn Error>> {
            let root = std::env::temp_dir().join(format!(
                "monad-core-workspace-inspection-{name}-{}",
                std::process::id()
            ));

            if root.exists() {
                fs::remove_dir_all(&root)?;
            }

            fs::create_dir_all(&root)?;
            fs::write(root.join("workspace.toml"), "name = \"test-workspace\"\n")?;

            for domain in EXPECTED_TOP_LEVEL_DOMAINS {
                fs::create_dir_all(root.join(domain))?;
            }

            for file in EXPECTED_FOUNDATION_FILES {
                let path = root.join(file);

                if let Some(parent) = path.parent() {
                    fs::create_dir_all(parent)?;
                }

                fs::write(path, "")?;
            }

            Ok(root)
        }

        #[test]
        fn build_info_uses_canonical_names() {
            let info = build_info();

            assert_eq!(info.product_name, "Monad Factory");
            assert_eq!(info.cli_name, "monad");
            assert_eq!(info.phase, "pre-implementation foundation");
        }

        #[test]
        fn inspection_reports_complete_workspace() -> Result<(), Box<dyn Error>> {
            let root = test_workspace("complete")?;
            let inspection = inspect_workspace(&root)?;

            assert!(inspection.workspace_manifest_loaded);
            assert_eq!(
                inspection.present_domain_count(),
                EXPECTED_TOP_LEVEL_DOMAINS.len()
            );
            assert_eq!(
                inspection.present_foundation_file_count(),
                EXPECTED_FOUNDATION_FILES.len()
            );
            assert!(inspection.is_complete());

            fs::remove_dir_all(root)?;

            Ok(())
        }

        #[test]
        fn inspection_reports_missing_domain() -> Result<(), Box<dyn Error>> {
            let root = test_workspace("missing-domain")?;
            fs::remove_dir_all(root.join("apps"))?;

            let inspection = inspect_workspace(&root)?;

            assert!(inspection.missing_domain_names().contains(&"apps"));
            assert!(!inspection.is_complete());

            fs::remove_dir_all(root)?;

            Ok(())
        }
    }
    ''',
)

write_file(
    "crates/monad-cli/src/commands/inspect.rs",
    r'''
    //! Inspect command renderer.

    use std::path::Path;

    use monad_core::{inspect_workspace, WorkspaceInspection};

    use crate::commands::unknown_argument;

    const TARGETS: &[&str] = &["workspace", "scope", "toolchain", "memory"];

    /// Render an inspect command response.
    pub fn render(args: &[String]) -> Result<String, String> {
        let target = args.first().map_or("workspace", String::as_str);

        match target {
            "workspace" => workspace(),
            "scope" => Ok(scope()),
            "toolchain" => Ok(toolchain()),
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

        lines
            .extend(["foundation_files:".to_string()]);

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
    }
    ''',
)

write_file(
    "docs/cli/workspace-inspection.md",
    """
    # Workspace Inspection

    `monad inspect workspace` performs the first real repository inspection pass for Monad Factory.

    It reads the actual repository root, verifies that `workspace.toml` can be loaded, checks expected top-level v1 foundation domains, checks expected foundation files, and renders deterministic output for humans and future automation.

    Example:

    ```bash
    cargo run -p monad-cli -- inspect workspace
    ```

    The command currently reports:

    - workspace root
    - workspace manifest load status
    - workspace manifest line count
    - expected top-level domains present
    - expected foundation files present
    - missing domains
    - missing foundation files
    - per-domain entry counts

    This is not a downgrade of the v1 scope. It is the first concrete inspection engine under the approved maximal functional v1 command surface.
    """,
)

# Update CLI index if needed.
index_path = ROOT / "docs/cli/00-index.md"
index_text = index_path.read_text(encoding="utf-8")
if "Workspace Inspection" not in index_text:
    index_text = index_text.replace(
        "- [Command Surface](./command-surface.md)",
        "- [Command Surface](./command-surface.md)\n- [Workspace Inspection](./workspace-inspection.md)",
    )
    index_path.write_text(index_text, encoding="utf-8")
    print("updated docs/cli/00-index.md")

# Strengthen Rust workspace smoke checks.
check_path = ROOT / "scripts/check-rust-workspace.sh"
check_text = check_path.read_text(encoding="utf-8")

if '"docs/cli/workspace-inspection.md",' not in check_text:
    check_text = check_text.replace(
        '"docs/cli/command-surface.md",',
        '"docs/cli/command-surface.md",\n        "docs/cli/workspace-inspection.md",',
    )

if "workspace_manifest_loaded: true" not in check_text:
    check_text = check_text.replace(
        "cargo run -p monad-cli -- inspect workspace >/dev/null",
        "cargo run -p monad-cli -- inspect workspace | grep \"workspace_manifest_loaded: true\" >/dev/null",
    )

check_path.write_text(check_text, encoding="utf-8")
print("updated scripts/check-rust-workspace.sh")

print("workspace inspection engine generated")

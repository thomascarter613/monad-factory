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
        self.foundation_files
            .iter()
            .filter(|file| file.exists)
            .count()
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

fn inspect_domain(root: &Path, name: &str) -> Result<WorkspaceDomain, WorkspaceInspectionError> {
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

/// Status for a native foundation check.
#[derive(Debug, Clone, Copy, Eq, PartialEq)]
pub enum CheckStatus {
    /// The check passed.
    Pass,

    /// The check produced a non-fatal warning.
    Warn,

    /// The check failed.
    Fail,
}

impl CheckStatus {
    /// Return a stable lowercase status string.
    #[must_use]
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Pass => "pass",
            Self::Warn => "warn",
            Self::Fail => "fail",
        }
    }
}

impl Display for CheckStatus {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(self.as_str())
    }
}

/// One native foundation check item.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct FoundationCheckItem {
    /// Stable item name.
    pub name: String,

    /// Check status.
    pub status: CheckStatus,

    /// Human-readable check message.
    pub message: String,
}

/// Native foundation check report.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct FoundationCheckReport {
    /// Workspace root used for the check.
    pub root: PathBuf,

    /// Overall check status.
    pub status: CheckStatus,

    /// Individual check items.
    pub items: Vec<FoundationCheckItem>,

    /// Workspace inspection used by the check.
    pub inspection: WorkspaceInspection,
}

impl FoundationCheckReport {
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

/// Run the native Monad Factory foundation check.
///
/// # Errors
///
/// Returns an error when workspace inspection fails.
pub fn run_foundation_check(
    root: &Path,
) -> Result<FoundationCheckReport, WorkspaceInspectionError> {
    let inspection = inspect_workspace(root)?;
    let mut items = Vec::new();

    items.push(FoundationCheckItem {
        name: "workspace-manifest".to_string(),
        status: CheckStatus::Pass,
        message: format!(
            "`workspace.toml` loaded with {} line(s)",
            inspection.workspace_manifest_line_count
        ),
    });

    let missing_domains = inspection.missing_domain_names();
    items.push(FoundationCheckItem {
        name: "top-level-domains".to_string(),
        status: if missing_domains.is_empty() {
            CheckStatus::Pass
        } else {
            CheckStatus::Fail
        },
        message: if missing_domains.is_empty() {
            format!(
                "all {} expected top-level domains are present",
                inspection.domains.len()
            )
        } else {
            format!("missing domains: {}", missing_domains.join(", "))
        },
    });

    let missing_files = inspection.missing_foundation_file_names();
    items.push(FoundationCheckItem {
        name: "foundation-files".to_string(),
        status: if missing_files.is_empty() {
            CheckStatus::Pass
        } else {
            CheckStatus::Fail
        },
        message: if missing_files.is_empty() {
            format!(
                "all {} expected foundation files are present",
                inspection.foundation_files.len()
            )
        } else {
            format!("missing files: {}", missing_files.join(", "))
        },
    });

    add_required_file_check(
        &mut items,
        &inspection,
        "canonical-v1-scope",
        "docs/product/v1-maximal-functional-scope-and-delivery-plan.md",
    );

    add_required_file_check(
        &mut items,
        &inspection,
        "monad-memory-index",
        ".monad/memory/MEMORY.md",
    );

    add_required_file_check(&mut items, &inspection, "rust-workspace", "Cargo.toml");

    add_required_file_check(&mut items, &inspection, "root-toolchain", "mise.toml");

    let status = if items.iter().any(|item| item.status == CheckStatus::Fail) {
        CheckStatus::Fail
    } else if items.iter().any(|item| item.status == CheckStatus::Warn) {
        CheckStatus::Warn
    } else {
        CheckStatus::Pass
    };

    Ok(FoundationCheckReport {
        root: inspection.root.clone(),
        status,
        items,
        inspection,
    })
}

fn add_required_file_check(
    items: &mut Vec<FoundationCheckItem>,
    inspection: &WorkspaceInspection,
    name: &str,
    relative_path: &str,
) {
    let exists = inspection
        .foundation_files
        .iter()
        .any(|file| file.relative_path == relative_path && file.exists);

    items.push(FoundationCheckItem {
        name: name.to_string(),
        status: if exists {
            CheckStatus::Pass
        } else {
            CheckStatus::Fail
        },
        message: if exists {
            format!("required file `{relative_path}` is present")
        } else {
            format!("required file `{relative_path}` is missing")
        },
    });
}

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
        toolchain_check_script_status: presence_status(
            package_text.contains("\"check:toolchain\""),
        ),
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

    #[test]
    fn foundation_check_passes_for_complete_workspace() -> Result<(), Box<dyn Error>> {
        let root = test_workspace("foundation-pass")?;
        let report = run_foundation_check(&root)?;

        assert_eq!(report.status, CheckStatus::Pass);
        assert_eq!(report.fail_count(), 0);
        assert!(report.pass_count() > 0);

        fs::remove_dir_all(root)?;

        Ok(())
    }

    #[test]
    fn foundation_check_fails_for_missing_file() -> Result<(), Box<dyn Error>> {
        let root = test_workspace("foundation-fail")?;
        fs::remove_file(root.join(".monad/memory/MEMORY.md"))?;

        let report = run_foundation_check(&root)?;

        assert_eq!(report.status, CheckStatus::Fail);
        assert!(report.fail_count() > 0);

        fs::remove_dir_all(root)?;

        Ok(())
    }
}

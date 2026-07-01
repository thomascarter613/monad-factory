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
        assert_eq!(
            backend_role("pgvector"),
            "semantic memory inside PostgreSQL"
        );
        assert_eq!(
            backend_role("qdrant"),
            "external vector retrieval accelerator"
        );
    }

    #[test]
    fn planned_backend_names_are_registered() {
        let backends = planned_backends("sqlite pgvector qdrant");

        assert_eq!(backends.len(), 3);
        assert!(backends
            .iter()
            .all(|backend| backend.status == CheckStatus::Pass));
    }
}

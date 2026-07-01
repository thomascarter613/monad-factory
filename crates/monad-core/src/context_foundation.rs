//! Native context foundation model for handoffs, context packs, and AI exports.

use std::fs;
use std::path::{Path, PathBuf};

use crate::{
    build_repository_graph, inspect_memory, inspect_toolchain, inspect_workspace, CheckStatus,
    WorkspaceInspectionError,
};

/// Stable local context pack identifier for the current repository foundation.
pub const CONTEXT_PACK_ID: &str = "monad-factory-local-context";

/// Planned generated handoff location for future persisted handoff artifacts.
pub const CONTEXT_HANDOFF_PATH: &str = ".monad/context/handoff.md";

/// AI/tool export targets included in the approved v1 command surface.
pub const CONTEXT_EXPORT_TARGETS: &[&str] =
    &["generic-ai", "codex", "claude", "cursor", "github-copilot"];

/// Static context artifact declaration.
#[derive(Debug, Clone, Copy, Eq, PartialEq)]
pub struct ContextArtifactSpec {
    /// Stable artifact name.
    pub name: &'static str,

    /// Artifact path relative to the repository root.
    pub relative_path: &'static str,

    /// Artifact kind.
    pub kind: &'static str,
}

/// Expected artifacts for the current native context foundation.
pub const EXPECTED_CONTEXT_ARTIFACTS: &[ContextArtifactSpec] = &[
    ContextArtifactSpec {
        name: "canonical-v1-scope",
        relative_path: "docs/product/v1-maximal-functional-scope-and-delivery-plan.md",
        kind: "source-of-truth",
    },
    ContextArtifactSpec {
        name: "workspace-manifest",
        relative_path: "workspace.toml",
        kind: "workspace",
    },
    ContextArtifactSpec {
        name: "rust-workspace",
        relative_path: "Cargo.toml",
        kind: "workspace",
    },
    ContextArtifactSpec {
        name: "root-package-manifest",
        relative_path: "package.json",
        kind: "toolchain",
    },
    ContextArtifactSpec {
        name: "monad-memory-index",
        relative_path: ".monad/memory/MEMORY.md",
        kind: "memory",
    },
    ContextArtifactSpec {
        name: "memory-policy",
        relative_path: "policies/memory/memory-policy.md",
        kind: "policy",
    },
    ContextArtifactSpec {
        name: "cli-command-surface",
        relative_path: "docs/cli/command-surface.md",
        kind: "cli",
    },
    ContextArtifactSpec {
        name: "agent-instructions",
        relative_path: "AGENTS.md",
        kind: "agent",
    },
];

/// Inspected context artifact.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct ContextArtifact {
    /// Stable artifact name.
    pub name: String,

    /// Artifact path relative to the repository root.
    pub relative_path: String,

    /// Artifact kind.
    pub kind: String,

    /// Absolute artifact path.
    pub path: PathBuf,

    /// Presence status.
    pub status: CheckStatus,

    /// Line count when the artifact is present and readable.
    pub line_count: usize,
}

/// Native context foundation report.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct ContextFoundation {
    /// Canonical repository root.
    pub root: PathBuf,

    /// Stable context pack id.
    pub pack_id: String,

    /// Planned handoff artifact path.
    pub handoff_path: String,

    /// Inspected context artifacts.
    pub artifacts: Vec<ContextArtifact>,

    /// Registered export targets.
    pub export_targets: Vec<String>,

    /// Workspace domain count from native workspace inspection.
    pub workspace_domain_count: usize,

    /// Graph node count from native graph construction.
    pub graph_node_count: usize,

    /// Registered memory backend count from native memory inspection.
    pub memory_backend_count: usize,

    /// Declared root tool count from native toolchain inspection.
    pub declared_tool_count: usize,
}

impl ContextFoundation {
    /// Count present context artifacts.
    #[must_use]
    pub fn present_artifact_count(&self) -> usize {
        self.artifacts
            .iter()
            .filter(|artifact| artifact.status == CheckStatus::Pass)
            .count()
    }

    /// Return missing context artifact names.
    #[must_use]
    pub fn missing_artifact_names(&self) -> Vec<&str> {
        self.artifacts
            .iter()
            .filter(|artifact| artifact.status == CheckStatus::Fail)
            .map(|artifact| artifact.name.as_str())
            .collect()
    }

    /// Return whether the context foundation is complete.
    #[must_use]
    pub fn is_complete(&self) -> bool {
        self.missing_artifact_names().is_empty()
            && !self.export_targets.is_empty()
            && self.workspace_domain_count > 0
            && self.graph_node_count > 0
            && self.memory_backend_count > 0
            && self.declared_tool_count > 0
    }

    /// Return a stable status for the context foundation.
    #[must_use]
    pub fn status(&self) -> CheckStatus {
        if self.is_complete() {
            CheckStatus::Pass
        } else {
            CheckStatus::Fail
        }
    }
}

/// Inspect the native context foundation.
///
/// # Errors
///
/// Returns an error when workspace, graph, memory, or toolchain inspection fails.
pub fn inspect_context_foundation(
    root: &Path,
) -> Result<ContextFoundation, WorkspaceInspectionError> {
    let workspace = inspect_workspace(root)?;
    let graph = build_repository_graph(root)?;
    let memory = inspect_memory(root)?;
    let toolchain = inspect_toolchain(root)?;

    let artifacts = EXPECTED_CONTEXT_ARTIFACTS
        .iter()
        .map(|spec| inspect_context_artifact(&workspace.root, spec))
        .collect::<Vec<_>>();

    let workspace_domain_count = workspace.present_domain_count();

    Ok(ContextFoundation {
        root: workspace.root,
        pack_id: CONTEXT_PACK_ID.to_string(),
        handoff_path: CONTEXT_HANDOFF_PATH.to_string(),
        artifacts,
        export_targets: CONTEXT_EXPORT_TARGETS
            .iter()
            .map(ToString::to_string)
            .collect(),
        workspace_domain_count,
        graph_node_count: graph.nodes.len(),
        memory_backend_count: memory.registered_backend_count(),
        declared_tool_count: toolchain.declared_tool_count(),
    })
}

fn inspect_context_artifact(root: &Path, spec: &ContextArtifactSpec) -> ContextArtifact {
    let path = root.join(spec.relative_path);
    let text = read_optional(path.clone());

    ContextArtifact {
        name: spec.name.to_string(),
        relative_path: spec.relative_path.to_string(),
        kind: spec.kind.to_string(),
        status: presence_status(path.is_file()),
        line_count: text.lines().count(),
        path,
    }
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
    fn context_export_targets_are_registered() {
        assert!(CONTEXT_EXPORT_TARGETS.contains(&"generic-ai"));
        assert!(CONTEXT_EXPORT_TARGETS.contains(&"codex"));
        assert!(CONTEXT_EXPORT_TARGETS.contains(&"claude"));
        assert!(CONTEXT_EXPORT_TARGETS.contains(&"cursor"));
    }

    #[test]
    fn context_artifact_specs_include_source_of_truth() {
        assert!(EXPECTED_CONTEXT_ARTIFACTS
            .iter()
            .any(|artifact| artifact.name == "canonical-v1-scope"));
    }
}

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

if "mod context_foundation;" not in lib_text:
    if "mod graph;\n" in lib_text:
        lib_text = lib_text.replace("mod graph;\n", "mod graph;\nmod context_foundation;\n")
    elif "mod memory;\n" in lib_text:
        lib_text = lib_text.replace("mod memory;\n", "mod memory;\nmod context_foundation;\n")
    else:
        raise SystemExit("Could not find module insertion point in crates/monad-core/src/lib.rs")

if "pub use context_foundation::" not in lib_text:
    export = '''
pub use context_foundation::{
    inspect_context_foundation, ContextArtifact, ContextArtifactSpec, ContextFoundation,
    CONTEXT_EXPORT_TARGETS, CONTEXT_HANDOFF_PATH, CONTEXT_PACK_ID, EXPECTED_CONTEXT_ARTIFACTS,
};

'''
    if "pub use graph::" in lib_text:
        lib_text = lib_text.replace("pub use graph::", export + "pub use graph::")
    elif "pub use memory::" in lib_text:
        lib_text = lib_text.replace("pub use memory::", export + "pub use memory::")
    else:
        raise SystemExit("Could not find export insertion point in crates/monad-core/src/lib.rs")

lib_path.write_text(lib_text, encoding="utf-8")
print("updated crates/monad-core/src/lib.rs")


write_file(
    "crates/monad-core/src/context_foundation.rs",
    r'''
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
    pub const CONTEXT_EXPORT_TARGETS: &[&str] = &[
        "generic-ai",
        "codex",
        "claude",
        "cursor",
        "github-copilot",
    ];

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
        match fs::read_to_string(path) {
            Ok(text) => text,
            Err(_error) => String::new(),
        }
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
    ''',
)


write_file(
    "crates/monad-cli/src/commands/context.rs",
    r'''
    //! Context command renderer.

    use std::path::Path;

    use monad_core::ContextFoundation;
    use monad_core::{inspect_context_foundation, CONTEXT_HANDOFF_PATH};

    use crate::commands::unknown_argument;

    const COMMANDS: &[&str] = &["help", "pack", "verify", "handoff", "exports"];

    /// Render a context command response.
    pub fn render(args: &[String]) -> Result<String, String> {
        let command = args.first().map_or("help", String::as_str);

        match command {
            "help" | "--help" | "-h" => Ok(help()),
            "pack" => pack(),
            "verify" => verify(),
            "handoff" => handoff(),
            "exports" => exports(),
            unknown => Err(unknown_argument("context", unknown, COMMANDS)),
        }
    }

    fn pack() -> Result<String, String> {
        let foundation =
            inspect_context_foundation(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_pack(&foundation))
    }

    fn verify() -> Result<String, String> {
        let foundation =
            inspect_context_foundation(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_verify(&foundation))
    }

    fn handoff() -> Result<String, String> {
        let foundation =
            inspect_context_foundation(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_handoff(&foundation))
    }

    fn exports() -> Result<String, String> {
        let foundation =
            inspect_context_foundation(Path::new(".")).map_err(|error| error.to_string())?;

        Ok(render_exports(&foundation))
    }

    fn render_pack(foundation: &ContextFoundation) -> String {
        let mut lines = vec![
            "context_command: pack".to_string(),
            "engine: native".to_string(),
            format!("workspace_root: {}", foundation.root.display()),
            format!("pack_id: {}", foundation.pack_id),
            format!(
                "context_artifacts_present: {}/{}",
                foundation.present_artifact_count(),
                foundation.artifacts.len()
            ),
            format!("workspace_domains: {}", foundation.workspace_domain_count),
            format!("graph_nodes: {}", foundation.graph_node_count),
            format!("memory_backends: {}", foundation.memory_backend_count),
            format!("declared_tools: {}", foundation.declared_tool_count),
            format!("status: {}", foundation.status()),
            "artifacts:".to_string(),
        ];

        for artifact in &foundation.artifacts {
            lines.push(format!(
                "  - {}: {} kind={} path={} lines={}",
                artifact.name,
                artifact.status,
                artifact.kind,
                artifact.relative_path,
                artifact.line_count
            ));
        }

        lines.join("\n")
    }

    fn render_verify(foundation: &ContextFoundation) -> String {
        [
            "context_command: verify".to_string(),
            "engine: native".to_string(),
            format!("workspace_root: {}", foundation.root.display()),
            format!("pack_id: {}", foundation.pack_id),
            format!("status: {}", foundation.status()),
            format!(
                "missing_context_artifacts: {}",
                render_missing_values(&foundation.missing_artifact_names())
            ),
            format!(
                "context_artifacts_present: {}/{}",
                foundation.present_artifact_count(),
                foundation.artifacts.len()
            ),
        ]
        .join("\n")
    }

    fn render_handoff(foundation: &ContextFoundation) -> String {
        [
            "context_command: handoff".to_string(),
            "engine: native".to_string(),
            format!("workspace_root: {}", foundation.root.display()),
            format!("pack_id: {}", foundation.pack_id),
            format!("handoff_path: {}", foundation.handoff_path),
            "source_of_truth: docs/product/v1-maximal-functional-scope-and-delivery-plan.md"
                .to_string(),
            "handoff_summary: repository foundation, native checks, memory, graph, and context command surfaces are inspectable through monad".to_string(),
            format!("status: {}", foundation.status()),
        ]
        .join("\n")
    }

    fn render_exports(foundation: &ContextFoundation) -> String {
        let mut lines = vec![
            "context_command: exports".to_string(),
            "engine: native".to_string(),
            format!("workspace_root: {}", foundation.root.display()),
            format!("pack_id: {}", foundation.pack_id),
            format!("export_targets_registered: {}", foundation.export_targets.len()),
            format!("handoff_path: {CONTEXT_HANDOFF_PATH}"),
            "export_targets:".to_string(),
        ];

        for target in &foundation.export_targets {
            lines.push(format!("  - {target}"));
        }

        lines.push(format!("status: {}", foundation.status()));

        lines.join("\n")
    }

    fn render_missing_values(values: &[&str]) -> String {
        if values.is_empty() {
            "none".to_string()
        } else {
            values.join(", ")
        }
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
        fn renders_native_pack_command() -> Result<(), String> {
            let output = render(&args(&["pack"]))?;

            assert!(output.contains("context_command: pack"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("context_artifacts_present:"));

            Ok(())
        }

        #[test]
        fn renders_native_verify_command() -> Result<(), String> {
            let output = render(&args(&["verify"]))?;

            assert!(output.contains("context_command: verify"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("missing_context_artifacts:"));

            Ok(())
        }

        #[test]
        fn renders_handoff_command() -> Result<(), String> {
            let output = render(&args(&["handoff"]))?;

            assert!(output.contains("context_command: handoff"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("source_of_truth"));

            Ok(())
        }

        #[test]
        fn renders_exports_command() -> Result<(), String> {
            let output = render(&args(&["exports"]))?;

            assert!(output.contains("context_command: exports"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("export_targets:"));

            Ok(())
        }
    }
    ''',
)

write_file(
    "docs/cli/context-command.md",
    """
    # Native Context Command Group

    The `monad context` command group exposes native context-pack, verification, handoff, and export state.

    Examples:

    ```bash
    cargo run -p monad-cli -- context pack
    cargo run -p monad-cli -- context verify
    cargo run -p monad-cli -- context handoff
    cargo run -p monad-cli -- context exports
    ```

    Current commands:

    - `monad context pack`
    - `monad context verify`
    - `monad context handoff`
    - `monad context exports`

    The native context foundation currently combines:

    - canonical v1 source-of-truth document
    - workspace manifest
    - Rust workspace manifest
    - root package manifest
    - Monad Memory index
    - memory policy
    - CLI command surface documentation
    - agent instructions
    - repository graph status
    - memory backend status
    - root toolchain declaration status

    This is part of the approved v1 maximal functional context-pack, handoff, AI-tool export, governance, AI-readiness, and CLI scope.
    """,
)

index_path = ROOT / "docs/cli/00-index.md"
index_text = index_path.read_text(encoding="utf-8")
if "Native Context Command Group" not in index_text:
    index_text = index_text.replace(
        "- [Native Graph Command](./graph-command.md)",
        "- [Native Graph Command](./graph-command.md)\n- [Native Context Command Group](./context-command.md)",
    )
    index_path.write_text(index_text, encoding="utf-8")
    print("updated docs/cli/00-index.md")

check_path = ROOT / "scripts/check-rust-workspace.sh"
check_text = check_path.read_text(encoding="utf-8")

if '"crates/monad-core/src/context_foundation.rs",' not in check_text:
    check_text = check_text.replace(
        '"crates/monad-core/src/graph.rs",',
        '"crates/monad-core/src/graph.rs",\n        "crates/monad-core/src/context_foundation.rs",',
    )

if '"docs/cli/context-command.md",' not in check_text:
    check_text = check_text.replace(
        '"docs/cli/graph-command.md",',
        '"docs/cli/graph-command.md",\n        "docs/cli/context-command.md",',
    )

replacements = {
    'cargo run -p monad-cli -- context pack >/dev/null':
        'cargo run -p monad-cli -- context pack | grep "engine: native" >/dev/null',
    'cargo run -p monad-cli -- context verify >/dev/null':
        'cargo run -p monad-cli -- context verify | grep "engine: native" >/dev/null',
    'cargo run -p monad-cli -- context handoff >/dev/null':
        'cargo run -p monad-cli -- context handoff | grep "engine: native" >/dev/null',
    'cargo run -p monad-cli -- context exports >/dev/null':
        'cargo run -p monad-cli -- context exports | grep "engine: native" >/dev/null',
}

for old, new in replacements.items():
    check_text = check_text.replace(old, new)

if 'cargo run -p monad-cli -- context verify | grep "engine: native" >/dev/null' not in check_text:
    check_text = check_text.replace(
        'cargo run -p monad-cli -- context pack | grep "engine: native" >/dev/null',
        'cargo run -p monad-cli -- context pack | grep "engine: native" >/dev/null\ncargo run -p monad-cli -- context verify | grep "engine: native" >/dev/null',
    )

if 'cargo run -p monad-cli -- context handoff | grep "engine: native" >/dev/null' not in check_text:
    check_text = check_text.replace(
        'cargo run -p monad-cli -- context verify | grep "engine: native" >/dev/null',
        'cargo run -p monad-cli -- context verify | grep "engine: native" >/dev/null\ncargo run -p monad-cli -- context handoff | grep "engine: native" >/dev/null',
    )

if 'cargo run -p monad-cli -- context exports | grep "engine: native" >/dev/null' not in check_text:
    check_text = check_text.replace(
        'cargo run -p monad-cli -- context handoff | grep "engine: native" >/dev/null',
        'cargo run -p monad-cli -- context handoff | grep "engine: native" >/dev/null\ncargo run -p monad-cli -- context exports | grep "engine: native" >/dev/null',
    )

check_path.write_text(check_text, encoding="utf-8")
print("updated scripts/check-rust-workspace.sh")

print("context engine generated")

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

if "mod graph;" not in lib_text:
    marker = "mod memory;\n"
    if marker not in lib_text:
        raise SystemExit("Could not find memory module marker in crates/monad-core/src/lib.rs")

    lib_text = lib_text.replace(marker, marker + "mod graph;\n")

if "pub use graph::" not in lib_text:
    marker = "pub use memory::{\n"
    if marker not in lib_text:
        raise SystemExit("Could not find memory exports marker in crates/monad-core/src/lib.rs")

    graph_export = '''
pub use graph::{
    build_repository_graph, GraphEdge, GraphNode, GraphRenderFormat, RepositoryGraph,
};

'''
    lib_text = lib_text.replace(marker, graph_export + marker)

lib_path.write_text(lib_text, encoding="utf-8")
print("updated crates/monad-core/src/lib.rs")


write_file(
    "crates/monad-core/src/graph.rs",
    r'''
    //! Native repository graph model for `Monad Factory`.

    use std::fmt::{Display, Formatter};
    use std::path::{Path, PathBuf};

    use crate::{inspect_workspace, CheckStatus, WorkspaceInspectionError};

    /// Supported graph rendering formats.
    #[derive(Debug, Clone, Copy, Eq, PartialEq)]
    pub enum GraphRenderFormat {
        /// Human-readable text format.
        Text,

        /// JSON object format.
        Json,

        /// Mermaid graph format.
        Mermaid,

        /// Graphviz DOT format.
        Dot,
    }

    impl GraphRenderFormat {
        /// Parse a graph render format.
        #[must_use]
        pub fn parse(value: &str) -> Option<Self> {
            match value {
                "text" => Some(Self::Text),
                "json" => Some(Self::Json),
                "mermaid" => Some(Self::Mermaid),
                "dot" => Some(Self::Dot),
                _ => None,
            }
        }

        /// Return the stable format name.
        #[must_use]
        pub const fn as_str(self) -> &'static str {
            match self {
                Self::Text => "text",
                Self::Json => "json",
                Self::Mermaid => "mermaid",
                Self::Dot => "dot",
            }
        }
    }

    impl Display for GraphRenderFormat {
        fn fmt(&self, formatter: &mut Formatter<'_>) -> std::fmt::Result {
            formatter.write_str(self.as_str())
        }
    }

    /// One repository graph node.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct GraphNode {
        /// Stable node id.
        pub id: String,

        /// Human-readable label.
        pub label: String,

        /// Node kind.
        pub kind: String,

        /// Node path relative to the repository root.
        pub relative_path: String,

        /// Node presence status.
        pub status: CheckStatus,
    }

    /// One repository graph edge.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct GraphEdge {
        /// Source node id.
        pub from: String,

        /// Target node id.
        pub to: String,

        /// Edge relation name.
        pub relation: String,
    }

    /// Native repository graph.
    #[derive(Debug, Clone, Eq, PartialEq)]
    pub struct RepositoryGraph {
        /// Canonical repository root.
        pub root: PathBuf,

        /// Graph nodes.
        pub nodes: Vec<GraphNode>,

        /// Graph edges.
        pub edges: Vec<GraphEdge>,
    }

    impl RepositoryGraph {
        /// Count present graph nodes.
        #[must_use]
        pub fn present_node_count(&self) -> usize {
            self.nodes
                .iter()
                .filter(|node| node.status == CheckStatus::Pass)
                .count()
        }

        /// Return whether all graph nodes are present.
        #[must_use]
        pub fn is_complete(&self) -> bool {
            self.nodes.iter().all(|node| node.status == CheckStatus::Pass)
        }

        /// Render the repository graph in the requested format.
        #[must_use]
        pub fn render(&self, format: GraphRenderFormat) -> String {
            match format {
                GraphRenderFormat::Text => self.render_text(),
                GraphRenderFormat::Json => self.render_json(),
                GraphRenderFormat::Mermaid => self.render_mermaid(),
                GraphRenderFormat::Dot => self.render_dot(),
            }
        }

        fn render_text(&self) -> String {
            let mut lines = vec![
                "graph_format: text".to_string(),
                "engine: native".to_string(),
                format!("workspace_root: {}", self.root.display()),
                format!("nodes_present: {}/{}", self.present_node_count(), self.nodes.len()),
                format!("edges: {}", self.edges.len()),
                format!(
                    "status: {}",
                    if self.is_complete() {
                        "complete"
                    } else {
                        "incomplete"
                    }
                ),
                "nodes:".to_string(),
            ];

            for node in &self.nodes {
                lines.push(format!(
                    "  - {}: {} kind={} path={}",
                    node.id, node.status, node.kind, node.relative_path
                ));
            }

            lines.push("edges:".to_string());

            for edge in &self.edges {
                lines.push(format!("  - {} -> {} relation={}", edge.from, edge.to, edge.relation));
            }

            lines.join("\n")
        }

        fn render_json(&self) -> String {
            let node_lines = self
                .nodes
                .iter()
                .map(|node| {
                    format!(
                        "    {{\"id\":\"{}\",\"label\":\"{}\",\"kind\":\"{}\",\"path\":\"{}\",\"status\":\"{}\"}}",
                        escape_json(&node.id),
                        escape_json(&node.label),
                        escape_json(&node.kind),
                        escape_json(&node.relative_path),
                        node.status
                    )
                })
                .collect::<Vec<_>>();

            let edge_lines = self
                .edges
                .iter()
                .map(|edge| {
                    format!(
                        "    {{\"from\":\"{}\",\"to\":\"{}\",\"relation\":\"{}\"}}",
                        escape_json(&edge.from),
                        escape_json(&edge.to),
                        escape_json(&edge.relation)
                    )
                })
                .collect::<Vec<_>>();

            [
                "{".to_string(),
                "  \"format\": \"json\",".to_string(),
                "  \"engine\": \"native\",".to_string(),
                format!("  \"workspaceRoot\": \"{}\",", escape_json(&self.root.display().to_string())),
                format!("  \"nodesPresent\": {},", self.present_node_count()),
                format!("  \"nodeCount\": {},", self.nodes.len()),
                format!("  \"edgeCount\": {},", self.edges.len()),
                format!("  \"status\": \"{}\",", if self.is_complete() { "complete" } else { "incomplete" }),
                "  \"nodes\": [".to_string(),
                node_lines.join(",\n"),
                "  ],".to_string(),
                "  \"edges\": [".to_string(),
                edge_lines.join(",\n"),
                "  ]".to_string(),
                "}".to_string(),
            ]
            .join("\n")
        }

        fn render_mermaid(&self) -> String {
            let mut lines = vec![
                "graph TD".to_string(),
                "  %% engine: native".to_string(),
                format!("  %% workspace_root: {}", self.root.display()),
            ];

            for node in &self.nodes {
                lines.push(format!(
                    "  {}[\"{} ({})\"]",
                    sanitize_mermaid_id(&node.id),
                    node.label,
                    node.kind
                ));
            }

            for edge in &self.edges {
                lines.push(format!(
                    "  {} -->|{}| {}",
                    sanitize_mermaid_id(&edge.from),
                    edge.relation,
                    sanitize_mermaid_id(&edge.to)
                ));
            }

            lines.join("\n")
        }

        fn render_dot(&self) -> String {
            let mut lines = vec![
                "digraph monad_factory {".to_string(),
                "  graph [label=\"Monad Factory Repository Graph\"];".to_string(),
            ];

            for node in &self.nodes {
                lines.push(format!(
                    "  {} [label=\"{} ({})\"];",
                    sanitize_dot_id(&node.id),
                    escape_dot(&node.label),
                    escape_dot(&node.kind)
                ));
            }

            for edge in &self.edges {
                lines.push(format!(
                    "  {} -> {} [label=\"{}\"];",
                    sanitize_dot_id(&edge.from),
                    sanitize_dot_id(&edge.to),
                    escape_dot(&edge.relation)
                ));
            }

            lines.push("}".to_string());
            lines.join("\n")
        }
    }

    /// Build the native repository graph from workspace inspection.
    ///
    /// # Errors
    ///
    /// Returns an error when workspace inspection fails.
    pub fn build_repository_graph(root: &Path) -> Result<RepositoryGraph, WorkspaceInspectionError> {
        let inspection = inspect_workspace(root)?;

        let mut nodes = vec![GraphNode {
            id: "repo".to_string(),
            label: "repo".to_string(),
            kind: "root".to_string(),
            relative_path: ".".to_string(),
            status: CheckStatus::Pass,
        }];

        nodes.extend(inspection.domains.iter().map(|domain| GraphNode {
            id: domain.name.clone(),
            label: domain.name.clone(),
            kind: "domain".to_string(),
            relative_path: domain.name.clone(),
            status: presence_status(domain.exists),
        }));

        let edges = inspection
            .domains
            .iter()
            .map(|domain| GraphEdge {
                from: "repo".to_string(),
                to: domain.name.clone(),
                relation: "contains".to_string(),
            })
            .collect::<Vec<_>>();

        Ok(RepositoryGraph {
            root: inspection.root,
            nodes,
            edges,
        })
    }

    const fn presence_status(present: bool) -> CheckStatus {
        if present {
            CheckStatus::Pass
        } else {
            CheckStatus::Fail
        }
    }

    fn escape_json(value: &str) -> String {
        value
            .replace('\\', "\\\\")
            .replace('"', "\\\"")
            .replace('\n', "\\n")
    }

    fn escape_dot(value: &str) -> String {
        value.replace('\\', "\\\\").replace('"', "\\\"")
    }

    fn sanitize_mermaid_id(value: &str) -> String {
        sanitize_identifier(value)
    }

    fn sanitize_dot_id(value: &str) -> String {
        sanitize_identifier(value)
    }

    fn sanitize_identifier(value: &str) -> String {
        value
            .chars()
            .map(|character| {
                if character.is_ascii_alphanumeric() {
                    character
                } else {
                    '_'
                }
            })
            .collect()
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn parses_supported_formats() {
            assert_eq!(GraphRenderFormat::parse("text"), Some(GraphRenderFormat::Text));
            assert_eq!(GraphRenderFormat::parse("json"), Some(GraphRenderFormat::Json));
            assert_eq!(
                GraphRenderFormat::parse("mermaid"),
                Some(GraphRenderFormat::Mermaid)
            );
            assert_eq!(GraphRenderFormat::parse("dot"), Some(GraphRenderFormat::Dot));
            assert_eq!(GraphRenderFormat::parse("xml"), None);
        }

        #[test]
        fn renders_static_graph_without_external_dependencies() {
            let graph = RepositoryGraph {
                root: PathBuf::from("/repo"),
                nodes: vec![
                    GraphNode {
                        id: "repo".to_string(),
                        label: "repo".to_string(),
                        kind: "root".to_string(),
                        relative_path: ".".to_string(),
                        status: CheckStatus::Pass,
                    },
                    GraphNode {
                        id: "apps".to_string(),
                        label: "apps".to_string(),
                        kind: "domain".to_string(),
                        relative_path: "apps".to_string(),
                        status: CheckStatus::Pass,
                    },
                ],
                edges: vec![GraphEdge {
                    from: "repo".to_string(),
                    to: "apps".to_string(),
                    relation: "contains".to_string(),
                }],
            };

            assert!(graph.render(GraphRenderFormat::Text).contains("engine: native"));
            assert!(graph.render(GraphRenderFormat::Json).contains("\"engine\": \"native\""));
            assert!(graph.render(GraphRenderFormat::Mermaid).contains("graph TD"));
            assert!(graph.render(GraphRenderFormat::Dot).contains("digraph monad_factory"));
        }
    }
    ''',
)

write_file(
    "crates/monad-cli/src/commands/graph.rs",
    r'''
    //! Graph command renderer.

    use std::path::Path;

    use monad_core::{build_repository_graph, GraphRenderFormat};

    use crate::commands::unknown_argument;

    const FORMATS: &[&str] = &["text", "json", "mermaid", "dot"];

    /// Render a graph command response.
    pub fn render(args: &[String]) -> Result<String, String> {
        let format_name = args.first().map_or("text", String::as_str);

        match format_name {
            "--help" | "-h" | "help" => Ok(help()),
            value => {
                let Some(format) = GraphRenderFormat::parse(value) else {
                    return Err(unknown_argument("graph", value, FORMATS));
                };

                let graph = build_repository_graph(Path::new(".")).map_err(|error| error.to_string())?;

                Ok(graph.render(format))
            }
        }
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
        fn renders_text() -> Result<(), String> {
            let output = render(&args(&["text"]))?;

            assert!(output.contains("graph_format: text"));
            assert!(output.contains("engine: native"));
            assert!(output.contains("nodes:"));

            Ok(())
        }

        #[test]
        fn renders_mermaid() -> Result<(), String> {
            let output = render(&args(&["mermaid"]))?;

            assert!(output.contains("graph TD"));
            assert!(output.contains("repo -->|contains| crates"));

            Ok(())
        }

        #[test]
        fn renders_json() -> Result<(), String> {
            let output = render(&args(&["json"]))?;

            assert!(output.contains("\"format\": \"json\""));
            assert!(output.contains("\"engine\": \"native\""));
            assert!(output.contains("\"nodes\""));

            Ok(())
        }

        #[test]
        fn renders_dot() -> Result<(), String> {
            let output = render(&args(&["dot"]))?;

            assert!(output.contains("digraph monad_factory"));
            assert!(output.contains("repo -> crates"));

            Ok(())
        }
    }
    ''',
)

write_file(
    "docs/cli/graph-command.md",
    """
    # Native Graph Command

    `monad graph` renders a native repository graph model built from actual workspace inspection.

    Examples:

    ```bash
    cargo run -p monad-cli -- graph text
    cargo run -p monad-cli -- graph json
    cargo run -p monad-cli -- graph mermaid
    cargo run -p monad-cli -- graph dot
    ```

    Supported formats:

    - `text`
    - `json`
    - `mermaid`
    - `dot`

    The graph currently includes the repository root and expected top-level v1 foundation domains, with presence status derived from the workspace inspection engine.

    This is part of the approved v1 maximal functional graph, CLI, governance, inspection, context, and AI-readiness scope.
    """,
)

index_path = ROOT / "docs/cli/00-index.md"
index_text = index_path.read_text(encoding="utf-8")
if "Native Graph Command" not in index_text:
    index_text = index_text.replace(
        "- [Native Memory Command Group](./memory-command.md)",
        "- [Native Memory Command Group](./memory-command.md)\n- [Native Graph Command](./graph-command.md)",
    )
    index_path.write_text(index_text, encoding="utf-8")
    print("updated docs/cli/00-index.md")

check_path = ROOT / "scripts/check-rust-workspace.sh"
check_text = check_path.read_text(encoding="utf-8")

if '"crates/monad-core/src/graph.rs",' not in check_text:
    check_text = check_text.replace(
        '"crates/monad-core/src/memory.rs",',
        '"crates/monad-core/src/memory.rs",\n        "crates/monad-core/src/graph.rs",',
    )

if '"docs/cli/graph-command.md",' not in check_text:
    check_text = check_text.replace(
        '"docs/cli/memory-command.md",',
        '"docs/cli/memory-command.md",\n        "docs/cli/graph-command.md",',
    )

replacements = {
    'cargo run -p monad-cli -- graph text >/dev/null':
        'cargo run -p monad-cli -- graph text | grep "engine: native" >/dev/null',
    'cargo run -p monad-cli -- graph json >/dev/null':
        'cargo run -p monad-cli -- graph json | grep "\\"engine\\": \\"native\\"" >/dev/null',
    'cargo run -p monad-cli -- graph mermaid >/dev/null':
        'cargo run -p monad-cli -- graph mermaid | grep "graph TD" >/dev/null',
    'cargo run -p monad-cli -- graph dot >/dev/null':
        'cargo run -p monad-cli -- graph dot | grep "digraph monad_factory" >/dev/null',
}

for old, new in replacements.items():
    check_text = check_text.replace(old, new)

check_path.write_text(check_text, encoding="utf-8")
print("updated scripts/check-rust-workspace.sh")

print("graph engine generated")

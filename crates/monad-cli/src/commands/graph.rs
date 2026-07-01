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

            let graph =
                build_repository_graph(Path::new(".")).map_err(|error| error.to_string())?;

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

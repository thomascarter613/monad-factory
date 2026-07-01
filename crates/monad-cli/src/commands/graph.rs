//! Graph command renderer.

use crate::commands::unknown_argument;

const FORMATS: &[&str] = &["text", "json", "mermaid", "dot"];

pub fn render(args: &[String]) -> Result<String, String> {
    let format = args.first().map_or("text", String::as_str);

    match format {
        "text" => Ok(text()),
        "json" => Ok(json()),
        "mermaid" => Ok(mermaid()),
        "dot" => Ok(dot()),
        "--help" | "-h" | "help" => Ok(help()),
        unknown => Err(unknown_argument("graph", unknown, FORMATS)),
    }
}

fn text() -> String {
    [
        "graph_format: text",
        "nodes:",
        "  - repo",
        "  - apps",
        "  - packages",
        "  - services",
        "  - crates",
        "  - infra",
        "  - policies",
        "  - memory",
        "edges:",
        "  - repo -> apps",
        "  - repo -> packages",
        "  - repo -> services",
        "  - repo -> crates",
        "  - repo -> infra",
        "  - repo -> policies",
        "  - repo -> memory",
    ]
    .join("\n")
}

fn json() -> String {
    [
        "{",
        "  \"format\": \"json\",",
        "  \"nodes\": [\"repo\", \"apps\", \"packages\", \"services\", \"crates\", \"infra\", \"policies\", \"memory\"],",
        "  \"edges\": [",
        "    [\"repo\", \"apps\"],",
        "    [\"repo\", \"packages\"],",
        "    [\"repo\", \"services\"],",
        "    [\"repo\", \"crates\"],",
        "    [\"repo\", \"infra\"],",
        "    [\"repo\", \"policies\"],",
        "    [\"repo\", \"memory\"]",
        "  ]",
        "}",
    ]
    .join("\n")
}

fn mermaid() -> String {
    [
        "graph TD",
        "  repo[repo]",
        "  apps[apps]",
        "  packages[packages]",
        "  services[services]",
        "  crates[crates]",
        "  infra[infra]",
        "  policies[policies]",
        "  memory[memory]",
        "  repo --> apps",
        "  repo --> packages",
        "  repo --> services",
        "  repo --> crates",
        "  repo --> infra",
        "  repo --> policies",
        "  repo --> memory",
    ]
    .join("\n")
}

fn dot() -> String {
    [
        "digraph monad_factory {",
        "  repo -> apps;",
        "  repo -> packages;",
        "  repo -> services;",
        "  repo -> crates;",
        "  repo -> infra;",
        "  repo -> policies;",
        "  repo -> memory;",
        "}",
    ]
    .join("\n")
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
    fn renders_mermaid() -> Result<(), String> {
        let output = render(&args(&["mermaid"]))?;

        assert!(output.contains("graph TD"));
        assert!(output.contains("repo --> crates"));

        Ok(())
    }

    #[test]
    fn renders_json() -> Result<(), String> {
        let output = render(&args(&["json"]))?;

        assert!(output.contains("\"format\": \"json\""));
        assert!(output.contains("\"nodes\""));

        Ok(())
    }
}

//! Check command renderer.

use crate::commands::unknown_argument;

const TARGETS: &[&str] = &[
    "all",
    "foundation",
    "toolchain",
    "ci",
    "github-planning",
    "rust",
];

pub fn render(args: &[String]) -> Result<String, String> {
    let target = args.first().map_or("all", String::as_str);

    match target {
        "all" => Ok(response("all", "bun run check")),
        "foundation" => Ok(response("foundation", "bun run check:foundation")),
        "toolchain" => Ok(response("toolchain", "bun run check:toolchain")),
        "ci" => Ok(response("ci", "bun run check:ci")),
        "github-planning" => Ok(response("github-planning", "bun run check:github-planning")),
        "rust" => Ok(response("rust", "bun run check:rust")),
        "--help" | "-h" | "help" => Ok(help()),
        unknown => Err(unknown_argument("check", unknown, TARGETS)),
    }
}

fn response(target: &str, delegated_command: &str) -> String {
    [
        format!("check_target: {target}"),
        format!("delegated_command: {delegated_command}"),
        "status: registered".to_string(),
        "scope: core v1 validation surface".to_string(),
    ]
    .join("\n")
}

fn help() -> String {
    [
        "Usage:",
        "  monad check [target]",
        "",
        "Targets:",
        "  all",
        "  foundation",
        "  toolchain",
        "  ci",
        "  github-planning",
        "  rust",
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
    fn defaults_to_all() -> Result<(), String> {
        let output = render(&args(&[]))?;

        assert!(output.contains("check_target: all"));
        assert!(output.contains("bun run check"));

        Ok(())
    }

    #[test]
    fn renders_rust_target() -> Result<(), String> {
        let output = render(&args(&["rust"]))?;

        assert!(output.contains("check_target: rust"));
        assert!(output.contains("bun run check:rust"));

        Ok(())
    }
}

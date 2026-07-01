//! Context command renderer.

use crate::commands::unknown_argument;

const COMMANDS: &[&str] = &["help", "pack", "verify", "handoff", "exports"];

pub fn render(args: &[String]) -> Result<String, String> {
    let command = args.first().map_or("help", String::as_str);

    match command {
        "help" | "--help" | "-h" => Ok(help()),
        "pack" => Ok(response(
            "pack",
            "context pack creation is a core v1 command surface",
        )),
        "verify" => Ok(response(
            "verify",
            "context pack verification is a core v1 command surface",
        )),
        "handoff" => Ok(response(
            "handoff",
            "cross-session handoff generation is a core v1 command surface",
        )),
        "exports" => Ok(response(
            "exports",
            "AI tool export generation is a core v1 command surface",
        )),
        unknown => Err(unknown_argument("context", unknown, COMMANDS)),
    }
}

fn response(command: &str, description: &str) -> String {
    [
        format!("context_command: {command}"),
        format!("description: {description}"),
        "source_of_truth: docs/product/v1-maximal-functional-scope-and-delivery-plan.md"
            .to_string(),
        "status: registered".to_string(),
    ]
    .join("\n")
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
    fn renders_handoff_command() -> Result<(), String> {
        let output = render(&args(&["handoff"]))?;

        assert!(output.contains("context_command: handoff"));
        assert!(output.contains("core v1"));

        Ok(())
    }
}

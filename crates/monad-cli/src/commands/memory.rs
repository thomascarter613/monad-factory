//! Memory command renderer.

use crate::commands::unknown_argument;

const COMMANDS: &[&str] = &["status", "backends", "policy"];

pub fn render(args: &[String]) -> Result<String, String> {
    let command = args.first().map_or("status", String::as_str);

    match command {
        "status" => Ok(status()),
        "backends" => Ok(backends()),
        "policy" => Ok(policy()),
        "--help" | "-h" | "help" => Ok(help()),
        unknown => Err(unknown_argument("memory", unknown, COMMANDS)),
    }
}

fn status() -> String {
    [
        "memory_status: registered",
        "memory_index: .monad/memory/MEMORY.md",
        "scope: local-first inspectable policy-governed Monad Memory",
        "planned_backends: sqlite, pgvector, qdrant",
    ]
    .join("\n")
}

fn backends() -> String {
    [
        "memory_backends:",
        "  - sqlite",
        "  - pgvector",
        "  - qdrant",
        "backend_policy: local-first with optional external retrieval acceleration",
    ]
    .join("\n")
}

fn policy() -> String {
    [
        "memory_policy: policies/memory/memory-policy.md",
        "governance: inspectable, policy-governed, LLM-agnostic",
        "scope: core v1 memory foundation",
    ]
    .join("\n")
}

fn help() -> String {
    [
        "Usage:",
        "  monad memory [command]",
        "",
        "Commands:",
        "  status",
        "  backends",
        "  policy",
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
    fn renders_backend_plan() -> Result<(), String> {
        let output = render(&args(&["backends"]))?;

        assert!(output.contains("sqlite"));
        assert!(output.contains("pgvector"));
        assert!(output.contains("qdrant"));

        Ok(())
    }
}

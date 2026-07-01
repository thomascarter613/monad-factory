//! Inspect command renderer.

use crate::commands::unknown_argument;

const TARGETS: &[&str] = &["workspace", "scope", "toolchain", "memory"];

pub fn render(args: &[String]) -> Result<String, String> {
    let target = args.first().map_or("workspace", String::as_str);

    match target {
        "workspace" => Ok(workspace()),
        "scope" => Ok(scope()),
        "toolchain" => Ok(toolchain()),
        "memory" => Ok(memory()),
        "--help" | "-h" | "help" => Ok(help()),
        unknown => Err(unknown_argument("inspect", unknown, TARGETS)),
    }
}

fn workspace() -> String {
    [
        "inspect_target: workspace",
        "workspace_manifest: workspace.toml",
        "moon_workspace: .moon/workspace.yml",
        "cargo_workspace: Cargo.toml",
        "status: registered",
    ]
    .join("\n")
}

fn scope() -> String {
    [
        "inspect_target: scope",
        "source_of_truth: docs/product/v1-maximal-functional-scope-and-delivery-plan.md",
        "scope_model: v1 maximal functional scope",
        "downgrade_policy: approved v1 capabilities remain core v1 scope",
    ]
    .join("\n")
}

fn toolchain() -> String {
    [
        "inspect_target: toolchain",
        "toolchain_manifest: mise.toml",
        "javascript_package_manager: bun",
        "task_orchestrator: moon",
        "rust_workspace: Cargo.toml",
    ]
    .join("\n")
}

fn memory() -> String {
    [
        "inspect_target: memory",
        "memory_index: .monad/memory/MEMORY.md",
        "policy: policies/memory/memory-policy.md",
        "planned_backends: sqlite, pgvector, qdrant",
    ]
    .join("\n")
}

fn help() -> String {
    [
        "Usage:",
        "  monad inspect [target]",
        "",
        "Targets:",
        "  workspace",
        "  scope",
        "  toolchain",
        "  memory",
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
    fn renders_scope_source_of_truth() -> Result<(), String> {
        let output = render(&args(&["scope"]))?;

        assert!(output.contains("v1 maximal functional scope"));
        assert!(output.contains("source_of_truth"));

        Ok(())
    }
}

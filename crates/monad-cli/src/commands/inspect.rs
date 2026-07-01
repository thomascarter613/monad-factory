//! Inspect command renderer.

use std::path::Path;

use monad_core::{inspect_toolchain, inspect_workspace, ToolchainInspection, WorkspaceInspection};

use crate::commands::unknown_argument;

const TARGETS: &[&str] = &["workspace", "scope", "toolchain", "memory"];

/// Render an inspect command response.
pub fn render(args: &[String]) -> Result<String, String> {
    let target = args.first().map_or("workspace", String::as_str);

    match target {
        "workspace" => workspace(),
        "scope" => Ok(scope()),
        "toolchain" => toolchain(),
        "memory" => Ok(memory()),
        "--help" | "-h" | "help" => Ok(help()),
        unknown => Err(unknown_argument("inspect", unknown, TARGETS)),
    }
}

fn workspace() -> Result<String, String> {
    let inspection = inspect_workspace(Path::new(".")).map_err(|error| error.to_string())?;

    Ok(render_workspace_inspection(&inspection))
}

fn render_workspace_inspection(inspection: &WorkspaceInspection) -> String {
    let missing_domains = inspection.missing_domain_names();
    let missing_files = inspection.missing_foundation_file_names();

    let mut lines = vec![
        "inspect_target: workspace".to_string(),
        format!("workspace_root: {}", inspection.root.display()),
        "workspace_manifest: workspace.toml".to_string(),
        format!(
            "workspace_manifest_loaded: {}",
            inspection.workspace_manifest_loaded
        ),
        format!(
            "workspace_manifest_lines: {}",
            inspection.workspace_manifest_line_count
        ),
        format!(
            "top_level_domains_present: {}/{}",
            inspection.present_domain_count(),
            inspection.domains.len()
        ),
        format!(
            "foundation_files_present: {}/{}",
            inspection.present_foundation_file_count(),
            inspection.foundation_files.len()
        ),
        format!(
            "missing_domains: {}",
            render_missing_values(&missing_domains)
        ),
        format!(
            "missing_foundation_files: {}",
            render_missing_values(&missing_files)
        ),
        format!(
            "status: {}",
            if inspection.is_complete() {
                "complete"
            } else {
                "incomplete"
            }
        ),
        "domains:".to_string(),
    ];

    for domain in &inspection.domains {
        lines.push(format!(
            "  - {}: {} entries={}",
            domain.name,
            if domain.exists { "present" } else { "missing" },
            domain.entry_count
        ));
    }

    lines.push("foundation_files:".to_string());

    for file in &inspection.foundation_files {
        lines.push(format!(
            "  - {}: {}",
            file.relative_path,
            if file.exists { "present" } else { "missing" }
        ));
    }

    lines.join("\n")
}

fn render_missing_values(values: &[&str]) -> String {
    if values.is_empty() {
        "none".to_string()
    } else {
        values.join(", ")
    }
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

fn toolchain() -> Result<String, String> {
    let inspection = inspect_toolchain(Path::new(".")).map_err(|error| error.to_string())?;

    Ok(render_toolchain_inspection(&inspection))
}

fn render_toolchain_inspection(inspection: &ToolchainInspection) -> String {
    let missing_files = inspection.missing_file_names();
    let missing_tools = inspection.missing_tool_names();

    let mut lines = vec![
        "inspect_target: toolchain".to_string(),
        "engine: native".to_string(),
        format!("workspace_root: {}", inspection.root.display()),
        format!(
            "toolchain_files_present: {}/{}",
            inspection.present_file_count(),
            inspection.files.len()
        ),
        format!(
            "mise_tools_declared: {}/{}",
            inspection.declared_tool_count(),
            inspection.declared_tools.len()
        ),
        format!(
            "missing_toolchain_files: {}",
            render_missing_values(&missing_files)
        ),
        format!(
            "missing_mise_tools: {}",
            render_missing_values(&missing_tools)
        ),
        format!(
            "package_manager: {}",
            inspection.package_manager.as_deref().unwrap_or("missing")
        ),
        format!(
            "rust_toolchain_channel: {}",
            inspection
                .rust_toolchain_channel
                .as_deref()
                .unwrap_or("missing")
        ),
        format!("check_script_status: {}", inspection.check_script_status),
        format!(
            "toolchain_check_script_status: {}",
            inspection.toolchain_check_script_status
        ),
        format!(
            "rust_check_script_status: {}",
            inspection.rust_check_script_status
        ),
        format!(
            "moon_workspace_status: {}",
            inspection.moon_workspace_status
        ),
        format!(
            "moon_toolchains_status: {}",
            inspection.moon_toolchains_status
        ),
        format!(
            "cargo_workspace_status: {}",
            inspection.cargo_workspace_status
        ),
        format!(
            "status: {}",
            if inspection.is_complete() {
                "complete"
            } else {
                "incomplete"
            }
        ),
        "declared_tools:".to_string(),
    ];

    for tool in &inspection.declared_tools {
        lines.push(format!(
            "  - {}: {} version={}",
            tool.name,
            if tool.declared { "present" } else { "missing" },
            tool.version.as_deref().unwrap_or("missing")
        ));
    }

    lines.push("toolchain_files:".to_string());

    for file in &inspection.files {
        lines.push(format!(
            "  - {}: {}",
            file.relative_path,
            if file.exists { "present" } else { "missing" }
        ));
    }

    lines.join("\n")
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

    #[test]
    fn renders_real_workspace_inspection() -> Result<(), String> {
        let output = render(&args(&["workspace"]))?;

        assert!(output.contains("workspace_manifest_loaded: true"));
        assert!(output.contains("top_level_domains_present:"));
        assert!(output.contains("foundation_files_present:"));
        assert!(output.contains("domains:"));
        assert!(output.contains("foundation_files:"));

        Ok(())
    }

    #[test]
    fn renders_real_toolchain_inspection() -> Result<(), String> {
        let output = render(&args(&["toolchain"]))?;

        assert!(output.contains("inspect_target: toolchain"));
        assert!(output.contains("engine: native"));
        assert!(output.contains("toolchain_files_present:"));
        assert!(output.contains("mise_tools_declared:"));
        assert!(output.contains("declared_tools:"));

        Ok(())
    }
}

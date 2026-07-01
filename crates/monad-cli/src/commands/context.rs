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
        format!(
            "export_targets_registered: {}",
            foundation.export_targets.len()
        ),
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

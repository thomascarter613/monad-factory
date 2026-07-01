//! Memory command renderer.

use std::path::Path;

use monad_core::MemoryInspection;
use monad_core::{inspect_memory, MEMORY_INDEX_PATH, MEMORY_POLICY_PATH};

use crate::commands::unknown_argument;

const COMMANDS: &[&str] = &["status", "backends", "policy"];

/// Render a memory command response.
pub fn render(args: &[String]) -> Result<String, String> {
    let command = args.first().map_or("status", String::as_str);

    match command {
        "status" => status(),
        "backends" => backends(),
        "policy" => policy(),
        "--help" | "-h" | "help" => Ok(help()),
        unknown => Err(unknown_argument("memory", unknown, COMMANDS)),
    }
}

fn status() -> Result<String, String> {
    let inspection = inspect_memory(Path::new(".")).map_err(|error| error.to_string())?;

    Ok(render_status(&inspection))
}

fn backends() -> Result<String, String> {
    let inspection = inspect_memory(Path::new(".")).map_err(|error| error.to_string())?;

    Ok(render_backends(&inspection))
}

fn policy() -> Result<String, String> {
    let inspection = inspect_memory(Path::new(".")).map_err(|error| error.to_string())?;

    Ok(render_policy(&inspection))
}

fn render_status(inspection: &MemoryInspection) -> String {
    [
        "memory_command: status".to_string(),
        "engine: native".to_string(),
        format!("workspace_root: {}", inspection.root.display()),
        format!(
            "memory_files_present: {}/{}",
            inspection.present_file_count(),
            inspection.files.len()
        ),
        format!(
            "memory_backends_registered: {}/{}",
            inspection.registered_backend_count(),
            inspection.backends.len()
        ),
        format!(
            "missing_memory_files: {}",
            render_missing_values(&inspection.missing_file_names())
        ),
        format!(
            "local_first_policy_status: {}",
            inspection.local_first_policy_status
        ),
        format!(
            "inspectable_policy_status: {}",
            inspection.inspectable_policy_status
        ),
        format!(
            "policy_governed_status: {}",
            inspection.policy_governed_status
        ),
        format!(
            "status: {}",
            if inspection.is_complete() {
                "complete"
            } else {
                "incomplete"
            }
        ),
    ]
    .join("\n")
}

fn render_backends(inspection: &MemoryInspection) -> String {
    let mut lines = vec![
        "memory_command: backends".to_string(),
        "engine: native".to_string(),
        format!("workspace_root: {}", inspection.root.display()),
        format!(
            "memory_backends_registered: {}/{}",
            inspection.registered_backend_count(),
            inspection.backends.len()
        ),
        "memory_backends:".to_string(),
    ];

    for backend in &inspection.backends {
        lines.push(format!(
            "  - {}: {} role={}",
            backend.name, backend.status, backend.role
        ));
    }

    lines.join("\n")
}

fn render_policy(inspection: &MemoryInspection) -> String {
    [
        "memory_command: policy".to_string(),
        "engine: native".to_string(),
        format!("workspace_root: {}", inspection.root.display()),
        format!("memory_index: {MEMORY_INDEX_PATH}"),
        format!("memory_policy: {MEMORY_POLICY_PATH}"),
        format!(
            "local_first_policy_status: {}",
            inspection.local_first_policy_status
        ),
        format!(
            "inspectable_policy_status: {}",
            inspection.inspectable_policy_status
        ),
        format!(
            "policy_governed_status: {}",
            inspection.policy_governed_status
        ),
        "governance_model: local-first inspectable policy-governed Monad Memory".to_string(),
    ]
    .join("\n")
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
    fn renders_native_status() -> Result<(), String> {
        let output = render(&args(&["status"]))?;

        assert!(output.contains("memory_command: status"));
        assert!(output.contains("engine: native"));
        assert!(output.contains("memory_files_present:"));

        Ok(())
    }

    #[test]
    fn renders_backend_plan() -> Result<(), String> {
        let output = render(&args(&["backends"]))?;

        assert!(output.contains("memory_command: backends"));
        assert!(output.contains("sqlite"));
        assert!(output.contains("pgvector"));
        assert!(output.contains("qdrant"));

        Ok(())
    }

    #[test]
    fn renders_policy_status() -> Result<(), String> {
        let output = render(&args(&["policy"]))?;

        assert!(output.contains("memory_command: policy"));
        assert!(output.contains(MEMORY_INDEX_PATH));
        assert!(output.contains(MEMORY_POLICY_PATH));

        Ok(())
    }
}

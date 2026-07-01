//! Check command renderer.

use std::path::Path;

use monad_core::{
    run_foundation_check, run_memory_check, run_toolchain_check, FoundationCheckReport,
    MemoryCheckReport, ToolchainCheckReport,
};

use crate::commands::unknown_argument;

const TARGETS: &[&str] = &[
    "all",
    "foundation",
    "toolchain",
    "memory",
    "ci",
    "github-planning",
    "rust",
];

/// Render a check command response.
pub fn render(args: &[String]) -> Result<String, String> {
    let target = args.first().map_or("all", String::as_str);

    match target {
        "all" => Ok(response("all", "bun run check")),
        "foundation" => foundation(),
        "toolchain" => toolchain(),
        "memory" => memory(),
        "ci" => Ok(response("ci", "bun run check:ci")),
        "github-planning" => Ok(response("github-planning", "bun run check:github-planning")),
        "rust" => Ok(response("rust", "bun run check:rust")),
        "--help" | "-h" | "help" => Ok(help()),
        unknown => Err(unknown_argument("check", unknown, TARGETS)),
    }
}

fn foundation() -> Result<String, String> {
    let report = run_foundation_check(Path::new(".")).map_err(|error| error.to_string())?;

    Ok(render_foundation_report(&report))
}

fn toolchain() -> Result<String, String> {
    let report = run_toolchain_check(Path::new(".")).map_err(|error| error.to_string())?;

    Ok(render_toolchain_report(&report))
}

fn memory() -> Result<String, String> {
    let report = run_memory_check(Path::new(".")).map_err(|error| error.to_string())?;

    Ok(render_memory_report(&report))
}

fn render_foundation_report(report: &FoundationCheckReport) -> String {
    let mut lines = vec![
        "check_target: foundation".to_string(),
        "engine: native".to_string(),
        format!("workspace_root: {}", report.root.display()),
        format!("status: {}", report.status),
        format!("pass_count: {}", report.pass_count()),
        format!("warn_count: {}", report.warn_count()),
        format!("fail_count: {}", report.fail_count()),
        format!(
            "top_level_domains_present: {}/{}",
            report.inspection.present_domain_count(),
            report.inspection.domains.len()
        ),
        format!(
            "foundation_files_present: {}/{}",
            report.inspection.present_foundation_file_count(),
            report.inspection.foundation_files.len()
        ),
        "items:".to_string(),
    ];

    for item in &report.items {
        lines.push(format!(
            "  - {}: {} - {}",
            item.name, item.status, item.message
        ));
    }

    lines.join("\n")
}

fn render_toolchain_report(report: &ToolchainCheckReport) -> String {
    let mut lines = vec![
        "check_target: toolchain".to_string(),
        "engine: native".to_string(),
        format!("workspace_root: {}", report.root.display()),
        format!("status: {}", report.status),
        format!("pass_count: {}", report.pass_count()),
        format!("warn_count: {}", report.warn_count()),
        format!("fail_count: {}", report.fail_count()),
        format!(
            "toolchain_files_present: {}/{}",
            report.inspection.present_file_count(),
            report.inspection.files.len()
        ),
        format!(
            "mise_tools_declared: {}/{}",
            report.inspection.declared_tool_count(),
            report.inspection.declared_tools.len()
        ),
        "items:".to_string(),
    ];

    for item in &report.items {
        lines.push(format!(
            "  - {}: {} - {}",
            item.name, item.status, item.message
        ));
    }

    lines.join("\n")
}

fn render_memory_report(report: &MemoryCheckReport) -> String {
    let mut lines = vec![
        "check_target: memory".to_string(),
        "engine: native".to_string(),
        format!("workspace_root: {}", report.root.display()),
        format!("status: {}", report.status),
        format!("pass_count: {}", report.pass_count()),
        format!("warn_count: {}", report.warn_count()),
        format!("fail_count: {}", report.fail_count()),
        format!(
            "memory_files_present: {}/{}",
            report.inspection.present_file_count(),
            report.inspection.files.len()
        ),
        format!(
            "memory_backends_registered: {}/{}",
            report.inspection.registered_backend_count(),
            report.inspection.backends.len()
        ),
        "items:".to_string(),
    ];

    for item in &report.items {
        lines.push(format!(
            "  - {}: {} - {}",
            item.name, item.status, item.message
        ));
    }

    lines.join("\n")
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
        "  memory",
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

    #[test]
    fn renders_native_foundation_check() -> Result<(), String> {
        let output = render(&args(&["foundation"]))?;

        assert!(output.contains("check_target: foundation"));
        assert!(output.contains("engine: native"));
        assert!(output.contains("items:"));

        Ok(())
    }

    #[test]
    fn renders_native_toolchain_check() -> Result<(), String> {
        let output = render(&args(&["toolchain"]))?;

        assert!(output.contains("check_target: toolchain"));
        assert!(output.contains("engine: native"));
        assert!(output.contains("toolchain_files_present:"));
        assert!(output.contains("mise_tools_declared:"));
        assert!(output.contains("items:"));

        Ok(())
    }

    #[test]
    fn renders_native_memory_check() -> Result<(), String> {
        let output = render(&args(&["memory"]))?;

        assert!(output.contains("check_target: memory"));
        assert!(output.contains("engine: native"));
        assert!(output.contains("memory_files_present:"));
        assert!(output.contains("memory_backends_registered:"));
        assert!(output.contains("items:"));

        Ok(())
    }
}

from __future__ import annotations

import os
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def clean(content: str) -> str:
    value = textwrap.dedent(content).lstrip()
    if not value.endswith("\n"):
        value += "\n"
    return value


def write_file(relative_path: str, content: str, mode: int | None = None) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean(content), encoding="utf-8")
    if mode is not None:
        os.chmod(path, mode)
    print(f"wrote {relative_path}")


memory_path = ROOT / "crates/monad-core/src/memory.rs"
memory_text = memory_path.read_text(encoding="utf-8")

insert_candidates = [
    "\n#[cfg(test)]\nmod tests {\n",
    "\n    #[cfg(test)]\n    mod tests {\n",
]

memory_check_engine = r'''
/// One native memory check item.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct MemoryCheckItem {
    /// Stable item name.
    pub name: String,

    /// Check status.
    pub status: CheckStatus,

    /// Human-readable check message.
    pub message: String,
}

/// Native memory check report.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct MemoryCheckReport {
    /// Workspace root used for the check.
    pub root: PathBuf,

    /// Overall check status.
    pub status: CheckStatus,

    /// Individual check items.
    pub items: Vec<MemoryCheckItem>,

    /// Memory inspection used by the check.
    pub inspection: MemoryInspection,
}

impl MemoryCheckReport {
    /// Count passing check items.
    #[must_use]
    pub fn pass_count(&self) -> usize {
        self.items
            .iter()
            .filter(|item| item.status == CheckStatus::Pass)
            .count()
    }

    /// Count warning check items.
    #[must_use]
    pub fn warn_count(&self) -> usize {
        self.items
            .iter()
            .filter(|item| item.status == CheckStatus::Warn)
            .count()
    }

    /// Count failing check items.
    #[must_use]
    pub fn fail_count(&self) -> usize {
        self.items
            .iter()
            .filter(|item| item.status == CheckStatus::Fail)
            .count()
    }
}

/// Run the native Monad Memory foundation check.
///
/// # Errors
///
/// Returns an error when memory inspection fails.
pub fn run_memory_check(root: &Path) -> Result<MemoryCheckReport, WorkspaceInspectionError> {
    let inspection = inspect_memory(root)?;
    let mut items = Vec::new();

    add_memory_file_check(&mut items, &inspection);
    add_memory_backend_check(&mut items, &inspection);
    add_memory_policy_checks(&mut items, &inspection);

    let status = summarize_memory_check_status(&items);

    Ok(MemoryCheckReport {
        root: inspection.root.clone(),
        status,
        items,
        inspection,
    })
}

fn add_memory_file_check(items: &mut Vec<MemoryCheckItem>, inspection: &MemoryInspection) {
    let missing_files = inspection.missing_file_names();

    items.push(MemoryCheckItem {
        name: "memory-files".to_string(),
        status: presence_status(missing_files.is_empty()),
        message: if missing_files.is_empty() {
            format!("all {} expected memory files are present", inspection.files.len())
        } else {
            format!("missing memory files: {}", missing_files.join(", "))
        },
    });
}

fn add_memory_backend_check(items: &mut Vec<MemoryCheckItem>, inspection: &MemoryInspection) {
    let missing_backends = inspection
        .backends
        .iter()
        .filter(|backend| backend.status == CheckStatus::Fail)
        .map(|backend| backend.name.as_str())
        .collect::<Vec<_>>();

    items.push(MemoryCheckItem {
        name: "memory-backends".to_string(),
        status: presence_status(missing_backends.is_empty()),
        message: if missing_backends.is_empty() {
            format!(
                "all {} planned memory backends are registered",
                inspection.backends.len()
            )
        } else {
            format!("missing memory backend references: {}", missing_backends.join(", "))
        },
    });
}

fn add_memory_policy_checks(items: &mut Vec<MemoryCheckItem>, inspection: &MemoryInspection) {
    let checks = [
        (
            "local-first-memory-policy",
            inspection.local_first_policy_status,
            "memory foundation must include local-first policy language",
        ),
        (
            "inspectable-memory-policy",
            inspection.inspectable_policy_status,
            "memory foundation must include inspectable policy language",
        ),
        (
            "policy-governed-memory",
            inspection.policy_governed_status,
            "memory foundation must include policy-governed memory language",
        ),
    ];

    for (name, status, message) in checks {
        add_memory_status_check(items, name, status, message.to_string());
    }
}

fn summarize_memory_check_status(items: &[MemoryCheckItem]) -> CheckStatus {
    if items.iter().any(|item| item.status == CheckStatus::Fail) {
        CheckStatus::Fail
    } else if items.iter().any(|item| item.status == CheckStatus::Warn) {
        CheckStatus::Warn
    } else {
        CheckStatus::Pass
    }
}

fn add_memory_status_check(
    items: &mut Vec<MemoryCheckItem>,
    name: &str,
    status: CheckStatus,
    message: String,
) {
    items.push(MemoryCheckItem {
        name: name.to_string(),
        status,
        message,
    });
}
'''

if "pub struct MemoryCheckReport" not in memory_text:
    insert_before = next((candidate for candidate in insert_candidates if candidate in memory_text), None)

    if insert_before is None:
        raise SystemExit(
            "Could not find insertion point in crates/monad-core/src/memory.rs. "
            "Expected a crate-root #[cfg(test)] mod tests block."
        )

    memory_text = memory_text.replace(insert_before, memory_check_engine + insert_before)
    memory_path.write_text(memory_text, encoding="utf-8")
    print("updated crates/monad-core/src/memory.rs")
else:
    print("crates/monad-core/src/memory.rs already contains memory check engine")


lib_path = ROOT / "crates/monad-core/src/lib.rs"
lib_text = lib_path.read_text(encoding="utf-8")

replacements = {
    "inspect_memory, MemoryBackend, MemoryFile, MemoryInspection, EXPECTED_MEMORY_FILES,":
        "inspect_memory, run_memory_check, MemoryBackend, MemoryCheckItem, MemoryCheckReport, MemoryFile, MemoryInspection, EXPECTED_MEMORY_FILES,",
}

for old, new in replacements.items():
    if old in lib_text and "run_memory_check" not in lib_text:
        lib_text = lib_text.replace(old, new)

lib_path.write_text(lib_text, encoding="utf-8")
print("updated crates/monad-core/src/lib.rs exports")


write_file(
    "crates/monad-cli/src/commands/check.rs",
    r'''
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
            "github-planning" => Ok(response(
                "github-planning",
                "bun run check:github-planning",
            )),
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
    ''',
)

write_file(
    "docs/cli/memory-check.md",
    """
    # Native Memory Check

    `monad check memory` runs a native validation engine over the local-first Monad Memory foundation.

    Example:

    ```bash
    cargo run -p monad-cli -- check memory
    ```

    Current checks include:

    - expected memory foundation files
    - planned memory backend references for SQLite, pgvector, and Qdrant
    - local-first memory policy language
    - inspectable memory policy language
    - policy-governed memory language

    This is part of the approved v1 maximal functional memory, governance, CLI, AI-readiness, and context-continuity scope.
    """,
)

for path in [
    ROOT / "docs/cli/command-surface.md",
]:
    text = path.read_text(encoding="utf-8")
    if "memory" not in text.split("## Check targets", 1)[1].split("```", 2)[1]:
        text = text.replace(
            "github-planning\nrust",
            "github-planning\nmemory\nrust",
        )
        path.write_text(text, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")

index_path = ROOT / "docs/cli/00-index.md"
index_text = index_path.read_text(encoding="utf-8")
if "Native Memory Check" not in index_text:
    index_text = index_text.replace(
        "- [Memory Inspection](./memory-inspection.md)",
        "- [Memory Inspection](./memory-inspection.md)\n- [Native Memory Check](./memory-check.md)",
    )
    index_path.write_text(index_text, encoding="utf-8")
    print("updated docs/cli/00-index.md")

check_path = ROOT / "scripts/check-rust-workspace.sh"
check_text = check_path.read_text(encoding="utf-8")

if '"docs/cli/memory-check.md",' not in check_text:
    check_text = check_text.replace(
        '"docs/cli/memory-inspection.md",',
        '"docs/cli/memory-inspection.md",\n        "docs/cli/memory-check.md",',
    )

if 'cargo run -p monad-cli -- check memory | grep "engine: native" >/dev/null' not in check_text:
    check_text = check_text.replace(
        'cargo run -p monad-cli -- check toolchain | grep "engine: native" >/dev/null',
        'cargo run -p monad-cli -- check toolchain | grep "engine: native" >/dev/null\ncargo run -p monad-cli -- check memory | grep "engine: native" >/dev/null',
    )

check_path.write_text(check_text, encoding="utf-8")
print("updated scripts/check-rust-workspace.sh")

print("memory check engine generated")

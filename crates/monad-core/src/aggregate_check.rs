//! Native aggregate check engine for the `monad check all` command.

use std::path::{Path, PathBuf};

use crate::{
    build_repository_graph, inspect_context_foundation, run_foundation_check, run_memory_check,
    run_toolchain_check, CheckStatus, WorkspaceInspectionError,
};

/// One native aggregate check item.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct AggregateCheckItem {
    /// Stable item name.
    pub name: String,

    /// Check status.
    pub status: CheckStatus,

    /// Human-readable check message.
    pub message: String,
}

/// Native aggregate check report.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct AggregateCheckReport {
    /// Workspace root used for the aggregate check.
    pub root: PathBuf,

    /// Overall aggregate status.
    pub status: CheckStatus,

    /// Individual aggregate check items.
    pub items: Vec<AggregateCheckItem>,
}

impl AggregateCheckReport {
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

/// Run the native aggregate check.
///
/// # Errors
///
/// Returns an error when one of the underlying native inspections or checks fails to run.
pub fn run_all_checks(root: &Path) -> Result<AggregateCheckReport, WorkspaceInspectionError> {
    let foundation = run_foundation_check(root)?;
    let toolchain = run_toolchain_check(root)?;
    let memory = run_memory_check(root)?;
    let context = inspect_context_foundation(root)?;
    let graph = build_repository_graph(root)?;

    let items = vec![
        aggregate_item(
            "foundation",
            foundation.status,
            format!(
                "{} pass, {} warn, {} fail",
                foundation.pass_count(),
                foundation.warn_count(),
                foundation.fail_count()
            ),
        ),
        aggregate_item(
            "toolchain",
            toolchain.status,
            format!(
                "{} pass, {} warn, {} fail",
                toolchain.pass_count(),
                toolchain.warn_count(),
                toolchain.fail_count()
            ),
        ),
        aggregate_item(
            "memory",
            memory.status,
            format!(
                "{} pass, {} warn, {} fail",
                memory.pass_count(),
                memory.warn_count(),
                memory.fail_count()
            ),
        ),
        aggregate_item(
            "context",
            context.status(),
            format!(
                "{}/{} context artifacts present",
                context.present_artifact_count(),
                context.artifacts.len()
            ),
        ),
        aggregate_item(
            "graph",
            presence_status(graph.is_complete()),
            format!(
                "{}/{} graph nodes present",
                graph.present_node_count(),
                graph.nodes.len()
            ),
        ),
    ];

    Ok(AggregateCheckReport {
        root: foundation.root,
        status: summarize_status(&items),
        items,
    })
}

fn aggregate_item(name: &str, status: CheckStatus, message: String) -> AggregateCheckItem {
    AggregateCheckItem {
        name: name.to_string(),
        status,
        message,
    }
}

fn summarize_status(items: &[AggregateCheckItem]) -> CheckStatus {
    if items.iter().any(|item| item.status == CheckStatus::Fail) {
        CheckStatus::Fail
    } else if items.iter().any(|item| item.status == CheckStatus::Warn) {
        CheckStatus::Warn
    } else {
        CheckStatus::Pass
    }
}

const fn presence_status(present: bool) -> CheckStatus {
    if present {
        CheckStatus::Pass
    } else {
        CheckStatus::Fail
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn summarize_status_passes_when_all_items_pass() {
        let items = vec![
            aggregate_item("one", CheckStatus::Pass, "ok".to_string()),
            aggregate_item("two", CheckStatus::Pass, "ok".to_string()),
        ];

        assert_eq!(summarize_status(&items), CheckStatus::Pass);
    }

    #[test]
    fn summarize_status_fails_when_any_item_fails() {
        let items = vec![
            aggregate_item("one", CheckStatus::Pass, "ok".to_string()),
            aggregate_item("two", CheckStatus::Fail, "bad".to_string()),
        ];

        assert_eq!(summarize_status(&items), CheckStatus::Fail);
    }
}

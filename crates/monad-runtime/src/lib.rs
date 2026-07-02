use monad_core::{CommandOutcome, Finding};

#[derive(Debug, thiserror::Error)]
pub enum RuntimeError {
#[error("tool was not found: {0}")]
ToolNotFound(String),
}

pub fn task_stub(
action: impl Into<String>,
target: Option<&str>,
dry_run: bool,
) -> CommandOutcome {
let action = action.into();
let target_label = target.unwrap_or("workspace");

```
let summary = if dry_run {
    format!("Would run `{action}` for `{target_label}`")
} else {
    format!("Stubbed `{action}` for `{target_label}`")
};

CommandOutcome::ok(action, summary).with_finding(Finding::info(
    "runtime.stub",
    "Runtime execution is stubbed. Wire this to native tools later.",
))
```

}

pub fn tool_available(tool: &str) -> bool {
which::which(tool).is_ok()
}

use camino::Utf8Path;
use monad_core::{CommandOutcome, Finding};

pub fn doctor(root: &Utf8Path) -> CommandOutcome {
let mut outcome = CommandOutcome::ok("doctor", format!("Checked workspace at {root}"));

```
for required in ["Cargo.toml", "crates"] {
    let path = root.join(required);
    if !path.exists() {
        outcome = outcome.with_finding(Finding::warning(
            "workspace.missing-path",
            format!("Expected path is missing: {required}"),
        ));
    }
}

for tool in ["git", "cargo"] {
    if !monad_runtime::tool_available(tool) {
        outcome = outcome.with_finding(Finding::warning(
            "tool.missing",
            format!("Required tool not found on PATH: {tool}"),
        ));
    }
}

outcome
```

}

pub fn validate_stub(domain: &str, target: Option<&str>) -> CommandOutcome {
CommandOutcome::ok(
"validate",
format!(
"Stubbed validation for domain `{domain}` target `{}`",
target.unwrap_or("workspace")
),
)
}

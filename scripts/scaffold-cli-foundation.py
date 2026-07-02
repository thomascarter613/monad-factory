from pathlib import Path
import os
import textwrap

ROOT = Path.cwd()
FORCE = os.environ.get("FORCE", "0") == "1"

def write(path: str, content: str):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and not FORCE:
        print(f"skip existing: {path}")
        return

    if target.exists() and FORCE:
        backup = target.with_suffix(target.suffix + ".bak")
        backup.write_text(target.read_text())
        print(f"backup: {backup}")

    target.write_text(textwrap.dedent(content).lstrip())
    print(f"write: {path}")

def touch_dir(path: str):
    target = ROOT / path
    target.mkdir(parents=True, exist_ok=True)
    print(f"dir: {path}")

# ---------------------------------------------------------------------
# Root workspace
# ---------------------------------------------------------------------

write("Cargo.toml", r'''
[workspace]
resolver = "2"
members = [
  "crates/monad-cli",
  "crates/monad-core",
  "crates/monad-config",
  "crates/monad-generator",
  "crates/monad-runtime",
  "crates/monad-validation",
  "crates/monad-registry",
  "crates/monad-templates",
]

[workspace.package]
version = "0.1.0"
edition = "2021"
license = "MIT"
repository = "https://github.com/example/monad"
homepage = "https://github.com/example/monad"
documentation = "https://github.com/example/monad"
rust-version = "1.80"

[workspace.dependencies]
monad-core = { path = "crates/monad-core" }
monad-config = { path = "crates/monad-config" }
monad-generator = { path = "crates/monad-generator" }
monad-runtime = { path = "crates/monad-runtime" }
monad-validation = { path = "crates/monad-validation" }
monad-registry = { path = "crates/monad-registry" }
monad-templates = { path = "crates/monad-templates" }

clap = { version = "4", features = ["derive", "env", "wrap_help", "cargo"] }
clap_complete = "4"
color-eyre = "0.6"
thiserror = "2"
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "fmt", "json"] }

serde = { version = "1", features = ["derive"] }
serde_json = "1"
toml = "0.8"
toml_edit = { version = "0.22", features = ["serde"] }

camino = { version = "1", features = ["serde1"] }
fs-err = "3"
ignore = "0.4"
walkdir = "2"
globset = "0.4"
petgraph = "0.6"
indexmap = { version = "2", features = ["serde"] }
semver = { version = "1", features = ["serde"] }
uuid = { version = "1", features = ["v4", "serde"] }
time = { version = "0.3", features = ["serde", "formatting", "parsing"] }
which = "8"

indicatif = "0.18"
owo-colors = "4"

[workspace.dev-dependencies]
assert_cmd = "2"
assert_fs = "1"
predicates = "3"
tempfile = "3"
insta = { version = "1", features = ["yaml", "json", "redactions"] }
pretty_assertions = "1"
rstest = "0.23"
''')

write(".gitignore", r'''
/target
/.monad
.DS_Store
.env
.env.*
!.env.example
node_modules
dist
coverage
.pytest_cache
.ruff_cache
__pycache__
.idea
.vscode/*
!.vscode/extensions.json
!.vscode/settings.json
''')

write("rust-toolchain.toml", r'''
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
''')

write("README.md", r'''
# Monad CLI

Monad is a developer CLI for interactively generating, validating, and managing fully configured polyglot monorepos.

## Local development

```bash
cargo fmt --all
cargo check --workspace
cargo test --workspace
cargo run -p monad-cli -- --help
```

## Example commands

```bash
cargo run -p monad-cli -- new my-platform
cargo run -p monad-cli -- init
cargo run -p monad-cli -- add app web --framework tanstack-start --language typescript
cargo run -p monad-cli -- add service api --language rust --runtime axum
cargo run -p monad-cli -- doctor
cargo run -p monad-cli -- list commands
```

''')

write("scripts/check-rust-workspace.sh", r'''
#!/usr/bin/env bash
set -euo pipefail

cargo fmt --all --check
cargo check --workspace
cargo test --workspace
''')

# ---------------------------------------------------------------------

# Crate directories

# ---------------------------------------------------------------------

for crate in [
    "monad-cli",
    "monad-core",
    "monad-config",
    "monad-generator",
    "monad-runtime",
    "monad-validation",
    "monad-registry",
    "monad-templates",
]:
    touch_dir(f"crates/{crate}/src")

# ---------------------------------------------------------------------

# monad-core

# ---------------------------------------------------------------------

write("crates/monad-core/Cargo.toml", r'''
[package]
name = "monad-core"
version.workspace = true
edition.workspace = true
license.workspace = true
rust-version.workspace = true

[dependencies]
serde.workspace = true
serde_json.workspace = true
thiserror.workspace = true
camino.workspace = true
indexmap.workspace = true
petgraph.workspace = true
semver.workspace = true
uuid.workspace = true
time.workspace = true
''')

write("crates/monad-core/src/lib.rs", r'''
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum Severity {
Info,
Warning,
Error,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Finding {
pub code: String,
pub severity: Severity,
pub message: String,
pub path: Option<String>,
pub recommendation: Option<String>,
}

impl Finding {
pub fn info(code: impl Into<String>, message: impl Into<String>) -> Self {
Self {
code: code.into(),
severity: Severity::Info,
message: message.into(),
path: None,
recommendation: None,
}
}

```
pub fn warning(code: impl Into<String>, message: impl Into<String>) -> Self {
    Self {
        code: code.into(),
        severity: Severity::Warning,
        message: message.into(),
        path: None,
        recommendation: None,
    }
}

pub fn error(code: impl Into<String>, message: impl Into<String>) -> Self {
    Self {
        code: code.into(),
        severity: Severity::Error,
        message: message.into(),
        path: None,
        recommendation: None,
    }
}
```

}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct CommandOutcome {
pub action: String,
pub summary: String,
pub changed: bool,
pub findings: Vec<Finding>,
}

impl CommandOutcome {
pub fn ok(action: impl Into<String>, summary: impl Into<String>) -> Self {
Self {
action: action.into(),
summary: summary.into(),
changed: false,
findings: Vec::new(),
}
}

```
pub fn changed(action: impl Into<String>, summary: impl Into<String>) -> Self {
    Self {
        action: action.into(),
        summary: summary.into(),
        changed: true,
        findings: Vec::new(),
    }
}

pub fn with_finding(mut self, finding: Finding) -> Self {
    self.findings.push(finding);
    self
}
```

}

#[derive(Debug, Clone, Serialize)]
pub struct CommandSpec {
pub domain: &'static str,
pub actions: &'static [&'static str],
}

pub fn command_catalog() -> Vec<CommandSpec> {
vec![
CommandSpec { domain: "new", actions: &["workspace", "app", "from-template", "from-preset"] },
CommandSpec { domain: "init", actions: &["detect", "adopt-existing", "write-manifest"] },
CommandSpec { domain: "bootstrap", actions: &["devcontainer", "ci", "hooks", "docker", "all"] },
CommandSpec { domain: "wizard", actions: &["new", "init", "add", "repair", "configure"] },
CommandSpec { domain: "add", actions: &["app", "service", "package", "lib", "cli", "worker", "job", "function", "tool", "db", "ci", "docker", "docs", "test"] },
CommandSpec { domain: "remove", actions: &["app", "service", "package", "tool", "ci", "env", "secret"] },
CommandSpec { domain: "generate", actions: &["component", "page", "route", "endpoint", "migration", "openapi", "sdk", "dockerfile", "ci", "docs", "adr", "context"] },
CommandSpec { domain: "configure", actions: &["package-manager", "monorepo-engine", "formatter", "linter", "hooks", "ci", "docker", "devcontainer", "renovate", "release", "observability", "secrets", "security"] },
CommandSpec { domain: "tool", actions: &["list", "info", "add", "remove", "configure", "upgrade", "doctor", "versions", "pin"] },
CommandSpec { domain: "env", actions: &["list", "add", "remove", "validate", "diff", "generate", "pull", "push", "sync", "example", "print"] },
CommandSpec { domain: "secrets", actions: &["list", "add", "remove", "set", "get", "validate", "scan", "rotate", "sync", "pull", "push", "provider"] },
CommandSpec { domain: "db", actions: &["add", "remove", "list", "init", "generate", "migrate", "rollback", "reset", "seed", "studio", "shell", "status", "diff", "introspect", "backup", "restore", "validate", "connect"] },
CommandSpec { domain: "api", actions: &["add", "list", "generate", "validate", "lint", "docs", "mock", "test", "client", "sdk", "gateway", "version"] },
CommandSpec { domain: "auth", actions: &["add", "configure", "remove", "providers", "provider", "roles", "permissions", "policy", "generate", "validate"] },
CommandSpec { domain: "ci", actions: &["init", "generate", "validate", "lint", "run", "explain", "doctor", "add", "remove", "matrix", "cache", "secrets"] },
CommandSpec { domain: "docker", actions: &["init", "generate", "build", "run", "push", "scan", "validate", "compose", "dockerfile"] },
CommandSpec { domain: "docs", actions: &["init", "generate", "serve", "build", "validate", "lint", "index", "adr", "roadmap", "architecture", "api", "changelog", "onboarding", "runbook", "handoff"] },
CommandSpec { domain: "security", actions: &["init", "scan", "audit", "sbom", "license", "scorecard", "fix", "validate"] },
CommandSpec { domain: "context", actions: &["pack", "verify", "current-state", "handoff", "bootstrap", "summarize", "index", "search", "diff", "export"] },
CommandSpec { domain: "template", actions: &["list", "info", "add", "remove", "create", "validate", "test", "publish", "install", "update"] },
CommandSpec { domain: "preset", actions: &["list", "info", "create", "apply", "validate", "export", "import"] },
CommandSpec { domain: "plugin", actions: &["list", "search", "install", "remove", "update", "enable", "disable", "info", "validate", "create", "publish"] },
CommandSpec { domain: "registry", actions: &["list", "add", "remove", "search", "login", "publish", "sync"] },
]
}

#[cfg(test)]
mod tests {
use super::*;

```
#[test]
fn command_catalog_contains_core_commands() {
    let catalog = command_catalog();
    assert!(catalog.iter().any(|item| item.domain == "add"));
    assert!(catalog.iter().any(|item| item.domain == "generate"));
    assert!(catalog.iter().any(|item| item.domain == "doctor"));
}
```

}
''')

# ---------------------------------------------------------------------

# monad-config

# ---------------------------------------------------------------------

write("crates/monad-config/Cargo.toml", r'''
[package]
name = "monad-config"
version.workspace = true
edition.workspace = true
license.workspace = true
rust-version.workspace = true

[dependencies]
monad-core.workspace = true

serde.workspace = true
serde_json.workspace = true
toml.workspace = true
toml_edit.workspace = true
thiserror.workspace = true
camino.workspace = true
fs-err.workspace = true
indexmap.workspace = true
''')

write("crates/monad-config/src/lib.rs", r'''
use camino::Utf8Path;
use serde::{Deserialize, Serialize};

#[derive(Debug, thiserror::Error)]
pub enum ConfigError {
#[error("I/O error: {0}")]
Io(#[from] std::io::Error),

```
#[error("TOML serialization error: {0}")]
TomlSerialize(#[from] toml::ser::Error),

#[error("TOML deserialization error: {0}")]
TomlDeserialize(#[from] toml::de::Error),
```

}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct MonadManifest {
pub workspace: WorkspaceConfig,
pub tooling: ToolingConfig,
pub layout: LayoutConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct WorkspaceConfig {
pub name: String,
pub package_manager: String,
pub monorepo_engine: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ToolingConfig {
pub formatter: String,
pub linter: String,
pub hooks: String,
pub ci: String,
pub container_runtime: String,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct LayoutConfig {
pub apps_dir: String,
pub services_dir: String,
pub packages_dir: String,
pub libs_dir: String,
pub infra_dir: String,
pub docs_dir: String,
}

pub fn default_manifest(name: impl Into<String>) -> MonadManifest {
MonadManifest {
workspace: WorkspaceConfig {
name: name.into(),
package_manager: "bun".to_string(),
monorepo_engine: "turbo+moon".to_string(),
},
tooling: ToolingConfig {
formatter: "biome".to_string(),
linter: "biome".to_string(),
hooks: "lefthook".to_string(),
ci: "github-actions".to_string(),
container_runtime: "docker".to_string(),
},
layout: LayoutConfig {
apps_dir: "apps".to_string(),
services_dir: "services".to_string(),
packages_dir: "packages".to_string(),
libs_dir: "libs".to_string(),
infra_dir: "infra".to_string(),
docs_dir: "docs".to_string(),
},
}
}

pub fn write_manifest(root: &Utf8Path, manifest: &MonadManifest) -> Result<(), ConfigError> {
let path = root.join("monad.toml");
let content = toml::to_string_pretty(manifest)?;
fs_err::write(path, content)?;
Ok(())
}

pub fn read_manifest(root: &Utf8Path) -> Result<MonadManifest, ConfigError> {
let path = root.join("monad.toml");
let content = fs_err::read_to_string(path)?;
Ok(toml::from_str(&content)?)
}
''')

# ---------------------------------------------------------------------

# monad-templates

# ---------------------------------------------------------------------

write("crates/monad-templates/Cargo.toml", r'''
[package]
name = "monad-templates"
version.workspace = true
edition.workspace = true
license.workspace = true
rust-version.workspace = true

[dependencies]
''')

write("crates/monad-templates/src/lib.rs", r'''
pub const WORKSPACE_README: &str = r#"# {{name}}

Generated by Monad.

## Layout

* `apps/` - deployable applications
* `services/` - backend services and workers
* `packages/` - shared packages
* `libs/` - shared libraries
* `infra/` - infrastructure
* `docs/` - documentation
  "#;

pub const PROJECT_README: &str = r#"# {{name}}

Generated project stub.

## Next steps

1. Choose runtime/framework.
2. Add dependencies.
3. Add tests.
4. Wire into task graph.
5. Wire into CI.
   "#;
   ''')

# ---------------------------------------------------------------------

# monad-generator

# ---------------------------------------------------------------------

write("crates/monad-generator/Cargo.toml", r'''
[package]
name = "monad-generator"
version.workspace = true
edition.workspace = true
license.workspace = true
rust-version.workspace = true

[dependencies]
monad-core.workspace = true
monad-config.workspace = true
monad-templates.workspace = true

thiserror.workspace = true
camino.workspace = true
fs-err.workspace = true
serde.workspace = true
serde_json.workspace = true
tracing.workspace = true
''')

write("crates/monad-generator/src/lib.rs", r'''
use camino::{Utf8Path, Utf8PathBuf};
use monad_config::{default_manifest, write_manifest};
use monad_core::{CommandOutcome, Finding};

#[derive(Debug, thiserror::Error)]
pub enum GeneratorError {
#[error("I/O error: {0}")]
Io(#[from] std::io::Error),

```
#[error("configuration error: {0}")]
Config(#[from] monad_config::ConfigError),
```

}

pub fn new_workspace(
root: &Utf8Path,
name: &str,
dry_run: bool,
) -> Result<CommandOutcome, GeneratorError> {
let target = root.join(name);

```
if dry_run {
    return Ok(CommandOutcome::ok(
        "new",
        format!("Would create workspace at {target}"),
    ));
}

create_workspace_dirs(&target)?;
write_workspace_files(&target, name)?;

Ok(CommandOutcome::changed(
    "new",
    format!("Created workspace scaffold at {target}"),
))
```

}

pub fn init_workspace(root: &Utf8Path, dry_run: bool) -> Result<CommandOutcome, GeneratorError> {
let name = root
.file_name()
.map(ToOwned::to_owned)
.unwrap_or_else(|| "monad-workspace".to_string());

```
if dry_run {
    return Ok(CommandOutcome::ok(
        "init",
        format!("Would initialize Monad workspace in {root}"),
    ));
}

create_workspace_dirs(root)?;
write_workspace_files(root, &name)?;

Ok(CommandOutcome::changed(
    "init",
    format!("Initialized Monad workspace in {root}"),
))
```

}

pub fn add_stub(
root: &Utf8Path,
kind: &str,
name: &str,
dry_run: bool,
) -> Result<CommandOutcome, GeneratorError> {
let base_dir = match kind {
"app" | "apps" => "apps",
"service" | "services" => "services",
"package" | "packages" => "packages",
"lib" | "libs" | "library" => "libs",
"cli" | "tool" | "tools" => "tools",
"worker" | "job" | "function" => "services",
"docs" | "doc" => "docs",
"infra" => "infra",
other => other,
};

```
let target = root.join(base_dir).join(name);

if dry_run {
    return Ok(CommandOutcome::ok(
        "add",
        format!("Would add {kind} `{name}` at {target}"),
    ));
}

fs_err::create_dir_all(target.join("src"))?;
fs_err::write(
    target.join("README.md"),
    format!(
        "# {name}\n\nGenerated `{kind}` stub.\n\n## Next steps\n\n- Add implementation.\n- Add tests.\n- Wire into CI/task graph.\n"
    ),
)?;
fs_err::write(
    target.join(".gitkeep"),
    "",
)?;
fs_err::write(
    target.join("src").join(".gitkeep"),
    "",
)?;

Ok(CommandOutcome::changed(
    "add",
    format!("Added {kind} `{name}` at {target}"),
)
.with_finding(Finding::info(
    "stub.created",
    "This is a structural stub. Runtime-specific files can be generated by a later command.",
)))
```

}

fn create_workspace_dirs(root: &Utf8Path) -> Result<(), GeneratorError> {
for dir in [
"apps",
"services",
"packages",
"libs",
"tools",
"infra",
"docs",
"contracts",
"policies",
"scripts",
".github/workflows",
] {
fs_err::create_dir_all(root.join(dir))?;
}

```
Ok(())
```

}

fn write_workspace_files(root: &Utf8Path, name: &str) -> Result<(), GeneratorError> {
write_manifest(root, &default_manifest(name))?;

```
fs_err::write(
    root.join("README.md"),
    format!(
        "# {name}\n\nGenerated by Monad.\n\n## Layout\n\n- `apps/`\n- `services/`\n- `packages/`\n- `libs/`\n- `tools/`\n- `infra/`\n- `docs/`\n- `contracts/`\n- `policies/`\n"
    ),
)?;

fs_err::write(
    root.join(".gitignore"),
    "/node_modules\n/target\n/.monad\n.env\n.env.*\n!.env.example\n",
)?;

fs_err::write(root.join("apps").join(".gitkeep"), "")?;
fs_err::write(root.join("services").join(".gitkeep"), "")?;
fs_err::write(root.join("packages").join(".gitkeep"), "")?;
fs_err::write(root.join("libs").join(".gitkeep"), "")?;
fs_err::write(root.join("tools").join(".gitkeep"), "")?;
fs_err::write(root.join("infra").join(".gitkeep"), "")?;
fs_err::write(root.join("docs").join(".gitkeep"), "")?;

Ok(())
```

}

pub fn current_dir_utf8() -> Utf8PathBuf {
let cwd = std::env::current_dir().expect("current directory should be available");
Utf8PathBuf::from_path_buf(cwd).expect("current directory should be valid UTF-8")
}
''')

# ---------------------------------------------------------------------

# monad-runtime

# ---------------------------------------------------------------------

write("crates/monad-runtime/Cargo.toml", r'''
[package]
name = "monad-runtime"
version.workspace = true
edition.workspace = true
license.workspace = true
rust-version.workspace = true

[dependencies]
monad-core.workspace = true

thiserror.workspace = true
camino.workspace = true
which.workspace = true
tracing.workspace = true
''')

write("crates/monad-runtime/src/lib.rs", r'''
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
''')

# ---------------------------------------------------------------------

# monad-validation

# ---------------------------------------------------------------------

write("crates/monad-validation/Cargo.toml", r'''
[package]
name = "monad-validation"
version.workspace = true
edition.workspace = true
license.workspace = true
rust-version.workspace = true

[dependencies]
monad-core.workspace = true
monad-config.workspace = true
monad-runtime.workspace = true

thiserror.workspace = true
camino.workspace = true
fs-err.workspace = true
ignore.workspace = true
walkdir.workspace = true
globset.workspace = true
tracing.workspace = true
''')

write("crates/monad-validation/src/lib.rs", r'''
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
''')

# ---------------------------------------------------------------------

# monad-registry

# ---------------------------------------------------------------------

write("crates/monad-registry/Cargo.toml", r'''
[package]
name = "monad-registry"
version.workspace = true
edition.workspace = true
license.workspace = true
rust-version.workspace = true

[dependencies]
monad-core.workspace = true

serde.workspace = true
serde_json.workspace = true
thiserror.workspace = true
camino.workspace = true
fs-err.workspace = true
tracing.workspace = true
''')

write("crates/monad-registry/src/lib.rs", r'''
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RegistryTemplate {
pub name: &'static str,
pub description: &'static str,
}

pub fn built_in_templates() -> Vec<RegistryTemplate> {
vec![
RegistryTemplate {
name: "app-tanstack-start-typescript",
description: "TanStack Start TypeScript app stub",
},
RegistryTemplate {
name: "service-rust-axum",
description: "Rust Axum service stub",
},
RegistryTemplate {
name: "service-go-chi",
description: "Go Chi service stub",
},
RegistryTemplate {
name: "service-python-fastapi",
description: "Python FastAPI service stub",
},
RegistryTemplate {
name: "package-typescript",
description: "TypeScript shared package stub",
},
]
}
''')

# ---------------------------------------------------------------------

# monad-cli

# ---------------------------------------------------------------------

write("crates/monad-cli/Cargo.toml", r'''
[package]
name = "monad-cli"
version.workspace = true
edition.workspace = true
license.workspace = true
rust-version.workspace = true

[[bin]]
name = "monad"
path = "src/main.rs"

[dependencies]
monad-core.workspace = true
monad-config.workspace = true
monad-generator.workspace = true
monad-runtime.workspace = true
monad-validation.workspace = true
monad-registry.workspace = true

clap.workspace = true
clap_complete.workspace = true
color-eyre.workspace = true
serde_json.workspace = true
tracing.workspace = true
tracing-subscriber.workspace = true
camino.workspace = true
owo-colors.workspace = true

[dev-dependencies]
assert_cmd.workspace = true
predicates.workspace = true
''')

write("crates/monad-cli/src/main.rs", r'''
use clap::{Args, Parser, Subcommand};
use color_eyre::eyre::Result;
use monad_core::CommandOutcome;
use owo_colors::OwoColorize;

#[derive(Debug, Parser)]
#[command(
name = "monad",
version,
about = "Developer CLI for generating and managing polyglot monorepos",
disable_help_subcommand = true
)]
struct Cli {
#[arg(long, global = true)]
json: bool,

```
#[arg(long, global = true)]
dry_run: bool,

#[arg(short, long, global = true)]
verbose: bool,

#[command(subcommand)]
command: Commands,
```

}

#[derive(Debug, Subcommand)]
enum Commands {
New(NewArgs),
Init,
Bootstrap(FreeArgs),
Wizard(FreeArgs),

```
Add(EntityArgs),
Remove(EntityArgs),
Generate(EntityArgs),
Configure(FreeArgs),
Install(FreeArgs),
Upgrade(FreeArgs),
Migrate(FreeArgs),

Doctor,
Check,
Validate(FreeArgs),
Inspect(FreeArgs),
Explain(FreeArgs),
Graph(FreeArgs),
List(FreeArgs),
Status(FreeArgs),
Plan(FreeArgs),

Dev(TargetArgs),
Run(RunArgs),
Exec(RunArgs),
Task(FreeArgs),
Build(TargetArgs),
Test(TestArgs),
Lint(TargetArgs),
Format(FormatArgs),
Typecheck(TargetArgs),
Clean(FreeArgs),
Reset(FreeArgs),

Workspace(FreeArgs),
Project(FreeArgs),
App(FreeArgs),
Service(FreeArgs),
Package(FreeArgs),
Lib(FreeArgs),

Tool(FreeArgs),
Template(FreeArgs),
Preset(FreeArgs),
Plugin(FreeArgs),
Registry(FreeArgs),

Env(FreeArgs),
Secrets(FreeArgs),
Config(FreeArgs),

Db(FreeArgs),
Api(FreeArgs),
Auth(FreeArgs),
Events(FreeArgs),
Queue(FreeArgs),
Cache(FreeArgs),
Storage(FreeArgs),
Search(FreeArgs),

Ai(FreeArgs),
Context(FreeArgs),
Docs(FreeArgs),

Ci(FreeArgs),
Cd(FreeArgs),
Docker(FreeArgs),
Compose(FreeArgs),
K8s(FreeArgs),
Infra(FreeArgs),
Deploy(FreeArgs),

Release(FreeArgs),
Version(FreeArgs),
Changelog(FreeArgs),

Security(FreeArgs),
Policy(FreeArgs),
Compliance(FreeArgs),
Audit(FreeArgs),

Observability(FreeArgs),
Telemetry(FreeArgs),
Logs(FreeArgs),
Metrics(FreeArgs),
Trace(FreeArgs),

Coverage(FreeArgs),
Benchmark(FreeArgs),
Dependency(FreeArgs),
Lock(FreeArgs),
Snapshot(FreeArgs),
Import(FreeArgs),
Export(FreeArgs),
Sync(FreeArgs),
Repair(FreeArgs),

Completion(CompletionArgs),

#[command(name = "self")]
SelfCmd(FreeArgs),

Help(FreeArgs),
```

}

#[derive(Debug, Args)]
struct NewArgs {
name: String,

```
#[arg(long)]
preset: Option<String>,

#[arg(long)]
package_manager: Option<String>,

#[arg(long)]
monorepo_engine: Option<String>,

#[arg(long)]
interactive: bool,
```

}

#[derive(Debug, Args)]
struct EntityArgs {
kind: String,
name: Option<String>,

```
#[arg(trailing_var_arg = true)]
rest: Vec<String>,
```

}

#[derive(Debug, Args)]
struct FreeArgs {
action: Option<String>,
target: Option<String>,

```
#[arg(trailing_var_arg = true)]
rest: Vec<String>,
```

}

#[derive(Debug, Args)]
struct TargetArgs {
target: Option<String>,

```
#[arg(trailing_var_arg = true)]
rest: Vec<String>,
```

}

#[derive(Debug, Args)]
struct RunArgs {
target: Option<String>,
script: Option<String>,

```
#[arg(trailing_var_arg = true)]
rest: Vec<String>,
```

}

#[derive(Debug, Args)]
struct TestArgs {
target: Option<String>,

```
#[arg(long)]
unit: bool,

#[arg(long)]
integration: bool,

#[arg(long)]
e2e: bool,

#[arg(long)]
coverage: bool,

#[arg(trailing_var_arg = true)]
rest: Vec<String>,
```

}

#[derive(Debug, Args)]
struct FormatArgs {
#[arg(long)]
check: bool,

```
#[arg(long)]
write: bool,

#[arg(trailing_var_arg = true)]
rest: Vec<String>,
```

}

#[derive(Debug, Args)]
struct CompletionArgs {
shell: Option<String>,
}

fn main() -> Result<()> {
color_eyre::install()?;

```
tracing_subscriber::fmt()
    .with_env_filter(
        std::env::var("MONAD_LOG").unwrap_or_else(|_| "warn,monad=info".to_string()),
    )
    .init();

let cli = Cli::parse();
let root = monad_generator::current_dir_utf8();

let outcome = match cli.command {
    Commands::New(args) => monad_generator::new_workspace(&root, &args.name, cli.dry_run)?,

    Commands::Init => monad_generator::init_workspace(&root, cli.dry_run)?,

    Commands::Add(args) => {
        let name = args.name.unwrap_or_else(|| "unnamed".to_string());
        monad_generator::add_stub(&root, &args.kind, &name, cli.dry_run)?
    }

    Commands::Doctor => monad_validation::doctor(&root),

    Commands::List(args) if args.action.as_deref() == Some("commands") => {
        if cli.json {
            println!("{}", serde_json::to_string_pretty(&monad_core::command_catalog())?);
        } else {
            for item in monad_core::command_catalog() {
                println!("{}", item.domain.bold());
                for action in item.actions {
                    println!("  - {action}");
                }
            }
        }
        return Ok(());
    }

    Commands::Template(args) if args.action.as_deref() == Some("list") => {
        if cli.json {
            println!("{}", serde_json::to_string_pretty(
                &monad_registry::built_in_templates()
                    .iter()
                    .map(|template| {
                        serde_json::json!({
                            "name": template.name,
                            "description": template.description
                        })
                    })
                    .collect::<Vec<_>>()
            )?);
        } else {
            for template in monad_registry::built_in_templates() {
                println!("{} - {}", template.name.bold(), template.description);
            }
        }
        return Ok(());
    }

    Commands::Validate(args) => {
        monad_validation::validate_stub(
            args.action.as_deref().unwrap_or("workspace"),
            args.target.as_deref(),
        )
    }

    Commands::Check => monad_runtime::task_stub("check", Some("workspace"), cli.dry_run),

    Commands::Generate(args) => stub_entity("generate", args, cli.dry_run),
    Commands::Remove(args) => stub_entity("remove", args, cli.dry_run),

    Commands::Bootstrap(args) => stub_free("bootstrap", args, cli.dry_run),
    Commands::Wizard(args) => stub_free("wizard", args, cli.dry_run),
    Commands::Configure(args) => stub_free("configure", args, cli.dry_run),
    Commands::Install(args) => stub_free("install", args, cli.dry_run),
    Commands::Upgrade(args) => stub_free("upgrade", args, cli.dry_run),
    Commands::Migrate(args) => stub_free("migrate", args, cli.dry_run),
    Commands::Inspect(args) => stub_free("inspect", args, cli.dry_run),
    Commands::Explain(args) => stub_free("explain", args, cli.dry_run),
    Commands::Graph(args) => stub_free("graph", args, cli.dry_run),
    Commands::List(args) => stub_free("list", args, cli.dry_run),
    Commands::Status(args) => stub_free("status", args, cli.dry_run),
    Commands::Plan(args) => stub_free("plan", args, cli.dry_run),
    Commands::Task(args) => stub_free("task", args, cli.dry_run),
    Commands::Clean(args) => stub_free("clean", args, cli.dry_run),
    Commands::Reset(args) => stub_free("reset", args, cli.dry_run),
    Commands::Workspace(args) => stub_free("workspace", args, cli.dry_run),
    Commands::Project(args) => stub_free("project", args, cli.dry_run),
    Commands::App(args) => stub_free("app", args, cli.dry_run),
    Commands::Service(args) => stub_free("service", args, cli.dry_run),
    Commands::Package(args) => stub_free("package", args, cli.dry_run),
    Commands::Lib(args) => stub_free("lib", args, cli.dry_run),
    Commands::Tool(args) => stub_free("tool", args, cli.dry_run),
    Commands::Preset(args) => stub_free("preset", args, cli.dry_run),
    Commands::Plugin(args) => stub_free("plugin", args, cli.dry_run),
    Commands::Registry(args) => stub_free("registry", args, cli.dry_run),
    Commands::Env(args) => stub_free("env", args, cli.dry_run),
    Commands::Secrets(args) => stub_free("secrets", args, cli.dry_run),
    Commands::Config(args) => stub_free("config", args, cli.dry_run),
    Commands::Db(args) => stub_free("db", args, cli.dry_run),
    Commands::Api(args) => stub_free("api", args, cli.dry_run),
    Commands::Auth(args) => stub_free("auth", args, cli.dry_run),
    Commands::Events(args) => stub_free("events", args, cli.dry_run),
    Commands::Queue(args) => stub_free("queue", args, cli.dry_run),
    Commands::Cache(args) => stub_free("cache", args, cli.dry_run),
    Commands::Storage(args) => stub_free("storage", args, cli.dry_run),
    Commands::Search(args) => stub_free("search", args, cli.dry_run),
    Commands::Ai(args) => stub_free("ai", args, cli.dry_run),
    Commands::Context(args) => stub_free("context", args, cli.dry_run),
    Commands::Docs(args) => stub_free("docs", args, cli.dry_run),
    Commands::Ci(args) => stub_free("ci", args, cli.dry_run),
    Commands::Cd(args) => stub_free("cd", args, cli.dry_run),
    Commands::Docker(args) => stub_free("docker", args, cli.dry_run),
    Commands::Compose(args) => stub_free("compose", args, cli.dry_run),
    Commands::K8s(args) => stub_free("k8s", args, cli.dry_run),
    Commands::Infra(args) => stub_free("infra", args, cli.dry_run),
    Commands::Deploy(args) => stub_free("deploy", args, cli.dry_run),
    Commands::Release(args) => stub_free("release", args, cli.dry_run),
    Commands::Version(args) => stub_free("version", args, cli.dry_run),
    Commands::Changelog(args) => stub_free("changelog", args, cli.dry_run),
    Commands::Security(args) => stub_free("security", args, cli.dry_run),
    Commands::Policy(args) => stub_free("policy", args, cli.dry_run),
    Commands::Compliance(args) => stub_free("compliance", args, cli.dry_run),
    Commands::Audit(args) => stub_free("audit", args, cli.dry_run),
    Commands::Observability(args) => stub_free("observability", args, cli.dry_run),
    Commands::Telemetry(args) => stub_free("telemetry", args, cli.dry_run),
    Commands::Logs(args) => stub_free("logs", args, cli.dry_run),
    Commands::Metrics(args) => stub_free("metrics", args, cli.dry_run),
    Commands::Trace(args) => stub_free("trace", args, cli.dry_run),
    Commands::Coverage(args) => stub_free("coverage", args, cli.dry_run),
    Commands::Benchmark(args) => stub_free("benchmark", args, cli.dry_run),
    Commands::Dependency(args) => stub_free("dependency", args, cli.dry_run),
    Commands::Lock(args) => stub_free("lock", args, cli.dry_run),
    Commands::Snapshot(args) => stub_free("snapshot", args, cli.dry_run),
    Commands::Import(args) => stub_free("import", args, cli.dry_run),
    Commands::Export(args) => stub_free("export", args, cli.dry_run),
    Commands::Sync(args) => stub_free("sync", args, cli.dry_run),
    Commands::Repair(args) => stub_free("repair", args, cli.dry_run),
    Commands::SelfCmd(args) => stub_free("self", args, cli.dry_run),
    Commands::Help(args) => stub_free("help", args, cli.dry_run),

    Commands::Dev(args) => monad_runtime::task_stub("dev", args.target.as_deref(), cli.dry_run),
    Commands::Build(args) => monad_runtime::task_stub("build", args.target.as_deref(), cli.dry_run),
    Commands::Lint(args) => monad_runtime::task_stub("lint", args.target.as_deref(), cli.dry_run),
    Commands::Typecheck(args) => {
        monad_runtime::task_stub("typecheck", args.target.as_deref(), cli.dry_run)
    }
    Commands::Run(args) => monad_runtime::task_stub(
        format!(
            "run {}",
            args.script.as_deref().unwrap_or("default")
        ),
        args.target.as_deref(),
        cli.dry_run,
    ),
    Commands::Exec(args) => monad_runtime::task_stub(
        format!(
            "exec {}",
            args.script.as_deref().unwrap_or("command")
        ),
        args.target.as_deref(),
        cli.dry_run,
    ),
    Commands::Test(args) => {
        let mode = if args.unit {
            "unit"
        } else if args.integration {
            "integration"
        } else if args.e2e {
            "e2e"
        } else if args.coverage {
            "coverage"
        } else {
            "all"
        };

        monad_runtime::task_stub(format!("test:{mode}"), args.target.as_deref(), cli.dry_run)
    }
    Commands::Format(args) => {
        let mode = if args.check {
            "format:check"
        } else if args.write {
            "format:write"
        } else {
            "format"
        };

        monad_runtime::task_stub(mode, Some("workspace"), cli.dry_run)
    }
    Commands::Completion(args) => monad_runtime::task_stub(
        format!(
            "completion {}",
            args.shell.as_deref().unwrap_or("unknown-shell")
        ),
        Some("shell"),
        cli.dry_run,
    ),
};

print_outcome(&outcome, cli.json)?;
Ok(())
```

}

fn stub_entity(action: &str, args: EntityArgs, dry_run: bool) -> CommandOutcome {
let target = args.name.as_deref().unwrap_or("unnamed");
monad_runtime::task_stub(format!("{action} {}", args.kind), Some(target), dry_run)
}

fn stub_free(action: &str, args: FreeArgs, dry_run: bool) -> CommandOutcome {
let target = args.target.as_deref().or(args.action.as_deref());
monad_runtime::task_stub(action, target, dry_run)
}

fn print_outcome(outcome: &CommandOutcome, json: bool) -> Result<()> {
if json {
println!("{}", serde_json::to_string_pretty(outcome)?);
return Ok(());
}

```
let status = if outcome.changed {
    "changed".green().bold().to_string()
} else {
    "ok".blue().bold().to_string()
};

println!("{status} {}", outcome.summary);

for finding in &outcome.findings {
    println!(
        "  {} [{}] {}",
        "-".dimmed(),
        finding.code,
        finding.message
    );

    if let Some(recommendation) = &finding.recommendation {
        println!("    recommendation: {recommendation}");
    }
}

Ok(())
```

}
''')

touch_dir("crates/monad-cli/tests")

write("crates/monad-cli/tests/smoke.rs", r'''
use assert_cmd::Command;
use predicates::str::contains;

#[test]
fn help_command_works() {
let mut cmd = Command::cargo_bin("monad").unwrap();
cmd.arg("--help")
.assert()
.success()
.stdout(contains("polyglot monorepos"));
}

#[test]
fn list_commands_works() {
let mut cmd = Command::cargo_bin("monad").unwrap();
cmd.args(["list", "commands"])
.assert()
.success()
.stdout(contains("add"))
.stdout(contains("generate"));
}

#[test]
fn doctor_works() {
let mut cmd = Command::cargo_bin("monad").unwrap();
cmd.arg("doctor").assert().success();
}
''')

print("")
print("Scaffold complete.")
print("")
print("Next commands:")
print("  chmod +x scripts/check-rust-workspace.sh")
print("  cargo fmt --all")
print("  cargo check --workspace")
print("  cargo test --workspace")
print("  cargo run -p monad-cli -- --help")
print("  cargo run -p monad-cli -- list commands")

//! Canonical Monad CLI command catalog.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum CommandStage {
    Current,
    Planned,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct CommandGroup {
    pub(crate) name: &'static str,
    pub(crate) stage: CommandStage,
    pub(crate) description: &'static str,
    pub(crate) commands: &'static [&'static str],
}

pub(crate) fn command_groups() -> &'static [CommandGroup] {
    &[
        CommandGroup {
            name: "core",
            stage: CommandStage::Current,
            description: "Stable core CLI commands.",
            commands: &["help", "version", "info", "doctor"],
        },
        CommandGroup {
            name: "foundation",
            stage: CommandStage::Current,
            description: "Current foundation command groups.",
            commands: &["check", "inspect", "graph", "context", "memory"],
        },
        CommandGroup {
            name: "repository",
            stage: CommandStage::Planned,
            description: "Repository creation and initialization commands.",
            commands: &["new", "init", "bootstrap", "wizard", "import", "export"],
        },
        CommandGroup {
            name: "generation",
            stage: CommandStage::Planned,
            description: "Project, code, tooling, and configuration generation commands.",
            commands: &["add", "remove", "generate", "configure"],
        },
        CommandGroup {
            name: "workspace",
            stage: CommandStage::Planned,
            description: "Workspace and project management commands.",
            commands: &["workspace", "project", "app", "service", "package", "lib"],
        },
        CommandGroup {
            name: "tooling",
            stage: CommandStage::Planned,
            description: "Toolchain, template, preset, plugin, and registry commands.",
            commands: &[
                "tool", "install", "upgrade", "migrate", "template", "preset", "plugin", "registry",
            ],
        },
        CommandGroup {
            name: "developer-workflow",
            stage: CommandStage::Planned,
            description: "Daily development task commands.",
            commands: &[
                "dev",
                "run",
                "exec",
                "task",
                "build",
                "test",
                "lint",
                "format",
                "typecheck",
                "clean",
                "reset",
            ],
        },
        CommandGroup {
            name: "environment",
            stage: CommandStage::Planned,
            description: "Environment, configuration, and secret management commands.",
            commands: &["env", "secrets", "config"],
        },
        CommandGroup {
            name: "platform",
            stage: CommandStage::Planned,
            description: "Backend platform capability commands.",
            commands: &[
                "db", "api", "auth", "events", "queue", "cache", "storage", "search",
            ],
        },
        CommandGroup {
            name: "ai-context",
            stage: CommandStage::Planned,
            description: "AI-native repository context and handoff commands.",
            commands: &["ai", "context"],
        },
        CommandGroup {
            name: "delivery",
            stage: CommandStage::Planned,
            description: "CI, CD, container, infrastructure, and deployment commands.",
            commands: &["ci", "cd", "docker", "compose", "k8s", "infra", "deploy"],
        },
        CommandGroup {
            name: "release",
            stage: CommandStage::Planned,
            description: "Release, versioning, and changelog commands.",
            commands: &["release", "version", "changelog"],
        },
        CommandGroup {
            name: "governance",
            stage: CommandStage::Planned,
            description: "Security, policy, compliance, and audit commands.",
            commands: &["security", "policy", "compliance", "audit"],
        },
        CommandGroup {
            name: "observability",
            stage: CommandStage::Planned,
            description: "Observability and operational telemetry commands.",
            commands: &["observability", "telemetry", "logs", "metrics", "trace"],
        },
        CommandGroup {
            name: "quality",
            stage: CommandStage::Planned,
            description: "Coverage, benchmark, dependency, lock, and snapshot commands.",
            commands: &[
                "coverage",
                "benchmark",
                "dependency",
                "lock",
                "snapshot",
                "sync",
                "repair",
            ],
        },
        CommandGroup {
            name: "shell",
            stage: CommandStage::Planned,
            description: "Shell integration and self-management commands.",
            commands: &["completion", "self"],
        },
    ]
}

pub(crate) fn current_commands() -> Vec<&'static str> {
    command_groups()
        .iter()
        .filter(|group| group.stage == CommandStage::Current)
        .flat_map(|group| group.commands.iter().copied())
        .collect()
}

pub(crate) fn planned_commands() -> Vec<&'static str> {
    command_groups()
        .iter()
        .filter(|group| group.stage == CommandStage::Planned)
        .flat_map(|group| group.commands.iter().copied())
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn catalog_contains_current_command_surface() {
        let commands = current_commands();

        for expected in [
            "help", "version", "info", "doctor", "check", "inspect", "graph", "context", "memory",
        ] {
            assert!(commands.contains(&expected), "missing `{expected}`");
        }
    }

    #[test]
    fn catalog_contains_planned_generation_commands() {
        let commands = planned_commands();

        for expected in ["new", "init", "add", "generate", "ci", "docker", "security"] {
            assert!(commands.contains(&expected), "missing `{expected}`");
        }
    }
}

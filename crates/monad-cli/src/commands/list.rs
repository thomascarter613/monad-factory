//! List command surfaces known to the Monad CLI.

use crate::command_catalog::{command_groups, current_commands, planned_commands, CommandStage};

pub(crate) fn render(args: &[String]) -> Result<String, String> {
    match args.first().map(String::as_str).unwrap_or("commands") {
        "commands" => Ok(render_commands()),
        "current" => Ok(render_current()),
        "planned" => Ok(render_planned()),
        "groups" => Ok(render_groups()),
        "help" | "--help" | "-h" => Ok(render_help()),
        unknown => Err(format!(
            "unknown list command `{unknown}`\n\nRun `monad list help` for available list commands."
        )),
    }
}

fn render_help() -> String {
    [
        "Monad list commands",
        "",
        "Usage:",
        "  monad list commands      List current and planned command groups.",
        "  monad list current       List currently implemented command names.",
        "  monad list planned       List planned command names.",
        "  monad list groups        List command groups with descriptions.",
        "  monad list help          Show this help text.",
    ]
    .join("\n")
}

fn render_commands() -> String {
    let mut output = String::from("Monad CLI command catalog\n");

    for group in command_groups() {
        let stage = match group.stage {
            CommandStage::Current => "current",
            CommandStage::Planned => "planned",
        };

        output.push('\n');
        output.push_str(group.name);
        output.push_str(" [");
        output.push_str(stage);
        output.push_str("]\n");

        for command in group.commands {
            output.push_str("  monad ");
            output.push_str(command);
            output.push('\n');
        }
    }

    output
}

fn render_current() -> String {
    let mut output = String::from("Current Monad CLI commands\n\n");

    for command in current_commands() {
        output.push_str("  monad ");
        output.push_str(command);
        output.push('\n');
    }

    output
}

fn render_planned() -> String {
    let mut output = String::from("Planned Monad CLI commands\n\n");

    for command in planned_commands() {
        output.push_str("  monad ");
        output.push_str(command);
        output.push('\n');
    }

    output
}

fn render_groups() -> String {
    let mut output = String::from("Monad CLI command groups\n");

    for group in command_groups() {
        let stage = match group.stage {
            CommandStage::Current => "current",
            CommandStage::Planned => "planned",
        };

        output.push('\n');
        output.push_str(group.name);
        output.push_str(" [");
        output.push_str(stage);
        output.push_str("]\n  ");
        output.push_str(group.description);
        output.push('\n');
    }

    output
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn renders_command_catalog() {
        let output = render(&["commands".to_string()]).expect("catalog should render");

        assert!(output.contains("Monad CLI command catalog"));
        assert!(output.contains("monad help"));
        assert!(output.contains("monad add"));
        assert!(output.contains("monad generate"));
    }

    #[test]
    fn renders_current_commands() {
        let output = render(&["current".to_string()]).expect("current commands should render");

        assert!(output.contains("monad doctor"));
        assert!(output.contains("monad check"));
    }

    #[test]
    fn renders_planned_commands() {
        let output = render(&["planned".to_string()]).expect("planned commands should render");

        assert!(output.contains("monad new"));
        assert!(output.contains("monad add"));
        assert!(output.contains("monad ci"));
    }
}

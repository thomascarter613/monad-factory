//! CLI argument parsing and dispatch.

use std::fmt::{Display, Formatter};

use crate::commands;

#[derive(Debug, Clone, Eq, PartialEq)]
pub struct CliError {
    message: String,
}

impl CliError {
    pub fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
        }
    }
}

impl Display for CliError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(&self.message)
    }
}

impl std::error::Error for CliError {}

pub fn run(args: &[String]) -> Result<String, CliError> {
    let Some(command) = args.first() else {
        return Ok(commands::root_help());
    };

    let rest = &args[1..];

    match command.as_str() {
        "help" | "--help" | "-h" => Ok(commands::root_help()),
        "version" | "--version" | "-V" => Ok(commands::info::version_text()),
        "info" => Ok(commands::info::info_text()),
        "doctor" => Ok(commands::info::doctor_text()),
        "check" => commands::check::render(rest).map_err(CliError::new),
        "inspect" => commands::inspect::render(rest).map_err(CliError::new),
        "graph" => commands::graph::render(rest).map_err(CliError::new),
        "context" => commands::context::render(rest).map_err(CliError::new),
        "memory" => commands::memory::render(rest).map_err(CliError::new),
        unknown => Err(CliError::new(format!(
            "unknown command `{unknown}`\n\nRun `monad help` for available commands."
        ))),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn args(values: &[&str]) -> Vec<String> {
        values.iter().map(ToString::to_string).collect()
    }

    fn run_ok(values: &[&str]) -> Result<String, String> {
        run(&args(values)).map_err(|error| error.to_string())
    }

    #[test]
    fn help_is_default() -> Result<(), String> {
        let output = run_ok(&[])?;

        assert!(output.contains("Monad Factory CLI"));
        assert!(output.contains("monad check"));
        assert!(output.contains("monad memory"));

        Ok(())
    }

    #[test]
    fn version_uses_canonical_cli_name() -> Result<(), String> {
        let output = run_ok(&["version"])?;

        assert!(output.starts_with("monad "));

        Ok(())
    }

    #[test]
    fn info_uses_canonical_product_name() -> Result<(), String> {
        let output = run_ok(&["info"])?;

        assert!(output.contains(monad_core::PRODUCT_NAME));
        assert!(output.contains("phase: pre-implementation foundation"));

        Ok(())
    }

    #[test]
    fn command_groups_are_registered() -> Result<(), String> {
        let commands = [
            ["check", "all"],
            ["inspect", "workspace"],
            ["graph", "text"],
            ["context", "help"],
            ["memory", "status"],
        ];

        for command in commands {
            let output = run_ok(&command)?;
            assert!(!output.trim().is_empty());
        }

        Ok(())
    }

    #[test]
    fn unknown_command_fails() -> Result<(), String> {
        let error = match run(&args(&["nope"])) {
            Ok(output) => {
                return Err(format!(
                    "unknown command should fail but returned successful output: {output}"
                ));
            }
            Err(error) => error.to_string(),
        };

        assert!(error.contains("unknown command"));

        Ok(())
    }
}

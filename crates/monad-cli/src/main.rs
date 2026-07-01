//! Public `monad` command-line interface.

use monad_core::{build_info, CLI_NAME};

const HELP: &str = "Monad Factory CLI\n\nUsage:\n  monad help\n  monad version\n  monad info\n  monad doctor\n\nCommands:\n  help      Show this help text.\n  version   Show CLI version.\n  info      Show product and implementation information.\n  doctor    Explain how to run the repository doctor.\n";

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();

    match run(&args) {
        Ok(output) => {
            println!("{output}");
        }
        Err(message) => {
            eprintln!("{message}");
            std::process::exit(2);
        }
    }
}

fn run(args: &[String]) -> Result<String, String> {
    let command = args.first().map_or("help", String::as_str);

    match command {
        "help" | "--help" | "-h" => Ok(help_text()),
        "version" | "--version" | "-V" => Ok(version_text()),
        "info" => Ok(info_text()),
        "doctor" => Ok(doctor_text()),
        unknown => Err(format!(
            "unknown command `{unknown}`\n\nRun `monad help` for available commands."
        )),
    }
}

fn help_text() -> String {
    HELP.to_string()
}

fn version_text() -> String {
    let info = build_info();
    format!("{} {}", info.cli_name, info.version)
}

fn info_text() -> String {
    let info = build_info();

    format!(
        "product: {}\ncli: {}\nversion: {}\nphase: {}",
        info.product_name, info.cli_name, info.version, info.phase
    )
}

fn doctor_text() -> String {
    format!(
        "`{CLI_NAME} doctor` is reserved for the native CLI doctor. For the current repository foundation, run `bun run doctor`."
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    fn args(values: &[&str]) -> Vec<String> {
        values.iter().map(ToString::to_string).collect()
    }

    #[test]
    fn help_is_default() -> Result<(), String> {
        let output = run(&args(&[]))?;

        assert!(output.contains("Monad Factory CLI"));
        assert!(output.contains("monad help"));

        Ok(())
    }

    #[test]
    fn version_uses_canonical_cli_name() -> Result<(), String> {
        let output = run(&args(&["version"]))?;

        assert!(output.starts_with("monad "));

        Ok(())
    }

    #[test]
    fn info_uses_canonical_product_name() -> Result<(), String> {
        let output = run(&args(&["info"]))?;

        assert!(output.contains(monad_core::PRODUCT_NAME));
        assert!(output.contains("phase: pre-implementation foundation"));

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
            Err(error) => error,
        };

        assert!(error.contains("unknown command"));

        Ok(())
    }
}

//! Public `monad` command-line interface.

mod cli;
mod command_catalog;
mod commands;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();

    if args.first().map(String::as_str) == Some("list") {
        match commands::list::render(&args[1..]) {
            Ok(output) => {
                println!("{output}");
                return;
            }
            Err(error) => {
                eprintln!("{error}");
                std::process::exit(2);
            }
        }
    }

    match cli::run(&args) {
        Ok(output) => {
            println!("{output}");
        }
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(2);
        }
    }
}

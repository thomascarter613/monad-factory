//! Public `monad` command-line interface.

mod cli;
mod commands;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();

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

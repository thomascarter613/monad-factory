//! Command rendering modules for the `monad` CLI.

pub mod check;
pub mod context;
pub mod graph;
pub mod info;
pub mod inspect;
pub mod memory;

pub fn root_help() -> String {
    [
        "Monad Factory CLI",
        "",
        "Usage:",
        "  monad <command> [arguments]",
        "",
        "Core commands:",
        "  monad help                 Show this help text.",
        "  monad version              Show CLI version.",
        "  monad info                 Show product and implementation information.",
        "  monad doctor               Explain how to run repository doctor checks.",
        "",
        "Foundation command groups:",
        "  monad check [target]       Validate foundation, toolchain, Rust, CI, or all checks.",
        "  monad inspect [target]     Inspect workspace, scope, toolchain, or memory state.",
        "  monad graph [format]       Render the registered graph command surface.",
        "  monad context <command>    Work with context packs, handoffs, and AI exports.",
        "  monad memory [command]     Inspect local-first Monad Memory foundations.",
        "",
        "This command surface is part of core v1 scope. Current outputs are deterministic",
        "foundation responses that anchor the stable CLI shape while the deeper engines are",
        "implemented under the approved v1 maximal functional plan.",
    ]
    .join("\n")
}

pub fn unknown_argument(command: &str, value: &str, allowed: &[&str]) -> String {
    format!(
        "unknown argument `{value}` for `monad {command}`\n\nAllowed values: {}",
        allowed.join(", ")
    )
}

pub(crate) mod list;

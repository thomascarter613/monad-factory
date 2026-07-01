//! Informational command renderers.

use monad_core::{build_info, CLI_NAME};

pub fn version_text() -> String {
    let info = build_info();
    format!("{} {}", info.cli_name, info.version)
}

pub fn info_text() -> String {
    let info = build_info();

    [
        format!("product: {}", info.product_name),
        format!("cli: {}", info.cli_name),
        format!("version: {}", info.version),
        format!("phase: {}", info.phase),
        "scope: v1 maximal functional product-factory platform".to_string(),
        "source_of_truth: docs/product/v1-maximal-functional-scope-and-delivery-plan.md"
            .to_string(),
    ]
    .join("\n")
}

pub fn doctor_text() -> String {
    format!(
        "`{CLI_NAME} doctor` is reserved for the native CLI doctor command. For the current repository foundation, run `bun run doctor` or `bun run doctor:strict`."
    )
}

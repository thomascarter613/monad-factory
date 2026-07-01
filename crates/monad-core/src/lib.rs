//! Core domain primitives and shared runtime contracts for Monad Factory.

/// Canonical product name.
pub const PRODUCT_NAME: &str = "Monad Factory";

/// Canonical public CLI command name.
pub const CLI_NAME: &str = "monad";

/// Current implementation phase.
pub const IMPLEMENTATION_PHASE: &str = "pre-implementation foundation";

/// Build and product identity exposed by the CLI and future services.
#[derive(Debug, Clone, Eq, PartialEq)]
pub struct BuildInfo {
    /// Product name.
    pub product_name: &'static str,

    /// CLI command name.
    pub cli_name: &'static str,

    /// Cargo package version.
    pub version: &'static str,

    /// Current implementation phase.
    pub phase: &'static str,
}

/// Return build and product identity for the current crate graph.
#[must_use]
pub const fn build_info() -> BuildInfo {
    BuildInfo {
        product_name: PRODUCT_NAME,
        cli_name: CLI_NAME,
        version: env!("CARGO_PKG_VERSION"),
        phase: IMPLEMENTATION_PHASE,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn build_info_uses_canonical_names() {
        let info = build_info();

        assert_eq!(info.product_name, "Monad Factory");
        assert_eq!(info.cli_name, "monad");
        assert_eq!(info.phase, "pre-implementation foundation");
    }
}

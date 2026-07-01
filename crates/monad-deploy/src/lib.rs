//! Deployment integration primitives for Docker, Kubernetes, Nomad, Helm, and `OpenTofu` paths.

/// Return the canonical crate name.
#[must_use]
pub const fn crate_name() -> &'static str {
    "monad_deploy"
}

/// Return the canonical public CLI name from the shared core crate.
#[must_use]
pub const fn cli_name() -> &'static str {
    monad_core::CLI_NAME
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exposes_canonical_crate_name() {
        assert_eq!(crate_name(), "monad_deploy");
    }

    #[test]
    fn shares_canonical_cli_name() {
        assert_eq!(cli_name(), "monad");
    }
}

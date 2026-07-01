# Native Context Command Group

The `monad context` command group exposes native context-pack, verification, handoff, and export state.

Examples:

```bash
cargo run -p monad-cli -- context pack
cargo run -p monad-cli -- context verify
cargo run -p monad-cli -- context handoff
cargo run -p monad-cli -- context exports
```

Current commands:

- `monad context pack`
- `monad context verify`
- `monad context handoff`
- `monad context exports`

The native context foundation currently combines:

- canonical v1 source-of-truth document
- workspace manifest
- Rust workspace manifest
- root package manifest
- Monad Memory index
- memory policy
- CLI command surface documentation
- agent instructions
- repository graph status
- memory backend status
- root toolchain declaration status

This is part of the approved v1 maximal functional context-pack, handoff, AI-tool export, governance, AI-readiness, and CLI scope.

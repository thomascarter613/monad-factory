# Native Toolchain Check

`monad check toolchain` runs a native validation engine over the root development control plane.

Example:

```bash
cargo run -p monad-cli -- check toolchain
```

Current checks include:

- expected root toolchain files
- expected `mise.toml` tool declarations
- Bun package manager declaration
- Rust toolchain channel declaration
- root check script presence
- root toolchain check script presence
- Rust check script presence
- moon workspace/toolchain configuration presence
- Cargo workspace declaration

This is part of the approved v1 maximal functional CLI, governance, and root control-plane scope.

# Toolchain Inspection

`monad inspect toolchain` runs a native inspection pass over the root development control plane.

Example:

```bash
cargo run -p monad-cli -- inspect toolchain
```

The command currently reports:

- expected root toolchain files
- expected `mise.toml` tool declarations
- Bun package manager declaration
- Rust toolchain channel declaration
- root check script presence
- moon workspace/toolchain configuration presence
- Cargo workspace presence

This is part of the approved v1 maximal functional CLI and governance scope. It does not replace deeper future validation; it establishes the first native inspection engine for the root toolchain.

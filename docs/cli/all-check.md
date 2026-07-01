# Native Aggregate Check

`monad check all` runs the native aggregate readiness check.

Example:

```bash
cargo run -p monad-cli -- check all
```

The aggregate currently includes:

- native foundation check
- native toolchain check
- native memory check
- native context foundation readiness
- native repository graph readiness

This replaces the earlier delegated-only `monad check all` response with a native report while preserving root `bun run check` as the full local/CI validation command.

This is part of the approved v1 maximal functional CLI, governance, inspection, memory, context, graph, and repository-control scope.

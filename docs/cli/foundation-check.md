# Native Foundation Check

`monad check foundation` runs the first native validation engine in the public `monad` CLI.

It uses the core workspace inspection engine to validate the repository foundation directly instead of only describing a delegated shell command.

Example:

```bash
cargo run -p monad-cli -- check foundation
```

Current checks include:

- workspace manifest presence and loadability
- expected top-level domain coverage
- expected foundation file coverage
- canonical v1 scope document presence
- Monad Memory index presence
- Rust workspace presence
- root toolchain manifest presence

This command is part of the approved v1 maximal functional CLI scope. It is intentionally implemented as a real native engine now, while deeper validation engines continue to be added incrementally under the same v1 plan.

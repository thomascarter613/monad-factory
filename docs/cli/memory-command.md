# Native Memory Command Group

The `monad memory` command group exposes native Monad Memory foundation state through the public CLI.

Examples:

```bash
cargo run -p monad-cli -- memory status
cargo run -p monad-cli -- memory backends
cargo run -p monad-cli -- memory policy
```

Current commands:

- `monad memory status`
- `monad memory backends`
- `monad memory policy`

These commands use the same native memory inspection engine as `monad inspect memory` and `monad check memory`.

This is part of the approved v1 maximal functional memory, governance, AI-readiness, context-continuity, and CLI scope.

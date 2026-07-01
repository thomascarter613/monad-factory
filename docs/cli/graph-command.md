# Native Graph Command

`monad graph` renders a native repository graph model built from actual workspace inspection.

Examples:

```bash
cargo run -p monad-cli -- graph text
cargo run -p monad-cli -- graph json
cargo run -p monad-cli -- graph mermaid
cargo run -p monad-cli -- graph dot
```

Supported formats:

- `text`
- `json`
- `mermaid`
- `dot`

The graph currently includes the repository root and expected top-level v1 foundation domains, with presence status derived from the workspace inspection engine.

This is part of the approved v1 maximal functional graph, CLI, governance, inspection, context, and AI-readiness scope.

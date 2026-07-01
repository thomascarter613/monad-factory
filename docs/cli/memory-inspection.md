# Memory Inspection

`monad inspect memory` runs a native inspection pass over the local-first Monad Memory foundation.

Example:

```bash
cargo run -p monad-cli -- inspect memory
```

Current inspection includes:

- `.monad/memory/MEMORY.md`
- `policies/memory/memory-policy.md`
- `.monad/config.toml`
- `docs/memory/00-index.md`
- canonical v1 scope document presence
- planned memory backend registration for SQLite, pgvector, and Qdrant
- local-first, inspectable, and policy-governed memory language

This is part of the approved v1 maximal functional memory, governance, CLI, and AI-readiness scope.

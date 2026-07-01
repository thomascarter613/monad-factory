# Workspace Inspection

`monad inspect workspace` performs the first real repository inspection pass for Monad Factory.

It reads the actual repository root, verifies that `workspace.toml` can be loaded, checks expected top-level v1 foundation domains, checks expected foundation files, and renders deterministic output for humans and future automation.

Example:

```bash
cargo run -p monad-cli -- inspect workspace
```

The command currently reports:

- workspace root
- workspace manifest load status
- workspace manifest line count
- expected top-level domains present
- expected foundation files present
- missing domains
- missing foundation files
- per-domain entry counts

This is not a downgrade of the v1 scope. It is the first concrete inspection engine under the approved maximal functional v1 command surface.

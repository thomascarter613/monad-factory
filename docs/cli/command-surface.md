# Monad CLI Command Surface

The public CLI command name is:

```txt
monad
```

The first stable command surface includes:

```txt
monad help
monad version
monad info
monad doctor
monad check [target]
monad inspect [target]
monad graph [format]
monad context <command>
monad memory [command]
```

This command surface is part of the approved v1 maximal functional scope. The current implementation establishes deterministic foundation responses, test coverage, and stable command grouping while deeper engines are implemented under the canonical v1 delivery plan.

The canonical v1 source of truth remains:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```

## Check targets

```txt
all
foundation
toolchain
ci
github-planning
rust
```

## Inspect targets

```txt
workspace
scope
toolchain
memory
```

## Graph formats

```txt
text
json
mermaid
dot
```

## Context commands

```txt
pack
verify
handoff
exports
```

## Memory commands

```txt
status
backends
policy
```

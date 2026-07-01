# Toolchain Strategy

## Principle

Monad OS should wrap and coordinate native tools rather than replace all of them.

Monad owns:

- intent
- graph
- policy
- evidence
- recommendations
- user-facing workflow

Native tools provide execution.

## Default Direction

Recommended defaults:

- CLI/core: Rust
- package manager: Bun
- docs frontend: Fumadocs
- JS/TS task graph backend: Nx under Monad wrapper
- optional polyglot task backend: moon
- portable CI execution: Dagger
- optional strict reproducibility: Nix
- enterprise hermetic backend: Pants or Buck2
- maximum-scale backend: Buck2

## Nx Under the Hood

Nx may be used internally while the user-facing interface remains Monad.

Example user command:

```bash
monad run web:build
```

Internal backend may call:

```bash
nx run web:build
```

Monad should not dishonestly hide Nx. It should abstract Nx as an implementation backend.

## Non-Bazel Enterprise Build Options

Bazel remains a reference point for hermetic large-scale builds, but Monad should support non-Bazel options:

- Buck2 for maximum-scale enterprise builds
- Pants for backend-heavy and Python-heavy enterprise monorepos
- Please as a less mainstream but interesting reproducible build option
- Nix for reproducible environments and remote builders/caches
- Dagger for portable CI execution
- Earthly for containerized repeatable builds
- Gradle/Develocity for JVM-heavy enterprise teams

## Key Rule

Build engines are replaceable.

Monad should not be permanently coupled to one task runner, build system, CI system, package manager, cloud, database, or AI provider.

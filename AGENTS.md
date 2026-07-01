title: "AI Agent Instructions"
description: "Repository instructions for AI assistants and agentic workflows."
status: "approved"
canonical: true
---------------

# AI Agent Instructions

The canonical v1 planning artifact is:

```txt
docs/product/v1-maximal-functional-scope-and-delivery-plan.md
```

AI assistants must treat that document as the source of truth for v1 scope.

## Rules

AI assistants should:

1. Prefer explicit, reviewable changes.
2. Preserve local-first usability.
3. Avoid introducing secrets.
4. Avoid unapproved network dependencies.
5. Link changes back to work packets.
6. Update documentation when behavior changes.
7. Preserve maximal functional v1 scope.
8. Avoid silently downgrading features to scaffold-only or post-v1.
9. Produce verification commands after meaningful changes.

Private memory must not be committed unless explicitly exported and reviewed.

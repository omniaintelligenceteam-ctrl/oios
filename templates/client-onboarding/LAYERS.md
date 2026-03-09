---
layer: reference
cadence: never
description: Explains the 5-layer context hierarchy for this client
---

# Context Layers

All context is organized into 5 layers. Higher layers change less often and carry more weight.

| Layer | Purpose | Update Cadence | Files |
|-------|---------|----------------|-------|
| **L0 — Foundation** | Identity, voice, values | Never (unless company changes) | `L0-identity.md`, `L0-communication.md` |
| **L1 — Strategy** | Products, pricing, goals | Quarterly | `L1-business.md`, `L1-goals.md` |
| **L2 — Operations** | Current focus, tools, team | Weekly / as-needed | `L2-priorities.md`, `L2-tools.md`, `L2-team.md` |
| **L3 — Projects** | Per-project context | Per-project | Created as needed |
| **L4 — Sessions** | Scratch notes, quick captures | Ephemeral | Created as needed |

## Rules

- L0-L1 files are the source of truth. If lower layers conflict, L0-L1 wins.
- Every context file has YAML frontmatter showing its layer and update cadence.

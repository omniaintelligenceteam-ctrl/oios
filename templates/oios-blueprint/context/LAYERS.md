---
layer: reference
cadence: never
description: Context layer hierarchy reference
---

# Context Layers (SSoT Hierarchy)

All context is organized into 5 layers. Higher layers change less often and carry more weight.

| Layer | Purpose | Update Cadence | Files |
|-------|---------|----------------|-------|
| **L0 — Foundation** | Identity, voice, values | Never (unless company changes) | `company.md`, `voice.md` |
| **L1 — Strategy** | Services, pricing, goals | Quarterly | `services.md`, `goals.md` |
| **L2 — Operations** | Current focus, tools, team | Weekly / as-needed | `priorities.md`, `team.md`, `tools.md` |
| **L3 — Projects** | Per-project context | Per-project | `pipeline/`, `jobs/` |
| **L4 — Sessions** | Scratch notes, quick captures | Ephemeral | `calls/`, `briefings/` |

## Rules

- L0-L1 files are the source of truth. If L2-L4 conflicts with L0-L1, L0-L1 wins.
- Always check the layer before updating — don't update L0 files casually.
- When in doubt about which file to update, check this reference.

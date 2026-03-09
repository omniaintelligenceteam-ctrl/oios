---
layer: reference
cadence: never
description: Explains the 5-layer context hierarchy
---

# Context Layers (SSoT Hierarchy)

All context is organized into 5 layers. Higher layers change less often and carry more weight.

| Layer | Purpose | Update Cadence | Location |
|-------|---------|----------------|----------|
| **L0 — Foundation** | Identity, voice, values | Never (unless company changes) | `context/me.md`, `context/communication-defaults.md` |
| **L1 — Strategy** | Products, pricing, goals | Quarterly | `context/work.md`, `context/goals.md` |
| **L2 — Operations** | Current focus, tools, team | Weekly / as-needed | `context/current-priorities.md`, `context/tools-and-integrations.md`, `context/team.md` |
| **L3 — Projects** | Per-project context | Per-project | `projects/` (one folder per project) |
| **L4 — Sessions** | Scratch notes, quick captures | Ephemeral | `inbox/` |

## When to Update What

- **Focus shifts mid-week** → update `current-priorities.md` (L2)
- **New quarter starts** → update `goals.md` (L1), review `work.md` (L1)
- **New tool/integration added** → update `tools-and-integrations.md` (L2)
- **New project kicks off** → create folder in `projects/` (L3)
- **Quick idea or raw note** → drop in `inbox/` (L4), process later
- **Company identity changes** → update `me.md` (L0) — rare

## Rules

- L0-L1 files are the source of truth. If L2-L4 conflicts with L0-L1, L0-L1 wins.
- L3 and L4 are never auto-loaded — reference them when working on a specific project.
- Every context file has YAML frontmatter showing its layer and update cadence.

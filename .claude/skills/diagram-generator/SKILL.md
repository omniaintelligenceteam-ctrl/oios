---
name: diagram-generator
description: >
  Generate polished HTML diagrams from plain English descriptions or structured lists. Auto-detects the best diagram type (flowchart, process map, architecture, decision tree, org chart, sequence diagram). No external APIs needed. Outputs a self-contained HTML file that opens in any browser. Triggers on "make a diagram", "create a flowchart", "diagram this", "visualize this process", "draw a decision tree", or /diagram-generator. Also triggers on "map out this process", "show me how this flows", or "turn this into a diagram".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Diagram Generator

Turn plain English descriptions or structured lists into polished, self-contained HTML diagrams. Auto-detects diagram type. No API keys, no installs — opens in any browser.

## Diagram Types

| Type | Use when... | Mermaid syntax |
|------|-------------|----------------|
| Flowchart | Steps, decisions, branching paths | `flowchart TD` |
| Sequence | Two or more systems interacting | `sequenceDiagram` |
| Process map | Linear workflow, stages | `flowchart LR` |
| Decision tree | If/then branches, choices | `flowchart TD` with diamonds |
| Org chart | Hierarchy, reporting structure | `flowchart TD` |
| Architecture | System components and connections | `flowchart LR` |

## Execution

### 1. Parse the input

Extract:
- **What to diagram** — the process, system, or flow being described
- **Diagram type** — auto-detect from content, or use what the user specifies
- **Title** — derive from the description or ask if unclear

### 2. Detect the best diagram type

Rules:
- Steps in sequence → flowchart (top-down) or process map (left-right)
- "If X then Y" → decision tree
- "System A sends to System B" → sequence diagram
- "Reports to / manages" → org chart
- Components with connections → architecture diagram

### 3. Write the Mermaid syntax

Generate clean, readable Mermaid. Rules:
- Node labels: short (3-5 words max)
- Use shapes: rectangles for steps, diamonds for decisions, rounded for start/end
- Left-right layout for long horizontal flows, top-down for hierarchies
- Group related nodes with subgraphs when helpful

### 4. Wrap in styled HTML

Output a self-contained HTML file with embedded Mermaid.js:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{TITLE}</title>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>
    body {
      background: #0f172a;
      color: #e2e8f0;
      font-family: 'Segoe UI', system-ui, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 40px 20px;
    }
    h1 {
      font-size: 1.75rem;
      font-weight: 700;
      margin-bottom: 8px;
      color: #f8fafc;
    }
    p.subtitle {
      color: #64748b;
      font-size: 0.9rem;
      margin-bottom: 40px;
    }
    .mermaid {
      background: #1e293b;
      border-radius: 12px;
      padding: 40px;
      border: 1px solid #334155;
      max-width: 1200px;
      width: 100%;
    }
    .brand {
      margin-top: 24px;
      font-size: 0.75rem;
      color: #334155;
    }
  </style>
</head>
<body>
  <h1>{TITLE}</h1>
  <p class="subtitle">{SUBTITLE}</p>
  <div class="mermaid">
{MERMAID_SYNTAX}
  </div>
  <div class="brand">Omnia Intelligence AI</div>
  <script>mermaid.initialize({ theme: 'dark', startOnLoad: true });</script>
</body>
</html>
```

### 5. Save the file

Save to: `projects/diagrams/{descriptive-name}.html`

### 6. Deliver

- Provide the file path
- Tell the user: "Open in your browser — F11 for fullscreen"
- Offer to adjust layout, add detail, or change colors

## Edge cases

- **Input is too vague**: Ask one question — "What's the starting point and the end goal?"
- **Too many steps for one diagram**: Split into 2 diagrams or use subgraphs
- **User specifies a type**: Use it, don't override their choice
- **Mermaid syntax error risk**: Keep node labels simple, avoid special characters in labels

## Output files

| File | Description |
|------|-------------|
| `projects/diagrams/{name}.html` | Self-contained diagram file |

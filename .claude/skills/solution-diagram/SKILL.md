---
name: solution-diagram
description: >
  Generate polished, client-facing demo visuals that show how OIOS automates a business workflow. Takes a description of a client's problem and the AI solution, outputs a professional HTML diagram you can screenshare on demos. Triggers on "solution diagram", "demo visual", "make a visual for this client", "show how this works", "create a demo diagram", "visualize the solution", or /solution-diagram. Also triggers on phrases like "make something to show the prospect", "build a workflow visual", or "diagram this for a demo".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Solution Diagram

Generate a polished, client-facing HTML visual that shows exactly how OIOS automates a business workflow. The output looks professional enough to show on a demo call — dark-themed, icon-rich, three-panel layout: Problem → OIOS Processing → Automated Results.

## When to Use

- Prepping for a demo with a specific prospect
- Showing a CEO what their workflow looks like after AI implementation
- Creating a leave-behind visual after a sales call
- Visualizing any "before AI / after AI" transformation

## Execution

### 1. Gather the info

Extract from the user's message:
- **Client/industry** — who is this for? (e.g., "landscaping company", "dental office", "auto dealership")
- **The problem** — what's painful right now? (e.g., "misses calls after hours", "manually enters leads into CRM")
- **The AI solution** — what does OIOS do? (e.g., "AI receptionist captures every call", "auto-scores leads and routes to CRM")
- **The outputs/actions** — what automatically happens? (e.g., "confirmation text sent", "follow-up scheduled", "owner alerted via Slack")
- **Title** — a punchy headline for the diagram (e.g., "AI Receptionist — Never Miss a Lead Again")

If any of these are missing, ask one focused question to fill in the gap.

### 2. Generate the HTML visual

Output a single self-contained HTML file. No external dependencies except Mermaid CDN (optional — for flow diagrams) or pure CSS/SVG for the layout.

#### Layout: Three-panel horizontal flow

```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   THE PROBLEM   │ →  │   OIOS PROCESSING    │ →  │  AUTOMATIC ACTIONS  │
│                 │    │                      │    │                     │
│ [Trigger event] │    │ Step 1: Transcribe   │    │ ✓ Text confirmation │
│                 │    │ Step 2: Extract info │    │ ✓ CRM entry         │
│ [Pain point]    │    │ Step 3: Score lead   │    │ ✓ Owner alert       │
│                 │    │ Step 4: Detect intent│    │ ✓ Follow-up queued  │
└─────────────────┘    └──────────────────────┘    └─────────────────────┘
```

#### HTML template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TITLE}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0f172a;
      color: #e2e8f0;
      font-family: 'Segoe UI', system-ui, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 40px 20px;
    }
    .header {
      text-align: center;
      margin-bottom: 12px;
    }
    .header h1 {
      font-size: 2rem;
      font-weight: 700;
      color: #f8fafc;
      letter-spacing: -0.5px;
    }
    .header p {
      color: #94a3b8;
      font-size: 1rem;
      margin-top: 6px;
    }
    .diagram {
      display: flex;
      align-items: stretch;
      gap: 0;
      width: 100%;
      max-width: 1100px;
      margin-top: 32px;
    }
    .panel {
      flex: 1;
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 28px 24px;
    }
    .panel-title {
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: #64748b;
      margin-bottom: 20px;
    }
    .panel.trigger { border-color: #475569; }
    .panel.process { border-color: #6366f1; background: #1a1f3a; }
    .panel.actions { border-color: #10b981; background: #0f2018; }
    .arrow {
      display: flex;
      align-items: center;
      padding: 0 12px;
      color: #475569;
      font-size: 1.8rem;
    }
    .trigger-box {
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 16px;
      text-align: center;
      margin-bottom: 12px;
    }
    .trigger-box .icon { font-size: 2rem; margin-bottom: 8px; }
    .trigger-box .label { font-size: 0.85rem; color: #94a3b8; }
    .step {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 12px;
      background: #0f172a;
      border-radius: 8px;
      margin-bottom: 10px;
      border: 1px solid #2d3748;
    }
    .step-icon {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: #6366f1;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
      flex-shrink: 0;
    }
    .step-text .step-title {
      font-size: 0.85rem;
      font-weight: 600;
      color: #e2e8f0;
    }
    .step-text .step-desc {
      font-size: 0.75rem;
      color: #64748b;
      margin-top: 2px;
    }
    .action-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 12px;
      background: #0f1f14;
      border-radius: 8px;
      margin-bottom: 10px;
      border: 1px solid #1a3a24;
    }
    .action-icon {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      background: #10b981;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
      flex-shrink: 0;
    }
    .action-text {
      font-size: 0.85rem;
      color: #a7f3d0;
      font-weight: 500;
    }
    .action-sub {
      font-size: 0.72rem;
      color: #4ade80;
      margin-top: 2px;
    }
    .brand {
      margin-top: 32px;
      font-size: 0.75rem;
      color: #334155;
      text-align: center;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>{TITLE}</h1>
    <p>{SUBTITLE}</p>
  </div>

  <div class="diagram">
    <!-- Panel 1: The Problem / Trigger -->
    <div class="panel trigger">
      <div class="panel-title">The Problem</div>
      {TRIGGER_CONTENT}
    </div>

    <div class="arrow">→</div>

    <!-- Panel 2: OIOS Processing -->
    <div class="panel process">
      <div class="panel-title">OIOS Processing</div>
      {PROCESS_STEPS}
    </div>

    <div class="arrow">→</div>

    <!-- Panel 3: Automatic Actions -->
    <div class="panel actions">
      <div class="panel-title">Automatic Actions</div>
      {ACTION_ITEMS}
    </div>
  </div>

  <div class="brand">Powered by Omnia Intelligence AI · omniaintelligence.ai</div>
</body>
</html>
```

### 3. Populate the template

Fill in all `{PLACEHOLDERS}` with content specific to this client/use case:

- `{TITLE}` — punchy headline (e.g., "AI Receptionist — Never Miss a Lead Again")
- `{SUBTITLE}` — one-liner value prop (e.g., "Every call captured. Every lead scored. Every follow-up automatic.")
- `{TRIGGER_CONTENT}` — 1-2 trigger boxes showing what currently happens (the problem)
- `{PROCESS_STEPS}` — 3-5 step cards showing what OIOS does in sequence
- `{ACTION_ITEMS}` — 3-5 action cards showing what automatically happens as a result

Use relevant emojis as icons. Match the content to the client's industry and specific pain points.

### 4. Save the file

Save to: `projects/diagrams/{client-name}-solution-diagram.html`

If no client name is given, use: `projects/diagrams/solution-diagram-{YYYY-MM-DD}.html`

### 5. Deliver

Tell the user:
- File path (clickable)
- "Open in your browser to preview — looks best in fullscreen (F11)"
- Offer to tweak colors, content, or layout

## Customization

After generating, offer these quick tweaks if the user wants:
- **Different color scheme** — swap the green actions panel to blue, purple, orange
- **Add client logo** — drop in a logo URL at the top
- **More/fewer steps** — adjust the process panel
- **Different title/subtitle** — sharpen the copy

## Examples of use

- "Make a solution diagram for a landscaping company — they miss calls on job sites"
- "Create a demo visual for a dental office showing automated appointment reminders"
- "Show how OIOS handles lead follow-up for a car dealership"
- "Build a diagram showing the AI email triage workflow"

## Output files

| File | Description |
|------|-------------|
| `projects/diagrams/{client}-solution-diagram.html` | Client-facing demo visual |

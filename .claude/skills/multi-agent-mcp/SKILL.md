---
name: multi-agent-mcp
description: >
  Register other AI tools (Codex, other Claude instances, Gemini) as MCP servers so Claude can orchestrate them as specialized workers. Use when building complex features that benefit from parallel implementation across multiple models — Claude reasons and plans, workers implement. Triggers on "multi-agent MCP", "delegate to Codex", "orchestrate workers", "register MCP workers", or requests to parallelize across multiple AI models.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Multi-Agent MCP Orchestration

Register other AI tools (Codex, other Claude instances) as MCP servers. Claude becomes the manager, delegating to specialized workers — each behaving like a separate engineer on your team.

## How it works

```bash
claude mcp add codex-review -- codex mcp-server
claude mcp add codex-refactor -- codex mcp-server
claude mcp add codex-tests -- codex mcp-server
```

Each registered tool behaves like a separate engineer. Claude dispatches tasks, collects results, validates. Local multi-agent dev loop with role separation: Claude reasons + plans, workers implement.

## Why it works

Different models have different strengths. Claude is the best reasoner and planner. Codex is strong at isolated coding tasks in sandboxed environments. Gemini can process video and massive context windows. By wiring them together via MCP, you get the best of all worlds — orchestrated by the strongest planner.

## Demo

Set up a real project where Claude manages three Codex workers. Give Claude a feature request. Watch it break the task into subtasks, delegate each to a different Codex instance (one for frontend, one for backend, one for tests), collect results, review for consistency, and merge. Show the actual MCP server registration and the back-and-forth in the terminal.

## The prompt

The CLAUDE.md instructions that tell Claude how to use its MCP-registered workers. How to define roles, set expectations, handle failures.

## When to use it

Complex projects where you want to parallelize implementation across multiple models. Overkill for simple tasks.

## Setup

```bash
# Register workers by role
claude mcp add codex-frontend -- codex mcp-server
claude mcp add codex-backend -- codex mcp-server
claude mcp add codex-tests -- codex mcp-server
```

Add to your CLAUDE.md:

```markdown
## Worker Roles
- codex-frontend: UI components, styling, client-side logic
- codex-backend: API routes, database queries, server logic
- codex-tests: Unit tests, integration tests, test coverage

## Orchestration Rules
1. Break feature requests into frontend / backend / test subtasks
2. Dispatch each subtask to the appropriate worker
3. Collect results and review for consistency
4. Resolve conflicts before merging
5. If a worker fails, retry once then handle manually
```

## Links

- MCP specification: https://modelcontextprotocol.io
- MCP server registry: https://github.com/modelcontextprotocol/servers
- Codex CLI: https://github.com/openai/codex

# Self-Improvement Pipeline

The EA logs every correction and preference into `lessons-queue.jsonl`. Over time, patterns emerge. The engine detects them and suggests rules.

## How It Works

1. **Capture** — When Wes corrects output or states a preference, the EA appends a lesson to `lessons-queue.jsonl`
2. **Detect** — Run `engine.py` to find patterns (tags appearing 3+ times)
3. **Promote** — Copy suggested rules into CLAUDE.md's Learned Rules section

## Lesson Format

Each line in `lessons-queue.jsonl` is a JSON object:

```json
{
  "id": 1,
  "timestamp": "2026-03-08T14:30:00Z",
  "source": "human-feedback",
  "lesson": "Don't use bullet points in outbound emails",
  "context": "Was drafting cold outreach",
  "severity": "medium",
  "status": "pending",
  "tags": ["style", "email"]
}
```

**Fields:**
- `id` — Sequential integer
- `timestamp` — ISO 8601
- `source` — `human-feedback`, `self-detected`, or `pattern-match`
- `lesson` — What was learned
- `context` — What triggered it
- `severity` — `low`, `medium`, or `high`
- `status` — `pending`, `promoted`, or `dismissed`
- `tags` — Array of category strings for grouping

## Running the Engine

```bash
# Show digest — patterns, tag frequency, suggested rules
python self-improver/engine.py

# Promote pattern lessons (marks them as 'promoted' in the queue)
python self-improver/engine.py --promote
```

## For OIOS Clients

When OIOS handles workflows for a client, corrections from the client's team get logged the same way. The system genuinely learns — "Your AI gets smarter the more you use it" isn't marketing, it's this pipeline.

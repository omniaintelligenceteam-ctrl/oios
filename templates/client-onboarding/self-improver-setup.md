# Self-Improvement Pipeline Setup

## What This Does

Every time the client's team corrects the AI — wrong tone, missed detail, bad assumption — the correction gets logged. Over time, patterns emerge. The AI stops making the same mistakes.

This is the "Your AI gets smarter the more you use it" promise, and it actually works.

## Setup Steps

1. Create a `self-improver/` directory in the client's project folder
2. Create an empty `lessons-queue.jsonl` file
3. Add logging instructions to the client's AI configuration (same format as Wes's EA)
4. Run `engine.py` weekly during the first month to check for patterns
5. Promote suggested rules into the client's learned rules

## Lesson Format

```json
{"id": 1, "timestamp": "2026-03-08T14:30:00Z", "source": "human-feedback", "lesson": "Always include job number in follow-up emails", "context": "Client corrected missing job number", "severity": "medium", "status": "pending", "tags": ["email", "followup"]}
```

## Selling This to the Client

- "Most AI tools are static — they're the same on day 90 as day 1. OIOS learns."
- "Every correction your team makes teaches the system. After a month, it knows your business."
- "We run a pattern report weekly. If the AI keeps making the same mistake, we fix it permanently."

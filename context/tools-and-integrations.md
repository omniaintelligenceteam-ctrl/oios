# Tools & Integrations

## Active Tools

### Claude Code
- Primary AI coding and EA environment
- This is where you live

### OpenClaw
- Wes's primary workflow tool alongside Claude Code
- Used for building and demonstrating AI workflows to clients
- Central to the Silent AI Partner product offering

---

## Skills APIs (set up when using these skills)

### Kia API / Nano Banana 2K
- Used by: `infographic-generator` skill
- Env var: `KIA_API_KEY`
- Also needs: `IMAGEBB_API_KEY` for logo hosting (imgbb.com)

### YouTube Data API v3
- Used by: `lead-magnet-creator`, `rag-database-builder` skills
- Env var: `YOUTUBE_API_KEY`
- Setup: console.cloud.google.com → Create Project → Enable YouTube Data API v3 → Credentials → API Key

### Notion API
- Used by: `lead-magnet-creator` skill
- Env vars: `NOTION_API_KEY`, `NOTION_PAGE_ID`
- Setup: notion.so/my-integrations → New Integration → copy token

### Pinecone
- Used by: `rag-database-builder` skill
- Env var: `PINECONE_API_KEY`
- Index: `omnia-rag`, model: `multilingual-e5-large`
- Setup: app.pinecone.io → free tier available

### OpenRouter
- Used by: `rag-database-builder` skill (chat interface)
- Env var: `OPENROUTER_API_KEY`
- Allows switching models dynamically without changing code

---

## Not Yet Configured (Worth Exploring)

- MCP servers — none set up yet
- CRM — no tool selected
- Email integration — not connected
- Calendar integration — not connected

---

## How to Use This File

When a new tool is added or integrated, document it here:

```
### [Tool Name]
- What it does
- How Wes uses it
- Any relevant credentials/config location (no passwords here)
- Gotchas or notes
```

---
name: rag-database-builder
description: Use when Wes wants to build a searchable knowledge base from a YouTube channel, website, or content source, or wants to query a knowledge base that's already been built. Triggers on "build a RAG", "scrape this channel into a database", "create a knowledge base from", or "ask questions about [person/channel]".
disable-model-invocation: false
---

# RAG Database Builder

Scrape a YouTube channel → vectorize the content → store in Pinecone → launch a queryable chatbot.

## Required Environment Variables

```
YOUTUBE_API_KEY=your_key_here      # From console.cloud.google.com → YouTube Data API v3
PINECONE_API_KEY=your_key_here     # From app.pinecone.io
OPENROUTER_API_KEY=your_key_here   # From openrouter.ai — for the chat interface
```

Add to `CLAUDE.local.md` under `## API Keys`. Never commit.

## Pinecone Setup (first time only)

1. Go to app.pinecone.io → Create Index
2. Index name: `omnia-rag`
3. Embedding model: **multilingual-e5-large** (best for semantic search — don't use the default small model)
4. Dimensions: 1024
5. Metric: cosine

> The model choice matters. multilingual-e5-large dramatically improves retrieval quality.

## Process

### Step 1: Get the source
User provides a YouTube channel URL, handle (@channel), or video list.

Ask if not provided: "Which channel or content source? And how many videos — last 10, or more?"

### Step 2: Scrape the channel

```bash
# Get channel's recent videos via YouTube Data API
curl "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=CHANNEL_ID&maxResults=10&order=date&type=video&key=$YOUTUBE_API_KEY"
```

For each video, extract transcript using captions API or yt-dlp fallback (same as lead-magnet-creator skill).

### Step 3: Chunk the content

Split each transcript into ~500 token chunks with 50 token overlap. Each chunk gets metadata:
```json
{
  "video_id": "abc123",
  "title": "Video Title",
  "url": "https://youtube.com/watch?v=abc123",
  "chunk_index": 0,
  "text": "chunk content here"
}
```

### Step 4: Vectorize and upsert to Pinecone

```python
# Pseudocode — Claude will implement using pinecone-client
from pinecone import Pinecone

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("omnia-rag")

# Generate embeddings using multilingual-e5-large
# Upsert vectors with metadata
index.upsert(vectors=[
    {"id": "video_id-chunk_0", "values": [embedding], "metadata": {...}}
])
```

> Upsert = update + insert. Running this again on the same channel refreshes stale content without duplicating.

### Step 5: Build the chat interface

Launch a simple query loop:

```python
# User asks a question
query = "What tips do you have for X?"

# Embed the query
query_embedding = embed(query)

# Semantic search in Pinecone
results = index.query(vector=query_embedding, top_k=5, include_metadata=True)

# Pass results + query to OpenRouter for synthesis
response = openrouter.chat(
    model="anthropic/claude-sonnet-4-6",
    messages=[
        {"role": "system", "content": "You are an AI assistant with access to [channel name]'s content. Answer based on the retrieved context."},
        {"role": "user", "content": f"Context:\n{results}\n\nQuestion: {query}"}
    ]
)
```

### Step 6: Confirm and document

- Confirm how many videos were scraped and vectors stored
- Show a test query to verify retrieval works
- Ask: "Want to set this up to refresh daily? Or query it now?"
- Log the channel/source to `references/rag-sources.md`

## Daily Refresh

To keep the database current, re-run Steps 2-4 on a schedule. Upsert handles duplicates automatically — only new content gets added.

## Notes

- This same pattern works for any content source: website (use Firecrawl), podcast (use transcript), docs
- Start with 10 videos. Scale up once the setup is confirmed working.
- Save the channel details and index name to `references/rag-sources.md` so we know what's in the database
- The chatbot can reference video URLs in its answers — make sure metadata includes the URL

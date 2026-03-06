---
name: lead-magnet-creator
description: Use when Wes provides a YouTube URL and wants it turned into a lead magnet, guide, or repurposed content asset. Triggers on "turn this into a lead magnet", "repurpose this video", "make a guide from this YouTube", or pasting a YouTube URL with intent to create content.
disable-model-invocation: false
---

# Lead Magnet Creator

Turn any YouTube video into a structured, valuable lead magnet — saved locally and pushed to Notion.

## Required Environment Variables

```
YOUTUBE_API_KEY=your_key_here    # From console.cloud.google.com → YouTube Data API v3
NOTION_API_KEY=your_key_here     # From notion.so/my-integrations
NOTION_PAGE_ID=your_page_id      # The Notion page where lead magnets get created
```

Add to `CLAUDE.local.md` under `## API Keys`. Never commit.

## Process

### Step 1: Get the YouTube URL
User provides a URL. If not given, ask: "Which YouTube video?"

### Step 2: Scrape the transcript

```bash
# Using YouTube Data API v3 to get captions
curl "https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=VIDEO_ID&key=$YOUTUBE_API_KEY"
```

Extract the video ID from the URL, fetch available caption tracks, download the transcript.

> If captions aren't available via API, use `yt-dlp --write-auto-subs` as fallback:
> `yt-dlp --write-auto-subs --skip-download --sub-format vtt -o "%(title)s" [URL]`

### Step 3: Structure the lead magnet

**Format:**
```
# [Title — action-oriented, specific]

## The Big Idea
[One paragraph. What's the core thing this teaches?]

## Why This Matters
[One paragraph. What problem does this solve?]

## [Section 1 Title]
[Key insight + 2-3 action steps]

## [Section 2 Title]
...

## [Section 3-5 as needed]

## Quick Win You Can Do Today
[One concrete action the reader can take immediately]

## Resources & Next Steps
[Links, tools, or follow-up content mentioned]
```

**Voice rules:**
- Wes's tone: casual, direct, confident
- No hyphens as bullet points (use dashes only for ranges, not lists)
- No "excited to share" or cringe openers
- Make it feel like a friend wrote it, not a content machine
- Valuable over long — cut anything that doesn't earn its place

### Step 4: Save locally

```
references/lead-magnets/YYYY-MM-DD-[slug-title].md
```

### Step 5: Push to Notion

```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent": { "page_id": "'$NOTION_PAGE_ID'" },
    "properties": {
      "title": [{ "text": { "content": "[Lead Magnet Title]" } }]
    },
    "children": [
      [formatted blocks — headings, paragraphs, callouts]
    ]
  }'
```

Use Notion block types: `heading_1`, `heading_2`, `paragraph`, `callout`, `bulleted_list_item`.
No plain walls of text — use callout blocks for key insights, bullets for action steps.

### Step 6: Confirm delivery

- Show local file path
- Show Notion page link
- Ask: "Want a cover image generated for this? (uses infographic-generator skill)"

## Notes

- This can repurpose anything — swap YouTube for podcast transcript, blog post, email thread
- Save the lead magnet structure as a template if a new format works well
- If transcript quality is poor (auto-captions), note it and ask Wes to verify key points

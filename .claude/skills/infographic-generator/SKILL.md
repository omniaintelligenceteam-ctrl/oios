---
name: infographic-generator
description: Use when Wes wants to turn text, bullet points, or a brain dump into a branded visual infographic. Triggers on requests like "make an infographic", "visualize this", "create a graphic for", or when pasting content that needs to be illustrated.
disable-model-invocation: false
---

# Infographic Generator

Generate branded infographics from any text input using the Kia API (Nano Banana 2K model).

## Required Environment Variables

```
KIA_API_KEY=your_key_here         # From kia.ai or wherever you got access
IMAGEBB_API_KEY=your_key_here     # From imgbb.com — needed to host logo for API
```

Add these to `CLAUDE.local.md` under a `## API Keys` section (never commit them).

## Brand Defaults

> Fill these in once, then every infographic uses your brand automatically.

```
BRAND_COLORS = ["#REPLACE_PRIMARY", "#REPLACE_SECONDARY", "#REPLACE_ACCENT"]
BRAND_FONT = "REPLACE_WITH_YOUR_FONT"
LOGO_URL = "REPLACE_WITH_HOSTED_LOGO_URL"  # Upload to imgbb.com, paste URL here
```

## Process

### Step 1: Get the input
Accept any of:
- Raw text or bullet points
- A brain dump or rough notes
- A topic + key points to illustrate
- A document section to visualize

Ask if not provided: "What's the content, and what's the purpose of this graphic?"

### Step 2: Build the image prompt

Structure the prompt for Nano Banana 2K:
```
Style: [brand colors], [brand font], clean modern infographic, 16:9 ratio
Layout: [diagram / flowchart / comparison / timeline / list — pick best fit]
Content: [structured version of the input]
Logo: [logo URL if provided]
Quality: 2K resolution
Tone: professional but approachable, easy to follow
```

### Step 3: Call the Kia API

```bash
curl -X POST https://api.kia.ai/v1/generate \
  -H "Authorization: Bearer $KIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nanobana-2k",
    "prompt": "[your prompt here]",
    "width": 1920,
    "height": 1080,
    "quality": "high"
  }'
```

> If the endpoint or model name differs from your account, check kia.ai/docs and update this skill.

### Step 4: Batch mode (optional)

If Wes wants multiple variations, fire off 5 calls with slightly different layout/style prompts and return all 5 image URLs.

Ask: "Want one version or 5 variations to pick from?"

### Step 5: Deliver

- Show the image URL(s)
- Ask: "Want me to adjust the style, layout, or content?"
- Offer to save the prompt to `references/examples/infographic-prompts.md` if it worked well

## Notes

- Always ask about purpose before generating — a "summary infographic" looks different from a "comparison chart"
- If no logo URL is set, generate without it and note the gap
- Save winning prompts to `references/examples/` so future graphics stay consistent

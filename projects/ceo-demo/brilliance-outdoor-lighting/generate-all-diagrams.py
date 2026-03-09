import requests
import base64
import json
import sys
import os

API_KEY = "AIzaSyBL0sFJJx669deo_Aa0pDKdJbTbzQrqofQ"
MODEL = "gemini-3-pro-image-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

DIAGRAMS = [
    {
        "filename": "ai-proposals-diagram.png",
        "prompt": """Create a professional, clean infographic diagram showing an "AI Proposal Generator" system for a landscape lighting company. Dark background (#1A1A2E), modern style, 16:9 landscape ratio.

The diagram should show this flow from left to right:

1. LEFT SIDE - "Consultation Notes" - Show a clipboard/notepad icon with messy handwritten notes, voice memo icon
2. MIDDLE - "AI Proposal Engine" - Show a document/gear icon processing the notes, with these steps:
   - Extracts scope, measurements, fixture counts
   - Calculates pricing from rate card
   - Applies brand template
   - Adds photos and renders
3. RIGHT SIDE - "Professional Proposal" - Show a polished PDF document with:
   - Branded header with company logo
   - Itemized pricing table
   - Project timeline
   - Terms and signature line

Title: "AI Proposals — 2 Hours to 2 Minutes"
Subtitle: "From messy consultation notes to a branded PDF proposal, automatically."

Key stat callout: "90% faster — from 2 hours per proposal down to 2 minutes"

Style: flat design, tech company aesthetic, clean vector/illustration style. Colors: dark navy background, red accent (#E94560), teal (#0F3460), gold (#F5C518). Do NOT include any watermarks."""
    },
    {
        "filename": "ai-followups-diagram.png",
        "prompt": """Create a professional, clean infographic diagram showing an "AI Follow-Up System" for a landscape lighting company. Dark background (#1A1A2E), modern style, 16:9 landscape ratio.

The diagram should show a TIMELINE flowing left to right with 3 stages:

1. STAGE 1 (Day 1) - "Thank You + Proposal"
   - Email icon with checkmark
   - "Sent automatically after consultation"
   - Green color (#2ECC71)

2. STAGE 2 (Day 3) - "Gentle Check-In"
   - Text message icon
   - "Hey Sarah, any questions about the proposal?"
   - Gold color (#F5C518)

3. STAGE 3 (Day 7) - "Value Add + Urgency"
   - Calendar icon with alert
   - "Spring schedule filling up — want to lock in your June deadline?"
   - Red accent (#E94560)

Below the timeline, show a "RESULTS" bar:
- "Before AI: 20% follow-up rate, deals go cold"
- "After AI: 100% follow-up rate, 3x more closes"

Title: "AI Follow-Ups — Never Let a Lead Go Cold"
Subtitle: "Automated 3-stage sequences that keep every deal moving."

Style: flat design, tech company aesthetic, clean vector/illustration style. Dark navy background. Do NOT include any watermarks."""
    },
    {
        "filename": "ai-crew-scheduling-diagram.png",
        "prompt": """Create a professional, clean infographic diagram showing an "AI Crew Scheduling" system for a landscape lighting company. Dark background (#1A1A2E), modern style, 16:9 landscape ratio.

The diagram should show:

1. LEFT SIDE - "Inputs" - Three input sources feeding into the system:
   - Confirmed jobs (calendar icon)
   - Crew availability (people icons)
   - Materials inventory (box/warehouse icon)

2. CENTER - "AI Scheduler" - A central processing hub that:
   - Optimizes routes between job sites
   - Matches crew skills to job requirements
   - Checks materials needed vs. in stock
   - Avoids double-bookings

3. RIGHT SIDE - "Output: Weekly Schedule" - A clean weekly calendar/grid showing:
   - Team A: Monday 8am - Henderson (Frisco), Tuesday 8am - Martinez (Plano)
   - Team B: Monday 8am - Commercial HOA (Southlake)
   - Materials list auto-generated per job

Title: "AI Crew Scheduling — No More Whiteboard Chaos"
Subtitle: "From sticky notes and group texts to optimized daily schedules."

Key stat: "Before: whiteboard + group text, double-bookings monthly. After: zero conflicts, crews know exactly where to go."

Style: flat design, tech company aesthetic, clean vector/illustration style. Colors: dark navy, teal (#0F3460), green (#2ECC71), gold (#F5C518). Do NOT include any watermarks."""
    },
    {
        "filename": "ai-reviews-referrals-diagram.png",
        "prompt": """Create a professional, clean infographic diagram showing an "AI Reviews & Referrals" system for a landscape lighting company. Dark background (#1A1A2E), modern style, 16:9 landscape ratio.

The diagram should show a FLOW starting from job completion:

1. TOP - "Job Completed" - Show a house with landscape lighting glowing, checkmark

2. MIDDLE - Three automated actions triggered in sequence:
   - Day 1: "Thank You Text" - Heart icon - "Thanks for choosing Brilliance! We loved working on your property."
   - Day 3: "Review Request" - 5 stars icon - "Would you mind leaving us a quick Google review? Here's the link: [link]"
   - Day 7: "Referral Ask" - People/share icon - "Know anyone who'd love lighting like yours? We'll give you both $200 off."

3. BOTTOM - "Results Dashboard" showing:
   - Google rating: 4.9 stars (127 reviews)
   - 23 referrals this quarter
   - $46K revenue from referrals alone

Title: "AI Reviews & Referrals — Turn Every Job Into 3 More"
Subtitle: "Automated post-install sequences that build your reputation and pipeline."

Style: flat design, tech company aesthetic, clean vector/illustration style. Colors: dark navy, green (#2ECC71), gold (#F5C518), red accent (#E94560). Do NOT include any watermarks."""
    },
    {
        "filename": "ai-weekly-reports-diagram.png",
        "prompt": """Create a professional, clean infographic diagram showing an "AI Weekly Report" for a landscape lighting company. Dark background (#1A1A2E), modern style, 16:9 landscape ratio.

The diagram should show a DASHBOARD layout — like a CEO would see on Monday morning:

1. TOP ROW - Three big KPI cards:
   - "Revenue This Week: $47,200" (green, up arrow, +12%)
   - "Active Leads: 23" (gold, with pipeline breakdown)
   - "Crew Utilization: 87%" (teal, with bar chart)

2. MIDDLE ROW - Two sections side by side:
   - LEFT: "Wins This Week" - 3 bullet items (Henderson job closed $7,200, 5 new Google reviews, 2 referral leads came in)
   - RIGHT: "Watch List" - 3 items needing attention (Martinez proposal overdue 3 days, Team B truck needs service, 2 leads going cold)

3. BOTTOM - "AI Recommendation" bar:
   - "Priority this week: Close the Martinez deal ($12K) and follow up on the 2 cold leads. Estimated recovery: $18K."

Title: "AI Weekly Report — Your Monday Morning Briefing"
Subtitle: "Pipeline, revenue, crew status, and priorities — generated automatically."

Style: flat design, dashboard aesthetic, clean vector/illustration style. Colors: dark navy background, green (#2ECC71) for positive, red (#E94560) for alerts, gold (#F5C518) for metrics, teal (#0F3460) for charts. Do NOT include any watermarks."""
    }
]

for i, diagram in enumerate(DIAGRAMS):
    print(f"\n[{i+1}/{len(DIAGRAMS)}] Generating {diagram['filename']}...")

    payload = {
        "contents": [{"parts": [{"text": diagram["prompt"]}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }

    try:
        resp = requests.post(URL, json=payload, timeout=180)

        if resp.status_code != 200:
            print(f"  ERROR: HTTP {resp.status_code}")
            print(f"  {resp.text[:200]}")
            continue

        data = resp.json()
        if "candidates" not in data:
            print(f"  ERROR: No candidates")
            continue

        parts = data["candidates"][0]["content"]["parts"]
        image_saved = False

        for part in parts:
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                out_path = os.path.join(OUT_DIR, diagram["filename"])
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  Saved: {diagram['filename']} ({len(img_bytes)/1024:.1f} KB)")
                image_saved = True

        if not image_saved:
            print(f"  WARNING: No image in response")

    except Exception as e:
        print(f"  ERROR: {e}")

print("\nDone! All diagrams generated.")

import requests
import base64
import os
import sys

API_KEY = "AIzaSyBL0sFJJx669deo_Aa0pDKdJbTbzQrqofQ"
MODEL = "gemini-3-pro-image-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT_DIR, exist_ok=True)

BRAND = """
Style rules for ALL images:
- Dark navy background (#0A0A14 to #1A1A2E gradient)
- Brand colors: red (#E94560), teal/blue (#0F3460), gold (#F5C518), green (#2ECC71)
- Clean, modern, flat design with subtle glassmorphism effects
- Professional tech company aesthetic
- 16:9 landscape ratio (1920x1080 feel)
- Do NOT include any watermarks, logos, or text that says "AI generated"
- Minimal text — let the visual design speak
- Subtle glow effects and gradients
"""

IMAGES = [
    {
        "filename": "hero-problem.png",
        "prompt": f"""Create a cinematic, dark-themed hero illustration representing "a business leaking money." {BRAND}

Visual concept: A stylized, abstract visualization of a business hemorrhaging revenue.

Show:
- Center: An abstract building/business icon made of geometric shapes, glowing faintly in teal (#0F3460)
- From the building, streams of gold/amber particles (#F5C518) are flowing outward and dissipating — representing money leaking away
- Below: Abstract phone icons with red X marks — representing missed calls
- Scattered document icons fading out — representing forgotten follow-ups and lost proposals
- The overall mood is dramatic and urgent — like watching opportunity slip away
- Subtle grid/matrix pattern in the background for a tech feel
- A faint red glow (#E94560) around the edges creating urgency

This should feel like a high-end SaaS landing page hero image. Cinematic, moody, impactful. No people, no stock photo feel. Pure abstract tech visualization."""
    },
    {
        "filename": "pillar-receptionist.png",
        "prompt": f"""Create a sleek, futuristic illustration representing an "AI Receptionist" that never misses a call. {BRAND}

Visual concept: A phone call being answered and processed by intelligent AI.

Show:
- Center: A glowing phone icon surrounded by a circular AI interface — like a HUD display
- Sound waves emanating from the phone, being captured and processed
- Connected nodes showing data being extracted: caller name, phone number, service needed, urgency level
- Each data point is a small glassmorphism card connected by glowing lines
- A green checkmark pulse effect — call answered successfully
- On one side: "24/7" text subtly glowing
- Background: dark with subtle circuit-board patterns and floating particles
- The phone should feel alive — pulsing with energy, not static
- Color emphasis: red (#E94560) for the phone glow, green (#2ECC71) for success indicators
- Small badge showing "< 1 sec" response time

Futuristic, premium, like a command interface from a sci-fi movie. Clean lines, no clutter."""
    },
    {
        "filename": "pillar-backoffice.png",
        "prompt": f"""Create a sleek illustration representing "AI Back Office Automation" — killing paperwork. {BRAND}

Visual concept: Documents, proposals, and follow-ups being processed automatically.

Show:
- Left side: A stack of messy, overlapping paper documents and sticky notes — glowing faintly red to indicate the problem
- Center: A processing beam/portal effect — papers going in messy, coming out organized
- Right side: Clean, organized digital documents — a proposal template, a follow-up timeline, a schedule — all glowing green
- Timeline bar at the bottom showing: Day 1 → Day 3 → Day 7 → Day 14 (follow-up sequence)
- Small stat callouts: "30 sec" for proposal generation, "100%" for follow-up rate
- Floating icons: calendar, checkmark, document, clock — connected by golden (#F5C518) lines
- The transformation from chaos to order should be the visual story
- Color emphasis: gold (#F5C518) as primary accent, red for the problem side, green for the solution side

Premium tech aesthetic. The visual should communicate "automation" and "efficiency" without being generic."""
    },
    {
        "filename": "pillar-command-center.png",
        "prompt": f"""Create a stunning illustration of an "AI Command Center Dashboard" — complete business visibility. {BRAND}

Visual concept: A real-time business intelligence dashboard floating in space.

Show:
- A large holographic-style dashboard floating at a slight angle, like a futuristic control center
- Three main KPI cards across the top: Revenue ($127,400 in green), Active Leads (23 in gold), Close Rate (34% in teal)
- Below: A pipeline visualization showing deals flowing through stages
- A chat/message interface showing a natural language query: "How's my pipeline?"
- Small notification badges showing proactive alerts
- Morning briefing icon with a clock showing 6:30 AM
- The dashboard should have a glassmorphism aesthetic — frosted glass panels with subtle transparency
- Ambient glow from the dashboard illuminating the dark space around it
- Data visualization elements: mini charts, progress bars, trend arrows
- Color emphasis: green (#2ECC71) as primary, with gold and teal accents

This should look like something from Iron Man's JARVIS or a Bloomberg terminal redesigned by a top design agency. Impressive, data-rich but not cluttered."""
    },
    {
        "filename": "full-loop-flow.png",
        "prompt": f"""Create a horizontal flow diagram showing the complete OIOS customer journey — "From Ring to Revenue." {BRAND}

Visual concept: Six connected stages flowing left to right, showing how OIOS handles a lead from first call to closed deal.

Show these 6 stages as connected nodes/cards:
1. PHONE ICON (red glow) — "Call Comes In" — phone ringing with incoming wave
2. PERSON ICON (red glow) — "Lead Captured" — contact card being created
3. DOCUMENT ICON (gold glow) — "Proposal Drafted" — professional document generated
4. CHECKMARK ICON (green glow) — "You Approve" — thumbs up / approval button
5. ARROWS ICON (gold glow) — "Follow-Ups Run" — automated message sequence
6. DOLLAR ICON (green glow) — "Deal Closes" — money/success celebration

Connect them with flowing, glowing lines — like an energy pulse traveling through the pipeline.
Each node should be a glassmorphism card with an icon inside.
Below the flow, a subtle text: "You just text. OIOS handles the rest."
The pulse of energy should be moving from left to right, creating a sense of momentum and inevitability.

Premium, animated-feeling (even though it's static). Each stage should feel like it belongs in a high-end product demo."""
    },
    {
        "filename": "roi-impact.png",
        "prompt": f"""Create a striking data visualization showing the ROI impact of OIOS — the before/after transformation. {BRAND}

Visual concept: A dramatic split-screen comparison showing business metrics before and after OIOS.

LEFT SIDE (dark, red-tinted — "Before"):
- Call answer rate: 60% (shown as a circular gauge, mostly empty, red)
- Admin hours: 20 hrs/week (large, heavy number)
- Follow-up rate: 50% (half-filled bar)
- Mood: stressful, chaotic, losses

RIGHT SIDE (bright, green-tinted — "After"):
- Call answer rate: 98% (circular gauge, nearly full, green)
- Admin hours: 3 hrs/week (small, light number)
- Follow-up rate: 100% (completely filled bar)
- Mood: controlled, efficient, gains

CENTER DIVIDER: A glowing vertical line or transformation effect where red becomes green

Bottom section: A large ROI number "650%" glowing in green, with a visual contrast of "Monthly Cost" (small) vs "Revenue Recovered" (large)

The contrast should be dramatic — the "before" side should feel heavy and alarming, the "after" side should feel light and successful. Like a medical before/after but for a business.

Make it feel like real data, not clipart. Dashboard-quality visualization."""
    }
]

if len(sys.argv) > 1:
    indices = [int(x) for x in sys.argv[1:]]
    IMAGES = [IMAGES[i] for i in indices if i < len(IMAGES)]

for i, img in enumerate(IMAGES):
    print(f"\n[{i+1}/{len(IMAGES)}] Generating {img['filename']}...")

    payload = {
        "contents": [{"parts": [{"text": img["prompt"]}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }

    try:
        resp = requests.post(URL, json=payload, timeout=180)

        if resp.status_code != 200:
            print(f"  ERROR: HTTP {resp.status_code}")
            print(f"  {resp.text[:300]}")
            continue

        data = resp.json()
        if "candidates" not in data:
            print(f"  ERROR: No candidates in response")
            if "error" in data:
                print(f"  {data['error'].get('message', '')[:200]}")
            continue

        parts = data["candidates"][0]["content"]["parts"]
        image_saved = False

        for part in parts:
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                out_path = os.path.join(OUT_DIR, img["filename"])
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  Saved: {img['filename']} ({len(img_bytes)/1024:.1f} KB)")
                image_saved = True
            elif "text" in part:
                print(f"  Text response: {part['text'][:100]}")

        if not image_saved:
            print(f"  WARNING: No image data in response")

    except requests.exceptions.Timeout:
        print(f"  ERROR: Request timed out (180s)")
    except Exception as e:
        print(f"  ERROR: {e}")

print(f"\nDone! Images saved to: {OUT_DIR}")

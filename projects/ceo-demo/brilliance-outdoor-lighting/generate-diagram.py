import requests
import base64
import json
import sys
import os

API_KEY = "AIzaSyBL0sFJJx669deo_Aa0pDKdJbTbzQrqofQ"
MODEL = "gemini-3-pro-image-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

PROMPT = """Create a professional, clean infographic diagram showing an "AI Receptionist" system for a landscape lighting company. Dark background (#1A1A2E), modern style.

The diagram should show this flow from left to right:

1. LEFT SIDE - "Customer Calls" - Show a phone icon with incoming call waves
2. MIDDLE - "AI Receptionist" - Show a brain/AI icon processing the call, with these outputs branching out:
   - Transcribes the call in real-time
   - Extracts: customer name, phone, address, job scope, budget, timeline
   - Scores the lead (A/B/C grade)
   - Detects buying signals and sentiment
3. RIGHT SIDE - "Automatic Actions" - Show 4 action boxes:
   - Confirmation text sent to customer (2 min)
   - Alert sent to owner via Slack (1 min)
   - Lead logged to CRM with full profile
   - Follow-up reminders scheduled

Use colors: dark navy background, red accent (#E94560), teal (#0F3460), gold (#F5C518), green (#2ECC71) for positive actions.
Make it look like a premium SaaS product diagram. Clean lines, rounded corners on boxes, subtle gradients.
Title at top: "AI Receptionist — Never Miss a Lead Again"
Subtitle: "Every call captured. Every lead scored. Every follow-up automatic."

Style: flat design, tech company aesthetic, 16:9 landscape ratio, no photorealism — clean vector/illustration style.
Do NOT include any watermarks or AI model names."""

payload = {
    "contents": [{
        "parts": [{"text": PROMPT}]
    }],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"]
    }
}

print("Generating AI Receptionist diagram...")
print(f"Using model: {MODEL}")

try:
    resp = requests.post(URL, json=payload, timeout=120)

    if resp.status_code != 200:
        print(f"Error: HTTP {resp.status_code}")
        print(resp.text[:500])
        sys.exit(1)

    data = resp.json()

    if "candidates" not in data:
        print("Error: No candidates in response")
        print(json.dumps(data, indent=2)[:500])
        sys.exit(1)

    parts = data["candidates"][0]["content"]["parts"]

    image_saved = False
    for part in parts:
        if "text" in part:
            print(f"Model response: {part['text'][:200]}")
        elif "inlineData" in part:
            img_bytes = base64.b64decode(part["inlineData"]["data"])
            out_dir = os.path.dirname(os.path.abspath(__file__))
            out_path = os.path.join(out_dir, "ai-receptionist-diagram.png")
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            print(f"Image saved to: {out_path}")
            print(f"File size: {len(img_bytes) / 1024:.1f} KB")
            image_saved = True

    if not image_saved:
        print("Warning: No image data found in response")
        print(json.dumps(data, indent=2)[:1000])

except requests.exceptions.Timeout:
    print("Error: Request timed out after 120 seconds")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

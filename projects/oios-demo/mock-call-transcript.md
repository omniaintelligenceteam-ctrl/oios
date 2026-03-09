# Mock Phone Call — AI Receptionist vs. Manual

## Scenario: Customer calls a service business after hours

**Time:** 7:42 PM (after business hours)
**Caller:** Mike Torres (business owner looking for commercial HVAC service)
**Receiver:** OIOS AI Receptionist

---

## WITHOUT OIOS

*Ring... ring... ring...*

**Voicemail:** "You've reached ABC Services. Our office hours are 8 AM to 5 PM. Please leave a message and we'll get back to you."

*Mike hangs up. Calls the next company on Google.*

**Result:** Lead lost. $12,000 job gone.

---

## WITH OIOS

**AI:** Thanks for calling ABC Services. This is Alex, how can I help you tonight?

**Mike:** Hey, yeah — I've got a commercial property on 5th Street and our HVAC system went down today. We need someone out here to take a look. It's a restaurant so we can't have it down long.

**AI:** I understand — a restaurant without HVAC is an emergency. Let me get some details so we can get someone to you as fast as possible. What's the address of the property?

**Mike:** 847 East 5th Street, Suite 200.

**AI:** Got it. And is this a rooftop unit, split system, or do you know the make and model?

**Mike:** It's a rooftop Carrier unit. I think it's about 5 tons. It's blowing warm air — won't cool below 78 degrees.

**AI:** That sounds like it could be a compressor or refrigerant issue. We can definitely take a look. I have openings tomorrow morning — would 8 AM work, or do you need emergency service tonight?

**Mike:** Tomorrow at 8 is fine. It's not life or death, just need it fixed before the lunch rush.

**AI:** I've got you down for 8 AM tomorrow at 847 East 5th Street. Our tech will call you 30 minutes before arrival. What's the best number to reach you?

**Mike:** 512-555-3891.

**AI:** Perfect. You'll get a confirmation text in just a moment with all the details. Is there anything else I can help with?

**Mike:** No, that's great. Thanks.

**AI:** Have a good night, Mike. We'll see you tomorrow at 8.

---

**Duration:** 1 minute 52 seconds
**Result:** Lead captured, appointment booked, confirmation sent — all after hours, no human needed.

---

## What OIOS Extracted (Automatically)

| Field | Value |
|-------|-------|
| Customer | Mike Torres |
| Phone | 512-555-3891 |
| Property | 847 E 5th St, Suite 200 (commercial/restaurant) |
| Equipment | Carrier rooftop unit, ~5 ton |
| Issue | Blowing warm air, won't cool below 78°F |
| Urgency | High — restaurant, needs fix before lunch rush |
| Appointment | Tomorrow 8:00 AM |
| Estimated Job Value | $800 - $2,500 (commercial HVAC service call) |
| Lead Score | 88/100 — Grade: A |

## Auto-Actions Triggered

1. **+30 sec** — Confirmation text to Mike with appointment details
2. **+1 min** — Alert to on-call tech: "Commercial emergency lead, 8 AM tomorrow"
3. **+1 min** — CRM entry created with full profile
4. **+1 min** — Calendar event created, 30-min pre-arrival call reminder set
5. **Watchdog** — If no service report filed by 2 PM tomorrow, alert owner

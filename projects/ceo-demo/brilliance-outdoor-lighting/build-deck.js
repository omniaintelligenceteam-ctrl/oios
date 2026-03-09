const pptxgen = require("pptxgenjs");
const pres = new pptxgen();

// ── Theme ──
const DARK = "1A1A2E";
const NAVY = "16213E";
const TEAL = "0F3460";
const ACCENT = "E94560";
const WHITE = "FFFFFF";
const LIGHT = "E8E8E8";
const MUTED = "A0A0B0";
const GOLD = "F5C518";
const GREEN = "2ECC71";
const BG_CARD = "222244";

pres.layout = "LAYOUT_WIDE";
pres.author = "Omnia Intelligence AI";
pres.title = "Voice AI Agent — Landscape Lighting Demo";

// ═══════════════════════════════════════════════════════════
// SLIDE 1 — THE PROBLEM
// ═══════════════════════════════════════════════════════════
let slide1 = pres.addSlide();
slide1.background = { color: DARK };

// Accent bar at top
slide1.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: "100%", h: 0.06, fill: { color: ACCENT },
});

slide1.addText("Every Missed Call Is a Lost Job.", {
  x: 0.8, y: 0.8, w: 8, h: 1.2,
  fontSize: 40, fontFace: "Calibri", bold: true,
  color: WHITE,
});

slide1.addText(
  "Your office manager answers 60% of calls.\nThe other 40%? Gone.",
  {
    x: 0.8, y: 2.0, w: 8, h: 0.9,
    fontSize: 20, fontFace: "Calibri",
    color: MUTED, lineSpacingMultiple: 1.4,
  }
);

// Stat cards — three across
const stats = [
  { num: "8-12", label: "Missed calls\nper day", color: ACCENT },
  { num: "$5K", label: "Average job\nvalue", color: GOLD },
  { num: "$60K+", label: "Lost revenue\nper month", color: ACCENT },
];

stats.forEach((s, i) => {
  let xPos = 0.8 + i * 3.6;
  // Card background
  slide1.addShape(pres.ShapeType.rect, {
    x: xPos, y: 3.4, w: 3.2, h: 2.0,
    fill: { color: BG_CARD },
    rectRadius: 0.15,
  });
  // Big number
  slide1.addText(s.num, {
    x: xPos, y: 3.5, w: 3.2, h: 1.0,
    fontSize: 48, fontFace: "Calibri", bold: true,
    color: s.color, align: "center",
  });
  // Label
  slide1.addText(s.label, {
    x: xPos, y: 4.4, w: 3.2, h: 0.8,
    fontSize: 14, fontFace: "Calibri",
    color: MUTED, align: "center", lineSpacingMultiple: 1.3,
  });
});

// Footer
slide1.addText("Source: ServiceTitan Industry Benchmarks, 2025", {
  x: 0.8, y: 6.8, w: 8, h: 0.4,
  fontSize: 10, fontFace: "Calibri", color: MUTED, italic: true,
});

// ═══════════════════════════════════════════════════════════
// SLIDE 2 — THE SOLUTION
// ═══════════════════════════════════════════════════════════
let slide2 = pres.addSlide();
slide2.background = { color: DARK };
slide2.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: "100%", h: 0.06, fill: { color: ACCENT },
});

slide2.addText("What If Every Call Was Captured?", {
  x: 0.8, y: 0.6, w: 10, h: 1.0,
  fontSize: 38, fontFace: "Calibri", bold: true, color: WHITE,
});

slide2.addText(
  "An AI that listens to every call — answered or recorded —\nand takes action automatically.",
  {
    x: 0.8, y: 1.5, w: 10, h: 0.8,
    fontSize: 18, fontFace: "Calibri", color: MUTED, lineSpacingMultiple: 1.4,
  }
);

// Flow diagram: 3 boxes with arrows
const flow = [
  { icon: "PHONE", title: "Customer Calls", desc: "Answered or voicemail", x: 0.6 },
  { icon: "AI", title: "AI Listens", desc: "Transcribes & extracts data", x: 4.3 },
  { icon: "ACTION", title: "Auto-Actions", desc: "Follow-up, CRM, alerts", x: 8.0 },
];

flow.forEach((f, i) => {
  // Box
  slide2.addShape(pres.ShapeType.rect, {
    x: f.x, y: 3.0, w: 3.4, h: 2.6,
    fill: { color: BG_CARD }, rectRadius: 0.15,
  });
  // Icon circle
  slide2.addShape(pres.ShapeType.ellipse, {
    x: f.x + 1.2, y: 3.2, w: 1.0, h: 1.0,
    fill: { color: TEAL },
  });
  // Icon text
  slide2.addText(f.icon === "PHONE" ? "\u260E" : f.icon === "AI" ? "\u2699" : "\u26A1", {
    x: f.x + 1.2, y: 3.25, w: 1.0, h: 1.0,
    fontSize: 28, fontFace: "Calibri", color: WHITE, align: "center", valign: "middle",
  });
  // Title
  slide2.addText(f.title, {
    x: f.x, y: 4.3, w: 3.4, h: 0.5,
    fontSize: 18, fontFace: "Calibri", bold: true, color: WHITE, align: "center",
  });
  // Desc
  slide2.addText(f.desc, {
    x: f.x, y: 4.8, w: 3.4, h: 0.5,
    fontSize: 13, fontFace: "Calibri", color: MUTED, align: "center",
  });

  // Arrow between boxes
  if (i < 2) {
    slide2.addText("\u27A4", {
      x: f.x + 3.4, y: 3.8, w: 0.9, h: 1.0,
      fontSize: 30, color: ACCENT, align: "center", valign: "middle",
    });
  }
});

// ═══════════════════════════════════════════════════════════
// SLIDE 3 — SAMPLE CALL TRANSCRIPT
// ═══════════════════════════════════════════════════════════
let slide3 = pres.addSlide();
slide3.background = { color: DARK };
slide3.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: "100%", h: 0.06, fill: { color: ACCENT },
});

slide3.addText("Real Call. Real Data.", {
  x: 0.8, y: 0.4, w: 8, h: 0.7,
  fontSize: 34, fontFace: "Calibri", bold: true, color: WHITE,
});

slide3.addText("A homeowner calls about patio + driveway lighting. Here's a snippet:", {
  x: 0.8, y: 1.0, w: 10, h: 0.5,
  fontSize: 15, fontFace: "Calibri", color: MUTED,
});

// Transcript card
slide3.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.6, w: 12.3, h: 4.8,
  fill: { color: BG_CARD }, rectRadius: 0.15,
});

const transcript = [
  { speaker: "Sarah", text: "We just finished building a patio and we're looking at getting lighting done. Our neighbors — the Thompsons — had y'all do their yard and it looks amazing.", color: GOLD },
  { speaker: "Lisa", text: "So you're looking at patio lighting mostly?", color: LIGHT },
  { speaker: "Sarah", text: "Patio for sure, and path lights down the driveway — it's really dark. And uplighting on three big live oaks in the front.", color: GOLD },
  { speaker: "Sarah", text: "We'd love to get it done before June — we're throwing a big backyard party for my daughter's graduation.", color: GOLD },
  { speaker: "Lisa", text: "Do you have a budget range in mind?", color: LIGHT },
  { speaker: "Sarah", text: "Somewhere in the five to eight thousand range?", color: GOLD },
];

let yPos = 1.8;
transcript.forEach((t) => {
  slide3.addText([
    { text: t.speaker + ":  ", options: { bold: true, color: t.color, fontSize: 13 } },
    { text: t.text, options: { color: LIGHT, fontSize: 13 } },
  ], {
    x: 0.9, y: yPos, w: 11.5, h: 0.65,
    fontFace: "Calibri", lineSpacingMultiple: 1.2,
  });
  yPos += 0.7;
});

// Tag
slide3.addText("1 min 47 sec  |  Inbound  |  Tuesday 10:23 AM", {
  x: 0.9, y: 6.5, w: 6, h: 0.3,
  fontSize: 11, fontFace: "Calibri", color: MUTED, italic: true,
});

// ═══════════════════════════════════════════════════════════
// SLIDE 4 — WHAT THE AI EXTRACTS
// ═══════════════════════════════════════════════════════════
let slide4 = pres.addSlide();
slide4.background = { color: DARK };
slide4.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: "100%", h: 0.06, fill: { color: ACCENT },
});

slide4.addText("What the AI Extracts — Automatically", {
  x: 0.8, y: 0.4, w: 10, h: 0.7,
  fontSize: 34, fontFace: "Calibri", bold: true, color: WHITE,
});

slide4.addText("From that 2-minute call, the AI produces this in under 10 seconds:", {
  x: 0.8, y: 1.0, w: 10, h: 0.5,
  fontSize: 15, fontFace: "Calibri", color: MUTED,
});

// Left column — customer data card
slide4.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.7, w: 6.0, h: 4.6,
  fill: { color: BG_CARD }, rectRadius: 0.15,
});

const dataRows = [
  ["Customer", "Sarah Henderson"],
  ["Phone", "214-555-0847"],
  ["Address", "4521 Oak Hollow Dr, Frisco TX"],
  ["Referral", "Thompson family (past client)"],
  ["Scope", "Patio (8), driveway paths (12), tree uplights (6)"],
  ["Budget", "$5,000 - $8,000 (confirmed)"],
  ["Timeline", "Before June — daughter's graduation"],
  ["Next Step", "On-site consultation Thursday 2 PM"],
];

let dataY = 1.9;
dataRows.forEach((row) => {
  slide4.addText([
    { text: row[0], options: { bold: true, color: MUTED, fontSize: 13 } },
  ], {
    x: 0.8, y: dataY, w: 1.8, h: 0.45,
    fontFace: "Calibri",
  });
  slide4.addText(row[1], {
    x: 2.7, y: dataY, w: 3.6, h: 0.45,
    fontSize: 13, fontFace: "Calibri", color: WHITE,
  });
  dataY += 0.52;
});

// Right column — scoring card
slide4.addShape(pres.ShapeType.rect, {
  x: 6.8, y: 1.7, w: 6.0, h: 2.1,
  fill: { color: BG_CARD }, rectRadius: 0.15,
});

slide4.addText("Lead Score", {
  x: 6.8, y: 1.8, w: 6.0, h: 0.5,
  fontSize: 16, fontFace: "Calibri", bold: true, color: MUTED, align: "center",
});

slide4.addText("92 / 100", {
  x: 6.8, y: 2.2, w: 3.0, h: 1.0,
  fontSize: 52, fontFace: "Calibri", bold: true, color: GREEN, align: "center",
});

slide4.addText("Grade: A", {
  x: 9.8, y: 2.2, w: 3.0, h: 1.0,
  fontSize: 36, fontFace: "Calibri", bold: true, color: GREEN, align: "center",
});

// Sentiment card
slide4.addShape(pres.ShapeType.rect, {
  x: 6.8, y: 4.0, w: 6.0, h: 2.3,
  fill: { color: BG_CARD }, rectRadius: 0.15,
});

slide4.addText("Buying Signals Detected", {
  x: 6.8, y: 4.1, w: 6.0, h: 0.5,
  fontSize: 16, fontFace: "Calibri", bold: true, color: MUTED, align: "center",
});

const signals = [
  "Budget ready ($5-8K confirmed)",
  "Emotional deadline (graduation party)",
  "Referral from happy past client",
  "Zero hesitation on consultation",
];

let sigY = 4.6;
signals.forEach((s) => {
  slide4.addText("\u2713  " + s, {
    x: 7.1, y: sigY, w: 5.5, h: 0.38,
    fontSize: 13, fontFace: "Calibri", color: GREEN,
  });
  sigY += 0.4;
});

// ═══════════════════════════════════════════════════════════
// SLIDE 5 — ACTIONS TRIGGERED
// ═══════════════════════════════════════════════════════════
let slide5 = pres.addSlide();
slide5.background = { color: DARK };
slide5.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: "100%", h: 0.06, fill: { color: ACCENT },
});

slide5.addText("What Happens Next — Without Lifting a Finger", {
  x: 0.8, y: 0.4, w: 11, h: 0.7,
  fontSize: 34, fontFace: "Calibri", bold: true, color: WHITE,
});

slide5.addText("All triggered automatically within 2 minutes of the call ending:", {
  x: 0.8, y: 1.0, w: 10, h: 0.5,
  fontSize: 15, fontFace: "Calibri", color: MUTED,
});

const actions = [
  {
    time: "10:25 AM",
    delay: "+2 min",
    title: "Confirmation Text to Sarah",
    desc: "\"Thanks for calling Brilliance! Your consultation is confirmed for Thursday, March 6 at 2:00 PM.\"",
    color: GREEN,
  },
  {
    time: "10:24 AM",
    delay: "+1 min",
    title: "Slack Alert to Jake",
    desc: "\"Hot lead — Sarah Henderson, $5-8K patio + driveway, Frisco. Close probability: 85%. Assign your best rep.\"",
    color: GOLD,
  },
  {
    time: "10:24 AM",
    delay: "+1 min",
    title: "CRM Entry Created",
    desc: "Full lead profile with score (92/A), contact info, scope, budget, referral source, consultation date.",
    color: ACCENT,
  },
  {
    time: "Wed 10 AM",
    delay: "Scheduled",
    title: "Day-Before Reminder",
    desc: "Text to Sarah + assigned rep: \"Your consultation is tomorrow at 2 PM.\"",
    color: MUTED,
  },
  {
    time: "Sat 2 PM",
    delay: "Watchdog",
    title: "Proposal Follow-Up",
    desc: "If no proposal sent within 48 hours of consultation: \"Hey Jake — Sarah's an A-lead. Want me to draft the proposal?\"",
    color: MUTED,
  },
];

let actY = 1.7;
actions.forEach((a) => {
  // Card
  slide5.addShape(pres.ShapeType.rect, {
    x: 0.5, y: actY, w: 12.3, h: 0.9,
    fill: { color: BG_CARD }, rectRadius: 0.1,
  });
  // Time badge
  slide5.addShape(pres.ShapeType.rect, {
    x: 0.7, y: actY + 0.15, w: 1.4, h: 0.6,
    fill: { color: TEAL }, rectRadius: 0.08,
  });
  slide5.addText(a.delay, {
    x: 0.7, y: actY + 0.15, w: 1.4, h: 0.6,
    fontSize: 12, fontFace: "Calibri", bold: true, color: WHITE, align: "center", valign: "middle",
  });
  // Title
  slide5.addText(a.title, {
    x: 2.3, y: actY + 0.05, w: 4, h: 0.4,
    fontSize: 16, fontFace: "Calibri", bold: true, color: a.color,
  });
  // Desc
  slide5.addText(a.desc, {
    x: 2.3, y: actY + 0.42, w: 10.3, h: 0.4,
    fontSize: 12, fontFace: "Calibri", color: LIGHT, italic: true,
  });
  actY += 1.0;
});

// ═══════════════════════════════════════════════════════════
// SLIDE 6 — BEFORE / AFTER + ROI
// ═══════════════════════════════════════════════════════════
let slide6 = pres.addSlide();
slide6.background = { color: DARK };
slide6.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: "100%", h: 0.06, fill: { color: ACCENT },
});

slide6.addText("Before vs. After", {
  x: 0.8, y: 0.4, w: 8, h: 0.7,
  fontSize: 36, fontFace: "Calibri", bold: true, color: WHITE,
});

// Before card
slide6.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 1.3, w: 6.0, h: 3.5,
  fill: { color: BG_CARD }, rectRadius: 0.15,
});

slide6.addText("WITHOUT AI", {
  x: 0.5, y: 1.4, w: 6.0, h: 0.5,
  fontSize: 18, fontFace: "Calibri", bold: true, color: ACCENT, align: "center",
});

const before = [
  "40% of calls missed — no voicemail follow-up",
  "Customer info on sticky notes",
  "\"I'll call them back\" (never does)",
  "No lead scoring — treat every call the same",
  "No reminders — appointments forgotten",
  "No idea how many leads slip through",
];

let befY = 2.0;
before.forEach((b) => {
  slide6.addText("\u2717  " + b, {
    x: 0.8, y: befY, w: 5.5, h: 0.4,
    fontSize: 13, fontFace: "Calibri", color: ACCENT,
  });
  befY += 0.43;
});

// After card
slide6.addShape(pres.ShapeType.rect, {
  x: 6.8, y: 1.3, w: 6.0, h: 3.5,
  fill: { color: BG_CARD }, rectRadius: 0.15,
});

slide6.addText("WITH AI", {
  x: 6.8, y: 1.4, w: 6.0, h: 0.5,
  fontSize: 18, fontFace: "Calibri", bold: true, color: GREEN, align: "center",
});

const after = [
  "Every call captured — answered or recorded",
  "Full lead profile auto-generated",
  "Follow-up texts sent in under 2 minutes",
  "AI scores + grades every lead automatically",
  "Day-before reminders to customer + rep",
  "48-hour watchdog catches dropped balls",
];

let aftY = 2.0;
after.forEach((a) => {
  slide6.addText("\u2713  " + a, {
    x: 7.1, y: aftY, w: 5.5, h: 0.4,
    fontSize: 13, fontFace: "Calibri", color: GREEN,
  });
  aftY += 0.43;
});

// ROI bar at bottom
slide6.addShape(pres.ShapeType.rect, {
  x: 0.5, y: 5.2, w: 12.3, h: 1.6,
  fill: { color: TEAL }, rectRadius: 0.15,
});

slide6.addText("Recovered Revenue", {
  x: 0.8, y: 5.3, w: 4, h: 0.5,
  fontSize: 14, fontFace: "Calibri", color: MUTED,
});

slide6.addText("10 recovered leads/week  x  $5K avg job  x  30% close rate", {
  x: 0.8, y: 5.7, w: 6, h: 0.5,
  fontSize: 14, fontFace: "Calibri", color: LIGHT,
});

slide6.addText("$75K / month", {
  x: 7.5, y: 5.3, w: 5, h: 1.4,
  fontSize: 52, fontFace: "Calibri", bold: true, color: GOLD, align: "center", valign: "middle",
});

// ═══════════════════════════════════════════════════════════
// SLIDE 7 — FULL AI PLAYBOOK
// ═══════════════════════════════════════════════════════════
let slide7 = pres.addSlide();
slide7.background = { color: DARK };
slide7.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: "100%", h: 0.06, fill: { color: ACCENT },
});

slide7.addText("Phone AI Is Just the Start.", {
  x: 0.8, y: 0.4, w: 10, h: 0.8,
  fontSize: 36, fontFace: "Calibri", bold: true, color: WHITE,
});

slide7.addText("The Silent AI Partner handles your entire back office:", {
  x: 0.8, y: 1.1, w: 10, h: 0.5,
  fontSize: 16, fontFace: "Calibri", color: MUTED,
});

const playbook = [
  { icon: "\u260E", title: "Phone AI", desc: "Every call captured, transcribed, and actioned", pct: "100%" },
  { icon: "\u270E", title: "Proposals", desc: "Generated from consultation notes in minutes, not hours", pct: "90%" },
  { icon: "\u2709", title: "Follow-Ups", desc: "3-stage sequences that never let a lead go cold", pct: "100%" },
  { icon: "\u2630", title: "Crew Scheduling", desc: "Automated job assignments with materials lists", pct: "80%" },
  { icon: "\u2605", title: "Reviews & Referrals", desc: "Post-install requests sent automatically", pct: "100%" },
  { icon: "\u25A0", title: "Weekly Reports", desc: "Pipeline, revenue, and crew utilization at a glance", pct: "100%" },
];

let pbY = 1.8;
playbook.forEach((p, i) => {
  let col = i < 3 ? 0.5 : 6.8;
  let row = i < 3 ? pbY + i * 1.5 : pbY + (i - 3) * 1.5;

  // Card
  slide7.addShape(pres.ShapeType.rect, {
    x: col, y: row, w: 6.0, h: 1.3,
    fill: { color: BG_CARD }, rectRadius: 0.12,
  });
  // Icon
  slide7.addShape(pres.ShapeType.ellipse, {
    x: col + 0.2, y: row + 0.2, w: 0.9, h: 0.9,
    fill: { color: TEAL },
  });
  slide7.addText(p.icon, {
    x: col + 0.2, y: row + 0.2, w: 0.9, h: 0.9,
    fontSize: 22, align: "center", valign: "middle", color: WHITE,
  });
  // Title + desc
  slide7.addText(p.title, {
    x: col + 1.3, y: row + 0.15, w: 3.5, h: 0.45,
    fontSize: 16, fontFace: "Calibri", bold: true, color: WHITE,
  });
  slide7.addText(p.desc, {
    x: col + 1.3, y: row + 0.6, w: 4.2, h: 0.5,
    fontSize: 12, fontFace: "Calibri", color: MUTED,
  });
  // Automation %
  slide7.addText(p.pct, {
    x: col + 5.0, y: row + 0.2, w: 0.8, h: 0.9,
    fontSize: 20, fontFace: "Calibri", bold: true, color: GREEN, align: "center", valign: "middle",
  });
});

// Bottom note
slide7.addText("50-80% of back-office work — automated.", {
  x: 0.8, y: 6.6, w: 12, h: 0.5,
  fontSize: 18, fontFace: "Calibri", bold: true, color: GOLD, align: "center",
});

// ═══════════════════════════════════════════════════════════
// SLIDE 8 — NEXT STEPS / CTA
// ═══════════════════════════════════════════════════════════
let slide8 = pres.addSlide();
slide8.background = { color: DARK };
slide8.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: "100%", h: 0.06, fill: { color: ACCENT },
});

slide8.addText("Want This Running\nfor Your Business?", {
  x: 1.5, y: 1.5, w: 10.3, h: 2.0,
  fontSize: 48, fontFace: "Calibri", bold: true, color: WHITE, align: "center",
  lineSpacingMultiple: 1.2,
});

slide8.addText("Customized to your workflows. Live in 2 weeks.", {
  x: 1.5, y: 3.5, w: 10.3, h: 0.7,
  fontSize: 20, fontFace: "Calibri", color: MUTED, align: "center",
});

// CTA button shape
slide8.addShape(pres.ShapeType.rect, {
  x: 4.3, y: 4.5, w: 4.7, h: 0.9,
  fill: { color: ACCENT }, rectRadius: 0.12,
});
slide8.addText("Let's Talk", {
  x: 4.3, y: 4.5, w: 4.7, h: 0.9,
  fontSize: 24, fontFace: "Calibri", bold: true, color: WHITE, align: "center", valign: "middle",
});

// Contact info
slide8.addText("Wes\nCEO, Omnia Intelligence AI", {
  x: 1.5, y: 5.8, w: 10.3, h: 1.0,
  fontSize: 16, fontFace: "Calibri", color: MUTED, align: "center",
  lineSpacingMultiple: 1.5,
});

// ── Save ──
const outPath = "c:/Users/default.DESKTOP-ON29PVN/OneDrive/Pictures/New folder/Wes EA/projects/ceo-demo/brilliance-outdoor-lighting/showcase-deck.pptx";
pres.writeFile({ fileName: outPath })
  .then(() => console.log("PPTX saved to: " + outPath))
  .catch((err) => console.error("Error:", err));

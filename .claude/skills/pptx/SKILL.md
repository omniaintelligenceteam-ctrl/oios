---
name: pptx
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill."
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX Skill

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Unpack → edit XML → repack |
| Create from scratch | Use pptxgenjs |

---

## Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview
python scripts/thumbnail.py presentation.pptx

# Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## Converting to Images

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

---

## Design Ideas

**Don't create boring slides.** Plain bullets on a white background won't impress anyone.

### Before Starting

- **Pick a bold, content-informed color palette**: Should feel designed for THIS topic
- **Dominance over equality**: One color dominates (60-70%), 1-2 supporting, one sharp accent
- **Dark/light contrast**: Dark for title + conclusion, light for content — or commit to dark throughout
- **Commit to a visual motif**: Pick ONE distinctive element and repeat it

### Color Palettes

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| **Teal Trust** | `028090` (teal) | `00A896` (seafoam) | `02C39A` (mint) |
| **Cherry Bold** | `990011` (cherry) | `FCF6F5` (off-white) | `2F3C7E` (navy) |

### For Each Slide

**Every slide needs a visual element** — image, chart, icon, or shape.

**Layout options:**
- Two-column (text left, illustration right)
- Icon + text rows (icon in colored circle, bold header, description below)
- Large stat callouts (big numbers 60-72pt with small labels)
- Timeline or process flow

### Typography

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

### Avoid

- Don't repeat the same layout across slides
- Don't center body text
- Don't default to blue — pick colors that reflect the topic
- Don't create text-only slides
- **NEVER use accent lines under titles** — hallmark of AI-generated slides

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

### Content QA

```bash
python -m markitdown output.pptx
```

Check for leftover placeholder text:
```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum"
```

### Visual QA

Convert to images, then inspect:

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements
- Text overflow or cut off at edges
- Elements too close (< 0.3" gaps)
- Uneven gaps
- Low-contrast text or icons
- Leftover placeholder content

For each slide, list issues or areas of concern.
```

### Verification Loop

1. Generate slides → Convert to images → Inspect
2. List issues found
3. Fix issues
4. Re-verify affected slides
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Dependencies

- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - thumbnail grids
- `npm install -g pptxgenjs` - creating from scratch
- LibreOffice (`soffice`) - PDF conversion
- Poppler (`pdftoppm`) - PDF to images

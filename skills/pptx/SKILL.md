---
name: pptx
description: 'Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions "deck," "slides," "presentation," or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.'
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX Skill

## Quick Reference

| Task                          | Guide                                                  |
| ----------------------------- | ------------------------------------------------------ |
| Read/analyze content          | `python -m markitdown presentation.pptx`               |
| Create or edit Yuma deck      | Use Yuma template — see [Creating Yuma Presentations](#creating-yuma-presentations) |
| Edit an existing presentation | Read [editing.md](editing.md)                          |
| Create without a template     | Read [pptxgenjs.md](pptxgenjs.md) (last resort only)  |

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

## Creating Yuma Presentations

**Always start from `artifacts/Yuma Powerpoint template final.pptx`.** This file embeds the full Yuma slide master — fonts, brand colors, Y-motif backgrounds, logo, footer bars, and slide numbers are all built into the layouts. **Do not apply these styles by hand.**

### Workflow

1. **Unpack the template:**
   ```bash
   python scripts/office/unpack.py "artifacts/Yuma Powerpoint template final.pptx" unpacked/
   ```

2. **Add slides** using `add_slide.py` with the appropriate layout file (see [Layout Reference](#layout-reference)):
   ```bash
   python scripts/add_slide.py unpacked/ slideLayout1.xml   # title slide
   python scripts/add_slide.py unpacked/ slideLayout9.xml   # content slide
   ```
   Add each `<p:sldId>` printed by the command into `ppt/presentation.xml` → `<p:sldIdLst>`, in slide order.

3. **Delete the template's example slides** — remove all original `<p:sldId>` entries from `<p:sldIdLst>`.

4. **Edit content** in each slide XML — text only. Fonts, colors, backgrounds, and logo all inherit from the layout/master; do not override them.

5. **Clean and pack:**
   ```bash
   python scripts/clean.py unpacked/
   python scripts/office/pack.py unpacked/ output.pptx --original "artifacts/Yuma Powerpoint template final.pptx"
   ```

See [editing.md](editing.md) for full details on the unpack/edit/pack workflow.

### Layout Reference

**Vary your layouts** — monotonous presentations are a common failure mode. Use the right layout for each content type.

| Layout file          | Layout name                    | Use for                                     |
| -------------------- | ------------------------------ | ------------------------------------------- |
| `slideLayout1.xml`   | PPTtitle-green                 | Title / cover slide (green background)      |
| `slideLayout2.xml`   | PPTtitle-white-bg_image        | Title slide (white background + image)      |
| `slideLayout3.xml`   | Agenda_4Items                  | Agenda with up to 4 items                   |
| `slideLayout4.xml`   | Agenda_8Items                  | Agenda with 5–8 items                       |
| `slideLayout5.xml`   | Section1                       | Section divider (style 1)                   |
| `slideLayout6.xml`   | Section2                       | Section divider (style 2)                   |
| `slideLayout7.xml`   | Section3                       | Section divider (style 3)                   |
| `slideLayout8.xml`   | Title-only                     | Title only, no body                         |
| `slideLayout9.xml`   | Title-and-body                 | Standard title + body text                  |
| `slideLayout10.xml`  | Title-and-body-in-2columns     | Two-column content                          |
| `slideLayout11.xml`  | Title-and-3image-3body         | 3 images + 3 body sections                  |
| `slideLayout12.xml`  | Title-body_left-image_right    | Body text left, image right                 |
| `slideLayout13.xml`  | Title-image_left-body_right    | Image left, body text right                 |
| `slideLayout14.xml`  | Title_White-background_image   | White background with full image            |
| `slideLayout15.xml`  | Title_Black-background_image   | Black background with full image            |
| `slideLayout16.xml`  | Title-background green         | Title with green background                 |
| `slideLayout17.xml`  | TheFutureIsYuman               | Statement / "The future is yuman." tagline  |
| `slideLayout18.xml`  | Thankyou                       | Thank you / closing slide                   |
| `slideLayout19.xml`  | Title-and-chart                | Title + chart placeholder                   |

---

## Editing Workflow

**Read [editing.md](editing.md) for full details.**

Use when editing an existing presentation (not the Yuma template workflow above):

1. Analyze slides with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

---

## Creating Without a Template

**Read [pptxgenjs.md](pptxgenjs.md) for full details.**

Use only when there is no template and the output is not a Yuma-branded presentation. For all Yuma presentations, use the template workflow above.

---

## Yuma Design System (Reference / QA)

The following documents the Yuma brand. The `artifacts/Yuma Powerpoint template final.pptx` slide master already encodes all of this — use it for QA to verify the output matches brand standards, not as a manual implementation guide.

### Color Palette

| Color         | Hex      | Role                                                                |
| ------------- | -------- | ------------------------------------------------------------------- |
| Black         | `000000` | Primary text, dark backgrounds                                      |
| White         | `FFFFFF` | Light backgrounds, text on dark                                     |
| Off White     | `F8F5F5` | Subtle background alternative                                       |
| Forest Green  | `005D45` | **Primary brand color** — title slide backgrounds, section emphasis |
| Future Green  | `21E467` | Bright accent — sparingly for highlights                            |
| Bright Green  | `00E953` | Title text on dark green backgrounds                                |
| Granular Grey | `F0ECE9` | Footer bar background, secondary surfaces                           |
| Earth         | `C4A892` | Warm neutral accent                                                 |
| Purple        | `6434DA` | Accent — footer source labels, subtle highlights                    |
| Pink          | `EBA8FF` | Accent — thank-you/closing slide backgrounds                        |

For charts, use series colors: `005D45`, `6434DA`, `EBA8FF`, `C4A892`, `4FC36B`.

### Typography

**Heading font:** Bogue Slab Thin (embedded in the template). **Body font:** Inter.

| Element                 | Size    | Weight             |
| ----------------------- | ------- | ------------------ |
| Title slide heading     | 60pt    | regular (not bold) |
| Content slide title     | 35pt    | regular (not bold) |
| Statement / quote text  | 45–60pt | regular (not bold) |
| Body text               | 16pt    | regular            |
| Agenda / section number | 60pt    | regular            |
| Footer / slide number   | 10pt    | regular            |

**Key rules:** headings are NEVER bold. Body text is left-aligned (center only on statement slides).

### Overall Design Principles

- **Minimalist and clean**: lots of whitespace, flat design, no gradients, no shadows
- **Left-aligned by default**: center only on statement/quote slides
- **No accent lines under titles**, no rounded corners, no shadows
- **Zero-padded section numbers**: "01", "02", "03"
- **Vary layouts**: mix title+body, two-column, text+image, and chart slides
- **Dark/light sandwich**: Forest Green title → White content slides → Pink closing

### Avoid (Yuma-Specific)

- **NEVER use colors outside the Yuma palette**
- **NEVER bold headings**
- **NEVER center body text**
- **NEVER use shadows or gradients**
- **NEVER use accent lines under titles**
- **NEVER skip the logo** — content slides must have the Yuma logo in the footer (it is in the slide master; don't remove it)
- **Don't mix fonts** — heading and body fonts come from the master; do not override them
- **Don't repeat the same layout**

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step. If you found zero issues on first inspection, you weren't looking hard enough.

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

### Visual QA

**⚠️ USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and will see what you expect, not what's there. Subagents have fresh eyes.

Convert slides to images (see [Converting to Images](#converting-to-images)), then use this prompt:

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. /path/to/slide-01.jpg (Expected: [brief description])
2. /path/to/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

### Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Converting to Images

Convert presentations to individual slide images for visual inspection:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

This creates `slide-01.jpg`, `slide-02.jpg`, etc.

To re-render specific slides after fixes:

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

## Dependencies

- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - thumbnail grids
- `pip install cairosvg` - Y-motif background generation (also needs the `cairo` system library: `brew install cairo` on macOS)
- `npm install -g pptxgenjs` - creating without a template (last resort)
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images

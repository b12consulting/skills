---
name: pptx
description: 'Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions "deck," "slides," "presentation," or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill.'
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX Skill

## Quick Reference

| Task                         | Guide                                    |
| ---------------------------- | ---------------------------------------- |
| Read/analyze content         | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read [editing.md](editing.md)            |
| Create from scratch          | Read [pptxgenjs.md](pptxgenjs.md)        |

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

## Editing Workflow

**Read [editing.md](editing.md) for full details.**

1. Analyze template with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

---

## Creating from Scratch

**Read [pptxgenjs.md](pptxgenjs.md) for full details.**

Use when no template or reference presentation is available.

---

## Yuma Design System (Mandatory)

**All presentations MUST follow the Yuma brand design.** Do not invent colors, pick your own fonts, or freestyle the layout. Every design choice below comes from the official Yuma brand guidelines and must be applied consistently.

### Slide Dimensions

Always use `LAYOUT_WIDE` (13.33" × 7.5"). This is the standard Yuma slide format.

```javascript
pres.layout = "LAYOUT_WIDE"; // 13.33" × 7.5"
```

### Color Palette

Use ONLY these colors. Do not introduce any color outside this palette.

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

**Color usage rules:**

- Title/cover slides: **Forest Green** (`005D45`) background with **Bright Green** (`00E953`) title text and White subtitle text
- Content slides: **White** background with **Black** text
- Statement/quote slides: White background (or Forest Green for emphasis)
- Section dividers: White background with Black text
- Thank-you/closing: **Pink** (`EBA8FF`) background with Black text
- Footer bar on content slides: **Granular Grey** (`F0ECE9`) background
- Charts: use `005D45`, `6434DA`, `EBA8FF`, `C4A892`, `4FC36B` as series colors

### Typography

**Heading font:** `Merriweather` (the Google Fonts substitute for Bogue Slab Thin, which is not available in PptxGenJS). Use regular weight — Yuma headings are thin/light, not bold.

**Body font:** `Inter` (available via Google Fonts). Use light weight where possible, regular for emphasis.

**Fallbacks** (if the above are unavailable): `Times New Roman` for headings, `Arial` for body.

| Element                     | Font         | Size    | Weight             | Spacing           |
| --------------------------- | ------------ | ------- | ------------------ | ----------------- |
| Title slide heading         | Merriweather | 60pt    | regular (not bold) | tight             |
| Title slide subtitle (name) | Inter        | 20pt    | bold               | —                 |
| Title slide subtitle (date) | Inter        | 20pt    | regular            | —                 |
| Content slide title         | Merriweather | 35pt    | regular (not bold) | —                 |
| Statement/quote text        | Merriweather | 45–60pt | regular (not bold) | tight             |
| Body text                   | Inter        | 16pt    | regular            | charSpacing: -0.6 |
| Body bold labels            | Inter        | 16pt    | bold               | charSpacing: -0.6 |
| Agenda numbers              | Merriweather | 60pt    | regular            | —                 |
| Agenda item title           | Inter        | 30pt    | bold               | —                 |
| Agenda item description     | Inter        | 16pt    | regular            | —                 |
| Section divider number      | Merriweather | 60pt    | regular            | —                 |
| Section divider title       | Inter        | 30pt    | bold               | —                 |
| Footer text / source        | Inter        | 10pt    | regular            | —                 |
| Slide number                | Inter        | 10pt    | regular            | —                 |
| Closing "Thank you"         | Inter        | 15pt    | regular            | charSpacing: 0.6  |

**Key typography rules:**

- Headings are NEVER bold — Yuma's brand uses a thin serif font for headings
- Body text uses -0.6pt character spacing (`charSpacing: -0.6` in PptxGenJS)
- Left-align all text (titles, body, lists) — do NOT center except on statement slides
- Statement/quote slides: center-aligned, tight line spacing (80%)
- Body line spacing: 110%
- Title line spacing: 90%

### Iconic Y-Motif Backgrounds

A signature element of Yuma presentations is the **oversized Y symbol** used as a decorative background motif. The Y is rendered in a tone-on-tone style (slightly different shade than the background) and bleeds off the slide edges.

Pre-generated background images are available in `skills/yuma-design/references/`:

| Background               | File                         | Usage                            |
| ------------------------ | ---------------------------- | -------------------------------- |
| Green + bright Y (right) | `yuma-bg-title-green.png`    | Title/cover slides               |
| Green + bright Y (left)  | `yuma-bg-section-green.png`  | Section dividers with green bg   |
| White + subtle grey Y    | `yuma-bg-content-subtle.png` | Statement slides, accent content |
| Pink + darker pink Y     | `yuma-bg-closing-pink.png`   | Thank-you/closing slides         |

```javascript
// Title slide with Y-motif background
slide.background = {
  path: "skills/yuma-design/references/yuma-bg-title-green.png",
};

// Statement slide with subtle Y
slide.background = {
  path: "skills/yuma-design/references/yuma-bg-content-subtle.png",
};
```

**When to use Y-motif backgrounds:**

- Title/cover slide: **always** use `yuma-bg-title-green.png`
- Section dividers: optionally use a green Y background for visual impact
- Statement/quote slides: use `yuma-bg-content-subtle.png` for a branded feel
- Closing slide: **always** use `yuma-bg-closing-pink.png`
- Content slides: plain white — do NOT use Y backgrounds on text-heavy slides

**To regenerate or customize backgrounds**, run:

```bash
python scripts/generate_backgrounds.py
```

This script renders the Yuma symbol SVG (`skills/yuma-design/references/Yuma_Symbol_Black-RGB.svg`) at 250% slide height onto colored backgrounds. Requires `cairosvg` and `Pillow`. Edit the script to adjust positioning, scale, or add new color variants.

### Yuma Logo

**Every content slide must include the Yuma logo in the footer.** The logo file is at `skills/yuma-design/references/Yuma_logo_Black-RGB.png` (use `Yuma_logo_White-RGB.png` on dark backgrounds).

Title slides also show the logo — in white, top-right corner.

```javascript
// Footer logo — bottom-left of every content slide
slide.addImage({
  path: "skills/yuma-design/references/Yuma_logo_Black-RGB.png",
  x: 0.38,
  y: 6.9,
  w: 0.89,
  h: 0.37,
});

// Title slide logo — top-right, white variant
slide.addImage({
  path: "skills/yuma-design/references/Yuma_logo_White-RGB.png",
  x: 10.8,
  y: 0.4,
  w: 1.6,
  h: 0.66,
});
```

The footer logo should NOT appear on title, statement, or closing slides.

### Slide Number

Content slides display the slide number at the bottom-right, 10pt Inter, right-aligned.

```javascript
slide.addText(String(slideNum), {
  x: 9.3,
  y: 6.9,
  w: 3.85,
  h: 0.4,
  fontFace: "Inter",
  fontSize: 10,
  color: "000000",
  align: "right",
  margin: 0,
});
```

### Slide Types & Layout Patterns

Use the following patterns for each slide type. **Vary your layouts** — don't repeat the same content layout for every slide.

#### 1. Title / Cover Slide

- Background: `yuma-bg-title-green.png` (Forest Green with bright green Y-motif on right)
- Yuma logo: top-right, white variant (x: 10.8", y: 0.4", w: 1.6")
- Title: 60pt Merriweather, **Bright Green** (`00E953`) text, left-aligned, lower-left area (x: 0.37", y: 2.35", w: 8")
- Subtitle line 1 (author name): 20pt Inter bold, White text (x: 0.37", y: 6.15")
- Subtitle line 2 (date): 20pt Inter regular, White text, directly below name
- No footer logo, no slide number

#### 2. Agenda Slide

- Background: White
- "Agenda" title: 35pt Merriweather, top-left
- Numbered items in a **staircase layout** — each item steps down and to the right:
  - Number: 60pt Merriweather (e.g., "01", "02", "03", "04")
  - Item title: 30pt Inter bold, next to the number
  - Description: 16pt Inter regular, below the title
- Items arranged diagonally across the slide, not in a simple grid
- Logo + slide number in footer

#### 3. Section Divider

- Background: White (or optional background image)
- Large section number: 60pt Merriweather, vertically centered, left side
- Section title + description: 30pt Inter bold + 16pt Inter, next to the number
- No logo on these (they act as visual breaks)

#### 4. Content Slide (Title + Body)

- Background: White
- Title: 35pt Merriweather, top-left (x: 0.37", y: 0.6", w: 12.5", h: 0.6")
- Body area: (x: 0.37", y: 1.31", w: 8.3", h: 5.4") — leave right margin for breathing room
- Body text: 16pt Inter with charSpacing: -0.6, lineSpacingMultiple: 1.1
- Text hierarchy (use PptxGenJS `indentLevel` for nesting):
  - Level 0: regular text, no bullet, no indent
  - Level 0 + bold: inline labels/headers (e.g. "Item one in Inter Light (Bold) 16pt")
  - Level 1: • bullet (use `bullet: true`), regular text
  - Level 2: ○ sub-bullet (use `bullet: {code: "o"}`), regular text
- **Important**: body text items are an array of `{ text, options }` objects. Each item in the list hierarchy must be a separate entry with `breakLine: true` and the appropriate `indentLevel` and `bullet` setting.
- Logo + slide number in footer

#### 5. Two-Column Content

- Same as content slide but body area split into two columns
- Left column: x 0.37", width ~5.3"
- Right column: x ~6.7", width ~5.3"
- Both columns share the same title at top

#### 6. Content + Image (Split Layout)

- Title at top (one half)
- Text on one side (~47% width), image placeholder on the other (~47% width)
- Can be text-left/image-right OR image-left/text-right — vary across slides

#### 7. Statement / Quote Slide

- Background: `yuma-bg-content-subtle.png` (white with subtle grey Y) or plain white, or `yuma-bg-title-green.png`
- Large text: 45–60pt Merriweather, left-aligned or center-aligned, tight line spacing (80%)
- Text positioned at left-center (x: 0.37", y: ~1.4", w: ~6.6") — not full width, to leave room for visual balance
- No footer, no logo, no slide number

#### 8. Chart Slide

- Title: 35pt Merriweather, top-left
- Chart area positioned below title
- Use Yuma palette colors for chart series: `005D45`, `6434DA`, `EBA8FF`, `C4A892`, `4FC36B`
- Logo + slide number in footer

#### 9. Thank You / Closing Slide

- Background: `yuma-bg-closing-pink.png` (pink with subtle Y-motif)
- "Thank you." text: 15pt Inter, bottom-left area (x: 0.37", y: 6.7")
- Contact email: 15pt Inter, below
- Optional: Large Yuma tagline ("The future is yuman.") in 60pt Merriweather at center
- No footer logo, no slide number

### Overall Design Principles

- **Minimalist and clean**: Yuma's style is understated — lots of whitespace, flat design, no gradients, no shadows, no decorative shapes
- **Left-aligned by default**: Almost all text (titles, body, lists) is left-aligned. Only statement/quote slides use center alignment
- **No accent lines or underlines**: Do not put decorative lines under or next to titles
- **No rounded corners, no shadows, no gradients**: Keep shapes simple and flat
- **Zero-padded section numbers**: Use "01", "02", "03" format, not "1", "2", "3"
- **Consistent margins**: ~0.37" left margin, ~0.37" from edges on all sides
- **Vary layouts**: Don't use the same content layout for every slide. Mix title+body, two-column, text+image, and chart slides
- **Dark/light sandwich**: Forest Green title slide → White content slides → Pink closing slide

### Avoid (Yuma-Specific)

- **NEVER use colors outside the Yuma palette** — no blues, reds, oranges, or teals
- **NEVER bold the headings** — Yuma headings use thin/light weight serif fonts; bolding them breaks the brand
- **NEVER center body text** — left-align paragraphs and lists; center only statement slides
- **NEVER use shadows or gradients** — the design is completely flat
- **NEVER use accent lines under titles** — use whitespace or background color instead
- **NEVER skip the logo** — content slides must have the Yuma logo in the footer
- **NEVER use generic color palettes** — only the Yuma brand colors listed above
- **Don't mix fonts** — use only Merriweather (headings) and Inter (body), nothing else
- **Don't repeat the same layout** — vary columns, cards, and callouts across slides
- **Don't create text-only slides** — add images, icons, charts, or visual elements
- **Don't forget text box padding** — set `margin: 0` on text boxes when aligning with shapes or icons

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

- `npx skills add b12consulting/skills --skill yuma-design` - Yuma brand design assets
- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - thumbnail grids
- `pip install cairosvg` - Y-motif background generation (also needs the `cairo` system library: `brew install cairo` on macOS)
- `npm install -g pptxgenjs` - creating from scratch
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images

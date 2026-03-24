"""Generate Yuma-branded slide backgrounds with the iconic Y symbol.

Creates background PNGs featuring the oversized Yuma "Y" symbol in the
two-tone style used across Yuma brand materials. Outputs are written to
skills/yuma-design/references/.

Requirements: cairosvg, Pillow (and the cairo system library).
"""

import io
import re
from pathlib import Path

import cairosvg
from PIL import Image

# Resolve paths relative to this script's location
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
SVG_PATH = (
    REPO_ROOT / "skills" / "yuma-design" / "references" / "Yuma_Symbol_Black-RGB.svg"
)
OUT_DIR = REPO_ROOT / "skills" / "yuma-design" / "references"

# Slide dimensions (1920×1080 for high-quality backgrounds)
W, H = 1920, 1080

# Yuma brand colors (RGB tuples)
FOREST_GREEN = (0, 93, 70)  # 005D46
BRIGHT_GREEN = (33, 228, 103)  # 21E467
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (235, 169, 255)  # EBA9FF


def render_symbol(fill_color_hex: str, size: int) -> Image.Image:
    """Render the Y symbol SVG at given size with given fill color."""
    svg = SVG_PATH.read_text()
    svg = re.sub(r"<path ", f'<path fill="{fill_color_hex}" ', svg)
    png_data = cairosvg.svg2png(bytestring=svg.encode(), output_height=size)
    return Image.open(io.BytesIO(png_data)).convert("RGBA")


def make_background(
    bg_color: tuple,
    symbol_color_hex: str,
    symbol_scale: float,
    x_offset_pct: float,
    y_offset_pct: float,
    filename: str,
) -> Path:
    """Create a slide background with the Y symbol.

    Args:
        bg_color: RGB tuple for background
        symbol_color_hex: hex color for the Y symbol (e.g. "#21E467")
        symbol_scale: symbol height relative to slide height (2.5 = 250%)
        x_offset_pct: horizontal center as fraction of slide width
        y_offset_pct: vertical center as fraction of slide height
        filename: output filename
    """
    bg = Image.new("RGB", (W, H), bg_color)
    sym_h = int(H * symbol_scale)
    symbol = render_symbol(symbol_color_hex, sym_h)

    sym_w = symbol.width
    x = int(W * x_offset_pct - sym_w / 2)
    y = int(H * y_offset_pct - sym_h / 2)

    bg.paste(symbol, (x, y), symbol)
    out_path = OUT_DIR / filename
    bg.save(str(out_path), quality=95)
    print(f"Created {out_path.relative_to(REPO_ROOT)} ({bg.size})")
    return out_path


def main():
    # Title slide: Forest Green bg + bright green Y on right side
    make_background(
        bg_color=FOREST_GREEN,
        symbol_color_hex="#21E467",
        symbol_scale=2.5,
        x_offset_pct=0.85,
        y_offset_pct=0.45,
        filename="yuma-bg-title-green.png",
    )

    # Section divider: Forest Green bg + green Y on LEFT side
    make_background(
        bg_color=FOREST_GREEN,
        symbol_color_hex="#21E467",
        symbol_scale=2.5,
        x_offset_pct=0.15,
        y_offset_pct=0.45,
        filename="yuma-bg-section-green.png",
    )

    # Subtle accent: White bg + grey Y for statement slides
    make_background(
        bg_color=WHITE,
        symbol_color_hex="#F0ECE9",
        symbol_scale=2.5,
        x_offset_pct=0.85,
        y_offset_pct=0.45,
        filename="yuma-bg-content-subtle.png",
    )

    # Closing slide: Pink bg + darker pink Y
    make_background(
        bg_color=PINK,
        symbol_color_hex="#D88AEE",
        symbol_scale=2.5,
        x_offset_pct=0.85,
        y_offset_pct=0.45,
        filename="yuma-bg-closing-pink.png",
    )

    print("\nDone! Background images generated.")


if __name__ == "__main__":
    main()

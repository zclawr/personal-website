#!/usr/bin/env python3
"""Regenerate img/bg.jpg from img/background.png.

The source scan (an Art Nouveau "Bearberry" ornament plate) is upside down,
very slightly skewed, and 12 MB. This script turns it upright, deskews it so
the plate's frame runs parallel to the page edges, crops away the blank paper
margin and caption, then desaturates, lowers contrast and lightens it toward
the page colour so the whole plate can sit behind the content as one image.

Run from the site root:  python3 tools/make_bg.py
"""
from pathlib import Path
from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "img" / "background.png"
OUT = ROOT / "img" / "bg.jpg"

# Counter-clockwise rotation in degrees. 180 turns the scan upright; the extra
# tenth of a degree squares up the plate frame (measured from its divider lines).
ROTATE = 180.1

# Crop box (left, top, right, bottom) after rotation: the plate's outer frame
# plus a little of the surrounding paper, dropping the caption below it.
CROP = (90, 15, 2350, 3400)

OUT_WIDTH = 1800     # final width in px (height follows the aspect ratio)
SATURATION = 0.8     # 1.0 = original colour, 0 = greyscale
CONTRAST = 0.8       # 1.0 = original contrast
LIGHTEN = 0.45       # fraction blended toward PAGE_COLOUR (0 = none, 1 = flat)
PAGE_COLOUR = (244, 241, 232)   # --bg in css/style.css, so the paper margin blends in
JPEG_QUALITY = 78


def main() -> None:
    im = Image.open(SRC).convert("RGB")
    im = im.rotate(ROTATE, resample=Image.BICUBIC, fillcolor=(255, 255, 255)).crop(CROP)
    im = im.resize((OUT_WIDTH, round(OUT_WIDTH * im.height / im.width)), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(SATURATION)
    im = ImageEnhance.Contrast(im).enhance(CONTRAST)
    im = Image.blend(im, Image.new("RGB", im.size, PAGE_COLOUR), LIGHTEN)
    im.save(OUT, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    print(f"wrote {OUT.relative_to(ROOT)} {im.size[0]}x{im.size[1]} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

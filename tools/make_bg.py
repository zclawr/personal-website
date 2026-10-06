#!/usr/bin/env python3
"""Regenerate img/bgN.jpg from the scanned plates img/backgroundN.png.

The sources are 12 MB scans of Art Nouveau botanical ornament plates (Bearberry,
Rhododendron, Anemone, Dogtooth Violet, Clammy Lychnis, ...). Some were scanned
upside down, every one is very slightly skewed, and each sits at a different
spot on the page. For each plate this script turns it upright, deskews it so the
plate's outer frame runs parallel to the page edges, crops to the frame plus a
small, consistent strip of paper (dropping the caption below the frame), then
desaturates, lowers contrast and lightens it toward the page colour so it can
sit behind the content as one image.

Per-plate values were measured by fitting straight lines to the plate's outer
frame: ROTATE squares the frame up, FRAME is where the frame's outer line lands
after that rotation. The crop margins around the frame are shared so every
output has the same look as bg1.jpg.

Run from the site root:  python3 tools/make_bg.py          # all plates
                         python3 tools/make_bg.py 3 6      # just some
"""
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageStat

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"

# Per plate: counter-clockwise rotation in degrees (180 turns an upside-down
# scan upright; the fraction squares up the frame) and the outer frame line's
# (left, top, right, bottom) in source pixels *after* that rotation.
PLATES = {
    1: dict(rotate=180.10, frame=(150, 70, 2290, 3370)),   # Bearberry (reference)
    2: dict(rotate=179.89, frame=(180, 100, 2346, 3436)),  # Rhododendron
    3: dict(rotate=0.24,   frame=(189, 131, 2348, 3449)),  # Hare's-ear
    4: dict(rotate=180.14, frame=(110, 96, 2266, 3428)),   # Anemone
    5: dict(rotate=0.11,   frame=(300, 56, 2449, 3357)),   # Dogtooth Violet
    6: dict(rotate=1.19,   frame=(213, 53, 2368, 3353)),   # Clammy Lychnis
}

# Paper kept around the frame, in source pixels (clamped to the scan edge where
# a plate sits too close to it). The bottom is tighter to stay above the caption.
MARGIN_SIDE = 60
MARGIN_TOP = 55
MARGIN_BOTTOM = 30

OUT_WIDTH = 1800     # final width in px (height follows the aspect ratio)
SATURATION = 0.8     # 1.0 = original colour, 0 = greyscale
CONTRAST = 0.8       # 1.0 = original contrast
LIGHTEN = 0.45       # fraction blended toward PAGE_COLOUR (0 = none, 1 = flat)
PAGE_COLOUR = (244, 241, 232)   # --bg in css/style.css, so the paper margin blends in
JPEG_QUALITY = 78


def paper_colour(im: Image.Image) -> tuple[int, int, int]:
    """Median colour of a strip just inside the scan's top edge, i.e. blank paper.
    Used to fill the wedges the deskew rotation exposes at the corners."""
    strip = im.crop((im.width // 4, 8, 3 * im.width // 4, 28))
    return tuple(int(round(v)) for v in ImageStat.Stat(strip).median)


def make(n: int) -> None:
    spec = PLATES[n]
    src = IMG / f"background{n}.png"
    out = IMG / f"bg{n}.jpg"

    im = Image.open(src).convert("RGB")
    im = im.rotate(spec["rotate"], resample=Image.BICUBIC, fillcolor=paper_colour(im))

    left, top, right, bottom = spec["frame"]
    crop = (
        max(0, left - MARGIN_SIDE),
        max(0, top - MARGIN_TOP),
        min(im.width, right + MARGIN_SIDE),
        min(im.height, bottom + MARGIN_BOTTOM),
    )
    im = im.crop(crop)

    im = im.resize((OUT_WIDTH, round(OUT_WIDTH * im.height / im.width)), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(SATURATION)
    im = ImageEnhance.Contrast(im).enhance(CONTRAST)
    im = Image.blend(im, Image.new("RGB", im.size, PAGE_COLOUR), LIGHTEN)
    im.save(out, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    print(f"wrote {out.relative_to(ROOT)} {im.size[0]}x{im.size[1]} "
          f"({out.stat().st_size // 1024} KB)  rotate={spec['rotate']} crop={crop}")


def main(argv: list[str]) -> None:
    plates = [int(a) for a in argv] or sorted(PLATES)
    for n in plates:
        make(n)


if __name__ == "__main__":
    main(sys.argv[1:])

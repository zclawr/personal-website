#!/usr/bin/env python3
"""Regenerate img/bg-tile.jpg from img/background.png.

The source scan (an Art Nouveau "Bearberry" ornament plate) is upside down and
12 MB, so this script rotates it, crops one all-over panel, mirror-tiles it so
the edges meet seamlessly, then desaturates, lowers contrast and lightens it
into a faint wash suitable for a page background.

Run from the site root:  python3 tools/make_bg_tile.py
"""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "img" / "background.png"
OUT = ROOT / "img" / "bg-tile.jpg"

# Crop box (left, top, right, bottom) in source-pixel coordinates, taken from the
# *unrotated* scan: the green-berries panel in the lower-left of the plate.
CROP = (262, 2074, 656, 2747)

TILE_WIDTH = 640      # final tile width in px (height follows the aspect ratio)
SATURATION = 0.6     # 1.0 = original colour, 0 = greyscale
CONTRAST = 0.55       # 1.0 = original contrast
LIGHTEN = 0.68        # fraction blended toward white (0 = none, 1 = all white)
JPEG_QUALITY = 82


def main() -> None:
    panel = Image.open(SRC).convert("RGB").crop(CROP).rotate(180)

    # 2x2 mirror tile: every edge meets its own reflection, so it repeats seamlessly.
    w, h = panel.size
    tile = Image.new("RGB", (2 * w, 2 * h))
    tile.paste(panel, (0, 0))
    tile.paste(ImageOps.mirror(panel), (w, 0))
    tile.paste(ImageOps.flip(panel), (0, h))
    tile.paste(ImageOps.flip(ImageOps.mirror(panel)), (w, h))

    tile = tile.resize((TILE_WIDTH, round(TILE_WIDTH * tile.height / tile.width)), Image.LANCZOS)
    tile = ImageEnhance.Color(tile).enhance(SATURATION)
    tile = ImageEnhance.Contrast(tile).enhance(CONTRAST)
    tile = Image.blend(tile, Image.new("RGB", tile.size, "white"), LIGHTEN)

    tile.save(OUT, "JPEG", quality=JPEG_QUALITY, optimize=True)
    print(f"wrote {OUT.relative_to(ROOT)} {tile.size[0]}x{tile.size[1]} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()

"""Generate favicon files from img/icon.JPG.

Writes favicon.ico (16/32/48 px), favicon.png (192 px) and
apple-touch-icon.png (180 px) to the repo root. Requires Pillow.

    python3 tools/make_favicon.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "img" / "icon.JPG"


def square(im: Image.Image) -> Image.Image:
    """Centre-crop to a square so every output is undistorted."""
    w, h = im.size
    side = min(w, h)
    left, top = (w - side) // 2, (h - side) // 2
    return im.crop((left, top, left + side, top + side))


def main() -> None:
    im = square(Image.open(SRC).convert("RGB"))

    im.resize((192, 192), Image.LANCZOS).save(ROOT / "favicon.png", optimize=True)
    im.resize((180, 180), Image.LANCZOS).save(ROOT / "apple-touch-icon.png", optimize=True)
    im.resize((48, 48), Image.LANCZOS).save(
        ROOT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print("wrote favicon.ico, favicon.png, apple-touch-icon.png")


if __name__ == "__main__":
    main()

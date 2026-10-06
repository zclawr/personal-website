"""Stitch img/bg1.jpg ... img/bg6.jpg into a 3x2 grid with even spacing."""
from PIL import Image
import statistics

COLS, ROWS = 3, 2
GAP = 40                 # pixels between plates (and around the border)
OUT = "img/bg_grid.jpg"

plates = [Image.open(f"img/bg{i}.jpg").convert("RGB") for i in range(1, 7)]
# Fill colour = median colour of the plates' outer 8px margins.
edge = []
for p in plates:
    pw, ph = p.size
    for box in [(0, 0, pw, 8), (0, ph - 8, pw, ph), (0, 0, 8, ph), (pw - 8, 0, pw, ph)]:
        edge += list(p.crop(box).getdata())
BG = tuple(round(statistics.median(c)) for c in zip(*edge))

w = max(p.width for p in plates)
h = max(p.height for p in plates)

canvas = Image.new("RGB", (COLS * w + (COLS + 1) * GAP, ROWS * h + (ROWS + 1) * GAP), BG)
for idx, p in enumerate(plates):
    r, c = divmod(idx, COLS)
    x = GAP + c * (w + GAP) + (w - p.width) // 2
    y = GAP + r * (h + GAP) + (h - p.height) // 2
    canvas.paste(p, (x, y))

canvas.save(OUT, quality=92)
print(f"wrote {OUT} {canvas.size} fill={BG}")

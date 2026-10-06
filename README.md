# Personal website

Static site for Zach Lawrence: plain HTML and CSS, no build step.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Home: portrait, bio, links, Teaching section |
| `publications.html` | Papers with summaries, plus talks and posters |
| `CV.pdf` | Linked from the home page header; opens in a new tab |
| `css/style.css` | Shared styles (colours are CSS variables at the top) |

## Editing

- **Bio / Teaching**: edit the HTML directly. Placeholder sections
  contain an HTML comment showing a suggested format.
- **CV**: replace `CV.pdf`. Nothing else needs to change.
- **Links**: `links.csv` is the record of header links (`label,url`). The
  header in `index.html` is hand-written, so update both when adding a link.
- **Nav**: the `<header class="topbar">` block is duplicated in every page;
  edit both when adding a page.
- **Background**: `img/bg.jpg` is the whole ornament plate, generated from
  `img/background.png` (which is gitignored because it is 12 MB) by

      python3 tools/make_bg.py

  The script turns the scan upright, deskews it, crops to the plate frame and
  softens the colours. Adjust `ROTATE`, `CROP`, `SATURATION`, `CONTRAST`, or
  `LIGHTEN` in that script to taste. Requires Pillow (`pip install pillow`).

## Preview locally

    python3 -m http.server 8000

then open <http://localhost:8000>. Opening `index.html` directly also works,
but some browsers block opening the PDF over `file://`.

## Deploy to GitHub Pages

1. Create a GitHub repo named `zclawr.github.io` (for `https://zclawr.github.io/`)
   or any other name (for `https://zclawr.github.io/<repo>/`; all paths are
   relative so either works).
2. Push this folder:

       git remote add origin git@github.com:zclawr/zclawr.github.io.git
       git push -u origin main

3. In the repo settings, under **Pages**, set the source to *Deploy from a
   branch*, branch `main`, folder `/ (root)`.

`.nojekyll` tells GitHub Pages to serve the files as-is.

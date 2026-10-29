# eCash Card brand

The eCash Card mark is a chip card with three banknotes fanned up from behind it: cash, and the card that carries it. It is drawn in lime with forest outlines, so it reads on light and dark grounds alike. This folder holds the marks, the icons, the wordmark, the web icons and the colors. `generate.py` draws all of it from one set of shapes and colors: change it, run it, and commit what it writes.

```sh
pip install fonttools uharfbuzz   # once; rsvg-convert comes from: brew install librsvg
python3 brand/generate.py
```

## The mark

| File | Use |
| --- | --- |
| `mark/ecash-card-mark.svg` | The color mark: lime card and notes with forest outlines. On paper, on ink and most other grounds. |
| `mark/ecash-card-mark-forest.svg` | One color, forest line art: for one-color print and embossing on light stock. |
| `mark/ecash-card-mark-white.svg` | One color, white line art: on photos and colored grounds. |
| `mark/ecash-card-mark-small.svg`, `-small-forest.svg` | The outlines only, drawn heavier, for 40 px and below, where the notes' inner lines and the chip's contacts would blur. |
| `mark/*-1024.png` | The color, forest and white marks as 1024 px PNGs. |

## The icon

| File | Use |
| --- | --- |
| `icon/ecash-card-icon.svg`, `-1024.png` | The app icon: the mark at 62% of the side on paper. It is square; iOS and the stores round the corners. |
| `icon/ecash-card-avatar.svg`, `-400.png` | Social profiles and the GitHub org. The mark sits smaller, so a circle crop keeps room around it. |

## The wordmark

`lockup/ecash-card-lockup-on-light` and `-on-dark` (SVG and PNG) set the mark beside "ecashcard": "ecash" in Figtree 800 and "card" in Figtree 400, tracked in by 0.02 em, with the mark 1.25 em tall and a 0.32 em gap. On paper the letters are ink and muted; on ink they are paper and a warm grey. The letters are outlines, so the files work without the font. ecashcard.org's header draws the same lockup in HTML and brings it in once on load: the card pops in, the notes fan up from behind it, and the word slides in.

## Web

`web/favicon.svg` (the small mark), `favicon.ico` (16, 32 and 48 px), `favicon-32.png`, `apple-touch-icon.png` (180 px), and `icon-192.png` and `icon-512.png` for a web app manifest.

## Colors and type

`tokens.json` and `tokens.css` list every color with its use. The main ones:

| Token | Value | Use |
| --- | --- | --- |
| `paper` | `#F6F3EC` | The ground: the site, the icon and the deck. |
| `ink` | `#17191C` | Headings and text, and dark bands. |
| `copper`, `copper-dark` | `#B8651F`, `#8F4C13` | The accent: link underlines and the small labels over each section. |
| `lime` | `#B8E06A` | The mark's card and notes, the Paid tick, and labels on ink. |
| `forest` | `#13231E` | The mark's outlines and the one-color mark. |

Figtree is the typeface for every word in the brand, and the small labels are set in IBM Plex Mono (the site uses the system monospace). `fonts/Figtree-Variable.ttf` covers every weight, under the SIL Open Font License in `fonts/OFL.txt`.

## Using the mark

- Keep clear space of at least a quarter of the mark's height on every side.
- Use the full mark from 41 px up, or 10 mm in print, and the small mark below that.
- Use the color mark wherever it can go; the forest and white marks are for one-color printing and photos.
- Keep the mark's shape, angle and colors as drawn. Stretching, turning, recoloring or separating the notes from the card makes a different mark.

## Moving pictures

The site's films (the hero loop and one tile per reason) come from the ecashcard-film repository's `render-site.sh`; their rendered files live in `dist/media/`.

## What uses it

ecashcard.org's favicon, header, home-screen icon and social image use the mark already, and the GitHub org avatar is the same drawing on paper. The site's copies sit in `dist/` and move to these files when the site next changes. No print pieces yet: eCash Card is the projects' home, and each card's own library holds its print.

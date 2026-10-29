#!/usr/bin/env python3
"""Draws the eCash Card brand library from one set of shapes and colors: the mark (color, one-color forest and white,
and a simpler small version), the app icon and avatar, the wordmark lockups with outlined letters, the web icons and
the color tokens. Change this file, run it from the repo root and commit what it writes:

    python3 brand/generate.py

It needs fontTools and uharfbuzz (pip install fonttools uharfbuzz) and rsvg-convert (brew install librsvg).
"""
import io, json, os, struct, subprocess

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
import uharfbuzz as hb

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'fonts', 'Figtree-Variable.ttf')

NAME, WORD, DOMAIN, SLUG = 'eCash Card', ('ecash', 'card'), 'ecashcard.org', 'ecash-card'

# every color in the brand, with its use (written to tokens.json and tokens.css)
TOKENS = [
    ('paper', '#F6F3EC', 'The ground: the site, the icon and the deck.'),
    ('ink', '#17191C', 'Headings and text on paper, and "ecash" in the wordmark. Dark bands.'),
    ('body', '#3D4047', 'Body text on paper.'),
    ('muted', '#6B6F78', 'Secondary text, and "card" in the wordmark on paper.'),
    ('copper', '#B8651F', 'The accent: link underlines and small labels.'),
    ('copper-dark', '#8F4C13', 'Labels on paper (the mono kicker over each section).'),
    ('lime', '#B8E06A', 'The mark\'s card and notes, the Paid tick, and labels on ink.'),
    ('forest', '#13231E', 'The mark\'s outlines and the one-color mark.'),
    ('paper-on-ink', '#F6F3EC', 'Text on ink, and "ecash" in the dark wordmark.'),
    ('muted-on-ink', '#A9A59B', '"card" in the dark wordmark.'),
]
C = {k: v for k, v, _ in TOKENS}


# ---------------------------------------------------------------- the mark
# A chip card with three banknotes fanned up from behind it: cash, and the card that carries it. 66 x 64 units.
VB = (-1, 0, 66, 64)


def _note(tx, ty, rot, fill, stroke, small):
    if small:   # the note's outline and its central circle only, drawn heavier
        return (f'<g transform="translate({tx} {ty}) rotate({rot})"><rect x="-16" y="-10" width="32" height="20" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
                f'<circle r="4.2" fill="none" stroke="{stroke}" stroke-width="2.4"/></g>')
    return (f'<g transform="translate({tx} {ty}) rotate({rot})"><rect x="-16" y="-10" width="32" height="20" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<rect x="-13" y="-7" width="26" height="14" rx="2" fill="none" stroke="{stroke}" stroke-width="1.5"/>'
            f'<circle r="4" fill="none" stroke="{stroke}" stroke-width="1.6"/>'
            f'<circle cx="-9" r="1.3" fill="{stroke}"/><circle cx="9" r="1.3" fill="{stroke}"/></g>')


def _card(uid, fill, stroke, small):
    if small:   # the card and a plain chip, drawn heavier
        return (f'<rect x="4" y="26.5" width="56" height="35.3" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="3.6"/>'
                f'<rect x="11" y="39.2" width="13" height="10" rx="2.2" fill="{fill}" stroke="{stroke}" stroke-width="2.6"/>')
    return (f'<rect x="4" y="26.5" width="56" height="35.3" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            f'<clipPath id="{uid}c"><rect x="11" y="39.2" width="13" height="10" rx="2.2"/></clipPath>'
            f'<rect x="11" y="39.2" width="13" height="10" rx="2.2" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
            f'<path clip-path="url(#{uid}c)" d="M15.3 39.2V49.2M19.7 39.2V49.2M11 42.7H15.3M11 45.7H15.3M19.7 42.7H24M19.7 45.7H24" stroke="{stroke}" stroke-width="1.2" fill="none"/>')


def _drawing(uid, fill, stroke, small=False):
    return (_note(20, 22, -40, fill, stroke, small) + _note(29, 19, -25, fill, stroke, small)
            + _note(39, 20, -10, fill, stroke, small) + _card(uid, fill, stroke, small))


def mark(uid, color=None, small=False):
    """(defs, body) of the mark. color None: lime with forest outlines. A color: one-color line art in that color,
    the notes hidden behind the card as in the color mark (a luminance mask: outlines white, fills black)."""
    if color is None:
        return '', _drawing(uid, C['lime'], C['forest'], small)
    defs = (f'<mask id="{uid}m" maskUnits="userSpaceOnUse" x="-2" y="-2" width="70" height="68">'
            f'{_drawing(uid + "k", "#000", "#fff", small)}</mask>')
    return defs, f'<rect x="-2" y="-2" width="70" height="68" fill="{color}" mask="url(#{uid}m)"/>'


def mark_svg(uid, color=None, small=False):
    d, b = mark(uid, color, small)
    x, y, w, h = VB
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w * 4}" height="{h * 4}"><title>{NAME}</title><defs>{d}</defs>{b}</svg>\n'


def place_mark(uid, x, y, w, color=None, small=False):
    d, b = mark(uid, color, small)
    vx, vy, vw, vh = VB
    return f'<svg x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{w * vh / vw:.2f}" viewBox="{vx} {vy} {vw} {vh}" overflow="visible"><defs>{d}</defs>{b}</svg>'


def icon_svg(uid, size, share, small=False):
    """The mark on paper, centered, `share` of the side wide."""
    w = size * share; h = w * VB[3] / VB[2]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">'
            f'<rect width="{size}" height="{size}" fill="{C["paper"]}"/>{place_mark(uid, (size - w) / 2, (size - h) / 2 - size * 0.01, w, None, small)}</svg>\n')


# ---------------------------------------------------------------- type: Figtree, shaped with HarfBuzz and outlined
_inst = {}


def _font(weight):
    if weight not in _inst:
        f = instantiateVariableFont(TTFont(FONT), {'wght': weight})
        buf = io.BytesIO(); f.save(buf)
        _inst[weight] = (f, hb.Font(hb.Face(buf.getvalue())), f['head'].unitsPerEm)
    return _inst[weight]


def outline(text, weight, size, x, y, track=0.0):
    """Path data for `text` at font size `size`, its baseline starting at (x, y), letters spaced by `track` em;
    returns (d, width)."""
    f, hbf, upem = _font(weight)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties(); hb.shape(hbf, buf, {})
    glyphs, order, s, pen, adv = f.getGlyphSet(), f.getGlyphOrder(), size / upem, None, 0.0
    pen = SVGPathPen(glyphs)
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        glyphs[order[info.codepoint]].draw(TransformPen(pen, (s, 0, 0, -s, x + (adv + pos.x_offset) * s, y - pos.y_offset * s)))
        adv += pos.x_advance + track * upem
    return pen.getCommands(), adv * s - track * size


# ---------------------------------------------------------------- files
def write(rel, text):
    path = os.path.join(HERE, rel); os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(text); return path


def render(svg, rel, w=None, h=None, fmt='png'):
    path = os.path.join(HERE, rel); os.makedirs(os.path.dirname(path), exist_ok=True)
    cmd = ['rsvg-convert', '-f', fmt, '-o', path]
    if w: cmd += ['-w', str(w)]
    if h: cmd += ['-h', str(h)]
    subprocess.run(cmd + [svg], check=True); return path


def ico(rel, sources):
    """A .ico of PNG entries: sources = [(png path, size), ...]."""
    data = [open(p, 'rb').read() for p, _ in sources]
    head, off = struct.pack('<HHH', 0, 1, len(sources)), 6 + 16 * len(sources)
    entries = b''
    for (_, n), d in zip(sources, data):
        entries += struct.pack('<BBBBHHII', n % 256, n % 256, 0, 0, 1, 32, len(d), off); off += len(d)
    open(os.path.join(HERE, rel), 'wb').write(head + entries + b''.join(data))



def lockup_svg(uid, dark):
    """The mark beside the wordmark: "ecash" in Figtree 800 and "card" in 400, tracked in by 0.02 em, with the mark
    1.25 em tall and a 0.32 em gap; a quarter of the mark's height clear on every side."""
    size, track = 100.0, -0.02
    mh = 1.25 * size; mw = mh * VB[2] / VB[3]; gap = 0.32 * size; pad = mh / 4
    base = pad + mh / 2 + 0.36 * size
    tx = pad + mw + gap
    d1, w1 = outline(WORD[0], 800, size, tx, base, track)
    d2, w2 = outline(WORD[1], 400, size, tx + w1 + track * size, base, track)
    W, H = tx + w1 + track * size + w2 + pad, mh + 2 * pad
    c1, c2 = (C['paper-on-ink'], C['muted-on-ink']) if dark else (C['ink'], C['muted'])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}">'
            f'{place_mark(uid, pad, pad, mw)}<path d="{d1}" fill="{c1}"/><path d="{d2}" fill="{c2}"/></svg>\n'), W, H


def main():
    # the mark
    for name, color in (('', None), ('-forest', C['forest']), ('-white', '#FFFFFF')):
        svg = write(f'mark/{SLUG}-mark{name}.svg', mark_svg('m', color))
        render(svg, f'mark/{SLUG}-mark{name}-1024.png', w=1024)
    # below 40 px the notes' inner lines and the chip's contacts would blur: the small mark keeps outlines only
    write(f'mark/{SLUG}-mark-small.svg', mark_svg('m', None, True))
    write(f'mark/{SLUG}-mark-small-forest.svg', mark_svg('m', C['forest'], True))
    # the icon: the mark at 62% of the side on paper; square (iOS and the stores round the corners)
    icon = write(f'icon/{SLUG}-icon.svg', icon_svg('i', 1024, 0.62))
    render(icon, f'icon/{SLUG}-icon-1024.png', 1024, 1024)
    av = write(f'icon/{SLUG}-avatar.svg', icon_svg('a', 400, 0.5))
    render(av, f'icon/{SLUG}-avatar-400.png', 400, 400)
    # the wordmark
    for dark in (True, False):
        svg, W, H = lockup_svg('l', dark)
        p = write(f'lockup/{SLUG}-lockup-on-{"dark" if dark else "light"}.svg', svg)
        render(p, f'lockup/{SLUG}-lockup-on-{"dark" if dark else "light"}.png', w=int(W * 3))
    # web: the favicon is the small mark on its own, so it sits on any browser tab
    fav = write('web/favicon.svg', mark_svg('f', None, True))
    for n in (16, 32, 48):
        render(fav, f'web/.f{n}.png', n, n)
    ico('web/favicon.ico', [(os.path.join(HERE, f'web/.f{n}.png'), n) for n in (16, 32, 48)])
    os.replace(os.path.join(HERE, 'web/.f32.png'), os.path.join(HERE, 'web/favicon-32.png'))
    for n in (16, 48):
        os.remove(os.path.join(HERE, f'web/.f{n}.png'))
    for n, rel in ((180, 'web/apple-touch-icon.png'), (192, 'web/icon-192.png'), (512, 'web/icon-512.png')):
        render(icon, rel, n, n)
    # tokens
    write('tokens.json', json.dumps({'name': NAME, 'font': 'Figtree', 'labels': 'IBM Plex Mono (or the system monospace)',
                                     'colors': [{'token': k, 'value': v, 'use': u} for k, v, u in TOKENS]}, indent=2) + '\n')
    write('tokens.css', f'/* {NAME} colors (brand/generate.py writes this file) */\n:root {{\n'
          + ''.join(f'  --{k}: {v};  /* {u} */\n' for k, v, u in TOKENS)
          + '  --font: "Figtree", ui-sans-serif, system-ui, sans-serif;\n  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;\n}\n')
    print('wrote the', NAME, 'brand library in', HERE)


if __name__ == '__main__':
    main()

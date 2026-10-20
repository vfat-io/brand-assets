#!/usr/bin/env python3
"""Outline the kit's lettering into the vector masters in sources/.

    python scripts/outline.py path/to/static/fonts/og

The fonts are not distributed: use the Roboto files in the frontend's static/fonts/og/,
since other Roboto builds can change the existing masters. The builder reads only the
outlined masters.
"""

import sys
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
# Master name: font file and text, set at the glyphs' advance widths without kerning.
# Lines are left-aligned, LINE_HEIGHT em apart.
LETTERING = {
    "wordmark": ("Roboto-Black.ttf", "VFAT"),
    "domain": ("Roboto-Regular.ttf", "vfat.io"),
    "tagline": ("Roboto-Bold.ttf", "Less busywork.\nMore control."),
}
LINE_HEIGHT = 1.2


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    fonts = Path(sys.argv[1])
    for name, (font_file, text) in LETTERING.items():
        (ROOT / "sources" / f"{name}.svg").write_text(outline(fonts / font_file, text))
        print(f"Outlined {name}: {text}")


def outline(font_path, text):
    font = TTFont(font_path)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    path, bounds = SVGPathPen(glyphs), BoundsPen(glyphs)
    x = y = 0
    for character in text:
        if character == "\n":
            x, y = 0, y + LINE_HEIGHT * font["head"].unitsPerEm
            continue
        name = cmap[ord(character)]
        # Font units point up; SVG units point down.
        for pen in (path, bounds):
            glyphs[name].draw(TransformPen(pen, (1, 0, 0, -1, x, y)))
        x += font["hmtx"][name][0]
    left, top, right, bottom = bounds.bounds
    width, height = right - left, bottom - top
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" height="{height:g}" '
            f'viewBox="{left:g} {top:g} {width:g} {height:g}">'
            f'<path fill="#000000" d="{path.getCommands()}"/></svg>\n')


if __name__ == "__main__":
    main()

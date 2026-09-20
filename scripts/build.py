#!/usr/bin/env python3
"""Export the public kit from self-contained vector masters."""

import hashlib
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v1.0.0"
NS = "http://www.w3.org/2000/svg"
ASSETS = []
COLORS = {
    "black": "#000000",
    "white": "#ffffff",
    "social-background": "#121113",
    "icon-background": "#262626",
    "accent": "#009aff",
}


def main():
    for tone in ("black", "white"):
        color = COLORS[tone]
        export(f"logos/mark/vfat-mark-{tone}", 285, 285,
               shape("bird", 0, 0, 285, color), "transparent", [256, 512, 1024])
        export(f"logos/horizontal/vfat-logo-{tone}", 840, 285,
               lockup(color), "transparent", [512, 1024, 2048])

    for theme, background, foreground in (
        ("dark", COLORS["icon-background"], COLORS["white"]),
        ("light", COLORS["white"], COLORS["black"]),
    ):
        # Preserve the app icon's original bird placement and corner radius.
        original_width = 422.63
        icon = rect(original_width, original_width, background, radius=51.305)
        icon += shape("bird", 81.438, 80.834, 285 * 0.9123, foreground)
        export(f"icons/vfat-icon-{theme}", original_width, original_width,
               icon, "transparent-corners", [64, 128, 256, 512, 1024])

    for theme, background, foreground in (
        ("dark", COLORS["social-background"], COLORS["white"]),
        ("light", COLORS["white"], COLORS["black"]),
    ):
        landscape = rect(1200, 630, background)
        landscape += f'<g transform="translate(222 157) scale(0.9)">{lockup(foreground)}</g>'
        landscape += shape("domain", 542, 476, 116, foreground)
        export(f"social/vfat-social-landscape-{theme}", 1200, 630,
               landscape, background, [1200], size_suffix=False)
        square = rect(1080, 1080, background)
        square += shape("bird", 330, 196, 420, foreground)
        square += shape("wordmark", 305, 689, 470, foreground)
        square += shape("domain", 482, 932, 116, foreground)
        export(f"social/vfat-social-square-{theme}", 1080, 1080,
               square, background, [1080], size_suffix=False)

    (ROOT / "colors.json").write_text(json.dumps(COLORS, indent=2) + "\n")
    manifest = {
        "version": VERSION,
        "website": "https://vfat.io",
        "usage": "https://github.com/vfat-io/brand-assets/blob/main/USAGE.md",
        "base_url": f"https://raw.githubusercontent.com/vfat-io/brand-assets/{VERSION}/",
        "assets": sorted(ASSETS, key=lambda asset: asset["path"]),
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    preview()
    print(f"Exported {len(ASSETS)} assets and the preview sheet.")


def shape(name, x, y, width, color):
    svg = ET.parse(ROOT / "sources" / f"{name}.svg").getroot()
    left, top, source_width, _ = map(float, svg.attrib["viewBox"].split())
    scale = width / source_width
    paths = "".join(f'<path fill="{color}" d="{p.attrib["d"]}"/>'
                    for p in svg.iter(f"{{{NS}}}path"))
    return (f'<g transform="translate({x:g} {y:g}) scale({scale:.10g}) '
            f'translate({-left:g} {-top:g})">{paths}</g>')


def lockup(color):
    return shape("bird", 16, 20, 245, color) + shape("wordmark", 318, 90, 480, color)


def rect(width, height, color, radius=0):
    return f'<rect width="{width:g}" height="{height:g}" rx="{radius:g}" fill="{color}"/>'


def export(stem, width, height, body, background, png_widths, size_suffix=True):
    svg = (f'<svg xmlns="{NS}" width="{width:g}" height="{height:g}" '
           f'viewBox="0 0 {width:g} {height:g}" role="img" aria-label="VFAT">'
           f'<title>VFAT</title>{body}</svg>\n')
    path = ROOT / f"{stem}.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)
    record(path, width, height, background)
    for png_width in png_widths:
        png_height = math.floor(png_width * height / width + 0.5)
        suffix = f"-{png_width}" if size_suffix else ""
        png_path = ROOT / f"{stem}{suffix}.png"
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(png_path),
                        output_width=png_width, output_height=png_height)
        record(png_path, png_width, png_height, background)


def record(path, width, height, background):
    ASSETS.append({
        "path": str(path.relative_to(ROOT)),
        "format": path.suffix[1:],
        "width": width,
        "height": height,
        "background": background,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    })


def preview():
    # Pillow's bundled font keeps the documentation preview reproducible.
    sheet = Image.new("RGB", (1280, 1512), "#eeedef")
    draw = ImageDraw.Draw(sheet)
    title_font = ImageFont.load_default(size=36)
    label_font = ImageFont.load_default(size=20)
    draw.text((40, 32), "VFAT / BRAND ASSETS", fill="#121113", font=title_font)
    draw.text((40, 88), "Logos, app icons and social images", fill="#555555", font=label_font)
    samples = [
        ("logos/mark/vfat-mark-black-512.png", "#ffffff", "Black mark / light backgrounds"),
        ("logos/mark/vfat-mark-white-512.png", "#121113", "White mark / dark backgrounds"),
        ("logos/horizontal/vfat-logo-black-1024.png", "#ffffff", "Horizontal logo / black"),
        ("logos/horizontal/vfat-logo-white-1024.png", "#121113", "Horizontal logo / white"),
        ("icons/vfat-icon-dark-512.png", "#ffffff", "App icon / dark"),
        ("icons/vfat-icon-light-512.png", "#121113", "App icon / light"),
        ("social/vfat-social-landscape-dark.png", "#121113", "Social landscape / 1200 x 630"),
        ("social/vfat-social-square-light.png", "#ffffff", "Social square / 1080 x 1080"),
    ]
    for index, (path, background, label) in enumerate(samples):
        x, y = 40 + (index % 2) * 620, 148 + (index // 2) * 336
        tile = Image.new("RGB", (580, 272), background)
        asset = Image.open(ROOT / path).convert("RGBA")
        limit = (540, 240) if index in (2, 3, 6, 7) else (210, 210)
        asset.thumbnail(limit, Image.Resampling.LANCZOS)
        tile.paste(asset, ((580 - asset.width) // 2, (272 - asset.height) // 2), asset)
        sheet.paste(tile, (x, y))
        draw.text((x, y + 286), label, fill="#121113", font=label_font)
    (ROOT / "previews").mkdir(exist_ok=True)
    sheet.save(ROOT / "previews/brand-kit.png")


if __name__ == "__main__":
    main()

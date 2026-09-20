# Asset sources and maintenance

## Provenance

The bird artwork is taken unchanged from VFAT's frontend logo. Source snapshot: `vfat-io/vfat-io` commit `c0641a9c03363d1e74a2bfa9fc8f95bf5794c63a`, checked on 2026-09-20.

| Source in the frontend | Use in this kit |
| --- | --- |
| `src/lib/components/ui/Logo.svelte` | Bird path and original `0 0 285 285` viewBox, preserved in `sources/bird.svg` |
| `static/icon.svg` | Dark icon color, corner radius, and bird placement |
| `src/lib/server/og/brand.ts` | Social background, foreground, accent, and Roboto font family |
| `static/fonts/og/Roboto-Black.ttf` | Outlined “VFAT” in `sources/wordmark.svg` |
| `static/fonts/og/Roboto-Regular.ttf` | Outlined “vfat.io” in `sources/domain.svg` |

The horizontal composition, light icon, and neutral social layouts were prepared for this kit. They reuse the existing bird and typography; the bird was not redrawn. The outlined lettering was produced using fontTools 4.59.2. No font binaries or frontend application code are distributed in the kit. The public SVG masters are sufficient to reproduce all exports, without access to the frontend repository.

## Rebuild

Requires Python 3.10+ and the Cairo system library (for example, `libcairo2` on Debian/Ubuntu). The initial release was exported on Linux with Python 3.12 and Cairo 1.18.0. Raster checksums can differ across Cairo or dependency versions.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
```

Edit the vector masters in `sources/` or the layouts in `scripts/build.py`, then rebuild. All public SVG lettering must remain outlined, and SVGs must not require scripts, external images, or external fonts. The builder writes the public SVG/PNG assets, the README preview, `colors.json`, and `manifest.json`.

Review the preview sheet at `previews/brand-kit.png`, check transparency and dimensions, and inspect changes before publishing. Keep existing version tags unchanged. For a new release, update `VERSION` in the builder and the versioned examples in the README, regenerate assets, and publish a new tag.

The release ZIP contains `README.md`, `USAGE.md`, `LICENSE.md`, `SOURCES.md`, `colors.json`, `manifest.json`, and the `logos/`, `icons/`, `social/`, `sources/`, and `previews/` directories. The GitHub source archive additionally contains the export script and dependency list.

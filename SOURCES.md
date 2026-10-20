# Asset sources and maintenance

## Provenance

The bird artwork is taken unchanged from VFAT's frontend logo. Source snapshot: `vfat-io/vfat-io` commit `c0641a9c03363d1e74a2bfa9fc8f95bf5794c63a`, checked on 2026-09-20.

| Source in the frontend | Use in this kit |
| --- | --- |
| `src/lib/components/ui/Logo.svelte` | Bird path and original `0 0 285 285` viewBox, preserved in `sources/bird.svg` |
| `static/icon.svg` | Dark icon color, corner radius, and bird placement |
| `src/lib/server/og/brand.ts` | Social background, foreground, and Roboto font family |
| `static/fonts/og/Roboto-Black.ttf` | Outlined “VFAT” in `sources/wordmark.svg` |
| `static/fonts/og/Roboto-Regular.ttf` | Outlined “vfat.io” in `sources/domain.svg` |
| `static/fonts/og/Roboto-Bold.ttf` | Outlined X banner tagline in `sources/tagline.svg` |

The horizontal composition, light icon, neutral social layouts, and X banner were prepared for this kit. They reuse the existing bird and typography; the bird was not redrawn. The banner's tagline, “Less busywork. More control.”, is the closing line of VFAT's product tour. `scripts/outline.py` produces the outlined lettering with fontTools 4.59.2. No font binaries or frontend application code are distributed in the kit. The public SVG masters are sufficient to reproduce all exports, without access to the frontend repository.

The colors added in version 1.1.0 were checked at `vfat-io/vfat-io` commit `323131dcc78ac9c9ac54993dc785c7ba2e4ccb93` on 2026-10-20. Blue is the app's `--primary-solid` and Light blue its dark-theme `--primary`, both in `src/lib/styles/theme.css`. The dark and light backgrounds are the app's `browserThemeColors` (`src/lib/styles/browserThemeColors.ts`). Version 1.0.0 listed `#009AFF`, the link-preview cards' accent at the time, as the accent; the app's blues replace it.

## Rebuild

Requires Python 3.10+ and the Cairo system library (for example, `libcairo2` on Debian/Ubuntu). The initial release was exported on Linux with Python 3.12 and Cairo 1.18.0. Raster checksums can differ across Cairo or dependency versions.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
```

Edit the vector masters in `sources/` or the layouts in `scripts/build.py`, then rebuild. All public SVG lettering must remain outlined, and SVGs must not require scripts, external images, or external fonts. The builder writes the public SVG/PNG assets, the README preview, `colors.json`, `colors.css`, and `manifest.json`.

To change lettering, such as the banner's tagline, edit `LETTERING` in `scripts/outline.py`. Then outline it from the frontend's `static/fonts/og/` directory and rebuild:

```sh
.venv/bin/python scripts/outline.py path/to/static/fonts/og
.venv/bin/python scripts/build.py
```

The outliner rewrites every lettering master. With the frontend's font files, the unchanged ones come out byte-identical; other Roboto builds can change them. The banner scales its tagline to fit its box, so check the banner after a longer or shorter line.

Review the preview sheet at `previews/brand-kit.png`, check transparency and dimensions, and inspect changes before publishing. The Build workflow rebuilds every pull request on Ubuntu 24.04 and fails if the committed assets differ from the build, so commit the rebuilt files with each change.

## Release

Update `VERSION` in the builder and the versioned links in the README, rebuild, and merge. Then push the matching tag from `main`, for example `git tag v1.1.0 && git push origin v1.1.0`. The Release workflow checks the tag against `VERSION`, rebuilds, and packages the ZIP and `SHA256SUMS.txt` with `scripts/package.py`. It attaches them to a draft release: write the notes and publish it. Keep existing version tags unchanged.

The release ZIP contains `README.md`, `USAGE.md`, `LICENSE.md`, `SOURCES.md`, `colors.json`, `colors.css`, `manifest.json`, and the `logos/`, `icons/`, `social/`, `sources/`, and `previews/` directories. The GitHub source archive additionally contains the scripts, the workflows, and the dependency list.

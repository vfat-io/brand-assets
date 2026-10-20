#!/usr/bin/env python3
"""Package the committed kit as the release ZIP and its checksum file in dist/.

    python scripts/package.py

Entries carry the commit time of HEAD, so a commit always packages to the same bytes.
"""

import hashlib
import subprocess
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "vfat-brand-assets"
CONTENTS = ["README.md", "USAGE.md", "LICENSE.md", "SOURCES.md", "colors.json", "colors.css",
            "manifest.json", "logos", "icons", "social", "sources", "previews"]


def main():
    paths = git("ls-files", "-z", "--", *CONTENTS).split("\0")[:-1]
    stamp = time.gmtime(int(git("log", "-1", "--format=%ct")))[:6]
    archive = ROOT / "dist" / f"{NAME}.zip"
    archive.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive, "w") as bundle:
        for path in sorted(paths):
            entry = zipfile.ZipInfo(f"{NAME}/{path}", stamp)
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            bundle.writestr(entry, (ROOT / path).read_bytes(), compresslevel=9)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (archive.parent / "SHA256SUMS.txt").write_text(f"{digest}  {archive.name}\n")
    print(f"Packaged {len(paths)} files: {digest}  {archive.relative_to(ROOT)}")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True,
                          text=True).stdout.strip("\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Write WebP copies of the page images at the widths build.py offers in srcset, into assets/img/sized/.

Usage: python3 _src/images.py
Run it after adding or changing a JPEG in assets/img; unchanged images are skipped.
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
OUT = IMG / "sized"
WIDTHS = (200, 320, 480, 640, 800, 960)
# 70 is where Lighthouse stops reporting "increase the compression"; at that level the covers' small text stays sharp.
QUALITY = 70
SETTINGS = OUT / ".settings"
# og.jpg is only read by social networks, which want the full JPEG.
SKIP = {"og.jpg"}


def sized_name(rel, width):
    return rel.with_suffix("").as_posix().replace("/", "--") + f"-{width}.webp"


def targets(source):
    width = Image.open(source).width
    return [w for w in WIDTHS if w < width] + [width]


def main():
    OUT.mkdir(exist_ok=True)
    settings = f"widths={WIDTHS} quality={QUALITY}\n"
    # New widths or quality make every existing copy stale, whatever its date.
    fresh = SETTINGS.exists() and SETTINGS.read_text() == settings
    written = skipped = 0
    expected = set()
    for source in sorted(IMG.rglob("*.jpg")):
        rel = source.relative_to(IMG)
        if rel.parts[0] == "sized" or rel.name in SKIP:
            continue
        image = None
        for width in targets(source):
            out = OUT / sized_name(rel, width)
            expected.add(out)
            if fresh and out.exists() and out.stat().st_mtime >= source.stat().st_mtime:
                skipped += 1
                continue
            image = image or Image.open(source).convert("RGB")
            height = round(image.height * width / image.width)
            image.resize((width, height), Image.LANCZOS).save(out, "WEBP", quality=QUALITY, method=6)
            written += 1
    stale = [p for p in OUT.glob("*.webp") if p not in expected]
    for p in stale:
        p.unlink()
    SETTINGS.write_text(settings)
    print(f"immagini webp: {written} scritte, {skipped} già aggiornate, {len(stale)} rimosse, {len(expected)} attese")
    return 0 if written + skipped == len(expected) else 1


if __name__ == "__main__":
    sys.exit(main())

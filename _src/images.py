#!/usr/bin/env python3
"""Write AVIF and WebP copies of the page images at the widths build.py offers in srcset, into assets/img/sized/.

Usage: python3 _src/images.py
Run it after adding or changing a JPEG in assets/img; unchanged images are skipped.
"""
import io
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
OUT = IMG / "sized"
WIDTHS = (200, 320, 480, 640, 800, 960)
# 70 is where Lighthouse stops reporting "increase the compression"; at that level the covers' small text stays sharp.
WEBP_QUALITY = 70
# PageSpeed and DevTools measure an image's drawn size without the phone's pixel ratio (Lighthouse issue #17080), so on
# their 1.75x phone every correctly sized copy looks at least 1 - 1/1.75^2 = 67% too big, and up to 82% just past a
# breakpoint. They report it once that "waste" passes 12,288 bytes, which 14 KB can never reach: every AVIF a phone can
# pick (up to 800 px) gets the best quality that fits in it. A copy that cannot fit even at the lowest quality keeps the
# best one instead; check_sizes.py then checks what PageSpeed's phone really loads on each page.
AVIF_PHONE_BYTES = 14_000
AVIF_PHONE_WIDTH = 800
AVIF_QUALITIES = (60, 55, 50, 45, 40, 35, 30)
AVIF_SPEED = 4
SETTINGS = OUT / ".settings"  # bump the text below to force a full rewrite
# og.jpg is only read by social networks, which want the full JPEG.
SKIP = {"og.jpg"}


def sized_name(rel, width, ext):
    return rel.with_suffix("").as_posix().replace("/", "--") + f"-{width}.{ext}"


def targets(source):
    width = Image.open(source).width
    return [w for w in WIDTHS if w < width] + [width]


def encode_avif(image, width):
    """The highest quality that fits the phone budget; above the phone widths the best listed quality."""
    best = None
    for quality in AVIF_QUALITIES:
        out = io.BytesIO()
        image.save(out, "AVIF", quality=quality, speed=AVIF_SPEED)
        best = best or out.getvalue()
        if width > AVIF_PHONE_WIDTH or len(out.getvalue()) <= AVIF_PHONE_BYTES:
            return out.getvalue(), quality, True
    return best, AVIF_QUALITIES[0], False


def main():
    OUT.mkdir(exist_ok=True)
    settings = (f"widths={WIDTHS} webp={WEBP_QUALITY} avif={AVIF_QUALITIES} speed={AVIF_SPEED} "
                f"phone={AVIF_PHONE_BYTES}@{AVIF_PHONE_WIDTH} fallback=best\n")
    # New widths or qualities make every existing copy stale, whatever its date.
    fresh = SETTINGS.exists() and SETTINGS.read_text() == settings
    written = skipped = 0
    over_budget = []
    expected = set()
    for source in sorted(IMG.rglob("*.jpg")):
        rel = source.relative_to(IMG)
        if rel.parts[0] == "sized" or rel.name in SKIP:
            continue
        image = None
        for width in targets(source):
            outs = {ext: OUT / sized_name(rel, width, ext) for ext in ("avif", "webp")}
            expected.update(outs.values())
            if fresh and all(o.exists() and o.stat().st_mtime >= source.stat().st_mtime for o in outs.values()):
                skipped += 2
                continue
            image = image or Image.open(source).convert("RGB")
            resized = image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)
            resized.save(outs["webp"], "WEBP", quality=WEBP_QUALITY, method=6)
            data, quality, fits = encode_avif(resized, width)
            outs["avif"].write_bytes(data)
            if not fits:
                over_budget.append(f"{outs['avif'].name} ({len(data)} byte a qualità {quality})")
            written += 2
    stale = [p for p in OUT.iterdir() if p.suffix in (".webp", ".avif") and p not in expected]
    for p in stale:
        p.unlink()
    SETTINGS.write_text(settings)
    print(f"immagini avif+webp: {written} scritte, {skipped} già aggiornate, {len(stale)} rimosse, {len(expected)} attese")
    for item in over_budget:
        print("   non entra nel limite per i telefoni, tenuta alla qualità piena:", item)
    return 0 if written + skipped == len(expected) else 1


if __name__ == "__main__":
    sys.exit(main())

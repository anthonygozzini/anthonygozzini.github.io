#!/usr/bin/env python3
"""Cut the Geist fonts down to what the site draws, for build.py to embed in every page.

Usage: python3 _src/fonts.py
Reads the full variable fonts from Vercel's "geist" npm package (1.7.2) in _src/fonts/ and writes geist-sans.woff2
(weights 400-600) and geist-mono.woff2
(weight 500) next to them, plus coverage.txt with every character they contain, which check.py compares with the pages.
Embedding the fonts is what keeps text from moving: nothing to download, nothing to swap, nothing for Chrome to wait for.
"""
import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = Path(__file__).resolve().parent / "fonts"
BASIC = "".join(map(chr, range(0x20, 0x7F)))
ACCENTED = "àáâäçèéêëìíîïñòóôöùúûüÀÁÈÉÌÍÒÓÙÚÇßœŒ©®°·«»€"
PUNCTUATION = "\u00a0\u2013\u2014\u2018\u2019\u201c\u201d\u2022\u2026\u203a"
# The arrows the copy uses. Google's "latin" cut of Geist lacks them, and every one missing sent Chrome looking through the
# system fonts: that search was 10 of the 14 ms of the home page's first layout on PageSpeed's phone.
ARROWS = "\u2190\u2191\u2192\u2193\u2197\u25b6"
# (source, output, weight range kept, characters). The mono face only draws shortcut digits and language codes.
FACES = [
    ("Geist-Variable.woff2", "geist-sans.woff2", (400, 600), BASIC + ACCENTED + PUNCTUATION + ARROWS),
    ("GeistMono-Variable.woff2", "geist-mono.woff2", 500, "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ "),
]


def cut(source, weights, text):
    # Characters first, then weights: the full font's variation data breaks the subsetter once the axis is limited.
    font = TTFont(FONTS / source)
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "liga", "calt"]
    subsetter = subset.Subsetter(options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    font = instancer.instantiateVariableFont(font, {"wght": weights})
    covered = "".join(sorted(chr(c) for c in font.getBestCmap()))
    out = io.BytesIO()
    font.flavor = "woff2"
    font.save(out)
    return out.getvalue(), covered


ROOT = FONTS.parent.parent
FAVICON = ROOT / "assets" / "favicon.svg"
# The "AG" mark: 24 px Geist semibold, centred on x = 32 with its baseline at y = 41, in a 64 px dark tile.
MARK = {"text": "AG", "size": 24, "weight": 600, "center": 32, "baseline": 41}


def pair_kerning(font, left, right):
    """The kern feature's adjustment between two glyphs (pair positioning, formats 1 and 2)."""
    gpos = font["GPOS"].table
    indices = {i for record in gpos.FeatureList.FeatureRecord if record.FeatureTag == "kern"
               for i in record.Feature.LookupListIndex}
    for index in sorted(indices):
        lookup = gpos.LookupList.Lookup[index]
        for sub in lookup.SubTable:
            sub = getattr(sub, "ExtSubTable", sub)
            if getattr(sub, "LookupType", lookup.LookupType) != 2 or left not in sub.Coverage.glyphs:
                continue
            if sub.Format == 1:
                pairs = sub.PairSet[sub.Coverage.glyphs.index(left)].PairValueRecord
                for pair in pairs:
                    if pair.SecondGlyph == right:
                        return getattr(pair.Value1, "XAdvance", 0) or 0
            else:
                first = sub.ClassDef1.classDefs.get(left, 0)
                second = sub.ClassDef2.classDefs.get(right, 0)
                value = sub.Class1Record[first].Class2Record[second].Value1
                advance = getattr(value, "XAdvance", 0) if value else 0
                if advance:
                    return advance
            break
    return 0


def write_favicon():
    """The favicon's letters as outlines: an SVG image cannot use the page's fonts, so <text> made Chrome search the
    system fonts on every page load (a 9-17 ms main-thread layout, PageSpeed's "unattributable" long task)."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    font = instancer.instantiateVariableFont(TTFont(FONTS / "Geist-Variable.woff2"), {"wght": MARK["weight"]})
    cmap, glyphs = font.getBestCmap(), font.getGlyphSet()
    names = [cmap[ord(c)] for c in MARK["text"]]
    scale = MARK["size"] / font["head"].unitsPerEm
    advances = [font["hmtx"][n][0] for n in names]
    kerns = [pair_kerning(font, a, b) for a, b in zip(names, names[1:])] + [0]
    width = sum(advances) + sum(kerns)
    x = MARK["center"] / scale - width / 2
    paths = []
    for name, advance, kern in zip(names, advances, kerns):
        pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x * scale, MARK["baseline"])))
        paths.append(pen.getCommands())
        x += advance + kern
    FAVICON.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#121417"/>'
                       f'<path fill="#ffffff" d="{" ".join(paths)}"/></svg>\n', encoding="utf-8")
    return width * scale, sum(kerns) * scale


def main():
    coverage = {}
    for source, output, weights, text in FACES:
        data, covered = cut(source, weights, text)
        (FONTS / output).write_bytes(data)
        coverage[output] = covered
        missing = sorted(set(text) - set(covered))
        print(f"{output}: {len(data)} byte, {len(covered)} caratteri" + (f", assenti nel font: {''.join(missing)}" if missing else ""))
    width, kern = write_favicon()
    print(f"favicon.svg: lettere in tracciati, larghezza {width:.2f} px, crenatura {kern:.3f} px")
    (FONTS / "coverage.txt").write_text("".join(f"{name}\t{chars}\n" for name, chars in coverage.items()), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

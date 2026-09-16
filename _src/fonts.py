#!/usr/bin/env python3
"""Cut the Geist fonts down to what the site draws, for build.py to embed in every page.

Usage: python3 _src/fonts.py
Reads the Google Fonts "latin" files in _src/fonts/ and writes geist-sans.woff2 (weights 400-600) and geist-mono.woff2
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
PUNCTUATION = "\u00a0\u2013\u2014\u2018\u2019\u201c\u201d\u2022\u2026\u203a\u2191\u2193"
# (source, output, weight range kept, characters). The mono face only draws shortcut digits and language codes.
FACES = [
    ("geist-latin.woff2", "geist-sans.woff2", (400, 600), BASIC + ACCENTED + PUNCTUATION),
    ("geist-mono-latin.woff2", "geist-mono.woff2", 500, "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ "),
]


def cut(source, weights, text):
    font = instancer.instantiateVariableFont(TTFont(FONTS / source), {"wght": weights})
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["kern", "liga", "calt"]
    subsetter = subset.Subsetter(options)
    subsetter.populate(text=text)
    subsetter.subset(font)
    covered = "".join(sorted(chr(c) for c in font.getBestCmap()))
    out = io.BytesIO()
    font.flavor = "woff2"
    font.save(out)
    return out.getvalue(), covered


def main():
    coverage = {}
    for source, output, weights, text in FACES:
        data, covered = cut(source, weights, text)
        (FONTS / output).write_bytes(data)
        coverage[output] = covered
        missing = sorted(set(text) - set(covered))
        print(f"{output}: {len(data)} byte, {len(covered)} caratteri" + (f", assenti nel font: {''.join(missing)}" if missing else ""))
    (FONTS / "coverage.txt").write_text("".join(f"{name}\t{chars}\n" for name, chars in coverage.items()), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

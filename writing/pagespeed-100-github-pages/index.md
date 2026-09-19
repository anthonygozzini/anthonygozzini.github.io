# Getting 100 in every PageSpeed category on GitHub Pages

By Anthony Gozzini · Published 19 Sep 2026 · 5 min read

> Fonts, one image and a cache I don't control. What each fix cost in milliseconds, and the three items nobody can fix from a repository.

This site is plain HTML. A Python script turns one content file into pages, and GitHub Pages serves them for free. Nothing about it is heavy. Reaching 100 in every PageSpeed category still took a week of evenings, because most of what held it back was invisible until I measured it.

The rule I set myself was simple: no insight left unread. A green score with a list of warnings under it is a score I don't trust.

## The fonts took three attempts

The site is set in Geist. Preloading it was the obvious first move, and the worst: Chrome holds the first paint while a preloaded font is in flight, up to its own 1.5-second cap. The page appeared when the font did.

A normal stylesheet link was worse in a different way. The text painted immediately in a fallback face and then jumped when Geist arrived: a layout shift of 0.317 on a page where nothing had ever moved.

Putting the font inside the CSS as a data URI fixed both, and added a third problem: 14 KB of the stylesheet were now bytes no rule referenced, which Lighthouse counts as unused CSS.

What finally worked: cut the two faces down to the characters the site actually draws, 13.8 KB and 2.3 KB, and hand them to the page as data blocks in script tags the browser never compiles. A three-line script turns each block into a FontFace before the first layout. The same bytes as a regular script were a 50 to 78 ms long task; as data blocks they cost nothing.

One detail I didn't see coming: the arrows in the copy are missing from Google's Latin cut of Geist, and every missing character sent Chrome hunting through the system fonts. That search was 10 of the 14 ms of the home page's first layout. Vercel's own package has the arrows.

## One image decides the LCP

On every page the largest element is a cover image. Served from a CDN it needs a second connection before it can even start: on PageSpeed's phone that was 0.7 s of extra LCP, on its desktop 0.5 s. Served from GitHub Pages it lands in the caching report instead.

So the one size both of PageSpeed's screens need travels inside the HTML as an AVIF, and the larger copies stay on the CDN for dense screens. The page carries its own most important pixels; everything else is still fetched only when a browser needs it.

## The cache I don't control

GitHub Pages sends the same ten-minute cache for every file and offers no way to change it. Ten minutes is short enough that PageSpeed asks for a longer one on every static file.

Files that are committed now travel through a CDN with the commit written into the URL, which makes them immutable for a year. The page itself keeps its ten minutes, because that is the file I actually want re-fetched.

## Each page gets only the CSS it can use

Every page carries its own stylesheet, cut to the rules that can match what is on it. Cutting styles by hand is how sites break quietly, so the build does it and a second script proves it: it opens every page in a headless browser, on three screen sizes, in four states, once with the cut stylesheet and once with the full one, and compares every computed property of every element and pseudo-element. On the last run that was 356,148 values and zero differences.

## The long task was the favicon

PageSpeed kept reporting a long task it could only label "unattributable". It was the favicon: an SVG with a text element in it. An SVG can't use the page's fonts, so on every load the browser went looking through the system ones, 9 to 17 ms of it. Now those two letters are outlines, drawn by the same script that cuts the fonts.

The saved theme and the time-of-day greeting moved out of the parsing task for the same reason. Reading them from local storage while the page was being parsed was enough to push that task past 50 ms.

## What a repository can't fix

Some items stay open and always will. A content security policy, HSTS, COOP, X-Frame-Options and Trusted Types are all response headers, and GitHub Pages doesn't let you send any. Fixing them means a domain of my own and a service in front of the site. The CDN is also flagged, correctly, as a third party, and one browser-support item counts against any use of FontFace at all.

I'd rather say that out loud than pretend the list is empty.

## The part worth copying

Not the tricks: the checks. One command rebuilds the site, confirms the output matches what is committed, then verifies every internal link, every description, the structured data, the markdown copies, the pinned CDN files and the embedded fonts. The style check compares computed values. A third script measures what PageSpeed's phone would really download for each image, because Lighthouse ignores pixel density when it decides an image is too big. Then Lighthouse runs on all 27 pages, phone and desktop: 54 runs, 100 everywhere.

The site and all of it are [in the open](https://github.com/anthonygozzini/anthonygozzini.github.io). A number you have checked is worth more than a number you hope for.

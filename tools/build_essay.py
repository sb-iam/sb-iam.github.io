#!/usr/bin/env python3
"""Build a site essay page from a Markdown source.

Usage:
  build_essay.py SOURCE.md OUT_DIR --series "Open Ecosystem" --part "Part 1 of 6" \
      --date "Aug 20, 2026" --slug golden-era-open-ecosystem [--css-version 20260820p]

Conventions in the Markdown source:
  # Title                      -> <h1> and <title>
  *dek line*                   -> first italic-only paragraph after the H1 becomes the dek
  ## 2. Section                -> H2 sections; the on-page rail is generated from them
  ![F3 — caption](diagrams/F3-x.svg)   -> inline SVG figure (file read relative to SOURCE)
  *italic line right after a figure*    -> appended to that figure's caption
  > pull quote                 -> site pull-quote blockquote
  | tables |                   -> wrapped in .table-wrap
  ```fences```                 -> .essay-code panels
  ## References                -> everything after it is wrapped in .references
  A final paragraph starting "Next:" or "Next in the series" -> .next-in-series
Figures whose filename contains "F3" get the hero-figure class.
"""
import argparse
import html
import pathlib
import re
import sys

import markdown

HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{description}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <title>{title} - Shakthi Bachala</title>
  <script>
    (function () {{
      try {{ var savedTheme = localStorage.getItem("sb-theme"); document.documentElement.dataset.theme = savedTheme === "light" ? "light" : "dark"; }}
      catch (error) {{ document.documentElement.dataset.theme = "dark"; }}
    }})();
  </script>
  <link rel="stylesheet" href="../../styles.css?v={css_version}">
</head>
<body>
  <a class="skip-link" href="#article">Skip to article</a>
  <div class="site-shell">
    <header class="site-header">
      <a class="brand" href="/" aria-label="Shakthi Bachala home"><span class="brand-mark">SB</span><span>Shakthi Bachala</span></a>
      <nav class="site-nav" aria-label="Primary navigation"><a href="/#about">About</a><a href="/#experience">Experience</a><a href="/research-statement/">Research</a><a href="/#publications">Publications</a><a href="/#blog" aria-current="page">Blog</a><a href="/#contact">Contact</a></nav>
      <button class="theme-toggle" type="button" data-theme-toggle aria-label="Switch to white theme" aria-pressed="false"><span class="theme-swatch" aria-hidden="true"></span><span data-theme-label>White</span></button>
    </header>
    <main id="article"><article>
      <header class="hero article-hero writing-article-hero"><div class="signal-grid" aria-hidden="true"></div><div class="hero-copy"><div class="article-meta"><span>{series}</span><span>{part}</span><span>{date}</span></div><h1>{title}</h1><p class="dek">{dek}</p></div></header>
      <div class="article-layout"><aside class="article-rail"><nav aria-label="On this page"><p>On this page</p><ol>
{rail}
      </ol></nav></aside><div class="article-body">
"""

FOOTER = """
      </div></div>
    </article></main>
    <footer class="site-footer"><span>Shakthi Bachala</span><span>{series} · {part}</span><span>2026</span></footer>
  </div>
  <script src="/theme.js?v=20260820m" defer></script>
</body>
</html>
"""


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def inline_svg(path: pathlib.Path) -> str:
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg)
    # Drop fixed pixel width/height on the root so CSS controls layout.
    m = re.match(r"(\s*<svg\b)([^>]*)(>)", svg, flags=re.S)
    if m:
        attrs = re.sub(r'\s(width|height)="[^"]*"', "", m.group(2))
        if "width=" not in attrs:
            attrs += ' width="100%"'
        svg = m.group(1) + attrs + m.group(3) + svg[m.end():]
    return svg.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("out_dir")
    ap.add_argument("--series", required=True)
    ap.add_argument("--part", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--css-version", default="20260820p")
    args = ap.parse_args()

    src = pathlib.Path(args.source).resolve()
    text = src.read_text(encoding="utf-8")
    text = re.sub(r"^\s*<!--.*?-->\s*", "", text, count=1, flags=re.S)  # leading source note

    lines = text.splitlines()
    title = None
    dek = ""
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            body_start = i + 1
            break
    if title is None:
        sys.exit("no H1 title found")
    j = body_start
    while j < len(lines) and not lines[j].strip():
        j += 1
    if j < len(lines):
        m = re.fullmatch(r"\*(.+)\*", lines[j].strip())
        if m and not lines[j].strip().startswith("*["):
            dek = m.group(1).strip()
            j += 1
    body_md = "\n".join(lines[j:])

    # Figures: replace image syntax with a token, remember file + caption.
    figures = {}

    def fig_sub(m):
        alt, rel = m.group(1), m.group(2)
        key = f"@@FIG{len(figures)}@@"
        figures[key] = {"alt": alt.strip(), "path": (src.parent / rel).resolve(), "extra": ""}
        return "\n\n" + key + "\n\n"

    body_md = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", fig_sub, body_md)
    # Italic line directly after a figure -> caption continuation.
    for key in list(figures):
        pat = re.compile(re.escape(key) + r"\n+\*([^*\n][^\n]*)\*[ \t]*\n")
        m = pat.search(body_md)
        if m:
            figures[key]["extra"] = m.group(1).strip()
            body_md = body_md[: m.start()] + key + "\n" + body_md[m.end():]

    md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "md_in_html"], output_format="html5")
    out = md.convert(body_md)

    # Headings: ids + rail.
    rail = []

    def h2_sub(m):
        inner = m.group(1)
        sid = slugify(inner)
        label = re.sub(r"^\s*\d+\.\s*", "", inner)  # the <ol> supplies the number
        rail.append(f'        <li><a href="#{sid}">{label}</a></li>')
        return f'<h2 id="{sid}">{inner}</h2>'

    out = re.sub(r"<h2>(.*?)</h2>", h2_sub, out, flags=re.S)

    # Figures -> <figure>
    for key, f in figures.items():
        if not f["path"].exists():
            sys.exit(f"missing figure file: {f['path']}")
        # Caption: the italic line after the figure wins; the alt text is the fallback.
        text = f["extra"] or f["alt"]
        label, dash, cap = text.partition("—")
        if dash and len(label.strip()) <= 4:
            caption = f"<strong>{html.escape(label.strip())}</strong> {html.escape(cap.strip())}"
        else:
            caption = html.escape(text)
        cls = "article-figure hero-figure" if "F3" in f["path"].name else "article-figure"
        fig_html = f'<figure class="{cls}">\n{inline_svg(f["path"])}\n<figcaption>{caption}</figcaption>\n</figure>'
        out = out.replace(f"<p>{key}</p>", fig_html).replace(key, fig_html)

    # Tables, code, lead, references, next-in-series.
    out = re.sub(r"<table>", '<div class="table-wrap"><table>', out)
    out = re.sub(r"</table>", "</table></div>", out)
    out = re.sub(r"<pre><code([^>]*)>", r'<div class="essay-code"><pre><code\1>', out)
    out = re.sub(r"</code></pre>", "</code></pre></div>", out)
    out = re.sub(r"^<p>", '<p class="lead">', out, count=1)
    m = re.search(r'<h2 id="references[^"]*">', out)
    if m:
        out = out[: m.start()] + '<section class="references">\n' + out[m.start():] + "\n</section>"
    out = re.sub(r"<p>(<em>)?(Next(?: in the series)?:)", r'<p class="next-in-series">\1\2', out)
    nxt = re.search(r'<p class="next-in-series">.*?</p>\n?', out, flags=re.S)
    refs = out.find('<section class="references">')
    if nxt and refs != -1 and nxt.start() > refs:
        block = nxt.group(0)
        out = out[: nxt.start()] + out[nxt.end():]
        refs = out.find('<section class="references">')
        out = out[:refs] + block + out[refs:]
    # External links open in a new tab, like the rest of the site.
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" target="_blank" rel="noreferrer"', out)

    description = html.escape(dek or title, quote=True)
    page = HEADER.format(
        title=html.escape(title, quote=True), description=description, css_version=args.css_version,
        series=html.escape(args.series), part=html.escape(args.part), date=html.escape(args.date),
        dek=html.escape(dek), rail="\n".join(rail),
    ) + out + FOOTER.format(series=html.escape(args.series), part=html.escape(args.part))

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(page, encoding="utf-8")
    words = len(re.sub(r"<[^>]+>", " ", out).split())
    print(f"wrote {out_dir / 'index.html'}: {len(page):,} bytes, ~{words:,} words, {len(rail)} sections, {len(figures)} figures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build deliverable.pdf from deliverable.md: pandoc -> HTML with embedded fonts and images -> Chromium.

Adapted from build_pdf.py (the protocol builder) and independent of it. Run it from this folder:
    nix shell nixpkgs#pandoc nixpkgs#chromium nixpkgs#qpdf -c python3 build_deliverable_pdf.py
The fonts (Source Sans 3, Source Serif 4, IBM Plex Mono) come from nixpkgs through `nix build`.
qpdf corrects the titles of the PDF's bookmarks. The intermediate files go to a temporary folder.
"""
import base64
import html
import json
import mimetypes
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / "deliverable.md", HERE / "deliverable.pdf"
RUNNING_HEAD = "Evaluación de Vulnerabilidades Web · OWASP Juice Shop"


def run(*cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def text_of(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


# --- fonts: the protocol's text families, embedded so that Chromium needs no installed fonts.
# Chromium embeds .ttf files as real fonts but turns .otf (CFF) files into Type 3 drawings, which some
# viewers render poorly; nixpkgs has Source Code Pro only as .otf, so code uses IBM Plex Mono (.ttf).
FACES = [  # family, file name without extension, weight, style
    ("Source Sans 3", "SourceSans3-Regular", 400, "normal"),
    ("Source Sans 3", "SourceSans3-It", 400, "italic"),
    ("Source Sans 3", "SourceSans3-Semibold", 600, "normal"),
    ("Source Sans 3", "SourceSans3-Bold", 700, "normal"),
    ("Source Sans 3", "SourceSans3-BoldIt", 700, "italic"),
    ("Source Serif 4", "SourceSerif4-Semibold", 600, "normal"),
    ("Source Serif 4", "SourceSerif4-SemiboldIt", 600, "italic"),
    ("IBM Plex Mono", "IBMPlexMono-Regular", 400, "normal"),
    ("IBM Plex Mono", "IBMPlexMono-SemiBold", 600, "normal"),
]
STORES = run("nix", "build", "--no-link", "--print-out-paths",
             "nixpkgs#source-sans", "nixpkgs#source-serif", "nixpkgs#ibm-plex").split()


def font_src(name):
    for ext, fmt in (("ttf", "truetype"), ("otf", "opentype")):
        for store in STORES:
            for path in sorted(Path(store).rglob(f"{name}.{ext}")):
                return f'url(data:font/{ext};base64,{base64.b64encode(path.read_bytes()).decode()}) format("{fmt}")'
    sys.exit(f"font {name} not found in {STORES}")


fonts = "\n".join(f'@font-face {{ font-family: "{family}"; font-weight: {weight}; font-style: {style}; '
                  f"src: {font_src(name)}; }}" for family, name, weight, style in FACES)

# --- markdown -> HTML. commonmark_x reads the file the way GitHub and the VS Code preview show it:
# a list may follow a line without a blank line in between, and "Probabilidad \ Impacto" keeps its backslash.
# implicit_figures turns an image alone in its paragraph into a figure captioned with its alt text.
body = run("pandoc", str(SRC), "-f", "commonmark_x+implicit_figures", "-t", "html5", "--wrap=none")

# pandoc writes each letter of a formula's words in its own <em>: join them into whole words
body = re.sub(r'<span class="math[^"]*">.*?</span>', lambda m: m[0].replace("</em><em>", ""), body, flags=re.S)


# links point to evidence files in this folder or to localhost, which a reader of the PDF cannot open: keep the text
def unlink(m):
    return m[0] if re.match(r"https?://(?!localhost|127\.)", m[1]) else m[2]


body = re.sub(r'<a href="([^"]*)"[^>]*>(.*?)</a>', unlink, body, flags=re.S)


# the text cites screenshots by file name, so each caption names its file; then the image is embedded
def name_file(m):
    src = re.search(r'<img src="([^"]+)"', m[0])[1]
    return m[0].replace("</figcaption>", f' <span class="file">{src}</span></figcaption>')


def embed(m):
    path = HERE / m[1]
    mime = mimetypes.guess_type(path.name)[0]
    return f'<img src="data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"'


body = re.sub(r"<figure>.*?</figure>", name_file, body, flags=re.S)
body = re.sub(r'<img src="(?!data:)([^"]+)"', embed, body)
assert not re.search(r'<img(?![^>]*src="data:)', body), "an image was not embedded"

# --- the report's own risk levels get one color each: severity summary, risk bands, matrix and findings table
SEVERITY = {"Crítica": "crit", "Alta": "high", "Media": "med", "Baja": "low", "Informativa": "info"}
LEVEL = {"Crítico": "crit", "Alto": "high", "Medio": "med", "Bajo": "low"}


def color_cells(table, cols):
    def row(tr):
        i = -1

        def cell(td):
            nonlocal i
            i += 1
            word = re.search("|".join(LEVEL), text_of(td[2])) if i in cols else None
            return f'<td{td[1]} class="lv-{LEVEL[word[0]]}">{td[2]}</td>' if word else td[0]
        return re.sub(r"<td([^>]*)>(.*?)</td>", cell, tr[0], flags=re.S)
    return re.sub(r"<tr[^>]*>.*?</tr>", row, table, flags=re.S)


def style_table(m):
    table = m[0]
    heads = [text_of(th) for th in re.findall(r"<th[^>]*>(.*?)</th>", table, re.S)]
    if "Crítica" in heads and "Informativa" in heads:
        table = re.sub(r"<th([^>]*)>(.*?)</th>",
                       lambda th: f'<th{th[1]} class="lv-{SEVERITY.get(text_of(th[2]), "info")}">{th[2]}</th>', table)
        return table.replace("<table>", '<table class="severity">', 1)
    if heads and "Probabilidad" in heads[0]:
        return color_cells(table, set(range(1, len(heads)))).replace("<table>", '<table class="matrix">', 1)
    cols = {i for i, h in enumerate(heads) if "Riesgo" in h and "Confianza" not in h}
    return color_cells(table, cols) if cols else table


body = re.sub(r"<table>.*?</table>", style_table, body, flags=re.S)

# --- print typography, applied outside tags and code: no line break inside a number, before a unit,
# after ≤ ≈ <, or inside an identifier such as VULN-01, CWE-89 or ID.RA-01
NBSP, NNBSP = "\u00a0", "\u202f"


def typeset(text):
    text = re.sub(r"(?<=\d) (?=\d{3}(?!\d))", NNBSP, text)
    text = re.sub(r"(?<=\d) (?=(?:%|ms|min|h|s|días|pet/s|peticiones/s)(?![\w/]))", NBSP, text)
    text = re.sub(r"(≤|≈|&lt;) (?=\d)", "\\1" + NBSP, text)
    return re.sub(r"\b[A-Z][A-Z.]*-\d+\b", r'<span class="nw">\g<0></span>', text)


parts = re.split(r"(<pre\b.*?</pre>|<code\b.*?</code>|<[^>]+>)", body, flags=re.S)
body = "".join(part if i % 2 else typeset(part) for i, part in enumerate(parts))


# in table cells, paths and names may also break after / or : between words (docs/swagger, headers:cross-origin)
# and after the dots of a host name (fonts.googleapis.com), so narrow columns need not be as wide as their
# longest name; numbers (A03:2021, HTTP/1.1) and file names (swagger.json) stay whole
def soft_breaks(table):
    def add(text):
        text = re.sub(r"(?<=\w{3}[/:])(?=[^\W\d_]{3})", "<wbr>", text)
        return re.sub(r"(?<=\w{3}\.)(?=[^\W\d_]{3,}\.)", "<wbr>", text)
    parts = re.split(r"(<[^>]+>)", table[0])
    return "".join(part if i % 2 else add(part) for i, part in enumerate(parts))


body = re.sub(r"<table\b.*?</table>", soft_breaks, body, flags=re.S)

# a paragraph ending in ":" introduces the table, code or list after it: keep the two on the same page
body = re.sub(r"<p>((?:(?!</p>).)*?:(?:</(?:strong|em)>)*)</p>(?=\s*<(?:table|div|pre|ul|ol|figure)\b)",
              r'<p class="lead">\1</p>', body, flags=re.S)

# title block: the line under the title (institution and course) is a subtitle
body = re.sub(r"(</h1>\s*)<p>", r'\1<p class="subtitle">', body, count=1)
title = text_of(re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)[1])

CSS = """
@page { size: A4; margin: 20mm 18mm 20mm 18mm;
  @top-right { content: "RUNNING_HEAD"; font: 400 8pt "Source Sans 3", sans-serif; color: #5F6A70; }
  @bottom-center { content: counter(page) " / " counter(pages); font: 400 8.5pt "Source Sans 3", sans-serif; color: #5F6A70; } }
@page :first { @top-right { content: none; } }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Source Sans 3", "Segoe UI", Arial, sans-serif; font-size: 10.4pt; line-height: 1.45; color: #15232B; margin: 0; }
h1 { font: 600 20pt/1.18 "Source Serif 4", Georgia, serif; margin: 0 0 2.5mm; color: #15232B; }
h1 ~ h1 { break-before: page; font-size: 17pt; margin-bottom: 4mm; }
p.subtitle { color: #3B4950; margin: 0 0 5mm; }
h2 { font: 600 14.5pt/1.25 "Source Serif 4", Georgia, serif; margin: 8mm 0 3mm; padding-bottom: 1.5mm; border-bottom: 1px solid #CDC3B2; break-after: avoid; }
h3 { font: 600 11.8pt/1.3 "Source Serif 4", Georgia, serif; margin: 6mm 0 2mm; break-after: avoid; }
h4 { font: 600 10.6pt/1.3 "Source Serif 4", Georgia, serif; margin: 5mm 0 2mm; color: #3B4950; break-after: avoid; }
h2 code, h3 code, h4 code { font-weight: 600; }
p { margin: 0 0 2.4mm; }
p.lead { break-after: avoid; }
ul, ol { margin: 0 0 2.6mm; padding-left: 6mm; }
li { margin: 0 0 1.2mm; }
li > ul, li > ol { margin: 1.2mm 0 0; }
li > p { margin-bottom: 1.2mm; }
blockquote { margin: 3mm 0 4mm; padding: 2.6mm 4.5mm; background: #F8EBDA; border-left: 3px solid #BF6A12; border-radius: 3px; break-inside: avoid; }
blockquote p { margin: 0; }
code { font-family: "IBM Plex Mono", Consolas, monospace; font-size: .86em; background: #F3EEE4; padding: 0 .22em; border-radius: 3px; overflow-wrap: break-word; }
pre { font-size: 9pt; line-height: 1.4; background: #F3EEE4; border: 1px solid #E4DDD0; border-radius: 4px; padding: 2.4mm 3.4mm; margin: 1.6mm 0 3.6mm;
  white-space: pre-wrap; overflow-wrap: anywhere; break-inside: avoid; }
pre code { background: none; padding: 0; font-size: .92em; }
code span.ex { font-weight: 600; }
code span.at { color: #94500A; }
code span.st, code span.ch { color: #006E65; }
code span.dt { color: #6A44A8; }
code span.fu, code span.op { color: #5F6A70; }
.nw { white-space: nowrap; }
hr { display: none; }
table { width: 100%; border-collapse: collapse; font-size: 8.8pt; line-height: 1.34; margin: 1mm 0 4.5mm; }
thead th { text-align: left; font-weight: 700; color: #15232B; background: #F3EEE4; border-bottom: 1.2px solid #CDC3B2; padding: 3.5px 6px; vertical-align: bottom; }
td { border-bottom: 1px solid #E4DDD0; padding: 3.5px 6px; vertical-align: top; text-align: left; }
tr { break-inside: avoid; }
td code, th code { font-size: .9em; }
.lv-crit { background: #F9DEDC; color: #8C1D18; }
.lv-high { background: #FBE5D3; color: #8A3A06; }
.lv-med  { background: #FBEFC9; color: #6E5200; }
.lv-low  { background: #DCEFE3; color: #1E6B3A; }
.lv-info { background: #E6EAEC; color: #3B4950; }
table.severity { width: 70%; margin: 1.5mm auto 4mm; }
table.severity th { text-align: center; border-bottom: none; padding: 5px 6px; }
table.severity td { font: 600 15pt/1.2 "Source Serif 4", Georgia, serif; padding: 5px 6px; }
table.matrix td { font-weight: 600; }
table.matrix td:first-child { background: #F3EEE4; color: #15232B; }
figure { margin: 3mm 0 5mm; text-align: center; break-inside: avoid; }
figure img { max-width: 100%; max-height: 118mm; width: auto; height: auto; border: 1px solid #E4DDD0; }
figcaption { font-size: 9pt; color: #3B4950; margin-top: 1.6mm; }
figcaption .file { font: 400 8pt "IBM Plex Mono", Consolas, monospace; color: #5F6A70; margin-left: 1.5mm; }
.math.display { display: block; text-align: center; margin: 3mm 0; font-size: 11.5pt; }
""".replace("RUNNING_HEAD", RUNNING_HEAD)

doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>{fonts}
{CSS}</style></head><body>
{body}
</body></html>"""
print("html bytes:", len(doc.encode()))

headings = [text_of(h) for h in re.findall(r"<h[1-6][^>]*>(.*?)</h[1-6]>", body, re.S)]


def retitle_bookmarks(pdf):
    """Chromium makes a bookmark per heading but repeats the text of a heading that opens a page
    ("Riesgo3. Modelo de Estimación de Riesgo") and drops the space where a title wraps:
    give each bookmark the text of its heading, in document order."""
    data = json.loads(run("qpdf", "--warning-exit-0", "--json=2", "--json-key=outlines", "--json-key=qpdf", str(pdf)))
    refs = []

    def walk(items):
        for item in items:
            refs.append(item["object"])
            walk(item["kids"])
    walk(data["outlines"])
    if len(refs) != len(headings):
        print(f"warning: {len(refs)} bookmarks for {len(headings)} headings; bookmark titles left as Chromium wrote them")
        return
    header, objects = data["qpdf"]
    patch = {f"obj:{ref}": {"value": {**objects[f"obj:{ref}"]["value"], "/Title": "u:" + title}}
             for ref, title in zip(refs, headings)}
    patch_file = pdf.with_suffix(".json")
    patch_file.write_text(json.dumps({"qpdf": [header, patch]}, ensure_ascii=False), encoding="utf-8")
    run("qpdf", "--warning-exit-0", str(pdf), f"--update-from-json={patch_file}", "--replace-input")


with tempfile.TemporaryDirectory() as tmp:
    page, pdf = Path(tmp) / "deliverable.html", Path(tmp) / "deliverable.pdf"
    page.write_text(doc, encoding="utf-8")
    chrome = subprocess.run(["chromium", "--headless=new", "--no-sandbox", "--disable-gpu", f"--user-data-dir={tmp}/profile",
                             "--no-pdf-header-footer", "--generate-pdf-document-outline", "--virtual-time-budget=3000",
                             f"--print-to-pdf={pdf}", page.as_uri()], capture_output=True, text=True)
    if not pdf.exists():
        sys.exit(f"Chromium did not write the PDF:\n{chrome.stderr}")
    retitle_bookmarks(pdf)
    OUT.write_bytes(pdf.read_bytes())  # replaces the old PDF only once the new one is complete
print("wrote", OUT)

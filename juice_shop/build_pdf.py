"""Build protocol.pdf from protocol.md: pandoc -> HTML with the deck's fonts and inline SVG figures -> Chromium.

Run from the repository root:
    nix shell nixpkgs#pandoc nixpkgs#chromium -c python3 scripts/build_protocol_pdf.py
The intermediate files go to cache/build/, which git ignores.
"""
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BUILD = REPO / "cache" / "build"
BUILD.mkdir(parents=True, exist_ok=True)

deck = (REPO / "slides/index.html").read_text(encoding="utf-8")
fonts = "\n".join(re.findall(r"@font-face\{.*?\}", deck, flags=re.S))
assert fonts.count("@font-face") >= 3, fonts.count("@font-face")

md = (REPO / "protocol.md").read_text(encoding="utf-8")
# print typography only (protocol.md keeps plain spaces): no line break inside a number or before its unit
md = re.sub(r"(?<=\d) (?=\d{3}(?!\d))", "\u202f", md)
md = re.sub(r"(?<=\d) (?=(?:%|GB|TB|MB|GiB|Mb|cM/Mb|MB/s)(?![\w]))", "\u00a0", md)
tmp_md = BUILD / "protocol.print.md"
tmp_md.write_text(md, encoding="utf-8")
body = subprocess.run(
    ["pandoc", str(tmp_md), "-f", "markdown", "-t", "html5", "--wrap=none"],
    check=True, capture_output=True, text=True).stdout


def inline_svg(m):
    src = m.group(1)
    svg = (REPO / src).read_text(encoding="utf-8")
    svg = re.sub(r"^<\?xml[^>]*\?>\s*", "", svg)
    return svg


body = re.sub(r'<img src="(protocol_figures/[^"]+\.svg)"[^>]*/?>', inline_svg, body)
assert "<img" not in body, "an image was not inlined"
# wide figures (mind map, schedule) get a landscape page of their own
for label in ("Mapa mental", "Cronograma"):
    i = body.find(f'aria-label="{label}')
    assert i > 0, label
    j = body.rfind("<figure>", 0, i)
    body = body[:j] + '<figure class="wide">' + body[j + len("<figure>"):]
# keep "Tabla N." captions with their table
body = re.sub(r"<p><strong>Tabla (\d+)\.</strong>", r'<p class="tcap"><strong>Tabla \1.</strong>', body)
# title block: the first paragraph is the kicker
body = body.replace("<p><strong>Protocolo de proyecto · Ciencia de Datos · Investigación proyectual</strong></p>",
                    '<p class="kicker">Protocolo de proyecto · Ciencia de Datos · Investigación proyectual</p>', 1)

CSS = """
@page { size: A4; margin: 20mm 19mm 20mm 19mm;
  @bottom-center { content: counter(page) " / " counter(pages); font: 400 8.5pt "Source Sans 3", sans-serif; color: #5F6A70; }
  @top-right { content: "Protocolo de proyecto · Ciencia de Datos"; font: 400 8pt "Source Sans 3", sans-serif; color: #5F6A70; } }
@page :first { @top-right { content: none; } }
:root { --paper:#FBF9F4; --card:#FFFFFF; --wash:#F3EEE4; --line:#E4DDD0; --line-strong:#CDC3B2; --ink:#15232B; --ink-2:#3B4950;
  --muted:#5F6A70; --teal:#008C80; --ochre:#BF6A12; --violet:#8257C4; --teal-ink:#006E65; --ochre-ink:#94500A;
  --ochre-wash:#F8EBDA; --ochre-soft:#F1D3AE; --kar-0:#AE95E0; --kar-1:#8257C4; --kar-2:#4D2C7C; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Source Sans 3", "Segoe UI", Arial, sans-serif; font-size: 10.4pt; line-height: 1.45; color: #15232B; margin: 0; }
@page wide { size: A4 landscape; margin: 14mm 16mm 16mm 16mm;
  @bottom-center { content: counter(page) " / " counter(pages); font: 400 8.5pt "Source Sans 3", sans-serif; color: #5F6A70; }
  @top-right { content: "Protocolo de proyecto · Ciencia de Datos"; font: 400 8pt "Source Sans 3", sans-serif; color: #5F6A70; } }
figure.wide { page: wide; margin: 0; }
figure svg[aria-label^="Sitios"] { max-width: 132mm; margin: 0 auto; }
figure.wide svg { max-height: 158mm; width: 100%; }
h1 + p { text-align: left; }
p.kicker { font: 700 8.5pt/1.2 "Source Sans 3", sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #94500A; margin: 0 0 3mm; text-align: left; }
h1 { font: 600 20pt/1.18 "Source Serif 4", Georgia, serif; margin: 0 0 4mm; color: #15232B; }
h2 { font: 600 14.5pt/1.25 "Source Serif 4", Georgia, serif; margin: 8mm 0 3mm; padding-bottom: 1.5mm; border-bottom: 1px solid #CDC3B2; break-after: avoid; }
h3 { font: 600 11.5pt/1.3 "Source Serif 4", Georgia, serif; margin: 5.5mm 0 2mm; break-after: avoid; }
p { margin: 0 0 2.4mm; text-align: justify; }
ul, ol { margin: 0 0 2.6mm; padding-left: 6mm; } li { margin: 0 0 1.2mm; }
blockquote { margin: 3mm 0 4mm; padding: 2.6mm 4.5mm; background: #F8EBDA; border-left: 3px solid #BF6A12; border-radius: 3px; }
blockquote p { margin: 0; }
code { font-family: "Source Code Pro", Consolas, monospace; font-size: .86em; background: #F3EEE4; padding: 0 .22em; border-radius: 3px; }
hr { display: none; }
p.tcap { font-size: 9.3pt; margin: 3mm 0 1.2mm; break-after: avoid; text-align: left; }
table { width: 100%; border-collapse: collapse; font-size: 8.8pt; line-height: 1.34; margin: 0 0 4.5mm; }
thead th { text-align: left; font-weight: 700; color: #15232B; background: #F3EEE4; border-bottom: 1.2px solid #CDC3B2; padding: 3.5px 6px; }
td { border-bottom: 1px solid #E4DDD0; padding: 3.5px 6px; vertical-align: top; text-align: left; }
tr { break-inside: avoid; }
figure { margin: 3mm 0 5mm; break-inside: avoid; }
figure svg { width: 100%; height: auto; display: block; }
figcaption { font-size: 9pt; color: #3B4950; margin-top: 1.6mm; }
a { color: #006E65; text-decoration: none; overflow-wrap: anywhere; }
h2[id^="x."] ~ p { text-align: left; padding-left: 6mm; text-indent: -6mm; font-size: 9.4pt; margin-bottom: 1.6mm; }
"""

html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Protocolo de proyecto · Ciencia de Datos</title>
<style>{fonts}
{CSS}</style></head><body>
{body}
</body></html>"""
out_html = BUILD / "protocol.html"
out_html.write_text(html, encoding="utf-8")
print("html bytes:", len(html.encode()))

subprocess.run(["chromium", "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=3000", f"--print-to-pdf={REPO / 'protocol.pdf'}", out_html.as_uri()],
               check=True, capture_output=True)
print("wrote", REPO / "protocol.pdf")

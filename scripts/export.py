"""Export a project document to a readable, self-contained HTML (and PDF if a
Chromium browser is installed). Standard library only.

Usage:
    python scripts/export.py                       # active project's deliverable.md (or strategy.md)
    python scripts/export.py projects/<slug>/strategy.md
    python scripts/export.py <file.md> --no-pdf

Output goes to projects/<slug>/export/<name>.html and .pdf. Every [E-nnn]
citation becomes a link to an appendix with that evidence row, so a reader can
check each claim without opening the repository.
"""
from __future__ import annotations

import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from _common import parse_ledger, project_dir

CSS = """
body{font:15px/1.55 -apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:#1d1d1f;max-width:900px;margin:32px auto;padding:0 20px}
h1{font-size:26px;margin:0 0 12px}h2{font-size:21px;margin:32px 0 10px;border-bottom:1px solid #ddd;padding-bottom:4px}
h3{font-size:17px;margin:22px 0 8px}h4{font-size:15px}
table{border-collapse:collapse;margin:12px 0;width:100%;font-size:13px}
th,td{border:1px solid #ccc;padding:5px 7px;vertical-align:top;text-align:left}th{background:#f3f3f3}
code{background:#f3f3f3;padding:1px 4px;border-radius:3px;font-size:13px}
pre{background:#f6f6f6;padding:10px;overflow-x:auto}blockquote{border-left:3px solid #ccc;margin:8px 0;padding:2px 12px;color:#555}
a.e{color:#0b5cad;text-decoration:none;font-size:12px}hr{border:0;border-top:1px solid #ddd;margin:24px 0}
.meta{color:#666;font-size:12px}#evidence td{font-size:11.5px}
@media print{body{margin:0;max-width:none}h2{page-break-after:avoid}tr{page-break-inside:avoid}}
"""


def inline(text: str) -> str:
    codes: list[str] = []

    def keep(m):
        codes.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w])_(?!\s)(.+?)(?<!\s)_(?![\w])", r"<em>\1</em>", text)
    text = re.sub(r"E-(\d{3,})", r'<a class="e" href="#E-\1">E-\1</a>', text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def to_html(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    para: list[str] = []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            flush()
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            out.append("<pre><code>" + html.escape("\n".join(block)) + "</code></pre>")
        elif s.startswith("<!--"):
            flush()
            while i < len(lines) and "-->" not in lines[i]:
                i += 1
        elif not s:
            flush()
        elif m := re.match(r"(#{1,6})\s+(.*)", s):
            flush()
            n = len(m.group(1))
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
        elif re.fullmatch(r"-{3,}|\*{3,}", s):
            flush()
            out.append("<hr>")
        elif s.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            flush()
            head = cells(s)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            out.append("<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
                       + "</table>")
            continue
        elif s.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + inline(" ".join(quote)) + "</blockquote>")
            continue
        elif re.match(r"\s*([-*+]|\d+[.)])\s+", line):
            flush()
            i = render_list(lines, i, out)
            continue
        else:
            para.append(s)
        i += 1
    flush()
    return "\n".join(out)


def render_list(lines: list[str], i: int, out: list[str]) -> int:
    """Render a (possibly nested) list starting at line i; return next line index."""
    stack: list[tuple[int, str]] = []  # (indent, tag)
    while i < len(lines):
        m = re.match(r"(\s*)([-*+]|\d+[.)])\s+(.*)", lines[i])
        if not m:
            if lines[i].strip() and stack and lines[i].startswith(" " * (stack[-1][0] + 2)):
                out[-1] = out[-1][:-5] + " " + inline(lines[i].strip()) + "</li>"
                i += 1
                continue
            break
        indent, tag = len(m.group(1).expandtabs(4)), ("ol" if m.group(2)[0].isdigit() else "ul")
        while stack and indent < stack[-1][0]:
            out.append(f"</{stack.pop()[1]}>")
        if not stack or indent > stack[-1][0]:
            stack.append((indent, tag))
            out.append(f"<{tag}>")
        out.append(f"<li>{inline(m.group(3))}</li>")
        i += 1
    while stack:
        out.append(f"</{stack.pop()[1]}>")
    # move nested lists inside the preceding <li>
    return i


def evidence_appendix(pdir: Path, body: str) -> str:
    rows, _ = parse_ledger(pdir / "evidence.md")
    cited = sorted(set(re.findall(r'href="#(E-\d{3,})"', body)), key=lambda x: int(x[2:]))
    if not cited:
        return ""
    trs = []
    for eid in cited:
        r = rows.get(eid)
        if not r:
            continue
        src = html.escape(r["source"])
        if r["source"].startswith("http"):
            src = f'<a href="{src}">{src}</a>'
        trs.append(f'<tr id="{eid}"><td>{eid}</td><td>{inline(r["claim"])}</td><td>{r["type"]}</td>'
                   f'<td>{src}</td><td>{r["date"]}</td><td>{r["rel"]}</td><td>{html.escape(r["status"])}</td></tr>')
    return ('<h2 id="evidence">Приложение: реестр доказательств / Evidence</h2>'
            '<p class="meta">F — факт из источника, H — гипотеза/допущение, P — прогноз, S — синтетические данные. '
            'Надёжность A–D. Полный реестр: evidence.md.</p>'
            '<table><tr><th>ID</th><th>Утверждение</th><th>Тип</th><th>Источник</th><th>Дата</th><th>Над.</th>'
            '<th>Статус</th></tr>' + "".join(trs) + "</table>")


def find_browser() -> str | None:
    for name in ("msedge", "chrome", "google-chrome", "chromium", "chromium-browser"):
        if p := shutil.which(name):
            return p
    for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"):
        if os.path.exists(p):
            return p
    return None


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if args:
        src = Path(args[0]).resolve()
    else:
        pdir = project_dir()
        if pdir is None:
            print("export: no active project")
            return 1
        src = pdir / "deliverable.md" if (pdir / "deliverable.md").exists() else pdir / "strategy.md"
    if not src.is_file():
        print(f"export: {src} not found")
        return 1
    pdir = src.parent
    md = src.read_text(encoding="utf-8")
    title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), src.stem)
    body = to_html(md)
    body += evidence_appendix(pdir, body)
    doc = (f'<!doctype html><html lang="ru"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width,initial-scale=1">'
           f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body>{body}</body></html>")
    out_dir = pdir / "export"
    out_dir.mkdir(exist_ok=True)
    out_html = out_dir / f"{src.stem}.html"
    out_html.write_text(doc, encoding="utf-8")
    print(f"HTML: {out_html}")
    if "--no-pdf" in argv:
        return 0
    browser = find_browser()
    if not browser:
        print("PDF: no Chrome/Edge found - open the HTML and use Print → Save as PDF.")
        return 0
    out_pdf = out_dir / f"{src.stem}.pdf"
    subprocess.run([browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf}", out_html.resolve().as_uri()],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    print(f"PDF: {out_pdf}" if out_pdf.exists() else "PDF: browser did not produce a file - print the HTML manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

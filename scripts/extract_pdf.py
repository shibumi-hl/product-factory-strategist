"""Extract a PDF's text to a UTF-8 file, page by page, so it can be read and cited
(`sources/<file>.pdf#page`) without console-encoding problems.

Usage:
    python scripts/extract_pdf.py projects/<slug>/sources/<file>.pdf
Writes projects/<slug>/analysis/<file>-text.txt with '=== page N ===' markers.

Needs `pypdf` (pip install pypdf) or PyMuPDF; scanned PDFs without a text layer
produce empty pages - read those as images instead.
"""
from __future__ import annotations

import sys
from pathlib import Path


def pages(path: Path) -> list[str]:
    try:
        import logging
        from pypdf import PdfReader
        logging.getLogger("pypdf").setLevel(logging.ERROR)  # harmless xref repair notices
        return [p.extract_text() or "" for p in PdfReader(str(path)).pages]
    except ImportError:
        pass
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf  # older PyMuPDF
        except ImportError:
            sys.exit("extract_pdf: install pypdf (pip install pypdf) or PyMuPDF")
    with pymupdf.open(str(path)) as doc:
        return [page.get_text() for page in doc]


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 1
    src = Path(argv[0]).resolve()
    if not src.is_file():
        print(f"extract_pdf: {src} not found")
        return 1
    project = src.parent.parent if src.parent.name == "sources" else src.parent
    out_dir = project / "analysis"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{src.stem}-text.txt"
    texts = pages(src)
    out.write_text("".join(f"=== page {i} ===\n{t.strip()}\n\n" for i, t in enumerate(texts, 1)), encoding="utf-8")
    empty = [i for i, t in enumerate(texts, 1) if not t.strip()]
    print(f"{len(texts)} pages -> {out}" + (f"; no text layer on pages {empty}" if empty else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

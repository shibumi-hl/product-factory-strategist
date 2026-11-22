"""Create a project folder from templates and make it active.

Usage:
    python scripts/new_project.py <slug> "<request text>"
    python scripts/new_project.py --switch <slug>
"""
from __future__ import annotations

import datetime as dt
import re
import shutil
import sys

from _common import ACTIVE_FILE, PROJECTS, ROOT

TEMPLATE = ROOT / "templates" / "project"


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[0] == "--switch":
        slug = argv[1]
        if not (PROJECTS / slug).is_dir():
            print(f"No project '{slug}'. Existing: {', '.join(existing()) or 'none'}")
            return 1
        ACTIVE_FILE.write_text(slug, encoding="utf-8")
        print(f"Active project: {slug}")
        return 0
    if len(argv) < 2:
        print(__doc__)
        return 1
    slug, request = argv[0], " ".join(argv[1:])
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,48}", slug):
        print("Slug: 2-49 chars, lowercase latin letters, digits and '-'.")
        return 1
    target = PROJECTS / slug
    if target.exists():
        print(f"Project '{slug}' already exists. Use --switch {slug} to resume it.")
        return 1
    shutil.copytree(TEMPLATE, target)
    for sub in ("analysis", "synthetic", "baseline"):
        (target / sub).mkdir(exist_ok=True)
    today = dt.date.today().isoformat()
    first_line = request.strip().split("\n")[0]
    title = first_line if len(first_line) <= 80 else first_line[:80].rsplit(" ", 1)[0] + "…"
    for path in target.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        text = text.replace("{{TITLE}}", title).replace("{{DATE}}", today).replace("{{REQUEST}}", request.strip())
        path.write_text(text, encoding="utf-8")
    ACTIVE_FILE.write_text(slug, encoding="utf-8")
    print(f"Created projects/{slug} and made it active.")
    print(f"Put source materials into projects/{slug}/sources/ , then continue in chat.")
    return 0


def existing() -> list[str]:
    return sorted(p.name for p in PROJECTS.iterdir() if p.is_dir() and not p.name.startswith((".", "_")))


if __name__ == "__main__":
    PROJECTS.mkdir(exist_ok=True)
    sys.exit(main(sys.argv[1:]))

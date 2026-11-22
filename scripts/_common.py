"""Shared helpers for the strategist scripts. Standard library only."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parent.parent)
PROJECTS = ROOT / "projects"
ACTIVE_FILE = PROJECTS / ".active"

EID = re.compile(r"E-\d{3,}")
ROW = re.compile(r"^\|\s*(E-\d{3,})\s*\|(.*)\|\s*$")
STATUS_OK = re.compile(r"^(active|superseded by E-\d{3,}.*|withdrawn:.+)$", re.I)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Windows consoles may default to a legacy code page; keep output readable.
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8")
    except Exception:
        pass


def active_slug() -> str | None:
    try:
        slug = ACTIVE_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return slug if slug and (PROJECTS / slug).is_dir() else None


def project_dir(slug: str | None = None) -> Path | None:
    slug = slug or active_slug()
    return PROJECTS / slug if slug else None


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def parse_ledger(path: Path) -> tuple[dict[str, dict], list[str]]:
    """Return ({id: row}, errors). Row keys: claim,type,source,date,rel,status,line."""
    rows: dict[str, dict] = {}
    errors: list[str] = []
    for n, line in enumerate(read(path).splitlines(), 1):
        m = ROW.match(line)
        if not m:
            continue
        eid = m.group(1)
        cols = [c.strip() for c in m.group(2).split("|")]
        if len(cols) != 6:
            errors.append(f"evidence.md:{n} {eid}: expected 7 columns, found {len(cols) + 1}")
            continue
        claim, typ, source, date, rel, status = cols
        if eid in rows:
            errors.append(f"evidence.md:{n} {eid}: duplicate ID (first on line {rows[eid]['line']})")
            continue
        rows[eid] = dict(claim=claim, type=typ.upper(), source=source, date=date,
                         rel=rel.upper(), status=status, line=n)
    return rows, errors


def budget_usd(pdir: Path) -> float | None:
    """First '$N' amount in brief.md → 'Agent budget' section, if any."""
    m = re.search(r"\$\s*(\d+(?:[.,]\d+)?)", section(read(pdir / "brief.md"), "Agent budget"))
    return float(m.group(1).replace(",", ".")) if m else None


def spent_usd(pdir: Path) -> float:
    import json
    try:
        data = json.loads(read(pdir / "cost.json") or "{}")
    except json.JSONDecodeError:
        return 0.0
    return sum(s.get("usd") or 0 for s in data.get("sessions", {}).values())


def budget_line(pdir: Path) -> str | None:
    budget = budget_usd(pdir)
    if not budget:
        return None
    spent = spent_usd(pdir)
    return f"${spent:.2f} of ${budget:.2f} budget ({spent / budget:.0%})"


def section(text: str, heading: str) -> str:
    """Body of a '## heading' section, without the heading line."""
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""

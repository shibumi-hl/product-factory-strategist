"""Deterministic checks on a project's evidence and documents.

Usage:
    python scripts/check.py                 # check the active project
    python scripts/check.py --impact        # list every citation of superseded/withdrawn evidence
    python scripts/check.py --project <slug>
    python scripts/check.py --no-run        # skip re-running analysis/*.py

Exit code 1 if there are errors.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _common import DATE, EID, STATUS_OK, active_slug, parse_ledger, project_dir, read

DOCS = ("options.md", "strategy.md", "deliverable.md", "decisions.md")
LABEL = re.compile(r"\((F|H|P|S)\)")
CITE = re.compile(r"\[(E-\d{3,}(?:\s*,\s*E-\d{3,})*)\]")
DEMAND_WORDS = re.compile(r"demand|want|need|share|market size|willing|%|спрос|хотят|нужн|доля|готовы", re.I)
UNOPENED = re.compile(r"snippet|unopened|not confirmed (?:in|by) (?:the )?source|выдержк|не открыт|в источнике не подтвержд", re.I)
NOT_EVIDENCE = re.compile(r"chat|conversation|previous answer|state\.md|decisions\.md|memory|переписк|чат", re.I)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.info: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def check_ledger(rows: dict, rep: Report) -> None:
    for eid, r in rows.items():
        where = f"evidence.md:{r['line']} {eid}"
        if r["type"] not in {"F", "H", "P", "S"}:
            rep.err(f"{where}: Type must be F, H, P or S (got '{r['type']}')")
        if not r["claim"]:
            rep.err(f"{where}: empty claim")
        if r["type"] in {"F", "P", "S"} and not r["source"]:
            rep.err(f"{where}: type {r['type']} needs a source")
        if r["type"] == "H" and not r["source"]:
            rep.warn(f"{where}: hypothesis without basis (cite E-IDs it infers from)")
        if r["source"] and NOT_EVIDENCE.search(r["source"]) and not r["source"].startswith("http"):
            rep.err(f"{where}: source '{r['source']}' is agent memory/state, not evidence")
        if (r["status"] == "active" and r["type"] == "F"
                and UNOPENED.search(r["claim"] + " " + r["source"])):
            rep.err(f"{where}: fact taken from a search snippet or an unopened page; open the source, "
                    f"or mark the row withdrawn / move the claim to H")
        if r["type"] == "F" and r["source"] and not (r["source"].startswith(("http", "sources/", "analysis/"))):
            rep.warn(f"{where}: fact source should be a URL, sources/… or analysis/… path")
        if r["date"] and not DATE.match(r["date"]):
            rep.err(f"{where}: Date must be YYYY-MM-DD")
        if not r["date"] and r["type"] != "H":
            rep.warn(f"{where}: no date")
        if r["rel"] not in {"A", "B", "C", "D"}:
            rep.err(f"{where}: Rel. must be A, B, C or D")
        if not STATUS_OK.match(r["status"]):
            rep.err(f"{where}: Status must be 'active', 'superseded by E-nnn …' or 'withdrawn: reason'")
        for ref in EID.findall(r["source"]):
            if ref not in rows:
                rep.err(f"{where}: source cites unknown {ref}")


def active_decision_lines(text: str) -> set[int]:
    """Line numbers belonging to decision blocks whose status is not superseded."""
    keep: set[int] = set()
    block: list[int] = []
    superseded = False
    lines = text.splitlines()
    for n, line in enumerate(lines + ["## END"], 1):
        if line.startswith("## "):
            if block and not superseded:
                keep.update(block)
            block, superseded = [], False
        block.append(n)
        if re.match(r"-\s*Status:\s*superseded", line.strip(), re.I):
            superseded = True
    return keep


def citations(text: str):
    """Yield (line_no, line, [ids]) for lines citing evidence, skipping fenced code."""
    in_code = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        ids = [i.strip() for group in CITE.findall(line) for i in group.split(",")]
        dep = re.match(r"\s*-\s*Depends on:\s*(.+)", line)
        if dep:
            ids += EID.findall(dep.group(1))
        if ids:
            yield n, line, ids


def check_docs(pdir: Path, rows: dict, rep: Report, impact: bool) -> list[str]:
    impacts: list[str] = []
    for name in DOCS:
        text = read(pdir / name)
        if not any(True for _ in citations(text)):
            rep.info.append(f"{name}: not started (no citations)")
            continue
        live = active_decision_lines(text) if name == "decisions.md" else None
        for n, line, ids in citations(text):
            where = f"{name}:{n}"
            for i in ids:
                if i not in rows:
                    rep.err(f"{where}: cites {i}, which is not in evidence.md")
                    continue
                status = rows[i]["status"]
                if not status.lower().startswith("active"):
                    msg = f"{where}: cites {i} ({status})"
                    impacts.append(msg + f"\n    {line.strip()[:160]}")
                    if name == "decisions.md":
                        if live is not None and n in live:
                            rep.warn(msg + " — active decision depends on outdated evidence")
                    else:
                        rep.err(msg + " — update the claim (run reassess)")
            known = [rows[i] for i in ids if i in rows]
            is_dep_line = line.strip().startswith("- Depends on:")
            if not is_dep_line and not line.lstrip().startswith("|") and not LABEL.search(line):
                rep.warn(f"{where}: claim cites evidence but has no (F)/(H)/(P) label")
            if known and all(r["type"] == "S" for r in known) and not is_dep_line:
                if DEMAND_WORDS.search(line):
                    rep.err(f"{where}: demand/frequency claim supported only by synthetic (S) evidence")
                else:
                    rep.warn(f"{where}: supported only by synthetic (S) evidence")
            if known and "(F)" in line and all(r["type"] in {"H", "S"} for r in known):
                rep.err(f"{where}: labelled (F) but cites only H/S evidence")
    return impacts


def check_options(pdir: Path, rep: Report) -> None:
    text = read(pdir / "options.md")
    if not CITE.search(text):
        return
    heads = re.findall(r"^## Option .*$", text, re.M)
    if len(heads) < 3:
        rep.err(f"options.md: {len(heads)} options; at least 3 required")
    if not any("[STATUS-QUO]" in h for h in heads):
        rep.err("options.md: no option marked [STATUS-QUO]")
    if not any("[STOP]" in h for h in heads):
        rep.err("options.md: no option marked [STOP]")
    if "<name>" in text:
        rep.warn("options.md: template placeholder '<name>' left in a heading")
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        if block.startswith("Option"):
            title = block.splitlines()[0]
            m = re.search(r"\*\*Strongest counterargument\*\*:\s*(.*)", block)
            if not m or len(m.group(1).strip()) < 15:
                rep.err(f"options.md: '{title}' has no real counterargument")


def check_strategy(pdir: Path, rep: Report) -> None:
    text = read(pdir / "strategy.md")
    if not CITE.search(text):
        return
    m = re.search(r"### Promise ↔ capability(.*?)(?=^#|\Z)", text, re.S | re.M)
    rows = [l for l in (m.group(1) if m else "").splitlines() if l.startswith("|") and "---" not in l][1:]
    if not rows:
        rep.err("strategy.md: promise ↔ capability table is empty")
    for row in rows:
        cols = [c.strip() for c in row.strip("|").split("|")]
        if len(cols) >= 3 and re.search(r"not supported|нет", cols[2], re.I):
            rep.err(f"strategy.md: promise '{cols[0]}' is not supported by the product")
        if len(cols) >= 4 and not EID.search(cols[3]):
            rep.warn(f"strategy.md: promise '{cols[0]}' has no evidence")
    for heading in ("Baseline", "Observation period", "Guardrail metrics", "Decision rule"):
        r = re.search(rf"^\|\s*{heading}[^|]*\|\s*([^|]*)\|", text, re.M)
        if not r or not r.group(1).strip():
            rep.err(f"strategy.md: validation plan field '{heading}' is empty")


def check_analysis(pdir: Path, rep: Report) -> None:
    """Run every analysis script: failure = ERROR, no CHECK line = WARNING."""
    import subprocess
    for script in sorted((pdir / "analysis").glob("*.py")):
        name = f"analysis/{script.name}"
        try:
            env = dict(__import__("os").environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
            res = subprocess.run([sys.executable, script.name], cwd=script.parent, capture_output=True,
                                 text=True, encoding="utf-8", errors="replace", timeout=120, env=env)
        except subprocess.TimeoutExpired:
            rep.err(f"{name}: did not finish in 120 s")
            continue
        if res.returncode != 0:
            tail = (res.stderr or res.stdout).strip().splitlines()[-1:] or ["no output"]
            rep.err(f"{name}: fails when re-run — {tail[0][:160]}")
        elif not re.search(r"^CHECK", res.stdout, re.M):
            rep.warn(f"{name}: no 'CHECK' hand-check line (see analyze-data skill)")


def main(argv: list[str]) -> int:
    slug = argv[argv.index("--project") + 1] if "--project" in argv else active_slug()
    pdir = project_dir(slug)
    if pdir is None or not pdir.is_dir():
        print("check: no active project")
        return 1
    rep = Report()
    rows, ledger_errors = parse_ledger(pdir / "evidence.md")
    rep.errors += ledger_errors
    check_ledger(rows, rep)
    impacts = check_docs(pdir, rows, rep, "--impact" in argv)
    check_options(pdir, rep)
    check_strategy(pdir, rep)
    if "--no-run" not in argv:
        check_analysis(pdir, rep)

    if "--impact" in argv:
        print(f"Impact of superseded/withdrawn evidence in {pdir.name}:")
        print("\n".join(impacts) if impacts else "  none")
        print()
    for label, items in (("ERROR", rep.errors), ("WARN", rep.warnings), ("info", rep.info)):
        for item in items:
            print(f"{label}: {item}")
    print(f"check {pdir.name}: {len(rows)} evidence rows, {len(rep.errors)} errors, {len(rep.warnings)} warnings")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

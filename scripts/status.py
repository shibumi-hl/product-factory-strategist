"""Show the active project's progress, evidence counts and cost.

Usage:
    python scripts/status.py            # human-readable
    python scripts/status.py --hook     # SessionStart hook: same text, framed as context
    python scripts/status.py --project <slug>
"""
from __future__ import annotations

import json
import sys
from collections import Counter

from _common import PROJECTS, active_slug, budget_line, parse_ledger, project_dir, read, section


def report(slug: str | None) -> str:
    pdir = project_dir(slug)
    if pdir is None or not pdir.is_dir():
        names = sorted(p.name for p in PROJECTS.glob("*") if p.is_dir() and not p.name.startswith((".", "_")))
        lines = ["No active project."]
        if names:
            lines.append("Existing projects: " + ", ".join(names) + " (resume: python scripts/new_project.py --switch <slug>)")
        lines.append('Start one: python scripts/new_project.py <slug> "<request>"')
        return "\n".join(lines)

    state = read(pdir / "state.md")
    rows, _ = parse_ledger(pdir / "evidence.md")
    by_type = Counter(r["type"] for r in rows.values() if r["status"].lower().startswith("active"))
    inactive = sum(1 for r in rows.values() if not r["status"].lower().startswith("active"))

    out = [f"Project: {pdir.name}",
           f"Stage: {section(state, 'Stage') or '?'}",
           f"Next step: {section(state, 'Next step') or '?'}"]
    remaining = section(state, "Remaining work")
    if remaining:
        out.append("Remaining work:\n" + remaining)
    unknowns = section(state, "Unknowns")
    if unknowns:
        out.append("Unknowns:\n" + unknowns)
    out.append("Evidence (active): " + (", ".join(f"{t}={n}" for t, n in sorted(by_type.items())) or "none")
               + (f"; superseded/withdrawn={inactive}" if inactive else ""))

    sources = [p.name for p in (pdir / "sources").glob("*") if p.name != "README.md"]
    out.append(f"Source files: {len(sources)}")

    cost = load_cost(pdir)
    if cost:
        out.append(f"Model cost so far: ${cost['total_usd']:.2f} across {len(cost['sessions'])} session(s); "
                   f"tokens in/out: {cost['total_input']:,}/{cost['total_output']:,}")
    line = budget_line(pdir)
    if line:
        out.append("Budget: " + line)
    log_lines = [l for l in read(pdir / "log.md").splitlines() if l.startswith("- ")]
    if log_lines:
        out.append("Last action: " + log_lines[-1][2:])
    return "\n".join(out)


def load_cost(pdir) -> dict | None:
    try:
        data = json.loads(read(pdir / "cost.json") or "null")
    except json.JSONDecodeError:
        return None
    if not data:
        return None
    sessions = data.get("sessions", {})
    data["total_usd"] = sum(s.get("usd", 0) for s in sessions.values())
    data["total_input"] = sum(m.get("input", 0) + m.get("cache_read", 0) + m.get("cache_write", 0)
                              for s in sessions.values() for m in s.get("models", {}).values())
    data["total_output"] = sum(m.get("output", 0) for s in sessions.values() for m in s.get("models", {}).values())
    return data


def main(argv: list[str]) -> int:
    slug = None
    if "--project" in argv:
        slug = argv[argv.index("--project") + 1]
    text = report(slug or active_slug())
    if "--hook" in argv:
        print("[Product Factory Strategist] Current project state (from projects/<slug>/state.md). "
              "Resume from 'Next step'; check items marked (assumed) first; do not repeat work already in log.md.\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

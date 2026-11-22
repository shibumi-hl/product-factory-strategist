"""Stop hook: price this session's token usage and store it in the active project's cost.json.

Claude Code passes JSON on stdin with session_id and transcript_path. We read the
transcript (and subagent transcripts next to it), sum usage per model, price it
with config/pricing.json and overwrite this session's entry (so re-runs never
double count). Never fails the session: errors go to stderr, exit 0.

Manual use: python scripts/cost.py --transcript <path.jsonl> [--session <id>]

Budget guard (budget = first $ amount in brief.md -> "Agent budget"):
  Stop hook        at >= 80% prints a systemMessage warning for the user.
  --prompt-hook    UserPromptSubmit hook: at >= 80% adds a budget line to the
                   agent's context; at >= 100% tells it to ask before more work.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

from _common import ROOT, budget_line, budget_usd, project_dir, spent_usd


def load_pricing() -> dict:
    data = json.loads((ROOT / "config" / "pricing.json").read_text(encoding="utf-8"))
    return data["models"]


def price_for(model: str, pricing: dict) -> dict | None:
    best = None
    for prefix, p in pricing.items():
        if model.startswith(prefix) and (best is None or len(prefix) > len(best[0])):
            best = (prefix, p)
    return best[1] if best else None


def usage_from(paths: list[Path]) -> dict:
    """Sum usage per model, counting each assistant message id once."""
    seen: dict[str, tuple[str, dict]] = {}
    for path in paths:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line in lines:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = rec.get("message") if isinstance(rec, dict) else None
            if not isinstance(msg, dict) or not msg.get("usage") or not msg.get("model"):
                continue
            key = msg.get("id") or rec.get("uuid") or f"{path}:{len(seen)}"
            seen[key] = (msg["model"], msg["usage"])  # last record per id wins (streaming updates)
    models: dict[str, dict] = {}
    for model, u in seen.values():
        m = models.setdefault(model, dict(input=0, output=0, cache_read=0, cache_write=0, messages=0))
        m["input"] += int(u.get("input_tokens") or 0)
        m["output"] += int(u.get("output_tokens") or 0)
        m["cache_read"] += int(u.get("cache_read_input_tokens") or 0)
        m["cache_write"] += int(u.get("cache_creation_input_tokens") or 0)
        m["messages"] += 1
    return models


def priced(models: dict, pricing: dict) -> float:
    total = 0.0
    for model, m in models.items():
        p = price_for(model, pricing)
        if not p:
            m["usd"] = None
            continue
        usd = (m["input"] * p["input"] + m["output"] * p["output"]
               + m["cache_read"] * p["cache_read"] + m["cache_write"] * p["cache_write"]) / 1_000_000
        m["usd"] = round(usd, 4)
        total += usd
    return round(total, 4)


def budget_state() -> tuple[str, float] | None:
    pdir = project_dir()
    if pdir is None:
        return None
    budget = budget_usd(pdir)
    if not budget:
        return None
    return budget_line(pdir) or "", spent_usd(pdir) / budget


def prompt_hook() -> int:
    state = budget_state()
    if state and state[1] >= 0.8:
        line, ratio = state
        msg = f"[Budget] {line}."
        if ratio >= 1:
            msg += (" The project budget is spent: before any further research or writing, "
                    "tell the user and ask them to approve a new budget (a human gate).")
        else:
            msg += " Prefer cheaper steps (haiku researcher, fewer sources) and say so."
        print(msg)
    return 0


def main(argv: list[str]) -> int:
    if "--prompt-hook" in argv:
        return prompt_hook()
    if "--transcript" in argv:
        transcript = Path(argv[argv.index("--transcript") + 1])
        session = argv[argv.index("--session") + 1] if "--session" in argv else transcript.stem
    else:
        payload = json.loads(sys.stdin.read() or "{}")
        transcript = Path(payload.get("transcript_path") or "")
        session = payload.get("session_id") or transcript.stem
    pdir = project_dir()
    if pdir is None or not transcript.is_file():
        return 0
    paths = [transcript] + sorted((transcript.parent / transcript.stem / "subagents").glob("*.jsonl"))
    models = usage_from(paths)
    usd = priced(models, load_pricing())

    cost_file = pdir / "cost.json"
    try:
        data = json.loads(cost_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = {"note": "Model token cost per Claude Code session, written by scripts/cost.py (Stop hook). "
                        "Prices from config/pricing.json. Excludes search/tool fees and human time.",
                "sessions": {}}
    data["sessions"][session] = {"updated": dt.datetime.now().isoformat(timespec="seconds"),
                                 "usd": usd, "models": models}
    data["total_usd"] = round(sum(s["usd"] for s in data["sessions"].values()), 4)
    cost_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    if "--transcript" in argv:
        print(f"session {session}: ${usd:.4f}; project total ${data['total_usd']:.4f}")
        return 0
    state = budget_state()
    if state and state[1] >= 0.8:
        print(json.dumps({"systemMessage": f"Budget warning: {state[0]}."}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # a cost hook must never break the session
        print(f"cost.py: {exc}", file=sys.stderr)
        sys.exit(0)

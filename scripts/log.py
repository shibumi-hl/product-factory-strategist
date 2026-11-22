"""Append a timestamped line to the active project's log.md.

Usage:
    python scripts/log.py <stage> "<what was done>" [files...]

Timestamps let `retro` measure time per stage; write the log through this
script rather than by hand.
"""
from __future__ import annotations

import datetime as dt
import sys

from _common import project_dir


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    pdir = project_dir()
    if pdir is None:
        print("log: no active project")
        return 1
    stage, action, files = argv[0], argv[1], ", ".join(argv[2:])
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"- {stamp} | {stage} | {action}" + (f" | {files}" if files else "")
    with open(pdir / "log.md", "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

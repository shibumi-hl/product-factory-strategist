"""PreToolUse hook for Write/Edit/MultiEdit/NotebookEdit.

Blocks (exit 2, reason on stderr, which Claude Code shows to the agent):
  1. any edit inside projects/<slug>/sources/ - raw materials are immutable;
  2. content that looks like an API key, token or private key.
"""
from __future__ import annotations

import json
import re
import sys

SECRET = re.compile(
    r"sk-ant-[A-Za-z0-9_\-]{20,}"
    r"|sk-[A-Za-z0-9]{32,}"
    r"|AKIA[0-9A-Z]{16}"
    r"|gh[pousr]_[A-Za-z0-9]{36,}"
    r"|xox[baprs]-[A-Za-z0-9\-]{10,}"
    r"|AIza[0-9A-Za-z_\-]{35}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
)


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    tool_input = payload.get("tool_input") or {}
    path = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "").replace("\\", "/")
    if re.search(r"(^|/)projects/[^/]+/sources/", path):
        print("Blocked: files in projects/<slug>/sources/ are original materials and must not be edited. "
              "Write derived results to evidence.md or analysis/ instead.", file=sys.stderr)
        return 2
    texts = [tool_input.get(k) for k in ("content", "new_string", "new_source")]
    texts += [e.get("new_string") for e in tool_input.get("edits") or [] if isinstance(e, dict)]
    for text in texts:
        if isinstance(text, str) and SECRET.search(text):
            print("Blocked: the content looks like a secret (API key, token or private key). "
                  "Secrets must not be stored in the repository; use environment variables.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

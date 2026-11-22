#!/usr/bin/env bash
# Run a script from scripts/ with the first working Python 3 interpreter.
# Usage: bash scripts/run.sh <script.py> [args...]
# Needed because on Windows "python"/"python3" may be the Microsoft Store stub.
dir="$(cd "$(dirname "$0")" && pwd)"
script="$1"; shift
for cand in "py -3" python3 python; do
  if $cand -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" >/dev/null 2>&1; then
    exec $cand "$dir/$script" "$@"
  fi
done
echo "Python 3.9+ not found. Install it from python.org and re-open the IDE." >&2
exit 0

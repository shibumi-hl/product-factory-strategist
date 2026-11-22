---
name: retro
description: Report time, cost, errors and human help for a finished project and compare the agent with a baseline (plain AI chat, manual analyst) on preregistered criteria, then propose improvements to the agent's skills or tools. Use at project end, «сколько стоило», «сравни с обычным чатом», «ретро».
---

# Retro and baseline comparison

Adapted from mattpocock *retro* (improve the environment, not just the output)
and gstack *eval-plan* (preregister the bar before measuring; price a pilot;
compare to the no-tool arm). Template: `templates/retro.md`.

## 1. Preregister (before running any baseline)

In `projects/<slug>/retro.md`, write the criteria and how each is scored:
time to final strategy, total cost, share of claims with a verifiable source,
number of options incl. status quo/stop, F/H/P labelling, promise–capability
mismatches, checker errors. Do not change them after you start.

## 2. Measure this run

- Cost and tokens: `cost.json` (Stop hook) → `python scripts/status.py`.
- Time: first and last timestamps in `log.md`.
- Errors, retries, re-routes, human corrections: from `log.md`.

## 3. Run baselines

- **Plain chat**: send the original request and the same source files to a
  fresh chat with no repo instructions. Save the answer to
  `projects/<slug>/baseline/plain-chat.md`. Note its cost.
- **Blind PM rating** (before you tell the user anything about the arms):
  put the agent's summary and the plain-chat answer side by side as
  "Answer 1" / "Answer 2" in random order, stripped of evidence IDs and file
  names, and ask the user to rate each 1–5 for "would I act on this". Only
  then reveal which is which. Record the order used.
- **Manual analyst**: estimate hours for the same scope from
  `knowledge/methods/baseline.md`, or use a real measurement if the team has one.
  Mark estimates (P).

Score all arms on the preregistered criteria. Ask the user before any paid
baseline run (gate).

## 4. Improve the agent

List what went wrong (slow lookups, failed tools, rows rejected, wrong routes)
and propose one change each: a checker rule (preferred — deterministic), a
skill wording fix, a new knowledge file, or a tool. Present to the user; apply
only what they accept.

Done when: `retro.md` has the preregistered table filled for every arm and a
ranked list of improvements.

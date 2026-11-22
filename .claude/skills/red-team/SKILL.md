---
name: red-team
description: Verify a strategy before hand-off - run the deterministic checker, then get a blind adversarial review from a red-team subagent that sees only the files, triage its findings, fix, and present the result with evidence. Use before claiming any options or strategy document is ready, «проверь», «готово?».
---

# Red team and verification

Adapted from superpowers *verification-before-completion* ("no completion
claim without fresh evidence") and *requesting-code-review*, plus gstack's
cold-read second opinion.

Two modes:

- **Options mode** — called by `options` before the option gate. Files:
  `brief.md`, `evidence.md`, `options.md` and every script in `analysis/`.
  Steps 1–3 only; then return to `options` step 5 (no approval gate here).
- **Strategy mode** (default) — before hand-off of the strategy. All steps.

## 1. Deterministic check

Run `python scripts/check.py`. Quote the summary line. Fix every ERROR. Each
WARNING is either fixed or explained in `strategy.md` → *Known limitations*.

## 2. Blind review

Dispatch the `red-team` subagent with only the mode's paths (strategy mode:
`brief.md`, `evidence.md`, `options.md`, `strategy.md`, plus `deliverable.md`
if it exists). Do not pass the conversation or your opinion — the reviewer
must not inherit our framing.

Without subagent support (e.g. Cursor): ask the user to open a new chat, paste
`.claude/agents/red-team.md` and the four paths, and bring back the findings.
If the user declines, review it yourself and say in the report that the
review was **not blind**.

## 3. Triage

Sort findings:

- **Valid and fixable** → fix now.
- **Valid, needs data** → add to `questions.md` and to *Known limitations*.
- **Disagree** → write one line why, with evidence.

One fix round. Re-run `scripts/check.py` after fixes.

## 4. Present

To the user, ≤300 words: the recommendation, the three strongest pieces of
evidence, the strongest counterargument and why we still recommend it, open
risks, the checker result and what the red team changed.

**Gate:** ask for approval. On yes: run `python scripts/export.py` (readable
HTML + PDF of `deliverable.md`, or of `strategy.md` when there is no
deliverable, with every evidence ID linked to an appendix), give the user the
file paths, set stage `approved`, then run `decision-log`.

Done when: checker shows 0 errors after the last edit, every red-team finding
has a disposition, and the user answered.

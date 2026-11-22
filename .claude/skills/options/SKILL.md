---
name: options
description: Generate at least three substantively different options - always including keep things as they are and discontinue - each with mechanism, evidence, costs, risks, its strongest counterargument and what would change our mind, then recommend one and stop for the user's choice. Use when research is done, or «какие варианты», «что делать».
---

# Options

Adapted from gstack *office-hours* Phase 3–4 (premise challenge, mandatory
alternatives, approval gate) and *plan-ceo-review* 0A–0D (do-nothing cost,
dream state). Framework: `knowledge/methods/options.md`.

## 1. Restate the situation

Five lines max, each claim with [E-…] and (F/H/P): what is known, what is
unknown, what the decision is.

## 2. Generate, then cut

Brainstorm 5–7 directions. Drop near-duplicates (same mechanism, different
name). Keep 3–5 that differ in **mechanism**, not in degree. Always keep:

- `[STATUS-QUO]` — keep things as they are. Describe its real cost and trend, not a straw man.
- `[STOP]` — discontinue the initiative; what is saved, what is lost.

## 3. Write each option

Use `templates/project/options.md`. For every option:

- **Mechanism**: why it would move the target metric.
- **For**: evidence, each line [E-…] (F/H/P).
- **Strongest counterargument**: the best case a smart opponent would make, with evidence.
- **Cost and effort**, **risks**, **what must be true** (assumptions as H).
- **What would change our mind**: the observation that would kill it.

## 3a. Separate the levers before you model impact

An option is usually a bundle of levers (a campaign, a product feature, a
tariff change). Before estimating any option's impact:

1. List every lever once, with its own effect estimate (H/P with ranges).
2. Mark which options could use each lever. A lever that does not depend on the
   option's own feature (e.g. an acquisition campaign, a support script) is a
   **shared lever**: add it to every option that could run it, including a
   "shared levers only" option next to `[STATUS-QUO]`.
3. Credit each option only with the increment of its own levers over that
   "shared levers only" baseline, and show that increment in the comparison
   table as a separate column or line.
4. If the recommendation holds only because a shared lever was credited to one
   option, it is not a recommendation: re-rank.

Write the lever list and the per-option increment into the analysis script
(`analysis/`) so the comparison is reproducible.

## 4. Compare and recommend

A table: option × (impact on target metric, confidence, cost, time, risk,
reversibility). Recommend one, in one sentence tied to the brief's goal, and say
which unknown matters most for this choice.

## 5. Gate

Run `python scripts/check.py`. Fix errors. Then run the `red-team` skill in
**options mode** (it reviews `options.md` and the `analysis/` scripts behind
it) and fix what it finds *before* the user sees the options: the user should
choose once, from corrected numbers. Show the table, the recommendation and
one line on what the review changed, and ask the user to choose. Do not write strategy before the choice. If the user
picks against the recommendation, record their reason in `options.md`.

Done when: check passes, the user chose, state stage = `option-chosen`.

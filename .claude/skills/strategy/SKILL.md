---
name: strategy
description: Write the aligned product strategy, communication strategy and validation plan for the chosen option, with a promise-to-capability table so no message overclaims what the product delivers. Use after the user picks an option, or «напиши стратегию», «что говорить аудитории».
---

# Strategy

Adapted from gstack *spec* (verified current state, quantified impact,
testable acceptance criteria). Methods: `knowledge/methods/product-strategy.md`,
`knowledge/methods/communication.md`, `knowledge/methods/validation.md`.
Template: `templates/project/strategy.md`. Every claim carries [E-…] and (F/H/P).

## 0. Follow the brief's own structure

If the brief prescribes a deliverable (sections, tables, calculations to show),
that structure wins. Write `projects/<slug>/deliverable.md` in the brief's
section order and language, with every requested table and calculation placed
next to the decision it supports. Then fill `strategy.md` as the checked core:
every section below must still be covered, and the deliverable cites the same
E-IDs. Before the gate, list each requirement of the brief and where the
deliverable answers it (a coverage table at the end of `deliverable.md`);
missing items are either added or named as gaps.

Figures given in the brief (market, baseline, unit rates) are evidence:
ledger rows with `Source: sources/<brief file>#page`. Numbers the brief says
are not given are assumptions (H) with a range and a way to measure them.

## 1. Product strategy

- **Target audience and need**: a concrete segment, its job-to-be-done, current alternative.
- **Alternatives** the audience has (including doing nothing).
- **Chosen direction** and **deliberate trade-offs**: what we will *not* do and who we will *not* serve.
- **Value ↔ cost ↔ revenue**: how value turns into money, unit economics with
  ranges, what drives cost. Forecasts are (P) with their assumptions.

## 2. Communication strategy

- **Audience and context**: where and when they meet the message.
- **Barriers**: to understanding, trusting and choosing (from evidence).
- **Key message** and **proof points** — each proof point cites evidence.
- **Channels and their roles** (awareness / explanation / conversion / retention).
- **Promise ↔ capability table**: every promise in the messages, the product
  capability that delivers it, evidence, status (delivered / planned / not
  supported). A promise without a delivered capability is removed or reworded.

## 3. Validation plan

- **Expected change**: metric, direction, size (P).
- **Baseline**: what we compare to (control group, previous period, region).
- **Observation period** and minimum sample.
- **Stop / scale criteria**.
- **Unintended consequences** to watch (cannibalisation, support load, churn of
  another segment) with a guardrail metric each.

## 4. Check alignment

Read product and comms side by side: same segment, same need, same value
proposition, no promise outside the product. Fix mismatches.

Then run the `red-team` skill.

Done when: all template sections are filled, the promise table has no
unsupported promise, `python scripts/check.py` passes, and — if the brief
prescribes a structure — `deliverable.md` follows it with a complete coverage table.

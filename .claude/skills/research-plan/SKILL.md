---
name: research-plan
description: Plan research as a map of decision-changing questions - each says which option its answer could kill, which method and source answer it, and what it costs - with a frontier, fog and out-of-scope list. Use after the brief is confirmed, or when new questions appear mid-research.
---

# Research plan

Adapted from mattpocock *wayfinder* (decision tickets, frontier, fog of war) and
superpowers *writing-plans* (steps with checkable results). Output:
`projects/<slug>/questions.md`.

## 1. List candidate questions

From the brief and premises, write every question that could matter.

## 2. Keep only decision-changing questions

For each, ask: *if the answer came back the other way, would the recommendation
change?* If no, move it to **Out of scope** with one line why. Typical
decision-changing questions: size of the affected segment, cause of the metric
change, what users do instead, competitor offers, cost to serve, barriers to choice.

## 3. Write each question as a ticket

```
### RQ-03 Do churned users switch to a competitor or stop using the category?
- Could change: kills option B (win-back campaign) if most stop using the category
- Method: public competitor reports + app-store reviews + 5 synthetic interviews (hypotheses only)
- Sources: approved list in brief.md
- Budget: ~15 min, ≤6 sources
- Blocked by: RQ-01
- Status: open | in-progress | answered (E-…) | blocked (reason)
```

## 4. Mark the frontier and the fog

Frontier = open, unblocked tickets. **Not yet specified** = questions you can
sense but cannot phrase sharply yet. They graduate into tickets as answers arrive.

## 5. Order by value per cost

Cheapest question that could kill an option goes first.

Done when: every ticket names the option it could change, a method, a source
type and a budget; the frontier is non-empty; state stage set to `planned`.

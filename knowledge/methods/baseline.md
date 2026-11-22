# Baseline comparison: method

## Arms

1. **This agent** — measured: time from `log.md`, cost from `cost.json`.
2. **Plain AI chat** — same request and files, no repo instructions, one model.
3. **Manual analyst** — measured if possible; otherwise an estimate (P) built
   from task counts: sources read × ~15 min, interviews × ~1.5 h (incl. notes),
   data analysis × 2–4 h, writing strategy 4–8 h, review 1–2 h. Multiply by
   the team's hourly cost.

## Criteria (preregister before running arms 2–3)

| Criterion | How scored |
|---|---|
| Time to final strategy | minutes |
| Total cost | money: model + tools + human review time |
| Claims with verifiable source | % of significant claims with a working source |
| Facts vs hypotheses labelled | % of claims labelled |
| Options incl. status quo and stop | count, yes/no |
| Promise–capability mismatches | count (lower is better) |
| Checker errors | `scripts/check.py` on each arm's output, after converting to the template |
| Decision-maker rating | 1–5 by the PM, blind to which arm produced it if possible |

Report the cost of the comparison itself.

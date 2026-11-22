# Projects

One folder per task, created by `python scripts/new_project.py <slug> "<request>"`.
`.active` holds the current slug. Each folder:

| File | Holds |
|---|---|
| `brief.md` | the framed task (confirmed by the user) |
| `state.md` | stage, next step, remaining work, unknowns — read on every resume |
| `evidence.md` | the ledger: every fact with source, type, date, reliability, status |
| `questions.md` | decision-changing research questions |
| `options.md` | ≥3 options incl. status quo and stop, comparison, user's choice |
| `strategy.md` | product + communication strategy + validation plan |
| `decisions.md` | append-only decisions with owners, metrics, triggers |
| `log.md` | one line per action |
| `cost.json` | token cost per session (written by the Stop hook) |
| `sources/` | original materials — read-only for the agent |
| `analysis/` | reproducible calculation scripts |
| `synthetic/` | simulated interview transcripts (labelled SYNTHETIC) |
| `baseline/` | outputs of baseline arms for comparison |

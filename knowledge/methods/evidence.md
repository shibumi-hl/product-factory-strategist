# Evidence ledger: format and rules

The ledger is `projects/<slug>/evidence.md`. It is the only place where facts
live. Every other document cites it. `scripts/check.py` parses it, so keep the
table format exactly.

```
| ID | Claim | Type | Source | Date | Rel. | Status |
|---|---|---|---|---|---|---|
| E-001 | Mobile subscribers in Russia, 2024: 256 mln SIM cards | F | https://example.org/report#p4 | 2025-03-10 | B | active |
```

## Columns

- **ID** — `E-` + three digits, never reused.
- **Claim** — one claim, with units and period.
- **Type**
  - **F** — fact stated directly by the source or computed from source data by a script in `analysis/`.
  - **H** — hypothesis or inference (ours or a source's opinion).
  - **P** — forecast/projection; write whose forecast and its assumptions.
  - **S** — synthetic: from a simulated respondent. Never proves demand or frequency.
- **Source** — one of:
  - a URL;
  - `sources/<file>` with page/sheet/cell/timestamp;
  - `analysis/<script>.py on sources/<file>` — a calculation on source files;
  - `analysis/<script>.py on E-001, E-006` — a calculation on public figures
    already in the ledger (the script names the E-ID next to each input value);
  - for H rows, `from E-003, E-007` — the rows it infers from.

  A calculation is F only if every input is F; otherwise it is H or P. Never
  cite chat history or a previous agent answer.
- **Date** — publication date of the source if known, else accessed date. `YYYY-MM-DD`.
- **Rel.** — reliability:
  - **A** primary and authoritative (regulator, official statistics, audited report, the product itself)
  - **B** primary but interested party (company press release, marketing page) or reputable secondary
  - **C** secondary or unverified (media retelling, blog, forum, app review sample)
  - **D** weak (anonymous, single anecdote, unclear method)
- **Status** — `active`, `superseded by E-nnn (YYYY-MM-DD)`, or `withdrawn: <reason> (YYYY-MM-DD)`.

## Citing in documents

Write the label after the claim and the ID: `ARPU grew 9% in 2024 (F) [E-004]`.
A sentence may cite several IDs: `[E-004, E-011]`. Hypotheses: `(H) [E-020]` or
`(H)` alone if it is the author's new hypothesis — then add it to the ledger as
an H row before the document is final.

## Cross-checking

A claim that alone picks or kills an option needs two independent sources or a
note "single source" and reliability no better than C.

## What is NOT evidence

The agent's previous summaries, `decisions.md`, `state.md`, memory from other
sessions, and synthetic interviews for anything about demand.

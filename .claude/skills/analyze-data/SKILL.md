---
name: analyze-data
description: Analyze spreadsheets and metrics reproducibly - validate units, periods, denominators and missing values, test competing explanations by trying to falsify them, and save every calculation as a re-runnable script whose outputs become ledger rows. Use for CSV/XLSX in sources/, metric questions ("why did retention drop"), or any number the strategy depends on.
---

# Analyze data

Adapted from superpowers *systematic-debugging* (root cause before fix;
falsify hypotheses) and *verification-before-completion* (no claim without a
fresh run). Methods: `knowledge/methods/data-analysis.md`.

## 1. Profile before you compute

Write `analysis/<nn>_profile.py` that prints for each table: rows, columns,
types, period covered, missing values per column, duplicates, obvious unit
mixes (rub vs thousand rub, % vs share). Run it. Record surprises in `log.md`.

## 2. State competing explanations

For a metric change, write 2–4 explanations as (H) rows, e.g. "retention fell
because of the March price change" vs "because of a new cohort mix". For each,
write what you would see in the data if it were **false**.

## 3. Try to falsify

Write one script per test in `analysis/`. With no data files (public-data
projects), inputs are ledger values typed into the script, each with its E-ID
in a comment. Compare like with like (same cohort
definition, same period length). Report effect size and the base, not only %.
Small samples: say n and do not generalise.

Every script ends with at least one **hand check**: one key number recomputed
the simplest way (plain arithmetic on the inputs, not the model's functions)
and compared with the model's result:

```python
assert abs(model_value - hand_value) < 0.01, (model_value, hand_value)
print(f"CHECK ok: <what> = {hand_value}")
```

`scripts/check.py` runs every `analysis/*.py`: a script that fails is an
ERROR, one without a `CHECK` line is a WARNING.

PDF sources: extract text with `python scripts/extract_pdf.py sources/<file>.pdf`
(UTF-8 into `analysis/`), never by printing to the console.

## 4. Record results

Each result = one ledger row: type F if computed from a source file, with
`Source: analysis/<script>.py on sources/<file>`. An explanation that survived
is still (H) unless a direct source confirms the cause.

## 5. Verify

Re-run every script from a clean start (`python analysis/<script>.py`) and
confirm the numbers in the ledger match the output. Quote the output.

Done when: every number cited from this stage has a script that reproduces it,
and the units/period/denominator are stated in the ledger row.

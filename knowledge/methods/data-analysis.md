# Data analysis: checklist

Before any number goes into the ledger:

- **Units**: currency, thousands vs units, % vs percentage points, per user vs total.
- **Period**: same length and season for compared periods; partial months flagged.
- **Denominator**: retention of whom (cohort definition), conversion from which step.
- **Missing values**: count per column; how handled (dropped, imputed, excluded) — stated.
- **Duplicates and outliers**: counted; rule for removal stated.
- **Sample size**: report n; no percentages on n < 30 without saying so.
- **Mix effects**: an overall rate can fall while every segment's rate rises (Simpson). Split by key segments.
- **Correlation ≠ cause**: a co-occurring change is (H) until a design (control group, natural experiment) supports it.

Qualitative methods: thematic coding of reviews/interviews — code book in
`analysis/`, count respondents per theme, quote exact words.

Every calculation is a script in `analysis/` (Python stdlib or pandas if
installed) that reads from `sources/` and prints its results. Re-run before citing.

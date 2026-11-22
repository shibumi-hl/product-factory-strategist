---
name: reassess
description: Reassess conclusions when new data arrives - add it to the ledger, mark contradicted or outdated evidence superseded, trace every option, strategy line and decision that depends on it, and update only what is affected. Use when the user adds a file or numbers, «появились новые данные», «пересмотри», or a reconsider-if trigger fires.
---

# Reassess on new data

Adapted from gstack *learn* prune (STALE / CONFLICT flags, ask before
removing) and mattpocock *chief-of-staff* lint.

## 1. Ingest

Process the new material with `collect` / `analyze-data` as usual. New rows get
new IDs; never edit old rows' claims.

## 2. Compare with existing evidence

For each new row, find ledger rows about the same thing. Classify:

- **Confirms** → write "confirms E-old" in the new row's claim; the old row stays as is.
- **Contradicts** → old row status `superseded by E-new (YYYY-MM-DD)`, or
  keep both and add an H row if you cannot tell which is right.
- **Outdated** (period passed, source updated) → `superseded`.
- **Wrong** (error found) → `withdrawn: <reason>`.

## 3. Trace impact

Run `python scripts/check.py --impact`. It lists every line in `options.md`,
`strategy.md` and `decisions.md` that cites a superseded or withdrawn row.

## 4. Update and report

For each affected line decide: still holds (cite the new evidence), weakened
(downgrade F→H, add limitation), or broken. If a broken claim supports the
chosen option or a decision, that is a gate: tell the user which decision is at
risk and what you recommend. Record the update in `log.md` and in a dated
*Change log* section at the end of the affected file.

An approved strategy may be updated with new figures (with a *Change log*
entry) without re-approval; a change to its decision rules or chosen option
needs the user. Decisions are never edited: a decision at risk is put to the
user, who may record a superseding D-entry.

Done when: every reference `check.py --impact` lists is either fixed or put to
the user at a gate, and the user has seen the list of changed conclusions.

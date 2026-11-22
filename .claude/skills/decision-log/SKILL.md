---
name: decision-log
description: Record a decision after approval - owner, date, metrics, commitments with deadlines, reconsider-if triggers and the evidence it depends on - and later show what needs deciding now and which commitments or assumptions are overdue. Use after strategy approval, «зафиксируй решение», «что по обязательствам», «что надо решить сейчас».
---

# Decision log

Adapted from mattpocock *domain-modeling* ADRs and *chief-of-staff* wiki
("write history, not the present"). File: `projects/<slug>/decisions.md`,
format in `templates/project/decisions.md`. Append-only.

## A. Record a decision

1. Ask the user (gate) for: owner, decision date, and anyone else committed —
   unless their approval message already gave them. Use roles, not names.
2. Write a `D-nnn` entry: what was decided, which option, why (2–3 lines with
   [E-…]), rejected options and why.
3. **Metrics**: target metric with baseline and target; guardrail metrics.
4. **Commitments**: who does what by when.
5. **Reconsider if**: concrete triggers, e.g. "conversion < 2% after 6 weeks",
   "competitor X launches a free tier", "E-014 is superseded".
6. **Depends on**: every E-ID the decision rests on.
7. Set stage `tracking`.

## B. Review ("what needs deciding now")

1. Run `python scripts/check.py --impact` and read `decisions.md`.
2. Report three lists: commitments past due; decisions whose evidence is
   superseded/withdrawn or older than the freshness limit in `brief.md`;
   triggers that may have fired (ask the user for the latest numbers if unknown).
3. Recommend what to decide now, smallest set first.

To change a decision, add a new entry that supersedes the old one; set the old
one's status to `superseded by D-nnn` with the date. Never edit its text.

Done when: the entry has owner, metric, at least one trigger and a non-empty
Depends-on list — or the review lists are delivered.

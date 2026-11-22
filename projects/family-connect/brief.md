# Brief: Связь для близких и собственных устройств: кому помочь в первую очередь, что изменить и почему оператору стоит вложить в это деньги

Created: 2026-11-22 · Status: confirmed 2026-11-22

## Original request
> Связь для близких и собственных устройств: кому помочь в первую очередь, что изменить и почему оператору стоит вложить в это деньги (бриф MegaFon, sources/megafon-brief.pdf)

## Decision to inform
Two decisions of the head of the direction (from materials, [E-012]):
1. **End of Q1:** fund a pilot (people + money) — approve a specific pilot, change its terms, or first remove a blocker.
2. **End of Q2 (with finance):** widen coverage, change the offer, or keep observing.
Plus: a one-year plan by quarter and a measurable landmark for the end of year 3. If data is insufficient — say which data and what to do until it arrives.

## Recipient of the output
Head of the direction and the finance team (case jury reads the same document). Format: **one document in Russian, five parts** as the brief prescribes, opening with first customers, chosen problem, offer and expected result; calculations placed next to the decisions they justify. File: `deliverable.md` (+ working `options.md`, `strategy.md`).

## Target outcome and success metric
Planned-year targets vs "no change" [E-003–E-007]: gross profit ≥ 285 (vs 279) mln RUB; active family groups (last month) ≥ 8 000 (vs 5 000); connected groups ≥ 12 000 (vs 8 000); connected multi-number owners ≥ 2 000 (vs 1 000); 14-day activation ≥ 60 % (vs 45 %). Profit lever: 500 RUB per extra paid month per number [E-008]; 6 mln gap = 12 000 extra paid months.

## Status quo
Organizer can already top up a member from the shared pool but learns of an outage from a plea for help; owners can switch numbers in the cabinet but miss that money/data ran out [E-010]. Base year runs behind plan on every metric [E-003–E-007].

## Target user (specific situation)
**Open — team's choice per the brief** (first service, test, expansion order). Chosen at the options gate between: family organizer at member's low-balance/limit moment; payer facing an unexplained charge; owner of a router SIM before its billing date.

## Constraints
Resources [E-009]: owner assigned; designer + analyst 0.5 FTE each to be allocated; 3 dev person-months tentative for Q2; 1 QA person-month unconfirmed. Consent rules: member controls visibility, payer confirms payments, location needs separate consent. No real company confidential data (fictional operator, training numbers).

## Available data and approved sources
`sources/megafon-brief.pdf` (all base figures). Public web data (≤24 months) — also used for market figures: to cross-check the brief's market/base numbers and to set ranges for values the brief does not give (cause frequencies, channel conversion, churn, alert effects); such values are labelled (H) with source, brief figures stay the calculation base. Not given and not invented as facts: cause frequencies, channel split, retention, dev cost [E-011] → stated as labelled assumptions (H) with ranges.

## Premises (confirmed / rejected)
- P1 confirmed: base-year active-group gap comes both from fewer connected groups (6 500 vs 7 500) and a lower active share (≈62 % vs ≈67 %) [E-004, E-005].
- P2 confirmed: main profit lever is retention (extra paid months), not a new paid add-on (H).
- P3 confirmed: Q2 pilot fits 3 dev person-months, starts with an alert linked to the existing top-up operation, randomised by family (H).

## Agent budget
$10 total model spend. Public evidence freshness ≤ 24 months (H, to confirm).

## Assumptions (H)
- Synthetic respondents may be used only to generate hypotheses (type S).

## PM answers
2026-11-22, frame gate: «Есть правки» → «В Q1 try to go into the market figures. thats all»
Interpretation (agent, stated to PM): Q1 changed — public data may inform market figures (cross-check + ranges for missing values, labelled H); Q2–Q5 and P1–P3 accepted as proposed.

## Change log
- 2026-11-22: Q1 data rule changed at frame gate: public data context-only → also used for market figures (as H ranges/cross-checks).

# Validation plan: method

| Field | Question it answers |
|---|---|
| Hypothesis | If we do X for segment Y, metric Z changes by N because of mechanism M. |
| Primary metric | One metric, exact definition, unit, source system. |
| Baseline | Control group, holdout region, matched cohort, or previous period (say why it is comparable). |
| Minimum detectable effect and sample | What effect is worth acting on; rough sample needed. |
| Observation period | Long enough for the behaviour cycle (e.g. a billing month). |
| Guardrail metrics | Side effects: cannibalisation, churn in other segments, support load, complaints. |
| Decision rule | Scale if …; stop if …; extend if … — set **before** the test. |
| Data check | Where the numbers come from and who validates them. |

## Realistic pool and start date

- **Eligible pool = base × every inclusion condition.** Multiply the starting
  base (customers, groups, households) by each condition a unit must meet to be
  in the test: tariff or product that supports it, consent, the resource the
  feature needs (free volume, a linked number), reachable channel, opt-in.
  Each factor is a ledger row (F if measured, H with a range otherwise). Show
  the pool in the base and the unfavourable scenario.
- **Sample check against the pool.** Compute the sample per arm, then the
  weeks needed to collect it from the eligible pool. If the period runs past
  the decision date, change the test (bigger effect, a faster primary metric,
  a different unit) instead of keeping a test that cannot answer in time.
- **Start date from the work chain.** Derive the launch date backwards from
  the allocated resources: build → test → launch prep → start. Use the
  person-months the brief allocates and the quarter they are available in.
  A start date earlier than the chain allows is an error, not an ambition.
- **Clustering.** If units are randomised in groups (families, stores,
  regions) but measured per member, inflate the sample by the design effect
  `1 + (m − 1) × ICC` (m — members per group); state the ICC as H.

Prefer the cheapest test that can kill the hypothesis (fake-door, landing page,
pilot in one region) before a full launch.

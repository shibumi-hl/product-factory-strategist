# Decisions

Append-only. To change a decision, add a new entry and mark the old one
superseded. Format:

```
## D-001 — <what was decided>
- Status: active | superseded by D-nnn (YYYY-MM-DD)
- Date: YYYY-MM-DD
- Owner: <role, not personal data>
- Option: <from options.md>
- Why: <2-3 lines with [E-…]>
- Rejected: <options and why>
- Metrics: <primary with baseline → target; guardrails>
- Commitments: <who · what · by YYYY-MM-DD>
- Reconsider if: <triggers>
- Depends on: E-001, E-004
```

## D-001 — Launch option C as a 12-month own-app travel eSIM pilot; E is the scale-up path
- Status: active
- Date: 2026-11-17
- Owner: Head of Travel & Roaming Products
- Option: C (own-brand data-only travel eSIM in our app for own subscribers, priced near independents); E (partner channels, all travellers) only if the pilot passes
- Why: operator packages cost 1.6x-3.1x more per GB than independent eSIMs Russians can pay for (F) [E-021, E-010]; buying before departure in a trusted app is an edge, as Turkey restricts some foreign eSIM sites (F) [E-009]; the pilot is the cheapest way to measure P4, which public data cannot answer (H) [E-025, E-030].
- Rejected: A status quo (leakage to cheaper eSIMs continues) (H) [E-024]; B stop (loses summer 2027 while rivals learn) (F) [E-003, E-004]; D roaming price cut (maximum cannibalisation) (H) [E-025]; E now (changes the own-subscribers-first brief; margin after commission unknown) (H) [E-020].
- Metrics: primary take-rate = paid activations / eligible exposed trips to pilot destinations, baseline 0, target 3%, about 40k activations in 12 months (P) [E-028]; brief target of 300k kept for C plus E. Guardrails: cannibalisation (buyers with a roaming package in the prior 12 months; roaming revenue per traveller exposed vs 20% holdout) below k_max (P) [E-029]; activation success >= 90%; support contacts per activation; refunds and complaints; churn exposed vs holdout.
- Commitments: Head of Travel & Roaming Products · price the partner contract and run the pre-launch k_max check (no launch at the planned price if k_max < 15%) · before launch; Head of Travel & Roaming Products · launch the pilot in five destinations with a 20% holdout · by 2027-05-31; Head of Travel & Roaming Products · interim read with finance sign-off · by 2027-09-30; Head of Travel & Roaming Products · final read and scale/extend/stop decision · by 2028-05-31. Others committed: not named by the PM.
- Reconsider if: k_max from the contracted cost < 15% at the planned price; take-rate < 1.5% at the September 2027 read; net revenue per exposed traveller > 5% below holdout and significant; activation success < 90%; MTS or Beeline cut travel-eSIM prices below 52 RUB/GB; any of E-021, E-028, E-029 is superseded.
- Depends on: E-003, E-004, E-009, E-010, E-018, E-019, E-020, E-021, E-023, E-024, E-025, E-028, E-029, E-030

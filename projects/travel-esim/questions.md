# Research questions

Each question must be able to change the decision. Format in
`.claude/skills/research-plan/SKILL.md`.

Source budget: ~12 total; 4 used in framing (E-001..E-005), ≤8 for this plan.

## Frontier

### RQ-01 (P1) What do travellers already get from big-four operators and independent eSIM sellers, at what price per GB, and can Russians pay for the independents?
- Could change: kills "launch a stand-alone travel eSIM" if cheaper, payable alternatives already cover the main destinations; favours [STATUS-QUO] / repricing the existing package instead
- Method: public price comparisons for Turkey/Egypt (top destinations [E-002]); compute ₽/GB in a script
- Sources: operator tariff round-ups, eSIM seller comparisons (C), operator press (B)
- Budget: ≤3 sources
- Blocked by: -
- Status: answered (E-006..E-010, E-014, E-015, E-021, E-024)

### RQ-02 How many of our travelling subscribers can technically use an eSIM, and is eSIM adoption in Russia growing?
- Could change: shrinks every eSIM option if eSIM-capable phones are a small minority; favours a SIM-less roaming repackage instead
- Method: public market statements on eSIM adoption in Russia
- Sources: trade press (B/C)
- Budget: ≤2 sources
- Blocked by: -
- Status: answered, partially (E-011..E-013, E-018, E-019); no share of eSIM-capable phones found

### RQ-03 Is the 300k activations / 12 months target reachable from own subscribers' trips?
- Could change: makes the brief's success target unrealistic → re-scope target or channel (open sale beyond own base)
- Method: analysis/01_sizing.py on outbound trips [E-001] × subscriber-share and eSIM-capability scenarios (H)
- Sources: E-001, E-016 + 1 operator-results source
- Budget: ≤1 source
- Blocked by: RQ-02
- Status: answered (E-022, E-023)

### RQ-04 (P4) Does travel-eSIM margin per activation exceed the roaming data revenue it replaces?
- Could change: kills options that cannibalise roaming if the replaced revenue is larger than eSIM margin
- Method: public wholesale/roaming revenue data
- Sources: operator reports
- Budget: ≤1 source
- Blocked by: -
- Status: blocked (no public data on operators' roaming revenue or eSIM wholesale cost; needs internal finance data) - see E-025

## Blocked
- RQ-04: internal data required (roaming data revenue per traveller, wholesale cost per GB). Public proxy only: retail price gap (E-021).

## Answered
- RQ-01, RQ-02 (partial), RQ-03

## Open for the pilot (from red-team, 2026-11-17; internal data, not public research)
- Variance of roaming revenue per traveller (last year's data) - sets the sample needed for the P4 revenue comparison.
- Wholesale cost per GB from the partner contract - sets k_max and the pre-launch go/no-go (E-029, E-030).
- Legal check: may past roaming data be used to target the pre-trip notice?

## Not yet specified (fog)
- Which message / value frame works for travellers (price, "no shop at the airport", keep messengers) - needs real behaviour data or a test; synthetic interviews deliberately skipped (budget, and S rows cannot show demand).
- Whether a Russian-operator brand is trusted more than foreign apps for travel data.

## Out of scope
- Inbound tourists buying Russian eSIMs: different product and customer; not asked.
- Corporate (B2B) travel: brief targets own retail subscribers first (Q6).
- Voice/SMS bundles: P2 confirmed the product is data-only.

# State: Travel data eSIM for Russians going abroad

## Stage
tracking

## Next step
GATE (waits on user): reassess found D-001 rests on superseded evidence (E-023, E-028, E-029) and its trigger "any of E-021, E-028, E-029 is superseded" fired. PM decides whether to record D-002 superseding D-001: (1) price floor 79 RUB/GB; (2) launch only if contracted wholesale gives k_max >= 25% (about 45 RUB/GB or less at 790 RUB), target 40 RUB/GB; (3) early cannibalisation read by 2027-07-31; (4) volume target restated as about 33k at 3%; optional (5) pre-trip push only to travellers without a roaming package in the last 12 months. Or keep D-001 unchanged.

## Done
- projects/travel-esim/brief.md - confirmed brief
- projects/travel-esim/questions.md - research plan RQ-01..RQ-04 + open pilot data needs
- projects/travel-esim/evidence.md - E-001..E-040 (E-023, E-028, E-029 superseded)
- projects/travel-esim/analysis/01_sizing.py - sizing and price-per-GB script
- projects/travel-esim/analysis/02_pilot_target.py - pilot target scenarios and break-even cannibalisation
- projects/travel-esim/options.md - options A-E; User's choice: C, E as scale-up
- projects/travel-esim/strategy.md - product, comms, validation plan; red-team round done; approved; reassessed with finance note
- projects/travel-esim/decisions.md - D-001 (approved 2026-11-17, owner Head of Travel & Roaming Products)
- projects/travel-esim/analysis/03_finance_reassess.py - finance-note unit economics, k_max, volume at 41% eSIM-capable

## Remaining work
- Open. PM decides on D-002 vs keeping D-001. (done-checked: check.py 0 errors, 5 warnings all on D-001 this turn)
- Open. Track D-001 commitments: contract pricing and k_max check before launch; launch by 2027-05-31; interim 2027-09-30; final 2028-05-31. (file-exists: decisions.md)

## Unknowns
- P4: cost side now indicative (48 RUB/GB, E-031; break-even k_max 22.9%, E-035); actual cannibalisation among buyers unknown until the pilot (E-039). Finance note is marked test data.
- Take-rate benchmark for an operator travel eSIM: no public sales volumes found (E-027); 3% pilot target is judgement.
- Share of our travelling subscribers with eSIM-capable phones: base share is 41% (E-034); travellers may differ (H).
- Our subscriber share of outbound travellers: operator unnamed; sizing uses 20-30% (H).
- MTS and Beeline subscriber counts end-2025: not in the source used (E-016).
- Which message frames value best: no behavioural data; to be A/B tested in the pilot.
- Most prices come from commercial eSIM-seller blogs (reliability C); not verified on operator sites (source budget).
- (Resolved 2026-11-17) Agent spend is now recorded: cost.json was back-filled for the two test runs ($3.60) and the Stop hook was verified in a real Claude Code session.

## Decisions so far
- Depth: full workflow - brief.md.
- Brief confirmed 2026-11-17; P2, P3 confirmed; P1, P4 -> RQ-01, RQ-04 - brief.md.
- Interviews/ux-audit skipped: source/budget limit and no UI to audit - log.md.
- PM chose C as pilot, E as scale-up path; P4 treated as open risk - options.md -> User's choice.
- Strategy approved, 40k pilot target and decision rules: D-001, 2026-11-17, owner Head of Travel & Roaming Products - decisions.md.

## History
- 2026-11-17 project created
- 2026-11-17 frame: 3 web searches, 4 sources, draft brief, questions sent to PM
- 2026-11-17 brief confirmed; stage framed -> planned (questions.md) -> researched (collect 5 sources, analysis/01_sizing.py, options.md)
- 2026-11-17 PM chose C (+E scale-up); stage -> option-chosen; 1 web search (source 10 of ~12), analysis/02_pilot_target.py, strategy.md, red-team round; waiting at gate: approve strategy
- 2026-11-17 PM approved strategy; D-001 recorded; stage -> tracking; reassess on sources/finance-note-2026-11.md (E-031..E-040); waiting at gate: D-002 or keep D-001

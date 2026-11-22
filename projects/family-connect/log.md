# Activity log

`YYYY-MM-DD HH:MM | stage | action | files`

- 2026-11-22 | new | project created | brief.md, state.md
- 2026-11-22 10:16 | frame | read megafon-brief.pdf (11 p.), extracted text, 13 ledger rows E-001..E-013, drafted brief | analysis/brief-text.txt, evidence.md, brief.md
- 2026-11-22 10:20 | frame | brief confirmed by PM (Q1 changed: public data into market figures) | brief.md, state.md
- 2026-11-22 10:20 | research-plan | 4 tickets RQ-01..RQ-04, frontier all 4; dev cost out of scope | questions.md
- 2026-11-22 10:21 | analyze-data | baseline gap decomposition from brief figures | analysis/01_baseline_gaps.py, evidence.md
- 2026-11-22 10:22 | collect | RQ-04 researcher: 15 rows E-054..E-068 (vendor benchmarks, B/C); support attach rate and invite acceptance not found | evidence.md
- 2026-11-22 10:22 | collect | RQ-01/02 researcher: rows E-014..E-028 + E-029 (H); no family-plan share, no router-SIM share, T2 not found | evidence.md
- 2026-11-22 10:25 | collect | RQ-03 researcher: rows E-034..E-053; rejected E-045, E-049, E-052 (no source URL); no measured effect of balance alerts on churn found; E-041 counter-evidence | evidence.md
- 2026-11-22 10:27 | analyze-data | options model: C/D/F/C+D-lite, base and unfavourable; no option closes 6 mln gap in year 1 | analysis/02_options_model.py, evidence.md
- 2026-11-22 10:28 | options | options.md: A, B, C, D, F + C+D-lite; recommend C | options.md, state.md
- 2026-11-22 10:35 | options | PM chose C | options.md, state.md
- 2026-11-22 10:36 | analyze-data | pilot sample/recruitment, funnel, payback per person-month, year-3 landmark | analysis/03_pilot_and_plan.py, evidence.md
- 2026-11-22 10:39 | strategy | strategy.md + deliverable.md (5 parts, RU) for option C | strategy.md, deliverable.md
- 2026-11-22 10:43 | red-team | blind review: 11 findings; corrected model 04 (campaign separated, consent/free-volume pool, dates, D base); E-073..E-077,E-079,E-081,E-084,E-086 superseded by E-088..E-095; C's own effect small, choice reopened | analysis/04_corrected_model.py, evidence.md
- 2026-11-22 10:43 | checkpoint | stage back to researched; strategy/deliverable marked as under revision | state.md, strategy.md, deliverable.md
- 2026-11-22 10:46 | analyze-data | plan checks: offer A/B size, D-lite pilot size, payback of chosen plan; brief rule rows E-100..E-102 | analysis/05_plan_checks.py, evidence.md
- 2026-11-22 10:51 | strategy | v2 rewrite after red-team: options.md, strategy.md, deliverable.md for C2; red-team findings 1-11 addressed | options.md, strategy.md, deliverable.md, state.md
- 2026-11-22 10:56 | strategy | PM approved C2 strategy | state.md, strategy.md
- 2026-11-22 10:57 | decision-log | D-001 drafted, owner pending PM confirmation (planned year assumed 2027) | decisions.md
- 2026-11-22 10:58 | decision-log | D-001 active, owner confirmed | decisions.md, state.md
- 2026-11-22 10:59 | retro | retro.md: preregistered criteria, this-run metrics, errors, 6 ranked improvements; baselines pending PM approval | retro.md
- 2026-11-22 13:57 | retro | plain-chat baseline started (PM approved: «Да, запустить»); opus subagent, brief text only, no repo instructions, no web
- 2026-11-22 14:01 | retro | plain-chat baseline done (≈3 min, ≈$0.7 P); scored on preregistered criteria; 5 errors found in its answer | projects/family-connect/baseline/plain-chat.md, projects/family-connect/retro.md
- 2026-11-22 14:05 | retro | PM approved improvements 1-3: options skill §3a shared levers; validation.md pool/start-date/clustering; researcher rule 6 + check.py UNOPENED rule. New rule withdrew E-036..E-039; deliverable line 80 recited E-011 | .claude/skills/options/SKILL.md, knowledge/methods/validation.md, .claude/agents/researcher.md, scripts/check.py, projects/family-connect/evidence.md, projects/family-connect/deliverable.md
- 2026-11-22 14:27 | retro | PM kept budget at $10 (declined raise to $14); skipped synthetic interviews, hand checks, retro update; ran export only

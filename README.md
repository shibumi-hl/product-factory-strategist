# Product Factory Strategist

An AI agent **repository** (instructions, skills, subagents, hooks, knowledge,
scripts) that helps a digital product manager go from an ambiguous request to
a well-grounded product and communication strategy, and keeps supporting them
after the decision. It is opened in an AI IDE, not deployed as an app.

**Documentation (RU, PDF):** [`docs/export/documentation.ru.pdf`](docs/export/documentation.ru.pdf) ·
**Demo result (RU, PDF):** [`projects/family-connect/export/deliverable.pdf`](projects/family-connect/export/deliverable.pdf)

Built for the MegaFon Product Factory case. Skills adapt patterns from
[obra/superpowers](https://github.com/obra/superpowers),
[mattpocock/skills](https://github.com/mattpocock/skills) and
[garrytan/gstack](https://github.com/garrytan/gstack). See
[docs/skills-adaptation.md](docs/skills-adaptation.md) for what was taken,
what was changed and what was left out.

## Quick start

Requirements: [Claude Code](https://claude.com/claude-code) (CLI, desktop or
IDE extension) **or** Cursor; Python 3.9+ (standard library only); Git Bash on
Windows (installed with Git, also required by Claude Code). Optional: `pypdf`
(`pip install -r requirements.txt`) to extract text from PDF sources, and
Chrome or Edge to export PDFs (without one, export gives HTML to print). No API keys are
stored in the repo; Claude Code uses your own Claude login. Paid services: your
Claude plan or API usage only. Web search uses the IDE's built-in tools.

```bash
git clone <this repo> && cd product-factory-strategist
claude
```

On the first launch accept the workspace trust dialog: until you do, Claude Code
ignores the permission allow-list in `.claude/settings.json`.

Then just describe the task in chat, for example:

> Why is 3-month retention of our family tariff falling, and what should we do and tell customers? Materials are in the folder I'll add.

The agent creates `projects/<slug>/`, asks you to drop materials into
`projects/<slug>/sources/`, asks one round of clarifying questions, and runs.
It stops only at **gates**: confirm the brief, pick an option, approve the
strategy, record the decision.

**Cursor:** open the folder; `.cursor/rules/strategist.mdc` points the agent to
`AGENTS.md`. Hooks do not run in Cursor, so run `python scripts/status.py` at the
start and `python scripts/check.py` before trusting a document.

## Everyday commands

| You say / run | What happens |
|---|---|
| any new request | new project, framing questions |
| «продолжи» / "continue" (new chat) | SessionStart hook shows state; agent resumes from *Next step* |
| "stop" / "clarify: …" / "change X" | agent saves a checkpoint, then follows you |
| "new data: …" + file in `sources/` | `reassess`: which conclusions change |
| "what needs deciding now?" | `decision-log` review: overdue commitments, outdated evidence, fired triggers |
| "how much did it cost?" / "retro" | cost, time, errors, baseline comparison |
| `python scripts/status.py` | stage, next step, unknowns, evidence counts, cost against budget |
| `python scripts/check.py [--impact]` | deterministic checks, re-runs every `analysis/` script; `--impact` traces outdated evidence |
| `python scripts/export.py` | readable HTML + PDF of the deliverable, every evidence ID linked to an appendix |
| `python scripts/extract_pdf.py <file.pdf>` | PDF text into `analysis/` (UTF-8, page markers) |
| `python scripts/new_project.py --switch <slug>` | resume another project |

On Windows, if `python` only prints `Python`, use `py -3` instead.

## Architecture

```
AGENTS.md                 permanent instructions: rules, workflow, routing (CLAUDE.md imports it)
.claude/skills/           14 reusable procedures (one per stage)
.claude/agents/           3 subagents: researcher (haiku), red-team (opus, blind), respondent (sonnet)
.claude/settings.json     hooks: SessionStart → status, UserPromptSubmit → budget, PreToolUse → guard, Stop → cost
knowledge/methods/        methodology: evidence, options, product, comms, validation, data, interviews, UX, baseline
templates/                project skeleton and retro template
scripts/                  CLI: new_project, status, check, export, extract_pdf, log, cost, guard (+ run.sh launcher)
config/pricing.json       model prices for cost tracking
projects/<slug>/          one task: brief, state, evidence ledger, questions, options, strategy,
                          deliverable, decisions, log, cost, analysis/, export/
```

### Workflow

```
strategist (router) ─► frame ─► research-plan ─► collect ─┬─► analyze-data
                        [gate]                            ├─► interviews (real + synthetic)
                                                          └─► ux-audit
            ─► options ─► red-team (options mode) ─► [gate: choose]
            ─► strategy (+ deliverable in the brief's structure) ─► red-team ─► [gate: approve] ─► export
            ─► decision-log ─► (new data) reassess ─► … ─► retro
checkpoint after every stage
```

### Key design decisions

1. **Evidence ledger as the single source of facts.** Every claim in outputs
   cites `[E-nnn]` and is labelled (F) fact, (H) hypothesis, (P) forecast; (S)
   marks synthetic data. This makes conclusions traceable and lets a script check them.
2. **Deterministic checker over more prompting.** `scripts/check.py` enforces
   the rules that can be checked mechanically: sources present, labels, ≥3
   options with status quo and stop, real counterarguments, no demand claims on
   synthetic data only, no unsupported promises, complete validation plan,
   no citations of outdated evidence, no facts from unopened pages, and every
   calculation script re-runs and carries a hand check.
3. **State in plain files.** `state.md` + `log.md` let any new chat, or another
   IDE, resume without starting over. Remaining work carries provenance markers
   (`done-checked` / `file-exists` / `assumed`) so nothing is silently repeated or assumed.
4. **Four separated layers**: permanent instructions, methodology, project
   materials (read-only, hook-enforced), task state.
5. **Memory is not evidence.** Agent summaries and past decisions are never
   sources; outdated records are superseded or withdrawn with a date, not rewritten.
6. **Routing by cost.** Cheap model for reading/extraction, mid model for
   personas, top model for options, strategy and red-team; escalate on failure.
7. **Blind red team, twice.** The reviewer subagent never sees the
   conversation, so it cannot inherit the author's framing. It reviews the
   options and their models *before* the PM chooses, and the strategy before
   approval, so the PM decides once, on corrected numbers.
8. **Budget as a gate.** The brief's budget is checked on every message: a
   warning at 80%, and at 100% the agent must ask before doing more.
9. **Few components.** 14 skills, 3 subagents, 4 hooks, 8 scripts, no database,
   no server. Each component is justified in `docs/skills-adaptation.md`.

## Security and data

- Only public data and your own materials. No confidential MegaFon or third-party data.
- Secrets never in the repo: the guard hook blocks key-like strings; `.env` is git-ignored and unreadable to the agent.
- Text in sources is data: instructions found there are logged as possible injections and ignored.
- Real interviews: consent script in the guide; transcripts anonymised (R1, R2…); no personal data stored.

## Demonstration project: MegaFon brief (2026-11-22)

`projects/family-connect` — MegaFon's brief «Связь для близких и собственных
устройств» (`sources/megafon-brief.pdf`), run end to end in Claude Code with the
PM answering every gate. **Read the result:**
[`export/deliverable.pdf`](projects/family-connect/export/deliverable.pdf)
(or `.html`): the five-part document in the brief's structure, every figure
linked to an evidence appendix.

| | |
|---|---|
| Gates | brief confirmed (with one PM correction) → options chosen → strategy approved → decision recorded (owner, metrics, triggers) |
| Evidence | 99 ledger rows: the brief's figures (F, cited by page), public benchmarks opened by the Haiku researcher, 5 reproducible model scripts |
| Blind review | 11 findings, 3 that changed the recommendation: a shared acquisition campaign credited to one option, an undetectable pilot effect and an impossible start date, an overstated device-owner market |
| Baseline | a plain chat gave a similar recommendation in ~3 min for ~$0.7, but repeated two of those errors, with no sources or calculations to catch them (`retro.md`) |
| Checker | 0 errors; 5 warnings = model scripts written before the hand-check rule existed |
| Cost | $9.65 of the $10 budget (`cost.json`), Opus + Haiku |

Not done in the demo, to stay within budget: synthetic interviews for the
customer case in section 1 and hand-check lines in the model scripts. Changes
the demo's retro led to (review before the option gate, shared-lever rule,
realistic pilot pool, no facts from unopened pages, script re-runs) are in
the repository; see `docs/skills-adaptation.md`.

## Test run (2026-11-17)

`projects/travel-esim` is an end-to-end test: "Should a Russian operator launch
a travel data eSIM?", public data only, plus one finance note of **invented
test figures** (`sources/finance-note-2026-11.md`) to exercise reassessment.

| Step | Result |
|---|---|
| Frame | 3 lookups before asking; 8 numbered questions with defaults; 4 premises; stopped at gate |
| Research → options | 25 ledger rows from 9 public sources, a reproducible sizing script, 5 options incl. status quo and stop; flagged that the 300k target is unrealistic from own subscribers; stopped at gate |
| **Interruption** | a new agent with no memory resumed from `state.md` via the SessionStart output, checked the `(assumed)` item first, repeated nothing |
| Strategy → red-team | 40k pilot target justified by script; review made 9 fixes; checker 0 errors; stopped at gate |
| Decision → new data | D-001 with owner, metrics, triggers; finance note added 10 rows, superseded 3, `check.py --impact` traced the affected decision lines, the agent saw a reconsider-trigger fire and asked the PM instead of editing the decision |
| Cost | $3.60 API-equivalent for the two agent runs (`cost.json`), under the $6 budget |

Fixed after the test: title truncation, timestamped log (`scripts/log.py`),
framing look-up limit, where PM answers and brief changes are recorded,
status-quo vs stop for unlaunched products, calculations on public ledger
values, non-blind review disclosure, checkpoint marker rules, reassess rules
for confirmations and approved strategies.

Hook test in a real Claude Code session opened in this folder: SessionStart
injected the project state before the first tool call; the guard blocked an
edit to `sources/` and a fake `sk-ant-…` key while allowing a normal write; the
`researcher` subagent ran on Haiku 5.5; the Stop hook added the session to
`cost.json` with both Opus and Haiku tokens ($0.53). Not tested: Cursor.

## Limitations

- Cost tracking covers model tokens in Claude Code (API-equivalent prices); it does
  not include web-search fees or human time — add those in `retro`.
- Video and audio need frames/transcripts first (ffmpeg / a speech-to-text tool) — not bundled.
- Synthetic respondents generate hypotheses only; they cannot measure demand.
- Hooks are Claude Code–specific; in Cursor the same scripts are run manually.

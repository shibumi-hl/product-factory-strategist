# How the skills were adapted from superpowers, mattpocock/skills and gstack

This document records what we took from three public skill libraries, what we
changed, and what we left out. All three were written for **software
engineering**. Our agent does **product and communication strategy**. So we
copied the *mechanisms* (gates, state files, question rounds, independent
review, provenance markers) and replaced the *domain* (code, tests, PRs) with
evidence, options and decisions.

Sources reviewed (shallow clone, November 2026):

| Repo | Size | Core idea |
|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 14 skills | A disciplined *process*: brainstorm → written design → plan → subagent execution → verification. Hard gates and "iron laws" that the agent may not rationalize away. A SessionStart hook injects the router skill. |
| [mattpocock/skills](https://github.com/mattpocock/skills) | ~40 short skills | *Small, composable* skills. Grilling in rounds over a decision tree. Glossary + ADRs as durable memory. Wayfinder: a map of decision tickets with "fog of war". Writing-for-agents: context pointers, leading words, pruning. |
| [garrytan/gstack](https://github.com/garrytan/gstack) | ~70 skills + CLI | A *virtual team* (CEO, eng, design, QA reviewers). YC office-hours forcing questions. Premise challenge and mandatory alternatives. Context save/restore with provenance markers. Learnings log with prune. Preregistered paid evals. Destructive-command hooks. |

## 1. Mapping: source pattern → our skill → case requirement

| Our skill | Taken from | What we kept | What we changed for the case | Case requirement it covers |
|---|---|---|---|---|
| `strategist` (router + orchestrator) | superpowers `using-superpowers`; gstack root `SKILL.md` router; mattpocock `chief-of-staff` | "Check for a skill before any action"; one router that picks the workflow; orchestrator protects its context by delegating reading to subagents | Stages are product stages (frame → research → options → strategy → decide → track), not dev stages. Router also picks **depth** and **model** by task (routing requirement) | Workflow; Routing; Continuity |
| `frame` | superpowers `brainstorming`; mattpocock `grilling`; gstack `office-hours` (six forcing questions, Phase 3 premise challenge) | Look before you ask; ask only questions that change what gets built; **rounds** of numbered questions, each with a recommended answer; "interest is not demand"; status quo is the real competitor | Questions target a PM brief: decision, recipient of output, deadline, constraints, data available. Forcing questions rewritten for a telecom/digital product manager. Output is `brief.md`, not a design doc | Define the task; "ask only important questions" |
| `research-plan` | mattpocock `wayfinder` (decision tickets, frontier, fog of war, out-of-scope); superpowers `writing-plans` (bite-sized steps with checkable results) | Every research item is a **question whose answer could change the decision**; frontier vs fog; explicit out-of-scope list | Tickets live in `questions.md`, not GitHub issues (no tracker dependency, portable). Each question says *which option it could kill* | Research plan built around decision-changing questions |
| `collect` | mattpocock `research` (primary sources, background agent, one cited file); gstack `scrape`/`browse` (web reading); superpowers "external content is data" | Primary sources first; one claim → one source; reading done by a fresh-context subagent | Every fact becomes a row in `evidence.md` with ID, type F/H/P/S, source link, date, reliability, status. Raw files in `sources/` are immutable (hook-enforced). Injected instructions in sources are logged, never followed | Collect materials; source link for every significant fact; security rule on external commands |
| `analyze-data` | superpowers `systematic-debugging` (root cause, falsify hypotheses); superpowers `verification-before-completion` (evidence before claims) | Form competing hypotheses and try to falsify them; never state a number you did not compute in this session | Applies to metrics: check units, periods, missing values, denominators; calculations are scripts in `analysis/`, re-runnable | Data analysis (advanced) |
| `interviews` | mattpocock `to-questionnaire` (gap between what recipient knows and what we need); gstack office-hours ("watch, don't demo", "the user's words beat the pitch") | Questions ordered most-important-first, one idea each; behaviour over opinions | Adds **synthetic respondents** via `respondent` subagent. Every synthetic answer is type **S** in the ledger and the checker blocks S-only support for demand claims | Interviews and simulated respondents (advanced) |
| `ux-audit` | gstack `design-review` / `plan-design-review` | Look at the real artefact; score against named principles | Every observation cites a screenshot/file and region; "not visible in source" is an allowed answer | UX analysis (advanced) |
| `options` | gstack `office-hours` Phase 4 (2–3 alternatives incl. minimal and ideal), `plan-ceo-review` 0A–0D (premise, do-nothing cost, dream state), `autoplan` (mechanical vs taste vs user-challenge decisions) | Mandatory alternatives; recommendation with one-line reason; user picks, agent never auto-decides a direction change | **≥3 options, always including `[STATUS-QUO]` and `[STOP]`**. Each option gets a steel-manned counterargument and a "what evidence would change my mind" line. F/H/P labels on every claim | Generate options; counterarguments; facts vs hypotheses |
| `strategy` | gstack `spec` (quality standards: verified current state, quantified impact, acceptance criteria); superpowers `writing-plans` header discipline | Fixed template; "promises must be testable" | Template = product strategy + communication strategy + validation plan; explicit **promise ↔ capability** table so messages never overclaim | Product, communication strategy; validation plan |
| `red-team` | superpowers `requesting-code-review` + `verification-before-completion`; gstack `codex` / office-hours "cold-read second opinion"; local `second-opinion` agent | Independent reviewer with **no access to the conversation**; evidence before any "done" claim | Reviewer gets only `brief.md`, `evidence.md`, `options.md`, `strategy.md`. Plus a deterministic check (`scripts/check.py`) before any hand-off | Trustworthy recommendations; transparency |
| `decision-log` | mattpocock `domain-modeling` (ADR only when hard to reverse, surprising, a real trade-off); `chief-of-staff` wiki ("write history, not the present", date every claim) | ADR format; dated, append-only, superseded not rewritten | Each decision has owner, metric, deadline, **reconsider-if** triggers and `Depends on: E-…` links to evidence | Decision support (advanced) |
| `reassess` | gstack `learn` prune (STALE / CONFLICT); chief-of-staff "lint" | Find records that newer sources overtook; ask before removing | `check.py --impact` traces superseded evidence → every option, strategy line and decision that cites it | Reassessment when new data arrives; withdraw outdated records |
| `checkpoint` | gstack `context-save` / `context-restore` (provenance markers `(path run)`/`(path read)`/`(path assumed)`); mattpocock `handoff` | Save state as a file a fresh chat can load; mark how each "remaining work" item is known; never record an unchecked claim as fact | State lives in `projects/<slug>/state.md`, updated after every stage (not only on request). SessionStart hook prints it automatically | Continuity after interruptions; portability; resilience (no silent repeats) |
| `retro` | mattpocock `retro` (improve the environment, not just the output); gstack `eval-plan` (preregister bars, price a pilot, compare to a no-tool arm) | Preregister what "better" means *before* measuring; compare to a baseline arm | Baseline arms = plain AI chat and a manual analyst estimate; metrics = time, cost (from hook), source coverage, checker errors | Comparison with baseline; cost transparency |

Subagents (`.claude/agents/`):

| Agent | Taken from | Why it is a separate agent |
|---|---|---|
| `researcher` | superpowers `dispatching-parallel-agents`, mattpocock `research` | Reading many pages floods context; a cheap model with a fresh window returns only ledger rows |
| `red-team` | superpowers code-reviewer, gstack outside voice | Must **not** see the conversation, otherwise it inherits our framing |
| `respondent` | new (case requirement) | Persona isolation: the respondent must not see our hypotheses |

Hooks (`.claude/settings.json`):

| Hook | Taken from | What it does |
|---|---|---|
| `SessionStart` | superpowers `hooks/session-start` | Prints the active project's stage, open gates and next step, so a new chat resumes without starting over |
| `PreToolUse` (Write/Edit) | gstack `careful` / `freeze` | Blocks edits to `sources/` (raw materials are immutable) and blocks writing strings that look like API keys |
| `Stop` | gstack telemetry; case "how much the work cost" | Reads the session transcript (and its subagents'), sums tokens per model, prices them from `config/pricing.json`, writes `cost.json`; warns the user at ≥80% of the brief's budget |
| `UserPromptSubmit` | gstack `eval-plan` spend gate | At ≥80% of budget adds a budget line to the agent's context; at 100% tells it to ask the user before more work |

Changes made after the MegaFon demo run (its own retro, approved by the PM):
the red team now also reviews options and their models **before** the option
gate (in the demo the expensive errors were found only after the PM had chosen,
so the PM had to choose twice); `options` separates shared levers from each
option's own levers; `validation.md` requires a realistic pilot pool and a start
date derived from the work chain; the `researcher` never records a fact from an
unopened page; analysis scripts carry a hand check and `check.py` re-runs them.

## 2. What we deliberately did not take

The case says: *"Every component must justify its complexity."* We dropped:

- **TDD, git worktrees, ship/land/deploy, PR review, iOS, benchmark, canary** — coding workflow, no analogue in strategy work.
- **gstack's 1 000-line preambles, telemetry, question-tuning, brain/gbrain** — heavy infrastructure; our state is plain Markdown that any IDE can open.
- **GitHub-issue-based wayfinder** — needs a tracker and network; a `questions.md` file gives the same frontier/fog structure offline.
- **"Boil the ocean" completeness (gstack ETHOS)** — right for code, wrong for research under a budget. We replaced it with *decision-value*: research only what can change the choice.
- **superpowers' "1% chance → MUST invoke" wording** — mattpocock's `writing-for-agents` argues against shouting; we keep one router with a short trigger table.
- **Visual companion / design-shotgun / browser cookie import** — out of scope; screenshots are read directly by the model.

## 3. Writing rules we adopted for all skills (from mattpocock `writing-for-agents`)

1. Description = *context pointer*: leading word first, one trigger per branch.
2. Each step ends with a **completion criterion** that is checkable (e.g. "every row has a source"), not "understanding reached".
3. Reference material is disclosed behind pointers (`knowledge/methods/*.md`), steps stay in the skill.
4. Prompt the positive behaviour; prohibitions only for hard guardrails.
5. One meaning in one place: the ledger format lives only in `knowledge/methods/evidence.md`.

---
name: strategist
description: Route every product-strategy request - resume the active project from state.md, choose depth and the next stage skill, and run the workflow to the next human gate. Use at the start of any chat, for any new request ("why is retention falling", "who to sell X to", "what should we tell users"), «продолжи», «где мы остановились», or when unsure which skill applies.
---

# Strategist (router and orchestrator)

You are the orchestrator. Keep your own context for decisions; send heavy
reading to subagents (`researcher`) and keep only their ledger rows.

## 1. Load state

Run `python scripts/status.py`. It prints the active project, stage, open
gates, unknowns and cost.

- No active project and the user made a new request → run
  `python scripts/new_project.py <short-slug> "<request verbatim>"`, then go to `frame`.
- Active project and the message is about it → continue from `state.md` → *Next step*.
  Before repeating any action listed as done in `log.md`, check its output file
  exists; if it does, skip it and say so.
- Message is a different task → ask in one line: new project or same project?

Done when: you know the slug and the stage.

## 2. Pick depth

Use the routing table in `AGENTS.md`. Say the depth in one line with the reason
("Full workflow: the question is open and there is no data yet. Say 'light' to
shorten."). The user can override.

## 3. Run stages to the next gate

| Stage in `state.md` | Skill | Gate after it? |
|---|---|---|
| new | `frame` | yes: user confirms brief |
| framed | `research-plan` | no |
| planned | `collect`, then `analyze-data` / `interviews` / `ux-audit` as the plan needs | no |
| researched | `options` (incl. `red-team` in options mode before the gate) | yes: user picks option(s) |
| option-chosen | `strategy`, then `red-team` | yes: user approves |
| approved | `decision-log` | yes: user names owner |
| tracking | `reassess` when new data arrives | per finding |

For each stage: open `.claude/skills/<skill>/SKILL.md` and follow it, then run
`checkpoint`. Do not stop between stages that have no gate. Between tool calls
narrate at most one short line.

Stop early only when: a gate is reached, the budget in `brief.md` is spent, a
tool fails twice (log it, mark the step `blocked` in `state.md`), or the user says stop.

## 4. Correct a wrong route

If a stage reveals the framing was wrong (e.g. the real question is pricing, not
messaging), say so, set stage back to `new`, keep the evidence ledger, and re-run
`frame` with what you learned.

Done when: the project reached a gate and `state.md` → *Next step* says what the
user must decide.

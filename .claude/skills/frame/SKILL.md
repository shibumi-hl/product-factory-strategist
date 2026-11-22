---
name: frame
description: Frame an ambiguous product request into a brief - the decision to make, who receives the output, deadline, constraints, available data and success criteria - by reading materials first and grilling only on what changes the next step. Use for a new project, «уточни задачу», or when the router finds the framing wrong.
---

# Frame the task

Adapted from superpowers *brainstorming*, mattpocock *grilling* and gstack
*office-hours* forcing questions. Output: `projects/<slug>/brief.md`.

## 1. Look before you ask

Read the request and every file in `sources/`. Write down what they already
answer. A written brief often settles the decision, recipient, deadline and
required output already: then ask only about what it leaves open (it may say
which choices are the team's), and record its figures as ledger rows. Never ask what the materials answer. Before the first round you may
also do up to 3 quick web lookups for facts that would otherwise be questions
(market size, who already sells this); facts you keep go into `evidence.md`
and count against the brief's source budget.

## 2. Ask in rounds

The **frontier** is every open question whose prerequisites are settled. Ask
the whole frontier in one message, numbered, each with your recommended answer,
worded so "yes" accepts it:

```
**Q1 – Decision.** What will be decided with this work? I assume: whether to
scale the family tariff to all regions in Q3. Yes?
```

Ground to cover (territory, not a script):

- **Decision**: what choice will this inform, by whom, by when.
- **Recipient**: who reads the output and what format they act on.
- **Status quo**: what happens if nothing changes; what users do today instead.
- **Demand evidence**: strongest *behavioural* signal (usage, payment, churn), not "interest".
- **Specific user**: a concrete segment with a situation, not "everyone 18–45".
- **Constraints**: budget, time, legal, brand, technical limits.
- **Data**: what exists, what is approved, what must not be used.
- **Success**: which number moves, from what baseline, by when.

Push once on vague answers ("seamless", "young audience"): ask for the
measurable version. Facts you can look up yourself, look up instead of asking.
Stop asking when the frontier is empty or the user says "enough, use your
assumptions" — then record each remaining assumption as (H).

## 3. Challenge premises

List 2–4 premises the request takes for granted, e.g.:

```
PREMISES
1. Retention is falling because of the product, not because of price changes. (H)
2. The audience is the existing base, not new users. (H)
```

Ask the user to confirm or reject. Rejected premises become research questions.

## 4. Write the brief

Use `templates/project/brief.md`. Mark what came from the user, what came from
materials (with ledger IDs) and what is your assumption (H).

**Gate:** show the brief in ≤250 words and ask for confirmation. Copy the
user's answers verbatim into `brief.md` → *PM answers*. On yes, set stage
`framed` in `state.md`. If a later stage proposes changing a confirmed field
(e.g. the target), put the change to the user at that stage's gate and, once
accepted, record it in `brief.md` → *Change log*.

Done when: every brief field is filled or explicitly marked unknown, and the user confirmed.

---
name: ux-audit
description: Audit interfaces, user journeys and visual composition from screenshots, recordings or live public pages, grounding every observation in what is visible in a named source file and region. Use for screenshots or videos in sources/, «посмотри интерфейс», onboarding/checkout/tariff-page reviews, or competitor UX comparison.
---

# UX audit

Adapted from gstack *design-review* / *plan-design-review*. Checklist:
`knowledge/methods/ux.md`.

## 1. Inventory the material

List each screenshot, recording or page with what it shows (screen, step,
platform, date). Say what you **cannot** see (e.g. "no error states provided").
Capability limits: images and PDFs are read directly; video needs frames
extracted first (`ffmpeg -i in.mp4 -vf fps=1 frames/%03d.png` if installed);
audio needs a transcript.

## 2. Walk the journey

For the user's goal from the brief, go step by step: what the user must notice,
understand, decide and do on each screen.

## 3. Record observations

Each observation: what is visible → why it matters for the goal → severity
(blocks / slows / cosmetic). Cite `sources/<file>` and region ("top banner",
"step 3 of 5"). Observations are type F; their effect on behaviour is (H)
unless data shows it.

## 4. Compare

If competitor screens exist, compare the same step side by side.

Done when: every observation cites a file and region, the journey covers every
step of the brief's user goal, and gaps in the material are listed.

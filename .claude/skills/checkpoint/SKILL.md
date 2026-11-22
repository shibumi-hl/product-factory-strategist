---
name: checkpoint
description: Save the project state to state.md so work resumes in any new chat or IDE without starting over - stage, next step, decisions so far, unknowns, and remaining work marked with how it is known. Use at the end of every stage, before a pause, when context grows large, «сохрани», «на сегодня всё», or when the user says stop.
---

# Checkpoint

Adapted from gstack *context-save* / *context-restore* (provenance markers)
and mattpocock *handoff*. File: `projects/<slug>/state.md`. The SessionStart
hook and `scripts/status.py` read it.

## Update state.md

Keep the template's sections. Overwrite every section except *History*;
append one line to *History*.

- **Stage** — one of: new, framed, planned, researched, option-chosen, approved, tracking.
- **Next step** — one concrete action, and whether it waits on the user (gate).
- **Done** — stage outputs that exist, by file path.
- **Remaining work** — each item starts with `Open.` and ends with a marker:
  `(done-checked)` you opened the output and it is complete;
  `(file-exists)` the file exists, content not re-checked;
  `(assumed)` you believe it but did not check.
  Exactly one marker per item, nothing else in the parentheses. Finished
  items move to *Done*. On resume, items marked `(assumed)` are checked first.
- **Unknowns** — what we do not know and why.
- **Decisions so far** — one line each with a pointer (brief, options, D-nnn),
  including the chosen depth and your own process calls.

Never record a file's contents (counts, sections) as fact unless you read it in
this turn.

Run `python scripts/log.py <stage> checkpoint state.md`.

Done when: `python scripts/status.py` prints the new stage and next step.

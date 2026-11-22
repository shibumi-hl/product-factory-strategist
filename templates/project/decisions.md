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

---
id: "{{PROJECT_CODE}}-HND-LOG"
title: Handover Log
type: handover_log
status: active
owner: "{{HANDOVER_OWNER}}"
updated: "{{YYYY-MM-DD}}"
tags:
  - elaef/handover
---

# Handover Log

This log records material handover lifecycle events. Full handover content belongs in [[02_current_handover]] while active and `90_records/` after preservation.

## Lifecycle events

| Handover ID | Type | Prepared by | Receiver | Cutoff | Transfer status | Acceptance status | Preserved record | Evidence / notes |
|---|---|---|---|---|---|---|---|---|
| {{HANDOVER_ID}} | {{TYPE}} | {{OUTGOING}} | {{RECEIVER}} | {{TIMESTAMP}} | draft | not_assessed | — | Starter not instantiated |

## Logging rules

- Append material lifecycle events; do not erase prior acceptance or rejection history.
- Correct errors transparently with a dated correction.
- Link to the preserved record when a handover is superseded or closed.
- Do not report `accepted` without receiver acknowledgment evidence.
- Do not include secrets or restricted content merely to make the log self-contained.

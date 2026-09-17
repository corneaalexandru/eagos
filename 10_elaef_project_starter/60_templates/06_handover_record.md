---
id: "{{PROJECT_CODE}}-HND-{{SEQUENCE}}"
title: "{{HANDOVER_TITLE}}"
type: handover
handover_type: "{{TYPE}}"
status: draft
project_id: "{{PROJECT_CODE}}-PRJ-001"
prepared_by: "{{OUTGOING}}"
intended_receiver: "{{RECEIVER}}"
prepared_at: "{{YYYY-MM-DDTHHMMSSZ}}"
state_cutoff: "{{YYYY-MM-DDTHHMMSSZ}}"
expires_on:
acceptance_evidence: []
framework_version: 4.0.0
tags:
  - elaef/handover
---

# {{HANDOVER_TITLE}}

## Identity and references

- **Project:** [{{PROJECT_NAME}}](../README.md)
- **Project ID:** `{{PROJECT_CODE}}-PRJ-001`
- **Type:** {{TYPE}}
- **Outgoing:** {{OUTGOING}}
- **Receiver:** {{RECEIVER}}
- **State cutoff:** {{TIMESTAMP}}
- **Reference map:** [reference map](../50_handover/01_reference_map.md)
- **Last trusted revision:** {{REVISION_COMMIT_OR_SNAPSHOT}}

## Required reading

1. {{LINK}}
2. {{LINK}}

## Current state

- **Phase:** {{PHASE}}
- **Current task:** {{ID_AND_LINK}}
- **Next ready task:** {{ID_AND_LINK}}
- **Blocker:** {{BLOCKER}}
- **Gate:** {{GATE}}
- **Major risk:** {{RISK}}

## Authorization

- **Authorized envelope:** {{SCOPE}}
- **Prohibited actions:** {{ACTIONS}}
- **Authorization evidence:** {{LINKS}}

## Completed

| Task / change | Output | Evidence | Validation |
|---|---|---|---|
| {{ITEM}} | {{OUTPUT}} | {{EVIDENCE}} | {{RESULT}} |

## In progress

| Task | Exact state | Remaining criteria | Work product | Owner |
|---|---|---|---|---|
| {{ITEM}} | {{STATE}} | {{CRITERIA}} | {{LOCATION}} | {{OWNER}} |

## Failed, blocked, or unverified

- {{ITEM_AND_EVIDENCE}}

## Material decisions, changes, and uncertainty

- **Decisions:** {{LINKS}}
- **Changes:** {{LINKS}}
- **Open items:** {{LINKS}}
- **Assumptions:** {{LINKS}}
- **Contradictions:** {{LINKS}}
- **Stale evidence:** {{LINKS}}

## External actions

| Action | Status | Final-state evidence | Unconfirmed |
|---|---|---|---|
| {{ACTION_OR_NONE}} | {{STATUS}} | {{EVIDENCE}} | {{UNKNOWN}}

## Changed references

| Reference / path | Change | Validation |
|---|---|---|
| {{REFERENCE}} | {{CHANGE}} | {{RESULT}} |

## Next justified action

{{ACTION}}

## Outgoing completion

- **Result:** {{NOT_READY_READY_FOR_REVIEW}}
- **Validator:** {{VALIDATOR}}
- **Validation evidence:** {{EVIDENCE}}

## Transfer

- **Status:** {{NOT_TRANSFERRED_OR_TRANSFERRED}}
- **Method:** {{METHOD}}
- **Transferred at:** {{TIMESTAMP}}
- **Evidence:** {{EVIDENCE}}

## Receiver acceptance

- **Outcome:** {{NOT_ASSESSED_ACCEPTED_ACCEPTED_WITH_CONDITIONS_OR_REJECTED}}
- **Receiver:** {{RECEIVER}}
- **Assessed at:** {{TIMESTAMP}}
- **Scope accepted:** {{SCOPE}}
- **References verified:** {{REFERENCES}}
- **Differences discovered:** {{DIFFERENCES}}
- **Conditions / exclusions:** {{CONDITIONS}}
- **First task assumed:** {{ACTIVITY}}
- **Evidence:** {{EVIDENCE}}

## Expiry or revalidation

{{TRIGGER}}

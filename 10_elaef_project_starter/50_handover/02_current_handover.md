---
id: "{{PROJECT_CODE}}-HND-CURRENT"
title: Current Handover
type: handover
handover_type: "{{SESSION_AGENT_PHASE_PAUSE_OWNERSHIP_ENVIRONMENT_OR_CLOSURE}}"
status: draft
project_id: "{{PROJECT_CODE}}-PRJ-001"
prepared_by: "{{OUTGOING_OWNER_AGENT_OR_SESSION}}"
intended_receiver: "{{RECEIVER_OR_UNASSIGNED}}"
prepared_at: "{{YYYY-MM-DDTHHMMSSZ}}"
state_cutoff: "{{YYYY-MM-DDTHHMMSSZ}}"
expires_on:
acceptance_evidence: []
framework_version: 4.0.0
tags:
  - elaef/handover
---

# Current Handover

> [!warning] Draft
> This template is not a completed handover. Verify it against authoritative records and record transfer and acceptance evidence separately.

## Identity

- **Project:** [{{PROJECT_NAME}}](../README.md)
- **Project ID:** `{{PROJECT_CODE}}-PRJ-001`
- **Handover type:** {{TYPE}}
- **Outgoing:** {{OUTGOING}}
- **Intended receiver:** {{RECEIVER}}
- **Prepared:** {{TIMESTAMP}}
- **State cutoff:** {{TIMESTAMP}}
- **Reference map:** [reference map](01_reference_map.md)

## Trusted-state anchor

- **Last trusted project revision:** {{REVISION_COMMIT_SNAPSHOT_OR_STATE_RECORD}}
- **Validation date:** {{DATE}}
- **Validator:** {{VALIDATOR}}
- **Post-cutoff changes known:** {{NONE_OR_LIST}}

## Required reading order

1. [README](../README.md)
2. [project state](../00_control/01_project_state.md)
3. [project activation](../00_control/02_project_activation.md)
4. [execution plan](../00_control/03_execution_plan.md)
5. [reference map](01_reference_map.md)
6. {{PROJECT_SPECIFIC_CRITICAL_RECORDS}}

## Current execution state

- **Project status:** {{STATUS}}
- **Phase:** {{PHASE}}
- **Workstream:** {{WORKSTREAM}}
- **Current task:** {{ACTIVITY_ID_AND_LINK}}
- **Next ready task:** {{ACTIVITY_ID_AND_LINK}}
- **Critical blocker:** {{BLOCKER}}
- **Active gate:** {{GATE_ID_AND_LINK}}
- **Major risk:** {{RISK_ID_AND_LINK}}

## Authorization

- **Active envelope:** {{AUTHORIZED_SCOPE}}
- **Explicitly prohibited:** {{PROHIBITED_ACTIONS}}
- **Approver:** {{APPROVAL_OWNER}}
- **Authorization evidence:** {{LINKS}}

## Completed since prior handover

| Task / change | Output | Evidence | Validation | Authoritative records updated |
|---|---|---|---|---|
| {{ID_OR_DESCRIPTION}} | {{OUTPUT}} | {{EVIDENCE}} | {{RESULT}} | {{LINKS}} |

## In progress

| Task | Exact state | Work product | Remaining completion criteria | Owner | Safe next step |
|---|---|---|---|---|---|
| {{ACTIVITY_ID}} | {{STATE}} | {{LOCATION}} | {{CRITERIA}} | {{OWNER}} | {{NEXT_STEP}} |

## Attempted, failed, or rolled back

| Task | Attempt | Result | External consequence | Recovery state | Evidence |
|---|---|---|---|---|---|
| {{ID}} | {{WHAT_WAS_ATTEMPTED}} | {{RESULT}} | {{NONE_OR_CONSEQUENCE}} | {{STATE}} | {{LINKS}} |

## Material decisions and changes

- **Decisions:** {{LINKS_OR_NONE}}
- **Changes:** {{LINKS_OR_NONE}}
- **Overrides:** {{LINKS_OR_NONE}}

## Open and uncertain

- **Open items:** {{LINKS_OR_NONE}}
- **Material assumptions:** {{LINKS_OR_NONE}}
- **Contradictions:** {{LINKS_OR_NONE}}
- **Stale evidence:** {{LINKS_OR_NONE}}
- **Access failures:** {{REFERENCES_OR_NONE}}

## Files and records changed

| Reference / path | Change | Authority | Validation |
|---|---|---|---|
| {{REF_ID_OR_PATH}} | {{CHANGE}} | {{AUTHORITATIVE_WORKING_OR_DERIVED}} | {{RESULT}} |

## External actions

| Action | Status | Final-state evidence | Still unconfirmed |
|---|---|---|---|
| {{ACTION_OR_NONE}} | {{DRAFT_QUEUED_SENT_COMPLETED_FAILED_UNKNOWN}} | {{EVIDENCE}} | {{UNKNOWN}}

## Next justified action

{{ONE_ACTION_LINKED_TO_DEPENDENCIES_EVIDENCE_AND_AUTHORITY}}

## Outgoing validation

- [ ] Critical references resolve or failures are explicit
- [ ] Cutoff and trusted revision recorded
- [ ] Completed, in-progress, blocked, failed, and unverified work separated
- [ ] External consequences and final-state evidence recorded
- [ ] Gates and prohibited actions explicit
- [ ] Changed records listed
- [ ] Sensitive information protected
- [ ] Next action justified
- [ ] No silent contradiction with authoritative records

## Transfer

- **Status:** Not transferred
- **Transfer method:** {{METHOD}}
- **Transferred at:**
- **Transfer evidence:**

## Receiver acceptance

- **Outcome:** Not assessed
- **Receiver:** {{RECEIVER}}
- **Assessed at:**
- **Scope accepted:**
- **References verified:**
- **Differences discovered:**
- **Conditions / exclusions:**
- **First task assumed:**
- **Acceptance evidence:**

Allowed outcomes:

- `accepted`
- `accepted_with_conditions`
- `rejected`

## Expiry or revalidation trigger

{{DATE_MATERIAL_STATE_CHANGE_AUTHORITY_CHANGE_OR_ENVIRONMENT_CHANGE}}

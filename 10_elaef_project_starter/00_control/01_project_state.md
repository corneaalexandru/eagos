---
id: "{{PROJECT_CODE}}-CTL-STATE"
title: Project State
type: project_state
status: setup
updated: "{{YYYY-MM-DD}}"
write_owner: "{{WRITE_OWNER}}"
revision: 0
lifecycle_stage: discover
tags:
  - elaef/control
  - elaef/state
---

# Project State

> [!info] Authority
> This is the authoritative current-state record. Dashboards and summaries are derived views.

## State

- **Project status:** Setup
- **Current phase:** Phase 0 — Project setup
- **Current workstream:** Initialization
- **Current task:** {{CURRENT_ACTIVITY_ID_OR_TBD}}
- **Next ready task:** {{NEXT_ACTIVITY_ID_OR_TBD}}
- **Critical blocker:** {{MATERIAL_MISSING_INPUT_OR_NONE}}; activation controls subsequent execution, not authorized setup
- **Active gate:** {{PROJECT_CODE}}-GAT-ACTIVATION
- **Major open item:** {{OPEN_ITEM}}
- **Major risk:** {{RISK_ID_OR_TBD}}
- **Recent decision:** None confirmed
- **Activation:** `not_assessed`

## Authorization state

- **Read authority:** {{READ_SCOPE}}
- **Write authority:** {{WRITE_SCOPE}}
- **External-action authority:** None unless explicitly recorded
- **Approval authority:** {{APPROVAL_OWNER}}

## Current evidence posture

- **Highest material evidence level:** {{E0_E1_E2_E3_OR_E4}}
- **Stale evidence affecting execution:** {{YES_NO_UNKNOWN}}
- **Unresolved contradiction:** {{YES_NO_UNKNOWN}}

## Write state

- **Write owner:** {{WRITE_OWNER}}
- **Revision:** 0
- **Last validated:** {{YYYY-MM-DD_OR_NOT_VALIDATED}}
- **Validation result:** Not validated

## Next justified action

Complete [project activation](02_project_activation.md) prerequisites.

## Conversation checkpoint

- **Focus / authoritative pointer:** Use the current owner request
- **Last completed conversational move:** None recorded
- **Material owner corrections / alternatives:** None recorded
- **Next proposed move / unresolved point:** Contribute useful possibilities or resume the next ready task
- **Authority:** See Authorization state

State above owns current task and readiness. The lifecycle stage is descriptive and never passes a gate. Save a dated material correction in the change log rather than rewriting history.

## Idea and initiative pointers

| Seed / initiative ID | Title / origin | Authoritative record or brief provisional seed |
|---|---|---|

Keep early seeds as hypotheses without invented sources. Use [the initiative template](../60_templates/08_initiative.md) for sustained separate work. Each initiative owns its current state; this table is navigation. Preserve existing execution records and link to them.

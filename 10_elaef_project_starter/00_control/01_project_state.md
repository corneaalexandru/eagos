---
id: "{{PROJECT_CODE}}-CTL-STATE"
title: Project State
type: project_state
status: setup
updated: "{{YYYY-MM-DD}}"
write_owner: "{{WRITE_OWNER}}"
revision: 0
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
- **Current activity:** {{CURRENT_ACTIVITY_ID_OR_TBD}}
- **Next ready activity:** {{NEXT_ACTIVITY_ID_OR_TBD}}
- **Critical blocker:** Activation gate not assessed
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

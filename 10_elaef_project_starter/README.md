---
id: "{{PROJECT_CODE}}-PRJ-001"
title: "{{PROJECT_NAME}}"
type: project
status: setup
framework: ELAEF
framework_version: 3.5.0
conformance_profile: "{{P0_P1_OR_P2}}"
naming_profile: obsidian_portable_v1
numbering_profile: numbered_project_v1
owner: "{{PROJECT_OWNER}}"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
activation_status: not_assessed
tags:
  - elaef/project
---

# {{PROJECT_NAME}}

The [charter](00_control/00_project_charter.md) and [state](00_control/01_project_state.md) own project definition and current execution truth. This hub is navigation and a concise summary; reconcile it after material changes instead of maintaining independent decisions here.

> [!warning] Template state
> This project remains in `setup` until all material placeholders are replaced and [Project Activation](00_control/02_project_activation.md) is assessed. Folder creation is not project activation.

## Purpose

{{WHY_THIS_PROJECT_EXISTS}}

## Objective

{{SPECIFIC_INTENDED_OUTCOME}}

## Intended beneficiary

{{PERSON_GROUP_OR_SYSTEM_BENEFITING}}

## Success criteria

- {{MEASURABLE_SUCCESS_CRITERION}}

## Scope

### Included

- {{IN_SCOPE}}

### Excluded

- {{OUT_OF_SCOPE}}

## Constraints

- {{CONSTRAINT}}

## Current state

- **Phase:** Setup
- **Current workstream:** Project initialization
- **Current activity:** Complete activation prerequisites
- **Next ready activity:** Determine from [project activation](00_control/02_project_activation.md)
- **Critical blocker:** Unassessed activation gate
- **Active gate:** `{{PROJECT_CODE}}-GAT-ACTIVATION`
- **Major risk:** {{MAJOR_RISK_OR_UNKNOWN}}

## Authorization envelope

### Internally authorized

- Read and organize supplied project information.
- Prepare internal drafts and project records.
- Perform other reversible internal work explicitly allowed by `AGENTS.md`.

### Not authorized unless explicitly added

- Spending or purchasing
- External communication or outreach
- Publication or deployment
- Contracting, registration, hiring, or legal commitment
- Disclosure of confidential or personal information
- Destructive or effectively irreversible change

## Authoritative records

- **Charter:** [project charter](00_control/00_project_charter.md)
- **State:** [project state](00_control/01_project_state.md)
- **Execution and dependencies:** [execution plan](00_control/03_execution_plan.md)
- **Evidence:** [evidence register](00_control/04_evidence_register.md)
- **Decisions:** [decision log](00_control/05_decision_log.md)
- **Risks:** [risk register](00_control/06_risk_register.md)
- **Gates:** [gate register](00_control/07_gate_register.md)
- **Activation:** [project activation](00_control/02_project_activation.md)
- **Material changes:** [change log](00_control/08_change_log.md)
- **Agent operating contract:** [AGENTS](AGENTS.md)
- **Handover system:** [handover hub](50_handover/00_handover_hub.md)
- **Reference map:** [reference map](50_handover/01_reference_map.md)
- **Current handover:** [current handover](50_handover/02_current_handover.md)
- **Handover lifecycle:** [handover log](50_handover/03_handover_log.md)

## Current focus

Complete the activation assessment without inferring facts, decisions, or authority from placeholders.

## Next justified action

Replace project-definition placeholders in [project charter](00_control/00_project_charter.md).

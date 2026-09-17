---
id: "{{PROJECT_CODE}}-PRJ-001"
title: "{{PROJECT_NAME}}"
type: project
status: setup
framework: EAGOS
framework_version: 4.0.0
conformance_profile: "{{P0_P1_OR_P2}}"
naming_profile: portable_markdown_v1
numbering_profile: numbered_project_v1
owner: "{{PROJECT_OWNER}}"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
activation_status: not_assessed
tags:
  - eagos/project
---

# {{PROJECT_NAME}}

The [charter](00_control/00_project_charter.md) owns project definition; [state](00_control/01_project_state.md) owns current execution truth. This hub provides navigation and a derived summary.

This project starts in `setup`. Complete the relevant records and assess [activation](00_control/02_project_activation.md) before subsequent execution. Authorized setup can prepare that assessment.

Use [the operating guide](01_operating_guide.md) and ordinary instructions such as "help me find an idea," "continue," "review," or "let's launch it." The agent should contribute possibilities and propose the next useful move. For several initiatives, keep stable pointers in the state record and use the [initiative template](60_templates/08_initiative.md) when sustained work warrants a separate record.

## Current state

- **Phase:** Setup
- **Current focus:** Define the project from supplied information
- **Current task:** Confirm readiness of `{{PROJECT_CODE}}-ACT-0001` in the [execution plan](00_control/03_execution_plan.md)
- **Blocker:** {{MATERIAL_MISSING_INPUT_OR_NONE}}
- **Activation:** `not_assessed`; applies to subsequent execution
- **Major risk and next action:** See [state](00_control/01_project_state.md)

## Authorization envelope

Record actual read, write, external-action, and approval authority in [state](00_control/01_project_state.md), with the source instruction or decision. A setup request may authorize internal preparation within its scope. This template grants no permission.

Spending, outreach, publication, deployment, contracting, registration, hiring, disclosure, and materially destructive change require explicit applicable authority and any required gate.

## Authoritative records

| Information | Location |
|---|---|
| Purpose, objective, beneficiary, success criteria, scope, and constraints | [Charter](00_control/00_project_charter.md) |
| State, authority, risks/blockers, and next action | [State](00_control/01_project_state.md) |
| Tasks and dependencies | [Execution plan](00_control/03_execution_plan.md) |
| Evidence | [Evidence register](00_control/04_evidence_register.md) |
| Decisions | [Decision log](00_control/05_decision_log.md) |
| Risks | [Risk register](00_control/06_risk_register.md) |
| Gates and activation | [Gate register](00_control/07_gate_register.md), [activation assessment](00_control/02_project_activation.md) |
| Material changes | [Change log](00_control/08_change_log.md) |
| Agent instructions | [AGENTS](AGENTS.md) |
| Continuity and references | [Handover hub](50_handover/00_handover_hub.md), [reference map](50_handover/01_reference_map.md) |
| Current handover and lifecycle | [Current handover](50_handover/02_current_handover.md), [log](50_handover/03_handover_log.md) |

## Next justified action

Use the actual owner request to fill the [charter](00_control/00_project_charter.md). Preserve unknowns; do not infer facts, decisions, or authority from template text.

## Organization and operating controls

Add only the records needed for actual work: [agent roles](60_templates/09_agent_role.md), [delegation](60_templates/10_delegation.md), [runtime deployment](60_templates/11_runtime_deployment.md), [recurring process](60_templates/12_recurring_process.md) and [Task attempts](60_templates/13_task_attempt.md). Their templates are proposals, not configured agents or granted authority.

Keep a responsibility chart and, when software is deployed, a separate role-to-instance map. The owner view should show purpose, knowledge/uncertainty, responsible roles, ready/blocked Tasks and pending decisions. The portable operating guide contains the shared rules; load detailed EAGOS organization/runtime guidance from the distribution when needed.

For an optional owner interface, define its sources, approval controls, runtime status and acceptance evidence in the [dashboard contract](60_templates/14_dashboard_contract.md).

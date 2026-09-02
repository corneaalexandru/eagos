---
id: "{{PROJECT_CODE}}-CTL-EXECUTION"
title: Execution Plan
type: execution_plan
status: setup
updated: "{{YYYY-MM-DD}}"
write_owner: "{{WRITE_OWNER}}"
revision: 0
tags:
  - elaef/control
  - elaef/execution
---

# Execution Plan

## Hierarchy

- **L1 Project:** {{PROJECT_NAME}}
- **L2 Workstream:** Project initialization
- **L3 Phase:** Phase 0 — Setup
- **L4 Deliverable:** Activation-ready project system

## Immediate Level 5 activities

### {{PROJECT_CODE}}-ACT-0001 — Instantiate project charter

- **Purpose:** Replace project-definition placeholders with authorized information.
- **Expected output:** Completed [[00_project_charter]].
- **Predecessors:** None.
- **Successors:** `{{PROJECT_CODE}}-ACT-0002`.
- **Evidence required:** Project-owner input and supplied project information.
- **Required evidence level:** E1 for initial definition; higher where consequence requires.
- **Owner:** {{PROJECT_OWNER}}
- **Write owner:** {{WRITE_OWNER}}
- **Status:** `ready`
- **Risks / blockers:** Project objective or authority may be unclear.
- **Gate:** {{PROJECT_CODE}}-GAT-ACTIVATION
- **Reversibility:** R1
- **Completion criteria:** Material placeholders resolved; facts and assumptions distinguished; owner validates meaning.
- **Related records:** [[00_project_charter]], [[01_project_state]]

### {{PROJECT_CODE}}-ACT-0002 — Establish initial project state

- **Purpose:** Create a trusted current-state baseline.
- **Expected output:** Updated [[01_project_state]], registers, and dependencies.
- **Predecessors:** `{{PROJECT_CODE}}-ACT-0001`.
- **Successors:** `{{PROJECT_CODE}}-ACT-0003`.
- **Evidence required:** Completed charter and classified project information.
- **Owner:** {{WRITE_OWNER}}
- **Status:** `not-started`
- **Gate:** {{PROJECT_CODE}}-GAT-ACTIVATION
- **Reversibility:** R1
- **Completion criteria:** Current activity, next activity, blocker, gate, major risk, authority, and revision are explicit.

### {{PROJECT_CODE}}-ACT-0003 — Establish project reference map

- **Purpose:** Make authoritative notes, folders, evidence, outputs, private locations, and environments discoverable for continuity.
- **Expected output:** Verified critical references in [[../50_handover/01_reference_map]].
- **Predecessors:** `{{PROJECT_CODE}}-ACT-0002`.
- **Successors:** `{{PROJECT_CODE}}-ACT-0004`.
- **Evidence required:** Existing project architecture and reachable authoritative records.
- **Owner:** {{WRITE_OWNER}}
- **Status:** `not-started`
- **Gate:** {{PROJECT_CODE}}-GAT-ACTIVATION
- **Reversibility:** R1
- **Completion criteria:** Project root, hub, state, execution, activation, evidence, decision, risk, gate, change, handover, and material controlled locations are mapped; critical references verified; failures explicit.

### {{PROJECT_CODE}}-ACT-0004 — Assess activation gate

- **Purpose:** Determine whether execution can safely begin.
- **Expected output:** Evidence-backed outcome in [[02_project_activation]].
- **Predecessors:** `{{PROJECT_CODE}}-ACT-0003`.
- **Successors:** First project-specific execution activity.
- **Evidence required:** All activation criteria or explicit conditions.
- **Owner:** {{APPROVAL_OWNER}}
- **Status:** `not-started`
- **Gate:** {{PROJECT_CODE}}-GAT-ACTIVATION
- **Reversibility:** R1
- **Completion criteria:** Outcome, approver, evidence, envelope, prohibited actions, and first authorized activity recorded.

## Blocked activities

- Project-specific execution is blocked until activation is `READY` or `READY WITH CONDITIONS`.

## Future work

Define only to Levels 2–4 until activation and early evidence justify Level 5 detail.

## Dependency rule

An activity becomes `ready` only when predecessors, inputs, evidence, scope, authorization, and applicable gates are satisfied.

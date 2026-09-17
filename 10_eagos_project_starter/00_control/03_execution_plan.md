---
id: "{{PROJECT_CODE}}-CTL-EXECUTION"
title: Execution Plan
type: execution_plan
status: setup
updated: "{{YYYY-MM-DD}}"
write_owner: "{{WRITE_OWNER}}"
revision: 0
tags:
  - eagos/control
  - eagos/execution
---

# Execution Plan

## Hierarchy

- **L1 Project:** {{PROJECT_NAME}}
- **L2 Workstream:** Project initialization
- **L3 Phase:** Phase 0 — Setup
- **L4 Deliverable:** Activation-ready project system

## Immediate Tasks

These proposed **setup tasks** may proceed under an applicable request to initialize the project. Confirm the actual scope and inputs before marking the first task ready. The activation gate is their deliverable and successor boundary, not a predecessor. They may prepare records and assess readiness while project-specific execution remains gated.

### {{PROJECT_CODE}}-ACT-0001 — Instantiate project charter

- **Purpose:** Replace project-definition placeholders with authorized information.
- **Expected output:** Completed [project charter](00_project_charter.md).
- **Predecessors:** None.
- **Successors:** `{{PROJECT_CODE}}-ACT-0002`.
- **Evidence required:** Project-owner input and supplied project information.
- **Required evidence level:** E1 for initial definition; higher where consequence requires.
- **Owner:** {{PROJECT_OWNER}}
- **Write owner:** {{WRITE_OWNER}}
- **Status:** `proposed`
- **Risks / blockers:** Project objective or authority may be unclear.
- **Gate relationship:** Prepares {{PROJECT_CODE}}-GAT-ACTIVATION; no activation passage required for authorized setup
- **Reversibility:** R1
- **Completion criteria:** Material placeholders resolved; facts and assumptions distinguished; owner validates meaning.
- **Related records:** [project charter](00_project_charter.md), [project state](01_project_state.md)

### {{PROJECT_CODE}}-ACT-0002 — Establish initial project state

- **Purpose:** Create a trusted current-state baseline.
- **Expected output:** Updated [project state](01_project_state.md), registers, and dependencies.
- **Predecessors:** `{{PROJECT_CODE}}-ACT-0001`.
- **Successors:** `{{PROJECT_CODE}}-ACT-0003`.
- **Evidence required:** Completed charter and classified project information.
- **Owner:** {{WRITE_OWNER}}
- **Status:** `not-started`
- **Gate relationship:** Prepares {{PROJECT_CODE}}-GAT-ACTIVATION; authorized setup may proceed before passage
- **Reversibility:** R1
- **Completion criteria:** Current task, next task, blocker, gate, major risk, authority, and revision are explicit.

### {{PROJECT_CODE}}-ACT-0003 — Establish project reference map

- **Purpose:** Make authoritative notes, folders, evidence, outputs, private locations, and environments discoverable for continuity.
- **Expected output:** Verified critical references in [reference map](../50_handover/01_reference_map.md).
- **Predecessors:** `{{PROJECT_CODE}}-ACT-0002`.
- **Successors:** `{{PROJECT_CODE}}-ACT-0004`.
- **Evidence required:** Existing project architecture and reachable authoritative records.
- **Owner:** {{WRITE_OWNER}}
- **Status:** `not-started`
- **Gate relationship:** Prepares {{PROJECT_CODE}}-GAT-ACTIVATION; authorized setup may proceed before passage
- **Reversibility:** R1
- **Completion criteria:** Project root, hub, state, execution, activation, evidence, decision, risk, gate, change, handover, and material controlled locations are mapped; critical references verified; failures explicit.

### {{PROJECT_CODE}}-ACT-0004 — Assess activation gate

- **Purpose:** Determine whether execution can safely begin.
- **Expected output:** Evidence-backed outcome in [project activation](02_project_activation.md).
- **Predecessors:** `{{PROJECT_CODE}}-ACT-0003`.
- **Successors:** First project-specific execution task.
- **Evidence required:** All activation criteria or explicit conditions.
- **Owner:** {{APPROVAL_OWNER}}
- **Status:** `not-started`
- **Gate relationship:** Prepares {{PROJECT_CODE}}-GAT-ACTIVATION; authorized setup may proceed before passage
- **Reversibility:** R1
- **Completion criteria:** Outcome, approver, evidence, envelope, prohibited actions, and first authorized task recorded.

## Blocked tasks

- Project-specific execution is blocked until activation is `READY` or `READY WITH CONDITIONS`.

## Future work

Define only to Levels 2–4 until activation and early evidence justify executable Tasks detail.

## Dependency rule

An task becomes `ready` only when predecessors, inputs, evidence, scope, authorization, and applicable gates are satisfied.

## Cycle budget

- **Active execution limit:** One task per write owner by default
- **Next useful result:** Completed charter based on supplied information
- **Research / tool limit:** Stop when the current decision has sufficient evidence; change method after two unchanged failures
- **Checkpoint:** Record material output, validation, blocker, and next action in the authoritative state

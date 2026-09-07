---
id: "{{PROJECT_CODE}}-PRJ-001"
title: "{{PROJECT_NAME}}"
type: project
status: setup
framework: ELAEF
framework_version: 3.5.0
conformance_profile: P0
naming_profile: obsidian_portable_v1
numbering_profile: numbered_project_v1
owner: "{{PROJECT_OWNER}}"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
activation_status: not_assessed
---

# {{PROJECT_NAME}}

This hub is the authoritative P0 project record. Agent instructions are in `AGENTS.md`. Keep one hub until separate ownership, access, or retrieval justifies splitting it. This file is copied to `README.md` when initializing P0.

## Definition

- **Objective and beneficiary:** {{OBJECTIVE_AND_BENEFICIARY}}
- **Success criteria:** {{MEASURABLE_SUCCESS}}
- **Scope and constraints:** {{SCOPE_AND_CONSTRAINTS}}
- **Excluded:** {{EXCLUSIONS}}
- **Failure / pause / stop criteria:** {{FAILURE_PAUSE_STOP}}

## State

- **Phase:** Setup
- **Current activity:** Define the project from owner input
- **Next action:** Complete the definition and assess activation
- **Blocker:** Project definition and activation are incomplete
- **Write owner:** {{PROJECT_OWNER}}
- **Trusted revision / backup:** {{REVISION_OR_RECOVERY_METHOD}}

## Evidence and uncertainty

| ID | Statement / source | Classification | Confidence / limitation | Review trigger |
|---|---|---|---|---|
| {{PROJECT_CODE}}-EVD-0001 | {{SOURCE_AND_FINDING}} | Unassessed input | Unknown until reviewed | Before relying on it |

## Activities

| ID | Output | Dependency / authority | Status | Completion evidence |
|---|---|---|---|---|
| {{PROJECT_CODE}}-ACT-0001 | Defined project and activation assessment | Owner's setup request | ready | Pending owner input and review |

Work on one execution activity at a time. Prepare later activities only as far as current evidence warrants. Record outputs and validation before claiming completion.

## Decisions and authorization

- **Setup authority:** The owner's request to initialize permits preparation of internal project records.
- **Execution envelope:** {{AUTHORIZED_SCOPE_AND_APPROVAL_EVIDENCE}}
- **External commitments:** Require applicable explicit authority and final-state evidence.
- **Decisions:** None recorded; recommendations remain proposals.

## Risks and open items

- **Current risk:** Unsupported assumptions could be treated as facts or authority.
- **Mitigation / owner:** Verify source and authority before commitment; {{PROJECT_OWNER}}.
- **Blocking question:** {{MOST_IMPORTANT_MISSING_INPUT}}

## Activation

- **State:** not_assessed
- **Outcome:** NOT READY
- **Criteria:** Definition, authority, first activity, evidence needs, recovery, and stop conditions are explicit.
- **Approver and approval evidence:** {{APPROVER_AND_EVIDENCE}}
- **Conditions / expiry:** {{CONDITIONS_OR_NONE_AND_REVIEW_TRIGGER}}

Setup may prepare this gate. An owner-authorized decision is required to change the activation outcome. A tool reporting no structural errors is not an activation decision.

## References

- **Project root:** This folder; relative locations travel with the project.
- **Authoritative records:** The sections of this hub.
- **Agent instructions:** `AGENTS.md`.
- **Sensitive locations and access:** {{CONTROLLED_LOCATOR_OR_NOT_APPLICABLE}}

## Handover

- **State cutoff / trusted revision:** Not yet prepared
- **Read first:** This hub and `AGENTS.md`
- **Changed / validated:** Skeleton created; project meaning and authority await assessment
- **Still unconfirmed:** Project definition and activation
- **Next action / blocker:** See State
- **Transfer:** Not recorded
- **Receiver acceptance:** Not assessed; acknowledgment evidence required

## Change history

- {{YYYY-MM-DD}} — Initialized under ELAEF 3.5.0. Setup only; no project execution or activation implied.

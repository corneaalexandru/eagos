---
id: "{{PROJECT_CODE}}-GAT-ACTIVATION"
title: Project Activation
type: gate
status: not_assessed
approver: "{{APPROVAL_OWNER}}"
assessed:
review_on:
tags:
  - elaef/control
  - elaef/gate
---

# Project Activation

## Commitment controlled

Transition from setup into evidence gathering, testing, or execution under a defined authorization envelope.

## Intended activation envelope

{{AUTHORIZED_SCOPE_AFTER_PASSAGE}}

## Criteria

- [ ] Project owner and decision-makers identified
- [ ] Objective, beneficiary, scope, exclusions, and constraints explicit
- [ ] Success, failure, pause, and stop conditions defined
- [ ] Framework, conformance, naming, and numbering profiles declared
- [ ] Authoritative records and write owners identified
- [ ] Facts, assumptions, hypotheses, evidence, decisions, risks, and open items distinguishable
- [ ] Immediate work decomposed to Level 5
- [ ] Current and next activities, dependencies, and blocker known
- [ ] Gates and authorization boundaries explicit
- [ ] Read, write, external-action, and approval authority defined
- [ ] Sensitive-data and access requirements defined where relevant
- [ ] Instruction provenance and untrusted-content rules active
- [ ] Version history, backup, or recovery method available
- [ ] Project root and authoritative records mapped in [[../50_handover/01_reference_map]]
- [ ] Handover ownership, cutoff, and acceptance rules active
- [ ] First activity has readiness and completion criteria
- [ ] Final-state evidence can be produced for authorized external actions

## Evidence reviewed

- [[00_project_charter]]
- [[01_project_state]]
- [[03_execution_plan]]
- [[06_risk_register]]
- [[07_gate_register]]
- [[../AGENTS]]
- [[../50_handover/01_reference_map]]

## Exceptions and conditions

{{NONE_OR_EXPLICIT_CONDITIONS_OWNER_DEADLINE_AND_CONSEQUENCE}}

## Prohibited actions after activation

- {{PROHIBITED_ACTION}}

## Outcome

- **Assessment:** `NOT READY`
- **Assessor:** {{ASSESSOR}}
- **Approver:** {{APPROVER}}
- **Assessment date:** {{YYYY-MM-DD}}
- **Evidence of approval:** {{EVIDENCE_OR_NONE}}
- **Review or expiry trigger:** {{TRIGGER}}
- **First authorized activity:** {{ACTIVITY_ID_OR_NONE}}

Allowed outcomes:

- `READY`
- `READY WITH CONDITIONS`
- `NOT READY`

## Current blocker

Uninstantiated project definition and unassessed criteria.

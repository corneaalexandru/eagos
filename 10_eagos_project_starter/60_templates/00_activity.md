---
id: "{{PROJECT_CODE}}-ACT-{{SEQUENCE}}"
title: "{{ACTIVITY_TITLE}}"
type: task
status: proposed
owner: "{{OWNER}}"
write_owner: "{{WRITE_OWNER}}"
predecessors: []
successors: []
gate:
reversibility: R1
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
revision: 0
outputs: []
validation_evidence: []
evidence_refs: []
delegation:
tags:
  - eagos/task
---

# {{ACTIVITY_TITLE}}

## Purpose

{{WHY_THIS_ACTIVITY_EXISTS}}

## Expected output

{{CONCRETE_ARTIFACT_RESULT_OR_CHANGE}}

## Readiness criteria

- [ ] Predecessors complete
- [ ] Required inputs available
- [ ] Required evidence available
- [ ] No blocking gate
- [ ] Scope and authority confirmed

## Completion criteria

- [ ] Expected output exists
- [ ] Required validation passed
- [ ] Authoritative records updated where necessary
- [ ] Dependencies reconsidered
- [ ] Final-state evidence recorded for any external action

## Evidence required

- **Required level:** {{E0_E1_E2_E3_OR_E4}}
- **Evidence links:** {{LINKS}}

## Dependencies

- **Predecessors:** {{IDS_OR_NONE}}
- **Successors:** {{IDS_OR_NONE}}

## Risks and blockers

- {{RISK_OR_BLOCKER}}

## Authorization

- **Gate:** {{GATE_ID_OR_NONE}}
- **Authorization evidence:** {{EVIDENCE_OR_NOT_REQUIRED}}
- **Authorized envelope:** {{SCOPE}}

## Execution record

- **Effort limit / stopping condition:** {{TIME_COST_ATTEMPTS_OR_EVIDENCE_THRESHOLD}}
- **Retry rule:** Check final state before repeating an action with uncertain external consequences; change method after two identical failures without new information.

- **Observed:**
- **Interpreted:**
- **Changed:**
- **Authorized by:**

## Validation

- **Method:**
- **Result:** Not validated
- **Validator:**
- **Date:**

## Next justified action

{{NEXT_ACTION_OR_STOP_CONDITION}}

## Attempts and recovery

Use `13_task_attempt.md` in this template folder for separate attempts when useful. Preserve Task identity, cumulative limits and previous outcomes. Check actual state before retrying uncertain external effects; a successful attempt alone does not pass a gate.

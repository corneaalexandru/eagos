---
id: "{{PROJECT_CODE}}-CTL-GATES"
title: Gate Register
type: gate_register
status: active
updated: "{{YYYY-MM-DD}}"
write_owner: "{{WRITE_OWNER}}"
revision: 0
tags:
  - elaef/control
  - elaef/gate
---

# Gate Register

## Active gates

### {{PROJECT_CODE}}-GAT-ACTIVATION — Project Activation

- **State:** `not_assessed`
- **Commitment controlled:** Transition from setup into scoped project execution.
- **Approver:** {{APPROVAL_OWNER}}
- **Required evidence:** [[02_project_activation]] criteria and linked control records
- **Required evidence level:** Proportionate to profile and intended envelope
- **Unresolved exceptions:** Project not instantiated
- **Reversibility:** R2
- **Actions authorized by passage:** Only those in the recorded activation envelope
- **Actions remaining prohibited:** All unrecorded external or material commitments
- **Assessment record:** [[02_project_activation]]

## Passed or conditionally passed gates

None.

## Failed, deferred, or expired gates

None.

## Gate rule

Only the authorized approver may set `passed` or `conditionally-passed`. A conditional pass must identify conditions, owner, deadline, prohibited actions, and consequence of non-closure.

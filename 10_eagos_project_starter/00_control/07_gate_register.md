---
id: "{{PROJECT_CODE}}-CTL-GATES"
title: Gate Register
type: gate_register
status: active
updated: "{{YYYY-MM-DD}}"
write_owner: "{{WRITE_OWNER}}"
revision: 0
tags:
  - eagos/control
  - eagos/gate
---

# Gate Register

## Active gates

### Project Activation — reference to authoritative assessment

- **Stable ID:** `{{PROJECT_CODE}}-GAT-ACTIVATION`
- **Authoritative record:** [project activation](02_project_activation.md)
- **Commitment controlled:** Transition from setup into scoped project execution
- **Current state, approver, evidence, conditions, and envelope:** Read the assessment record; do not maintain a second mutable copy here

## Passed or conditionally passed gates

Consult the linked assessment records for current outcomes. Add subsequent gates here as references or as inline authoritative records, with one definition per ID.

## Failed, deferred, or expired gates

None.

## Gate rule

Only the authorized approver may set `passed` or `conditionally-passed`. A conditional pass must identify conditions, owner, deadline, prohibited actions, and consequence of non-closure.

---
id: "{{PROJECT_CODE}}-HND-HUB"
title: Handover Hub
type: handover_hub
status: active
framework: ELAEF
framework_version: 3.5.0
module_version: 1.0.0
owner: "{{HANDOVER_OWNER}}"
updated: "{{YYYY-MM-DD}}"
tags:
  - elaef/handover
---

# Handover Hub

This folder is the project continuity layer. It points to authoritative records; it does not replace them.

## Read order

1. [Project Hub](../README.md)
2. [Project State](../00_control/01_project_state.md)
3. [Project Activation](../00_control/02_project_activation.md)
4. [Execution Plan](../00_control/03_execution_plan.md)
5. [Reference Map](01_reference_map.md)
6. [Current Handover](02_current_handover.md)
7. Relevant evidence, decision, risk, gate, and change records

## Records

- **Reference map:** [reference map](01_reference_map.md)
- **Current handover:** [current handover](02_current_handover.md)
- **Lifecycle log:** [handover log](03_handover_log.md)
- **Historical material handovers:** `90_records/`

## Supported handover types

- Session
- Agent
- Human-agent
- Phase
- Pause / resume
- Ownership
- Environment
- Closure

## Operating rule

1. Update authoritative project records first.
2. Verify critical references.
3. Prepare [current handover](02_current_handover.md) with a state cutoff and trusted revision.
4. Mark `ready_for_review` only when outgoing completion criteria pass.
5. Record transfer evidence before marking `transferred`.
6. Require receiver verification before `accepted` or `accepted_with_conditions`.
7. Preserve the material completed handover in `90_records/` and add an entry to [handover log](03_handover_log.md).
8. Reset [current handover](02_current_handover.md) for the next transition without erasing history.

## Authority boundary

A handover describes authorized state; it does not create new authority. The receiver remains bound by active gates, authorization envelopes, project instructions, and higher-order constraints.

## Security boundary

Do not place credentials, secret values, restricted personal data, or unnecessary confidential content in the handover. Reference the controlled location and access procedure without reproducing the protected content.

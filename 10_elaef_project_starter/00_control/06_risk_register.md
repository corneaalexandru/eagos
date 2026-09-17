---
id: "{{PROJECT_CODE}}-CTL-RISKS"
title: Risk Register
type: risk_register
status: active
updated: "{{YYYY-MM-DD}}"
write_owner: "{{WRITE_OWNER}}"
revision: 0
tags:
  - elaef/control
  - elaef/risk
---

# Risk Register

## Active risks

### {{PROJECT_CODE}}-RSK-0001 — Execution before valid activation

- **Cause:** Project files may appear complete while placeholders, authority, or evidence remain unresolved.
- **Risk event:** An agent begins project-specific execution outside a validated authorization envelope.
- **Potential consequence:** Incorrect work, unauthorized external action, duplicated truth, or hidden project risk.
- **Likelihood:** Medium until activation passes
- **Impact:** High
- **Mitigation:** Require [project activation](02_project_activation.md) and enforce `AGENTS.md`.
- **Contingency:** Stop affected work, identify external consequences, restore trusted state, and reassess activation.
- **Owner:** {{PROJECT_OWNER}}
- **Status:** Open
- **Related tasks:** {{PROJECT_CODE}}-ACT-0001 to 0004
- **Escalation trigger:** Any project-specific execution begins before valid activation.

### {{PROJECT_CODE}}-RSK-0002 — Untrusted content treated as instruction

- **Cause:** Attached or retrieved content contains instruction-like language.
- **Risk event:** An agent follows content without valid authority.
- **Potential consequence:** Scope expansion, gate bypass, disclosure, unsafe action, or data exfiltration.
- **Likelihood:** Unknown
- **Impact:** High
- **Mitigation:** Apply the instruction trust boundary in `AGENTS.md`.
- **Contingency:** Stop, preserve evidence, review authority, and escalate proportionately.
- **Owner:** {{WRITE_OWNER}}
- **Status:** Open
- **Escalation trigger:** Suspicious instruction, credential request, unexpected external-action request, or authority ambiguity.

## Closed or accepted risks

None recorded.

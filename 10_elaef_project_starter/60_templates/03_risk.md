---
id: "{{PROJECT_CODE}}-RSK-{{SEQUENCE}}"
title: "{{RISK_TITLE}}"
type: risk
status: open
owner: "{{OWNER}}"
likelihood: "{{LOW_MEDIUM_HIGH_OR_DEFINED_SCALE}}"
impact: "{{LOW_MEDIUM_HIGH_OR_DEFINED_SCALE}}"
review_on:
tags:
  - elaef/risk
---

# {{RISK_TITLE}}

## Risk statement

Because of **{{CAUSE}}**, **{{RISK_EVENT}}** may occur, resulting in **{{CONSEQUENCE}}**.

## Assessment

- **Likelihood:** {{ASSESSMENT_AND_BASIS}}
- **Impact:** {{ASSESSMENT_AND_BASIS}}
- **Evidence:** {{LINKS}}
- **Uncertainty:** {{LIMITATIONS}}

## Response

- **Strategy:** Avoid / Reduce / Transfer / Accept / Monitor
- **Mitigation:** {{ACTION}}
- **Contingency:** {{ACTION_IF_TRIGGERED}}
- **Owner:** {{OWNER}}

## Triggers

- **Early warning:** {{SIGNAL}}
- **Escalation trigger:** {{TRIGGER}}
- **Gate affected:** {{GATE_ID_OR_NONE}}

## Related records

- {{LINKS}}

## Residual risk

{{ASSESSMENT_AFTER_RESPONSE}}

## Closure

- **Status:** Open
- **Closure evidence:** None
- **Risk acceptance authority:** {{APPROVER}}

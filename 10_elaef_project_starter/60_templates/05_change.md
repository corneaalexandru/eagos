---
id: "{{PROJECT_CODE}}-CHG-{{SEQUENCE}}"
title: "{{CHANGE_TITLE}}"
type: change
status: recorded
change_date: "{{YYYY-MM-DD}}"
authorizer: "{{AUTHORIZER}}"
tags:
  - elaef/change
---

# {{CHANGE_TITLE}}

## Previous position

{{TRUSTED_PRIOR_STATE}}

## New position

{{NEW_STATE}}

## Reason

{{WHY_THE_CHANGE_IS_JUSTIFIED}}

## New evidence

- {{LINKS_OR_NONE}}

## Authorization

- **Authorizer:** {{AUTHORIZER}}
- **Decision reference:** {{DECISION_ID_OR_NONE}}
- **Authorization evidence:** {{EVIDENCE}}

## Impact

- **Scope:** {{IMPACT}}
- **Tasks:** {{IDS}}
- **Dependencies:** {{IMPACT}}
- **Risks:** {{IDS_OR_NONE}}
- **Gates:** {{IDS_OR_NONE}}
- **Automation / links:** {{IMPACT_OR_NONE}}

## Validation

- **Method:** {{METHOD}}
- **Result:** {{RESULT}}
- **Validator:** {{VALIDATOR}}
- **Date:** {{YYYY-MM-DD}}

## Rollback or recovery

{{PROCEDURE_OR_NOT_REQUIRED}}

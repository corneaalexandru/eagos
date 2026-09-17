---
id: "{{PROJECT_CODE}}-DLG-{{SEQUENCE}}"
title: "{{DELEGATION_TITLE}}"
type: delegation
status: draft
delegator: "{{DELEGATOR_ID_OR_HUMAN}}"
delegate: "{{DELEGATE_ID}}"
parent_delegation:
scope: "{{EXACT_SCOPE}}"
allowed_operations: []
allowed_targets: []
budget_limit: "0"
budget_unit: "{{UNIT_OR_CURRENCY}}"
valid_from: "{{YYYY-MM-DD}}"
expires_on: "{{EXPIRY_DATE}}"
subdelegation: forbidden
approver: "{{APPROVER}}"
authorization_evidence: []
---

# {{DELEGATION_TITLE}}

## Authority and limits

Record read, write, external-action and approval rights separately, with exclusions, applicable gates, accountable owner, review triggers and revocation method. Use exact operation/target strings, no wildcards. The numeric allocation is a shared cap, not a spend authorization; zero can describe no spending. Resource use, multiple currencies and prose scope require appropriate runtime/manual checks.

## Inheritance and enforcement

Children must fit every ancestor; child allocations share the parent total and actual use must also be metered. Expiry, revocation, new sessions, retries and substitute agents do not reset limits. Specify which controls are native, additional, manual or unsupported.

## Review and revocation

Record actual approver evidence, review date/trigger, revocation distribution to active descendants/jobs/access and final-state verification. This draft creates no delegation.

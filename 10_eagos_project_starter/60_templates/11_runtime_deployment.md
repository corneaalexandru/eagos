---
id: "{{PROJECT_CODE}}-RUN-{{SEQUENCE}}"
title: "{{DEPLOYMENT_NAME}}"
type: runtime_deployment
status: documented
platform: "{{PLATFORM}}"
platform_version: "{{PINNED_VERSION}}"
profile_reference: "{{PROFILE_LOCATION_AND_REVISION}}"
configuration_fingerprint: "{{CONFIGURATION_HASH}}"
environment: "{{ENVIRONMENT}}"
owner: "{{OWNER}}"
test_evidence: []
enforcement_evidence: []
activation_decision:
operating_scope: "{{EXACT_SCOPE}}"
required_control_gaps: unresolved
limitations: "{{KNOWN_LIMITATIONS}}"
---

# {{DEPLOYMENT_NAME}}

## Control map

Map identities, delegated authority, sandbox/tools/data, approvals, cumulative budgets, scheduling, retries, record writes, review and recovery to native/additional/manual/unsupported controls. Include configuration references and actual test results. Do not store credentials here.

## Acceptance and recovery

Preserve the tested versions, environment, negative tests, runtime evidence and approver decision. Tested is separate from active. Define rollback and demonstrate stopping jobs, descendants and access when suspended.

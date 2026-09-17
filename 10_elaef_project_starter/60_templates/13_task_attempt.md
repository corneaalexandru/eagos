---
id: "{{PROJECT_CODE}}-ATT-{{SEQUENCE}}"
title: "{{ATTEMPT_TITLE}}"
type: task_attempt
status: planned
task_id: "{{TASK_ID}}"
run_key: "{{LOGICAL_OPERATION_KEY}}"
executor: "{{EXECUTOR_ID}}"
outputs: []
validation_evidence: []
reconciliation_required:
---

# {{ATTEMPT_TITLE}}

## Attempt record

Record input revision, authority checked, start/end, tool/runtime version, actual cost, observed output, error and reviewer. Preserve this attempt when retrying; link the next attempt. A run key identifies the logical effect and supports duplicate prevention in the runtime.

## Uncertain outcome

If an external effect may have happened, mark uncertain and record the actual reconciliation required before another attempt. Resolve that uncertainty before starting another attempt with the same run key. A successful attempt is evidence for Task completion, not an automatic change to the Task or a passed gate.

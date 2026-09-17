---
title: ELAEF OpenClaw Profile
type: runtime_profile
profile_version: "1.0.0"
framework_version: "4.0.0"
status: documented
source_reviewed_on: 2026-09-16
tested_version: not_selected
---

# OpenClaw implementation profile

Candidate architecture: a coordinator, bounded specialist agents and an appropriately independent review path, mapped to ELAEF role/delegation records. Add only roles justified by workload and consequence. This is an implementation specification, not an installed configuration.

Official documentation describes per-agent workspaces/session state, agent routing/delegation, tool restrictions and sandbox configuration. Workspace selection alone is not a hard filesystem boundary. Review the selected version's effective permissions, cross-agent access, sandbox and host execution paths before claiming isolation.

Sources reviewed 2026-09-16: [multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent), [tool and agent permissions](https://docs.openclaw.ai/gateway/security/tool-permissions), [sandbox and tool policy](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated). These live documents can change; pin the installation version and archive the relevant source references for a deployment.

| ELAEF requirement | Proposed implementation route | What remains to prove |
|---|---|---|
| Role/instance mapping | Native agent identities plus ELAEF role register | Actual instances use the reviewed configuration |
| Task delegation | Platform delegation controls plus written scopes | Scope survives handoff; unauthorized delegation is denied |
| Filesystem/tool isolation | Native sandbox and tool policy, explicitly configured | Host/elevated paths and connector access cannot bypass required limits |
| Business authority | Additional policy/action-boundary adapter or manual approval path | Exact operation/target, expiry, revocation and approval identity checked |
| Shared budgets | Additional durable allocation/metering component unless demonstrated natively | Limits survive parallel children, retries and restarts |
| Record integrity | Designated writer with revision/transaction control | Conflicting updates detected; project records reconcile with session state |
| Scheduling and stop | Explicit runtime job configuration and revocation procedure | Actual jobs/workers stop; a prose schedule does not create a job |
| Final-state evidence | Tool-specific verification and audit export | A reported success corresponds to the actual intended effect |

## Bounded pilot procedure

1. Record version, environment, owner, source/configuration fingerprints and rollback. Use a temporary workspace with synthetic data and no external channels/accounts.
2. Configure only necessary agents/tools. Record native/manual/additional/unsupported controls for every integration requirement.
3. Produce one local artifact through assignment, execution, independent check where needed, and controlled record update.
4. Attempt forbidden path/tool access and child authority expansion. Test revocation, shared budget, duplicate run, interruption and conflicting write scenarios using isolated fixtures.
5. Preserve actual configuration, results and limitations. A missing enforcement component is an open gap, not a passing test.
6. Review the exact proposed operating scope and remaining gaps before activation. Installation, account connection, scheduling and external action require their applicable authority.

No ready-to-run configuration is shipped while the target version and enforcement components are unverified. [Integration contract](../07_runtime_integration.md).

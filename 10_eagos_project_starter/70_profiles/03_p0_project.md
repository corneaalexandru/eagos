---
id: "{{PROJECT_CODE}}-PRJ-001"
title: "{{PROJECT_NAME}}"
type: project
status: setup
framework: EAGOS
framework_version: 4.0.0
conformance_profile: P0
naming_profile: portable_markdown_v1
numbering_profile: numbered_project_v1
owner: "{{PROJECT_OWNER}}"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
activation_status: not_assessed
lifecycle_stage: discover
---

# {{PROJECT_NAME}}

This hub owns the project's current state. Start with the owner's actual situation and `AGENTS.md`; read `01_operating_guide.md` once. Use ordinary conversation. Unanswered fields block only work that depends on them; authorized exploration needs no completed intake.

## Definition

- **Objective, beneficiary and observable success:** {{OBJECTIVE_BENEFICIARY_AND_SUCCESS}}
- **Scope, exclusions, resource limit and stop conditions:** {{SCOPE_LIMITS_AND_STOP}}
- **Sensitive information, audience and access:** {{DATA_CONTROLS_OR_NOT_APPLICABLE}}

## State

This is the single current Task/checkpoint.

- **Task / state:** No execution Task selected; start from the current owner request.
- **Expected output and completion check:** Define before execution.
- **Inputs, predecessors, evidence and gate:** Resolve only those needed for the next action.
- **Last verified result / output pointer:** None yet.
- **Current blocker / next action:** Explore the starting point or continue the supplied work.
- **Owner correction / alternatives:** None recorded; preserve material changes in Change history.
- **Write owner:** {{PROJECT_OWNER}}
- **Trusted revision, recovery and cutoff:** {{RECOVERY_AND_CUTOFF}}

Use stable ACT IDs when work becomes material. Keep current state here; use one row per Task only if several Tasks need tracking. An execution attempt is not a new Task. Record output and validation before completion, cumulative limits across retries, and actual state before repeating an uncertain action.

## Evidence, risks and ideas

Record only real observations or explicitly classified assumptions. Add stable IDs and source/date/limitations when evidence informs a decision; do not create placeholder evidence records. Flag contrary, stale or disputed support before further commitment. Record material risks with owner, response and review trigger.

An idea seed such as `{{PROJECT_CODE}}-SEED-0001` needs only its origin, possible benefit, owner reaction and next uncertainty. For multiple initiatives, link to their authoritative records instead of copying current state into this hub.

## Authority and activation

- **Actual setup request and permitted preparation:** {{SETUP_REQUEST_AND_SCOPE}}
- **Execution envelope, approver and approval evidence:** {{EXECUTION_AUTHORITY}}
- **Conditions, expiry and reassessment trigger:** {{CONDITIONS_AND_EXPIRY}}
- **Activation outcome:** NOT READY until assessed; synchronize the frontmatter declaration with the recorded outcome.

Assess purpose/success, inputs, evidence, first ready Task, authority, data controls, write ownership, recovery and stop conditions before gated execution. READY maps to `passed`; READY WITH CONDITIONS maps to `conditionally-passed`; NOT READY leaves activation unpassed. Record assessor, evidence and actual authorized decision when applicable. Setup must not depend on the activation it prepares. Stage and structural checks grant no authority.

Reuse valid scoped authority; external commitments need applicable explicit authority and final-state verification. A newly copied hub creates no approval.

## Handover

At a material pause, update the single checkpoint above with output pointers, remaining uncertainty, authority and next action. Read current records before resuming; do not restart intake or reset limits. Split files only for separate ownership, access, retrieval or scale.

For transfer or closure, verify outputs, remaining obligations, reference access, ownership and actual acknowledgment. Record the receiver/date/evidence and any conditions before claiming acceptance. A personal project can finish without launch or monetization.

## Change history

- {{YYYY-MM-DD}} — Initialized under EAGOS 4.0.0. Setup only; no execution or activation implied.

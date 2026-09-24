# Opportunity ownership update — prepared 2026-09-24

- Removed the separate discovery starter and retired new-portfolio initialization. New opportunity discovery belongs to the applicable portfolio owner.
- Kept the earlier ODS schema 1 integrity checker read-only so existing records and manifests remain assessable. Core EAGOS 4.0.0 project setup and governance remain available.

# Release changes

## Practical assurance update — 2026-09-17

- Simplified the P0 hub to one Task/checkpoint and removed placeholder evidence rows while retaining authority, activation, risk, recovery and closure requirements.
- Added end-to-end offline workflows for output creation, resumption, gate/receipt checks, revocation and evidence classification; CI runs them directly.
- Added outcome/overhead/resumption measures and explicit evidence states for scoped effectiveness assessment.
- Extended release review to hosted repository metadata and post-publication state, which file tests cannot verify.

## Maintenance update — 2026-09-17

- Made setup and templates editor-neutral; new files use `portable_markdown_v1` for the unchanged naming rules. Existing project records and original manifests are preserved.
- Closed excluded-file body reads through heading links and special hub/activation reads.
- Reject empty/unresolved completion, approval and acceptance evidence; reject declared delegation self-approval.
- Check declared activation-decision date bounds for active runtimes.
- Require discovery screening from approved selections and actionable handovers independently of candidate labels; enforce claim state/evidence consistency.
- Clarified role/instance/deployment states and the manual ledger required beyond active-child budget sums. Corrected discovery copy.
- Excluded root maintenance artifacts from Git while keeping reusable starter paths trackable.
- Added negative regression cases; current base versions remain EAGOS 4.0.0 / Discovery 1.3.0. Existing manifests and approvals are preserved.

## EAGOS 4.0.0 / Discovery 1.3.0 — 2026-09-16

- Added an optional AI agent system and owner-dashboard contract: agent-led preparation, approval inbox, feedback, freshness and version-bound decisions.
- Consolidated the specification into 24 sections covering evidence-led project execution.
- Added an agent organization chart, role/delegation contracts, company operations and runtime implementation profiles.
- Named executable work **Task**, with separate attempts, recovery and evidence-impact diagnostics.
- Added bounded delegation, runtime-state and duplicate-attempt checks without claiming live enforcement.

Prior releases remain in repository history and the separate maintenance archive. This file is release information, not agent startup context.

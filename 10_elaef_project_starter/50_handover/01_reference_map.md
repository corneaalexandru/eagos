---
id: "{{PROJECT_CODE}}-REF-MAP"
title: Project Reference Map
type: reference_map
status: setup
owner: "{{REFERENCE_OWNER}}"
write_owner: "{{WRITE_OWNER}}"
updated: "{{YYYY-MM-DD}}"
revision: 0
tags:
  - elaef/handover
  - elaef/reference
---

# Project Reference Map

> [!warning] Template state
> Replace location and ownership placeholders, then verify critical references. A listed path is not verified merely because it looks plausible.

## Project identity and roots

| Reference ID | Type | Name | Record ID | Location | Authority | Owner | Access | Last verified | Status |
|---|---|---|---|---|---|---|---|---|---|
| `{{PROJECT_CODE}}-REF-ROOT` | project_root | Project root | `{{PROJECT_CODE}}-PRJ-001` | `{{PROJECT_ROOT_WITH_ENVIRONMENT_CONTEXT}}` | authoritative | {{PROJECT_OWNER}} | internal | not_verified | unknown |
| `{{PROJECT_CODE}}-REF-HUB` | note | Project hub | `{{PROJECT_CODE}}-PRJ-001` | [README](../README.md) | authoritative | {{PROJECT_OWNER}} | internal | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-AGENTS` | note | Agent operating contract | — | [AGENTS](../AGENTS.md) | authoritative | {{PROJECT_OWNER}} | internal | {{YYYY-MM-DD}} | active |

## Authoritative control records

| Reference ID | Type | Name | Record ID | Location | Authority | Owner | Access | Last verified | Status |
|---|---|---|---|---|---|---|---|---|---|
| `{{PROJECT_CODE}}-REF-CHARTER` | note | Project charter | `{{PROJECT_CODE}}-CTL-CHARTER` | [project charter](../00_control/00_project_charter.md) | authoritative | {{PROJECT_OWNER}} | internal | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-STATE` | note | Project state | `{{PROJECT_CODE}}-CTL-STATE` | [project state](../00_control/01_project_state.md) | authoritative | {{WRITE_OWNER}} | internal | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-EXECUTION` | note | Execution plan | `{{PROJECT_CODE}}-CTL-EXECUTION` | [execution plan](../00_control/03_execution_plan.md) | authoritative | {{WRITE_OWNER}} | internal | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-EVIDENCE` | note | Evidence register | `{{PROJECT_CODE}}-CTL-EVIDENCE` | [evidence register](../00_control/04_evidence_register.md) | authoritative | {{WRITE_OWNER}} | internal | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-DECISIONS` | note | Decision log | `{{PROJECT_CODE}}-CTL-DECISIONS` | [decision log](../00_control/05_decision_log.md) | authoritative | {{WRITE_OWNER}} | internal | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-RISKS` | note | Risk register | `{{PROJECT_CODE}}-CTL-RISKS` | [risk register](../00_control/06_risk_register.md) | authoritative | {{WRITE_OWNER}} | internal | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-GATES` | note | Gate register | `{{PROJECT_CODE}}-CTL-GATES` | [gate register](../00_control/07_gate_register.md) | authoritative | {{WRITE_OWNER}} | internal | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-ACTIVATION` | note | Activation gate | `{{PROJECT_CODE}}-GAT-ACTIVATION` | [project activation](../00_control/02_project_activation.md) | authoritative | {{APPROVAL_OWNER}} | internal | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-CHANGES` | note | Change log | `{{PROJECT_CODE}}-CTL-CHANGES` | [change log](../00_control/08_change_log.md) | authoritative | {{WRITE_OWNER}} | internal | {{YYYY-MM-DD}} | active |

## Project folders

| Reference ID | Type | Purpose | Location | Authority role | Owner | Access | Create allowed | Last verified | Status |
|---|---|---|---|---|---|---|---|---|---|
| `{{PROJECT_CODE}}-REF-CONTROL-FOLDER` | folder | Project-wide control records | `../00_control/` | authoritative | {{WRITE_OWNER}} | internal | controlled | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-DOMAINS-FOLDER` | folder | Persistent domain knowledge | `../10_domains/` | authoritative_by_record | {{WRITE_OWNER}} | internal | when_justified | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-EXECUTION-FOLDER` | folder | Phase and pilot execution records | `../20_execution/` | authoritative_by_record | {{WRITE_OWNER}} | internal | when_justified | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-EVIDENCE-FOLDER` | folder | Source evidence and evidence notes | `../30_evidence/` | source_and_authoritative_index | {{EVIDENCE_OWNER}} | {{ACCESS_CLASS}} | controlled | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-OUTPUTS-FOLDER` | folder | Project-generated artifacts | `../40_outputs/` | output | {{OUTPUT_OWNER}} | {{ACCESS_CLASS}} | controlled | {{YYYY-MM-DD}} | active |
| `{{PROJECT_CODE}}-REF-PRIVATE-FOLDER` | private_location | Restricted project records | `../80_private/` | controlled | {{PRIVATE_DATA_OWNER}} | restricted | explicit_authority_only | not_verified | unknown |
| `{{PROJECT_CODE}}-REF-ARCHIVE-FOLDER` | archive | Inactive and superseded records | `../90_archive/` | archive | {{ARCHIVE_OWNER}} | {{ACCESS_CLASS}} | controlled | {{YYYY-MM-DD}} | active |

## Repositories and environments

| Reference ID | Type | Name | Location | Revision / environment | Authority | Owner | Access | Last verified | Status |
|---|---|---|---|---|---|---|---|---|---|
| `{{PROJECT_CODE}}-REF-REPOSITORY` | repository | Project repository | {{REPOSITORY_PATH_OR_URI_OR_NONE}} | {{BRANCH_TAG_OR_COMMIT}} | authoritative_or_none | {{OWNER}} | {{ACCESS_CLASS}} | not_verified | unknown |
| `{{PROJECT_CODE}}-REF-OBSIDIAN-VAULT` | tool_environment | Obsidian vault | {{VAULT_NAME_AND_ROOT_OR_NONE}} | {{DEVICE_OR_ENVIRONMENT}} | environment | {{OWNER}} | {{ACCESS_CLASS}} | not_verified | unknown |

## External systems and controlled locations

| Reference ID | Type | Name | Location | Purpose | Authority | Owner | Access | Last verified | Status |
|---|---|---|---|---|---|---|---|---|---|
| {{REFERENCE_ID}} | external_uri | {{SYSTEM_OR_RESOURCE}} | {{CONTROLLED_URI_OR_LOCATOR}} | {{PURPOSE}} | {{AUTHORITY_ROLE}} | {{OWNER}} | {{ACCESS_CLASS}} | not_verified | unknown |

## Moved, unavailable, or superseded references

| Reference ID | Previous location | Status | Replaced by | Reason | Date |
|---|---|---|---|---|---|
| {{REFERENCE_ID}} | {{OLD_LOCATION}} | {{MOVED_UNAVAILABLE_SUPERSEDED}} | {{NEW_REFERENCE_OR_NONE}} | {{REASON}} | {{YYYY-MM-DD}} |

## Verification log

| Date | Verifier | Scope | Result | Failures / limitations | Change reference |
|---|---|---|---|---|---|
| {{YYYY-MM-DD}} | {{VERIFIER}} | Initial critical references | not_verified | Template not instantiated | {{CHANGE_ID_OR_NONE}} |

## Reference rules

- Prefer stable IDs and project-relative or Wikilink locations.
- State host/environment context for absolute paths.
- Do not store credentials or secret values here.
- Verify both reachability and meaning.
- Update this map after material moves, renames, access changes, or supersession.

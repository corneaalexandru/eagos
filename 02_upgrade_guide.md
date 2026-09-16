# ELAEF upgrade guide

The current release is **ELAEF 3.6.0** with optional **ODS 1.2.0**. Existing projects retain their declared versions, records, and approvals until deliberately upgraded.

## 3.5.1 / ODS 1.1.1 to the unified lifecycle

This additive revision introduces one conversational operating guide, proactive facilitation, and the Discover, Shape, Incubate, Develop, Launch, Operate, and Evolve lifecycle. It preserves existing evidence levels, phases, statuses, IDs, gates, and authority. The optional `lifecycle_stage` property is descriptive; older records may omit it.

1. Inventory the current records and preserve a trusted snapshot and original manifests.
2. Review the new guide and reconcile its agent contract with local instructions and existing authority.
3. Add a compact conversation checkpoint and initiative pointers only where useful. Keep current truth in its existing authoritative location.
4. Copy the guide into the workspace, verify links, and record adoption. P0 adds `01_operating_guide.md`; discovery adds `03_operating_guide.md`. The distribution's maintained source is `04_operating_guide.md`; the starter copies are verified identical portable views.
5. For multiple initiatives, use a separate record only when sustained work or ownership justifies it. Preserve seed/record relationships and actual handover evidence.
6. Recheck affected records, then change version declarations through a documented migration. Do not retroactively invent stage transitions, source evidence, selection, launch, or acceptance.

ODS retains schema 1 and reads 1.0.0, 1.1.0, 1.1.1, and 1.2.0 workspaces. The new core initializer adds the operating guide to its P0 baseline. Existing manifests remain historical installation evidence; no automatic migration/rebase is performed.

The former detailed phase sequence remains valid; the seven stages are a simpler conversational view. Core discovery/idea shaping is available without a separate ODS installation. Use ODS when structured research and comparison help the current work.

## 3.5.0 → 3.5.1

This compatible maintenance patch shortens operating guidance, clarifies setup authority and naming, corrects the embedded hub's initial state, and fixes comparison of the two supported initial activation spellings. Record schemas and controls are unchanged.

Review the revised agent contract and reconcile useful changes with local instructions. Remove template-derived authority claims only by recording the actual owner request; preserve valid existing approvals. Keep original IDs, evidence, manifests, and history. No automatic migration or public release is implied. For ODS 1.0.0/1.1.0, use the [discovery upgrade guidance](03_opportunity_discovery.md#compatibility-and-lifecycle).

## 3.4 → 3.5

ELAEF 3.5 is an additive release. Existing IDs, filenames, evidence, decisions, and authorization envelopes retain their meaning. Projects may stay on 3.4 until an upgrade is useful. New fields and tools are optional; the command-line validator checks a documented subset, not full conformance.

## What changed and why

- A short operating contract reduces repeated reading, duplicate records, repeated approval questions, and unnecessary future-task detail.
- A P0 hub makes the existing lightweight profile usable without creating the full folder baseline.
- Authorized setup can prepare its own activation gate, resolving the circular dependency in the previous starter.
- Relative Markdown links make copied starters usable in Obsidian and readable on GitHub.
- Offline initialization, structural checks, inventory, and baseline comparisons make routine checks repeatable.
- The initializer preserves unresolved facts and approvals. It does not create an active project or grant authority.

## Upgrade an existing project

1. Record its current framework version and trusted revision or backup.
2. Inventory the actual project and identify authoritative records. Preserve original evidence names and any established naming exceptions.
3. Read the revised agent contract and adopt only applicable changes. Preserve project-specific instructions and stronger controls.
4. Clarify setup activities versus commitments controlled by activation. Retain current gate outcomes unless the authorized approver changes them.
5. Optionally adopt the validator. For record-per-note automation, add scalar-list properties where useful: activities use `outputs` and `validation_evidence`; approved gates/decisions use `authorization_evidence`; conditional gates use `conditions` and `conditions_due`; accepted handovers use `acceptance_evidence`.
6. Normalize gate states only if needed: `not_assessed` and the older `not-assessed` are both understood. The starter writes `not_assessed`. `passed` corresponds to READY and `conditionally-passed` to READY WITH CONDITIONS. Keep hub, gate state, and assessment meaning consistent.
7. Recheck affected links and records. Record exceptions and known limitations, then update the project's declared version after migration review.

Do not replace active project records with blank templates. No existing project is automatically migrated by this release.

## Baselines and comparison

The initializer creates `00_elaef_manifest.json`, a tool record with a schema version, framework version, paths, and SHA-256 fingerprints of original templates and rendered files. It contains no approvals and is not a second project-state record. It does not replace a backup.

```bash
python3 20_tools/00_elaef.py inventory ../my_project
python3 20_tools/00_elaef.py drift ../my_project
python3 20_tools/00_elaef.py drift ../my_project --against-release .
```

`drift` identifies changed/missing baseline files and new local files. With a release path, it also identifies changed/removed template sources and new template candidates. Simultaneous local and upstream changes require manual reconciliation. P0 may show P1/P2 files as new candidates; this does not mean P0 requires them. Comparison never merges, renames, deletes, or updates the manifest.

For a manually created or older project without a manifest, use inventory and a version-controlled diff. Do not manufacture a baseline claiming to represent a historical state you have not verified. Preserve the original manifest through later upgrades, and record migration evidence separately; automatic baseline rebasing is not implemented.

## Distribution maintenance

A prepared release must contain a specification, starter, and tools that agree on their declared versions. Local maintenance may be ahead of the published release; label that difference explicitly. Compare the local starter and tools with the release checkout before publishing; review release contents, run checks, and verify the pushed commit. Keep private project records outside the public distribution.

The release includes conventional `.gitignore` files and a GitHub Actions workflow as documented tool-required naming exceptions. `.gitignore` prevents accidental tracking of some new files; it is not access control and cannot remove already tracked sensitive content.

## Compatibility and limitations

No existing element is removed. No community plugin, external service, or Python package is required. The optional CLI requires Python 3.9+. Manual Markdown use remains supported.

The validator reads flat scalar/list frontmatter, inline relative Markdown links, Wikilinks, explicit record IDs, and selected lifecycle fields. Nested YAML, reference-style Markdown links, prose/table semantics, domain-specific policies, access permissions, evidence truth, and remote availability require other checks or review. Findings against legitimate consolidated records or naming exceptions should be assessed, not corrected mechanically. A structural pass never sets READY or accepted.

The toolkit has automated fixture coverage; effectiveness in a live project and receiver resumption still require a project pilot. License selection remains a separate owner decision.

# Adopt EAGOS in existing work

Read this guide when changing an existing installation. Everyday work starts with the project contract and current checkpoint.

1. Inventory actual state, instructions, valid authority, dependencies and local customizations. Preserve a trusted baseline and recovery path.
2. Map the required changes. Retain stronger controls, stable IDs, raw evidence, decisions, original manifests and valid scoped approvals.
3. Merge instructions; never overlay active state with blank templates. Add roles, recurring processes and runtime records only where needed.
4. Validate structure, affected behavior, references and authority. Configuration requires separate enforcement tests before operational use.
5. Record adoption, exceptions, checks and rollback, then update version declarations. A new framework version does not itself migrate or activate a project.

## Compatibility reference

| Existing interface | Supported treatment |
|---|---|
| Level 5 activity / `type: activity` | Task / `type: task`; ACT IDs and readiness/completion meanings are retained |
| Current EAGOS manifests | Read unchanged; new installations also use `00_eagos_manifest.json` |
| Existing ELAEF installation | Its CLI, manifest and starter source paths remain readable without rewriting records |
| Former discovery module | Retired from new EAGOS installation. Existing schema 1 records and original manifests remain unchanged; legacy `check` remains a read-only standalone integrity diagnostic, while `init` refuses new portfolios. See the [legacy checker](20_tools/00_tools_index.md#former-discovery-entry-point). |


Rollback restores prior instructions/configuration while reconciling subsequent work and external effects. Preserve evidence and attempt history. Retiring a runtime also requires verified shutdown of its jobs and access.

## Validator corrections

The validator corrections tighten diagnostics without migrating existing records or changing original manifests. Previously accepted blank evidence entries, self-approved delegations, expired activation authority, unscreened selection/handover records and unsupported claim states may now produce errors. Reconcile them against actual evidence and current authority; never invent approvals or rewrite historical evidence to make a check pass. Checked roots and required entrypoints must not use symlink aliases. Inactive budget reservations still require the separate allocation/use ledger described in the organization guide.

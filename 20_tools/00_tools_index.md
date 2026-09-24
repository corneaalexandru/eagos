# Offline EAGOS tools

Run `python3 20_tools/00_eagos.py --help` from the package root. Python 3.9+ and its standard library are sufficient. Tools do not use the network, send information, approve gates, or migrate existing projects.

| Command | Purpose | Writes |
|---|---|---|
| `init DEST --code DEMO --name "Project" --owner "Owner" --profile P0` | Preview a new project | None |
| Same command with `--apply` | Create the previewed skeleton in a new destination | New files only; refuses existing destinations |
| `check ROOT --mode template` | Check reusable starter structure | None |
| `check ROOT --mode setup` | Structural checks; unresolved project fields are warnings | None |
| `check ROOT --mode active` | Unresolved live fields and absent activation declarations are errors | None |
| `inventory ROOT` | List eligible project paths | None |
| `drift ROOT --against-release PACKAGE` | Compare baseline, local files, and optional release | None |

`check --format json` emits machine-readable findings. Exit code `0` means no errors in the checks performed, `1` means findings reached the configured failure threshold, and `2` means invalid input or an operational failure. `--fail-on-warnings` makes warnings fail CI too. Reusable templates/profiles may retain placeholders in all modes; archive records and live handovers remain checked, so review legitimate historical exceptions.

Checks cover missing local links/headings, ambiguous Wikilinks, duplicate explicit record definitions, Markdown fences, the supported frontmatter subset, naming deviations, profile declarations, lifecycle vocabulary, explicit predecessor cycles, missing dependency IDs, selected completion/approval/acceptance fields, date expiry, and hub/activation disagreement. Required completion, approval and acceptance lists must contain resolved nonblank strings; a nonempty list containing empty or unknown entries is insufficient. They do not establish the truth or sufficiency of the contents.

Frontmatter uses flat `key: value` properties and scalar lists (`[]`, JSON-style inline arrays, or indented `- value` lines). Quote dates/placeholders/strings where necessary. Unsupported YAML produces a diagnostic requiring another validator; the tool does not claim to parse all YAML. Record dependencies use stable IDs. Code fences and inline code are excluded from link scans. External links are not fetched. Private/raw evidence bodies, symlinks, hidden folders, dependency caches, and their contents are not traversed. Links to excluded files are checked for existence only, without inspecting headings or bodies. The same read policy applies to the hub and activation record; excluded entrypoints cannot establish their required declarations. A checked root containing symlink components is rejected.

The initializer sets the supplied owner as the initial write owner. Other delegated owners and approvers stay unresolved. A partially interrupted initialization may leave an incomplete destination; inspect it and choose a recovery action rather than rerunning over it.

Run the fixture suite from the package root:

```bash
python3 30_tests/01_test_eagos.py -v
python3 20_tools/00_eagos.py check 10_eagos_project_starter --mode template --fail-on-warnings
```

See the [quick start](../01_quick_start.md) and [upgrade guide](../02_upgrade_guide.md). The maintained specification is `00_eagos.md` at the package root. `EAGOS_SPEC_PATH` selects a candidate in the core tests.

## Former discovery entry point

New opportunity records belong to the applicable portfolio owner. See the [adoption guide](../02_upgrade_guide.md#compatibility-reference) for older workspaces. The legacy CLI supports read-only `check ROOT [--format json]` without a portfolio-owner installation. Legacy `init` fails without creating files. Core EAGOS initialization and validation remain independent.

Run `python3 30_tests/02_test_discovery.py -v` for retirement and read-only legacy checks. New research workflow tests belong with the portfolio owner. A structural check cannot verify source truth, approval identity, evidence sufficiency or receiver acceptance.

## Unified conversational lifecycle

The tools install files and check structure; an AI agent uses [the operating guide](../04_operating_guide.md) to conduct the conversation. The root guide is the maintained distribution source; its portable core copy must match. P0 includes `01_operating_guide.md` alongside its hub and agent contract.

Core records may declare `lifecycle_stage` using `discover`, `shape`, `incubate`, `develop`, `launch`, `operate`, or `evolve`. The checker reports unsupported values in live records; the field is optional for older records and never grants activation or authority. It does not interpret or execute natural-language instructions, assess stage appropriateness, or prove launch completion.

Run `python3 30_tests/03_test_unified.py -v` for portable-guide installation, manifest consistency, optional-stage validation, and non-activation regression checks. The [conversation scenarios](../30_tests/04_conversation_scenarios.md) define separate behavioral evaluation; they require actual responses and review before claiming conversational effectiveness.

## EAGOS 4 governance diagnostics

The maintained CLI is `00_eagos.py`. New projects receive `00_eagos_manifest.json`. Existing interfaces and supported schemas are listed once in the [adoption guide](../02_upgrade_guide.md).

The core `check` command also reads optional Task, role, delegation, deployment, recurring-process and attempt records. It checks Task/legacy-activity completion and readiness, exact delegation operation/target subsets, valid date intervals, parent status and issuer, permitted subdelegation, cycles, finite nonnegative allocations, matching units and summed active child allocations. It checks declared deployment evidence/activation references, including any declared valid_from/expires_on bounds on authority used by active deployments, attempt-to-Task references, duplicate running/succeeded/uncertain run keys and declared stale/disputed evidence dependencies.

Use exact allowlists and decimal budget strings. Every active delegation has `valid_from`, `expires_on`, `budget_limit`, `budget_unit`, `subdelegation`, issuer/delegate, scope, approver and authorization evidence. Root grants rely on actual human authority; this tool cannot authenticate it. Child allocations reserve part of their parent's budget; actual use must still be metered by a runtime/manual control. Active-child sums exclude inactive grants and are not an available-balance calculation. A separate allocation/use ledger must retain outstanding reservations and consumption across suspension, expiry and revocation, with explicit return authority before reuse. Delegate/approver equality is rejected using exact strings; identity aliases and approval authenticity remain outside the checker. No wildcard or semantic scope interpretation is supported.

Optional `evidence_refs` contains supporting record IDs. The tool flags missing references and stale/disputed declared support for ready/running/active records. It does not decide evidence truth, adequacy or actual provenance. Prose-only relationships require review.

A passing diagnostic cannot enforce access, track actual resource use, revoke jobs, detect all duplicate external effects, prove test evidence authenticity or activate a runtime. Templates in `60_templates/` remain uninstantiated and are not treated as live records. Run `python3 30_tests/05_test_governance.py -v` for the bounded synthetic regression cases.

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

Checks cover missing local links/headings, ambiguous Wikilinks, duplicate explicit record definitions, Markdown fences, the supported frontmatter subset, naming deviations, profile declarations, lifecycle vocabulary, explicit predecessor cycles, missing dependency IDs, selected completion/approval/acceptance fields, date expiry, and hub/activation disagreement. They do not establish the truth or sufficiency of the contents.

Frontmatter uses flat `key: value` properties and scalar lists (`[]`, JSON-style inline arrays, or indented `- value` lines). Quote dates/placeholders/strings where necessary. Unsupported YAML produces a diagnostic requiring another validator; the tool does not claim to parse all YAML. Record dependencies use stable IDs. Code fences and inline code are excluded from link scans. External links are not fetched. Private/raw evidence bodies, symlinks, hidden folders, dependency caches, and their contents are not traversed. Links to excluded files can be checked for existence without reading their content.

The initializer sets the supplied owner as the initial write owner. Other delegated owners and approvers stay unresolved. A partially interrupted initialization may leave an incomplete destination; inspect it and choose a recovery action rather than rerunning over it.

Run the fixture suite from the package root:

```bash
python3 30_tests/01_test_eagos.py -v
python3 20_tools/00_eagos.py check 10_eagos_project_starter --mode template --fail-on-warnings
```

See the [quick start](../01_quick_start.md) and [upgrade guide](../02_upgrade_guide.md). The maintained specification is `00_eagos.md` at the package root. `EAGOS_SPEC_PATH` selects a candidate in the core tests.

## Discovery extension

EAGOS Discovery / ODS 1.3.0 uses a separate optional CLI, `python3 20_tools/01_discovery.py --help`, and the existing EAGOS helper module. It leaves execution-project records and activation under the core toolkit. The interactive playbook governs conversation; this tool handles files and structural checks only.

```bash
python3 20_tools/01_discovery.py init ../my_discovery --code IDEAS --name "Opportunity portfolio" --owner "Your name"
python3 20_tools/01_discovery.py init ../my_discovery --code IDEAS --name "Opportunity portfolio" --owner "Your name" --apply
python3 20_tools/01_discovery.py check ../my_discovery
python3 20_tools/01_discovery.py check ../my_discovery --format json
python3 30_tests/02_test_discovery.py -v
```

Initialization copies the eight generic Markdown files into a new destination and records a baseline manifest. Preview does not write; `--apply` refuses existing destinations and symlink components. A partial interruption may leave a new incomplete directory; inspect it before deciding how to recover. The manifest supports manual comparison; core `drift` remains specific to the execution starter.

`check` reads flat properties and `discovery` fenced records in the authoritative `00_opportunity_workspace.md`. It checks record IDs/types, required fields, cross-references, vocabulary, reported budget/cap counts, cumulative investigations, portfolio-wide open validation slots, claim/source compatibility, rating ranges, track compatibility, mandatory screens, selection references, and receipt fields. It never edits records or traverses private/raw evidence. Exit codes are 0 for no errors, 1 for integrity findings, and 2 for invalid input/operational failures. Review warnings in context; they do not confer approval.

This checker does **not** rank opportunities, verify actual query counts/time, inspect external sources, establish claim truth or independence, assess complete economics/test methodology, authenticate approvals, check receiving-project activation, or prove acceptance. Prose and search logs still need review. Additional authoritative workspace files are not silently ingested; retain structured records in the single workspace under schema 1. For an uninstantiated starter, inspect its templates and links; `check` expects an instantiated portfolio identity.

See the [discovery guide](../03_opportunity_discovery.md) and [protocol](../11_opportunity_discovery_starter/02_discovery_protocol.md).

Supported extension versions are defined by the discovery CLI; unsupported versions are rejected. Prose seeds, conversation checkpoints and journals are intentionally outside the structural checker. A valid empty portfolio can support a conversation without any research records. Preserve the original installation manifest when upgrading; record the migration separately.

## Unified conversational lifecycle

The tools install files and check structure; an AI agent uses [the operating guide](../04_operating_guide.md) to conduct the conversation. The root guide is the maintained distribution source; its portable core/discovery copies must match. P0 includes `01_operating_guide.md` alongside its hub and agent contract. Discovery includes the same guide as `03_operating_guide.md`.

Core records may declare `lifecycle_stage` using `discover`, `shape`, `incubate`, `develop`, `launch`, `operate`, or `evolve`. The checker reports unsupported values in live records; the field is optional for older records and never grants activation or authority. It does not interpret or execute natural-language instructions, assess stage appropriateness, or prove launch completion.

Run `python3 30_tests/03_test_unified.py -v` for portable-guide installation, manifest consistency, optional-stage validation, and non-activation regression checks. The [conversation scenarios](../30_tests/04_conversation_scenarios.md) define separate behavioral evaluation; they require actual responses and review before claiming conversational effectiveness.

## EAGOS 4 governance diagnostics

The maintained CLI is `00_eagos.py`. New projects receive `00_eagos_manifest.json`. Existing interfaces and supported schemas are listed once in the [adoption guide](../02_upgrade_guide.md).

The core `check` command also reads optional Task, role, delegation, deployment, recurring-process and attempt records. It checks Task/legacy-activity completion and readiness, exact delegation operation/target subsets, valid date intervals, parent status and issuer, permitted subdelegation, cycles, finite nonnegative allocations, matching units and summed active child allocations. It checks declared deployment evidence/activation references, attempt-to-Task references, duplicate running/succeeded/uncertain run keys and declared stale/disputed evidence dependencies.

Use exact allowlists and decimal budget strings. Every active delegation has `valid_from`, `expires_on`, `budget_limit`, `budget_unit`, `subdelegation`, issuer/delegate, scope, approver and authorization evidence. Root grants rely on actual human authority; this tool cannot authenticate it. Child allocations reserve part of their parent's budget; actual use must still be metered by a runtime/manual control. No wildcard or semantic scope interpretation is supported.

Optional `evidence_refs` contains supporting record IDs. The tool flags missing references and stale/disputed declared support for ready/running/active records. It does not decide evidence truth, adequacy or actual provenance. Prose-only relationships require review.

A passing diagnostic cannot enforce access, track actual resource use, revoke jobs, detect all duplicate external effects, prove test evidence authenticity or activate a runtime. Templates in `60_templates/` remain uninstantiated and are not treated as live records. Run `python3 30_tests/05_test_governance.py -v` for the bounded synthetic regression cases.

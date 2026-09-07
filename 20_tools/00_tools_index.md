# Offline ELAEF tools

Run `python3 20_tools/00_elaef.py --help` from the package root. Python 3.9+ and its standard library are sufficient. Tools do not use the network, send information, approve gates, or migrate existing projects.

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
python3 30_tests/01_test_elaef.py -v
python3 20_tools/00_elaef.py check 10_elaef_project_starter --mode template --fail-on-warnings
```

See the [quick start](../01_quick_start.md) and [upgrade guide](../02_upgrade_guide.md). The private maintenance workspace's canonical specification lives in its separately indexed Obsidian vault; the public distribution carries its portable copy at the repository root.

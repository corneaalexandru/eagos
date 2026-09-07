# Evidence-Led Agent Execution Framework

ELAEF 3.5 helps humans and AI agents turn an idea into evidence-backed project execution, with clear records, useful next actions, and explicit authority for commitments.

> Build by evidence, one gate at a time.

Start with the [quick start](01_quick_start.md). Use the [full specification](00_evidence_led_agent_execution_framework.md) as a reference and the [agent contract](10_elaef_project_starter/AGENTS.md) for routine work. Existing projects can adopt improvements through the [upgrade guide](02_upgrade_guide.md).

## Create a project

With Python 3.9+ installed, run from this repository:

```bash
python3 20_tools/00_elaef.py init ../my_project --code DEMO --name "My project" --owner "Your name" --profile P0
```

Review the preview, then repeat with `--apply`. Use P0 for a small reversible project, P1 for collaboration, or P2 for higher-consequence work. Unknown facts and approvals remain unresolved; setup does not activate execution.

```bash
python3 20_tools/00_elaef.py check ../my_project --mode setup
```

Manual copying is also supported. The numbered [starter](10_elaef_project_starter/README.md) and [P0 hub](10_elaef_project_starter/70_profiles/03_p0_project.md) are plain Markdown with YAML properties and relative links. Open the project folder in Obsidian or copy it into a vault; no community plugin is required.

## What's included

- [Complete specification](00_evidence_led_agent_execution_framework.md) — evidence, activities, gates, authority, numbering, and handovers
- [Project starter](10_elaef_project_starter/README.md) — P0/P1/P2 controls and templates
- [Offline tools](20_tools/00_tools_index.md) — setup, structural checks, inventory, and baseline comparisons
- [Regression fixtures](30_tests/00_tests_index.md) — repeatable checks, also run by GitHub Actions
- [Changelog](CHANGELOG.md) — versions and compatibility

Checks identify structural issues; they do not prove source truth, pass gates, grant authority, or accept a handover. Read the [documented limits](02_upgrade_guide.md#compatibility-and-limitations).

## Get updates

```bash
git pull --ff-only
```

Keep actual project work in its own folder. Updating this toolkit does not overwrite or migrate those projects. Use the upgrade guide to assess changes before adoption.

## License

No license has been selected. Public visibility does not itself grant an explicit reuse license. License selection remains an owner decision.

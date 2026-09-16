# ELAEF — Discover, develop, launch, and evolve

ELAEF 3.6.0 is one evidence-led framework for working with an AI agent from early ideas through incubation, development, launch, operation, and improvement.

Use ordinary conversation. The agent contributes possibilities, recommends the next useful move, progresses authorized work, and keeps the context current.

Start with the [operating guide](04_operating_guide.md), or say:

> Help me discover and develop worthwhile ideas through to completion or operation. Be an active thinking partner, suggest useful next steps, and keep the process simple. Continue ready work within our agreed scope and ask one important question when you need my input.

The shared lifecycle is **Discover → Shape → Incubate → Develop → Launch → Operate → Evolve**. Stages may repeat or change direction, and a personal or creative project can complete without becoming a business. Stage labels and recommendations do not authorize commitments.

## Start or continue

| Need | Entry point |
|---|---|
| Work conversationally | [Operating guide](04_operating_guide.md) |
| Create or adapt a workspace | [Quick start](01_quick_start.md) |
| Use detailed opportunity research | [Discovery guide](03_opportunity_discovery.md) |
| Adopt an update | [Upgrade guide](02_upgrade_guide.md) |
| Inspect the complete framework | [Specification](00_evidence_led_agent_execution_framework.md) |

## Optional command-line setup

Plain Markdown use requires no plugin. With Python 3.9+, preview a lightweight workspace:

```bash
python3 20_tools/00_elaef.py init ../my_workspace --code IDEAS --name "Ideas and initiatives" --owner "Your name" --profile P0
```

Repeat with `--apply` to create it, then check it:

```bash
python3 20_tools/00_elaef.py check ../my_workspace --mode setup
```

The package also includes the [core starter](10_elaef_project_starter/README.md), optional [discovery starter](11_opportunity_discovery_starter/README.md), [offline tools](20_tools/00_tools_index.md), and [test suite](30_tests/00_tests_index.md). Structural checks do not establish evidence truth, readiness, authorization, conversation quality, or acceptance.

## Updates and compatibility

```bash
git pull --ff-only
```

Updating this repository does not migrate separate project workspaces. Preserve their records, IDs, evidence, approvals, and original manifests; use the upgrade guide before adopting changes.

## License

No license has been selected. Public visibility does not itself grant an explicit reuse license.

---
title: EAGOS Discovery
type: extension_guide
extension: EAGOS-ODS
extension_version: "1.3.0"
framework_version: "4.0.0"
updated: 2026-09-16
---

# EAGOS Discovery

Use the [shared operating guide](04_operating_guide.md) from discovery through incubation, development, launch, operation, and evolution. This optional module adds detailed opportunity research, comparison, selection, and receipt records within the same conversational experience.

Discover and shape opportunities with an AI agent through conversation. Start without an idea, bring an observation or rough concept, or resume earlier thinking. The agent contributes possibilities, builds on your reactions, and asks one useful question at a time.

Research enters when a factual uncertainty matters. You do not need a complete profile, budget, business model, or ranked shortlist to begin.

## Start here

- Use the [interactive kickoff](11_opportunity_discovery_starter/01_agent_kickoff_prompt.md) with an AI agent.
- Resume your working portfolio for current ideas and the conversation checkpoint.
- Read the [playbook](11_opportunity_discovery_starter/04_interactive_discovery.md) for conversation moves and examples.
- Use the [protocol](11_opportunity_discovery_starter/02_discovery_protocol.md) and [templates](11_opportunity_discovery_starter/60_templates/00_discovery_records.md) when research, comparison, or handoff needs formal records.

Explore, shape, research, challenge, compare, and prepare are flexible moves. Say “try another angle,” “combine these,” “research that assumption,” or “help me shape this into a project.” The agent records material changes and preserves alternatives.

Discovery owns idea history and comparison. After an accepted handoff, the receiving project owns execution state. Interest, research, scores, and generated folders do not authorize selection or launch.

## Create another portfolio

From this package root, preview, create, and check:

```bash
python3 20_tools/01_discovery.py init ../my_discovery --code IDEAS --name "Opportunity portfolio" --owner "Your name"
python3 20_tools/01_discovery.py init ../my_discovery --code IDEAS --name "Opportunity portfolio" --owner "Your name" --apply
python3 20_tools/01_discovery.py check ../my_discovery
```

The parent must exist; initialization refuses existing destinations and symlink components. It creates eight Markdown files and a baseline manifest. Manual copying of the [generic starter](11_opportunity_discovery_starter/README.md) is also supported.

Use the files with an agent that can read them, or supply them as context. Without write access, the agent returns a copyable checkpoint and discloses that it was not saved. No hosted application, plugin, or autonomous runtime is required.

## Records and lifecycle

Discovery uses Markdown, schema-1 records and optional Python 3.9+ tools. Current extension version: 1.3.0. The extension identifier is `EAGOS-ODS`. Structural checks cannot prove conversation quality, source truth, actual research effort, approval identity or receiving-project acceptance.

For an existing portfolio, follow the [adoption guide](02_upgrade_guide.md). Preserve the workspace, IDs, evidence, history and original manifest; merge local customizations rather than replacing state with a blank template.

To remove the extension, stop cycles, preserve/export the workspace and handoff references, and remove navigation/tool use. Receiving projects retain their own records and authority.

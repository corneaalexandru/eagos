---
title: Opportunity Discovery and Selection
type: extension_guide
extension: ELAEF-ODS
extension_version: "1.2.0"
framework_version: "3.6.0"
updated: 2026-09-14
---

# Opportunity Discovery and Selection

Use the [shared operating guide](04_operating_guide.md) from discovery through incubation, development, launch, operation, and evolution. This optional module adds detailed opportunity research, comparison, selection, and receipt records within the same conversational experience.

Discover and shape opportunities with an AI agent through conversation. Start without an idea, bring an observation or rough concept, or resume earlier thinking. The agent contributes possibilities, builds on your reactions, and asks one useful question at a time.

Research enters when a factual uncertainty matters. You do not need a complete profile, budget, business model, or ranked shortlist to begin.

## Start here

- Use the [interactive kickoff](11_opportunity_discovery_starter/01_agent_kickoff_prompt.md) with an AI agent.
- Resume your own working portfolio for current ideas and the conversation checkpoint.
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

## Compatibility and lifecycle

| Item | Contract |
|---|---|
| Extension | `ELAEF-ODS` 1.2.0; unified interface over locally verified ELAEF 3.6.0 |
| Core rules | Evidence levels, phases, gates, and P0/P1/P2 remain unchanged |
| Records | Schema 1; prose checkpoint/idea board/journal and existing structured research, decision, and handoff records |
| Authority | Actual owner instructions and valid envelopes; templates grant none |
| Tools | Markdown; optional Python 3.9+ standard-library CLI using `00_elaef.py` |
| Failure | Preserve partial/conflicting evidence, report failed retrievals, stop the affected action, continue independent authorized work |
| Checks | Accept ODS 1.0.0, 1.1.0, 1.1.1, and 1.2.0; unsupported versions fail |
| Limits | Structural checks cannot prove conversation quality, source truth, actual research effort, approval identity, or receiving-project acceptance |

To upgrade, preserve the workspace, IDs, evidence, history, and original manifest. Reconcile generic changes with local customizations; never replace active state with a blank template. From 1.0.0, add the playbook and conversational sections. From 1.1.0/1.1.1, review the unified guide and contract, add initiative continuity pointers where useful, and preserve all current records. Schema 1 requires no conversion. Existing workspaces retain their declarations until reviewed adoption.

To remove the extension, stop cycles, preserve/export the workspace and handoff references, and remove navigation/tool use. Receiving projects continue under their own authority.

Personal portfolios and maintenance history stay outside this public package. Earlier research remains history and does not set the owner's current direction.

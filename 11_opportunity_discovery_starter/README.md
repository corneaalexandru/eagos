---
title: "{{PROJECT_NAME}}"
type: discovery_portfolio
extension: EAGOS-ODS
extension_version: "1.3.0"
framework_version: "4.0.0"
owner: "{{PROJECT_OWNER}}"
naming_profile: portable_markdown_v1
numbering_profile: numbered_project_v1
---

# Opportunity discovery portfolio

Use this workspace with an AI agent to discover opportunities, business ideas and new projects through conversation. Explore possibilities, react to them, reshape them and bring in research when it can resolve a useful question. You can start without an idea or return to one already taking shape.

Start by saying: **“Help me discover ideas interactively. Let's explore a few directions and build on my reactions.”** The [kickoff prompt](01_agent_kickoff_prompt.md) gives the full reusable instruction. The agent keeps the records while you focus on the ideas.

The [shared operating guide](03_operating_guide.md) covers incubation, development, launch, operation, and improvement as well. This portfolio retains discovery history; follow linked receiving-project records after accepted handoff. Keep one conversational experience and one authoritative location for each current fact.

## Read in this order

1. [Workspace](00_opportunity_workspace.md) — the only authoritative mandate, current state, research records, decisions, and continuity record.
2. [Agent operating contract](AGENTS.md) — authority, research loop, and stopping rules.
3. [Interactive discovery](04_interactive_discovery.md) — conversation moves, idea shaping, research transitions and resumption.
4. [Kickoff prompt](01_agent_kickoff_prompt.md) — interactive default and optional research prompts.
5. [Protocol](02_discovery_protocol.md) — evidence, comparisons and execution handoff when relevant.
6. [Record templates](60_templates/00_discovery_records.md) — copy individual records when needed.

This README is navigation, not a second status record. Keep the initial portfolio in one workspace. Add separate evidence notes only when source volume warrants it. Stable IDs survive splitting; update the authoritative location explicitly before moving a record.

## Begin with a conversation

Start from a curiosity, problem, desired outcome or rough idea. Keep a small idea board and conversation checkpoint; do not require sources, scores, a complete mandate or an investment budget to explore. Unknowns remain explicit. The owner can change direction, combine ideas, ask for research or pause and resume.

## When research becomes useful

Fill the owner, mandate, current request reference, allowed research actions, limits, and one current activity. Leave unknowns visible. Installation prepares records; it does not authorize research or approve selection. A current owner request for a bounded research cycle can supply that authority without a second approval ceremony.

Use public sources when authorized. Read existing project records only when relevant and accessible within the request. Treat prior-chat project names as context until their actual records are reconciled. Never infer available money, time, customer access, or employer permission from biography.

## Optional checking

From the EAGOS package, run `python3 20_tools/01_discovery.py check PATH_TO_THIS_PORTFOLIO`. The tool reads the workspace and reports selected structural issues. It never fetches sources, updates records, ranks opportunities, grants approval, or checks whether a human truly accepted a handoff. Manual Markdown use remains complete without it.

The baseline manifest records original file hashes and source paths for manual upgrade comparison. Keep it as installation evidence; it is not current project truth. Core project `drift` is not the discovery migration tool. The checker does not validate conversation checkpoints, idea-board prose or agent behavior.

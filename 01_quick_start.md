# Start working with ELAEF

Use one instruction for ideas, incubation, development, launch, and ongoing work:

> Help me discover and develop worthwhile ideas through to completion or operation. Be an active thinking partner: offer possibilities, build on my reactions, challenge assumptions, and suggest the next useful step. Keep the process simple and our records current. Continue ready work within our agreed scope; ask one important question when you need my input.

Add your idea, goal, or current situation if you have one. “Help me find an idea” is enough to begin a conversation. Afterward, use ordinary instructions such as “continue,” “review,” “change direction,” or “pause.”

The [operating guide](04_operating_guide.md) explains the shared lifecycle and what the agent should do.

## What the agent handles

1. Read existing context and the live checkpoint; recognize the useful lifecycle stage.
2. Contribute useful thinking or work, propose the next worthwhile move, and resolve one important uncertainty at a time.
3. Use a small idea board initially. Add evidence, activities, decisions, and initiative records as sustained work or consequence requires.
4. Preserve alternatives and corrections, carry valid authority forward, and update affected records.
5. Save enough context to resume. Without write access, return a copyable checkpoint and disclose that it was not saved.

Conversation and internal setup can precede activation within their actual authority. Further investigation, development, or launch must satisfy applicable project gates and approved scope. Existing stronger controls remain in force.

## Optional workspace setup

Provide the files to an AI agent, copy the starter, or ask the agent to set up a workspace. Choose P0 for low-consequence reversible work; use P1/P2 when collaboration, policy, or consequence requires stronger controls.

For the agent or maintainer, from this package root:

```bash
python3 20_tools/00_elaef.py init ../my_workspace --code IDEAS --name "Ideas and initiatives" --owner "Your name" --profile P0
```

This previews the files. Add `--apply` to create them, then run `check ../my_workspace --mode setup`. The parent must exist; existing destinations and symlink components are refused. Facts and approvals remain unresolved. Inspect an interrupted creation before recovery.

P0 creates a hub, agent contract, portable operating guide, Git exclusions, and installation manifest. For manual setup, copy `70_profiles/03_p0_project.md` from the execution starter as `README.md`, plus `AGENTS.md`, `01_operating_guide.md`, and `.gitignore`. A manifest is optional.

Open the folder as an Obsidian vault or place it in an existing vault. Start with its README; no community plugin is required. Check relative links after moving individual templates.

## Existing work and deeper methods

Inventory existing records first. Preserve IDs, evidence, owner instructions, approvals, and original manifests. Link to existing execution state; do not recreate it in a portfolio or infer inactivity from an old summary.

For detailed opportunity research, use [ODS](03_opportunity_discovery.md) when it helps the current question. You can still brainstorm and shape initiatives directly in a core workspace.

Use the [upgrade guide](02_upgrade_guide.md) before adopting changes and the [tool guide](20_tools/00_tools_index.md) for structural checks. A clean check does not establish evidence truth, readiness, authorization, or acceptance.

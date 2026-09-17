# Start working with EAGOS

Turn an unclear idea, problem, or objective into a practical project with classified knowledge, evidence-backed decisions, authorized activities, measurable outputs, and durable records.

> Help me turn this idea, problem, or objective into a practical result. Contribute useful thinking, classify what we know and assume, and suggest the next useful step. Continue ready work within our agreed authority, validate results, and keep the records current. Ask one important question when my input is needed.

Bring the actual situation. “Help me find an idea” is also a valid starting point; an existing problem needs no discovery exercise. Continue with ordinary instructions such as “review,” “change direction,” or “pause.” The [operating guide](04_operating_guide.md) explains the interaction.

## What the agent handles

1. Read existing context and the live checkpoint; recognize the useful lifecycle stage.
2. Contribute useful thinking or work, propose the next worthwhile move, and resolve one important uncertainty at a time.
3. Start with the supplied objective or a small idea seed. Add Tasks, evidence, decisions and initiative records as sustained work or consequence requires.
4. Preserve alternatives and corrections, carry valid authority forward, and update affected records.
5. Save enough context to resume. Without write access, return a copyable checkpoint and disclose that it was not saved.

Conversation and internal setup can precede activation within their actual authority. Further investigation, development, or launch must satisfy applicable project gates and approved scope. Existing stronger controls remain in force.

## Optional workspace setup

For a small task, begin with one sentence: “The result I need is …; I will know it works when …”. The agent should use known context to define the next output, its check and applicable authority, then do ready work. Add records as they become useful. You do not need to name a lifecycle stage, design an organization chart or fill every hub field first.

The P0 hub has one combined current Task/checkpoint. Record unknowns where they matter; add evidence entries only when evidence exists. If several sections repeat the same fact, keep its current value in one place and link to it. Use P1/P2 when consequence or existing policy requires their controls.

Provide the files to an AI agent, copy the starter, or ask the agent to set up a workspace. Choose P0 for low-consequence reversible work; use P1/P2 when collaboration, policy, or consequence requires stronger controls.

For the agent or maintainer, from this package root:

```bash
python3 20_tools/00_eagos.py init ../my_workspace --code DEMO --name "My project" --owner "Your name" --profile P0
```

This previews the files. Add `--apply` to create them, then run `check ../my_workspace --mode setup`. The parent must exist; existing destinations and symlink components are refused. Facts and approvals remain unresolved. Inspect an interrupted creation before recovery.

P0 creates a hub, agent contract, portable operating guide, Git exclusions, and installation manifest. For manual setup, copy `70_profiles/03_p0_project.md` from the execution starter as `README.md`, plus `AGENTS.md`, `01_operating_guide.md`, and `.gitignore`. A manifest is optional.

Open the folder in your preferred Markdown editor. Start with its README; no editor-specific plugin is required. Check relative links after moving individual templates.

## Existing work and deeper methods

Inventory existing records first. Preserve IDs, evidence, owner instructions, approvals, and original manifests. Link to existing execution state; do not recreate it in a portfolio or infer inactivity from an old summary.

For detailed opportunity research, use [ODS](03_opportunity_discovery.md) when it helps the current question. You can still brainstorm and shape initiatives directly in a core workspace.

Use the [upgrade guide](02_upgrade_guide.md) before adopting changes and the [tool guide](20_tools/00_tools_index.md) for structural checks. A clean check does not establish evidence truth, readiness, authorization, or acceptance.

## Add organization or runtime controls when needed

Use [agent organization](05_agent_organization.md) for responsibilities and delegation, [company operations](06_company_operations.md) for recurring work, and [runtime integration](07_runtime_integration.md) before configuring software. Templates for roles, delegations, deployments, recurring processes and task attempts are in the core starter. They create no team, schedule, account connection or permission.

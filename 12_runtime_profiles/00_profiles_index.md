# EAGOS Runtime Profiles

All profiles in 4.0.0 are **documented**. No supported installation/version combination has yet passed the integration acceptance suite in this distribution.

| Profile | Intended use | Current state |
|---|---|---|
| [Manual agent](03_manual_agent.md) | Human-directed agent using portable records | Documented method; actual capabilities depend on the host |
| [OpenClaw](01_openclaw.md) | Configured agents, workspaces, tool use and coordination | Candidate mapping; not configured/tested/active |
| [LangGraph](02_langgraph.md) | Custom stateful workflows with explicit orchestration | Candidate mapping; not configured/tested/active |

See the [integration contract](../07_runtime_integration.md). Each deployed profile must pin its exact software/model versions, record a configuration fingerprint, and collect actual control evidence. Documentation access on 2026-09-16 is source evidence, not installed-version compatibility.

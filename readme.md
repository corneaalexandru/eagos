---
title: EAGOS 5.1.0
type: overview
status: active
framework: EAGOS
framework_version: "5.1.0"
updated: 2026-09-25
---

# EAGOS 5.1.0

**Evidence-led Agent Governance and Operations System**

*From intent to governed action.*

*Build by Evidence, One Gate at a Time.*

Turn an unclear idea, problem, or objective into a practical project with classified knowledge, evidence-backed decisions, authorized activities, measurable outputs, and durable records.

EAGOS is a standalone methodology with an optional deterministic Python engine. Use it manually, in Markdown or Obsidian, with ChatGPT, Claude, Codex or another agent, or inside an organization's software. No particular operating environment or provider is required.

## Start with a conversation

1. Read [the core contract](eagos.md). Bring an idea, problem, question, objective, existing project, operational activity or decision to investigate.
2. Keep a project note. Adapt [the one-file example](examples/project.md), retaining only useful sections. Create folders progressively when work needs them.
3. Give your assistant the contract, current note and actual authority, then say:

> Help me turn this idea, problem, or objective into a practical result using EAGOS. Distinguish what we know from what we assume, identify the next useful step, gather evidence where needed, carry out authorized work, validate the result, and keep the project records current. Ask me only when a material decision, missing dependency or authority issue requires my input.

For example: “I have this business idea. Help me investigate it.” Clarify the idea, test its assumptions and use the findings to decide what comes next. No software installation is needed for this path. A copied example or prompt grants no authority.

## Optional Python engine

Use Python 3.9 or later. The library checks explicit rules; people and agents assess evidence quality and make judgments. See the contract's implementation boundary before integrating it.

The [governance API](eagos/governance.py) exposes `validate_policy`, `authority_reasons`, `validate_decision` and `process_reasons`; [tests](tests/test_governance.py) contain executable examples. Existing schema-1 policies declaring 5.0.x remain accepted.

Roles may add `authority_kinds` (`read`, `write`, `external`, `approval`), `parent_role` and `max_attempts`. Pass the actual `authority_kind` and, when required, complete `usage_by_role` and `attempts_by_role` counters to `authority_reasons`. Counts are direct per role; the engine calculates ancestor totals including siblings and descendants. Failed attempts still count. Decision records may add `expires_at`.

`process_reasons` checks declared status, `max_parallel`, `max_runs`, `budget_minor` and `expires_at` against supplied occurrence counts and resource use. It neither schedules work nor replaces action authority checks. Hosts must maintain accurate counters and enforce results; the engine does not authenticate callers or collect usage itself.

```sh
python3 -m unittest discover -s tests -v
python3 check.py
```

These checks validate the library and documents, not operational enforcement. [Sources](sources.md) record provenance and compatibility boundaries.

## License

Owner-controlled code and documentation are licensed under [Apache-2.0](LICENSE). [NOTICE](NOTICE) preserves attribution and clarifies trademark and third-party boundaries.

# Discovery record gallery

Copy only the needed block to the authoritative workspace. Replace example IDs and values, preserve literal `unknown` when a fact is missing, and add explanation after the block. These are synthetic templates, not live facts, approvals, or research. IDs start with the portfolio code. Dates use ISO 8601. Flat fields and scalar lists are supported; nested YAML is not. Use quoted strings containing colons or hashes.

## Cycle

```discovery
id: DEMO-CYC-0001
type: cycle
status: planned
scope: Broad preliminary exploration
authority: unknown
started_on: unknown
query_limit: 12
source_limit: 20
candidate_limit: 10
investigation_limit: 3
minutes_limit: 45
queries_used: 0
sources_used: 0
minutes_used: 0
investigated_candidates: []
stop_reason: unknown
result: unknown
```

Statuses: planned, in-progress, complete, paused. Record adopted cap rationale and the owner research instruction. The portfolio-wide `validation_limit` is authoritative in the workspace frontmatter and applies across cycles. After the block maintain a dated search log with the actual query strings, source inspection attempts and outcomes, and cumulative effort. `sources_used` counts inspection attempts, not just successfully registered sources. Completed/paused runs require an actual stop reason and result, including partial or no-new-commitment results.

## Source

```discovery
id: DEMO-SRC-0001
type: source
title: Replace with the inspected source title
kind: public
status: inspected
location: unknown
origin: unknown
published_on: unknown
inspected_on: unknown
independence_group: unknown
finding: unknown
locator: unknown
limitations: unknown
```

Kinds: public, internal, synthetic, search_lead. Statuses: inspected, partial, unavailable. A public source should link to the precise page. Internal locators must not expose private data to external searches. Record a partial/inaccessible page as such and explain what was observable. Never use the template as inspected evidence.

## Signal

```discovery
id: DEMO-SIG-0001
type: signal
source_ids: ["DEMO-SRC-0001"]
lens: repeated_problems
observation: unknown
interpretation: unknown
```

Keep the observed fact distinct from the possible opportunity it suggests. An owner-provided idea may begin without a signal; label it a hypothesis and investigate it.

## Candidate

```discovery
id: DEMO-OPP-0001
type: candidate
cycle_id: DEMO-CYC-0001
track: commercial
status: framed
title: Replace with a precise opportunity title
beneficiary: unknown
problem: unknown
situation: unknown
consequence: unknown
alternatives: unknown
mechanism: unknown
access_route: unknown
value_model: unknown
signal_ids: []
critical_unknown: unknown
next_action: Frame a testable beneficiary and problem hypothesis
validation_slot: none
```

Tracks: commercial, strategic_creative, internal_tool. For parked/rejected items add `reason` and `reopen_trigger`; for merged items add `merged_into`. For selected/promoted items add `selection_decision`. For promoted items add `handover_id`. `validation_slot` is none/open/closed; selected/promoted VALIDATE work uses open until verified execution completion, cancellation, or explicit release, then closed with `validation_completion_evidence`. A new cycle does not reset an open slot.

## Claim

```discovery
id: DEMO-CLM-0001
type: claim
candidate_id: DEMO-OPP-0001
claim: The stated beneficiary has the specific problem under investigation
context: market
status: unknown
evidence_level: E0
supporting_sources: []
opposing_sources: []
decision_context: Whether to investigate this problem further
rationale: No source inspected for this claim yet
limitations: unknown
review_on: unknown
```

Contexts: market, operational, preparation. Statuses: unknown, supported, disputed, refuted, stale. Non-E0 assessments need evidence references and a rationale appropriate to the claimed level. Refuting sources may justify a refuted claim's evidence profile without supporting its proposition. Do not infer that two URLs are independent or that E4 follows from a source count.

## Screening record

```discovery
id: DEMO-SCR-0001
type: screen
candidate_id: DEMO-OPP-0001
constraint: time_capacity
result: unknown
scope: Next bounded internal investigation
reason: Required effort and available owner time are unresolved
basis: unknown
```

One current record per candidate/constraint. Record changes in dated prose rather than duplicate current outcomes. The default constraints are in the workspace's `required_filters` property.

## Criterion assessment

```discovery
id: DEMO-ASM-0001
type: assessment
candidate_id: DEMO-OPP-0001
profile: commercial
criterion: problem_value
low: unknown
high: unknown
claim_ids: ["DEMO-CLM-0001"]
rationale: No rating until the importance of the problem has a basis
```

Use one record per candidate/criterion. Numeric bounds are 1–5; both endpoints must be unknown together, or justified numeric values with low <= high. The profile must match the candidate track. Use all eight criteria for a complete score; a partial contribution must show coverage. Add the comparison narrative, economic/outcome model, downside/sensitivity pass, and existing-project/no-commitment alternatives in prose. The checker does not calculate or rank candidates.

## Next experiment proposal

```discovery
id: DEMO-EXP-0001
type: experiment
candidate_id: DEMO-OPP-0001
status: proposed
hypothesis: unknown
decision_changed: unknown
inputs_or_participants: unknown
method: unknown
measurement: unknown
success: unknown
failure: unknown
inconclusive: unknown
resources: unknown
data_and_privacy: unknown
authority_required: unknown
stop_condition: unknown
```

This extension records proposed experiments. Conduct/results belong in a separately authorized research activity or the receiving execution project. Do not change this proposal into an executed test without authority, predeclared thresholds, and actual result evidence.

## Selection or other decision

```discovery
id: DEMO-DEC-0001
type: decision
status: proposed
outcome: defer
candidate_ids: []
date: unknown
approver: unknown
authorization_evidence: []
target_stage: unknown
objective: unknown
scope: unknown
exclusions: unknown
resources: unknown
conditions: unknown
review_trigger: unknown
```

Outcomes: select, park, reject, defer, no_new_commitment, strengthen_existing. Statuses: proposed, approved, rejected, superseded. An approved select decision identifies exactly one candidate and a DEFINE, DISCOVER, or VALIDATE stage, plus the actual approval basis and resource envelope. Optional `expires_on` must be current when used. Multiple validation selections remain constrained by the portfolio's cap. A decision to select does not certify acceptance or activation.

## Execution handover

```discovery
id: DEMO-HND-0001
type: handover
candidate_id: DEMO-OPP-0001
decision_id: DEMO-DEC-0001
status: draft
target_stage: unknown
claim_ids: []
remaining_hypotheses: unknown
risks: unknown
success: unknown
failure: unknown
first_activity: unknown
next_gate: unknown
execution_state: unknown
receiver: unknown
accepted_on: unknown
acceptance_evidence: []
```

Statuses: draft, ready_for_review, transferred, accepted, accepted_with_conditions, rejected, expired. Before transfer, complete the packet and specify the first L5 activity's purpose, inputs, predecessors, output, completion check, authority, and stopping condition in prose. The linked decision owns objective/scope/resources. Accepted-with-conditions packets add `conditions` and `permitted_work`. Actual receiver evidence is required; writing an acceptance field is not proof of receipt. The receiving project assesses its own activation and gate readiness.

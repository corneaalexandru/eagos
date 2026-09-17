---
title: Opportunity Discovery and Selection Protocol
type: extension
extension: EAGOS-ODS
extension_version: "1.3.0"
framework_version: "4.0.0"
updated: 2026-09-14
---

# Opportunity Discovery and Selection Protocol

Use the [shared operating guide](03_operating_guide.md) throughout the lifecycle. This protocol supplies detailed discovery methods; after actual handoff, follow the receiving project for development, launch, operation, and evolution.

Begin with the [interactive discovery playbook](04_interactive_discovery.md): explore, shape and challenge possibilities with the owner, and use research when a factual uncertainty matters. This protocol governs research, formal comparison and handoff; it is not a mandatory intake questionnaire or a requirement to research before brainstorming. EAGOS execution develops a selected opportunity through its existing phases and gates. Selection approves only the stated next stage, not business viability or launch.

## 1. Research and decision sequence

| Stage | Work and minimum output | Exit check |
|---|---|---|
| Orient | Reconcile mandate, authority, existing commitments, decisions, and current activity | A bounded activity is ready; material unknowns are visible |
| Scan | Collect dated, traceable observations through relevant search lenses | Sources and observations are distinguishable from interpretations |
| Frame | Define beneficiary, situation, problem, alternatives, possible mechanism, access, value, and critical uncertainty | Distinct opportunity hypothesis; deduplicated against the portfolio |
| Screen | Assess mandatory constraints for the next contemplated commitment | Each filter is pass/fail/unknown with basis; failures cannot be offset |
| Investigate | Examine decision-changing claims and counterevidence for a limited shortlist | Sources inspected within limits; evidence scope and gaps recorded |
| Compare | Compare within an appropriate track; include existing work and no commitment | Ratings have reasons; unknowns remain visible; sensitivity tested |
| Recommend | Prepare the smallest useful next commitment and its test | A reviewable decision package, including a valid no-commitment option |
| Handover | Transfer only the approved stage, objective, resources, and evidence | Receiving project acknowledges receipt and controls its own activation |

These checks apply when the corresponding activity is needed; they are not eight mandatory owner approvals. Early conversational seeds use the lightweight workspace idea board without a formal cycle. Within existing authority, the agent can frame, deduplicate, screen, research, and compare. A material owner choice or expanded external commitment requires the applicable decision.

## 2. Mandate and authority

Record desired outcomes, relevant capabilities, existing commitments, hours/work pattern, financial horizon, budget/loss limits, geography/access, exclusions, and research permissions progressively as they become relevant. Do not turn this list into a required intake form. Each material field is confirmed, proposed, assumed, or unknown, with its basis. A mandate can be usable for exploration while incomplete for investment or execution.

The current user instruction supplies authority when its scope covers the work. Record that instruction and carry it forward. Unknowns do not require repeated questions when an independent authorized task can progress. Silence never confirms a proposed priority or expands permission.

Default first-cycle ceilings are proposed operating settings: **12 queries, 20 source inspections, 10 candidates, 3 deeper investigations, 1 concurrent newly selected validation project, 45 research minutes**. Adopt them explicitly in the cycle record. Count queries individually even when sent in one tool call; count inspection attempts, including failures; count research effort across resumptions. Source rereads consume an inspection unless using a still-current local note without another retrieval. Log actual queries and inspections in prose after the cycle record. The CLI checks reported counts, not tool execution or elapsed effort.

The 10-candidate and 3-investigation limits count all unique candidates entering those sets during the cycle, including subsequently parked or merged items. Parking does not refund research capacity. The validation limit applies portfolio-wide to selected/promoted validation work still open, including promotions from previous cycles. Record receiving-project completion before releasing that slot. Existing projects not promoted here do not silently consume this new-project cap, but their demands still matter in the mandate.

Stop at the first exhausted cap, useful evidence saturation, an adequate decision package, or a blocking dependency. End with a documented partial result if needed; never fill a quota with weak ideas.

## 3. Opportunity framing and tracks

Use this statement:

> For a specific beneficiary in a specific situation, a defined problem causes an observable consequence. Existing alternatives are identified. A possible improvement uses a stated mechanism and access route to produce measurable value. Value capture or intended benefit remains a hypothesis. The critical uncertainty is explicit.

Separate the problem from its solution. Consider a manual service, training, template, partnership, existing software, and a new product as alternatives where relevant. Do not assume software is the answer. Deduplicate on beneficiary/problem/context rather than similar titles; merge with `merged_into` and preserve both histories.

| Track | Essential questions |
|---|---|
| `commercial` | Who benefits, who buys, who can authorize payment, why now, how reached, what alternative spend, and what delivery/acquisition economics? |
| `strategic_creative` | Who is the audience/beneficiary, what outcome matters, how will it reach them, what production rhythm is sustainable, and what useful assets accumulate? |
| `internal_tool` | Which workflow/user, what baseline, what measurable benefit, what adoption path, what maintenance/integration cost, and is an existing tool sufficient? |

Cross-track selection is a narrative resource-allocation decision under the owner's objectives. Numerical scores from different profiles are not interchangeable.

## 4. Evidence and claims

Preserve the parent framework's definitions:

| Level | Meaning |
|---|---|
| E0 — UNKNOWN | No meaningful evidence |
| E1 — ANECDOTAL | Intuition, individual experience, opinion, isolated examples, or weak claims |
| E2 — INDICATIVE | Some supporting evidence exists, but not enough for material commitment |
| E3 — SUPPORTED | Multiple credible sources or meaningful direct evidence support the conclusion |
| E4 — VALIDATED | Evidence is sufficiently strong for the intended execution or decision context |

Apply levels to a specific claim and intended decision. Record population, jurisdiction, period, source independence, limitations, opposing evidence, review date, and rationale. An E4 claim is not absolute truth or a validated business. Two agents repeating one source are not two sources.

Sources record title, location, publisher/origin, published date or unknown, inspected date, status, independence group, observed finding, and limits. Preserve a short relevant excerpt or precise section/page locator; do not copy entire copyrighted publications. A search result is a lead until the underlying source is inspected. A failed or partial read must not become a full-read claim.

Distinguish evidence of a problem from evidence of reachable customers, payment, deliverability, repeatable acquisition, retention, and profitable economics. Advertised prices do not prove achievable sales; enthusiastic reactions do not prove payment; one pilot does not prove repeatability. Synthetic interviews, personas, and simulations can support preparation claims only. They cannot support market evidence levels.

Record both supporting and opposing source IDs. A source may qualify or challenge one claim while supporting another. Mark conflicting claims disputed; do not average away disagreement. Recheck volatile facts and decision-critical sources when their date or scope no longer fits. If a review date passes, treat the claim as due for review rather than silently keeping it current.

## 5. Hard filters

Default mandatory filters are `mandate_fit`, `time_capacity`, `resource_exposure`, `access_and_delivery`, and `legal_privacy_conflict`. Tailor them to the actual mandate and next contemplated commitment, retaining stronger existing constraints. Each screening record names the candidate, constraint, pass/fail/unknown outcome, rationale, evidence or authority basis, and scope.

- **Pass:** Sufficient basis for the specific next commitment; not a blanket lifetime clearance.
- **Fail:** The proposed commitment cannot proceed under the current mandate. Park/reject or propose a narrower alternative and rescreen.
- **Unknown:** Bounded investigation may resolve it. It prevents a commitment that relies on that constraint being satisfied.

Selection/promotion requires each required filter to pass for the approved stage. An unknown launch budget need not block an explicitly bounded internal DEFINE activity whose required resources are confirmed; state the narrower screening scope. Never label a launch constraint passed merely because research is inexpensive.

## 6. Comparison without false precision

The profiles below are proposed defaults, not confirmed owner preferences or empirical weights. Use a different explicit profile when the decision needs it; the optional checker recognizes only these three profiles. Score 1 (weak), 2 (limited), 3 (plausible), 4 (strong), 5 (exceptional) against the defined criterion and current comparison set. Explain each rating and cite relevant claim IDs. Evidence strength remains separate from attractiveness.

| Criterion ID | Commercial | Strategic / creative | Internal tool |
|---|---:|---:|---:|
| `problem_value` — importance of problem or intended outcome | 20 | 20 | 25 |
| `access_adoption` — customer/audience access or adoption | 15 | 15 | 15 |
| `value_efficiency` — economics or benefit for total effort | 15 | 10 | 15 |
| `capability_advantage` — relevant available advantage | 15 | 10 | 10 |
| `delivery_feasibility` — achievable delivery/production/maintenance | 10 | 15 | 15 |
| `learning_speed` — cost and time to useful evidence | 10 | 10 | 10 |
| `commitment_fit` — compatibility with current commitments | 10 | 10 | 5 |
| `compounding_value` — reusable assets and continuing value | 5 | 10 | 5 |
| Total | 100 | 100 | 100 |

Use `low: unknown` and `high: unknown` for an unsupported rating. Do not substitute zero, 3, or a speculative favorable bound. An evidenced range may express uncertainty, with a rationale for both ends. For known criteria K, calculate the **partial contribution interval** as `sum(weight * rating / 5)` and the **coverage** as `sum(weights in K)%`. Do not renormalize incomplete coverage or call that subtotal a complete score. If all criteria are known, the total interval is on a 20–100 scale. No machine-generated winner is required.

Run a sensitivity pass: adverse but plausible assumptions for the leading candidate, a credible alternative weighting, and the strongest alternative/no-commitment case. Record which claim changes the preference, overlap/rank reversals, and the next useful test. When uncertainty dominates, recommend resolving it rather than fine-tuning scores. An attractive but poorly evidenced option should remain visibly different from an adequately supported next commitment.

## 7. Economics, outcome models, and next tests

For commercial work include price range and basis, plausible volume/access constraints, acquisition effort, delivery effort, quality review, administration, support, software/model costs, maintenance, refunds, working capital, and cash timing. Distinguish observed amounts from assumptions. Model downside and break-even without claiming a forecast. Unknown critical costs remain a reason to investigate.

For creative/strategic work specify audience outcome, reach mechanism, production cadence, distribution effort, sustainability, and reusable assets. For tools specify current workflow time/error rate, realistic usage, improvement mechanism, adoption friction, build cost, and continuing maintenance. Compare with an existing solution and not building.

Each test proposal identifies the hypothesis, why it can change the decision, participants/inputs, measurement, predeclared success/failure/inconclusive thresholds, resources, privacy/data needs, stop conditions, and authority required. Set thresholds before data collection; preserve them if results disappoint. No universal number of interviews validates demand. A simulation tests preparation or mechanics, not customer behavior.

## 8. Candidate lifecycle and records

Candidate statuses: `framed`, `screened`, `investigating`, `compared`, `recommended`, `selected`, `promoted`, `parked`, `rejected`, `merged`. Progress only after the relevant checks, preserving a dated transition note. A later state is not a stronger evidence level. Promoted means accepted into execution, not launched or viable.

Screened through recommended records require screening of all mandatory constraints. Unknowns may remain visible; failures block advancement. Selected/promoted candidates require passing filters scoped to that approved stage and an approved selection decision. Park/reject with a reason and reopening trigger. Merged records link to a surviving ID. Resumption does not reopen an item without its trigger or an explicit owner decision.

The single workspace contains a prose conversation checkpoint, idea board and journal, plus flat YAML records in `discovery` code fences when formal research/decisions need them. Structured IDs use stable kinds: `CYC`, `SRC`, `SIG`, `OPP`, `CLM`, `SCR`, `ASM`, `EXP`, `DEC`, `HND`. Prose SEED IDs are not an added schema kind; when formalized, they point to the candidate rather than duplicate its current definition. Store structured references as scalar lists. A source supplies provenance; a claim supplies interpretation and evidence level. Candidate status, decision authority, and execution receipt each have one authoritative location.

The template gallery provides all record shapes. These structured blocks make links, limits, and selected state requirements checkable without a database or plugin. The optional tool reads the workspace only; splitting authoritative blocks into multiple files is a future schema change, not something the checker silently supports.

## 9. Decision and execution handover

Every material recommendation includes: current mandate and gaps; a small shortlist or no-commitment outcome; comparable criteria and sensitivity; source-supported findings and counterevidence; critical uncertainty; existing-project/no-new-work alternative; smallest next test; downside and resource envelope; and exact decision requested.

An approved selection decision records the owner, date, instruction/evidence reference, candidate, target stage, objective, scope, exclusions, resources, conditions, and expiry/review trigger. Reuse valid authority; do not copy a generic template's example approval.

The handover packet carries the approved decision, source/claim IDs, remaining hypotheses, risks, success/failure criteria, first Task, next gate, and proposed receiving state location. The first activity identifies its purpose, inputs, predecessors, required authority, expected output, completion check, and stop condition. Use the receiving EAGOS P0/P1/P2 profile appropriate to that activity's consequence.

1. Prepare a draft/ready-for-review packet. Selection does not itself create acceptance.
2. Under applicable setup authority, the receiving project inventories its records, checks the packet and permissions, and assesses its own activation.
3. Record transferred state and any receiver questions. Do not report acceptance from a sent/available packet.
4. Record actual receiver acknowledgment, date, and evidence. Conditional acceptance names conditions and permitted work. Only now may the candidate become promoted.
5. Link to the receiving project's authoritative state and stop duplicating it in discovery. Keep portfolio validation-slot status current through verified receipt/completion references.

If the packet is rejected, stale, or incomplete, preserve it and revise within authority. A historical approval cannot authorize a changed candidate, stage, or resource envelope. The discovery checker cannot verify external receipt, approval identity, actual source truth, legal sufficiency, or project activation.

## 10. Adaptation and maintenance

This extension adds discovery-specific records and checks; EAGOS core authority and evidence rules continue to apply. Use plain Markdown, flat YAML, relative links, stable IDs, and numbered filenames. Keep personal portfolios separate from reusable distribution files. Manual operation needs no plugins; the optional CLI uses Python 3.9+ and the standard library.

To adopt existing ideas, inventory and map their records; do not rewrite history or duplicate current execution state. To upgrade, compare the original manifest hashes and new generic templates, reconcile local edits, and preserve the old manifest and a change note. Core `drift` only supports execution starters. To remove the extension, stop cycles, preserve/export the workspace and handover references, and remove its navigation/tools; receiving projects retain their authority and evidence.

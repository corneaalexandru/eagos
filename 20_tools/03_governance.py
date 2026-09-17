"""Read-only EAGOS record diagnostics, not runtime policy enforcement."""

import datetime as dt
from decimal import Decimal, InvalidOperation


STATES = {
    "agent_role": {"proposed", "active", "suspended", "retired"},
    "delegation": {"draft", "active", "suspended", "expired", "revoked"},
    "runtime_deployment": {"documented", "configured", "tested", "active", "suspended", "retired"},
    "recurring_process": {"proposed", "active", "paused", "closed"},
    "task_attempt": {"planned", "running", "succeeded", "failed", "uncertain", "cancelled"},
}


def validate_records(records, add, today, placeholder):
    """Validate flat declarations only; the caller owns files and findings."""
    def known(value):
        return isinstance(value, str) and value.strip().lower() not in {"", "unknown", "tbd", "pending", "not_selected"} and not placeholder.search(value)

    def required(path, data, fields, code):
        for field in fields.split():
            value = data.get(field)
            list_field = field in {"authorization_evidence", "test_evidence", "enforcement_evidence", "outputs", "validation_evidence"}
            valid = isinstance(value, list) and value and all(known(v) for v in value) if list_field else known(value)
            if not valid:
                add("error", path, code, "Requires a resolved " + field)

    def strings(path, data, field):
        value = data.get(field)
        if not isinstance(value, list) or not value or not all(known(v) and "*" not in v for v in value):
            add("error", path, "delegation_scope", field + " requires a nonempty exact string allowlist; no wildcards")
            return set()
        return set(value)

    def budget(path, data):
        try:
            value = data.get("budget_limit")
            if isinstance(value, (bool, list, dict)):
                raise ValueError()
            result = Decimal(str(value))
            if not result.is_finite() or result < 0:
                raise ValueError()
            return result
        except (InvalidOperation, ValueError):
            add("error", path, "delegation_budget", "budget_limit must be a finite nonnegative decimal allocation")
            return None

    def date(path, data, field):
        try:
            value = dt.date.fromisoformat(str(data.get(field, "")))
            return value
        except ValueError:
            add("error", path, "delegation_date", field + " must be an ISO date")
            return None

    delegations = {}
    for record_id, (path, data) in records.items():
        kind, state = data.get("type"), data.get("status")
        if not isinstance(kind, str) or kind not in STATES:
            continue
        if not isinstance(state, str) or state not in STATES[kind]:
            add("error", path, "governance_state", "Unknown " + kind + " state: " + str(state))
        if kind == "delegation":
            delegations[record_id] = (path, data)
            if state == "active":
                required(path, data, "delegator delegate scope budget_unit approver authorization_evidence", "delegation_authority")
                if data.get("delegator") == data.get("delegate"):
                    add("error", path, "delegation_authority", "Self-delegation cannot create authority")
                if not isinstance(data.get("subdelegation"), str) or data.get("subdelegation") not in {"allowed", "forbidden"}:
                    add("error", path, "delegation_authority", "Declare subdelegation: allowed or forbidden")
                strings(path, data, "allowed_operations")
                strings(path, data, "allowed_targets")
                budget(path, data)
                start, end = date(path, data, "valid_from"), date(path, data, "expires_on")
                if start and end and (start > end or today < start or today > end):
                    add("error", path, "delegation_date", "Active delegation is outside its valid date interval")
        elif kind == "agent_role" and state == "active":
            required(path, data, "purpose accountable_to delegation", "role_contract")
        elif kind == "runtime_deployment":
            if state in {"configured", "tested", "active"}:
                required(path, data, "platform platform_version profile_reference configuration_fingerprint environment owner", "runtime_configuration")
            if state in {"tested", "active"}:
                required(path, data, "test_evidence limitations", "runtime_tests")
            if state == "active":
                required(path, data, "activation_decision enforcement_evidence operating_scope", "runtime_activation")
                ref = data.get("activation_decision")
                approval = records.get(ref, (None, {}))[1] if isinstance(ref, str) else {}
                if approval.get("type") != "decision" or approval.get("status") != "approved":
                    add("error", path, "runtime_activation", "Runtime needs a referenced approved activation decision")
                if data.get("required_control_gaps") != "none":
                    add("error", path, "runtime_activation", "Resolve required control gaps before declaring active")
        elif kind == "recurring_process" and state == "active":
            required(path, data, "owner trigger expected_output completion_check delegation recovery", "process_contract")
        elif kind == "task_attempt":
            ref = data.get("task_id")
            task = records.get(ref, (None, {}))[1] if isinstance(ref, str) else {}
            if task.get("type") not in {"task", "activity"}:
                add("error", path, "attempt_task", "Attempt must reference a Task or legacy activity")
            if state in {"running", "succeeded", "failed", "uncertain"}:
                required(path, data, "run_key executor", "attempt_identity")
            if state == "succeeded":
                required(path, data, "outputs validation_evidence", "attempt_completion")
            if state == "uncertain":
                required(path, data, "reconciliation_required", "attempt_recovery")

    allocations = {}
    for record_id, (path, child) in delegations.items():
        parent_id = child.get("parent_delegation")
        if not parent_id:
            continue
        if not isinstance(parent_id, str) or parent_id not in delegations:
            add("error", path, "delegation_parent", "Parent must reference a delegation record")
            continue
        visited, cursor = {record_id}, parent_id
        while cursor:
            if cursor in visited:
                add("error", path, "delegation_cycle", "Delegation ancestry contains a cycle")
                break
            visited.add(cursor)
            ancestor = delegations.get(cursor)
            if ancestor is None:
                break
            cursor = ancestor[1].get("parent_delegation")
            if not isinstance(cursor, str):
                break
        if child.get("status") != "active":
            continue
        parent_path, parent = delegations[parent_id]
        if parent.get("status") != "active" or parent.get("subdelegation") != "allowed":
            add("error", path, "delegation_parent", "Parent must be active and permit subdelegation")
        if child.get("delegator") != parent.get("delegate"):
            add("error", path, "delegation_parent", "Child delegator must be the parent's delegate")
        for field in ("allowed_operations", "allowed_targets"):
            if not strings(path, child, field).issubset(strings(parent_path, parent, field)):
                add("error", path, "delegation_expansion", "Child expands parent " + field)
        start, end = date(path, child, "valid_from"), date(path, child, "expires_on")
        pstart, pend = date(parent_path, parent, "valid_from"), date(parent_path, parent, "expires_on")
        if start and end and pstart and pend and (start < pstart or end > pend):
            add("error", path, "delegation_expansion", "Child validity exceeds parent interval")
        amount, maximum = budget(path, child), budget(parent_path, parent)
        if child.get("budget_unit") != parent.get("budget_unit"):
            add("error", path, "delegation_budget", "Child and parent allocation units must match")
        elif amount is not None and maximum is not None:
            allocations[parent_id] = allocations.get(parent_id, Decimal(0)) + amount
            if amount > maximum:
                add("error", path, "delegation_budget", "Child allocation exceeds parent")
    for parent_id, allocated in allocations.items():
        path, parent = delegations[parent_id]
        maximum = budget(path, parent)
        if maximum is not None and allocated > maximum:
            add("error", path, "delegation_budget", "Combined active child allocations exceed parent budget")

    run_keys = {}
    for record_id, (path, data) in records.items():
        refs = data.get("evidence_refs", [])
        if not isinstance(refs, list) or not all(isinstance(ref, str) for ref in refs):
            add("error", path, "evidence_reference", "evidence_refs must be a list of record IDs")
            refs = []
        for ref in refs:
            evidence = records.get(ref)
            if evidence is None:
                add("error", path, "evidence_reference", "Unknown supporting evidence ID: " + ref)
                continue
            if data.get("status") in {"ready", "in-progress", "active", "running"}:
                value = evidence[1]
                stale = value.get("status") in {"stale", "disputed", "contradicted", "refuted", "expired"}
                for field in ("review_on", "expires_on"):
                    raw = value.get(field)
                    if raw:
                        try:
                            stale = stale or dt.date.fromisoformat(str(raw)) < today
                        except ValueError:
                            stale = True
                if stale:
                    add("error", path, "evidence_impact", "Current work relies on stale/disputed evidence; revalidate " + ref)
        ref = data.get("delegation")
        if ref and (known(ref) or data.get("status") in {"ready", "in-progress", "active", "running"}):
            target = delegations.get(ref) if isinstance(ref, str) else None
            if target is None:
                add("error", path, "delegation_reference", "Unknown delegation reference")
            elif data.get("status") in {"ready", "in-progress", "active", "running"} and target[1].get("status") != "active":
                add("error", path, "delegation_readiness", "Current work requires an active delegation")
        if data.get("type") == "task_attempt" and data.get("status") in {"running", "succeeded", "uncertain"}:
            key = data.get("run_key")
            if known(key):
                if key in run_keys:
                    add("error", path, "attempt_duplicate", "Conflicting running/succeeded/uncertain attempts share run_key: " + key)
                run_keys[key] = record_id

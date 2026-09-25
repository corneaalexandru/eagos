"""Pure governance checks; organizations supply records, identities and effects."""

from datetime import datetime, timezone
import re

from . import GovernanceError, __version__
from .conventions import CONTRACT_VERSION, validate_identifier

AUTHORITY_KINDS = frozenset(("read", "write", "external", "approval"))


def _integer(value, label):
    if type(value) is not int or value < 0:
        raise GovernanceError(label + " must be a non-negative integer")
    return value


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _expiry(value):
    try:
        expiry = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if expiry.tzinfo is None:
            raise ValueError("timezone required")
        return expiry
    except (AttributeError, TypeError, ValueError) as exc:
        raise GovernanceError("Authority expiry requires an ISO timestamp with timezone") from exc


def _now(value):
    value = value or datetime.now(timezone.utc)
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise GovernanceError("Current time must have a timezone")
    return value


def _chain(roles, name):
    chain = []
    while name is not None:
        if name not in roles or name in chain:
            raise GovernanceError("Delegation must reference existing roles without cycles")
        chain.append(name)
        name = roles[name].get("parent_role")
    return chain


def _subtree(roles, name):
    return [candidate for candidate in roles if name in _chain(roles, candidate)]


def _total(counts, names, label):
    if not isinstance(counts, dict) or any(name not in counts for name in names):
        raise GovernanceError(label + " requires direct counts for every affected role")
    return sum(_integer(counts[name], label) for name in names)


def validate_policy(policy):
    """Validate explicit grants. A textual source is provenance, not authentication."""
    if not isinstance(policy, dict) or type(policy.get("schema_version")) is not int or policy["schema_version"] != CONTRACT_VERSION:
        raise GovernanceError("Unsupported policy contract")
    if not _text(policy.get("source")):
        raise GovernanceError("Policy requires its authority source")
    version = policy.get("framework_version", __version__)
    if policy.get("framework", "EAGOS") != "EAGOS" or not isinstance(version, str) or not re.fullmatch(r"5\.[01]\.\d+", version):
        raise GovernanceError("Policy requires a supported EAGOS 5.0 or 5.1 contract")
    directors, agents, roles = (policy.get(key) for key in ("directors", "agents", "roles"))
    if not isinstance(directors, list) or not directors or not isinstance(agents, dict) or not isinstance(roles, dict):
        raise GovernanceError("Policy requires directors, agents and roles")
    for director in directors:
        validate_identifier(director)
    for actor, role in agents.items():
        validate_identifier(actor)
        if not isinstance(role, str) or role not in roles:
            raise GovernanceError("Agent references an undefined role")
    for name, role in roles.items():
        validate_identifier(name)
        if not isinstance(role, dict) or type(role.get("enabled")) is not bool or type(role.get("allow_irreversible")) is not bool:
            raise GovernanceError("Role requires enabled and allow_irreversible flags")
        for key in ("capabilities", "workflows", "initiatives"):
            if not isinstance(role.get(key), list) or any(not _text(item) for item in role[key]):
                raise GovernanceError("Role requires an explicit " + key + " list")
            if key != "capabilities":
                for item in role[key]:
                    validate_identifier(item)
        _integer(role.get("max_risk"), "Role risk limit")
        _integer(role.get("budget_minor"), "Role budget")
        if "expires_at" not in role:
            raise GovernanceError("Role requires expires_at (null for no expiry)")
        if role["expires_at"] is not None:
            _expiry(role["expires_at"])
        if "authority_kinds" in role:
            kinds = role["authority_kinds"]
            if not isinstance(kinds, list) or any(not isinstance(kind, str) or kind not in AUTHORITY_KINDS for kind in kinds):
                raise GovernanceError("Unknown authority kind")
        if "max_attempts" in role:
            _integer(role["max_attempts"], "Attempt limit")
        if "parent_role" in role:
            validate_identifier(role["parent_role"])
    for name, child in roles.items():
        for parent_name in _chain(roles, name)[1:]:
            parent = roles[parent_name]
            for key in ("capabilities", "workflows", "initiatives", "authority_kinds"):
                if key in parent and key in child and not set(child[key]).issubset(parent[key]):
                    raise GovernanceError("Delegation expands " + key)
            for key in ("max_risk", "budget_minor", "max_attempts"):
                if key in parent and key in child and child[key] > parent[key]:
                    raise GovernanceError("Delegation expands " + key)
            if child["allow_irreversible"] and not parent["allow_irreversible"]:
                raise GovernanceError("Delegation expands irreversible authority")
            if parent["expires_at"] is not None and (child["expires_at"] is None or _expiry(child["expires_at"]) > _expiry(parent["expires_at"])):
                raise GovernanceError("Delegation outlives its parent grant")
    return policy


def authority_reasons(policy, task, actor, capability, reversible, used_minor, now=None,
                      *, authority_kind=None, usage_by_role=None, attempts_by_role=None):
    """Check grants. Role counters include prior descendants, siblings and failed attempts.

    Mapping values are direct per-role totals, not already aggregated. The host supplies
    durable counters; this check adds the proposed cost/attempt before authorizing it.
    """
    validate_policy(policy)
    if not isinstance(task, dict):
        raise GovernanceError("Task must be an object")
    for key in ("actor", "workflow", "initiative"):
        validate_identifier(task.get(key))
    validate_identifier(actor)
    _integer(task.get("risk"), "Task risk")
    _integer(task.get("cost_minor"), "Task cost")
    _integer(used_minor, "Used budget")
    if type(task.get("irreversible")) is not bool or type(reversible) is not bool or not _text(capability):
        raise GovernanceError("Task and adapter must declare reversibility and capability")
    now = _now(now)
    if authority_kind is not None and (not isinstance(authority_kind, str) or authority_kind not in AUTHORITY_KINDS):
        raise GovernanceError("Unknown authority kind")
    reasons = []
    if actor != task["actor"]:
        reasons.append("Only the assigned actor may execute this task")
    name = policy["agents"].get(actor)
    roles = policy["roles"]
    if name is None:
        return name, reasons + ["Actor has no enabled role"]
    chain = _chain(roles, name)
    for grant_name in chain:
        role = roles[grant_name]
        if not role["enabled"]:
            reasons.append("Role authority is disabled: " + grant_name)
        for key, value in (("capabilities", capability), ("workflows", task["workflow"]), ("initiatives", task["initiative"])):
            if value not in role[key]:
                reasons.append("Role does not authorize " + key + ": " + value)
        if "authority_kinds" in role and authority_kind not in role["authority_kinds"]:
            reasons.append("Role does not authorize the declared action kind")
        if task["risk"] > role["max_risk"]:
            reasons.append("Risk exceeds role limit")
        if (task["irreversible"] or not reversible) and not role["allow_irreversible"]:
            reasons.append("Irreversible action is outside role authority")
        if role["expires_at"] is not None and _expiry(role["expires_at"]) <= now:
            reasons.append("Role authority has expired: " + grant_name)
        subtree = _subtree(roles, grant_name)
        used = used_minor if len(chain) == len(subtree) == 1 and usage_by_role is None else _total(usage_by_role, subtree, "Budget accounting")
        if usage_by_role is not None and _total(usage_by_role, [name], "Budget accounting") != used_minor:
            raise GovernanceError("Direct role usage disagrees with used_minor")
        if used + task["cost_minor"] > role["budget_minor"]:
            reasons.append("Cumulative role budget would be exceeded")
        if "max_attempts" in role and _total(attempts_by_role, subtree, "Attempt accounting") + 1 > role["max_attempts"]:
            reasons.append("Cumulative attempt limit would be exceeded")
    return name, reasons


def validate_decision(decision, policy, task_hash, actor, now=None):
    """Validate approval scope. Hosts must also verify provenance and record integrity."""
    validate_policy(policy)
    if not isinstance(task_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", task_hash):
        raise GovernanceError("Decision scope requires an exact SHA-256 task hash")
    if not isinstance(decision, dict):
        return ["A Director decision record is required"]
    reasons = []
    if decision.get("status") != "approved" or decision.get("task_hash") != task_hash:
        reasons.append("A current Director approval is required")
    if decision.get("director") not in policy["directors"] or decision.get("director") == actor:
        reasons.append("Decision signer is not a distinct, current Director")
    if any(not _text(decision.get(key)) for key in ("reason", "source")):
        reasons.append("Decision requires its reason and authority source")
    if decision.get("expires_at") is not None and _expiry(decision["expires_at"]) <= _now(now):
        reasons.append("Decision has expired")
    return reasons


def process_reasons(process, started_runs, active_runs, used_minor, next_cost_minor=0, now=None):
    """Narrow a recurring process; the task still requires its current role grant."""
    if not isinstance(process, dict):
        raise GovernanceError("Process must be an object")
    validate_identifier(process.get("id"))
    if process.get("status") not in ("active", "paused", "stopped"):
        raise GovernanceError("Process status must be active, paused or stopped")
    for value, label in ((started_runs, "Started runs"), (active_runs, "Active runs"),
                         (used_minor, "Process usage"), (next_cost_minor, "Proposed cost")):
        _integer(value, label)
    if active_runs > started_runs:
        raise GovernanceError("Active runs cannot exceed started runs")
    maximum = _integer(process.get("max_parallel", 1), "Parallel run limit")
    if maximum == 0:
        raise GovernanceError("Parallel run limit must be positive")
    reasons = [] if process["status"] == "active" else ["Process is " + process["status"]]
    if active_runs >= maximum:
        reasons.append("Process overlap limit would be exceeded")
    if "max_runs" in process and started_runs + 1 > _integer(process["max_runs"], "Run limit"):
        reasons.append("Cumulative process run limit would be exceeded")
    if "budget_minor" in process and used_minor + next_cost_minor > _integer(process["budget_minor"], "Process budget"):
        reasons.append("Cumulative process budget would be exceeded")
    if process.get("expires_at") is not None and _expiry(process["expires_at"]) <= _now(now):
        reasons.append("Process authority has expired")
    return reasons

"""Pure governance checks; organizations supply records, identities and effects."""

from datetime import datetime, timezone

from . import GovernanceError, __version__
from .conventions import CONTRACT_VERSION, validate_identifier


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


def validate_policy(policy):
    """Validate explicit grants. A textual source is provenance, not authentication."""
    if not isinstance(policy, dict) or type(policy.get("schema_version")) is not int or policy["schema_version"] != CONTRACT_VERSION:
        raise GovernanceError("Unsupported policy contract")
    if not _text(policy.get("source")):
        raise GovernanceError("Policy requires its authority source")
    if policy.get("framework", "EAGOS") != "EAGOS" or policy.get("framework_version", __version__) != __version__:
        raise GovernanceError("Policy framework metadata does not match this EAGOS version")
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
    return policy


def authority_reasons(policy, task, actor, capability, reversible, used_minor, now=None):
    """Check a current grant, including cumulative spent and reserved minor units."""
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
    now = now or datetime.now(timezone.utc)
    if not isinstance(now, datetime) or now.tzinfo is None:
        raise GovernanceError("Current time must have a timezone")
    reasons = []
    if actor != task["actor"]:
        reasons.append("Only the assigned actor may execute this task")
    name = policy["agents"].get(actor)
    role = policy["roles"].get(name)
    if role is None or not role["enabled"]:
        return name, reasons + ["Actor has no enabled role"]
    for key, value in (("capabilities", capability), ("workflows", task["workflow"]), ("initiatives", task["initiative"])):
        if value not in role[key]:
            reasons.append("Role does not authorize " + key + ": " + value)
    if task["risk"] > role["max_risk"]:
        reasons.append("Risk exceeds role limit")
    if (task["irreversible"] or not reversible) and not role["allow_irreversible"]:
        reasons.append("Irreversible action is outside role authority")
    if role["expires_at"] is not None and _expiry(role["expires_at"]) <= now:
        reasons.append("Role authority has expired")
    if used_minor + task["cost_minor"] > role["budget_minor"]:
        reasons.append("Cumulative role budget would be exceeded")
    return name, reasons


def validate_decision(decision, policy, task_hash, actor):
    """Validate approval scope. Hosts must also verify provenance and record integrity."""
    validate_policy(policy)
    if not isinstance(decision, dict):
        return ["A Director decision record is required"]
    reasons = []
    if decision.get("status") != "approved" or decision.get("task_hash") != task_hash:
        reasons.append("A current Director approval is required")
    if decision.get("director") not in policy["directors"] or decision.get("director") == actor:
        reasons.append("Decision signer is not a distinct, current Director")
    if any(not _text(decision.get(key)) for key in ("reason", "source")):
        reasons.append("Decision requires its reason and authority source")
    return reasons

"""Shared rules are deterministic; hosts remain responsible for real-world effects."""

import copy
from datetime import datetime, timezone
from pathlib import Path
import unittest

from eagos import GovernanceError, __version__
from eagos.conventions import CONTRACT_VERSION, PATHS, validate_identifier, validate_evidence_path, validate_evidence_text
from eagos.governance import authority_reasons, validate_decision, validate_policy


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.policy = {"schema_version": 1, "source": "Director decision d_1",
                       "directors": ["director"], "agents": {"agent": "builder"},
                       "roles": {"builder": {"enabled": True, "capabilities": ["local.write"],
                           "workflows": ["build"], "initiatives": ["foundation"], "max_risk": 1,
                           "budget_minor": 10, "allow_irreversible": False, "expires_at": None}}}
        self.task = {"actor": "agent", "workflow": "build", "initiative": "foundation",
                     "risk": 1, "cost_minor": 4, "irreversible": False}

    def check(self, used=0, **changes):
        return authority_reasons(self.policy, dict(self.task, **changes), "agent", "local.write", True, used)

    def test_valid_grant_and_cumulative_budget(self):
        self.assertEqual(self.check(used=6), ("builder", []))
        self.assertIn("budget", self.check(used=7)[1][0])

    def test_missing_and_malformed_policy_fail_closed(self):
        for field, value in (("source", ""), ("schema_version", True), ("directors", []),
                             ("agents", {"agent": []}), ("roles", {"builder": {}})):
            with self.subTest(field=field), self.assertRaises(GovernanceError):
                validate_policy(dict(self.policy, **{field: value}))
        with self.assertRaises(GovernanceError):
            validate_policy(None)

    def test_explicit_role_limits_and_boolean_cost(self):
        for field, value in (("enabled", 1), ("allow_irreversible", "false"), ("budget_minor", -1),
                             ("capabilities", "local.write"), ("expires_at", "2026-01-01")):
            policy = copy.deepcopy(self.policy)
            policy["roles"]["builder"][field] = value
            with self.subTest(field=field), self.assertRaises(GovernanceError):
                validate_policy(policy)
        with self.assertRaises(GovernanceError):
            self.check(cost_minor=True)

    def test_scopes_and_irreversibility(self):
        for field, value in (("workflow", "other"), ("initiative", "other"), ("risk", 2), ("irreversible", True), ("actor", "other")):
            with self.subTest(field=field):
                self.assertTrue(self.check(**{field: value})[1])
        self.assertTrue(authority_reasons(self.policy, self.task, "agent", "external.send", True, 0)[1])
        self.assertTrue(authority_reasons(self.policy, self.task, "agent", "local.write", False, 0)[1])
        self.policy["roles"]["builder"]["enabled"] = False
        self.assertTrue(self.check()[1])

    def test_expiry_uses_injected_aware_time(self):
        self.policy["roles"]["builder"]["expires_at"] = "2026-09-25T12:00:00Z"
        for hour, denied in ((11, False), (12, True)):
            reasons = authority_reasons(self.policy, self.task, "agent", "local.write", True, 0,
                                        datetime(2026, 9, 25, hour, tzinfo=timezone.utc))[1]
            self.assertEqual(bool(reasons), denied)
        with self.assertRaises(GovernanceError):
            authority_reasons(self.policy, self.task, "agent", "local.write", True, 0, datetime(2026, 9, 25))

    def test_decision_needs_exact_scope_and_distinct_director(self):
        decision = {"status": "approved", "task_hash": "a" * 64, "director": "director",
                    "reason": "Bounded work", "source": "Recorded Director approval"}
        self.assertEqual(validate_decision(decision, self.policy, "a" * 64, "agent"), [])
        for field, value in (("status", "pending"), ("task_hash", "b" * 64), ("director", "agent"),
                             ("reason", ""), ("source", "")):
            self.assertTrue(validate_decision(dict(decision, **{field: value}), self.policy, "a" * 64, "agent"))
        self.policy["directors"].append("agent")
        self.assertTrue(validate_decision(dict(decision, director="agent"), self.policy, "a" * 64, "agent"))
        self.assertTrue(self.check(risk=2)[1])  # An approval does not enlarge role authority.

    def test_version_and_layout_agree(self):
        self.assertEqual(CONTRACT_VERSION, 1)
        self.assertIn('version = "' + __version__ + '"', (Path(__file__).parents[1] / "pyproject.toml").read_text())
        self.assertEqual(PATHS["policy"], "00_governance/policy.md")
        self.assertEqual(PATHS["inputs"], PATHS["tasks"] + "/inputs")
        self.assertIs(validate_policy(dict(self.policy, framework="EAGOS", framework_version=__version__))["roles"], self.policy["roles"])
        with self.assertRaises(GovernanceError):
            validate_policy(dict(self.policy, framework_version="4.0.0"))

    def test_evidence_and_identifier_conventions(self):
        self.assertEqual(validate_identifier("foundation_task_1"), "foundation_task_1")
        self.assertEqual(validate_evidence_path("30_evidence/research.md"), "30_evidence/research.md")
        validate_evidence_text("# Research\n\nObservation with its source and limits.")
        for value in ("", "# Title\n\n## Empty section", "# Title\n\n---"):
            with self.assertRaises(GovernanceError):
                validate_evidence_text(value)
        for value in ("../escape.md", "/30_evidence/x.md", "30_evidence/../x.md", "30_evidence/x.json", "evidence/x.md", "30_evidence/research-note.md"):
            with self.assertRaises(GovernanceError):
                validate_evidence_path(value)
        with self.assertRaises(GovernanceError):
            validate_identifier("Not clean")
        with self.assertRaises(GovernanceError):
            validate_identifier("foundation-task")


if __name__ == "__main__":
    unittest.main()

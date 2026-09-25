"""Shared rules are deterministic; hosts remain responsible for real-world effects."""

import copy
from datetime import datetime, timezone
from pathlib import Path
import unittest

from eagos import GovernanceError, __version__
from eagos.conventions import CONTRACT_VERSION, PATHS, markdown_body, validate_identifier, validate_evidence_path, validate_evidence_text
from eagos.governance import authority_reasons, process_reasons, validate_decision, validate_policy


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

    def test_legacy_policy_retains_original_authority_version(self):
        self.policy.update(framework="EAGOS", framework_version="5.0.0")
        before = copy.deepcopy(self.policy)
        self.assertEqual(self.check(), ("builder", []))
        self.assertEqual(self.policy, before)

    def test_frontmatter_is_not_substantive_evidence(self):
        metadata = "---\ntitle: Research\ntype: evidence\nstatus: verified\n---\n"
        with self.assertRaises(GovernanceError):
            validate_evidence_text(metadata + "# Empty observation\n")
        validate_evidence_text(metadata + "# Observation\n\nSource reports an observed change.")
        self.assertEqual(markdown_body(metadata + "Body"), "Body")
        with self.assertRaises(GovernanceError):
            markdown_body("---\ntitle: Unclosed")

    def test_declared_authority_kinds_are_enforced(self):
        self.policy["roles"]["builder"]["authority_kinds"] = ["write"]
        self.assertTrue(self.check()[1])
        self.assertEqual(authority_reasons(self.policy, self.task, "agent", "local.write", True, 0,
                                          authority_kind="write")[1], [])
        self.assertTrue(authority_reasons(self.policy, self.task, "agent", "local.write", True, 0,
                                         authority_kind="external")[1])

    def delegate(self):
        roles = self.policy["roles"]
        roles["manager"] = copy.deepcopy(roles["builder"])
        roles["builder"].update(parent_role="manager", budget_minor=6)
        roles["sibling"] = copy.deepcopy(roles["builder"])
        return {"manager": 0, "builder": 1, "sibling": 0}

    def test_delegation_cannot_expand_or_cycle(self):
        self.delegate()
        valid = copy.deepcopy(self.policy)
        for key, value in (("capabilities", ["external.send"]), ("max_risk", 2),
                           ("budget_minor", 11), ("allow_irreversible", True), ("parent_role", "builder")):
            self.policy = copy.deepcopy(valid)
            self.policy["roles"]["builder"][key] = value
            with self.subTest(key=key), self.assertRaises(GovernanceError):
                validate_policy(self.policy)
        self.policy = valid
        self.policy["roles"]["manager"]["expires_at"] = "2026-09-25T12:00:00Z"
        with self.assertRaises(GovernanceError):
            validate_policy(self.policy)  # A child cannot claim no expiry beyond an expiring parent.

    def test_delegation_shares_ancestor_budget_and_revocation(self):
        usage = self.delegate()
        with self.assertRaises(GovernanceError):
            self.check(used=1)
        def evaluate():
            return authority_reasons(self.policy, self.task, "agent", "local.write", True, 1,
                                     usage_by_role=usage)[1]
        self.assertEqual(evaluate(), [])
        usage["sibling"] = 6
        self.assertTrue(any("budget" in reason for reason in evaluate()))
        usage["sibling"] = 0
        self.policy["roles"]["manager"]["enabled"] = False
        self.assertTrue(any("disabled" in reason for reason in evaluate()))
        self.policy["roles"]["manager"]["enabled"] = True
        for role in self.policy["roles"].values():
            role["expires_at"] = "2020-01-01T00:00:00Z"
        self.assertTrue(any("expired" in reason for reason in evaluate()))

    def test_attempt_limits_include_failed_and_sibling_attempts(self):
        self.policy["roles"]["builder"]["max_attempts"] = 2
        with self.assertRaises(GovernanceError):
            self.check()
        self.assertTrue(authority_reasons(self.policy, self.task, "agent", "local.write", True, 0,
                                         attempts_by_role={"builder": 2})[1])
        usage = self.delegate()
        self.policy["roles"]["manager"]["max_attempts"] = 3
        counts = {"manager": 0, "builder": 1, "sibling": 2}
        reasons = authority_reasons(self.policy, self.task, "agent", "local.write", True, 1,
                                    usage_by_role=usage, attempts_by_role=counts)[1]
        self.assertTrue(any("attempt limit" in reason for reason in reasons))

    def test_process_limits_are_cumulative_and_do_not_schedule(self):
        process = {"id": "weekly_review", "status": "active", "max_runs": 3, "budget_minor": 5}
        self.assertEqual(process_reasons(process, 1, 0, 2, 3), [])
        for started, active, used, cost in ((3, 0, 0, 0), (1, 1, 0, 0), (1, 0, 3, 3)):
            self.assertTrue(process_reasons(process, started, active, used, cost))
        self.assertTrue(process_reasons(dict(process, status="paused"), 0, 0, 0))
        self.assertTrue(process_reasons(dict(process, expires_at="2020-01-01T00:00:00Z"), 0, 0, 0))
        with self.assertRaises(GovernanceError):
            process_reasons(dict(process, max_parallel=0), 0, 0, 0)

    def test_decision_scope_and_optional_expiry(self):
        decision = {"status": "approved", "task_hash": "a" * 64, "director": "director",
                    "reason": "Bounded work", "source": "Recorded approval", "expires_at": "2020-01-01T00:00:00Z"}
        self.assertIn("Decision has expired", validate_decision(decision, self.policy, "a" * 64, "agent"))
        with self.assertRaises(GovernanceError):
            validate_decision(decision, self.policy, "", "agent")


if __name__ == "__main__":
    unittest.main()

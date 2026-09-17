"""EAGOS 4 governance diagnostics using synthetic records and no real authority."""
import datetime as dt
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("eagos_test_core", ROOT / "20_tools/00_eagos.py")
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
TODAY = dt.date(2026, 9, 16)


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "project"
        core.init_project(self.root, "DEMO", "Synthetic fixture", "Test owner", "P0", True)

    def note(self, filename, data):
        path = self.root / filename
        path.write_text("---\n" + "\n".join(k + ": " + json.dumps(v) for k, v in data.items()) + "\n---\n\nSynthetic test only.\n")
        return path

    def codes(self):
        return {f["code"] for f in core.check(self.root, today=TODAY)["findings"] if f["severity"] == "error"}

    def grant(self, **changes):
        data = dict(id="DEMO-DLG-0001", type="delegation", status="active", delegator="Test owner", delegate="DEMO-ROLE-0001", scope="Synthetic local work", allowed_operations=["read", "write"], allowed_targets=["fixture"], budget_limit="100", budget_unit="test_units", valid_from="2026-09-01", expires_on="2026-09-30", subdelegation="allowed", approver="Test owner", authorization_evidence=["Synthetic fixture approval"])
        data.update(changes)
        return data

    def child(self, **changes):
        return self.grant(id="DEMO-DLG-0002", delegator="DEMO-ROLE-0001", delegate="DEMO-ROLE-0002", parent_delegation="DEMO-DLG-0001", budget_limit="40", **changes)

    def test_task_and_legacy_activity_have_identical_completion_requirements(self):
        for kind in ("task", "activity"):
            self.note("00_item.md", dict(id="DEMO-ACT-0900", type=kind, status="complete"))
            self.assertIn("completion", self.codes())

    def test_task_gate_and_predecessor_readiness_remain_enforced(self):
        self.note("00_item.md", dict(id="DEMO-ACT-0900", type="task", status="ready", gate="DEMO-GAT-0999", predecessors=["DEMO-ACT-0999"]))
        self.assertTrue({"gate_readiness", "dependency"}.issubset(self.codes()))

    def test_active_delegation_needs_real_declared_fields(self):
        self.note("00_grant.md", self.grant(authorization_evidence=[], approver="{{APPROVER}}"))
        self.assertIn("delegation_authority", self.codes())

    def test_valid_bounded_delegation_is_structurally_accepted(self):
        self.note("00_grant.md", self.grant())
        self.note("01_child.md", self.child())
        self.assertEqual(self.codes(), set())
        self.assertEqual(core.properties((self.root / "README.md").read_text())[0]["activation_status"], "not_assessed")

    def test_child_cannot_expand_operations_targets_or_dates(self):
        self.note("00_grant.md", self.grant())
        for change in ({"allowed_operations": ["send"]}, {"allowed_targets": ["external"]}, {"expires_on": "2026-10-01"}, {"valid_from": "2026-08-01"}):
            with self.subTest(change=change):
                self.note("01_child.md", self.child(**change))
                self.assertIn("delegation_expansion", self.codes())

    def test_combined_allocations_cannot_reset_parent_limit(self):
        self.note("00_grant.md", self.grant())
        child = self.child(); child["budget_limit"] = "60"
        self.note("01_child.md", child)
        second = dict(child, id="DEMO-DLG-0003", delegate="DEMO-ROLE-0003")
        self.note("02_child.md", second)
        self.assertIn("delegation_budget", self.codes())

    def test_inactive_parent_and_forbidden_subdelegation_fail(self):
        self.note("01_child.md", self.child())
        for change in ({"status": "revoked"}, {"subdelegation": "forbidden"}):
            self.note("00_grant.md", self.grant(**change))
            self.assertIn("delegation_parent", self.codes())

    def test_expired_future_and_invalid_dates_fail(self):
        for change in ({"expires_on": "2026-09-15"}, {"valid_from": "2026-09-17"}, {"expires_on": "someday"}):
            self.note("00_grant.md", self.grant(**change))
            self.assertIn("delegation_date", self.codes())

    def test_self_delegation_and_wrong_child_issuer_fail(self):
        self.note("00_grant.md", self.grant(delegate="Test owner"))
        self.assertIn("delegation_authority", self.codes())
        self.note("00_grant.md", self.grant())
        child = self.child(); child["delegator"] = "Another agent"
        self.note("01_child.md", child)
        self.assertIn("delegation_parent", self.codes())

    def test_delegation_cycles_and_unknown_parent_fail(self):
        self.note("00_grant.md", self.grant(parent_delegation="DEMO-DLG-0002"))
        self.note("01_child.md", self.child())
        self.assertIn("delegation_cycle", self.codes())
        self.note("00_grant.md", self.grant(parent_delegation="MISSING"))
        self.assertIn("delegation_parent", self.codes())

    def test_nonfinite_negative_and_mismatched_budgets_fail(self):
        for value in ("NaN", "Infinity", "-1", [], "unknown"):
            self.note("00_grant.md", self.grant(budget_limit=value))
            self.assertIn("delegation_budget", self.codes())
        self.note("00_grant.md", self.grant())
        self.note("01_child.md", self.child(budget_unit="different_units"))
        self.assertIn("delegation_budget", self.codes())

    def test_malformed_records_and_scope_fail_without_crashing(self):
        for field in ("id", "type", "status"):
            self.note("00_grant.md", self.grant(**{field: ["invalid"]}))
            self.assertIn("record_scalar", self.codes())
        for change in ({"allowed_operations": "read"}, {"allowed_targets": ["*"]}, {"subdelegation": ["allowed"]}):
            self.note("00_grant.md", self.grant(**change))
            self.assertTrue(self.codes())

    def test_ready_task_with_revoked_authority_is_reported(self):
        self.note("00_grant.md", self.grant(status="revoked"))
        self.note("01_task.md", dict(id="DEMO-ACT-0900", type="task", status="ready", delegation="DEMO-DLG-0001"))
        self.assertIn("delegation_readiness", self.codes())

    def test_runtime_active_cannot_be_inferred_from_configuration(self):
        self.note("00_runtime.md", dict(id="DEMO-RUN-0001", type="runtime_deployment", status="active"))
        self.assertTrue({"runtime_configuration", "runtime_tests", "runtime_activation"}.issubset(self.codes()))

    def test_runtime_requires_approved_decision_and_resolved_required_gaps(self):
        self.note("00_decision.md", dict(id="DEMO-DEC-0001", type="decision", status="approved", approver="Test owner", authorization_evidence=["Synthetic approval"]))
        data = dict(id="DEMO-RUN-0001", type="runtime_deployment", status="active", platform="Synthetic", platform_version="test-1", profile_reference="test profile", configuration_fingerprint="synthetic hash", environment="temporary test", owner="Test owner", test_evidence=["synthetic test"], enforcement_evidence=["synthetic observation"], limitations="Synthetic only", activation_decision="DEMO-DEC-0001", operating_scope="temporary fixture", required_control_gaps="none")
        self.note("01_runtime.md", data)
        self.assertEqual(self.codes(), set())
        self.note("01_runtime.md", dict(data, required_control_gaps="metering missing"))
        self.assertIn("runtime_activation", self.codes())

    def test_attempt_cannot_complete_task_and_duplicate_uncertain_run_is_flagged(self):
        task = self.note("00_task.md", dict(id="DEMO-ACT-0900", type="task", status="in-progress"))
        before = task.read_bytes()
        attempt = dict(id="DEMO-ATT-0001", type="task_attempt", status="uncertain", task_id="DEMO-ACT-0900", run_key="one-effect", executor="Test agent", reconciliation_required="Check actual effect")
        self.note("01_attempt.md", attempt)
        self.note("02_attempt.md", dict(attempt, id="DEMO-ATT-0002", status="running"))
        self.assertIn("attempt_duplicate", self.codes())
        self.assertEqual(task.read_bytes(), before)

    def test_evidence_change_flags_dependent_work_without_rewriting_history(self):
        evidence = self.note("00_evidence.md", dict(id="DEMO-EVD-0900", type="evidence", status="disputed"))
        task = self.note("01_task.md", dict(id="DEMO-ACT-0900", type="task", status="ready", evidence_refs=["DEMO-EVD-0900"]))
        before = {p: p.read_bytes() for p in (evidence, task)}
        self.assertIn("evidence_impact", self.codes())
        self.assertEqual({p: p.read_bytes() for p in before}, before)

    def test_legacy_manifest_and_source_paths_remain_readable(self):
        manifest = self.root / core.MANIFEST
        data = json.loads(manifest.read_text())
        data["framework_version"] = "4.0.0"
        data["source_paths"] = {k: v.replace("10_eagos_project_starter/", "10_elaef_project_starter/") for k, v in data["source_paths"].items()}
        legacy = self.root / core.LEGACY_MANIFEST
        legacy.write_text(json.dumps(data)); manifest.unlink()
        before = legacy.read_bytes()
        result = core.drift(self.root, ROOT)
        self.assertFalse(any(f.get("upstream") == "removed" for f in result["files"]))
        self.assertEqual(legacy.read_bytes(), before)

    def test_new_and_legacy_cli_return_same_diagnostics(self):
        outputs = []
        for script in ("00_eagos.py", "00_elaef.py"):
            result = subprocess.run([sys.executable, str(ROOT / "20_tools" / script), "check", str(self.root), "--format", "json"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            outputs.append(json.loads(result.stdout))
        self.assertEqual(outputs[0], outputs[1])



if __name__ == "__main__":
    unittest.main()

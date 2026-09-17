"""Discovery integrity scenarios in temporary folders; no network or real approvals."""

import contextlib
import copy
import datetime as dt
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("discovery", PACKAGE / "20_tools/01_discovery.py")
ods = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ods)


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.area = Path(self.temporary.name).resolve()
        self.root = self.area / "portfolio"
        ods.init_portfolio(self.root, "DEMO", "Demo portfolio", "Test owner", True)
        self.base = (self.root / ods.WORKSPACE).read_text()
        templates, errors = ods.blocks((PACKAGE / "11_opportunity_discovery_starter/60_templates/00_discovery_records.md").read_text())
        self.assertEqual(errors, [])
        self.templates = {r["type"]: r for _, r in templates}
        self.records = []

    def add(self, record_type, **changes):
        record = copy.deepcopy(self.templates[record_type])
        record.update(changes)
        self.records.append(record)
        return record

    def check(self):
        text = self.base
        for record in self.records:
            text += "\n```discovery\n" + "".join(k + ": " + json.dumps(v) + "\n" for k, v in record.items()) + "```\n"
        (self.root / ods.WORKSPACE).write_text(text)
        return ods.check(self.root, dt.date(2026, 9, 12))

    def codes(self):
        return {f["code"] for f in self.check()["findings"] if f["severity"] == "error"}

    def framed(self):
        self.add("cycle")
        return self.add("candidate")

    def promotion(self):
        self.framed()
        cycle, candidate = self.records
        cycle.update(investigated_candidates=[candidate["id"]])
        candidate.update(status="promoted", selection_decision="DEMO-DEC-0001", handover_id="DEMO-HND-0001")
        for field in "beneficiary problem situation consequence alternatives mechanism access_route value_model critical_unknown".split():
            candidate[field] = "Explicit synthetic test scenario"
        for index, constraint in enumerate(("mandate_fit", "time_capacity", "resource_exposure", "access_and_delivery", "legal_privacy_conflict"), 1):
            self.add("screen", id="DEMO-SCR-" + str(index).zfill(4), constraint=constraint, result="pass", scope="DEFINE only", basis="Synthetic test authority")
        decision = self.add("decision", status="approved", outcome="select", candidate_ids=[candidate["id"]], date="2026-09-12", approver="Fixture owner", authorization_evidence=["Fixture instruction"], target_stage="DEFINE")
        for field in "objective scope exclusions resources conditions review_trigger".split():
            decision[field] = "Explicit fixture envelope"
        handover = self.add("handover", status="accepted", target_stage="DEFINE", receiver="Fixture receiver", accepted_on="2026-09-12", acceptance_evidence=["Fixture acknowledgment"])
        for field in "remaining_hypotheses risks success failure first_activity next_gate execution_state".split():
            handover[field] = "Explicit fixture packet"
        return candidate, decision, handover

    def test_empty_instantiated_portfolio_is_valid_and_has_no_approval(self):
        result = self.check()
        self.assertEqual(result["errors"], 0, result)
        self.assertEqual(result["records"], 0)
        self.assertIn("status: setup", self.base)
        self.assertIn("No owner research instruction", self.base)

    def test_preview_writes_nothing_and_existing_destination_is_preserved(self):
        new = self.area / "new"
        result = ods.init_portfolio(new, "DEMO", "Name", "Owner")
        self.assertEqual(result["action"], "preview")
        self.assertFalse(new.exists())
        before = (self.root / ods.WORKSPACE).read_bytes()
        with self.assertRaisesRegex(ValueError, "already exists"):
            ods.init_portfolio(self.root, "DEMO", "Name", "Owner", True)
        self.assertEqual((self.root / ods.WORKSPACE).read_bytes(), before)

    def test_interactive_starter_is_portable_and_requires_no_research_records(self):
        playbook = self.root / "04_interactive_discovery.md"
        self.assertTrue(playbook.is_file())
        self.assertIn("DEMO-SEED-0001", playbook.read_text())
        manifest = json.loads((self.root / ods.MANIFEST).read_text())
        self.assertEqual(manifest["extension_version"], ods.VERSION)
        self.assertEqual(manifest["extension"], "EAGOS-ODS")
        self.assertEqual(manifest["framework_version"], ods.core.VERSION)
        self.assertEqual(manifest["baseline_hashes"][playbook.name], ods.core.digest(playbook.read_bytes()))
        self.base += "\n## Idea notes\nDEMO-SEED-0001: Unresearched hypothesis; no formal candidate yet.\n"
        result = self.check()
        self.assertEqual(result["errors"], 0, result)
        self.assertEqual(result["records"], 0)

    def test_legacy_workspace_remains_readable_and_unknown_versions_fail(self):
        original = self.base
        self.add("cycle")
        for version in ("1.0.0", "1.1.0", "1.1.1", "1.2.0"):
            with self.subTest(version=version):
                self.base = original.replace('extension_version: "' + ods.VERSION + '"', 'extension_version: "' + version + '"')
                self.assertNotIn("schema", self.codes())
                before = (self.root / ods.WORKSPACE).read_bytes()
                ods.check(self.root, dt.date(2026, 9, 12))
                self.assertEqual((self.root / ods.WORKSPACE).read_bytes(), before)
        self.base = original.replace('extension: EAGOS-ODS', 'extension: ELAEF-ODS')
        self.assertNotIn('schema', self.codes())
        self.base = original.replace('extension: EAGOS-ODS\n', '')
        self.assertNotIn('schema', self.codes())
        self.base = original.replace('extension: EAGOS-ODS', 'extension: unrelated')
        self.assertIn('schema', self.codes())
        for field, current in [('extension', 'EAGOS-ODS'), ('extension_version', '"' + ods.VERSION + '"')]:
            self.base = original.replace(field + ': ' + current, field + ': ["invalid"]')
            self.assertIn('schema', self.codes())
        self.base = original.replace('extension_version: "' + ods.VERSION + '"', 'extension_version: "9.0.0"')
        self.assertIn("schema", self.codes())

    def test_symlinks_and_invalid_identity_are_rejected(self):
        alias = self.area / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            ods.init_portfolio(alias / "child", "DEMO", "Name", "Owner", True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            ods.check(alias)
        with self.assertRaises(ValueError):
            ods.init_portfolio(self.area / "bad", "../bad", "Name", "Owner", True)

    def test_identity_quotes_and_links_are_escaped(self):
        new = self.area / "new"
        ods.init_portfolio(new, "DEMO", 'A "quoted" [link](elsewhere)', "O'Owner", True)
        self.assertEqual(ods.check(new)["errors"], 0)

    def test_read_only_check_preserves_hashes(self):
        before = {p.name: ods.core.digest(p.read_bytes()) for p in self.root.iterdir() if p.is_file()}
        ods.check(self.root)
        after = {p.name: ods.core.digest(p.read_bytes()) for p in self.root.iterdir() if p.is_file()}
        self.assertEqual(before, after)

    def test_frame_can_be_an_unproven_hypothesis(self):
        self.framed()
        self.assertEqual(self.check()["errors"], 0)

    def test_duplicate_ids_and_dangling_sources_fail(self):
        self.framed()
        self.add("candidate")
        self.add("signal")
        self.assertTrue({"duplicate_id", "reference"}.issubset(self.codes()))

    def test_search_caps_and_negative_counts_fail(self):
        c = self.add("cycle", queries_used=13, sources_used=-1)
        self.assertTrue({"budget", "number"}.issubset(self.codes()))
        c.update(queries_used=12, sources_used=20, minutes_used=45)
        self.assertEqual(self.check()["errors"], 0)

    def test_parking_does_not_refund_candidate_capacity(self):
        self.add("cycle", candidate_limit=1)
        for i in (1, 2):
            self.add("candidate", id="DEMO-OPP-000" + str(i), status="parked", reason="Constraint", reopen_trigger="Owner changes constraint")
        self.assertIn("budget", self.codes())

    def test_unknown_ratings_stay_unknown_and_zero_is_invalid(self):
        self.framed()
        rating = self.add("assessment", claim_ids=[])
        self.assertEqual(self.check()["errors"], 0)
        rating.update(low=0, high=0)
        self.assertIn("rating", self.codes())
        rating.update(low=4, high=3)
        self.assertIn("rating", self.codes())
        rating.update(low="unknown", high=3)
        self.assertIn("rating", self.codes())

    def test_cross_track_and_cross_candidate_assessment_fail(self):
        self.framed()
        self.add("candidate", id="DEMO-OPP-0002")
        self.add("claim", candidate_id="DEMO-OPP-0002")
        self.add("assessment", profile="internal_tool")
        self.assertTrue({"profile", "claim_scope"}.issubset(self.codes()))

    def test_synthetic_or_snippet_sources_cannot_support_market_evidence(self):
        self.framed()
        source = self.add("source", kind="synthetic", title="Simulation", location="Fixture", origin="Fixture", inspected_on="2026-09-12", independence_group="Fixture", finding="Simulated reactions", locator="Fixture", limitations="Synthetic")
        claim = self.add("claim", evidence_level="E2", supporting_sources=[source["id"]])
        self.assertIn("evidence", self.codes())
        claim["context"] = "preparation"
        self.assertEqual(self.check()["errors"], 0)
        source["kind"] = "search_lead"
        self.assertIn("evidence", self.codes())

    def test_unavailable_source_cannot_support_claim(self):
        self.framed()
        source = self.add("source", status="unavailable", location="Fixture", origin="Fixture", independence_group="Fixture", limitations="Retrieval failed")
        self.add("claim", evidence_level="E1", supporting_sources=[source["id"]])
        self.assertIn("evidence", self.codes())

    def test_hard_filter_fail_or_unknown_prevents_selection(self):
        self.promotion()
        self.assertEqual(self.check()["errors"], 0, self.check())
        self.records[2]["result"] = "fail"
        self.assertIn("screening", self.codes())
        self.records[2]["result"] = "unknown"
        self.assertIn("screening", self.codes())

    def test_recommendation_does_not_supply_selection_authority(self):
        candidate, decision, handover = self.promotion()
        decision["status"] = "proposed"
        self.assertTrue({"selection", "handover"}.issubset(self.codes()))

    def test_transfer_is_not_acceptance_and_empty_acceptance_fails(self):
        candidate, decision, handover = self.promotion()
        handover["status"] = "transferred"
        self.assertIn("promotion", self.codes())
        handover.update(status="accepted", acceptance_evidence=[])
        self.assertIn("acceptance", self.codes())

    def test_handover_must_match_selected_stage_and_candidate(self):
        candidate, decision, handover = self.promotion()
        handover["target_stage"] = "BUILD"
        self.assertIn("handover", self.codes())
        decision["target_stage"] = "BUILD"
        self.assertIn("vocabulary", self.codes())

    def test_conditional_acceptance_and_expired_authority_fail_closed(self):
        candidate, decision, handover = self.promotion()
        handover["status"] = "accepted_with_conditions"
        decision["expires_on"] = "2026-09-11"
        self.assertTrue({"acceptance", "expired_authority"}.issubset(self.codes()))

    def test_validation_cap_survives_completed_cycles(self):
        candidate, decision, handover = self.promotion()
        decision["target_stage"] = handover["target_stage"] = "VALIDATE"
        candidate["validation_slot"] = "open"
        self.records[0].update(status="complete", authority="Fixture instruction", started_on="2026-09-12", stop_reason="Handover", result="Fixture handover")
        other = self.add("candidate", id="DEMO-OPP-0002", validation_slot="open")
        self.assertIn("budget", self.codes())
        other.update(validation_slot="closed", validation_completion_evidence="Fixture completion")
        self.assertNotIn("budget", self.codes())

    def test_validation_selection_requires_slot_tracking(self):
        candidate, decision, handover = self.promotion()
        decision["target_stage"] = handover["target_stage"] = "VALIDATE"
        self.assertIn("validation_slot", self.codes())

    def test_investigations_are_cumulative_and_membership_is_checked(self):
        candidate, _, _ = self.promotion()
        self.records[0]["investigated_candidates"] = []
        self.assertIn("investigation_tracking", self.codes())
        self.records[0]["investigated_candidates"] = [candidate["id"], candidate["id"]]
        self.assertIn("duplicate_reference", self.codes())

    def test_parked_and_merged_records_preserve_continuity(self):
        c = self.framed()
        c["status"] = "parked"
        self.assertIn("incomplete", self.codes())
        c.update(status="merged", merged_into=c["id"])
        self.assertIn("merge_cycle", self.codes())

    def test_future_acceptance_and_malformed_date_fail(self):
        _, decision, handover = self.promotion()
        handover["accepted_on"] = "2027-01-01"
        decision["date"] = "not-a-date"
        self.assertTrue({"future_record", "date"}.issubset(self.codes()))

    def test_nested_examples_are_not_live_records_and_unclosed_fence_fails(self):
        self.base += '\n````markdown\n```discovery\nid: BAD\n```\n````\n'
        self.assertEqual(self.check()["records"], 0)
        self.base += '\n```discovery\nid: BAD\n'
        self.assertIn("fence", self.codes())

    def test_missing_validation_cap_and_bad_schema_fail(self):
        self.base = self.base.replace("validation_limit: 1", "validation_limit: unknown").replace('schema_version: "1"', 'schema_version: "9"')
        self.assertTrue({"number", "schema"}.issubset(self.codes()))

    def test_cli_errors_are_nonzero_and_json_is_parseable(self):
        self.framed()
        self.records[0]["queries_used"] = 13
        self.check()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            result = ods.main(["check", str(self.root), "--format", "json"])
        self.assertEqual(result, 1)
        self.assertGreater(json.loads(out.getvalue())["errors"], 0)


if __name__ == "__main__":
    unittest.main()

"""Behavior tests use disposable projects; no live project data or network."""

import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import re
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("elaef", PACKAGE / "20_tools/00_elaef.py")
elaef = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(elaef)


class ToolkitTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.area = Path(self.temporary.name).resolve()
        self.root = self.area / "project"

    def initialize(self, profile="P0", apply=True, **values):
        return elaef.init_project(self.root, values.get("code", "DEMO"), values.get("name", "Demo project"), values.get("owner", "Project owner"), profile, apply, PACKAGE)

    def note(self, name, properties=None, body=""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        frontmatter = "---\n" + "".join(key + ": " + json.dumps(value) + "\n" for key, value in (properties or {}).items()) + "---\n" if properties else ""
        path.write_text(frontmatter + body, encoding="utf-8")
        return path

    def codes(self, mode="setup"):
        return {f["code"] for f in elaef.check(self.root, mode)["findings"]}

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): elaef.digest(p.read_bytes()) for p in self.root.rglob("*") if p.is_file() and not p.is_symlink()}

    def test_preview_is_read_only(self):
        result = self.initialize(apply=False)
        self.assertEqual(result["action"], "preview")
        self.assertFalse(self.root.exists())

    def test_p0_is_small_and_not_activated(self):
        self.initialize()
        self.assertEqual(set(self.snapshot()), {"README.md", "AGENTS.md", "01_operating_guide.md", ".gitignore", elaef.MANIFEST})
        hub, _, _ = elaef.properties((self.root / "README.md").read_text())
        self.assertEqual(hub["activation_status"], "not_assessed")
        self.assertEqual(hub["conformance_profile"], "P0")
        result = elaef.check(self.root, "setup")
        self.assertEqual(result["errors"], 0, result)
        self.assertGreater(result["warnings"], 0)

    def test_full_profiles_leave_approvals_unresolved(self):
        for profile in ("P1", "P2"):
            with self.subTest(profile=profile):
                self.root = self.area / profile
                self.initialize(profile)
                self.assertTrue((self.root / "00_control/02_project_activation.md").is_file())
                self.assertIn("{{APPROVAL_OWNER}}", (self.root / "00_control/02_project_activation.md").read_text())
                result = elaef.check(self.root, "setup")
                self.assertEqual(result["errors"], 0, result)

    def test_existing_destination_is_never_overwritten(self):
        self.initialize()
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.initialize()
        self.assertEqual(before, self.snapshot())

    def test_symlink_destination_is_rejected(self):
        real = self.area / "real"
        real.mkdir()
        alias = self.area / "alias"
        alias.symlink_to(real, target_is_directory=True)
        self.root = alias / "project"
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.initialize()
        self.assertEqual(list(real.iterdir()), [])

    def test_bad_identity_is_rejected(self):
        for values in ({"code": "../bad"}, {"owner": "one\ntwo"}, {"name": "{{UNKNOWN}}"}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                self.initialize(**values)

    def test_quotes_and_markdown_in_identity_are_safe(self):
        self.initialize(name='A "quoted" [project] | café', owner="D'Owner")
        data, _, issues = elaef.properties((self.root / "README.md").read_text())
        self.assertEqual(issues, [])
        self.assertEqual(data["title"], 'A "quoted" [project] | café')
        self.assertEqual(data["owner"], "D'Owner")

    def test_active_mode_rejects_skeleton(self):
        self.initialize()
        self.assertTrue({"placeholder", "activation"}.issubset(self.codes("active")))

    def test_template_mode_passes_distribution(self):
        result = elaef.check(PACKAGE / "10_elaef_project_starter", "template")
        self.assertEqual(result["errors"], 0, result)
        self.assertEqual(result["warnings"], 0, result)

    def test_missing_and_ambiguous_links(self):
        self.initialize()
        self.note("10_notes/00_note.md", body="[missing](missing.md)\n[[01_shared]]\n")
        self.note("20_a/01_shared.md", body="# Shared\n")
        self.note("30_b/01_shared.md", body="# Shared\n")
        messages = [f["message"] for f in elaef.check(self.root)["findings"] if f["code"] == "link"]
        self.assertTrue(any("Missing" in m for m in messages))
        self.assertTrue(any("Ambiguous" in m for m in messages))

    def test_relative_links_and_headings_work_in_nested_vault(self):
        self.root = self.area / "vault" / "projects" / "alpha"
        self.root.parent.mkdir(parents=True)
        self.initialize()
        self.note("10_notes/00_note.md", body="## Result\n[hub](../README.md#state)\n[here](#result)\n")
        self.assertNotIn("link", self.codes())

    def test_broken_heading_is_found(self):
        self.initialize()
        self.note("00_link.md", body="[bad](README.md#absent)\n")
        self.assertIn("link", self.codes())

    def test_code_examples_are_not_live_links(self):
        self.initialize()
        self.note("00_example.md", body="`[sample](missing.md)`\n```md\n[[missing]]\n```\n")
        self.assertNotIn("link", self.codes())

    def test_unclosed_code_and_duplicate_properties_fail(self):
        self.initialize()
        self.note("00_bad.md", body="---\nid: A\nid: B\n---\n```\nopen\n")
        self.assertTrue({"fence", "frontmatter_subset"}.issubset(self.codes()))

    def test_nested_yaml_is_not_silently_validated(self):
        self.initialize()
        self.note("00_nested.md", body="---\npolicy:\n  owner: Person\n---\n")
        self.assertIn("frontmatter_subset", self.codes())

    def test_duplicate_record_ids_fail(self):
        self.initialize()
        self.note("10_notes/00_one.md", {"id": "DEMO-EVD-0002"})
        self.note("10_notes/01_two.md", {"id": "DEMO-EVD-0002"})
        self.assertIn("duplicate_id", self.codes())

    def test_duplicate_inline_definitions_fail(self):
        self.initialize()
        self.note("00_records.md", body="### DEMO-ACT-0099 — First\n\n### DEMO-ACT-0099 — Duplicate\n")
        self.assertIn("duplicate_id", self.codes())

    def test_cycles_and_missing_dependencies_fail(self):
        self.initialize()
        self.note("20_execution/0001_one.md", {"id": "DEMO-ACT-0010", "type": "activity", "status": "proposed", "predecessors": ["DEMO-ACT-0011", "DEMO-ACT-9999"]})
        self.note("20_execution/0002_two.md", {"id": "DEMO-ACT-0011", "type": "activity", "status": "proposed", "predecessors": ["DEMO-ACT-0010"]})
        self.assertTrue({"dependency", "dependency_cycle"}.issubset(self.codes()))

    def test_ready_activity_requires_complete_predecessor_and_passed_gate(self):
        self.initialize()
        self.note("00_previous.md", {"id": "DEMO-ACT-0008", "type": "activity", "status": "blocked"})
        self.note("01_current.md", {"id": "DEMO-ACT-0009", "type": "activity", "status": "ready", "predecessors": ["DEMO-ACT-0008"], "gate": "DEMO-GAT-PILOT"})
        self.note("02_gate.md", {"id": "DEMO-GAT-PILOT", "type": "gate", "status": "not_assessed"})
        self.assertTrue({"readiness", "gate_readiness"}.issubset(self.codes()))

    def test_completed_activity_needs_output_and_validation(self):
        self.initialize()
        self.note("00_activity.md", {"id": "DEMO-ACT-0010", "type": "activity", "status": "complete"})
        self.assertIn("completion", self.codes())
        self.note("00_activity.md", {"id": "DEMO-ACT-0010", "type": "activity", "status": "complete", "outputs": ["missing.md"], "validation_evidence": ["Reviewed locally"]})
        self.assertIn("output_link", self.codes())

    def test_gate_approval_and_acceptance_require_evidence(self):
        self.initialize()
        self.note("00_gate.md", {"id": "DEMO-GAT-0001", "type": "gate", "status": "conditionally-passed"})
        self.note("01_handover.md", {"id": "DEMO-HND-0001", "type": "handover", "status": "accepted"})
        self.assertTrue({"approval", "conditions", "acceptance"}.issubset(self.codes()))

    def test_elapsed_gate_and_evidence_dates_are_reported(self):
        self.initialize()
        self.note("00_gate.md", {"id": "DEMO-GAT-0001", "type": "gate", "status": "passed", "approver": "Owner", "authorization_evidence": ["Approved 2020-01-01"], "expires_on": "2020-01-02"})
        self.note("01_evidence.md", {"id": "DEMO-EVD-0002", "type": "evidence", "status": "current", "review_on": "2020-01-02"})
        findings = [f for f in elaef.check(self.root, today=dt.date(2026, 9, 8))["findings"] if f["code"] == "stale"]
        self.assertEqual({f["severity"] for f in findings}, {"error", "warning"})

    def test_initial_activation_spellings_are_equivalent_without_rewriting(self):
        self.initialize("P1")
        hub = self.root / "README.md"
        gate = self.root / "00_control/02_project_activation.md"
        for hub_state, gate_state in (("not_assessed", "not-assessed"), ("not-assessed", "not_assessed")):
            with self.subTest(hub=hub_state, gate=gate_state):
                hub.write_text(re.sub(r"activation_status: [^\n]+", "activation_status: " + hub_state, hub.read_text()))
                gate.write_text(re.sub(r"status: [^\n]+", "status: " + gate_state, gate.read_text(), count=1))
                before = self.snapshot()
                self.assertNotIn("activation_conflict", self.codes())
                self.assertIn("activation", self.codes("active"))
                self.assertEqual(before, self.snapshot())

    def test_conflicting_activation_states_fail(self):
        self.initialize("P1")
        path = self.root / "README.md"
        path.write_text(path.read_text().replace("activation_status: not_assessed", "activation_status: passed"))
        self.assertIn("activation_conflict", self.codes())

    def test_raw_private_and_symlink_content_not_read(self):
        self.initialize()
        self.note("80_private/secret.md", body="---\ninvalid\n")
        self.note("30_evidence/10_raw/original.md", body="[[missing]]\n```")
        (self.root / "00_linked.md").symlink_to(self.root / "80_private/secret.md")
        self.assertFalse({"frontmatter_subset", "link", "fence"} & self.codes())

    def test_diagnostics_do_not_modify_files(self):
        self.initialize()
        before = self.snapshot()
        elaef.check(self.root)
        elaef.drift(self.root, PACKAGE)
        list(elaef.files(self.root))
        self.assertEqual(before, self.snapshot())

    def test_drift_tracks_edits_missing_and_new_files(self):
        self.initialize()
        path = self.root / "README.md"
        path.write_text(path.read_text() + "\nLocal project addition\n")
        (self.root / "AGENTS.md").unlink()
        self.note("00_new.md", body="Project-specific note\n")
        result = elaef.drift(self.root, PACKAGE)
        states = {f["path"]: f["local"] for f in result["files"]}
        self.assertEqual(states["README.md"], "locally_modified")
        self.assertEqual(states["AGENTS.md"], "missing")
        self.assertIn("00_new.md", result["new_local_files"])

    def test_drift_detects_upstream_local_conflict_without_merging(self):
        self.initialize()
        manifest_path = self.root / elaef.MANIFEST
        manifest = json.loads(manifest_path.read_text())
        manifest["source_hashes"]["README.md"] = "0" * 64
        manifest_path.write_text(json.dumps(manifest))
        path = self.root / "README.md"
        path.write_text(path.read_text() + "\nLocal addition\n")
        result = elaef.drift(self.root, PACKAGE)
        self.assertEqual(next(f for f in result["files"] if f["path"] == "README.md")["review"], "manual_merge")

    def test_manifest_path_traversal_is_rejected(self):
        self.initialize()
        path = self.root / elaef.MANIFEST
        manifest = json.loads(path.read_text())
        manifest["baseline_hashes"]["../outside.md"] = "0" * 64
        path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "relative"):
            elaef.drift(self.root)

    def test_current_framework_version_and_sections(self):
        selected = os.environ.get("ELAEF_SPEC_PATH") or os.environ.get("EAGOS_SPEC_PATH")
        master = Path(selected) if selected else PACKAGE / "00_evidence_led_agent_execution_framework.md"
        self.assertTrue(master.is_file(), "Provide the current specification at package root or via ELAEF_SPEC_PATH; the maintenance reference map is also supported")
        content = master.read_text()
        data, _, issues = elaef.properties(content)
        self.assertEqual(issues, [])
        self.assertEqual(data.get("version"), elaef.VERSION)
        self.assertEqual(data.get("spec_version"), elaef.VERSION)
        numbers = [int(n) for n in re.findall(r"^## (\d+)\. ", content, re.M)]
        self.assertEqual(numbers, list(range(1, 25)))


if __name__ == "__main__":
    unittest.main()

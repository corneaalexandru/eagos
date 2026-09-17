"""End-to-end offline workflows. Synthetic authority, real temporary artifacts.

These tests exercise records and CLI processes, not model behavior or a runtime.
"""
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


core = load("workflow_core", "20_tools/00_eagos.py")
discovery_fixtures = load("workflow_discovery", "30_tests/02_test_discovery.py")


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.area = Path(self.temp.name).resolve()
        self.project = self.area / "project"
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

    def cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(ROOT / "20_tools/00_eagos.py"), *map(str, args)],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def initialize(self):
        args = ("init", self.project, "--code", "DEMO", "--name", "Synthetic workflow",
                "--owner", "Fixture owner", "--profile", "P0")
        self.cli(*args)
        self.assertFalse(self.project.exists())
        self.cli(*args, "--apply")
        self.assertEqual(self.cli("check", self.project, "--format", "json")["errors"], 0)
        self.cli("check", self.project, "--mode", "active", "--format", "json", expected=1)

    def note(self, name, **data):
        path = self.project / name
        path.write_text("---\n" + "".join(k + ": " + json.dumps(v) + "\n" for k, v in data.items()) +
                        "---\n\nSynthetic fixture only; no real authority.\n")
        return path

    def check(self, expected=0):
        return self.cli("check", self.project, "--format", "json", expected=expected)

    def test_reversible_build_resume_move_and_output_loss(self):
        self.initialize()
        manifest = (self.project / core.MANIFEST).read_bytes()
        source = self.project / "02_input.json"
        source.write_text(json.dumps(["gamma", "alpha", "beta"]))
        task = dict(id="DEMO-ACT-0001", type="task", status="ready", owner="Fixture owner")
        self.note("03_task.md", **task)
        self.check()
        output = self.project / "04_result.json"
        output.write_text(json.dumps(sorted(json.loads(source.read_text()))))
        self.assertEqual(json.loads(output.read_text()), ["alpha", "beta", "gamma"])
        task.update(status="complete", outputs=[output.name], validation_evidence=["Exact ordered-list assertion passed"])
        self.note("03_task.md", **task)
        receipt = self.project / "05_checkpoint.json"
        receipt.write_text(json.dumps({"task_id": task["id"], "next": "review result", "output": output.name,
                                       "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}))
        self.check()
        # Fresh process and relocated workspace; no in-memory state survives.
        moved = self.area / "resumed"
        shutil.move(str(self.project), moved)
        self.project = moved
        self.check()
        state = json.loads((moved / receipt.name).read_text())
        self.assertEqual(hashlib.sha256((moved / state["output"]).read_bytes()).hexdigest(), state["sha256"])
        self.assertEqual((moved / core.MANIFEST).read_bytes(), manifest)
        (moved / state["output"]).unlink()
        result = self.check(expected=1)
        self.assertIn("output_link", {f["code"] for f in result["findings"]})

    def test_gate_failure_correction_and_receipt_are_separate(self):
        self.initialize()
        task = dict(id="DEMO-ACT-0001", type="task", status="ready", gate="DEMO-GAT-0001")
        gate = dict(id="DEMO-GAT-0001", type="gate", status="failed")
        self.note("02_task.md", **task)
        self.note("03_gate.md", **gate)
        self.assertIn("gate_readiness", {f["code"] for f in self.check(expected=1)["findings"]})
        gate.update(status="passed", approver="Fixture approver", authorization_evidence=["Synthetic local-file scope"])
        self.note("03_gate.md", **gate)
        self.check()
        # The harness writes a local artifact; the checker does not execute or authorize it.
        result = self.project / "04_delivery.txt"
        result.write_text("Synthetic local delivery\n")
        task.update(status="complete", outputs=[result.name], validation_evidence=["Read-back matched expected text"])
        self.assertEqual(result.read_text(), "Synthetic local delivery\n")
        self.note("02_task.md", **task)
        self.note("05_receipt.md", id="DEMO-HND-0001", type="handover", status="transferred", acceptance_evidence=[])
        self.check()
        self.note("05_receipt.md", id="DEMO-HND-0001", type="handover", status="accepted", acceptance_evidence=[])
        self.assertIn("acceptance", {f["code"] for f in self.check(expected=1)["findings"]})
        self.note("05_receipt.md", id="DEMO-HND-0001", type="handover", status="accepted", acceptance_evidence=["Synthetic receipt assertion"])
        self.check()

    def test_revoked_delegation_is_seen_on_fresh_process(self):
        self.initialize()
        grant = dict(id="DEMO-DLG-0001", type="delegation", status="active", delegator="Fixture human",
                     delegate="Fixture agent", scope="Local synthetic work", allowed_operations=["read"],
                     allowed_targets=["fixture"], budget_limit="0", budget_unit="units",
                     valid_from="2000-01-01", expires_on="2099-12-31", subdelegation="forbidden",
                     approver="Fixture human", authorization_evidence=["Synthetic assertion"])
        self.note("02_delegation.md", **grant)
        self.note("03_task.md", id="DEMO-ACT-0001", type="task", status="ready", delegation=grant["id"])
        self.check()
        grant["status"] = "revoked"
        self.note("02_delegation.md", **grant)
        result = self.check(expected=1)
        self.assertIn("delegation_readiness", {f["code"] for f in result["findings"]})
        self.assertEqual(core.properties((self.project / "03_task.md").read_text())[0]["status"], "ready")

    def test_investigation_keeps_unproven_claims_separate_from_selection(self):
        case = discovery_fixtures.DiscoveryTests()
        case.setUp()
        self.addCleanup(case.doCleanups)
        case.framed()
        claim = case.add("claim", status="unknown", evidence_level="E0", claim="Synthetic question",
                         decision_context="Whether to investigate", rationale="No evidence yet")
        self.assertEqual(case.check()["errors"], 0)
        claim.update(status="supported", evidence_level="E1")
        self.assertIn("evidence", case.codes())
        source = case.add("source", kind="synthetic", status="inspected", title="Synthetic input",
                          location="fixture", origin="test harness", inspected_on="2026-09-12",
                          independence_group="one fixture", finding="Preparation example only",
                          locator="fixture section", limitations="No market evidence")
        claim.update(context="preparation", supporting_sources=[source["id"]])
        self.assertEqual(case.check()["errors"], 0)
        self.assertFalse(any(r["type"] == "decision" for r in case.records))
        claim["context"] = "market"
        self.assertIn("evidence", case.codes())


if __name__ == "__main__":
    unittest.main()

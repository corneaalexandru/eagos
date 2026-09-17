"""Portable unified-lifecycle integration checks; disposable records only."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

core = load("unified_core", ROOT / "20_tools/00_eagos.py")
ods = load("unified_ods", ROOT / "20_tools/01_discovery.py")


class UnifiedLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.area = Path(self.temp.name).resolve()

    def test_portable_guides_match_the_maintained_source(self):
        expected = (ROOT / "04_operating_guide.md").read_bytes()
        for relative in ("10_eagos_project_starter/01_operating_guide.md",
                         "11_opportunity_discovery_starter/03_operating_guide.md"):
            self.assertEqual((ROOT / relative).read_bytes(), expected, relative)
        data, body, issues = core.properties(expected.decode())
        self.assertEqual(issues, [])
        self.assertEqual(data["framework_version"], core.VERSION)
        self.assertFalse(core.prose(body)[1])

    def test_each_profile_installs_a_portable_guide_with_real_manifest_hashes(self):
        for profile in ("P0", "P1", "P2"):
            with self.subTest(profile=profile):
                root = self.area / profile
                preview = core.init_project(root, "DEMO", "Ideas", "Owner", profile)
                self.assertFalse(root.exists())
                self.assertIn("01_operating_guide.md", preview["files"])
                core.init_project(root, "DEMO", "Ideas", "Owner", profile, True)
                guide = root / "01_operating_guide.md"
                manifest = json.loads((root / core.MANIFEST).read_text())
                self.assertEqual(manifest["baseline_hashes"][guide.name], core.digest(guide.read_bytes()))
                self.assertEqual(manifest["source_paths"][guide.name], "10_eagos_project_starter/01_operating_guide.md")
                result = core.check(root, "setup")
                self.assertEqual(result["errors"], 0, result)
                self.assertEqual(core.properties((root / "README.md").read_text())[0]["activation_status"], "not_assessed")

    def test_discovery_installs_the_same_lifecycle_without_creating_research_or_approval(self):
        root = self.area / "discovery"
        ods.init_portfolio(root, "DEMO", "Ideas", "Owner", True)
        guide = root / "03_operating_guide.md"
        self.assertEqual(guide.read_bytes(), (ROOT / "04_operating_guide.md").read_bytes())
        result = ods.check(root)
        self.assertEqual(result["errors"], 0, result)
        self.assertEqual(result["records"], 0)
        data = core.properties((root / ods.WORKSPACE).read_text())[0]
        self.assertEqual(data["status"], "setup")
        self.assertEqual(data["extension_version"], ods.VERSION)
        manifest = json.loads((root / ods.MANIFEST).read_text())
        self.assertEqual(manifest["baseline_hashes"][guide.name], core.digest(guide.read_bytes()))

    def test_each_stage_remains_descriptive_and_cannot_activate_a_project(self):
        root = self.area / "project"
        core.init_project(root, "DEMO", "Ideas", "Owner", "P0", True)
        hub = root / "README.md"
        original = hub.read_text()
        for stage in sorted(core.LIFECYCLE_STAGES):
            with self.subTest(stage=stage):
                hub.write_text(original.replace("lifecycle_stage: discover", "lifecycle_stage: " + stage))
                before = hub.read_bytes()
                result = core.check(root, "active")
                codes = {f["code"] for f in result["findings"]}
                self.assertIn("activation", codes)
                self.assertNotIn("lifecycle_stage", codes)
                self.assertEqual(hub.read_bytes(), before)

    def test_absent_legacy_stage_is_valid_and_unsupported_stage_is_reported(self):
        root = self.area / "project"
        core.init_project(root, "DEMO", "Ideas", "Owner", "P0", True)
        hub = root / "README.md"
        original = hub.read_text()
        hub.write_text(original.replace("lifecycle_stage: discover\n", ""))
        self.assertEqual(core.check(root)["errors"], 0)
        for value in ("automatically-approved", '["launch"]'):
            with self.subTest(value=value):
                hub.write_text(original.replace("lifecycle_stage: discover", "lifecycle_stage: " + value))
                self.assertIn("lifecycle_stage", {f["code"] for f in core.check(root)["findings"]})

    def test_missing_required_guide_fails_before_creating_a_destination(self):
        package = self.area / "incomplete_package"
        starter = package / "10_eagos_project_starter"
        shutil.copytree(ROOT / "10_eagos_project_starter", starter)
        (starter / "01_operating_guide.md").unlink()
        destination = self.area / "project"
        with self.assertRaises(FileNotFoundError):
            core.init_project(destination, "DEMO", "Ideas", "Owner", "P0", True, package)
        self.assertFalse(destination.exists())

    def test_guide_source_fingerprint_is_checked_by_drift(self):
        root = self.area / "project"
        core.init_project(root, "DEMO", "Ideas", "Owner", "P0", True)
        guide = root / "01_operating_guide.md"
        guide.write_text(guide.read_text() + "\nA project-specific instruction.\n")
        before = guide.read_bytes()
        entry = next(x for x in core.drift(root, ROOT)["files"] if x["path"] == guide.name)
        self.assertEqual(entry["local"], "locally_modified")
        self.assertEqual(entry["upstream"], "unchanged")
        self.assertEqual(guide.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()

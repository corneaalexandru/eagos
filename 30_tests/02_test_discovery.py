"""Standalone read-only checks for earlier ODS schema 1 workspaces."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "20_tools/01_discovery.py"


class LegacyDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.area = Path(self.temp.name).resolve()
        self.workspace = self.area / "portfolio"
        self.workspace.mkdir()

    def write_workspace(self, version="1.3.0", extra=""):
        data = ("---\nschema_version: \"1\"\nextension: EAGOS-ODS\n"
                f"extension_version: \"{version}\"\n"
                "portfolio_code: DEMO\nowner: Fixture owner\nwrite_owner: Fixture writer\n"
                "required_filters: [\"mandate_fit\"]\nvalidation_limit: 1\n---\n" + extra)
        path = self.workspace / "00_opportunity_workspace.md"
        path.write_text(data)
        return path

    def cli(self, *args):
        return subprocess.run([sys.executable, str(TOOL), *map(str, args)],
                              capture_output=True, text=True)

    def test_retired_init_creates_nothing(self):
        destination = self.area / "new_portfolio"
        result = self.cli("init", destination, "--code", "DEMO", "--name", "Demo",
                          "--owner", "Owner", "--apply")
        self.assertEqual(result.returncode, 2)
        self.assertIn("retired", result.stderr)
        self.assertFalse(destination.exists())

    def test_supported_legacy_versions_check_without_writing(self):
        for version in ("1.0.0", "1.3.0"):
            with self.subTest(version=version):
                path = self.write_workspace(version)
                before = hashlib.sha256(path.read_bytes()).hexdigest()
                result = self.cli("check", self.workspace, "--format", "json")
                self.assertEqual(result.returncode, 0, result.stderr)
                data = json.loads(result.stdout)
                self.assertEqual(data["errors"], 0, data)
                self.assertEqual(data["records"], 0)
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)

    def test_unsupported_version_fails_without_writing(self):
        path = self.write_workspace("9.0.0")
        before = path.read_bytes()
        result = self.cli("check", self.workspace, "--format", "json")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("schema", {f["code"] for f in json.loads(result.stdout)["findings"]})
        self.assertEqual(path.read_bytes(), before)

    def test_malformed_legacy_fence_is_reported(self):
        self.write_workspace(extra="\n```discovery\nid: DEMO-OPP-0001\n")
        result = self.cli("check", self.workspace, "--format", "json")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("fence", {f["code"] for f in json.loads(result.stdout)["findings"]})


if __name__ == "__main__":
    unittest.main()

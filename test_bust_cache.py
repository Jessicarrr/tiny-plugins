import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import bust_cache


class BustCacheTests(unittest.TestCase):
    def make_repo(self, version="0.1.0+codex.old-token"):
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        manifest_path = root / "plugins" / "workflow" / ".codex-plugin" / "plugin.json"
        manifest_path.parent.mkdir(parents=True)
        manifest_path.write_text(
            json.dumps({"name": "workflow", "version": version}), encoding="utf-8"
        )
        marketplace_path = root / ".agents" / "plugins" / "marketplace.json"
        marketplace_path.parent.mkdir(parents=True)
        marketplace_path.write_text(json.dumps({"name": "tiny-plugins"}), encoding="utf-8")
        return root, manifest_path, marketplace_path

    def test_replaces_existing_suffix_and_reinstalls(self):
        root, manifest_path, marketplace_path = self.make_repo()
        run = Mock(return_value=subprocess.CompletedProcess([], 0))

        with patch.object(bust_cache, "find_codex", return_value="codex.CMD"):
            version = bust_cache.refresh_plugin(
                "workflow", root, marketplace_path, "local-test-123", run=run
            )

        self.assertEqual(version, "0.1.0+codex.local-test-123")
        self.assertEqual(json.loads(manifest_path.read_text(encoding="utf-8"))["version"], version)
        run.assert_called_once_with(
            ["codex.CMD", "plugin", "add", "workflow@tiny-plugins"], check=False
        )

    def test_preserves_version_prefix(self):
        root, manifest_path, marketplace_path = self.make_repo("1.2.3-beta.1+codex.previous")

        bust_cache.refresh_plugin(
            "workflow", root, marketplace_path, "local-test", install=False
        )

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.2.3-beta.1+codex.local-test")

    def test_rejects_plugin_name_mismatch_before_install(self):
        root, manifest_path, marketplace_path = self.make_repo()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["name"] = "different-plugin"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        original_contents = manifest_path.read_text(encoding="utf-8")
        run = Mock()

        with self.assertRaises(ValueError):
            bust_cache.refresh_plugin(
                "workflow", root, marketplace_path, "local-test", run=run
            )

        run.assert_not_called()
        self.assertEqual(manifest_path.read_text(encoding="utf-8"), original_contents)

    def test_rejects_invalid_marketplace_before_updating_manifest(self):
        root, manifest_path, marketplace_path = self.make_repo()
        original_contents = manifest_path.read_text(encoding="utf-8")
        marketplace_path.write_text(json.dumps({"name": "not valid"}), encoding="utf-8")

        with self.assertRaises(ValueError):
            bust_cache.refresh_plugin("workflow", root, marketplace_path, "local-test")

        self.assertEqual(manifest_path.read_text(encoding="utf-8"), original_contents)

    def test_reports_install_failure(self):
        root, _, marketplace_path = self.make_repo()
        run = Mock(return_value=subprocess.CompletedProcess([], 7))

        with patch.object(bust_cache, "find_codex", return_value="codex.CMD"):
            with self.assertRaisesRegex(RuntimeError, "exit code 7"):
                bust_cache.refresh_plugin(
                    "workflow", root, marketplace_path, "local-test", run=run
                )

    def test_reports_missing_codex(self):
        root, _, marketplace_path = self.make_repo()
        run = Mock()

        with patch.object(bust_cache, "find_codex", side_effect=FileNotFoundError("missing")):
            with self.assertRaisesRegex(FileNotFoundError, "missing"):
                bust_cache.refresh_plugin(
                    "workflow", root, marketplace_path, "local-test", run=run
                )

        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()

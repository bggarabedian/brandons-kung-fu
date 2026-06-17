"""Cockpit-bridge config-loader tests (stdlib unittest; no real vault)."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _util import (  # noqa: E402
    REPO_ROOT, kungfu, git_init, make_folders, run_doctor, write_config,
)


class ExampleTemplateTests(unittest.TestCase):
    def test_example_file_exists_and_is_valid_json(self):
        example = REPO_ROOT / kungfu.COCKPIT_EXAMPLE_NAME
        self.assertTrue(example.exists(), f"missing committed template: {example.name}")
        cfg = json.loads(example.read_text(encoding="utf-8"))
        self.assertIsInstance(cfg, dict)
        self.assertIn("cockpit_vault", cfg)
        self.assertIn("folders", cfg)

    def test_example_is_inert_placeholder(self):
        example = REPO_ROOT / kungfu.COCKPIT_EXAMPLE_NAME
        cfg = json.loads(example.read_text(encoding="utf-8"))
        # the committed template must NOT carry a real vault path
        self.assertIn("<", cfg["cockpit_vault"],
                      "committed example must keep a <placeholder> vault path")

    def test_example_lists_all_required_folders(self):
        example = REPO_ROOT / kungfu.COCKPIT_EXAMPLE_NAME
        cfg = json.loads(example.read_text(encoding="utf-8"))
        for name in kungfu.COCKPIT_REQUIRED_FOLDERS:
            self.assertIn(name, cfg["folders"])


class LoaderHardFailTests(unittest.TestCase):
    def test_missing_local_config_fails(self):
        # only the example present (copied in) — doctor must still fail until a
        # real local config exists.
        with tempfile.TemporaryDirectory() as r:
            repo = Path(r)
            git_init(repo)
            (repo / kungfu.COCKPIT_EXAMPLE_NAME).write_text(
                (REPO_ROOT / kungfu.COCKPIT_EXAMPLE_NAME).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            code, out, err = run_doctor(repo)
            self.assertNotEqual(code, 0)
            self.assertIn("not found", err)

    def test_invalid_json_fails(self):
        with tempfile.TemporaryDirectory() as r:
            repo = Path(r)
            git_init(repo)
            (repo / kungfu.COCKPIT_CONFIG_NAME).write_text("{ not valid json", encoding="utf-8")
            code, out, err = run_doctor(repo)
            self.assertNotEqual(code, 0)
            self.assertIn("not valid JSON", err)

    def test_placeholder_vault_fails(self):
        with tempfile.TemporaryDirectory() as r:
            repo = Path(r)
            git_init(repo)
            write_config(repo, repo, cockpit_vault="<ABSOLUTE path outside this repo>")
            code, out, err = run_doctor(repo)
            self.assertNotEqual(code, 0)
            self.assertIn("placeholder", err)

    def test_missing_vault_key_fails(self):
        with tempfile.TemporaryDirectory() as r:
            repo = Path(r)
            git_init(repo)
            (repo / kungfu.COCKPIT_CONFIG_NAME).write_text(
                json.dumps({"schema": 1, "folders": {}}), encoding="utf-8")
            code, out, err = run_doctor(repo)
            self.assertNotEqual(code, 0)
            self.assertIn("cockpit_vault", err)

    def test_non_object_config_fails(self):
        with tempfile.TemporaryDirectory() as r:
            repo = Path(r)
            git_init(repo)
            (repo / kungfu.COCKPIT_CONFIG_NAME).write_text("[]", encoding="utf-8")
            code, out, err = run_doctor(repo)
            self.assertNotEqual(code, 0)


if __name__ == "__main__":
    unittest.main()

"""Cockpit-bridge `doctor` safety-check tests (stdlib unittest; no real vault).

Each test builds a throwaway git repo and a throwaway vault under
tempfile.TemporaryDirectory(). No real vault, no plugins, no network.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _util import (  # noqa: E402
    kungfu, git_add, git_init, make_folders, run_doctor, write_config,
)


class GreenPathTests(unittest.TestCase):
    def test_clean_vault_passes(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            make_folders(vault)
            write_config(repo, vault)
            code, out, err = run_doctor(repo)
            self.assertEqual(code, 0, f"expected pass; out={out!r} err={err!r}")
            self.assertIn("OK", out)


class VaultLocationTests(unittest.TestCase):
    def test_vault_inside_repo_fails(self):
        with tempfile.TemporaryDirectory() as r:
            repo = Path(r)
            git_init(repo)
            vault = repo / "cockpit-vault"
            make_folders(vault)
            write_config(repo, vault)
            code, out, err = run_doctor(repo)
            self.assertEqual(code, 1)
            self.assertTrue("INSIDE the repo" in out or "git work tree" in out)

    def test_vault_inside_other_git_worktree_fails(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as h:
            repo, host = Path(r), Path(h)
            git_init(repo)
            git_init(host)               # a *different* repo that contains the vault
            vault = host / "vault"
            make_folders(vault)
            write_config(repo, vault)
            code, out, err = run_doctor(repo)
            self.assertEqual(code, 1)
            self.assertIn("git work tree", out)


class FolderTests(unittest.TestCase):
    def test_missing_folders_fail(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            make_folders(vault, names=["streams", "decisions"])   # incomplete
            write_config(repo, vault)
            code, out, err = run_doctor(repo)
            self.assertEqual(code, 1)
            self.assertIn("missing vault folder", out)


class TrackingTests(unittest.TestCase):
    def test_obsidian_tracked_fails(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            make_folders(vault)
            write_config(repo, vault)
            obs = repo / ".obsidian"
            obs.mkdir()
            (obs / "app.json").write_text("{}", encoding="utf-8")
            git_add(repo, ".obsidian/app.json")
            code, out, err = run_doctor(repo)
            self.assertEqual(code, 1)
            self.assertIn(".obsidian", out)

    def test_local_config_tracked_fails(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            make_folders(vault)
            write_config(repo, vault)
            git_add(repo, kungfu.COCKPIT_CONFIG_NAME)   # simulate a leak
            code, out, err = run_doctor(repo)
            self.assertEqual(code, 1)
            self.assertIn("tracked by git", out)


class NoNoteBodyReadTests(unittest.TestCase):
    def test_note_body_is_never_read_or_printed(self):
        secret = "TOP-SECRET-VAULT-CONTENT-DO-NOT-LEAK"
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            make_folders(vault)
            (vault / "streams" / "note.md").write_text(secret, encoding="utf-8")
            write_config(repo, vault)
            code, out, err = run_doctor(repo)
            self.assertEqual(code, 0)
            self.assertNotIn(secret, out)
            self.assertNotIn(secret, err)


if __name__ == "__main__":
    unittest.main()

"""Cockpit-bridge `init` folder-scaffold tests (stdlib unittest; no real vault).

Each test builds a throwaway git repo and a throwaway vault under
tempfile.TemporaryDirectory(). No real vault, no plugins, no network, no
.obsidian/, no note bodies are ever read or written.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from _util import (  # noqa: E402
    kungfu, git_add, git_init, make_folders, run_init, write_config,
)


def _existing_folders(vault: Path) -> list[str]:
    """Names of the required folders that currently exist as dirs under vault."""
    return [n for n in kungfu.COCKPIT_REQUIRED_FOLDERS if (vault / n).is_dir()]


class DryRunTests(unittest.TestCase):
    def test_dry_run_creates_nothing(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            write_config(repo, vault)
            code, out, err = run_init(repo, apply=False)
            self.assertEqual(code, 0, f"out={out!r} err={err!r}")
            self.assertIn("WOULD-CREATE", out)
            self.assertEqual(_existing_folders(vault), [], "dry-run must create no folders")


class ApplyTests(unittest.TestCase):
    def test_apply_creates_all_required_folders(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            write_config(repo, vault)
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 0, f"out={out!r} err={err!r}")
            self.assertIn("CREATED", out)
            self.assertEqual(sorted(_existing_folders(vault)),
                             sorted(kungfu.COCKPIT_REQUIRED_FOLDERS))

    def test_second_apply_is_idempotent(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            write_config(repo, vault)
            first_code, _o, _e = run_init(repo, apply=True)
            self.assertEqual(first_code, 0)
            before = sorted(_existing_folders(vault))
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 0, f"out={out!r} err={err!r}")
            self.assertIn("EXISTS", out)
            self.assertNotIn("CREATED", out, "second apply must create nothing new")
            self.assertEqual(sorted(_existing_folders(vault)), before)


class HardFailTests(unittest.TestCase):
    def test_missing_config_exits_2_and_creates_no_config(self):
        with tempfile.TemporaryDirectory() as r:
            repo = Path(r)
            git_init(repo)
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 2)
            self.assertIn("not found", err)
            self.assertFalse((repo / kungfu.COCKPIT_CONFIG_NAME).exists(),
                             "init must never create cockpit.local.json")

    def test_placeholder_vault_exits_2_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as r:
            repo = Path(r)
            git_init(repo)
            write_config(repo, repo, cockpit_vault="<ABSOLUTE path outside this repo>")
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 2)
            self.assertIn("placeholder", err)

    def test_absent_vault_root_exits_2_and_creates_zero_folders(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo = Path(r)
            vault = Path(v) / "nonexistent-vault"   # parent exists; vault root does not
            git_init(repo)
            write_config(repo, vault)
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 2)
            self.assertIn("does not exist", err)
            self.assertFalse(vault.exists(), "init must never create the vault root")

    def test_file_where_folder_expected_refuses_and_does_not_clobber(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            write_config(repo, vault)
            squatter = vault / "streams"            # a FILE where a folder is expected
            squatter.write_text("not a folder", encoding="utf-8")
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 2)
            self.assertIn("non-directory", err)
            self.assertTrue(squatter.is_file(), "the squatting file must be left intact")
            self.assertEqual(squatter.read_text(encoding="utf-8"), "not a folder")
            # no other folder should have been created (refusal is pre-write)
            self.assertEqual([n for n in kungfu.COCKPIT_REQUIRED_FOLDERS
                              if n != "streams" and (vault / n).is_dir()], [])


class SafetyGateTests(unittest.TestCase):
    def test_vault_inside_repo_refuses_and_creates_zero_folders(self):
        with tempfile.TemporaryDirectory() as r:
            repo = Path(r)
            git_init(repo)
            vault = repo / "cockpit-vault"
            vault.mkdir()                            # root exists, but it is INSIDE the repo
            write_config(repo, vault)
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 1)
            self.assertTrue("INSIDE the repo" in out or "git work tree" in out)
            self.assertEqual(_existing_folders(vault), [], "must create no folders inside a repo")

    def test_vault_inside_other_git_worktree_refuses_and_creates_zero_folders(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as h:
            repo, host = Path(r), Path(h)
            git_init(repo)
            git_init(host)                           # a *different* repo that contains the vault
            vault = host / "vault"
            vault.mkdir()
            write_config(repo, vault)
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 1)
            self.assertIn("git work tree", out)
            self.assertEqual(_existing_folders(vault), [])

    def test_tracked_local_config_refuses_and_creates_zero_folders(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            write_config(repo, vault)
            git_add(repo, kungfu.COCKPIT_CONFIG_NAME)   # simulate a leak: config tracked
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 1)
            self.assertIn("tracked by git", out)
            self.assertEqual(_existing_folders(vault), [])


class NoLeakTests(unittest.TestCase):
    def test_note_body_is_never_read_or_printed(self):
        secret = "TOP-SECRET-VAULT-CONTENT-DO-NOT-LEAK"
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            (vault / "streams").mkdir()                 # one folder pre-exists ...
            (vault / "streams" / "note.md").write_text(secret, encoding="utf-8")
            write_config(repo, vault)
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 0, f"out={out!r} err={err!r}")
            self.assertNotIn(secret, out)
            self.assertNotIn(secret, err)
            # the note body is left untouched
            self.assertEqual((vault / "streams" / "note.md").read_text(encoding="utf-8"), secret)

    def test_never_creates_dot_obsidian(self):
        with tempfile.TemporaryDirectory() as r, tempfile.TemporaryDirectory() as v:
            repo, vault = Path(r), Path(v)
            git_init(repo)
            write_config(repo, vault)
            code, out, err = run_init(repo, apply=True)
            self.assertEqual(code, 0)
            self.assertFalse((vault / ".obsidian").exists(),
                             "init must never create an .obsidian/ directory")


if __name__ == "__main__":
    unittest.main()

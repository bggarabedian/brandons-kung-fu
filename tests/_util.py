"""Shared helpers for the cockpit-bridge unittest suite (stdlib only).

Loads scripts/kungfu.py as a module and provides temp-repo / temp-vault helpers.
No real vault is ever touched; everything runs in tempfile.TemporaryDirectory().
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KUNGFU_PY = REPO_ROOT / "scripts" / "kungfu.py"


def load_kungfu():
    """Import scripts/kungfu.py as a module without requiring it on sys.path."""
    spec = importlib.util.spec_from_file_location("kungfu_under_test", KUNGFU_PY)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


kungfu = load_kungfu()


def git_init(path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(path)], check=True, capture_output=True)


def git_add(repo: Path, rel: str) -> None:
    subprocess.run(["git", "-C", str(repo), "add", "--", rel], check=True, capture_output=True)


def write_config(repo: Path, vault: Path, folders: dict | None = None,
                 cockpit_vault: str | None = None) -> Path:
    cfg = {
        "schema": 1,
        "cockpit_vault": cockpit_vault if cockpit_vault is not None else str(vault),
        "folders": folders if folders is not None else {n: n for n in kungfu.COCKPIT_REQUIRED_FOLDERS},
    }
    p = repo / kungfu.COCKPIT_CONFIG_NAME
    p.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return p


def make_folders(vault: Path, names=None) -> None:
    for n in (names if names is not None else kungfu.COCKPIT_REQUIRED_FOLDERS):
        (vault / n).mkdir(parents=True, exist_ok=True)


def run_doctor(repo: Path):
    """Run _cockpit_doctor(repo); return (exit_code, stdout, stderr).

    fail() raises SystemExit; capture it and normalize to an int exit code so a
    hard-fail is testable the same way as a soft (return 1) failure.
    """
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = kungfu._cockpit_doctor(repo)
        except SystemExit as e:
            code = e.code if isinstance(e.code, int) else 1
    return code, out.getvalue(), err.getvalue()

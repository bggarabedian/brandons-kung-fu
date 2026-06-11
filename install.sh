#!/usr/bin/env bash
# =============================================================================
# brandons-kung-fu — offline installer (bash)
#
# Local only. Does NOT: run git init, stage, commit, push, create remotes,
# install packages, or make any network call.
#
# Steps:
#   1. Verify we are at the brandons-kung-fu root.
#   2. If a git repo already exists here, wire the hook via
#      `git config core.hooksPath git-hooks` (never runs `git init`).
#   3. Seed git-hooks/denylist.local.txt from the example (never overwrites).
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# --- root detection via required marker files
missing=0
for marker in "git-hooks/pre-push.sh" "git-hooks/denylist.example.txt" "README.md"; do
  [ -f "$marker" ] || { echo "ERROR: missing '$marker'." >&2; missing=1; }
done
if [ "$missing" -ne 0 ]; then
  echo "ERROR: this is not the brandons-kung-fu root. Run install.sh from there." >&2
  exit 1
fi
echo "[bkf] root detected: $SCRIPT_DIR"

# --- make the hook executable (no-op on filesystems without exec bits)
chmod +x "git-hooks/pre-push.sh" 2>/dev/null || true

# --- hook wiring (local config only; never runs `git init`)
#     Wire ONLY when this kit root is itself the git top-level, so a parent repo
#     is never reconfigured.
TOPLEVEL="$(git rev-parse --show-toplevel 2>/dev/null || echo "")"
if [ -n "$TOPLEVEL" ]; then
  # normalize both paths (e.g. /d/x vs D:/x) before comparing
  top_norm="$(cd "$TOPLEVEL" 2>/dev/null && pwd -P || echo "")"
  root_norm="$(cd "$SCRIPT_DIR" 2>/dev/null && pwd -P || echo "")"
  if [ -n "$top_norm" ] && [ "$top_norm" = "$root_norm" ]; then
    git config core.hooksPath git-hooks
    echo "[bkf] hooks wired: core.hooksPath = git-hooks"
  else
    echo "[bkf] WARNING: Detected parent git repo; hook wiring skipped to avoid modifying the parent repo." >&2
    echo "[bkf]   Make the kit its own repo, then run:  git config core.hooksPath git-hooks"
  fi
else
  echo "[bkf] NOTE: no git repo here yet — hook wiring skipped (installer never runs 'git init')."
  echo "[bkf]   create a repo here, then run:  git config core.hooksPath git-hooks"
fi

# --- seed local denylist (never overwrite an existing one)
if [ -f "git-hooks/denylist.local.txt" ]; then
  echo "[bkf] git-hooks/denylist.local.txt already exists — left unchanged."
else
  cp "git-hooks/denylist.example.txt" "git-hooks/denylist.local.txt"
  echo "[bkf] seeded git-hooks/denylist.local.txt from the example."
fi

# --- next steps
cat <<'EOF'

Next steps:
  1. Edit git-hooks/denylist.local.txt — replace the placeholders with your own
     real protected terms (one literal term per line). It is gitignored.
  2. In a PRIVATE repo, make a test commit and push to confirm the pre-push hook
     runs and blocks any denylist term.
  3. Keep real tokens OUT of committed files — put them only in *.local files.

Done. No network, no installs, no git init, no commits were performed.
EOF

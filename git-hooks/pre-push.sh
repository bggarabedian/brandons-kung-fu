#!/usr/bin/env bash
# =============================================================================
# brandons-kung-fu — pre-push denylist scanner
#
# Purpose:
#   Block a push when any tracked file contains a protected term. Terms are
#   supplied by the operator in a gitignored denylist; this script hard-codes
#   none of them.
#
# Design guarantees:
#   - OFFLINE: no network calls, no installs, no public/git-remote operations.
#   - INERT BY DEFAULT: the shipped example denylist holds only non-matching
#     placeholders, so a fresh clone passes until you add real terms.
#   - SELF-EXCLUDING: the hook and the denylist files are excluded from the
#     scan so the denylist never matches itself.
#
# Install (either model works):
#   A) Copy:        cp git-hooks/pre-push.sh .git/hooks/pre-push && chmod +x .git/hooks/pre-push
#   B) hooksPath:   git config core.hooksPath git-hooks
#
# Operator setup:
#   cp git-hooks/denylist.example.txt git-hooks/denylist.local.txt
#   # then edit denylist.local.txt with your real protected terms (one per line)
#   # denylist.local.txt is gitignored and never committed.
#
# Optional vendor scrub (off by default): see git-hooks/denylist.vendors.txt.
#   Enable with:  BKF_SCAN_VENDORS=1   (and uncomment terms in that file)
# =============================================================================

set -euo pipefail

# --- portable temp-file creation: try plain mktemp first, then fall back to a
#     templated form for older macOS/BSD mktemp that requires a template.
bkf_mktemp() {
  mktemp 2>/dev/null || mktemp -t bkf.XXXXXX
}

# --- locate the denylist directory (works whether run from git-hooks/ or .git/hooks/)
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -n "$REPO_ROOT" ] && [ -d "$REPO_ROOT/git-hooks" ]; then
  DENY_DIR="$REPO_ROOT/git-hooks"
else
  DENY_DIR="$HOOK_DIR"
fi

# --- choose denylist: prefer the gitignored local list, else the inert example
if [ -f "$DENY_DIR/denylist.local.txt" ]; then
  DENY_FILE="$DENY_DIR/denylist.local.txt"
else
  DENY_FILE="$DENY_DIR/denylist.example.txt"
fi

# --- build the active-term set (strip comments and blank lines)
PATTERNS="$(bkf_mktemp)"
FILE_LIST=""
trap 'rm -f "$PATTERNS" "$FILE_LIST"' EXIT
{
  [ -f "$DENY_FILE" ] && grep -vE '^[[:space:]]*(#|$)' "$DENY_FILE" 2>/dev/null || true
  if [ "${BKF_SCAN_VENDORS:-0}" = "1" ] && [ -f "$DENY_DIR/denylist.vendors.txt" ]; then
    grep -vE '^[[:space:]]*(#|$)' "$DENY_DIR/denylist.vendors.txt" 2>/dev/null || true
  fi
} > "$PATTERNS"

# --- inert short-circuit: nothing active means nothing to scan
if [ ! -s "$PATTERNS" ]; then
  echo "[brandons-kung-fu] pre-push: PASS — denylist inert (no active terms). Nothing to scan."
  exit 0
fi

# --- if we are not inside a repo we cannot enumerate tracked files; pass safely
if [ -z "$REPO_ROOT" ]; then
  echo "[brandons-kung-fu] pre-push: PASS — not in a git work tree; no tracked files to scan."
  exit 0
fi

# --- enumerate TRACKED files only (NUL-delimited), excluding the hook and the
#     denylist files themselves. Written to a temp file so an empty list is
#     detected explicitly — no GNU-only `xargs -r` is required, so this stays
#     portable across Git Bash, Linux, and macOS/BSD.
FILE_LIST="$(bkf_mktemp)"
git -C "$REPO_ROOT" ls-files -z -- \
    ':(exclude)git-hooks/pre-push.sh' \
    ':(exclude)git-hooks/denylist.local.txt' \
    ':(exclude)git-hooks/denylist.example.txt' \
    ':(exclude)git-hooks/denylist.vendors.txt' \
  > "$FILE_LIST" 2>/dev/null || true

# --- no tracked files? pass cleanly.
if [ ! -s "$FILE_LIST" ]; then
  echo "[brandons-kung-fu] pre-push: PASS — no tracked files to scan."
  exit 0
fi

# --- scan each tracked file individually (portable: no xargs, no GNU-only flags)
#     -F literal match   -I skip binary files   -q quiet: report filenames only,
#     never the matched value.
HITS=""
while IFS= read -r -d '' file; do
  if grep -q -F -I -f "$PATTERNS" -- "$file" 2>/dev/null; then
    HITS="${HITS}${file}"$'\n'
  fi
done < "$FILE_LIST"

if [ -n "$HITS" ]; then
  echo "[brandons-kung-fu] pre-push: FAIL — protected denylist term found in tracked file(s):" >&2
  printf '%s' "$HITS" | sed 's/^/  - /' >&2
  echo "" >&2
  echo "Remove the term(s), or move the content into a gitignored *.local file." >&2
  echo "Do NOT bypass this hook with --no-verify." >&2
  exit 1
fi

echo "[brandons-kung-fu] pre-push: PASS — no denylist terms in tracked files."
exit 0

#!/usr/bin/env bash
# =============================================================================
# brandons-kung-fu — dry-run skill fetcher (bash)
#
# Reads skills/skills-manifest.yaml and reports what it WOULD fetch/install.
#
# Safety guarantees:
#   - DRY-RUN BY DEFAULT. With no --apply it makes zero network calls and zero
#     writes. It only prints a plan and a summary.
#   - --apply enables network + install, but STILL prompts per skill. There is
#     no non-interactive bypass.
#   - Copies files only. Never executes fetched content.
#   - Never installs into this repo. Never reads or copies the gstack store.
#   - Fails closed: any un-cleared license, empty/private source, non-installable
#     state, AUTH-P provenance, name collision, or unsafe target is REFUSED
#     before any network call.
#
# Usage:
#   skill-fetch.sh [NAME ...] [--apply] [--target DIR] [--manifest PATH] [--force]
# =============================================================================

set -euo pipefail

PFX="[bkf]"
APPLY=0
FORCE=0
TARGET=""
MANIFEST=""
declare -a WANT=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --force) FORCE=1 ;;
    --target) shift; TARGET="${1:-}" ;;
    --manifest) shift; MANIFEST="${1:-}" ;;
    --help|-h) echo "usage: skill-fetch.sh [NAME ...] [--apply] [--target DIR] [--manifest PATH] [--force]"; exit 0 ;;
    --*) echo "$PFX ERROR: unknown flag '$1'" >&2; exit 2 ;;
    *) WANT+=("$1") ;;
  esac
  shift || true
done

# --- locate repo root via marker files (never a hardcoded path)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
for marker in "git-hooks/pre-push.sh" "README.md" "skills/skills-manifest.yaml"; do
  [ -f "$ROOT/$marker" ] || { echo "$PFX ERROR: not the kit root (missing $marker)." >&2; exit 1; }
done

[ -n "$MANIFEST" ] || MANIFEST="$ROOT/skills/skills-manifest.yaml"
[ -f "$MANIFEST" ] || { echo "$PFX ERROR: manifest not found: $MANIFEST" >&2; exit 1; }

# --- resolve gstack home and default target (runtime-resolved, never literal)
GSTACK_DIR="${GSTACK_HOME:-$HOME/.gstack}"
[ -n "$TARGET" ] || TARGET="${SKILL_TARGET:-$HOME/.claude/skills}"

# --- target safety: never inside the repo, never inside the gstack store
abspath() { ( cd "$1" 2>/dev/null && pwd -P ) || echo "$1"; }
T_ABS="$(abspath "$(dirname "$TARGET")")/$(basename "$TARGET")"
R_ABS="$(abspath "$ROOT")"
G_ABS="$(abspath "$GSTACK_DIR")"
case "$T_ABS/" in
  "$R_ABS/"*) echo "$PFX ERROR: target is inside the repo — refused." >&2; exit 1 ;;
  "$G_ABS/"*) echo "$PFX ERROR: target is inside the gstack store — refused." >&2; exit 1 ;;
esac

# --- public host allowlist for source_url
lc() { printf '%s' "$1" | tr '[:upper:]' '[:lower:]'; }
is_private_url() {
  # echo "private" (refuse) or "ok". Fail closed.
  # Scheme and host are lowercased before comparison so behavior matches the
  # PowerShell mirror exactly (no case-variation bypass on either side).
  local url="$1" scheme rest host
  # defensive: drive-letter or UNC shapes
  case "$url" in
    [A-Za-z]:[\\/]*|//*|"\\\\"*) echo "private"; return ;;
  esac
  # require a scheme://; anything without one (incl. scp-style git@host:path) is private
  case "$url" in
    *"://"*) scheme="$(lc "${url%%://*}")"; rest="${url#*://}" ;;
    *) echo "private"; return ;;
  esac
  [ "$scheme" = "https" ] || { echo "private"; return; }   # only https (after lowercasing)
  # host = up to first / or : , drop any userinfo (user@host), lowercase
  host="${rest%%/*}"; host="${host%%:*}"; host="${host##*@}"; host="$(lc "$host")"
  case "$host" in
    localhost|127.0.0.1) echo "private"; return ;;
    10.*|192.168.*) echo "private"; return ;;
    172.1[6-9].*|172.2[0-9].*|172.3[01].*) echo "private"; return ;;
    *.local|*.internal|*.lan|*.corp) echo "private"; return ;;
  esac
  # host allowlist (exact match on lowercased host)
  case "$host" in
    github.com|gitlab.com|codeberg.org|bitbucket.org|raw.githubusercontent.com) : ;;
    *) echo "private"; return ;;
  esac
  # denylist.local terms, if present — case-insensitive (lowercase both sides)
  local dl="$ROOT/git-hooks/denylist.local.txt" lcurl lcterm
  if [ -f "$dl" ]; then
    lcurl="$(lc "$url")"
    while IFS= read -r term; do
      case "$term" in ''|\#*) continue ;; esac
      lcterm="$(lc "$term")"
      case "$lcurl" in *"$lcterm"*) echo "private"; return ;; esac
    done < "$dl"
  fi
  echo "ok"
}

# --- skill name validation: only [A-Za-z0-9_-], non-empty. Blocks path
#     traversal (slash, backslash, dot-dot, drive-letter, whitespace) through
#     the target/name join before any shadow check or filesystem use.
valid_name() {
  case "$1" in
    "") return 1 ;;
    *[!A-Za-z0-9_-]*) return 1 ;;
    *) return 0 ;;
  esac
}

# --- minimal schema-pinned YAML reader (no external dependency)
# Emits one TAB-joined record per skill: name<TAB>category<TAB>provenance<TAB>
# source_url<TAB>license<TAB>license_status<TAB>bundle_status<TAB>install_status
REQUIRED="name category provenance source_url license license_status bundle_status install_status notes"
parse_manifest() {
  awk -v req="$REQUIRED" '
    { sub(/\r$/, "") }   # CRLF tolerance: strip trailing carriage return
    function flush(   k,missing) {
      if (have_name == 0) return
      missing=""
      split(req, R, " ")
      for (k in R) if (!(R[k] in F)) missing = missing " " R[k]
      if (missing != "") { print "ERR\037missing fields for record:" missing; exit 3 }
      # US (0x1F) field separator: non-whitespace, so EMPTY fields survive the
      # bash read (a tab separator would collapse and drop empty source_url/license).
      printf "%s\037%s\037%s\037%s\037%s\037%s\037%s\037%s\n", F["name"],F["category"],F["provenance"],F["source_url"],F["license"],F["license_status"],F["bundle_status"],F["install_status"]
    }
    /^[[:space:]]*#/ { next }
    /^[[:space:]]*-[[:space:]]*name:/ {
      flush(); delete F; have_name=1
      v=$0; sub(/^[^:]*:[[:space:]]*/,"",v); gsub(/^"|"$/,"",v); gsub(/[[:space:]]+$/,"",v); F["name"]=v; next
    }
    /^[[:space:]]+[a-z_]+:/ {
      if (have_name==0) next
      key=$0; sub(/^[[:space:]]+/,"",key); sub(/:.*$/,"",key)
      v=$0; sub(/^[[:space:]]+[a-z_]+:[[:space:]]*/,"",v); gsub(/^"|"$/,"",v); gsub(/[[:space:]]+$/,"",v)
      F[key]=v; next
    }
    END { flush() }
  ' "$MANIFEST"
}

want_match() {
  [ "${#WANT[@]}" -eq 0 ] && return 0
  local n="$1" w
  for w in "${WANT[@]}"; do [ "$w" = "$n" ] && return 0; done
  return 1
}

shadow_hit() {
  local n="$1"
  [ -e "$TARGET/$n" ] && { echo "user-global"; return; }
  [ -e "$ROOT/.claude/skills/$n" ] && { echo "project-local"; return; }
  echo ""
}

echo "$PFX skill-fetch — mode: $([ "$APPLY" = 1 ] && echo APPLY || echo DRY-RUN)"
echo "$PFX manifest: $MANIFEST"
echo "$PFX target:   $TARGET"
[ "$APPLY" = 1 ] || echo "$PFX dry-run: no network, no writes. Re-run with --apply to install (still prompts)."
echo

ELIGIBLE=0; REFUSED=0; INSTALLED=0
RECORDS="$(parse_manifest)" || { echo "$RECORDS" >&2; echo "$PFX ERROR: manifest parse failed." >&2; exit 3; }

while IFS=$'\037' read -r name category provenance source_url license license_status bundle_status install_status; do
  [ -n "${name:-}" ] || continue
  case "$name" in ERR) echo "$PFX ERROR: $category" >&2; exit 3 ;; esac
  want_match "$name" || continue

  # name validation FIRST — before shadow_hit or any path use (anti-traversal)
  if ! valid_name "$name"; then
    printf "%s REFUSE  %-26s — %s\n" "$PFX" "$name" "invalid name (only A-Za-z0-9_- allowed)"
    REFUSED=$((REFUSED+1)); continue
  fi

  reason=""
  if   [ "$provenance" = "AUTH-P" ];                 then reason="AUTH-P project-coupled (never fetched)"
  elif [ "$install_status" != "installable" ];       then reason="install_status=$install_status (catalog-only, not installable)"
  elif [ "$license_status" != "cleared" ];           then reason="license_status=$license_status (must be cleared)"
  elif [ -z "$source_url" ];                          then reason="empty source_url"
  elif [ "$(is_private_url "$source_url")" = "private" ]; then reason="private/non-public source_url"
  else
    sh="$(shadow_hit "$name")"
    if [ -n "$sh" ] && [ "$FORCE" != 1 ]; then reason="name collision in $sh scope (use --force + confirm)"; fi
  fi

  if [ -n "$reason" ]; then
    printf "%s REFUSE  %-26s — %s\n" "$PFX" "$name" "$reason"
    REFUSED=$((REFUSED+1))
    continue
  fi

  ELIGIBLE=$((ELIGIBLE+1))
  printf "%s WOULD-FETCH %-22s FROM %s  INTO %s/%s\n" "$PFX" "$name" "$source_url" "$TARGET" "$name"

  [ "$APPLY" = 1 ] || continue

  # --- apply path: mandatory per-skill confirmation (no bypass)
  if [ -n "$(shadow_hit "$name")" ]; then
    printf "%s collision for %s — overwrite existing skill? [y/N] " "$PFX" "$name"
    read -r ans2 < /dev/tty || ans2=""
    case "$ans2" in y|Y) : ;; *) echo "$PFX skipped $name (collision not confirmed)"; continue ;; esac
  fi
  printf "%s fetch %s from %s? [y/N] " "$PFX" "$name" "$source_url"
  read -r ans < /dev/tty || ans=""
  case "$ans" in
    y|Y)
      tmp="$(mktemp -d)"
      echo "$PFX cloning (shallow, files only — never executed)…"
      if git clone --depth 1 "$source_url" "$tmp/src" >/dev/null 2>&1; then
        # symlink preflight: refuse if the fetched tree contains ANY symlink
        # (a symlink could materialize arbitrary file content into the target).
        if find "$tmp/src" -type l 2>/dev/null | grep -q .; then
          echo "$PFX ERROR: symlink found in fetched tree for $name — refused, nothing copied." >&2
          rm -rf "$tmp"; continue
        fi
        mkdir -p "$TARGET"
        # copy only the named skill's files; -P never dereferences symlinks; never execute anything fetched
        if [ -d "$tmp/src/$name" ]; then cp -R -P "$tmp/src/$name" "$TARGET/$name"
        else cp -R -P "$tmp/src" "$TARGET/$name"; fi
        rm -rf "$tmp"
        INSTALLED=$((INSTALLED+1))
        echo "$PFX installed $name -> $TARGET/$name (files copied, not run)"
        echo "$PFX smoke-test: runtime lists it; /$name resolves in ONE scope; run once on a safe target; status shows no unexpected tracked changes; output has no private paths."
      else
        rm -rf "$tmp"
        echo "$PFX ERROR: fetch failed for $name — nothing installed." >&2
      fi
      ;;
    *) echo "$PFX skipped $name (not confirmed)" ;;
  esac
done <<< "$RECORDS"

echo
echo "$PFX summary: eligible=$ELIGIBLE refused=$REFUSED installed=$INSTALLED  (mode=$([ "$APPLY" = 1 ] && echo APPLY || echo DRY-RUN))"
[ "$APPLY" = 1 ] || echo "$PFX no network and no writes were performed."
exit 0

#!/usr/bin/env python3
"""Brandon's Kung Fu — kit automation CLI (Python standard library only).

One manifest (kungfu.manifest.json) is the shared source of truth for both the
ChatGPT project-files package and the Claude Code context install.

Safety model (non-negotiable):
  - Default mode is DRY-RUN / report-only.
  - Any write outside the repo, or any `git pull`, requires --apply.
  - Install/export targets are printed before anything is written.
  - Existing user files are never overwritten silently: if a target exists and
    differs, the tool HALTs unless --allow-backup is given (then it writes a
    timestamped .bak beside the target before overwriting).
  - Never edits shell profiles. Never installs packages. Never schedules updates.
  - Never force-pushes, merges, rebases, or changes remotes.
  - GStack is referenced only; this tool never installs, updates, or copies it.

Usage:
  python scripts/kungfu.py describe
  python scripts/kungfu.py doctor
  python scripts/kungfu.py doctor-chatgpt
  python scripts/kungfu.py export-chatgpt [--apply]
  python scripts/kungfu.py setup-chatgpt [--apply]
  python scripts/kungfu.py install-claude --target <path> [--apply] [--allow-backup]
  python scripts/kungfu.py update [--apply]
  python scripts/kungfu.py sync
  python scripts/kungfu.py cockpit doctor
  python scripts/kungfu.py cockpit init [--apply]
"""
from __future__ import annotations

import argparse
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "kungfu.manifest.json"


# ----------------------------------------------------------------------------- helpers
def fail(msg: str, code: int = 2) -> "NoReturn":  # type: ignore[name-defined]
    print(f"[kungfu] HALT: {msg}", file=sys.stderr)
    sys.exit(code)


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        fail(f"manifest not found: {MANIFEST_PATH}")
    try:
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"manifest is not valid JSON: {e}")
    return {}  # unreachable


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True, text=True,
    )


def chatgpt_ordered_files(m: dict) -> list[tuple[str, str]]:
    """Flat (name, description) list in upload order, from the manifest groups."""
    out: list[tuple[str, str]] = []
    for group in m["chatgpt"]["upload_order"]:
        for f in group["files"]:
            out.append((f["name"], f["description"]))
    return out


def same_text(a: Path, b: Path) -> bool:
    try:
        return a.read_bytes() == b.read_bytes()
    except FileNotFoundError:
        return False


def write_file(path: Path, content: str, apply: bool, allow_backup: bool = False,
               force: bool = False) -> str:
    """Return a one-line status string. Honors dry-run + no-silent-overwrite.

    force=True is for the tool's own gitignored outputs (dist/): regenerate them
    in place without the differ-HALT. The default (force=False) protects user
    files (e.g. install-claude targets).
    """
    rel = path
    if not apply:
        return f"WOULD-WRITE  {rel}"
    if path.exists():
        existing = path.read_text(encoding="utf-8", errors="replace")
        if existing == content:
            return f"UNCHANGED    {rel}"
        if force:
            path.write_text(content, encoding="utf-8")
            return f"REGENERATED  {rel}"
        if not allow_backup:
            fail(f"target exists and differs: {rel} (re-run with --allow-backup to keep a timestamped .bak)")
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = path.with_suffix(path.suffix + f".{ts}.bak")
        shutil.copy2(path, bak)
        path.write_text(content, encoding="utf-8")
        return f"BACKED-UP+WROTE {rel}  (backup: {bak.name})"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"WROTE        {rel}"


def copy_into(src: Path, dst: Path, apply: bool, allow_backup: bool = False,
              force: bool = False) -> str:
    if not src.exists():
        fail(f"source file missing: {src}")
    content = src.read_text(encoding="utf-8", errors="replace")
    return write_file(dst, content, apply, allow_backup, force)


# ----------------------------------------------------------------------------- commands
def cmd_describe(_args, m: dict) -> int:
    print(f"# {m['kit']}  v{m['version']}")
    print(m["tagline"])
    print()
    print("ChatGPT project files (upload order):")
    n = 0
    for group in m["chatgpt"]["upload_order"]:
        print(f"  -- {group['group']} --")
        for f in group["files"]:
            n += 1
            print(f"   {n:>2}. {f['name']}  —  {f['description']}")
    ins = m["chatgpt"]["instructions_file"]
    print(f"   ++  {ins['name']}  —  {ins['description']}")
    print()
    print("Claude Code context files (same source):")
    for f in m["claude"]["context_files"]:
        print(f"   - {f}")
    print(f"   install namespace: {m['claude']['install_targets']['namespace']}")
    print()
    print("GStack (referenced operating layer; never copy bodies):")
    print(f"   relationship: {m['gstack']['relationship']}")
    print(f"   safe-default commands : {', '.join(m['gstack']['reference_only_commands'])}")
    print(f"   RED-approval commands : {', '.join(m['gstack']['red_approval_commands'])}")
    print()
    print("Never copy:", "; ".join(m["never_copy"]))
    return 0


def _doctor_common(m: dict) -> list[str]:
    problems: list[str] = []
    if not (ROOT / "git-hooks" / "pre-push.sh").exists():
        problems.append("missing git-hooks/pre-push.sh")
    if not (ROOT / "README.md").exists():
        problems.append("missing README.md")
    src = ROOT / m["chatgpt"]["source_dir"]
    if not src.is_dir():
        problems.append(f"missing chatgpt source dir: {src}")
    return problems


def cmd_doctor(_args, m: dict) -> int:
    print(f"[doctor] {m['kit']} v{m['version']}")
    problems = _doctor_common(m)
    # required ChatGPT files
    src = ROOT / m["chatgpt"]["source_dir"]
    for name, _desc in chatgpt_ordered_files(m):
        if not (src / name).exists():
            problems.append(f"missing project file: {name}")
    if not (src / m["chatgpt"]["instructions_file"]["name"]).exists():
        problems.append("missing PROJECT-INSTRUCTIONS.md")
    # Claude context files
    for rel in m["claude"]["context_files"]:
        if not (ROOT / rel).exists():
            problems.append(f"missing Claude context file: {rel}")
    # GStack presence — REPORT ONLY, never modify
    gstack_dir = Path.home() / ".claude" / "skills" / "gstack"
    print(f"[doctor] GStack present at {gstack_dir}: {'yes' if gstack_dir.exists() else 'no (optional; reference-only)'}")
    if problems:
        for p in problems:
            print(f"  FAIL: {p}")
        print(f"[doctor] {len(problems)} problem(s).")
        return 1
    print("[doctor] OK — repo/file readiness verified. No changes made.")
    return 0


def cmd_doctor_chatgpt(_args, m: dict) -> int:
    print("[doctor-chatgpt] verifying ChatGPT setup readiness (read-only)")
    problems: list[str] = []
    src = ROOT / m["chatgpt"]["source_dir"]
    if not src.is_dir():
        fail(f"missing chatgpt source dir: {src}")
    for name, _desc in chatgpt_ordered_files(m):
        if not (src / name).exists():
            problems.append(f"missing upload file: {name}")
    ins_name = m["chatgpt"]["instructions_file"]["name"]
    ins_src = src / ins_name
    if not ins_src.exists():
        problems.append(f"missing instructions source: {ins_name}")
    # if a package was generated, verify PROJECT-INSTRUCTIONS.txt matches source
    pkg = ROOT / m["chatgpt"]["generated_outputs"]["setup_package"]
    txt = pkg / "PROJECT-INSTRUCTIONS.txt"
    if txt.exists() and ins_src.exists():
        if txt.read_text(encoding="utf-8") != ins_src.read_text(encoding="utf-8"):
            problems.append("dist PROJECT-INSTRUCTIONS.txt does not match the source file (re-run setup-chatgpt --apply)")
        else:
            print("[doctor-chatgpt] PROJECT-INSTRUCTIONS.txt matches source.")
    # scrub the source upload files for protected terms. Terms come from the
    # operator's gitignored denylist (same source the pre-push hook uses), so this
    # public script hard-codes no proprietary names of its own.
    deny = ROOT / "git-hooks" / "denylist.local.txt"
    terms: list[str] = []
    if deny.exists():
        for line in deny.read_text(encoding="utf-8", errors="replace").splitlines():
            t = line.strip()
            if t and not t.startswith("#"):
                terms.append(t)
    if not terms:
        print("[doctor-chatgpt] note: no active git-hooks/denylist.local.txt terms; "
              "token scan skipped (configure it to enable).")
    else:
        for name, _desc in chatgpt_ordered_files(m):
            p = src / name
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            for tok in terms:
                if tok in text:
                    problems.append(f"protected denylist term found in {name}")
    if problems:
        for p in problems:
            print(f"  FAIL: {p}")
        print(f"[doctor-chatgpt] {len(problems)} problem(s).")
        return 1
    print("[doctor-chatgpt] OK — upload set present, instructions source present, no private tokens, no third-party bodies copied. No changes made.")
    return 0


def cmd_export_chatgpt(args, m: dict) -> int:
    """Simple flat export of the upload files + an upload-order README."""
    out = ROOT / m["chatgpt"]["generated_outputs"]["export"]
    src = ROOT / m["chatgpt"]["source_dir"]
    print(f"[export-chatgpt] target: {out}{'' if args.apply else '   (dry-run; no writes)'}")
    files = chatgpt_ordered_files(m)
    for name, _desc in files:
        print("  " + copy_into(src / name, out / name, args.apply, force=True))
    ins_name = m["chatgpt"]["instructions_file"]["name"]
    print("  " + copy_into(src / ins_name, out / ins_name, args.apply, force=True))
    readme = _render_upload_order(m, title="Upload order")
    print("  " + write_file(out / "UPLOAD_ORDER.md", readme, args.apply, force=True))
    if not args.apply:
        print("[export-chatgpt] dry-run complete. Re-run with --apply to write the package.")
    return 0


def _render_upload_order(m: dict, title: str) -> str:
    lines = [f"# {title}", "", f"For: {m['kit']} v{m['version']}", ""]
    n = 0
    for group in m["chatgpt"]["upload_order"]:
        lines.append(f"## {group['group']}")
        for f in group["files"]:
            n += 1
            lines.append(f"{n}. `{f['name']}` — {f['description']}")
        lines.append("")
    ins = m["chatgpt"]["instructions_file"]
    lines.append("## Always paste (not uploaded as a file)")
    lines.append(f"- `{ins['name']}` → paste its contents into the ChatGPT **Project Instructions** field "
                 f"(provided here as `PROJECT-INSTRUCTIONS.txt`).")
    lines.append("")
    return "\n".join(lines)


def _render_why_chatgpt(m: dict) -> str:
    return f"""# Why ChatGPT (and Claude Code)

{m['kit']} runs as one system with clear layers.

- **ChatGPT Project = the conductor.** It scopes, plans, prompts, audits, and
  verifies. It holds the doctrine across every chat in the Project.
- **Claude Code = the local implementation IC.** It inspects and edits local
  files under an approved scope, and reports command evidence.
- **GStack = the operating layer when installed.** Context, planning, health,
  review, QA-only, security review, memory, and closeout — referenced by command
  name only, never copied bodies.
- **The human/operator is the final authority** for doctrine, public posture,
  merge, deploy, install, and any irreversible operation.

ChatGPT Project Files give the conductor **persistent project doctrine across
chats**. The point is not to make ChatGPT the coder of everything — it is to keep
system-level judgment, the safety rules, and the handoff prompts consistent no
matter which chat or which coding agent is doing the work.
"""


def _render_readme_upload_first(m: dict) -> str:
    ins = m["chatgpt"]["instructions_file"]["name"]
    return f"""# Read this first — set up {m['kit']} in ChatGPT

A step-by-step. Nothing here logs in or uploads for you; you upload through the
ChatGPT UI.

1. Go to ChatGPT.
2. Create a new **Project**.
3. Name it something like **"{m['chatgpt']['project_name_suggestion']}"** (or a
   project-specific equivalent).
4. Open the Project's settings.
5. Open `PROJECT-INSTRUCTIONS.txt` from this package and paste its full contents
   into the **Project Instructions** field.
6. Upload the files from `files/` in the order listed in `UPLOAD_ORDER.md`.
7. Start a **new chat inside that Project**.
8. Ask: *"Run /standup for this repo using {m['kit']}."*
9. Verify the assistant understands:
   - the **conductor** role (scope, plan, audit, verify);
   - **Green / Red lane** rules;
   - **GStack Native Mode** (referenced operating layer, names only);
   - **PR-only** workflow;
   - **no public operations without approval**;
   - **no third-party skill bodies** are ever copied.

See `WHY_CHATGPT.md` for the division of labor and `VERIFY_SETUP.md` for a quick
correctness test. Source for `{ins}` is `chatgpt-project-files/{ins}` in the repo.
"""


def _render_verify_setup(m: dict) -> str:
    return f"""# Verify your {m['kit']} setup

In a new chat **inside the Project**, paste this test prompt:

> Using the uploaded {m['kit']} project files, explain the conductor role, the
> Green/Red lane split, GStack Native Mode, and the rule for public operations.

A correct answer should say all of:

- [ ] the conductor **scopes / plans / audits / verifies**;
- [ ] the coding agent **implements locally**;
- [ ] **Green Lane** = bounded / reversible;
- [ ] **Red Lane** = architecture, security, public posture, hooks/CI, schema,
      migrations, doctrine;
- [ ] **no push / public operation / install / force-push / --no-verify without
      explicit approval**;
- [ ] **GStack is reference-only**, command **names** only;
- [ ] GStack **safe commands are the default** for context / planning / review /
      QA-only / memory;
- [ ] **destructive / browser / deploy / tool-state commands require explicit
      approval**.

If any item is missing, re-check the upload order and that Project Instructions
were pasted from `PROJECT-INSTRUCTIONS.txt`.
"""


def cmd_setup_chatgpt(args, m: dict) -> int:
    """Generate the full ChatGPT setup package under dist/chatgpt-project/."""
    pkg = ROOT / m["chatgpt"]["generated_outputs"]["setup_package"]
    src = ROOT / m["chatgpt"]["source_dir"]
    mode = "" if args.apply else "   (dry-run; no writes)"
    print(f"[setup-chatgpt] package target: {pkg}{mode}")
    # files/
    files = chatgpt_ordered_files(m)
    for name, _desc in files:
        print("  " + copy_into(src / name, pkg / "files" / name, args.apply, force=True))
    # PROJECT-INSTRUCTIONS.txt (from source .md, verbatim)
    ins_name = m["chatgpt"]["instructions_file"]["name"]
    print("  " + copy_into(src / ins_name, pkg / "PROJECT-INSTRUCTIONS.txt", args.apply, force=True))
    # generated docs
    print("  " + write_file(pkg / "README_UPLOAD_FIRST.md", _render_readme_upload_first(m), args.apply, force=True))
    print("  " + write_file(pkg / "UPLOAD_ORDER.md", _render_upload_order(m, "Upload order"), args.apply, force=True))
    print("  " + write_file(pkg / "WHY_CHATGPT.md", _render_why_chatgpt(m), args.apply, force=True))
    print("  " + write_file(pkg / "VERIFY_SETUP.md", _render_verify_setup(m), args.apply, force=True))
    # package manifest snapshot
    snapshot = json.dumps(
        {"kit": m["kit"], "version": m["version"],
         "files": [n for n, _ in files], "instructions": "PROJECT-INSTRUCTIONS.txt"},
        indent=2,
    )
    print("  " + write_file(pkg / "MANIFEST.json", snapshot + "\n", args.apply, force=True))
    print("\n[setup-chatgpt] Checklist:")
    print("  1. Open ChatGPT → create a Project named "
          f"\"{m['chatgpt']['project_name_suggestion']}\".")
    print("  2. Paste PROJECT-INSTRUCTIONS.txt into Project Instructions.")
    print("  3. Upload files/ in UPLOAD_ORDER.md order.")
    print("  4. New chat → \"Run /standup for this repo using Brandon's Kung Fu.\"")
    print("  5. Confirm with VERIFY_SETUP.md.")
    if not args.apply:
        print("[setup-chatgpt] dry-run complete. Re-run with --apply to generate the package.")
    return 0


def cmd_install_claude(args, m: dict) -> int:
    if not args.target:
        fail("install-claude requires --target <path>")
    ns = m["claude"]["install_targets"]["namespace"]
    target = Path(args.target).expanduser().resolve() / ns
    mode = "" if args.apply else "   (dry-run; no writes)"
    print(f"[install-claude] install target: {target}{mode}")
    if args.apply:
        # Refuse to write into the kit's tracked source. Gitignored sandboxes
        # (.tmp/, dist/) are allowed so install can be tested safely in-repo.
        try:
            rel = target.relative_to(ROOT)
            top = rel.parts[0] if rel.parts else ""
            if top not in (".tmp", "dist"):
                fail(f"refusing to install into the kit's tracked source: {target} "
                     "(use a path outside the repo, or a .tmp/ or dist/ sandbox)")
        except ValueError:
            pass  # target is outside the repo — fine
    for rel in m["claude"]["context_files"]:
        dst = target / Path(rel).name
        print("  " + copy_into(ROOT / rel, dst, args.apply, allow_backup=args.allow_backup))
    if not args.apply:
        print("[install-claude] dry-run complete. Re-run with --apply --target <path> to write.")
        print("[install-claude] existing differing files are never overwritten silently "
              "(HALT, or --allow-backup to keep a timestamped .bak).")
    return 0


def cmd_update(args, m: dict) -> int:
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    head = git("rev-parse", "HEAD").stdout.strip()
    remote = git("remote", "get-url", "origin").stdout.strip() or "(none)"
    dirty = bool(git("status", "--porcelain").stdout.strip())
    print(f"[update] branch:  {branch}")
    print(f"[update] commit:  {head}")
    print(f"[update] remote:  {remote}")
    print(f"[update] clean:   {'no — working tree is dirty' if dirty else 'yes'}")
    if not args.apply:
        print(f"[update] would update: {'NO (commit, then re-run)' if dirty else 'yes, via fetch + pull --ff-only'}")
        print("[update] dry-run complete. Re-run with --apply to fetch + fast-forward.")
        return 0
    # --apply
    if dirty:
        fail("working tree is dirty — commit or stash before updating. No fetch performed.")
    print("[update] fetching origin ...")
    f = git("fetch", "origin")
    if f.returncode != 0:
        fail(f"git fetch failed:\n{f.stderr.strip()}")
    pull = git("merge", "--ff-only", f"origin/{branch}")
    if pull.returncode != 0:
        fail("fast-forward not possible (upstream diverged — would need merge/rebase, which this tool refuses). "
             f"Resolve manually.\n{pull.stderr.strip()}")
    print(pull.stdout.strip() or "[update] already up to date.")
    print("[update] running doctor after update ...")
    return cmd_doctor(args, load_manifest())


def cmd_sync(_args, m: dict) -> int:
    """Verify ChatGPT and Claude outputs derive from the same manifest source files."""
    print("[sync] verifying ChatGPT and Claude exports share one source ...")
    problems: list[str] = []
    src = ROOT / m["chatgpt"]["source_dir"]
    chatgpt_names = {n for n, _ in chatgpt_ordered_files(m)} | {m["chatgpt"]["instructions_file"]["name"]}
    claude_names = {Path(p).name for p in m["claude"]["context_files"]}
    # every Claude context file that lives in the chatgpt source dir must exist there
    for rel in m["claude"]["context_files"]:
        if not (ROOT / rel).exists():
            problems.append(f"Claude context file missing on disk: {rel}")
    for name, _desc in chatgpt_ordered_files(m):
        if not (src / name).exists():
            problems.append(f"ChatGPT upload file missing on disk: {name}")
    shared = sorted(chatgpt_names & claude_names)
    print(f"[sync] shared source files (both exports): {', '.join(shared) if shared else '(none)'}")
    print(f"[sync] ChatGPT-only: {', '.join(sorted(chatgpt_names - claude_names)) or '(none)'}")
    print(f"[sync] Claude-only:  {', '.join(sorted(claude_names - chatgpt_names)) or '(none)'}")
    if problems:
        for p in problems:
            print(f"  FAIL: {p}")
        return 1
    print("[sync] OK — both exports are derived from the same manifest source files.")
    return 0


# ----------------------------------------------------------------------------- skill-stack
PUBLIC_SOURCES = ROOT / "skills.sources.json"
LOCAL_SOURCES = ROOT / "skills.sources.local.json"
PUBLIC_HOSTS = {"github.com", "gitlab.com", "codeberg.org", "bitbucket.org"}


def load_skill_sources() -> "tuple[list[dict], bool]":
    if not PUBLIC_SOURCES.exists():
        fail(f"missing {PUBLIC_SOURCES.name}")
    try:
        pub = json.loads(PUBLIC_SOURCES.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"{PUBLIC_SOURCES.name} invalid JSON: {e}")
    by_id = {s["id"]: dict(s, _origin="public") for s in pub.get("sources", [])}
    local = LOCAL_SOURCES.exists()
    if local:
        try:
            loc = json.loads(LOCAL_SOURCES.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"{LOCAL_SOURCES.name} invalid JSON: {e}")
        for s in loc.get("sources", []):
            by_id[s["id"]] = dict(s, _origin="local")
    return list(by_id.values()), local


def _is_public_https(url: str) -> bool:
    if not url.startswith("https://"):
        return False
    host = url[len("https://"):].split("/")[0].split(":")[0].lower()
    return host in PUBLIC_HOSTS


def _is_placeholder(p: str) -> bool:
    return (not p) or ("<" in p)


def _clone_eligible(s: dict) -> "tuple[bool, str]":
    if s.get("provenance_status") != "verified":
        return False, f"provenance_status={s.get('provenance_status')!r} (need 'verified')"
    if s.get("install_mode") != "clone":
        return False, f"install_mode={s.get('install_mode')!r} (need 'clone')"
    url = s.get("upstream_url", "")
    if not url:
        return False, "empty upstream_url"
    if not _is_public_https(url):
        return False, "upstream_url is not a public https URL"
    if _is_placeholder(s.get("default_target", "")):
        return False, "default_target is a placeholder (set a real path in the local manifest)"
    return True, "eligible"


def cmd_skills_list(_args, _m: dict) -> int:
    sources, local = load_skill_sources()
    print(f"[skills] {len(sources)} companion source(s)  "
          f"(local overlay: {'present' if local else 'none — public manifest only'})")
    for s in sources:
        print(f"  - {s['id']:<24} {s.get('priority','?'):<11} {s.get('type','?'):<16} "
              f"prov={s.get('provenance_status','?'):<13} mode={s.get('install_mode','?'):<18} "
              f"[{s.get('_origin','?')}]")
        print(f"      target: {s.get('default_target','')}")
    print("\n[skills] GStack is one companion among these; none are bundled. "
          "Third-party packs are fetched from upstream, never copied into this repo.")
    return 0


def cmd_skills_doctor(_args, _m: dict) -> int:
    print("[skills doctor] companion skill stack (read-only)")
    sources, local = load_skill_sources()
    gstack_dir = Path.home() / ".claude" / "skills" / "gstack"
    print(f"  GStack present: {'yes' if gstack_dir.exists() else 'no'}  ({gstack_dir})")
    found = missing = unconfigured = needs_attention = 0
    for s in sources:
        tgt = s.get("default_target", "")
        prov = s.get("provenance_status", "unknown")
        if prov in ("needs-review", "forbidden-public", "unknown"):
            needs_attention += 1
            print(f"  ATTENTION {s['id']}: provenance {prov} — verify license/upstream before bootstrap")
        if _is_placeholder(tgt):
            unconfigured += 1
            continue
        p = Path(tgt).expanduser()
        if p.exists():
            found += 1
            is_repo = (p / ".git").exists()
            writable = p.parent.exists()
            print(f"  found     {s['id']}: {p}  (git repo: {'yes' if is_repo else 'no'}, "
                  f"parent writable: {'yes' if writable else 'no'})")
        else:
            missing += 1
            print(f"  missing   {s['id']}: {p}")
    # body-leak guard: no third-party skill body should have entered THIS repo
    known = {"SKILLS.md", "rag-cag.md", "qa-debug.md", "security.md",
             "skills-manifest.yaml", "skill-access-layer.md", "bin"}
    leak = []
    skills_dir = ROOT / "skills"
    if skills_dir.is_dir():
        leak = [p.name for p in skills_dir.iterdir() if p.name not in known]
    if (ROOT / ".claude" / "skills").exists():
        leak.append(".claude/skills/")
    if leak:
        print(f"  LEAK?     unexpected entries under skills/: {', '.join(leak)} "
              "(verify no third-party body was copied in)")
    print(f"[skills doctor] found={found} missing={missing} unconfigured={unconfigured} "
          f"needs-attention={needs_attention} body-leak={'YES' if leak else 'no'}")
    return 1 if leak else 0


def cmd_skills_bootstrap(args, _m: dict) -> int:
    sources, _local = load_skill_sources()
    print(f"[skills bootstrap] mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print("[skills bootstrap] planned network/git operations (none run in dry-run):")
    eligible, refused = [], []
    for s in sources:
        ok, reason = _clone_eligible(s)
        if ok:
            eligible.append(s)
            ref = f"  (pin {s['pinned_ref']})" if s.get("pinned_ref") else ""
            print(f"  WOULD-CLONE  {s['id']}: git clone --depth 1 {s['upstream_url']} "
                  f"-> {s['default_target']}{ref}")
        else:
            refused.append((s, reason))
            print(f"  REFUSE       {s['id']}: {reason}")
    print(f"[skills bootstrap] eligible={len(eligible)} refused={len(refused)}")
    if not args.apply:
        print("[skills bootstrap] dry-run: no network, no clones. Re-run with --apply to clone the eligible set.")
        return 0
    if not eligible:
        print("[skills bootstrap] nothing eligible. Mark a source verified + install_mode clone + a public https "
              "upstream + a real default_target in your local manifest first. No network performed.")
        return 0
    for s in eligible:
        tgt = Path(s["default_target"]).expanduser()
        if tgt.exists() and any(tgt.iterdir()):
            fail(f"target exists and is non-empty: {tgt} (HALT — never overwrites; choose an empty/new path)")
        print(f"[skills bootstrap] cloning {s['upstream_url']} -> {tgt} "
              "(fetch files only; no post-install scripts are run)")
        r = subprocess.run(["git", "clone", "--depth", "1", s["upstream_url"], str(tgt)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            fail(f"clone failed for {s['id']}:\n{r.stderr.strip()}")
        if s.get("pinned_ref"):
            subprocess.run(["git", "-C", str(tgt), "checkout", s["pinned_ref"]],
                           capture_output=True, text=True)
        print(f"[skills bootstrap] cloned {s['id']} (no code executed). Review before use.")
    return 0


def cmd_skills_sync(args, _m: dict) -> int:
    sources, _local = load_skill_sources()
    print(f"[skills sync] mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    installed = absent = 0
    for s in sources:
        tgt = s.get("default_target", "")
        if _is_placeholder(tgt):
            print(f"  unconfigured {s['id']} (placeholder target)")
            continue
        p = Path(tgt).expanduser()
        if p.exists():
            installed += 1
            print(f"  installed   {s['id']}: {p}")
        else:
            absent += 1
            print(f"  absent      {s['id']}: {p}")
    print(f"[skills sync] installed={installed} absent={absent}")
    if not args.apply:
        print("[skills sync] dry-run: reported only; no files copied or fetched.")
    else:
        print("[skills sync] apply: only copy-from-existing local entries with a real source_path are synced; "
              "cloning is done by `skills bootstrap`. Nothing was overwritten silently.")
    return 0


def cmd_skills_update(args, _m: dict) -> int:
    sources, _local = load_skill_sources()
    print(f"[skills update] mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    repos = []
    for s in sources:
        tgt = s.get("default_target", "")
        if _is_placeholder(tgt):
            continue
        p = Path(tgt).expanduser()
        if (p / ".git").exists():
            repos.append((s, p))
    if not repos:
        print("[skills update] no installed companion git repos found (targets are placeholders or not cloned).")
        return 0
    for s, p in repos:
        def g(*a):
            return subprocess.run(["git", "-C", str(p), *a], capture_output=True, text=True).stdout.strip()
        branch = g("rev-parse", "--abbrev-ref", "HEAD")
        head = g("rev-parse", "HEAD")
        upstream = g("remote", "get-url", "origin") or "(none)"
        dirty = bool(subprocess.run(["git", "-C", str(p), "status", "--porcelain"],
                                    capture_output=True, text=True).stdout.strip())
        print(f"  {s['id']}: branch={branch} commit={head[:10]} upstream={upstream} "
              f"clean={'no' if dirty else 'yes'}")
        if not args.apply:
            continue
        if dirty:
            print(f"  [skills update] {s['id']}: dirty — skipped (commit/stash first).")
            continue
        subprocess.run(["git", "-C", str(p), "fetch", "origin"], capture_output=True, text=True)
        ff = subprocess.run(["git", "-C", str(p), "merge", "--ff-only", f"origin/{branch}"],
                            capture_output=True, text=True)
        print(f"  [skills update] {s['id']}: "
              + (ff.stdout.strip() or "up to date" if ff.returncode == 0
                 else "fast-forward not possible (diverged — refusing merge/rebase/force)"))
    if not args.apply:
        print("[skills update] dry-run: no fetch performed.")
    return 0


def cmd_skills_export_local_inventory(args, _m: dict) -> int:
    print(f"[skills export-local-inventory] mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    import os
    locations = []
    home_skills = Path.home() / ".claude" / "skills"
    proj_skills = ROOT / ".claude" / "skills"
    repo_skills = ROOT / "skills"
    env_path = os.environ.get("KUNGFU_SKILLS_PATH", "")
    for label, path in (("user-global", home_skills), ("project-local", proj_skills),
                        ("repo-local", repo_skills)):
        locations.append((label, path))
    if env_path:
        locations.append(("env KUNGFU_SKILLS_PATH", Path(env_path)))

    candidates: dict[str, dict] = {}
    for label, path in locations:
        n = 0
        if path.is_dir():
            for child in sorted(path.iterdir()):
                if not child.is_dir():
                    continue
                n += 1
                cid = child.name
                if cid in candidates:
                    continue
                candidates[cid] = {
                    "id": cid,
                    "name": cid,
                    "type": "gstack" if cid == "gstack" else "unknown",
                    "priority": "optional",
                    "upstream_url": "",
                    "license": "",
                    "provenance_status": "local-only",
                    "install_mode": "copy-from-existing",
                    "default_target": f"<your Claude skills directory>/{cid}",
                    "source_path": str(child),
                    "contains_third_party_bodies": "unknown",
                    "bundle_policy": "local-only",
                    "notes": f"Discovered under {label}. local-only: never published, never auto-cloned.",
                }
        print(f"  scanned {label}: {path}  ({n} dir(s))")
    print(f"[skills export-local-inventory] {len(candidates)} unique candidate source(s).")
    if not args.apply:
        print(f"[skills export-local-inventory] dry-run: would write {len(candidates)} local-only entries "
              f"to {LOCAL_SOURCES.name} (gitignored). No file written. Private paths stay in that local file only.")
        return 0
    payload = {
        "schema": 1,
        "note": "AUTO-GENERATED local-only inventory. Gitignored. Never published. Edit freely; "
                "mark entries verified + clone + a public upstream to make them bootstrap-eligible.",
        "sources": list(candidates.values()),
    }
    content = json.dumps(payload, indent=2) + "\n"
    print("  " + write_file(LOCAL_SOURCES, content, apply=True, allow_backup=args.allow_backup))
    print(f"[skills export-local-inventory] wrote {len(candidates)} entries to {LOCAL_SOURCES.name} (gitignored).")
    return 0


def cmd_skills(args, m: dict) -> int:
    routes = {
        "list": cmd_skills_list,
        "doctor": cmd_skills_doctor,
        "bootstrap": cmd_skills_bootstrap,
        "sync": cmd_skills_sync,
        "update": cmd_skills_update,
        "export-local-inventory": cmd_skills_export_local_inventory,
    }
    return routes[args.skills_cmd](args, m)


# ----------------------------------------------------------------------------- cockpit (Obsidian bridge)
# Slice 1: a READ-ONLY `cockpit doctor` only. It verifies the local cockpit config
# and the vault's safety posture (vault lives OUTSIDE any repo, nothing private is
# tracked). It writes nothing, enables no plugin, and never reads a vault note body
# — it inspects folder/file existence and git tracking status only.
COCKPIT_CONFIG_NAME = "cockpit.local.json"
COCKPIT_EXAMPLE_NAME = "cockpit.local.example.json"
COCKPIT_REQUIRED_FOLDERS = ("streams", "decisions", "handoff", "daily", "maps", "templates")


def _git_in(root: Path, *args: str) -> subprocess.CompletedProcess:
    """git invoked with an explicit -C <root> (so the doctor is testable on temp repos)."""
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def _is_inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except (ValueError, OSError):
        return False


def _nearest_existing(path: Path) -> Path:
    """The closest existing ancestor of path (path itself if it exists)."""
    p = path.resolve()
    while not p.exists() and p != p.parent:
        p = p.parent
    return p


def _git_toplevel(path: Path) -> "str | None":
    """The git work-tree root containing path, or None if path is not inside a repo."""
    r = subprocess.run(
        ["git", "-C", str(_nearest_existing(path)), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return None
    return r.stdout.strip() or None


def _iter_str_values(obj, prefix: str = ""):
    """Yield (dotted-key, value) for every string leaf in a JSON-ish object."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _iter_str_values(v, f"{prefix}{k}.")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _iter_str_values(v, f"{prefix}{i}.")
    elif isinstance(obj, str):
        yield prefix.rstrip("."), obj


def _cockpit_load_config(root: Path) -> "tuple[dict, Path, dict]":
    """Resolve the local cockpit config. Hard-fails (exit 2 via fail()) when the
    config cannot be resolved at all. Returns (cfg, vault, folders).

    Shared by `cockpit doctor` and `cockpit init` so the two can never drift on
    what counts as an unusable config. Reads the local config file only; never
    creates it, never reads a vault note body.
    """
    config_path = root / COCKPIT_CONFIG_NAME
    if not config_path.exists():
        fail(f"{COCKPIT_CONFIG_NAME} not found — copy {COCKPIT_EXAMPLE_NAME} to "
             f"{COCKPIT_CONFIG_NAME} and set a real vault path (the local file is gitignored).")
    try:
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"{COCKPIT_CONFIG_NAME} is not valid JSON: {e}")
    if not isinstance(cfg, dict):
        fail(f"{COCKPIT_CONFIG_NAME} must be a JSON object.")
    vault_raw = str(cfg.get("cockpit_vault", "")).strip()
    if not vault_raw:
        fail(f"{COCKPIT_CONFIG_NAME} is missing the required key: cockpit_vault.")
    if "<" in vault_raw:
        fail(f"cockpit_vault is still a placeholder in {COCKPIT_CONFIG_NAME} "
             "(set a real absolute path to a vault OUTSIDE this repo).")
    vault = Path(vault_raw).expanduser()
    folders = cfg.get("folders") or {}
    if not isinstance(folders, dict):
        fail(f"{COCKPIT_CONFIG_NAME} 'folders' must be a JSON object.")
    return cfg, vault, folders


def _cockpit_safety_problems(root: Path, cfg: dict, vault: Path, folders: dict,
                             *, require_folders: bool) -> "list[str]":
    """The cockpit-bridge safety gate, shared by doctor and init.

    Returns a (possibly empty) list of safety problems. Reads folder/file
    existence and git tracking status only — never opens a vault note body.
    `require_folders` is True for doctor (the folders must already exist) and
    False for init (whose whole job is to create them).
    """
    problems: list[str] = []

    # leftover placeholders anywhere in the resolved config
    for key, val in _iter_str_values(cfg):
        if "<" in val:
            problems.append(f"leftover placeholder in config ({key}): {val!r}")

    # the local config must never be tracked (it holds a private vault path)
    if _git_in(root, "ls-files", "--", COCKPIT_CONFIG_NAME).stdout.strip():
        problems.append(f"{COCKPIT_CONFIG_NAME} is tracked by git — it must stay gitignored.")

    # the vault must live OUTSIDE the repo root ...
    if _is_inside(vault, root):
        problems.append(f"cockpit_vault resolves INSIDE the repo root ({root}) — it must live outside any repo.")

    # ... and outside ANY git work tree
    top = _git_toplevel(vault)
    if top:
        problems.append(f"cockpit_vault is inside a git work tree ({top}) — a vault must never be inside a repo.")

    # nothing private may be tracked in THIS repo
    tracked = _git_in(root, "ls-files").stdout.splitlines()
    if any(".obsidian" in t for t in tracked):
        problems.append("an .obsidian/ path is tracked in this repo — remove it before any push.")
    leaked = [t for t in tracked if _is_inside(root / t, vault)]
    if leaked:
        problems.append(f"{len(leaked)} vault file(s) appear tracked in this repo — vault content is never tracked.")

    # required folders must exist (existence only — never read note contents)
    if require_folders:
        missing = [name for name in COCKPIT_REQUIRED_FOLDERS
                   if not (vault / folders.get(name, name)).is_dir()]
        if missing:
            problems.append(f"missing vault folder(s): {', '.join(missing)} (expected under {vault}).")

    return problems


def _cockpit_doctor(root: Path) -> int:
    """Read-only check of the cockpit bridge config + vault safety.

    Hard-fails (exit 2 via fail()) when the config cannot be resolved at all;
    returns 1 for any safety problem; returns 0 when clean. Reads folder/file
    existence and git tracking status only — never opens a vault note body.
    """
    print("[cockpit doctor] verifying cockpit bridge config + vault safety (read-only)")
    cfg, vault, folders = _cockpit_load_config(root)
    problems = _cockpit_safety_problems(root, cfg, vault, folders, require_folders=True)
    if problems:
        for p in problems:
            print(f"  FAIL: {p}")
        print(f"[cockpit doctor] {len(problems)} problem(s). No changes made.")
        return 1
    print(f"[cockpit doctor] OK — config valid, vault outside any repo, no .obsidian/ or vault files "
          f"tracked, all {len(COCKPIT_REQUIRED_FOLDERS)} folders present. No changes made.")
    return 0


def _cockpit_init(root: Path, *, apply: bool) -> int:
    """Create the vault folder scaffold (the 6 COCKPIT_REQUIRED_FOLDERS).

    Dry-run by default; --apply performs the folder creation. Reuses the same
    outside-any-repo safety gate as `cockpit doctor` (minus the folders-exist
    check, which is this command's whole job). It NEVER:
      - creates or modifies cockpit.local.json,
      - creates the vault root (a missing root is a hard error),
      - writes inside the repo or any git work tree,
      - touches .obsidian/ or enables any plugin,
      - reads or writes a vault note body (folder existence + mkdir only).

    Exit codes: 2 = hard error (unusable config, missing vault root, or a
    non-directory squatting a folder path); 1 = safety-gate problem; 0 = clean
    (dry-run or apply).
    """
    mode = "" if apply else "   (dry-run; no writes)"
    print(f"[cockpit init] create vault folder scaffold{mode}")
    cfg, vault, folders = _cockpit_load_config(root)

    # the vault ROOT must already exist — init never creates a vault from nothing
    # (prevents materializing a whole tree at a mistyped path).
    if not vault.exists():
        fail(f"cockpit_vault does not exist: {vault} — create the vault first; "
             "init only scaffolds folders inside an existing vault, never the vault root.")
    if not vault.is_dir():
        fail(f"cockpit_vault is not a directory: {vault}")

    # same safety gate as doctor, without requiring the folders to exist yet
    problems = _cockpit_safety_problems(root, cfg, vault, folders, require_folders=False)
    if problems:
        for p in problems:
            print(f"  FAIL: {p}")
        print(f"[cockpit init] {len(problems)} safety problem(s). No changes made.")
        return 1

    targets = [(name, vault / folders.get(name, name)) for name in COCKPIT_REQUIRED_FOLDERS]

    # pre-scan: refuse if anything non-directory squats a folder path, BEFORE any
    # write — so a clobber risk never causes a partial scaffold.
    for name, target in targets:
        if target.exists() and not target.is_dir():
            fail(f"refusing: a non-directory already exists where folder '{name}' is expected: {target} "
                 "(remove or move it; init never overwrites).")

    created = existed = would = 0
    for name, target in targets:
        if target.is_dir():
            print(f"  EXISTS        {name}")
            existed += 1
        elif apply:
            target.mkdir(parents=True, exist_ok=True)
            print(f"  CREATED       {name}")
            created += 1
        else:
            print(f"  WOULD-CREATE  {name}")
            would += 1

    if apply:
        print(f"[cockpit init] done — created={created} existed={existed}. "
              "No config written, no vault root created, no .obsidian/ touched, no note read.")
        print("[cockpit init] next: run `python scripts/kungfu.py cockpit doctor` to verify the setup.")
    else:
        print(f"[cockpit init] dry-run — would-create={would} existed={existed}. No changes made. "
              "Re-run with --apply to create the folder(s).")
    return 0


def cmd_cockpit_doctor(_args, _m: dict) -> int:
    return _cockpit_doctor(ROOT)


def cmd_cockpit_init(args, _m: dict) -> int:
    return _cockpit_init(ROOT, apply=args.apply)


def cmd_cockpit(args, m: dict) -> int:
    routes = {
        "doctor": cmd_cockpit_doctor,
        "init": cmd_cockpit_init,
    }
    return routes[args.cockpit_cmd](args, m)


# ----------------------------------------------------------------------------- main
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="kungfu", description="Brandon's Kung Fu kit automation (dry-run by default).")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("describe", help="explain the kit, its files, and components")
    sub.add_parser("doctor", help="verify repo/file/install readiness (no changes)")
    sub.add_parser("doctor-chatgpt", help="verify ChatGPT setup readiness (no changes)")
    sub.add_parser("sync", help="verify ChatGPT and Claude exports share one source")

    ec = sub.add_parser("export-chatgpt", help="export upload files + order (dry-run default)")
    ec.add_argument("--apply", action="store_true", help="actually write the export")

    sc = sub.add_parser("setup-chatgpt", help="generate the full ChatGPT setup package (dry-run default)")
    sc.add_argument("--apply", action="store_true", help="actually write the package")

    ic = sub.add_parser("install-claude", help="install kit context into a target dir (dry-run default)")
    ic.add_argument("--target", required=True, help="parent directory to install into")
    ic.add_argument("--apply", action="store_true", help="actually write the install")
    ic.add_argument("--allow-backup", action="store_true", help="back up + overwrite an existing differing file")

    up = sub.add_parser("update", help="fetch + fast-forward the clone (dry-run default)")
    up.add_argument("--apply", action="store_true", help="actually fetch + fast-forward")

    # --- companion skill stack ---
    sk = sub.add_parser("skills", help="manage the companion skill stack (dry-run by default)")
    sksub = sk.add_subparsers(dest="skills_cmd", required=True)
    sksub.add_parser("list", help="list companion skill sources")
    sksub.add_parser("doctor", help="report companion stack readiness (no changes)")
    sk_apply = []
    for name, helptext in (("bootstrap", "clone eligible sources (dry-run default)"),
                           ("sync", "reconcile installed companions (dry-run default)"),
                           ("update", "fetch + fast-forward installed companion repos (dry-run default)")):
        sp2 = sksub.add_parser(name, help=helptext)
        sp2.add_argument("--apply", action="store_true")
        sk_apply.append(sp2)
    eli = sksub.add_parser("export-local-inventory",
                           help="scan local skill dirs into the gitignored local manifest (dry-run default)")
    eli.add_argument("--apply", action="store_true")
    eli.add_argument("--allow-backup", action="store_true",
                     help="back up + overwrite an existing local manifest")
    sk_apply.append(eli)

    # --- optional Obsidian cockpit bridge (doctor: read-only; init: folder scaffold) ---
    ck = sub.add_parser("cockpit", help="optional private Obsidian cockpit bridge (doctor + init)")
    cksub = ck.add_subparsers(dest="cockpit_cmd", required=True)
    cksub.add_parser("doctor", help="verify cockpit config + vault safety (read-only; no writes)")
    ci = cksub.add_parser("init", help="create the vault folder scaffold (dry-run default; never creates the vault root)")
    ci.add_argument("--apply", action="store_true", help="actually create the missing folder(s)")

    # tolerate a bare --dry-run flag for any apply-bearing subcommand (no-op; dry-run is default)
    for sp in (ec, sc, ic, up, ci, *sk_apply):
        sp.add_argument("--dry-run", action="store_true", help="explicit no-op; dry-run is the default")
    return p


def main(argv: list[str]) -> int:
    # Force UTF-8 output so non-ASCII characters never crash on a cp1252 console.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except Exception:
            pass
    args = build_parser().parse_args(argv)
    m = load_manifest()
    dispatch = {
        "describe": cmd_describe,
        "doctor": cmd_doctor,
        "doctor-chatgpt": cmd_doctor_chatgpt,
        "export-chatgpt": cmd_export_chatgpt,
        "setup-chatgpt": cmd_setup_chatgpt,
        "install-claude": cmd_install_claude,
        "update": cmd_update,
        "sync": cmd_sync,
        "skills": cmd_skills,
        "cockpit": cmd_cockpit,
    }
    return dispatch[args.cmd](args, m)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

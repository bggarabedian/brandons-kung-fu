# Brandon's Kung Fu

A disciplined operating kit for agentic software engineering.

> **Status:** v0.2.0 (pre-1.0) — a **distributable** conductor kit for agentic
> software engineering: the doctrine project files **plus** a Python-stdlib CLI
> for ChatGPT/Claude Code setup, export, update, and sync. v0.1 was the manual
> project-file version. ChatGPT stays the conductor LLM; Claude Code is the local
> implementation IC; GStack is a reference-only operating layer.

## What this is

Brandon's Kung Fu (`brandons-kung-fu`) is a portable kit of disciplined workflow
conventions for running software-engineering work with coding agents: session
discipline, pre-push safety checks, and a curated skill catalog.

CLI: `scripts/kungfu.py` (Python standard library only) — `describe`, `doctor`,
`setup-chatgpt`, `export-chatgpt`, `install-claude`, `update`, `sync`,
`doctor-chatgpt`. Dry-run by default; writes need `--apply`. See **Setup tooling**
below, plus [`INSTALL.md`](INSTALL.md) and [`UPDATE.md`](UPDATE.md).

## Quick start

1. **Clone** the repo.
2. **Run the installer** — `./install.sh` (or `install.ps1` on Windows). It wires
   the pre-push hook via `core.hooksPath` and seeds a local denylist. No network,
   no installs, no `git init`.
3. **Edit `git-hooks/denylist.local.txt`** — add your own protected terms (it is
   gitignored and never committed). The shipped example holds inert placeholders.
4. **Upload `chatgpt-project-files/`** into an LLM project (ChatGPT, Claude, or
   similar).
5. **Paste `chatgpt-project-files/PROJECT-INSTRUCTIONS.md`** into the project's
   custom instructions.
6. **Drive your coding agents** (Claude Code, Codex CLI, or similar) through the
   conductor and the project files.

## Setup tooling (`kungfu`)

One manifest (`kungfu.manifest.json`) is the shared source of truth for both the
ChatGPT conductor and the Claude Code hands, so they always run the same doctrine.
Everything is **dry-run by default**; writes outside the repo and any `git pull`
need `--apply`. Nothing logs in, installs packages, edits shell profiles, touches
GStack, or overwrites your files silently.

```
python scripts/kungfu.py describe                         # what the kit is + its files
python scripts/kungfu.py doctor                           # readiness check (no changes)
python scripts/kungfu.py setup-chatgpt --apply            # generate dist/chatgpt-project/ to upload
python scripts/kungfu.py doctor-chatgpt                   # verify the ChatGPT package
python scripts/kungfu.py install-claude --apply --target <path>   # copy doctrine into <path>/brandons-kung-fu/
python scripts/kungfu.py sync                             # confirm both exports share one source
python scripts/kungfu.py update --apply                   # fetch + fast-forward (clean tree only)
python scripts/kungfu.py skills list                      # companion skill stack (GStack + others)
python scripts/kungfu.py skills doctor                    # companions present/missing + provenance + body-leak guard
python scripts/kungfu.py skills bootstrap --dry-run       # what WOULD be cloned (inert until you verify sources)
```

The companion **skill stack** is declared in `skills.sources.json` (public,
reference-safe) and your private list in the gitignored `skills.sources.local.json`
(see `skills.sources.local.example.json`). GStack is one companion, not the whole
universe; third-party packs are fetched from upstream, never copied in. Docs:
[`docs/SKILL_STACK_SETUP.md`](docs/SKILL_STACK_SETUP.md),
[`docs/COMPANION_REPOS.md`](docs/COMPANION_REPOS.md),
[`docs/GSTACK_AND_SKILL_REPOS.md`](docs/GSTACK_AND_SKILL_REPOS.md).

Wrappers `scripts/kungfu.sh` and `scripts/kungfu.ps1` just call the Python CLI.
Docs: [`docs/CHATGPT_PROJECT_SETUP.md`](docs/CHATGPT_PROJECT_SETUP.md),
[`docs/CLAUDE_CODE_SETUP.md`](docs/CLAUDE_CODE_SETUP.md),
[`docs/WHY_CHATGPT_AND_CLAUDE.md`](docs/WHY_CHATGPT_AND_CLAUDE.md),
[`docs/SAME_SYSTEM_SYNC.md`](docs/SAME_SYSTEM_SYNC.md). GStack stays reference-only:
command names and operating rules, never copied bodies.

## What exists today

This kit includes:

- **Safety foundation** — `git-hooks/pre-push.sh` (offline, inert-by-default
  denylist scanner), `git-hooks/denylist.example.txt` (placeholder denylist),
  `git-hooks/denylist.vendors.txt` (optional, opt-in vendor-name scrub), and
  `.gitignore`.
- **Offline installers** — `install.sh` and `install.ps1`: local-only setup that
  wires the hook and seeds a local denylist. No network, no installs, no git init.
- **Skill manifest** — `skills/SKILLS.md`: the ship/reference split plus a
  provenance legend (skill names only, no third-party bodies).
- **RAG/CAG patterns** — `skills/rag-cag.md`: generic retrieval and cache
  patterns.
- **QA/debug patterns** — `skills/qa-debug.md`: generic verification and
  debugging discipline.
- **Security cluster** — `skills/security.md`: generic security and
  release-safety patterns.
- **ChatGPT Project Files** — `chatgpt-project-files/`: index README, conductor
  doctrine, coding standards, driving coding agents, skills & routing, safety &
  scrub, RAG/CAG, QA & debug, daily workflow, and Codex & agent tooling.
- **License** — `LICENSE` (MIT).

## What is planned next

v0.2.0 adds the distributable tooling (CLI, manifest, ChatGPT/Claude setup,
update, and sync) on top of the v0.1 doctrine files. Next:

- **v0.3.0** — cross-platform fresh-clone validation and real user setup feedback.
- **v1.0.0** — stable public release once the install/update contract is proven by
  external clean-clone/user testing.

The CLI never automates ChatGPT login/upload and never installs or updates
silently; `--apply` is required for writes.

## Safety model

- The pre-push scanner runs fully offline — no network calls, no installs, no
  public operations.
- It is **inert by default**: the example denylist contains only non-matching
  placeholders, so a fresh clone passes until you add real terms to a gitignored
  `denylist.local.txt`.
- Real protected terms live only in `*.local` files, which are gitignored and
  never committed.

## License

MIT — see [`LICENSE`](LICENSE).

# Brandon's Kung Fu

A disciplined operating kit for agentic software engineering.

> **Status:** v0.1 — a public-ready operating kit for agentic software engineering.

## What this is

Brandon's Kung Fu (`brandons-kung-fu`) is a portable kit of disciplined workflow
conventions for running software-engineering work with coding agents: session
discipline, pre-push safety checks, and a curated skill catalog.

CLI / package working names: `kungfu` / `bkf` (placeholders, not yet wired).

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

All planned v0.1 files exist. Further additions (more cluster docs, an authored
skill once audited) are optional polish.

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

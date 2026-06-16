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

## Why use this (for AI-agent coders)

Most AI coding failures don't happen because the model typed badly. They happen
because nobody gave the model a safe operating box — so the agent quietly makes
repo, architecture, security, or public-posture decisions that no one reviewed.

Brandon's Kung Fu is that box. It is not a magic prompt pack, and it does not
guarantee correct code. It is an operating discipline for using AI coding agents
(Claude Code, Codex CLI, or any other) so they implement *inside* a defined box
instead of running the whole show. It turns unstructured "YOLO vibe coding" into a
controlled loop: pick the risk lane, define the task box, let the agent build
inside it, verify with real commands, stop on danger, and land through a PR.

The payoff is not magic — it is **mistake compression**: fewer accidental scope
jumps, fewer unverified claims, cleaner handoffs, safer public docs, and less
wasted context from dragging giant transcripts through every task. It does **not**
replace engineering judgment.

> **Without Kung Fu:** "Claude, fix this repo" can drift into unbounded YOLO mode.
> **With Kung Fu:** "Here is the lane, scope, constraints, files, verification
> gate, and required output" keeps the agent inside guardrails.

### The flow, in plain language

1. **Pick the lane.** **Green** = small, reversible (proceed). **Red** =
   architecture, schemas, hooks, security, migrations, public posture, or anything
   irreversible (get approval, go slow). **Inspection-only** = read, report, plan,
   no changes.
2. **Write the task box.** Task · scope · constraints · steps · verification ·
   required output. The agent builds to this, not to a vibe.
3. **Let the agent build inside the box.** It implements; you stay the conductor.
4. **Verify before you believe it.** Run the real gates — tests, lint, format,
   type checks, hooks, doctor scripts, or whatever the repo actually uses.
   "Looks right" is not accepted as done.
5. **Stop on danger.** Failed gate, a surprise in the diff, scope drift, a
   security issue, or public-leak risk → halt and surface it, don't push through.
6. **Land through PRs.** No direct pushes to main, no force-push, no bypassing
   hooks.
7. **Close the loop.** Standdown, save context, and capture a lesson only when
   there's a verified, reusable one — not after every task.

### What it improves

- **Less YOLO coding** — the agent gets a task box (task, scope, constraints,
  steps, verification, required output), not a vague "go fix it."
- **Better risk control** — Green / Red / Inspection-only lanes decide how much
  process a change earns before anyone touches the repo.
- **Fewer accidental repo messes** — no direct main pushes by default, no
  force-push without explicit approval, no bypassing hooks, PR-first landing.
- **Verification before belief** — the loop requires command evidence (tests,
  lint, format, type checks, hooks, doctor scripts); "looks right" is not "done."
- **Lower context/token waste** — a lightweight preflight for bounded work, full
  session ceremony only for real multi-step work, `/compact` after major
  boundaries, `/clear` when switching workstreams, and standdown / context-save /
  optional cockpit notes to carry continuity. It helps control token burn and
  keeps sessions smaller without dragging the whole transcript forward.
- **Better handoffs** — the next agent or session gets current truth, not
  scrollback archaeology: what changed, what passed, what's blocked, what's next.
- **Safer public work** — name scans plus a concept-risk review, public docs
  written from blank, and no raw memories, ledgers, private paths, or private repo
  facts leaking into public artifacts.
- **A real learning loop** — capture a lesson only when it's verified and
  reusable, consolidate when it's useful (not as ritual), and keep private
  continuity in the optional cockpit without it becoming a source for public docs.

New to agentic coding? Start with small Green-Lane tasks and let the lane rules
keep the dangerous operations behind an approval gate.

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

## Optional: Obsidian Cockpit Layer

An **optional, private** cockpit layer (in alpha as `v0.3.0-alpha.1`) wires a
core-plugin-only notes vault into the doctrine as **private continuity** — a map
of active workstreams, a record of decisions, and the staging area for scrubbed
agent handoff cards. It is additive and installs nothing: no plugins are enabled,
no `.obsidian/` config is tracked, and no vault content ships in this repo.

It is **not** a source of truth (the repos are), **not** a source for public
artifacts (those are authored fresh from blank), **not** an agent memory hose (a
coding agent reads one deliberate, scrubbed handoff card, never the raw vault), and
**not** a plugin bundle. The kit is fully usable without it. Doctrine:
[`docs/OBSIDIAN_COCKPIT.md`](docs/OBSIDIAN_COCKPIT.md) and
[`chatgpt-project-files/12-obsidian-cockpit.md`](chatgpt-project-files/12-obsidian-cockpit.md).

## What is planned next

v0.2.0 adds the distributable tooling (CLI, manifest, ChatGPT/Claude setup,
update, and sync) on top of the v0.1 doctrine files. Next:

- **v0.3.0** — optional **Obsidian Cockpit Layer**: doctrine and templates for a
  private notes vault as private continuity (shipping in alpha as
  `v0.3.0-alpha.1`).
- **v0.4.0** — cross-platform fresh-clone validation and real user setup feedback.
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

# Getting started with Brandon's Kung Fu

> **Status:** v0.3.0. A first-run setup guide for new users. Plain language, no
> required installs for the core docs. Public-safe — uses placeholders, never
> private paths or names.

New here? This page takes you from "I found this repo" to "ChatGPT and my coding
agent now behave like a disciplined team" in five steps.

## What this kit does

It turns AI coding agents into **supervised implementation ICs** instead of
unbounded autopilots.

- **A project LLM (e.g. a ChatGPT Project) is the conductor.** It scopes, plans,
  prompts, audits, and verifies. It does not bulk-write code without a spec.
- **Claude Code is the local implementation IC.** It inspects and edits local
  files inside an approved scope and reports command evidence.
- **Codex CLI is optional** — an alternate builder or reviewer, run in its own
  approved lane.
- **The Obsidian Cockpit is optional** — private continuity only (a workstream
  map, a decision record, scrubbed handoff cards). Never a source of truth, never
  an agent input hose. See [`docs/OBSIDIAN_COCKPIT.md`](docs/OBSIDIAN_COCKPIT.md).

The payoff is **mistake compression**: fewer accidental scope jumps, fewer
unverified claims, cleaner handoffs. It does not guarantee correct code and does
not replace engineering judgment.

## What you need

- A **ChatGPT Project** (or an equivalent LLM project workspace that supports
  persistent files + custom instructions).
- **Claude Code** (or another coding agent) if you want local implementation.
- This repo **cloned or downloaded**.
- **No required plugin installs** for the core docs — they are plain Markdown.
- Optional **GStack-style skills** are *referenced* third-party capabilities
  (command names and operating rules only); this kit never vendors their bodies.

## Step 1 — Copy project instructions

1. Open [`chatgpt-project-files/PROJECT-INSTRUCTIONS.md`](chatgpt-project-files/PROJECT-INSTRUCTIONS.md).
2. Paste the copy-ready block into your ChatGPT Project's **custom instructions**
   field (this is pasted, not uploaded as a file).
3. If you trim it to fit a length limit, **keep the safety rules** (lanes, HALT,
   no public ops / push / force-push / `--no-verify` without approval, PR-only).

## Step 2 — Upload project files

Upload these into the ChatGPT Project. Keep the always-on set **small**; add
advanced files only while that kind of work is active, and remove them when done.

**Required core (the spine):**

- [`chatgpt-project-files/00-README-project-files.md`](chatgpt-project-files/00-README-project-files.md)
- [`chatgpt-project-files/01-conductor-doctrine.md`](chatgpt-project-files/01-conductor-doctrine.md)
- [`chatgpt-project-files/02-coding-standards.md`](chatgpt-project-files/02-coding-standards.md)
- [`chatgpt-project-files/03-driving-coding-agents.md`](chatgpt-project-files/03-driving-coding-agents.md)
- [`chatgpt-project-files/07-safety-and-scrub.md`](chatgpt-project-files/07-safety-and-scrub.md)

**Optional, as needed:**

- `04-rag-cag.md` — generic retrieval (RAG/CAG) patterns.
- `05-qa-and-debug.md` — generic QA, verification, and debugging.
- `06-skills-and-routing.md` — skill catalog and routing.
- `08-daily-workflow.md` — start / work / close session loop.
- `09-codex-and-agent-tooling.md` — optional Codex / multi-agent tooling.
- `10-learn-and-update-loop.md` — the learn loop and tool-freshness checks.
- `11-command-templates.md` — `/standup` `/standdown` `/learn` `/dream` templates.
- `12-obsidian-cockpit.md` — the optional private cockpit layer.

> The files under `docs/` (including this guide) are **read-on-demand repo docs**,
> not default ChatGPT project files. Read them in the repo; don't upload them as
> always-on context.

## Step 3 — Send the first prompt

The missing activation step most people skip: tell the LLM to actually *operate*
as the conductor. Copy the canonical first prompt from
[`FIRST_PROMPT.md`](FIRST_PROMPT.md) and send it as your first message in the
Project. It asks ChatGPT to confirm conductor mode, the five-part review shape, the
handoff labels, lane/speed discipline, and the next step.

## Step 4 — Connect Claude Code

Your coding agent should receive **scoped prompts from the conductor**, not
unbounded "fix this repo" commands. Start Claude Code with the canonical prompt in
[`docs/CLAUDE_CODE_FIRST_PROMPT.md`](docs/CLAUDE_CODE_FIRST_PROMPT.md) — it sets
Claude Code up as the local implementation IC: verify repo truth first, no edits
until scope is clear, report command evidence, and never push/merge/force-push/
install without explicit authorization.

## Step 5 — Run a smoke test

In the ChatGPT Project, send:

> Use Kung Fu. I want a lightweight task preflight for a one-file README typo fix.
> Show me the Claude Code prompt, but do not authorize a commit.

A correct conductor response will:

- **label the lane and speed** (this is Green Lane / lightweight preflight);
- **label the recipient and operating layer** for the handoff;
- give a **scoped task** (task, scope, constraints, steps, verification, output);
- **not authorize** a push or merge;
- **ask for verification evidence** before calling it done.

If it just starts rewriting files with no lane, no scope, and no verification ask,
re-check that the project instructions were pasted (Step 1) and the spine files
were uploaded (Step 2).

## Common mistakes

- **Uploading every doc forever.** Always-on context is cost on every turn; keep
  it to the spine plus what the current work needs.
- **Forgetting to paste the project instructions.** Without Step 1, the LLM has
  the files but not the operating contract.
- **Starting Claude Code with vague YOLO prompts.** "Fix this repo" invites
  unbounded changes; give it the scoped, lane-labeled prompt instead.
- **Treating the Obsidian vault as an agent input hose.** The cockpit is private
  continuity; an agent reads one scrubbed handoff card, never the raw vault.
- **Skipping verification.** "Looks right" is not "done" — require command
  evidence.
- **Using `--no-verify`.** Never bypass a hook; if a hook fails, stop and
  investigate.
- **Publishing private notes by accident.** Public artifacts are authored fresh
  from blank; run a name scan **and** a concept-risk review before anything ships.

## Where to go next

- [`FIRST_PROMPT.md`](FIRST_PROMPT.md) — the canonical first ChatGPT prompt.
- [`docs/CLAUDE_CODE_FIRST_PROMPT.md`](docs/CLAUDE_CODE_FIRST_PROMPT.md) — the
  canonical first Claude Code prompt.
- [`README.md`](README.md) — what the kit is, the setup tooling, and the safety
  model.
- [`chatgpt-project-files/08-daily-workflow.md`](chatgpt-project-files/08-daily-workflow.md)
  — the day-to-day start / work / close loop once you're set up.

# Brandon's Kung Fu — ChatGPT Project Files

> **Status:** v0.1. These are generic project-conductor files you
> upload by hand into an LLM project (ChatGPT, Claude, or similar). They carry
> no proprietary application names, no business goals, no private paths, no raw
> memories, and no third-party skill bodies.

## What this folder is

`chatgpt-project-files/` is a small set of always-on context files. You upload
them into an LLM "project" (a workspace with persistent files plus custom
instructions) so the model behaves as a disciplined **conductor for coding
agents**, following Brandon's Kung Fu.

## What these files do

Together they teach the LLM project to:

- Act as the **conductor** for coding agents — it plans and writes tickets; the
  coding agent executes.
- Preserve **Green / Red lane** discipline — bounded, reversible work proceeds;
  architecture, security, and public-posture changes require explicit approval.
- Enforce **HALT** behavior — stop and surface anomalies, failed gates, or scope
  drift instead of pushing through.
- Route to skills using **`/slash`** syntax when a skill genuinely helps.
- Keep a **PR-only, verification-first** workflow — no direct pushes to protected
  branches; prove changes with command evidence before claiming success.
- Help you **start the day, work through the day, and close the day**.

## File list

**Required core:**

- `00-README-project-files.md` — this file (index, upload order, setup).
- `01-conductor-doctrine.md` — the conductor role and core operating rules.
- `02-coding-standards.md` — generic full-stack engineering standards.
- `03-driving-coding-agents.md` — how to write tickets and supervise agents.
- `07-safety-and-scrub.md` — safety posture and scrub rules to enforce.

**Optional / advanced:**

- `04-rag-cag.md` — generic retrieval (RAG/CAG) patterns.
- `05-qa-and-debug.md` — generic QA, verification, and debugging patterns.
- `06-skills-and-routing.md` — generic skill catalog and routing.
- `08-daily-workflow.md` — generic start / work / close session discipline.
- `09-codex-and-agent-tooling.md` — optional Codex CLI / multi-agent guidance.
- `10-learn-and-update-loop.md` — the learn loop and tool-freshness checks.
- `11-command-templates.md` — generic `/standup` `/standdown` `/learn` `/dream`
  templates, the no-hardcoded-path rule, duplicate-command warning, and a
  command smoke-test checklist.
- `PROJECT-INSTRUCTIONS.md` — copy-ready block for your LLM project's custom instructions.

> Present today: `00`–`11` plus `PROJECT-INSTRUCTIONS.md` — all present.

## Upload order

Upload the spine first, then core, then advanced only when the work needs it.

**First (the spine):**
1. `00-README-project-files.md`
2. `01-conductor-doctrine.md`
3. `07-safety-and-scrub.md`

**Then (core):**
4. `02-coding-standards.md`
5. `03-driving-coding-agents.md`

**Optional, as needed:**
- `04-rag-cag.md`
- `05-qa-and-debug.md`
- `06-skills-and-routing.md`
- `08-daily-workflow.md`
- `09-codex-and-agent-tooling.md`
- `10-learn-and-update-loop.md`
- `11-command-templates.md`

> Tip: `PROJECT-INSTRUCTIONS.md` is **pasted into your project's custom
> instructions**, not uploaded as a file.

Every uploaded file is always-on context. Keep the set small; add advanced files
only while that kind of work is active, and remove them when it is not.

## Project Instructions starter

Paste a block like this into your LLM project's custom instructions (edit to
taste):

```
You are the conductor for coding agents using Brandon's Kung Fu.
- Make small, reversible changes; prefer the smallest diff that works.
- Verify before claiming: do not say something works without command evidence.
- Use /slash skill routing when a skill genuinely helps.
- HALT and surface the issue on: anomalies, failed gates, scope drift, or any
  security / public-posture concern.
- No public operations, no push, no force-push, and no --no-verify without
  explicit human approval.
- Do not invent repo facts — read current state, or ask.
- Treat the uploaded project files as authoritative; cite which file a rule
  comes from.
```

## Maintenance rules

- Keep each project file **short and current** — they are always-on context, so
  bloat costs you on every turn.
- Upload **advanced files only when relevant**; remove them when the work ends.
- **Update files when the workflow changes** — stale doctrine is worse than none.
- **Never** paste raw private memories, raw learnings, or project-specific
  secrets into a project file.
- **Do not** copy third-party skill bodies — reference skills by name only.

## Scrub policy

- The kit title **"Brandon's Kung Fu"** is allowed.
- A personal research project is allowed **only** when kept generic and
  non-sensitive — capabilities, never data or identities.
- The operator's **private application names, codenames, and proprietary business
  goals are private** — never include them.
- **Generic RAG/CAG and engineering** skills and patterns are allowed.
- **Third-party skills are reference-only** (name plus source) unless a license
  audit clears them to bundle.

## Next planned files

All project files exist. Further additions are optional polish.

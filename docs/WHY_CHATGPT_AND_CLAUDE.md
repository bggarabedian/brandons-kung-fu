# Why ChatGPT and Claude Code (division of labor)

Brandon's Kung Fu is one system with clear layers. Each layer has one job.

| Layer | Role |
|---|---|
| **ChatGPT Project** | the always-on **conductor brain** — scopes, plans, prompts, audits, verifies; holds doctrine across chats |
| **Claude Code** | the **local hands** — inspects and edits local files under an approved scope, reports command evidence |
| **GStack** | the **skill / orchestration muscle** when installed — context, planning, health, review, QA-only, security, memory, closeout (referenced by name only) |
| **GitHub repo** | the **source of truth** — doctrine and code live here; changes land via PR |
| **Manifest** (`kungfu.manifest.json`) | the **alignment contract** — both the ChatGPT and Claude exports come from this one list |
| **Project files** | the **portable doctrine package** — uploaded to ChatGPT, copied to Claude |
| **Verification** | **command evidence** — "it works" is a measurement, not an opinion |

## The point

The goal is **not** to make ChatGPT the coder of everything. The goal is to keep
**system-level judgment, the safety rules, and the handoff prompts consistent** no
matter which chat is open or which coding agent is building.

- The conductor decides *what* gets built and *how success is checked*.
- The coding agent builds inside that box and proves it with commands.
- The human/operator remains the **final authority** for doctrine, public posture,
  merge, deploy, install, and any irreversible operation.

GStack stays **reference-only**: command names and operating rules, never copied
bodies. Safe GStack commands are the default for context/planning/review/QA-only/
memory; destructive, browser, deploy, and tool-state commands require explicit
per-task approval.

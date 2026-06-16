# Brandon's Kung Fu — Obsidian Cockpit Layer (Project File)

> **Status: v0.3.0-alpha.1.** Optional / advanced. Conductor-facing doctrine for
> an **optional** private cockpit. Generic patterns and placeholder-only note
> skeletons — no proprietary names, no business goals, no private paths, no raw
> memories, no third-party plugin bodies. Upload this file only while cockpit work
> is active.

This file teaches the conductor how to use an **optional private cockpit** (a
core-plugin-only notes vault) without letting it become the source of truth or an
unchecked input hose for coding agents. The full public-safe overview is in
`../docs/OBSIDIAN_COCKPIT.md`.

## Where it fits in the workflow

The cockpit sits **beside** the daily loop, never inside the trust chain:

- **Repos** are the source of truth.
- **Session ledgers / checkpoints** are the operational continuity record.
- **The cockpit** is private continuity — a map of streams, a record of
  decisions, and the staging area for scrubbed handoff cards.

In the start/work/close loop (`08-daily-workflow.md`), the cockpit is touched at
two optional moments only:

- **After `/standdown` / context-save** — optionally mirror a short, scrubbed
  summary of the session into the vault (a stream note or a decision note). The
  ledger is still the real record; the cockpit just files a human-readable view.
- **Before a handoff** — optionally draft the agent's prompt as a cockpit
  **handoff card**, then scrub it and hand it over.

It is never a gate, never a verification surface, and never consulted as
authoritative repo state. If the cockpit and a repo disagree, the repo wins; if
the cockpit and the ledger disagree, the ledger wins.

## Vault privacy rule

The vault is **private and lives outside any public repo.**

- `<COCKPIT_VAULT>` is never inside `<REPO_ROOT>`.
- `.obsidian/` (the app's config directory) is **never tracked** and never
  committed.
- Raw vault notes, raw ledgers, raw memories, and raw learnings stay local; none
  of them are published.

If a vault path, an `.obsidian/` directory, or a real note ever appears staged in
a public repo, **HALT** and remove it before any push.

## Public/private boundary rule

Nothing crosses from the vault into a public artifact by copy.

- **Public docs are authored fresh from blank** — never copy a private note and
  scrub it. Find-and-replace leaves traces in phrasing and in history.
- A coding agent is **never pointed at the raw vault**. No "read my vault and
  continue" — that is an input hose, and it leaks.
- The only thing that crosses into a prompt is a **deliberate handoff card** (next
  section), one at a time, reviewed first.

## Handoff-card rule

A **handoff card** is a short brief authored *for* the agent — not a private note
forwarded to it.

A card carries only:

- the **capability or task** in generic terms;
- the **scope and constraints** (what is in, what is out);
- the **verification** that proves success;
- the **required output**.

A card must **never** carry private paths, private remotes, proprietary or
codename project names, raw memories, raw ledgers, raw learnings, or secrets. Use
repo-relative placeholders (`<REPO_ROOT>`, `<LEDGER_DIR>`, `<LOCAL_LEARNINGS_DIR>`)
and resolve them locally — never bake a real absolute path into a card that will
be pasted into a prompt.

**One card at a time.** The agent gets the card, not the vault.

## Concept-risk review rule

A name/token scan is **necessary but not sufficient.** It catches literal
forbidden tokens; it does **not** catch concept-level leakage — private
architecture or domain doctrine described accurately without naming it.

Before any card crosses into a prompt, and before any cockpit-derived text lands
in a public doc, run a **concept-risk review**: read it as an outsider and ask
*"does this reveal a private system or decision even though no protected name
appears?"* If yes, rewrite it generically or do not send it.

## Placeholder-only note skeletons

These are **note patterns to adapt locally**, not real vault content and not
runnable commands. Keep resolved copies out of any public repo.

**Stream note** (`<COCKPIT_VAULT>/streams/<stream>.md`):

```
# <stream name — generic>
status:: <active | paused | blocked>
lane:: <green | red>
relates-to:: [[<other stream>]]

## Goal
<one or two generic sentences>

## Next smallest move
<the next verifiable step>

## Notes
<private working notes — never published>
```

**Decision note** (`<COCKPIT_VAULT>/decisions/<decision>.md`):

```
# Decision: <generic title>
date:: <YYYY-MM-DD>
status:: <decided | revisit>

## Context
<what prompted the decision, in generic terms>

## Choice
<what was chosen>

## Rationale
<why — the durable reasoning worth keeping>
```

**Handoff card** (`<COCKPIT_VAULT>/handoff/<task>.md` — scrub before it leaves):

```
# Handoff card: <generic task>
recipient:: <Claude Code | Codex | other coding agent>
lane:: <green | red>

Task: <what to build, generic>
Scope: <in / out>
Constraints: <rules the change must respect; placeholders only, no real paths>
Verification: <exact command(s) that prove success>
Required output: <what the agent returns>
```

Before any handoff card is used: confirm no real paths, no private names, no raw
memories/ledgers/learnings, and that a concept-risk review passed.

## Related project files

- `../docs/OBSIDIAN_COCKPIT.md` — the public-safe overview and core-plugin layout.
- `07-safety-and-scrub.md` — the vault scrub rules and the public/private boundary.
- `08-daily-workflow.md` — where the optional cockpit touch points sit in the loop.
- `10-learn-and-update-loop.md` — which verified lessons may be mirrored privately.
- `11-command-templates.md` — placeholder-only cockpit card patterns.

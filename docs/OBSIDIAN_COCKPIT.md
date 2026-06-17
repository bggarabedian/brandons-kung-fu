# Brandon's Kung Fu — Obsidian Cockpit Layer

> **Release status: v0.3.0.** Optional, private, additive. This document
> is doctrine for an **optional** cockpit layer. It installs nothing, enables no
> plugins, and ships no real vault. The repos and the session ledgers stay the
> source of truth; Obsidian only organizes private continuity around them.

## What the cockpit is

The **cockpit** is an optional private workspace where the operator keeps a human
view of the work: a map of active workstreams, a record of decisions, and the
short scrubbed cards used to brief a coding agent. It is built from a notes app
(Obsidian) using its **core plugins only**.

It exists because three different stores answer three different questions, and
mixing them is what causes leaks and drift:

- **Repos** answer *"what is the committed truth?"* — they stay the source of
  truth.
- **Session ledgers / checkpoints** answer *"what happened this session and what
  is in flight?"* — they stay the operational continuity record.
- **The cockpit** answers *"how do these pieces relate, and what do I hand the
  agent next?"* — private continuity, nothing more.

The cockpit never overrides the first two. If the cockpit and a repo disagree,
the repo wins; if the cockpit and the ledger disagree, the ledger wins.

## What it is used for

- **Private continuity** — a durable personal view that survives across chats and
  sessions, kept outside any public repo.
- **Workstream map** — one note per active stream, linked so the relationships are
  visible at a glance (which stream blocks which, what is paused).
- **Decision map** — a record of decisions and their rationale, so a choice made
  weeks ago is findable instead of re-litigated.
- **Handoff cards** — short, deliberately scrubbed briefs that become the prompt
  for a coding agent. The card is authored for handoff, not copied from a raw note.

## What it is NOT

- **Not a source of truth.** The repo is. The cockpit is a private index that
  points at the truth; it does not replace it.
- **Not a source for public artifacts.** Nothing in the vault is copied into a
  public repo, doc, or release. Public artifacts are authored fresh from blank.
- **Not an agent memory hose.** A coding agent is never pointed at the raw vault
  and told to ingest it. Only a deliberate, scrubbed handoff card crosses into a
  prompt — one card at a time, reviewed before it goes.
- **Not a plugin bundle.** This layer ships no third-party plugin bodies and no
  `.obsidian/` config. It is core-plugin-only by design.

## Core-plugin-only layout

The cockpit is built from the notes app's **bundled core plugins** — no community
or third-party plugins are required, so there is nothing third-party to vendor or
audit into this kit. A workable layout (placeholders only — replace `<…>` locally,
never commit the resolved paths):

```
<COCKPIT_VAULT>/                 # private vault — lives OUTSIDE <REPO_ROOT>, never tracked
  streams/                       # one note per active workstream (Backlinks + Graph show relations)
  decisions/                     # one note per decision: context, choice, rationale
  handoff/                       # scrubbed handoff cards authored for agent prompts
  daily/                         # Daily Notes: a light per-day log of what moved
  maps/                          # Canvas boards: a visual map of streams and dependencies
  templates/                     # note skeletons (Templates core plugin)
```

Core plugins this uses, and why:

- **Daily Notes** — a per-day log entry without ceremony.
- **Templates** — consistent note skeletons (a stream note, a decision note, a card).
- **Properties** — light structured fields (status, lane, links) on a note.
- **Backlinks** — see what references a note without maintaining links by hand.
- **Graph** — a visual map of how streams and decisions connect.
- **Canvas** — a freeform board for laying out dependencies and plans.
- **Bases** — a table/database view over notes that carry the same properties.

None of these require network access, and none of them belong in a public repo.

## Safe use rules

1. **The vault lives outside any public repo.** `<COCKPIT_VAULT>` is never inside
   `<REPO_ROOT>`, and `.obsidian/` is never tracked.
2. **No raw vault note becomes a public artifact.** Author public docs fresh from
   blank; do not copy-and-scrub a private note.
3. **Handoff cards are deliberate and scrubbed.** A card carries the capability,
   the task, and the check — never private paths, remotes, names, raw memories,
   raw ledgers, or raw learnings.
4. **One card at a time into a prompt.** The agent receives the card, not the
   vault. No bulk ingest.
5. **Concept-risk review, not just a token scan.** A name scan misses private
   architecture or doctrine described without naming it. Review every card for
   concept-level leakage before it crosses into a prompt or a public doc.
6. **The repo and the ledger win.** When the cockpit disagrees with committed or
   ledgered truth, trust the repo and the ledger, and fix the note.

## Checking your setup

`cockpit doctor` is a **read-only** safety check (added in `v0.3.2-alpha.1`). It
confirms a private vault is wired correctly and never reads a note body:

```
python scripts/kungfu.py cockpit doctor
```

It needs a local `cockpit.local.json` — copy `cockpit.local.example.json`, set your
vault path, and keep it local (the real config is git-ignored). The check verifies
the vault lives **outside** this repo and any other git work tree, the expected
folders exist, and that neither `.obsidian/` nor the local config nor any vault
note is tracked by git. It reports problems and exits non-zero; a clean setup exits
zero. It makes no changes and reads no note content. Until you create the local
config it stops and tells you to copy the example.

## When to use / when not to use

**Use it when:**

- you run many parallel workstreams and need a private map to keep them straight;
- decisions accumulate and you want them findable instead of re-derived;
- you brief coding agents often and want a clean, repeatable handoff-card habit.

**Skip it when:**

- the work is a single bounded task — a lightweight preflight is enough;
- you would be tempted to treat the vault as the source of truth (it is not);
- adding it would slow a fast Green-Lane batch without earning its overhead.

The cockpit is optional. The kit is fully usable without it; this layer is for
operators who already keep a private notes practice and want it wired into the
doctrine cleanly, without leaking into anything public.

## Related

- `chatgpt-project-files/12-obsidian-cockpit.md` — the conductor-facing doctrine.
- `chatgpt-project-files/07-safety-and-scrub.md` — the public/private boundary and
  the vault-specific scrub rules.
- `chatgpt-project-files/11-command-templates.md` — placeholder-only cockpit card
  patterns (notes, not runnable commands).

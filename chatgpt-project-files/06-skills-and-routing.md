# Brandon's Kung Fu — Skills and Routing

> **Status:** private scaffold. Generic routing guidance only — no third-party
> skill bodies, no proprietary names. Skills are named here, never copied.

This file explains how the conductor routes to skills. The catalog itself lives in
[`../skills/SKILLS.md`](../skills/SKILLS.md).

## What a skill is here

A skill is a named, reusable capability you invoke with `/slash` syntax (for
example, `/qa-only`). This kit treats skills as a **catalog of names**, not a
bundled library.

## The three states

- **Bundled** — authored by the kit owner, generic, and scrub-clean. Only these
  ship inside the kit, and only after a per-skill scrub and license check.
- **Referenced** — third-party skills, listed by `/slash` name plus a source note.
  Their bodies are **never** copied here; install them from upstream.
- **Distilled** — a useful technique with no shippable skill. Documented as prose
  in a cluster file (such as `../skills/rag-cag.md`), never as a `/slash` link.

## Routing rules

- Route to a skill **only when it genuinely helps** the task.
- Use a skill **only if it exists** in the catalog, or is clearly marked
  unresolved there.
- **Do not invent skill names.** If a name is unknown, treat it as unresolved.
- **Do not link unresolved names.** A mismatch (wrong name) or a missing skill is
  documented, not linked, until the real name is confirmed.

## How to read the catalog

`SKILLS.md` tags each skill with a provenance marker:

- `AUTH-G` — owner-authored, generic; a bundle candidate after audit.
- `AUTH-P` — owner-authored but project-coupled; never bundled raw.
- `3P` — third-party; reference only.
- `MISMATCH` / `PHANTOM` — unresolved; resolve before linking.

Catalog clusters: core workflow, RAG/CAG, QA/debug, and security. (This kit has no
research or science cluster.)

## What never enters the kit

- No third-party skill body — reference by name only.
- No proprietary or project-coupled (`AUTH-P`) skill.
- No invented or unresolved `/slash` link presented as if it works.

## Related project files

- `../skills/SKILLS.md` — the skill catalog and provenance legend.
- `01-conductor-doctrine.md` — when and how the conductor routes.
- `07-safety-and-scrub.md` — the never-bundle and scrub rules.

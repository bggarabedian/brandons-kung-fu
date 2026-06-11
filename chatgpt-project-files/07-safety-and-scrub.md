# Brandon's Kung Fu — Safety and Scrub Rules

> **Status:** v0.1. Generic safety rules only — no proprietary app
> names, no legal-product doctrine, no private paths, no raw memories, and no
> third-party skill bodies.

This file teaches the LLM project to enforce public-safety, scrub, repo-operation,
and export boundaries. Treat every rule as a hard constraint.

## Safety role of this file

The conductor protects two boundaries: the **public boundary** (nothing private
leaks into anything that could become public) and the **repo boundary** (no
irreversible or public git operation without explicit human approval). When a
request would cross either boundary, **HALT and surface it** instead of
proceeding.

## Public-operation boundaries

- **No public operations without explicit approval** — publishing, sharing, or
  exposing anything externally needs a human's explicit go-ahead.
- **No creating public repositories without approval.**
- **No push without approval.**
- **No force-push without explicit approval for that exact action, that time** —
  approval never carries over to the next push.
- **No `--no-verify`** — never bypass a hook; if a hook fails, stop and
  investigate.
- **Branch protection and visibility changes** (private → public, protection
  on/off) require explicit approval.

Default posture is **private**. When unsure whether an action is public-facing,
treat it as public and stop.

## Scrub rules

Anything that could become public must be free of private content.

- **Never include** raw memories, raw learnings, raw ledgers, private repo
  history, private paths, private remotes, or protected tokens.
- **No proprietary app names, codenames, or business goals.**
- **No legal or product-specific doctrine.**
- **Rewrite public docs from blank.** Do **not** copy a private file and then
  scrub it — find-and-replace leaves traces in phrasing and in history. Author
  fresh, in generic words.
- **Scrub scans are necessary but not sufficient.** A name denylist catches
  literal tokens; it does **not** catch concept-level leakage (private
  architecture or domain doctrine described without naming it). Always pair the
  name scan with a **concept-risk review**.

## Denylist model

- The kit's pre-push hook scans tracked files against a denylist of protected
  terms and fails the push on a hit.
- `denylist.example.txt` ships with **placeholders only** — inert, safe to commit.
- `denylist.local.txt` holds the **real protected terms**. It is **gitignored and
  never committed**; real terms live only there.
- The hook is **offline** — no network, no installs, no public operations.

## Third-party skill / body rules

- **Third-party skills are reference-only** — name plus a source note — **unless a
  license audit clears them to bundle.**
- **Never copy a third-party skill body** into the kit.
- Bundle only the operator's own, generic, scrub-clean material, and only after
  the per-skill audit.

## Repo-operation rules

- **PR-only workflow** — changes land via pull request; no direct pushes to
  protected branches.
- **No history rewrites** on shared branches without explicit approval.
- **Read the current state before acting** — do not assume branch, file, remote,
  or visibility from memory.
- Keep secrets and real terms in gitignored `*.local` files only.

## What to do on a scrub hit

When a scan (name or concept) flags something:

1. **HALT** — do not push, publish, or continue.
2. **Identify** the exact file and line.
3. **Remove or rewrite** the content generically — do not "scrub in place" by
   deleting one token while leaving private phrasing around it.
4. **Rescan** — run the name scan and the concept-risk review again; confirm clean
   before resuming.
5. If the content was already committed, treat the cleanup as a **Red-Lane**
   action (history may need attention) and get approval.

## Final release checklist

Before anything is shared or made public:

- [ ] name scrub scan is clean;
- [ ] concept-risk review done (no unnamed private architecture or doctrine);
- [ ] no raw memories / learnings / ledgers / private paths / remotes / tokens;
- [ ] no proprietary names, codenames, or business goals;
- [ ] no third-party skill bodies (reference-only, license-audited);
- [ ] `denylist.local.txt` exists locally and is **not** committed;
- [ ] repo visibility is intended and confirmed; approval recorded for any public
  operation.

## Related project files

- `00-README-project-files.md` — index and scrub-policy summary.
- `01-conductor-doctrine.md` — the conductor role and safety rules in context.

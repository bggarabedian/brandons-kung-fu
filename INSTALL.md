# Installing Brandon's Kung Fu

Brandon's Kung Fu is **operating doctrine**, not an app. "Installing" means making
its doctrine available to your tools: as **ChatGPT Project Files** (the conductor)
and as **Claude Code context** (the local hands). One manifest
(`kungfu.manifest.json`) is the shared source of truth, so both come from the same
files.

> **Safety first.** Every command is **dry-run by default**. Nothing is written
> outside the repo, and no `git pull` runs, without `--apply`. The tool never
> installs packages, never edits shell profiles, never overwrites your files
> silently, and never touches GStack.

## Prerequisites

- Python 3 (standard library only — no pip installs).
- Git (for `update`).
- Optional: a GStack-style slash-skill pack for the operating layer. It is
  **referenced only** — never installed or copied by this kit.

## See what the kit is (no changes)

```
python scripts/kungfu.py describe
python scripts/kungfu.py doctor
```

`describe` prints the kit, its files, and what each does. `doctor` verifies
repo/file readiness and reports whether GStack appears present — it changes
nothing.

## Set up the ChatGPT conductor

```
python scripts/kungfu.py setup-chatgpt --dry-run   # prints the plan
python scripts/kungfu.py setup-chatgpt --apply     # writes dist/chatgpt-project/
python scripts/kungfu.py doctor-chatgpt            # verify the package
```

`--apply` generates `dist/chatgpt-project/` (gitignored) with the files to upload,
the Project Instructions text, the upload order, and plain-language setup/verify
docs. **It does not log into or upload to ChatGPT** — you upload through the
ChatGPT UI. Full walkthrough: `docs/CHATGPT_PROJECT_SETUP.md`.

A simpler flat export is also available:

```
python scripts/kungfu.py export-chatgpt --apply    # dist/chatgpt-project-files/
```

## Connect Claude Code

```
python scripts/kungfu.py install-claude --dry-run --target <path>
python scripts/kungfu.py install-claude --apply   --target <path>
```

This copies the kit's context files into `<path>/brandons-kung-fu/`. Pick a path
under your own Claude context/skills directory; the target is **printed before
anything is written**. An existing file that differs is **never overwritten
silently** — the tool HALTs, or, with `--allow-backup`, keeps a timestamped `.bak`
first. Details: `docs/CLAUDE_CODE_SETUP.md`.

## Companion skill stack (GStack + others)

Brandon's Kung Fu works as doctrine alone, but reaches full power with its
companion skill stack. GStack is one companion among several — all referenced,
never vendored.

```
python scripts/kungfu.py skills list                  # declared companions
python scripts/kungfu.py skills doctor                # present / missing / needs-review + body-leak guard
python scripts/kungfu.py skills bootstrap --dry-run   # exactly what WOULD be cloned, and where
python scripts/kungfu.py skills bootstrap --apply     # only eligible (verified) entries, only if you approve
```

Out of the box the public `skills.sources.json` marks every entry `needs-review`
with no URL, so `bootstrap` clones **nothing** until you verify sources and add
them (with a real public https upstream + license) to the gitignored
`skills.sources.local.json` (start from `skills.sources.local.example.json`).
Generate a candidate local list from your machine with
`python scripts/kungfu.py skills export-local-inventory --dry-run`. Full details:
`docs/SKILL_STACK_SETUP.md`, `docs/COMPANION_REPOS.md`, `docs/GSTACK_AND_SKILL_REPOS.md`.

## Verify both sides share one source

```
python scripts/kungfu.py sync
```

Confirms the ChatGPT upload set and the Claude context set both derive from the
manifest. See `docs/SAME_SYSTEM_SYNC.md`.

## What does NOT get installed

- **GStack** — referenced only; this kit never installs, updates, or copies it.
- **No packages**, no global tools, no shell-profile changes, no background jobs.
- **No third-party skill bodies** are ever copied — command names and rules only.

## What requires explicit approval

The GStack **RED** commands (anything that writes tracked files, commits, pushes,
merges, deploys, drives a browser, imports sessions, installs, or changes local
tool state) need per-task approval. The lists live in `kungfu.manifest.json` and
`chatgpt-project-files/06-skills-and-routing.md`.

## Uninstall / remove generated files

Everything this tool generates lives under `dist/` (gitignored). Remove it with:

```
rm -rf dist/chatgpt-project dist/chatgpt-project-files
```

A Claude install lives at `<path>/brandons-kung-fu/` — delete that folder to
remove it. Nothing else on your system was changed.

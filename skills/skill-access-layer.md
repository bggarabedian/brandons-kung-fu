# Brandon's Kung Fu — Skill Access Layer

> **Status:** v0.1. Generic guidance only — no third-party skill bodies, no
> proprietary names, no private paths, no raw memories. Catalog and metadata,
> never copied bodies.

This file explains how to find, reference, and (later) install skills safely
without breaking the two things that keep this kit shippable: **scrub-clean**
(no private content leaks) and **license-safe** (no third-party body ships
without a cleared license).

## Catalog vs. bundled skill body

- **Catalog entry** — a name, a provenance tag, and metadata. It tells you a
  skill *exists* and where it comes from. The catalog lives in
  [`SKILLS.md`](SKILLS.md); machine-readable metadata lives in
  [`skills-manifest.yaml`](skills-manifest.yaml).
- **Bundled body** — the actual skill file shipped inside this repo. A body
  ships **only** when it is owner-authored, generic, and has passed a per-skill
  scrub + license audit. Until then there is no body — just a catalog entry.

A manifest row is metadata, **not** proof a body is bundled here or installed on
your machine. Empty `source_url` and `install_status: reference` are the normal,
safe defaults.

## Public repo vs. local install

- **Public repo** (this repo) — carries catalog, provenance, metadata, doctrine,
  and (eventually) owner-authored generic bodies. It must never carry third-party
  bodies, project-coupled bodies, private paths, memories, or ledgers.
- **Local install** — skills you install for your own use live in your agent
  runtime's skill directory (a user-global `.claude/skills/` or a project-local
  `.claude/skills/`). Installing is a private action on your machine; it does not
  put anything into this public repo.

Keep the two separate. The public repo describes; your local install runs.

## Provenance labels

The manifest mirrors the `SKILLS.md` provenance tags (SKILLS.md is canonical):

| Tag | Meaning | Can it ship a body here? |
|---|---|---|
| `AUTH-G` | owner-authored, generic | Yes — after scrub + license audit |
| `AUTH-P` | owner-authored, project-coupled | **Never raw** |
| `3P` | third-party | **Never** — reference by name only |
| `MISMATCH` / `PHANTOM` | unresolved name | No — resolve first, never link live |
| `AUTHOR-NEW` | planned owner skill | No body yet — prose pattern until built |

## Why third-party bodies are reference-only

A third-party skill carries its author's license. Copying its body into this repo
re-publishes their work under this repo's distribution, which can violate that
license. So `3P` skills are listed by name with a source note and installed from
their own upstream — never copied here. A body moves off reference-only **only**
after a license audit confirms the license permits redistribution and the result
is recorded in the manifest (`license_status: cleared`).

## Why private Gstack / memory stays local

Conductor systems like Gstack carry project-coupled config, local memory stores,
and learnings that are specific to one operator. Those are `AUTH-P` or private:
never bundled, never copied into this repo. Only the **generic doctrine** they
embody (lanes, HALT, verify-before-claim) is distilled as fresh prose in the
project files. The distinction: ship the idea, never the operator's data.

## How to add source URLs safely

- Leave `source_url: ""` until you have verified a **public** source.
- A `source_url` must be a public URL (a public code-host or docs page). **Never**
  put a private remote, an internal host, or a local filesystem path in this
  field.
- An empty `source_url` is correct and safe. A guessed or private URL is a defect
  — it can leak structure and it points users at something they cannot reach.
- When you do add a URL, also fill `license` and move `license_status` toward
  `cleared` only after the audit below.

## License / provenance audit checklist

Before changing any entry to `license_status: cleared` or `bundle_status:
bundled`:

- [ ] Provenance confirmed (`AUTH-G` for bundling; `3P`/`AUTH-P` cannot bundle).
- [ ] Source identified and public; `source_url` set to that public URL.
- [ ] License identified by SPDX id and recorded in `license`.
- [ ] License permits redistribution under this repo's terms.
- [ ] No private names, paths, memories, or secrets in the body.
- [ ] Body is written fresh-from-blank if owner-authored — never derived from a
      private file by find-and-replace.
- [ ] Result recorded in both `skills-manifest.yaml` and `SKILLS.md`.

If any box fails, the skill stays reference-only.

## Duplicate local / global skill shadowing

A skill or command name can resolve from more than one scope — typically a
project-local skill directory and a user-global one. If both define the same
name, one **shadows** the other and the stale copy may win. Symptoms: a skill
behaves unlike the version you just edited.

- Before installing a skill, check **both** scopes for that name.
- Keep exactly one copy of each name. Precedence is runtime-specific — do not
  rely on which scope wins.
- On rename or removal, clear the old name from both scopes.

(Same rule as command templates — see `../chatgpt-project-files/11-command-templates.md`.)

## Installed-skill smoke-test checklist

After you install a skill locally, confirm all of:

- **Loads** — the runtime lists it and `/name` resolves without error.
- **One scope** — the name does not also exist in the other scope (no shadow).
- **Does what it claims** — run it once on a safe target and verify the described
  behavior, not just that it starts.
- **No surprise writes** — it writes only what it documents; check your repo's
  status shows no unexpected tracked changes.
- **No private leakage** — its output contains no private paths or names.

## Future dry-run fetcher (design only — no code here)

A later PR may add an importer that reads `skills-manifest.yaml` and helps install
skills. Its design constraints, fixed now so the build is bounded:

- **Dry-run by default.** With no apply flag it performs **no** network calls and
  **no** installs — it only prints what it *would* fetch and install.
- **Reports gaps.** Missing `source_url`, missing `license`, or
  `license_status` not `cleared` are reported, not silently skipped.
- **Shadow pre-check.** It checks both skill scopes for name collisions before
  proposing an install.
- **Hard refusals.** It refuses `AUTH-P`, refuses any entry whose license is not
  `cleared`, refuses an empty/private `source_url`, and refuses to overwrite an
  existing skill without an explicit force plus a second confirmation.
- **Never** installs into this repo or any shared path, and **never** reads or
  copies local memory stores.

## Rule — no fetch or install without explicit apply approval

**No downloader or importer in this kit may fetch from the network or install a
skill unless the user explicitly runs it with an apply flag and confirms.** The
default for any such tool is dry-run, offline, no side effects. This matches the
kit's offline installer posture: no network, no installs, no surprises.

## Related files

- [`SKILLS.md`](SKILLS.md) — canonical catalog and provenance legend.
- [`skills-manifest.yaml`](skills-manifest.yaml) — additive source/license metadata.
- `../chatgpt-project-files/06-skills-and-routing.md` — routing model.
- `../chatgpt-project-files/07-safety-and-scrub.md` — never-bundle and scrub rules.
- `../chatgpt-project-files/11-command-templates.md` — command shadowing + smoke tests.

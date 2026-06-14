# Companion repositories

A "companion repo" is an external skill/command/docs source that augments the
Brandon's Kung Fu doctrine. They are **referenced**, not vendored: this kit never
copies their bodies.

## The manifest

`skills.sources.json` declares each companion. Fields:

| Field | Meaning |
|---|---|
| `id` | stable short id |
| `name` | human name |
| `type` | `gstack` / `claude-skill-pack` / `command-pack` / `docs-pack` / `local-overlay` / `unknown` |
| `priority` | `required` / `recommended` / `optional` |
| `upstream_url` | public https URL, or `""` until verified |
| `pinned_ref` / `version` | a commit/tag to pin, when known |
| `license` | SPDX id once verified |
| `provenance_status` | `verified` / `needs-review` / `local-only` / `forbidden-public` |
| `install_mode` | `clone` / `copy-from-existing` / `manual` / `unsupported` |
| `default_target` | where it installs (placeholder until you set a real path) |
| `contains_third_party_bodies` | true/false/unknown |
| `bundle_policy` | `reference-only` / `owner-authored-bundle-ok` / `local-only` |
| `safe_commands` / `red_commands` | the safe-vs-approval command split for that pack |
| `notes` | free text |

## Eligibility for `bootstrap --apply`

A companion is auto-clonable **only** when **all** hold:

- `provenance_status: verified`
- `install_mode: clone`
- `upstream_url` is a **public https** URL (github.com / gitlab.com / codeberg.org / bitbucket.org)
- `default_target` is a real path (not a `<placeholder>`)

Anything else is **refused** with a printed reason. This is why the shipped public
manifest — every entry `needs-review` with an empty URL — clones nothing until you
verify sources yourself.

## Honesty rules

- **No invented repos, no hallucinated URLs.** A URL appears only after you verify
  it. Entries referenced from operator config are recorded by `id` with an empty
  URL and `needs-review` until confirmed.
- **No private repos in the public manifest.** Private/local-only sources live only
  in the gitignored `skills.sources.local.json`.
- **No scraping, no browser automation, no cookies/sessions.** Bootstrap is
  `git clone` of files; it runs no post-install scripts.

## Adding a companion you trust

1. Copy `skills.sources.local.example.json` → `skills.sources.local.json` (gitignored).
2. Add the source with the real public https `upstream_url`, a `pinned_ref`, the
   `license`, `provenance_status: verified`, `install_mode: clone`, and a real
   `default_target`.
3. `python scripts/kungfu.py skills bootstrap --dry-run` to see the plan.
4. `--apply` only when you are satisfied.

# Skill-stack setup

Brandon's Kung Fu works as **doctrine alone**, but it reaches full power with its
**companion skill stack** — GStack plus whatever other skill repositories you have
verified and chosen. This kit can describe, detect, and (with your explicit
approval) bootstrap that stack. It never bundles third-party bodies and never
clones anything you have not verified.

## The safe sequence

```
python scripts/kungfu.py skills list                  # what companions are declared
python scripts/kungfu.py skills doctor                # what's present / missing / needs review
python scripts/kungfu.py skills bootstrap --dry-run   # exactly what WOULD be cloned and where
# inspect the plan, verify licenses/upstreams
python scripts/kungfu.py skills bootstrap --apply     # only if you approve, and only eligible entries
```

**Dry-run is the default.** `bootstrap --apply` clones **only** entries that are
`provenance_status: verified`, `install_mode: clone`, with a **public https**
`upstream_url` and a real `default_target`. Out of the box every public entry is
`needs-review`, so `bootstrap` is **inert** until you verify and configure sources
yourself. Nothing logs in, scrapes, uses a browser, or runs post-install scripts —
bootstrap fetches files, it does not execute untrusted code.

## Public vs. local manifests

- **`skills.sources.json`** (committed, public) — only public, license-reviewable,
  reference-safe sources. URLs are filled in only when verified.
- **`skills.sources.local.json`** (gitignored) — your full collected list,
  including local-only paths and private repos. Start from
  `skills.sources.local.example.json`. The CLI merges local over public by `id`.
- **`skills export-local-inventory`** scans your known skill directories and writes
  a candidate `skills.sources.local.json` (gitignored). Private paths only ever go
  into that gitignored file — never into the public manifest or docs.

## Updating companions

```
python scripts/kungfu.py skills update --dry-run   # branch/commit/upstream/dirty/ff-possible per installed repo
python scripts/kungfu.py skills update --apply     # clean tree required; fetch + fast-forward only
```

`update --apply` refuses merge/rebase/force and skips dirty repos. See
`docs/COMPANION_REPOS.md` and `docs/GSTACK_AND_SKILL_REPOS.md`.

## Rules

- GStack is **one** companion, not the whole universe.
- Third-party skills are fetched from **upstream**, never copied into this repo.
- A skill body is bundled here only if it is owner-authored, generic, scrub-clean,
  and license/provenance audited.
- **You** approve every install and update. The CLI only ever reports a plan until
  you pass `--apply`.

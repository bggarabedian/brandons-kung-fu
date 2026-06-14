# GStack and the wider skill stack

GStack is an important companion, but it is **one** skill pack among several — not
the whole universe. Brandon's Kung Fu treats the entire companion stack the same
way: referenced, license-aware, user-approved, never vendored.

## Where GStack fits

- GStack is the **default operating layer** when installed: context, planning,
  health, review, QA-only, security review, memory, and closeout.
- It is **reference-only** — command names and operating rules, never copied bodies.
- It carries its own safe-vs-RED command split (see its entry in
  `skills.sources.json` and `06-skills-and-routing.md`).
- This kit **never** installs, updates, copies, or modifies GStack. `skills doctor`
  only **reports** whether it is present.

## The rest of the stack

Other skill repositories (claude-skill-packs, command-packs, docs-packs, and your
own local overlays) are declared in the same manifest with the same fields and the
same eligibility rules. Some may be `required` or `recommended`; most start
`optional` and `needs-review` until you verify their upstream and license.

## Why it is handled this way

- **One verification model.** Every companion — GStack included — must pass the
  same `verified` + `clone` + public-https + real-target gate before
  `bootstrap --apply` will touch it.
- **No special-casing.** GStack does not get an exemption from license/provenance
  review, and nothing about it is bundled.
- **Your collection stays yours.** Your full, machine-specific list of skill repos
  lives only in the gitignored `skills.sources.local.json`; generate a starting
  point with `skills export-local-inventory`.

## Quick reference

```
python scripts/kungfu.py skills list      # all companions incl. GStack
python scripts/kungfu.py skills doctor    # presence + provenance + body-leak guard
python scripts/kungfu.py skills bootstrap --dry-run   # plan only (inert until you verify sources)
```

See `docs/COMPANION_REPOS.md` for the manifest schema and `docs/SKILL_STACK_SETUP.md`
for the full setup flow.

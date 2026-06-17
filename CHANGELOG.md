# Changelog

All notable changes to Brandon's Kung Fu. This project is **pre-1.0**: the public
install/update contract is not yet stable, and no GitHub release is tagged yet.

## v0.3.2-alpha.1 — pending PR (unreleased)

The first **Cockpit Bridge** slice: a read-only `cockpit doctor` check that
verifies a private vault is wired safely, without ever reading a note body. The
example config and the check are additive; write commands come later (no version
bump — alpha, code-additive only).

- Add `cockpit doctor` (read-only) to `scripts/kungfu.py` — checks that a local
  `cockpit.local.json` resolves, the vault lives **outside** this repo and outside
  any other git work tree, the required folders exist, and that neither
  `.obsidian/` nor the local config nor any vault note is tracked by git. It never
  reads a note body; it reports problems and exits non-zero, clean exits zero, and
  hard-fails (exit 2) when no usable config is present.
- Add `cockpit.local.example.json` — an inert template with a `<placeholder>`
  vault path. The real `cockpit.local.json` is git-ignored, so a private vault
  path is never committed.
- `.gitignore`: ignore `cockpit.local.json`, keep the example tracked.
- Add stdlib `unittest` coverage (config loader + doctor safety checks, including
  a guard that a vault note body is never read or printed) — no third-party test
  dependencies.
- No write commands yet: `cockpit init` / `mirror` / `handoff` / `open` are not in
  this slice. `cockpit --help` exposes `doctor` only.
- Boundaries unchanged: nothing is installed, no plugin is enabled, no `.obsidian/`
  config is tracked, and no vault content ships.

## v0.3.1-alpha.2 — pending PR (unreleased)

Public GitHub community-standards surface (no version bump; docs/governance only).

- Add `CODE_OF_CONDUCT.md` — short, practical, authored fresh (no third-party body):
  expected behavior, unacceptable behavior, enforcement, and public-channel
  reporting.
- Add `CONTRIBUTING.md` — who the repo is for, contribution shape (issues + scoped
  PRs), the no-private-leakage / no-third-party-bodies / no-Co-Authored-By /
  no-force-push / no-`--no-verify` rules, lanes in plain terms, and the verification
  + scrub gates to run before opening a PR.
- Add `SECURITY.md` — supported versions (`0.3.x`, pre-1.0 caveat), how to report a
  vulnerability (prefer GitHub private reporting; otherwise a minimal public issue
  asking for a private channel, no exploit details), and a no-SLA-overclaim response
  note.
- Add GitHub issue forms under `.github/ISSUE_TEMPLATE/` — `bug_report.yml`,
  `docs_improvement.yml`, `setup_help.yml`, and `config.yml` (blank issues off;
  contact links to the setup guide and contributing docs).
- Add `.github/PULL_REQUEST_TEMPLATE.md` — lane + scope + files + verification +
  scrub/concept-risk checklist (no private content, no `.obsidian/`, no third-party
  bodies, no Co-Authored-By, no `--no-verify`, PR-only).
- README: add a **Community standards** section linking the above.
- Repository description set via `gh repo edit` (metadata only; topics, homepage,
  and visibility unchanged).
- Boundaries unchanged: public-safe, authored fresh from blank; no vault content, no
  `.obsidian/`, no third-party policy/skill bodies, no vendor endorsement, no
  overclaim.

## v0.3.1-alpha.1 — pending PR (unreleased)

First-run onboarding so new users can activate the kit (no version bump; docs
only).

- Add `GETTING_STARTED.md` — a GitHub-facing five-step setup guide: copy the
  project instructions, upload the spine project files (keep always-on context
  small), send the first prompts, connect the coding agent, run a smoke test, and
  avoid the common mistakes.
- Add `FIRST_PROMPT.md` — the canonical first ChatGPT conductor prompt (compact +
  full): operate as conductor, lane-first, the five-part review shape, the handoff
  labels, ceremony-matches-size, scrub + concept-risk, no repo-fact invention.
- Add `docs/CLAUDE_CODE_FIRST_PROMPT.md` — the canonical first Claude Code prompt
  (local implementation IC: verify repo truth first, no edits until scope is clear,
  lane discipline, command evidence, no push/merge/force-push/install/--no-verify
  without authorization, no Co-Authored-By, placeholders not private paths) plus a
  read-only smoke-test prompt.
- README: add a top-of-page **Start here** section linking the three onboarding
  docs.
- Boundaries unchanged: public-safe, placeholders only; no vault content, no
  `.obsidian/`, no third-party skill bodies, no vendor endorsement, no overclaim.

## v0.3.0

The optional **Obsidian Cockpit Layer**: doctrine and templates for a
private, core-plugin-only notes vault used as **private continuity** — a workstream
map, a decision record, and the staging area for scrubbed agent handoff cards. The
repos and session ledgers stay the source of truth; the cockpit only organizes
private continuity around them. Additive and doctrine-only — no plugins are
installed or enabled, no `.obsidian/` config is tracked, and no vault content ships.

- Add `docs/OBSIDIAN_COCKPIT.md` — public-safe overview: what the cockpit is and
  is not, a core-plugin-only layout (placeholders), safe-use rules, and when to
  use / not use it.
- Add `chatgpt-project-files/12-obsidian-cockpit.md` — conductor-facing doctrine:
  where it fits in the loop, the vault-privacy rule, the public/private boundary,
  the handoff-card rule, the concept-risk-review rule, and placeholder-only note
  skeletons.
- Wire the layer into the existing doctrine: `00-README-project-files.md` (file
  list + upload order), `07-safety-and-scrub.md` (vault scrub rules + release-
  checklist line), `08-daily-workflow.md` (optional cockpit touch point at
  close), `10-learn-and-update-loop.md` (which lessons may be mirrored privately
  vs. graduated publicly), `11-command-templates.md` (four placeholder-only
  cockpit card patterns + the `<COCKPIT_VAULT>` placeholder), and
  `PROJECT-INSTRUCTIONS.md` (a compact cockpit block).
- `.gitignore`: guard `.obsidian/` and a generic local `cockpit-vault/` so vault
  config and notes can never be tracked from a working copy.
- Manifest: add `11-command-templates.md` and `12-obsidian-cockpit.md` to the
  `kungfu.manifest.json` ChatGPT `upload_order` so `describe`, `export-chatgpt`,
  and `setup-chatgpt` package the full optional/advanced set.
- README: add a short, public-safe feature section for the optional layer, plus a
  beginner-facing **"Why use this (for AI-agent coders)"** section — the risk-lane
  / task-box / verify-with-commands / PR-first loop and what it improves (no
  overclaim, no vendor endorsement).
- Boundaries unchanged: vault is private, lives outside the repo; public docs are
  authored fresh from blank (never copy-and-scrub); a name scan is paired with a
  concept-risk review; no third-party plugin bodies are copied.

## v0.2.0 — pending PR (unreleased)

The installable / exportable distributable kit. v0.1 was the manual project-file
version; v0.2.0 adds automation so a downloader can set up ChatGPT (the conductor)
and Claude Code (the local hands) from the same source.

- Add `kungfu.manifest.json` — one manifest as the shared source of truth for the
  ChatGPT and Claude Code exports.
- Add `scripts/kungfu.py` (Python standard library only): `describe`, `doctor`,
  `doctor-chatgpt`, `export-chatgpt`, `setup-chatgpt`, `install-claude`, `update`,
  `sync`. Thin `scripts/kungfu.sh` / `scripts/kungfu.ps1` wrappers (call Python only).
- Add ChatGPT Project setup: `setup-chatgpt` generates an upload-ready package
  under `dist/chatgpt-project/` (README_UPLOAD_FIRST, PROJECT-INSTRUCTIONS.txt,
  files/, UPLOAD_ORDER, WHY_CHATGPT, VERIFY_SETUP, MANIFEST). The CLI does not
  automate ChatGPT login or upload — manual upload is the supported path.
- Add Claude Code setup path: `install-claude --target <path>` copies the
  doctrine into a namespaced `<path>/brandons-kung-fu/`.
- Add a safe update flow: `update --dry-run` report + `update --apply`
  fast-forward only (clean tree required; refuses merge/rebase/force/dirty).
- Add `sync` to verify both exports derive from the same manifest.
- All write/install/update behavior is explicit and **dry-run by default**;
  writes outside the repo and any `git pull` require `--apply`. No silent installs.
- GStack stays **reference-only**: command names and operating rules, never bodies.
- Docs: `INSTALL.md`, `UPDATE.md`, `docs/CHATGPT_PROJECT_SETUP.md`,
  `docs/CLAUDE_CODE_SETUP.md`, `docs/WHY_CHATGPT_AND_CLAUDE.md`,
  `docs/SAME_SYSTEM_SYNC.md`.

## v0.1.0

Initial manual project-file doctrine kit: ChatGPT project files (conductor
doctrine, coding standards, driving coding agents, skills & routing, safety &
scrub, RAG/CAG, QA & debug, daily workflow, Codex & agent tooling), the offline
pre-push denylist scanner + installers, and the skill manifest.

Later in the v0.1 line: **GStack Native Mode** added to the doctrine (PR #5) — a
GStack-style slash-skill pack documented as the default operating layer, kept
reference-only (command names and rules, never bodies).

---

## Roadmap (not yet released)

- **v0.4.0** — cross-platform fresh-clone validation and real user setup feedback.
- **v1.0.0** — stable public release once the install/update contract is proven by
  external clean-clone/user testing.

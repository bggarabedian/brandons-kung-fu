# Changelog

All notable changes to Brandon's Kung Fu. This project is **pre-1.0**: the public
install/update contract is not yet stable, and no GitHub release is tagged yet.

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

- **v0.3.0** — cross-platform fresh-clone validation and real user setup feedback.
- **v1.0.0** — stable public release once the install/update contract is proven by
  external clean-clone/user testing.

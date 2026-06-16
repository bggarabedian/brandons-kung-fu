# Contributing to Brandon's Kung Fu

Thanks for helping improve the kit. This repo is **operating doctrine and docs**
for supervising AI coding agents — not a hosted service and not application code.
Contributions are mostly prose: clearer doctrine, better onboarding, fixed
examples, and small tooling improvements.

## Who this is for

People using AI coding agents (Claude Code, Codex CLI, or others) who want agent
speed without unbounded repo damage — and who want to make the doctrine clearer for
the next person.

## How to contribute

- **Open an issue** for a bug, a docs gap, or a setup problem. Use the issue
  templates — they ask for the context a maintainer needs.
- **Open a PR** for a small, scoped improvement. Keep the diff focused; one logical
  change per branch.

**Do not** include in any contribution:

- private paths, private remotes, or private repo/product names;
- raw memories, raw ledgers, raw learnings, or real Obsidian vault notes;
- `.obsidian/` config;
- third-party skill or policy bodies (reference by name only);
- `Co-Authored-By` trailers;
- a force-push to a shared branch;
- `--no-verify` to bypass a hook.

## Pick a lane (it sets how much care a change needs)

- **Green** — small, reversible docs or examples. Proceed with a focused PR.
- **Red** — doctrine, security, public posture, hooks/CI, schema, migrations, or
  anything irreversible. Discuss in an issue first; expect tighter review.
- **Inspection-only** — read, report, plan. No edits.

When unsure which lane applies, treat it as Red.

## Verify before you open the PR

Run the kit's own gates and include the results in your PR:

```
python scripts/kungfu.py doctor
python scripts/kungfu.py skills doctor
git diff --check
```

Then do the **scrub checks**: a name scan for anything private, plus a
**concept-risk review** — read your change as an outsider and confirm it reveals no
private system or decision even when no protected name appears. Public docs are
**authored fresh from blank**, never copied-and-scrubbed.

## New here?

Start with the setup path, then the activation prompts:

- [`GETTING_STARTED.md`](GETTING_STARTED.md) — the five-step first run.
- [`FIRST_PROMPT.md`](FIRST_PROMPT.md) — the canonical first ChatGPT conductor prompt.
- [`docs/CLAUDE_CODE_FIRST_PROMPT.md`](docs/CLAUDE_CODE_FIRST_PROMPT.md) — the
  canonical first Claude Code prompt.

## Workflow expectations

- **PR-only** — changes land via pull request; no direct pushes to `main`.
- **Verify, don't assert** — command evidence, not "looks right."
- **Small and reversible** — prefer the smallest change that works.

See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) and [`SECURITY.md`](SECURITY.md).

# Brandon's Kung Fu — Codex CLI and Agent Tooling (Project File)

> **Status:** v0.1. Generic project-file guidance only — no
> proprietary names, no third-party skill bodies. Tool names below name the tools
> the guidance is about.

How to use additional coding agents alongside the conductor, safely.

## Roles

- **ChatGPT project (the conductor)** — architect and auditor. Scopes, plans,
  writes tasks, reviews, and verifies. Holds doctrine, security, and
  public-posture authority.
- **Claude Code** — local implementation IC. Inspects, edits within an approved
  scope, runs tests, reports.
- **Codex CLI** — an optional alternate coding agent: a second implementation
  lane, a reviewer, or a CLI-focused builder. Use it where it fits; it does not
  change the rules.

The conductor decides *what* and *how it is verified*; the coding agent builds
inside that box.

## Install policy

- **No automatic installs.** An agent never installs tooling on its own.
- **The user explicitly approves** any install, every time.
- **Use the official OpenAI install docs** for Codex CLI — follow the current
  upstream instructions, not a hard-coded snippet.
- **After install, verify** with `codex --version` (or the documented
  equivalent) before relying on it.

## Install references (documentation only — do not execute)

Pointers, not commands to run automatically. Confirm against current official
docs; package names, taps, and installer URLs change.

```
# Reference only — require explicit user approval before running any of these.
# Standalone installer:    see the official Codex CLI install page
# npm package:             npm install -g @openai/codex
# Homebrew (macOS/Linux):  brew install codex
# Windows (PowerShell):    follow the official PowerShell install instructions
```

Treat the exact package name, tap, and installer URL as check-the-docs items —
do not assume them.

## Claude Code + Codex coexistence

- **One conductor.** A single project drives the work.
- **One active implementation lane** unless you have explicitly parallelized. Two
  agents editing the same files at once is how you corrupt a tree.
- **Agents do not decide doctrine, security, or public posture.** Those stay with
  the human and the conductor.
- **Parallel work uses separate branches or worktrees.** Give each agent its own
  isolated lane, then integrate through review.

## Model and tool selection

- **Use the best available model or tool when it improves total speed, quality,
  reasoning, review, or safety.** For serious engineering, default to
  **frontier / high-capability models**.
- **Do not artificially downshift** from a high-capability model for real
  engineering work. Bad cheap output is expensive when it causes rework.
- **Faster/cheaper models are an optional optimization** for boilerplate and
  low-risk repetition — allowed, never a mandatory default.
- **Do not hard-code model names.** Available options depend on the current tool
  version, configuration, and account — verify them from your tool's output or
  official docs.

## Safety rules (same as the rest of the kit)

- **Green Lane** for bounded, reversible work; **Red Lane** for architecture,
  security, public posture, irreversible operations, hooks/CI, schema, migrations,
  doctrine, and anomalies.
- **HALT** on anomalies, failed gates, scope drift, or any security /
  public-posture concern.
- **No `--no-verify`.** **No force-push** without explicit, per-time approval.
- **PR-only workflow.** Run the scrub scans before any public release.

## `/cli-anything` (future pattern)

A planned pattern for turning a repeated workflow into a small, typed CLI tool —
so a routine you run by hand becomes one reliable command. It is a **v0.2
candidate**, noted as a prose pattern in `../skills/SKILLS.md`; **not a v0.1
blocker** and not a bundled skill yet.

## Related project files

- `01-conductor-doctrine.md` — the conductor role, lanes, HALT.
- `03-driving-coding-agents.md` — the task template and prompt patterns.
- `07-safety-and-scrub.md` — public-operation and scrub boundaries.

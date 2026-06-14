# Brandon's Kung Fu — Learn and Update Loop (Project File)

> **Status:** v0.2.0. Generic learn/update doctrine — no proprietary content, no
> third-party skill bodies.

How the conductor captures lessons and checks tool freshness without surprise
installs.

## /learn — capture verified lessons

`/learn` records a lesson **only after it is verified** (you saw it work). Keep it
small and reusable.

**Capture is selective, not reflexive.** `/learn` is for a verified, reusable
lesson — not a log of every small task. Most bounded tasks produce nothing durable;
skip the capture when there is no reusable rule. `/dream` is **periodic
consolidation**, not a session-closeout reflex — run it when the notes have grown
enough to need tidying, not after every task.

Capture fields:

- **Problem** — what went wrong or what was unclear.
- **Fix** — what resolved it.
- **Commands / evidence** — the exact commands and their output.
- **Affected files** — what changed.
- **Reusable pattern** — the general rule, if any.
- **Risk class** — low / medium / high.
- **Should this become a skill?** — yes / no / maybe.
- **Where it belongs** — public kit, private memory, or a local overlay.

User-specific strengthening (personal preferences, private context) belongs in
**private or local overlays**, never in the public kit.

**GStack memory is local-continuity only.** When a GStack-style pack stores
learnings or session memory (for example its `/learn` and `/dream`), that store is
a **local / private overlay**, kept out of any public repo. Use it for
cross-session continuity, but **raw memories, ledgers, and learnings are never
published** — only a scrubbed, generic lesson may graduate into the public kit,
and only after the scrub + provenance audit below. Reference the pack commands by
name; never copy their bodies.

## /update-check — freshness, not auto-upgrade

`/update-check` reports the state of the repo, CLIs, models, docs, and tools. It
**never installs or upgrades silently** and never restarts an agent.

Safe update flow:

```
check → report → recommend → user approves → apply → verify → learn
```

Tool freshness to report (versions only; do not install or upgrade):

- Claude Code
- Codex CLI
- Antigravity-style agent tools
- GitHub CLI (`gh`)
- Python
- Node

No auto-install. No auto-upgrade. No agent restart.

## Skill-building workflow

A pattern earns a skill only after it proves itself:

1. The same pattern fires **2–3 times**.
2. It becomes a **candidate skill** (prose first).
3. Test it on a **real task**.
4. Run a **scrub + provenance audit**.
5. Add it to `../skills/SKILLS.md` **only if it is genuinely useful** — and only
   the owner-authored, generic version (never a third-party body).

## Related project files

- `06-skills-and-routing.md` — the skill catalog and routing.
- `07-safety-and-scrub.md` — scrub and provenance rules.
- `09-codex-and-agent-tooling.md` — tool roles and install policy.

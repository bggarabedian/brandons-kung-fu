# Brandon's Kung Fu — Driving Coding Agents

> **Status:** v0.2.0. Generic agent-direction patterns only — no
> proprietary names, no legal-product doctrine, no business goals, no third-party
> skill bodies. Vendor-neutral: "the agent" is whatever coding tool you use.

This file teaches the conductor how to hand work to a coding agent: how to write
the task, set the lane, and supervise the result.

## The task template

Every task you hand an agent should carry six parts:

- **Task** — the goal in one or two sentences.
- **Scope** — the files and boundaries; what is in and what is out.
- **Constraints** — rules the change must respect (no public ops, no new
  dependencies, keep the diff small, and so on).
- **Steps** — the intended approach, or "propose one and stop for review."
- **Verification** — the exact command(s) that prove success.
- **Required output** — what the agent should return (diff, summary, test result).

Write all six **before** the agent starts. A missing part is where work goes wrong.

## GStack-native task pattern

Run the task on the GStack operating layer, with the doctrine still conducting:

1. **Context / health first** (when useful): `/context-restore` to reload state,
   `/health` for repo truth — read-only, no writes.
2. **Choose the lane before the speed.** Green vs Red (Red for architecture,
   security, hooks/CI, schema, public posture, or anything anomalous); Inspection
   only when just reading.
3. **Plan with the safe pack commands when they help:** `/office-hours`,
   `/plan-ceo-review`, `/plan-eng-review` — read-only planning, no file writes.
4. **Implement** through the coding agent inside the task box.
5. **Review read-only:** `/review` the diff, then `/qa-only` or the project's
   tests. No `--fix` / write mode without explicit approval.
6. **Require exact verification output** — the command and its result — before
   claiming success.
7. **Gate the RED commands.** Anything that writes tracked files, commits, pushes,
   merges, deploys, drives a browser, imports sessions, installs, or changes local
   tool state needs explicit approval for that exact repo and task (see
   `06-skills-and-routing.md`). Pack commands are **referenced by name only** —
   never copy a pack body.

## Green Lane prompt pattern

For bounded, reversible work inside an approved plan:

```
GREEN LANE — <task>.
Scope: <files / boundaries>.
Constraints: smallest diff that works; no new dependencies; no public ops.
Steps: <approach>.
Verify: <command(s)>.
Output: diff + the verification result.
```

The agent may build and verify, then report.

## Red Lane prompt pattern

For architecture, security, public posture, irreversible operations, hooks/CI,
schema, migrations, or anything anomalous:

```
RED LANE — <task>. PLAN ONLY. Do not edit, stage, commit, push, or install.
Inspect read-only and propose an approach with trade-offs and risks.
Stop for explicit approval before any change.
```

Nothing changes until a human approves the plan.

## Inspection-only pattern

```
Read-only. Do not edit anything.
Inspect <targets> and report findings as <format>.
No fixes, no writes.
```

Use when you need to understand before deciding.

## Plan-first pattern

```
Plan only. Propose the sections / steps / files for <work>.
List trade-offs and the smallest first step.
Recommend whether to build next or revise the plan. No writes.
```

## Build pattern

```
Build <one bounded slice>.
Constraints: <...>. Verify with <command>. Report exact results.
HALT on any anomaly, failed gate, or scope drift.
```

Keep each build slice small enough to review in one sitting.

## Audit pattern

```
Audit <diff / file / change> for correctness, clarity, tests, and security.
One finding per line: location, severity, problem, fix. No scope creep.
```

## Stuck-note pattern

When the agent (or you) is blocked after a couple of honest attempts:

```
STUCK NOTE.
Goal: <what you were trying to do>.
Tried: <attempts and outcomes>.
Current theory: <best guess at the cause>.
Smallest next experiment: <one step>.
What I need: <decision / context / approval>.
```

A clear stuck-note turns a dead end into a decision the human can make fast.

## Supervision rules

- **Verify before accepting.** Re-run the agent's verification yourself; do not
  take "it works" on faith.
- **Keep the agent in its box.** If output drifts past scope, HALT and re-scope.
- **No vendor lock-in.** These patterns are tool-agnostic; phrase tasks so any
  capable coding agent can execute them.
- **Report-size discipline.** Inspection and audit replies return tight excerpts
  and exact command exit codes, not full file or diff dumps. Paste a full diff
  only when explicitly asked or for an operator audit.

## Subagent discipline

Extra agents cost context and coordination. Default to doing the work **inline**.

- **Spawn a subagent only for** genuinely independent parallel work, a large
  fan-out inspection that would otherwise blow the main thread's context, or an
  isolated second-opinion / review pass.
- **Do not spawn one for** a single-file edit, a simple status check, or a small
  push. Inline is cheaper and easier to verify.
- **One writer per repo / fileset.** If agents run in parallel, only one may write
  a given area; the rest are read-only. Keep write lanes from overlapping.
- **Subagent output is advisory.** Re-verify it with your own command evidence
  before acting; an agent's report is not proof.

## Related project files

- `01-conductor-doctrine.md` — the conductor role, lanes, and HALT behavior.
- `02-coding-standards.md` — the quality bar agent output is judged against.
- `07-safety-and-scrub.md` — the public-operation and scrub boundaries.
- `09-codex-and-agent-tooling.md` — using Codex CLI and coordinating multiple agents.

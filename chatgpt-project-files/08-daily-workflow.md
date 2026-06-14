# Brandon's Kung Fu — Daily Workflow (Project File)

> **Status:** v0.1. Generic daily-workflow patterns only — no
> proprietary, legal, or business context, and no third-party skill bodies.
> Vendor-neutral.

A simple loop for running a day of agent-assisted engineering. Usable as-is.

## The loop (GStack-native)

`/context-restore` → `/standup` → `/health` → task/spec → `/plan-eng-review` or
`/plan-ceo-review` (when Red-lane or 3+ files) → implementation → `/review` →
`/qa-only` (or the right tests) → `/standdown` → `/context-save` → `/learn` →
`/dream`.

These are referenced third-party command names plus operating rules — never copy
their bodies. The lane/speed choice and safety rules below apply throughout; pack
output is advisory, not a gate, and never replaces command-evidence verification.

## Start the day

- Open the session: `/context-restore` to reload working context, a `/standup`
  pattern to capture repo truth (branch, clean or dirty, last commit, remote sync,
  any open work), and `/health` for a quick repo-health read.
- Choose the lane: **Green** (bounded, reversible) or **Red** (architecture,
  security, public posture, irreversible operations, hooks/CI, schema, migrations,
  doctrine, anomalies). When unsure, treat it as Red.
- Pick the **next smallest move** that advances the goal and is easy to verify.

## Work through the day

For each unit of work:

1. **Task** — write goal, scope, constraints, steps, verification, required output.
2. **Plan** — confirm the approach and the smallest first step.
3. **Execute** — make the smallest change that works.
4. **Verify** — `/review` the diff (read-only) and run `/qa-only` or the project's
   tests; report exact command output before claiming success.
5. **HALT** — on any anomaly, failed gate, scope drift, or security / public-posture
   concern, stop and surface it instead of pushing through.

Keep changes small and reviewable.

## Close the day

- Close the session: a `/standdown` pattern to write a short outcome artifact (what
  shipped, what is in flight, percent done, risks, the next kickoff line), then
  `/context-save` to preserve working context for the next session.
- Capture learnings (a `/learn` pattern): note any pattern or decision worth
  keeping.
- Consolidate memory (a `/dream` pattern): tidy and connect notes so they stay
  findable.
- Hand off: leave the next session a one-line kickoff and a clean repo state.

## Reminders

- **PR-only** — changes land via pull request; no direct pushes to protected
  branches.
- **No `--no-verify`** — if a hook fails, stop and investigate.
- **No force-push** without explicit, per-time approval.
- **Verify before claiming** — command evidence, not opinion.

## Related project files

- `01-conductor-doctrine.md` — lanes, HALT, verify.
- `03-driving-coding-agents.md` — the task template and prompt patterns.
- `07-safety-and-scrub.md` — public-operation and scrub boundaries.

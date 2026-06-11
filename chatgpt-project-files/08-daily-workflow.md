# Brandon's Kung Fu — Daily Workflow (Project File)

> **Status:** private scaffold. Generic daily-workflow patterns only — no
> proprietary, legal, or business context, and no third-party skill bodies.
> Vendor-neutral.

A simple loop for running a day of agent-assisted engineering. Usable as-is.

## Start the day

- Open the session (a `/standup` pattern): capture repo truth — branch, clean or
  dirty, last commit, sync with the remote, any open work.
- Choose the lane: **Green** (bounded, reversible) or **Red** (architecture,
  security, public posture, irreversible operations, hooks/CI, schema, migrations,
  doctrine, anomalies). When unsure, treat it as Red.
- Pick the **next smallest move** that advances the goal and is easy to verify.

## Work through the day

For each unit of work:

1. **Task** — write goal, scope, constraints, steps, verification, required output.
2. **Plan** — confirm the approach and the smallest first step.
3. **Execute** — make the smallest change that works.
4. **Verify** — run the gates; report exact command output.
5. **HALT** — on any anomaly, failed gate, scope drift, or security / public-posture
   concern, stop and surface it instead of pushing through.

Keep changes small and reviewable.

## Close the day

- Close the session (a `/standdown` pattern): write a short outcome artifact — what
  shipped, what is in flight, percent done, risks, and the next kickoff line.
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

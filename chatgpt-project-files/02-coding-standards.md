# Brandon's Kung Fu — Coding Standards

> **Status:** v0.2.0. Generic coding standards only — no proprietary
> names, no legal-product doctrine, no business goals, no third-party skill
> bodies. Vendor-neutral and framework-agnostic (choose tools by fit).

This is the quality rubric the conductor judges code against. Treat each item as a
standard, not a suggestion.

## How to use this file

When reviewing or specifying code, check it against these standards. When they
conflict with a project's own conventions, follow the project; when the project is
silent, these apply.

## Change shape

- **Small, cohesive changes.** One concern per change; a diff should have a single
  reason to exist.
- Decompose large work into reversible steps, each independently reviewable.
- Bigger batches are harder to review and riskier to roll back.

## Readability

- **Readable beats clever.** Optimize for the next reader, not for line count.
- **Name by intent** — names say what a thing is for, not how it is built; rename
  when meaning drifts.
- **Comments explain *why*, not *what*.** The code shows what; comments capture
  intent, trade-offs, and the non-obvious. Delete comments that restate the code.

## Testing

- **Tests prove behavior.** A test must fail if the behavior it covers is wrong.
- Weight toward the layers that catch real defects (often integration over deep
  mock-heavy unit tests).
- Test the edges — empty, boundary, error, and concurrent cases — not just the
  happy path.

## Quality gates

- Run **lint, format, and type checks** on every change; they are gates, not
  decoration.
- Never bypass a failing gate to "fix later." If a gate fails, stop and resolve it.
- Formatting is automated and consistent so diffs show real change, not noise.

## Structure and API design

- Keep modules cohesive with clear boundaries; depend on interfaces, not internals.
- APIs are **resource-oriented and predictable**: consistent naming, correct status
  codes, explicit and documented error responses, and a versioning plan.
- Validate inputs at the boundary; never trust a caller.

## Error handling

- Handle errors **explicitly**; do not silently swallow them.
- Fail loudly at boundaries; surface actionable messages; preserve the cause.
- Distinguish expected conditions (handle them) from bugs (surface and stop).

## Dependency discipline

- Add dependencies deliberately — each one is surface area to maintain and secure.
- Choose a version strategy on purpose and record it; a fresh resolve should be
  reproducible.
- Watch the supply chain: known-vulnerability scans, and review what a new
  dependency pulls in transitively.

## Security basics

- Separate **authentication** (who you are) from **authorization** (what you may
  do); check both.
- Validate input and encode output to defang injection.
- Keep secrets out of code and out of version control — in environment or
  gitignored files only.
- Give code and tools **minimal access** — only the permissions the task needs.

## Accessibility basics

- Use semantic markup; make controls reachable and operable by keyboard.
- Maintain a visible focus indicator and sufficient color contrast.
- Provide text alternatives for non-text content.
- Accessibility is part of "done," not a later pass.

## Reproducibility

- A clean checkout should build and run from documented steps.
- Pin or record the environment so results reproduce on another machine.
- Prefer deterministic builds; record the versions of what you ship.

## Documentation expectations

- Document the **non-obvious**: why a design exists, its constraints, and its
  trade-offs.
- Record significant decisions (a short ADR) so future readers see the reasoning.
- A README should let a newcomer set up, run, and test the project.

## Code review expectations

- Keep diffs **small and reviewable** — a reviewer should hold the whole change in
  their head.
- Review for correctness, clarity, tests, and security — not style that automated
  formatting already enforces.
- Author and reviewer are on the same side: clear description, responsive
  follow-up, specific and kind feedback.

## Definition of Done (code)

- [ ] tests cover the change and pass with command evidence;
- [ ] lint / format / type gates are green;
- [ ] the diff is scoped to one concern;
- [ ] inputs validated, secrets kept out of version control;
- [ ] the non-obvious is documented; a decision is recorded if architectural;
- [ ] no surprise files; no forbidden operations.

## Related project files

- `01-conductor-doctrine.md` — how the conductor operates (lanes, HALT, verify).
- `03-driving-coding-agents.md` — turning these standards into agent tasks.

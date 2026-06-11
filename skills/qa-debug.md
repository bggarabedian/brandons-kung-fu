# Brandon's Kung Fu — QA and Debug Patterns

> **Status:** v0.1. Generic engineering patterns only — no
> proprietary product, legal, business, or private-repo context, and no
> third-party skill body is copied here. Skills are *referenced* by name only.

This is prose documentation for the QA/debug cluster. It describes practices you
can apply in any codebase. It is not a skill, not a doctrine, and not a
specification for any particular product.

---

## What this cluster covers

**QA is not "run the tests at the end."** Quality is built in as you work, not
inspected in afterward. By the time a final test run is your *first* check, most
of the cost of a defect is already sunk.

**QA is a loop:** `inspect → isolate → change → verify → report`. You confirm the
current state, narrow the problem to one cause, make the smallest change, prove
it did what you intended (and broke nothing else), and report with evidence. Then
repeat.

**Verify before you claim.** "It works" is a measurement, not an opinion. If you
have not run the command and read the output, you do not know — so do not say so.

**A hook passing is not the same as doctrine passing.** Automated gates catch a
fixed set of failure modes. Green hooks mean "no known-bad pattern fired," not
"this change is correct and in-scope." Judgment still applies.

**A test must prove the relevant risk, not just produce green output.** A test
that passes without exercising the behavior you changed is false confidence. Ask:
*if my change were wrong, would this test fail?* If not, it is not testing your
change.

---

## The verification stack

Run cheap→expensive and narrow→broad, so the fastest signal fails first:

1. **Focused test(s)** — the specific case(s) covering the unit you changed.
2. **Unit tests** — the module's full unit set.
3. **Full test suite** — the whole project, to catch cross-module breakage.
4. **Lint** — style and common-bug static checks.
5. **Format check** — formatting is correct (don't let it mask real diffs).
6. **Type check** — static types resolve.
7. **Pre-push hook** — the repo's gate (e.g., a denylist/secret scan).
8. **Final scope / diff check** — read your own diff: is everything in it
   intended, and is anything missing?

Earlier steps are faster and more localized; running them first means you spend
the expensive full-suite run only on changes that already passed the cheap gates.

---

## Generic debugging patterns

- **Reproduce before fixing.** A bug you can't reproduce is a bug you can't
  confirm you fixed. Get a reliable repro first.
- **Inspect current truth before acting.** Read the actual file, branch, and
  state now — not what you remember. Memory drifts; the repo doesn't.
- **Smallest failing test first.** Shrink the repro to the minimal case that
  still fails. The smaller it is, the closer it points at the cause.
- **Distinguish failure classes.** Separate *environment failure* (tooling, env
  vars, missing services) from *code defect* (your logic) from *dependency drift*
  (a package resolved differently). Each has a different fix.
- **Compare against a baseline.** If a failure seems unrelated to your change,
  check it out on the baseline branch (e.g., `main`). If it fails there too, it
  isn't yours.
- **Fix orthogonal failures in a separate branch.** An unrelated failure you
  discover is its own unit of work. Fix it on its own branch, land it, then
  return.
- **Don't contaminate a docs/doctrine branch** with unrelated test or config
  fixes. Keep the branch's diff matching its purpose.
- **Halt on anomalies.** Unexpected output, unexpected state, a failed gate, or
  scope creep is a stop signal. Surface it; don't paper over it.

---

## Dependency-drift pattern

A common, confusing failure class deserves its own playbook:

- **Lower-bound pins resolve to newer APIs.** A spec like `pkg>=1.2` can install
  `1.9` in a fresh environment, with changed or removed APIs.
- **A fresh environment surfaces latent failures.** Code that "worked" against a
  stale local install can fail on a clean resolve. The clean resolve is the truth.
- **Prefer minimal test adaptation when production code is not wrong.** If the
  library legitimately changed and your code is still correct, update the test or
  the call site — don't bend the product to a stale assumption.
- **Avoid hard dependency pins unless a pin is the smallest safe fix.** Pinning
  freezes a problem in place; reach for it only when adapting is riskier.
- **Record the cause and the branch used to fix it,** so the next person sees why
  the version moved and where it was handled.

---

## Do / Do Not

| Do | Do Not |
|---|---|
| Confirm repo truth first (read current state) | Waive a failed gate without operator approval |
| Run focused tests before the full suite | Use `--no-verify` |
| Compare suspicious failures against main/baseline | Force-push without explicit approval |
| Fix unrelated failures on a separate branch | Mix unrelated fixes into doctrine/doc branches |
| Report exact commands and exit codes | Claim tests pass without command evidence |
| Keep commits small and scoped | Copy third-party skill bodies |

---

## Example workflow — a docs-only change fails tests

Scenario: you changed only documentation, but the test gate is red.

1. **Halt.** A docs-only diff should not break tests; treat this as an anomaly.
2. **Confirm the failure is unrelated** to your docs change (read the failing
   test; it should touch code you didn't edit).
3. **Test main/baseline.** Check out `main` and run the same gate. If it's red
   there too, the failure predates and is independent of your work.
4. **Fix the failure in a separate branch** — its own scoped unit of work.
5. **Land that fix** to `main` through the normal gate.
6. **Rebase the docs branch onto the now-green `main`.**
7. **Rerun the gate** on the rebased docs branch.
8. **Then push the docs branch** — green, and with a diff that contains only docs.

This keeps each branch's diff matching its stated purpose and never smuggles an
unrelated fix into a documentation change.

---

## Skills (referenced — see [SKILLS.md](SKILLS.md))

Referenced by name only. No third-party body is included here.

- `/quality-triad` — bundle-candidate after scrub audit (orchestrator).
- `/qa-only` — reference-only.
- `/verification-before-completion` — reference-only.
- `/pytest-patterns` — **mismatch**; the actual registry name may be
  `/python-testing-patterns`. Resolve before publishing any link.
- `/test-driven-development` — reference-only.
- `/phase-gated-debugging` — reference-only.
- `/root-cause-tracing` — reference-only.
- `/dependency-audit` — **mismatch**; the actual registry name may be
  `/dependency-management-deps-audit`. Resolve before publishing any link.

> Mismatched names above are flagged, not linked, so this file ships no dead
> `/slash` links.

---

## Next planned cluster files

- `skills/security.md` — security / release-safety cluster.

# Brandon's Kung Fu — QA and Debug (Project File)

> **Status:** v0.3.0. Generic patterns only — no proprietary, legal, or
> private-repo context, and no third-party skill bodies.

Concise conductor guidance for verification and debugging. The fuller cluster doc
is [`../skills/qa-debug.md`](../skills/qa-debug.md).

## QA is a loop

`inspect → isolate → change → verify → report`. Quality is built in as you work,
not inspected at the end. Verify before you claim: if you have not run the command
and read the output, you do not know.

## The verification stack

Run cheap→expensive and narrow→broad, so the fastest signal fails first:

1. focused test(s) for the changed unit
2. unit tests for the module
3. full test suite
4. lint
5. format check
6. type check
7. pre-push hook
8. final scope / diff check

## Exact command evidence

Report the command and its result, every time. "Tests pass" without the command
and its output is not evidence. Quote exit codes when they are the signal.

## Debugging loop

- Reproduce before fixing.
- Read current truth (file, branch, state) before acting.
- Shrink to the smallest failing case.
- Separate failure classes: environment vs code defect vs dependency drift.

## Dependency drift

A lower-bound version pin can resolve to a newer API in a fresh environment, so
code that "worked" can fail on a clean resolve. Prefer minimal test adaptation
when the production code is still correct; reach for a hard pin only as the
smallest safe fix; record the cause and where it was handled.

## Baseline comparison and orthogonal failures

- If a failure looks unrelated to your change, run the same gate on the baseline
  branch. If it fails there too, it is not yours.
- Fix an unrelated failure on its **own branch**; land it; rebase your branch onto
  the green baseline; then continue. Never fold an unrelated fix into a docs or
  doctrine branch.

## Do / Do Not

| Do | Do Not |
|---|---|
| Report exact commands and exit codes | Claim tests pass without command evidence |
| Compare suspicious failures to baseline | Waive a failed gate without approval |
| Fix unrelated failures separately | Use `--no-verify` |
| Keep commits small and scoped | Fold unrelated fixes into one branch |

See `../skills/qa-debug.md` for the full patterns.

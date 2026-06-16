<!-- Brandon's Kung Fu — pull request template. Keep the diff small and public-safe. -->

## Summary

<!-- What does this change and why, in a sentence or two. -->

## Lane

<!-- Pick one. When unsure, treat it as Red. -->

- [ ] **Green** — small, reversible docs/examples
- [ ] **Red** — doctrine, security, public posture, hooks/CI, schema, migrations, or anything irreversible
- [ ] **Inspection-only** — read/report/plan (no code change)

## Scope

<!-- What is in, what is out. -->

## Files changed

<!-- List the files and one line each. -->

## Verification

<!-- Paste the commands you ran and their results. "Looks right" is not "done." -->

```
python scripts/kungfu.py doctor
python scripts/kungfu.py skills doctor
git diff --check
```

## Checklist

- [ ] Lane selected and scope described above
- [ ] Verification commands run, with results pasted
- [ ] Name/scrub scan is clean
- [ ] Concept-risk review done (no private system/decision revealed without a name)
- [ ] No private paths, remotes, raw memories/ledgers, or real vault notes
- [ ] No `.obsidian/` content
- [ ] No third-party skill or policy bodies (reference by name only)
- [ ] No `Co-Authored-By` trailers
- [ ] No `--no-verify`
- [ ] PR only — no direct push to `main`, no force-push

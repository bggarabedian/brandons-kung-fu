# Updating a Brandon's Kung Fu clone

Updates are **explicit, opt-in, reversible, and safe**. The tool only ever
fast-forwards; it never merges, rebases, force-pushes, or changes remotes, and it
never runs `git pull` without `--apply`.

## Check first (no changes)

```
python scripts/kungfu.py update --dry-run
```

Reports:

- current branch;
- current commit;
- the `origin` remote;
- whether the working tree is clean;
- whether an update is possible.

## Apply an update

```
python scripts/kungfu.py update --apply
```

`--apply` only:

1. **requires a clean working tree** — if you have uncommitted changes, it HALTs
   and does nothing (commit or stash first);
2. runs `git fetch origin`;
3. **fast-forwards** the current branch to its `origin/<branch>` upstream
   (`git merge --ff-only`);
4. **refuses** if the branch has diverged (a fast-forward is impossible) — it will
   not merge, rebase, or force; resolve that manually;
5. runs `doctor` after updating to confirm readiness.

## After updating

Regenerate the ChatGPT package if you want the latest doctrine in the export:

```
python scripts/kungfu.py setup-chatgpt --apply
python scripts/kungfu.py doctor-chatgpt
```

Re-upload the changed files in your ChatGPT Project, and re-sync your Claude
install with `install-claude --apply --target <path>` (existing differing files
are backed up only with `--allow-backup`).

## What update never does

- No merge commits, no rebase, no force-push.
- No pull on a dirty tree.
- No remote, branch-protection, or config changes.
- No background or scheduled updates.

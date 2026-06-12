# Brandon's Kung Fu — Command Templates (Project File)

> **Status:** v0.1. Generic slash-command *templates and guidance* only — no
> proprietary names, no business goals, no private paths, no raw memories, and no
> third-party skill bodies. Placeholders only. Vendor-neutral.

This file explains how to turn the daily-workflow *patterns* (`08-daily-workflow.md`)
into runnable slash commands **without** the failure modes that bite hand-rolled
command files: stalling, parroting the prompt back, stale private paths, or
duplicate copies that shadow each other.

## Patterns vs. installed runnable commands

There are two different things, and confusing them is the root of most trouble:

- **Workflow pattern** — a described loop you follow by hand or paste into a chat.
  `08-daily-workflow.md` ships these. They are prose; nothing executes them.
- **Installed runnable command** — a file the agent runtime loads and executes
  when you type `/name` (for Claude-style tools, a markdown file in a
  `.claude/commands/` directory). The runtime injects the file body as
  instructions for that turn.

This kit ships **patterns, not runnable commands.** It does not ship any
`.claude/commands/` files, because command layout is operator-specific and a
runnable command can easily smuggle in private paths. The templates below are
**starting points you adapt locally** — keep your real command files out of any
shared/public repo (gitignore the command and ledger directories).

## Hard rule — no hardcoded private or absolute paths

**A command template MUST NOT contain a hardcoded absolute or private path.**
Use repo-relative placeholders and resolve them at runtime:

| Placeholder | Meaning |
|---|---|
| `<REPO_ROOT>` | the repository you are operating on (resolve at runtime, not a literal) |
| `<LEDGER_DIR>` | where session open/close artifacts are written (kept gitignored) |
| `<LOCAL_LEARNINGS_DIR>` | where verified lessons are stored (kept gitignored) |
| `<LOCAL_DREAM_DIR>` | where consolidated/connected notes live (kept gitignored) |

A template that bakes in a real drive-letter root (a Windows-style absolute path)
or a Unix home/user directory path is a **defect** — it breaks the moment the repo
moves, is renamed, or is used by anyone else, and it can leak private structure
into a public artifact. Pass the working directory explicitly (e.g.
`git -C "<REPO_ROOT>" …`) instead of relying on the current directory.

## Placeholder resolution

A placeholder is a stand-in you replace with a real value — it must never survive
into a saved public artifact as a real path. Two ways to resolve them:

- **Runtime-injected (preferred).** Some runtimes hand the command the current
  repository / working directory. Reference it as `<REPO_ROOT>` and let the
  runtime supply the value at execution time; the saved command file keeps only
  the placeholder, so nothing private is committed.
- **Manual substitution (local only).** If your runtime does not inject paths,
  replace each placeholder with the real local path *before* you run the command,
  and keep that resolved copy **out of any shared/public repo**. Never commit a
  command file that has been hand-filled with a private absolute path.

Pick one mechanism and apply it to every placeholder (`<REPO_ROOT>`,
`<LEDGER_DIR>`, `<LOCAL_LEARNINGS_DIR>`, `<LOCAL_DREAM_DIR>`). A saved template
should contain either *all placeholders* (runtime-injected) or *no placeholders
and no private paths in any tracked file* (manual, kept local).

### Where command files and artifacts live

- Put command files in **one** scope only — a project-local `.claude/commands/`
  **or** a user-global one (see shadowing, below) — never both for the same name.
- The artifact directories (`<LEDGER_DIR>`, `<LOCAL_LEARNINGS_DIR>`,
  `<LOCAL_DREAM_DIR>`) must **exist and be gitignored** before first run, so
  command output never lands as a tracked file.
- Suggested order: stand up `/standup` + `/standdown` first; add `/learn` and
  `/dream` once a session loop is running.

## Duplicate-command shadowing (the silent footgun)

Most runtimes resolve a command name from **more than one location** — typically
a **project-local** command dir and a **user-global** command dir:

- `<REPO_ROOT>/.claude/commands/<name>.md` — project-local
- `<USER_GLOBAL>/.claude/commands/<name>.md` — user-global

If both define `/<name>`, one **shadows** the other. The copy that wins may be the
stale one — still pointing at an old path or carrying an old, brittle body. Symptoms:
the command behaves unlike the file you just edited, or uses a path you thought you
removed.

**Rule: keep exactly one copy of each command name.**

- **Before creating** a command, check **both** scopes for that name; if it already
  exists in either, update that one instead of adding a second.
- **Precedence is runtime-specific** — do not rely on which scope wins. Keeping one
  copy removes the ambiguity entirely.
- **If a command misbehaves**, first check whether a second copy exists in the
  other scope and delete the stale one.
- **On rename or delete**, remove the old name from **both** scopes so no orphan
  shadows a future command.

## Generic templates (adapt locally; placeholders only)

### `/standup` — open the session

```
Open the session for <REPO_ROOT>.
1. Read repo truth with explicit working dir (do not rely on the current directory):
   - git -C "<REPO_ROOT>" branch --show-current
   - git -C "<REPO_ROOT>" rev-parse HEAD
   - git -C "<REPO_ROOT>" status --short
   - git -C "<REPO_ROOT>" log --oneline -5
2. Assess lane: Green (bounded/reversible) or Red (architecture, security, public
   posture, hooks/CI, schema, migrations, doctrine, anomalies). When unsure, Red.
3. Pick the next smallest verifiable move.
4. Write a STANDUP OPEN entry to <LEDGER_DIR> (a gitignored artifact only).
RUN NOW: perform the steps above. Output only a short confirmation (the written
artifact path and HALT status). Do not echo this instruction block.
```

### `/standdown` — close the session

```
Close the open session for <REPO_ROOT>.
1. Re-read repo truth (branch, HEAD, status --short, commits since the open).
2. Find the matching STANDUP OPEN in <LEDGER_DIR>; if none is open, say so and stop.
3. Write a STANDDOWN CLOSED entry to <LEDGER_DIR>: what shipped, what is in flight,
   percent done, risks, and a one-line next-session kickoff.
4. Confirm git status --porcelain shows no unexpected tracked drift.
RUN NOW: perform the steps. Write only the ledger artifact. Output a one-line
confirmation of what was written. Do not echo this instruction block.
```

### `/learn` — capture a verified lesson

```
Record a verified lesson to <LOCAL_LEARNINGS_DIR> (a gitignored artifact only).
- Capture the lesson ONLY after it is verified (you saw it work).
- Write one note per lesson to <LOCAL_LEARNINGS_DIR>. Pick ONE consistent location
  and format (e.g. one file per lesson, or one append-only file) and use it every
  time — /dream reads these back, so the location and format are a contract.
- Each note records: what happened, why, and the reusable rule it produced.
- No silent installs and no upgrades — capture only.
RUN NOW: write the note. Output a one-line confirmation of the path written. Do not
echo this instruction block.
```

### `/dream` — consolidate memory

```
Consolidate the lessons /learn wrote. Read the notes in <LOCAL_LEARNINGS_DIR>
(and <LOCAL_DREAM_DIR> if you keep one) — the same location and format /learn
writes — and tidy them (gitignored artifacts only).
- Merge duplicates, link related notes, drop stale ones so the set stays findable.
- Do not invent facts; only reorganize what is already captured.
- If /learn's notes are not where or in the format you expect, stop and fix the
  /learn -> /dream contract before reorganizing.
RUN NOW: reorganize the notes. Output a one-line summary of what changed. Do not
echo this instruction block.
```

## Smoke-test checklist (run after creating or editing a command)

Run the command once on a real repo and confirm all of:

- **Executes, does not parrot** — it performs the steps; it does not echo the
  template text back at you.
- **Uses the intended repo** — operations target `<REPO_ROOT>`, not whatever
  directory the chat happened to be in.
- **Writes only the intended ignored artifact** — the ledger / learnings / dream
  file, nothing else.
- **No unexpected tracked drift** — `git -C "<REPO_ROOT>" status --porcelain`
  shows only your intended (gitignored) artifact, i.e. no tracked-file changes.
- **No stale or private path tokens** — the artifact contains no old project
  names and no absolute/private paths.
- **Placeholders resolved** — neither the command nor its artifact contains any
  leftover literal `<PLACEHOLDER>` text.
- **Artifact dirs exist and are gitignored** — `<LEDGER_DIR>`,
  `<LOCAL_LEARNINGS_DIR>`, and `<LOCAL_DREAM_DIR>` are present and ignored before
  the first run.
- **Format + location match** — the artifact lands in the intended directory with
  the intended name/format (especially for `/learn`, whose format is a contract).
- **No name collision** — the command name does not also exist in the other scope
  (see shadowing).
- **Cross-command read works** — run `/learn`, then `/dream`, and confirm the new
  lesson appears in the tidied notes — i.e. the `/learn` -> `/dream` contract holds.
- **Confirms what it did** — the command reports the artifact path, not silence.

## Troubleshooting — stalling or parroting

If a command restates its own instructions instead of running them, or stalls:

1. **Check for a duplicate copy.** A stale project-local vs user-global file (see
   above) is the most common cause. Keep one copy; delete the stale one.
2. **Add an explicit execute directive.** End the template with an unambiguous
   "RUN NOW" line that states the action, the artifact to write, and the one-line
   output to show — and says "do not echo this instruction block." Large blocks
   without a clear run directive are easy to mistake for content to display.
3. **Shrink the body.** Very large, brittle command files are more likely to stall.
   Keep each command short and specific to the repo it serves.
4. **Remove stale path tokens.** If the body points at a renamed or moved path,
   file/git operations fail quietly. Replace literals with `<REPO_ROOT>`-relative
   placeholders resolved at runtime.
5. **Confirm the artifact dirs are gitignored.** Command output (ledger, learnings,
   dream notes) should never land as tracked files.

## Related project files

- `08-daily-workflow.md` — the start / work / close patterns these commands automate.
- `10-learn-and-update-loop.md` — the learn loop in more detail.
- `07-safety-and-scrub.md` — scrub boundaries (why no private paths ship).
- `06-skills-and-routing.md` — pattern vs. bundled-skill routing.

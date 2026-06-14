# ChatGPT Project setup

ChatGPT is used as the **conductor LLM**: it scopes, plans, prompts, audits, and
verifies. A **ChatGPT Project** gives it persistent project doctrine across every
chat in that Project. This is how you load Brandon's Kung Fu into it.

## 1. Generate the package

```
python scripts/kungfu.py setup-chatgpt --dry-run    # see the plan, write nothing
python scripts/kungfu.py setup-chatgpt --apply      # generate dist/chatgpt-project/
python scripts/kungfu.py doctor-chatgpt             # verify it
```

The generated `dist/chatgpt-project/` (gitignored) contains:

- `README_UPLOAD_FIRST.md` — the click-by-click steps;
- `PROJECT-INSTRUCTIONS.txt` — paste this into Project Instructions;
- `files/` — the project files to upload;
- `UPLOAD_ORDER.md` — the exact order;
- `WHY_CHATGPT.md` — the division of labor;
- `VERIFY_SETUP.md` — a correctness test;
- `MANIFEST.json` — a snapshot of what was packaged.

> The tool **does not upload anything to ChatGPT** and does not log in. You upload
> through the ChatGPT UI. Manual upload is the safe, supported path.

## 2. Create the Project in ChatGPT

1. Go to ChatGPT.
2. Create a new **Project**.
3. Name it like **"Brandon's Kung Fu"** (or a project-specific equivalent).
4. Open the Project settings.
5. Paste the full contents of `PROJECT-INSTRUCTIONS.txt` into **Project
   Instructions**.
6. Upload the files from `files/` in the order in `UPLOAD_ORDER.md`.

## 3. Where the project files are in the repo

The source lives in `chatgpt-project-files/`. The package's `files/` is generated
from there, and `PROJECT-INSTRUCTIONS.txt` is a verbatim copy of
`chatgpt-project-files/PROJECT-INSTRUCTIONS.md`. To re-pull after an update, re-run
`setup-chatgpt --apply`.

## 4. Test it

Start a **new chat inside the Project** and ask:

> Run /standup for this repo using Brandon's Kung Fu.

Then run the test in `VERIFY_SETUP.md`. The assistant should describe the
conductor role, the Green/Red lane split, GStack Native Mode (reference-only),
PR-only workflow, and the no-public-ops-without-approval rule.

## 5. Keep it current

After `python scripts/kungfu.py update --apply`, regenerate with
`setup-chatgpt --apply` and re-upload the changed files.

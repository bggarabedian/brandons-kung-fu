# Claude Code setup

Claude Code is the **local implementation IC**: it inspects and edits local files
under an approved scope and reports command evidence. This is how you give it the
same Brandon's Kung Fu doctrine the ChatGPT conductor uses — from the same
manifest source.

## Install the context

```
python scripts/kungfu.py install-claude --dry-run --target <path>
python scripts/kungfu.py install-claude --apply   --target <path>
```

- The kit copies its context files into **`<path>/brandons-kung-fu/`** (a clear,
  namespaced folder).
- Choose `<path>` inside your own Claude context or skills directory. The full
  target is **printed before anything is written**.
- **Dry-run is the default.** `--apply` is required to write.
- An existing file that **differs** is **never overwritten silently**: the tool
  HALTs, or with `--allow-backup` keeps a timestamped `.bak` before writing.
- The tool refuses to install into the kit repo itself.

## What gets copied

The owner-authored doctrine files listed under `claude.context_files` in
`kungfu.manifest.json` — the conductor doctrine, coding standards, agent-driving
patterns, skills routing, safety/scrub, daily workflow, learn/update loop,
project instructions, and the skills catalog/access-layer. **No third-party skill
bodies are ever copied** — command names and rules only.

## Point Claude Code at it

After installing, open Claude Code in your project and reference the doctrine
folder (`<path>/brandons-kung-fu/`) so the agent reads the conductor rules, lanes,
HALT behavior, and the safe-vs-RED command split before acting.

## GStack is referenced, not installed

If a GStack-style pack is present, `doctor` reports it. This kit never installs,
updates, copies, or modifies GStack. Safe GStack commands may be used when present;
RED commands require explicit per-task approval.

## Remove it

Delete `<path>/brandons-kung-fu/`. Nothing else on your system was changed.

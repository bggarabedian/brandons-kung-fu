# Same system, one source

The ChatGPT conductor and the Claude Code hands must run the **same doctrine**.
That alignment is enforced by a single manifest, not by hand-copying.

## The alignment contract

`kungfu.manifest.json` is the **one source of truth**:

- `chatgpt.upload_order` + `chatgpt.instructions_source` define exactly what the
  ChatGPT Project gets.
- `claude.context_files` define exactly what Claude Code gets.
- Both lists point at the **same files in `chatgpt-project-files/`** (plus the
  skills catalog for Claude).
- `gstack.reference_only_commands` and `gstack.red_approval_commands` define the
  safe-vs-RED command split both layers must honor.

## Verify alignment

```
python scripts/kungfu.py sync
```

`sync` reports the shared source files, the ChatGPT-only files, and the
Claude-only files, and confirms every referenced file exists on disk. If a file is
missing or the lists drift, it fails — so the two exports can never silently
diverge.

```
python scripts/kungfu.py doctor-chatgpt
```

`doctor-chatgpt` additionally checks that a generated
`dist/chatgpt-project/PROJECT-INSTRUCTIONS.txt` is byte-identical to its source
`chatgpt-project-files/PROJECT-INSTRUCTIONS.md`, that no private/proprietary tokens
appear in the upload set, and that no third-party skill bodies were copied.

## Why it matters

If the conductor and the hands run different rules, the safety model breaks: one
side could approve what the other forbids. One manifest, two derived exports,
verified by `sync` — that is how the system stays one system.

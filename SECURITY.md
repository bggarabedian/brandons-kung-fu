# Security Policy

Brandon's Kung Fu is a **docs and tooling kit** — operating doctrine, Markdown
project files, and a small Python-standard-library CLI. It is **not a hosted
service** and stores no user data. The main security surface is the offline
pre-push denylist scanner and the scrub discipline that keeps private content out
of public artifacts.

## Supported versions

| Version | Supported |
|---|---|
| `0.3.x` (current pre-1.0 line) | Yes — fixes land on `main` |
| older / pre-`0.3` | Best effort only |

This project is **pre-1.0**: the public install/update contract is not yet stable,
and no GitHub release is tagged yet. Treat versions as moving until `v1.0.0`.

## Reporting a vulnerability

- **Preferred:** use GitHub's **private vulnerability reporting** for this repo, if
  it is enabled (repo → Security → "Report a vulnerability").
- **Otherwise:** open a **minimal public issue** that says you have a security
  concern and asks a maintainer for a private channel — **without** including
  exploit details, payloads, or sensitive specifics in the public issue.

Please **do not** post in public issues or PRs:

- secrets, credentials, tokens, or keys;
- working exploit details or payloads;
- private repo paths, private remotes, or protected terms;
- anyone's private personal information.

## What to expect

This is a small, volunteer-maintained kit. Maintainers aim to acknowledge a valid
report and discuss next steps as capacity allows — there is **no guaranteed
response time or SLA**. Fixes are prioritized by real-world impact. Thank you for
reporting responsibly.

## Scope

In scope: the doctrine docs, the `scripts/kungfu.py` CLI, and the `git-hooks/`
scanner. Out of scope: third-party tools referenced by name (coding agents,
skill packs), which are governed by their own projects.

# Brandon's Kung Fu — Security and Release-Safety Patterns

> **Status:** private scaffold. Generic security patterns only — no proprietary
> names, no legal-product doctrine, no third-party skill bodies. Skills are
> referenced by name only.

Prose documentation for the security cluster — generic engineering patterns you
can apply in any codebase.

## Secrets

- Keep secrets out of source and out of version control — in environment variables
  or gitignored files only.
- Never log a secret; redact tokens and credentials in output.
- Rotate on exposure; assume a leaked secret is compromised.

## Denylist scanning

- Scan tracked files for protected terms before they can be published; fail the
  push on a hit.
- Ship an **inert example** denylist (placeholders only) and keep the real terms
  in a **gitignored local** file that is never committed.
- Run the scanner offline — no network, no installs.

## Threat modeling

- For each feature, ask: what can go wrong, who could abuse it, and what is the
  blast radius.
- Identify trust boundaries and the data that crosses them.
- Design the control before the feature ships, not after an incident.

## Minimal access

- Give every component, token, and tool the **least access** it needs — nothing
  more.
- Put an approval gate in front of irreversible or high-impact actions.
- Separate identity (who) from authorization (what is allowed).

## Public-operation gates

- No publishing, sharing, or external exposure without explicit approval.
- Default posture is private; treat an ambiguous action as public and stop.
- Record approval for any public operation.

## Dependency review

- Review what a new dependency adds, including its transitive pulls.
- Scan for known vulnerabilities and keep dependencies current.
- Prefer fewer, well-maintained dependencies over many thin ones.

## Branch protection

- Protect shared branches: require review, require passing checks, block direct
  pushes.
- No history rewrites on shared branches without explicit approval.
- Changes land via pull request.

## Hook discipline

- Pre-commit and pre-push hooks run on every operation; never bypass with
  `--no-verify`.
- If a hook fails, stop and investigate — a failing gate is a signal, not an
  obstacle.
- Keep the hook source in version control and the real protected terms out of it.

## Final release checklist

Before anything ships or is made public:

- [ ] secret scan and denylist scan are clean;
- [ ] dependencies reviewed; no known-vulnerable versions;
- [ ] minimal-access review done for new tokens and tools;
- [ ] branch protection in place; the change landed via pull request;
- [ ] no public operation performed without recorded approval;
- [ ] a concept-risk review done in addition to the name scans.

## Skills (referenced — see [SKILLS.md](SKILLS.md))

Referenced by name only. No third-party body is included here.

- `/threat-modeling-expert` — reference-only.
- `/secrets-management` — reference-only.
- `/defense-in-depth` — reference-only.

## Related files

- `SKILLS.md` — the skill catalog and provenance legend.
- `../chatgpt-project-files/07-safety-and-scrub.md` — the kit's safety/scrub
  posture.

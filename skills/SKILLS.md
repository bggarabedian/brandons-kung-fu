# Brandon's Kung Fu — Skill Manifest

> **Status:** private scaffold. This is a **manifest, not a skill library.**
> It names skills and describes them generically. It contains **no third-party
> skill body**. A skill moves from "referenced" to "bundled" only after a
> per-skill scrub + license audit.

## The ship / reference split

- **Bundled** — Brandon-authored, scrub-clean, *generic* orchestrators only.
  Their files live under `skills/_authored/` — and only after the audit clears
  them. Nothing is bundled yet.
- **Referenced** — third-party skills, listed by `/slash` name plus a generic
  source note. Their bodies are **never** copied into this kit; install them
  from their own upstream pack.
- **Distilled** — useful techniques that have no shippable skill: documented
  later as prose in the cluster files (`rag-cag.md`, etc.), **never** as a dead
  `/slash` link.
- **Private** — proprietary or project-coupled skills: never exported, never
  named here.

> Exact upstream + license for every `3P` row is resolved during the per-skill
> audit; until then a `3P` note stays generic on purpose.

## Provenance legend

| Tag | Meaning |
|---|---|
| `AUTH-G` | Brandon-authored, generic. **Bundle candidate** *after* scrub audit. |
| `AUTH-P` | Brandon-authored but proprietary / project-coupled. **Never bundle raw.** |
| `3P` | Third-party. **Reference only** (name + source note). Never copy the body. |
| `PHANTOM` | Requested name not found in the registry. Document as a prose pattern, or author a new generic skill, or drop. |
| `MISMATCH` | Requested name differs from the actual registry name. Resolve the real name before linking. |
| `AUTHOR-NEW` | A planned, owner-authored generic skill — documented as a prose pattern until built; never a third-party body. |

## Kit-action vocabulary

- **bundle-candidate** — eligible to ship after scrub + license audit (not yet bundled).
- **reference-only** — name + source note; install from upstream.
- **resolve** — fix a `MISMATCH`/`PHANTOM` before any link is published.
- **command/pattern** — a workflow idea, not (yet) a bundled skill.

---

## Catalog

### A. Core workflow / operating discipline

Generic session and review discipline. Bundled: none yet.

| Slash | Provenance | Kit action |
|---|---|---|
| `/qa-only` | `3P` | reference-only |
| `/verification-before-completion` | `3P` | reference-only |
| `/architect-review` | `3P` / unresolved | reference-only until provenance audit |
| `/security-review` | `3P` / unresolved | reference-only until provenance audit |
| `/context-engineering` | `MISMATCH` / `3P` | resolve real registry name before linking |
| `/learn` | command/pattern | not a bundled skill yet |
| `/standup` | command/pattern | not a bundled skill yet |
| `/standdown` | command/pattern | not a bundled skill yet |
| `/dream` | command/pattern | not a bundled skill yet |
| `/cli-anything` | `AUTHOR-NEW` | prose pattern — turns repeatable workflows into small typed CLI tools (no body yet) |

### B. RAG / CAG / AI app engineering

Retrieval, vector storage, and evaluation. Bundled: none yet (one orchestrator is a candidate).

| Slash | Provenance | Kit action |
|---|---|---|
| `/rag-full-stack` | `AUTH-G` (orchestrator) | bundle-candidate after scrub audit |
| `/rag-engineer` | `3P` | reference-only |
| `/rag-implementation` | `3P` | reference-only |
| `/vector-database-engineer` | `3P` | reference-only |
| `/llm-evaluation` | `3P` | reference-only |
| `/advanced-evaluation` | `3P` | reference-only |
| `/embedding-strategies` | `3P` | reference-only |
| `/hybrid-search` | `MISMATCH` | resolve — actual may be `/hybrid-search-implementation` |
| `/bm25-patterns` | `PHANTOM` | document as prose pattern, or author new |
| `/reranking-strategies` | `PHANTOM` | document as prose pattern, or author new |
| `/knowledge-graph-rag` | `PHANTOM` | document as prose pattern, or author new |
| `/multi-vector-retrieval` | `PHANTOM` / `MISMATCH` | resolve (nearest: `/similarity-search-patterns`) or document as prose |

### C. QA / testing / debugging

Test discipline and root-cause work. Bundled: none yet (one orchestrator is a candidate).

| Slash | Provenance | Kit action |
|---|---|---|
| `/quality-triad` | `AUTH-G` (orchestrator) | bundle-candidate after scrub audit |
| `/pytest-patterns` | `MISMATCH` | resolve — actual may be `/python-testing-patterns` |
| `/test-driven-development` | `3P` | reference-only |
| `/phase-gated-debugging` | `3P` | reference-only |
| `/root-cause-tracing` | `3P` | reference-only |
| `/dependency-audit` | `MISMATCH` | resolve — actual may be `/dependency-management-deps-audit` |

### D. Security / release safety

Threat modeling and secret hygiene. Bundled: none yet.

| Slash | Provenance | Kit action |
|---|---|---|
| `/threat-modeling-expert` | `3P` | reference-only |
| `/secrets-management` | `3P` | reference-only |
| `/defense-in-depth` | `3P` | reference-only |

---

## Never-bundle rules

1. No third-party skill body without a completed **license audit**.
2. No raw private / `AUTH-P` (Brandon-proprietary, project-coupled) skills.
3. No proprietary doctrine of any kind.
4. No private project names or goals.
5. No raw memories, learnings, or ledgers.
6. No copy-private-then-scrub workflow — any authored skill is written **fresh
   from blank**, never derived from a private file by find-and-replace.

## Next planned files

- The cluster docs (`rag-cag.md`, `qa-debug.md`, `security.md`) now exist.
- `skills/_authored/` — created **only after** a per-skill scrub + license audit
  confirms an `AUTH-G` orchestrator is clean to bundle. Empty / absent until then.

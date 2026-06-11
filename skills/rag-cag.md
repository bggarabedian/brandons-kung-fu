# Brandon's Kung Fu — RAG/CAG Patterns

> **Status:** private scaffold. Generic, domain-neutral engineering patterns
> only — no proprietary corpus, product, legal, or business context, and no
> third-party skill body is copied here. Skills are *referenced* by name; their
> implementations live in their own upstream packs.

This is prose documentation for the retrieval cluster. It describes patterns you
can apply in any RAG/CAG system. It is not a skill, not a doctrine, and not a
specification for any particular product.

---

## What this cluster covers

### RAG — retrieval-augmented generation

RAG grounds a model's output in evidence fetched at query time. Instead of
relying on parametric memory, the system retrieves relevant documents, assembles
them into context, and asks the model to answer **from that context**. The win
is freshness and traceability: answers can cite the exact source they came from,
and you can update knowledge by updating the index, not by retraining.

### CAG — cache-aware / cache-augmented context

CAG reuses previously assembled context or previously computed retrieval results
to cut latency and cost. A cache can sit at several layers: embedding cache,
retrieval-result cache, assembled-context cache, or generation cache. CAG is an
**optimization layer on top of RAG** — never a replacement for it.

### Retrieval stays the source of truth

The retrieval layer is authoritative. A cache is a performance shortcut whose
only job is to return the *same answer retrieval would have produced, faster*.
The moment a cache can return something retrieval would not, it has become a
correctness hazard. Design so that a cache miss always falls back to live
retrieval, and so that cached results can be revalidated against the index.

### When cache helps

- Stable, high-traffic prefixes (system prompts, fixed instructions, static
  reference snippets) that change rarely.
- Deterministic, non-personal sub-results that many queries share.
- Expensive recomputation (re-embedding large stable corpora) where the inputs
  have not changed.

### When cache is dangerous

- Personal, per-user, per-tenant, or session-private data — caching it risks
  cross-user or cross-tenant leakage.
- Time-sensitive or frequently superseded sources — a stale hit is a wrong
  answer with high confidence.
- Anything where the cache key does not fully capture what makes the result
  correct (tenant, region, version, freshness, access scope). An undercaptured key
  is a silent correctness bug.

---

## The four-layer RAG stack

A production RAG system has four layers. Treat each as independently testable.

**1. Ingestion + chunking.**
Normalize sources, strip boilerplate, and split into retrievable units. Chunk on
semantic boundaries where possible; keep overlap small but non-zero so context
isn't severed mid-thought. Attach metadata to every chunk at ingestion
(`source_id`, `section`, `version`, `last_seen`, access scope) — metadata you
fail to capture here cannot be filtered on later.

**2. Retrieval + ranking.**
Turn a query into candidate chunks. Combine recall (get everything plausibly
relevant) with precision (rank the best to the top). This is where dense, sparse,
hybrid, and reranking patterns (below) apply.

**3. Context assembly.**
Select, order, and pack the ranked chunks into the model's context window under a
token budget. De-duplicate near-identical chunks, preserve source attribution so
the answer can cite, and keep the highest-value evidence where the model attends
best. Record what was assembled so a result is reproducible.

**4. Evaluation + regression gates.**
Measure retrieval and end-to-end quality on a fixed eval set, and **block
releases on regressions**. Without this layer, every prompt or index change is an
unmeasured gamble. (See evaluation patterns and the referenced eval skills.)

---

## Generic retrieval patterns

**Metadata-first retrieval.**
Filter before (or alongside) you rank. If a query is scoped to a version, a
source type, or an access boundary, apply that as a hard metadata predicate so
out-of-scope chunks never compete for the context budget. Cheap, deterministic,
and it removes whole classes of wrong-context errors.

**Dense retrieval.**
Embed query and chunks into a vector space and retrieve by nearest-neighbor.
Strong on paraphrase and semantic similarity; weak on rare exact tokens
(identifiers, codes, names) that embeddings smear together.

**Sparse retrieval (incl. BM25).**
Term-frequency methods such as BM25 score lexical overlap. They excel exactly
where dense retrieval is weak: exact terms, rare tokens, and short keyword
queries. BM25 is described here as a *pattern* — there is no dedicated kit skill
for it; use it directly in your retrieval layer.

**Hybrid retrieval.**
Run dense and sparse together and fuse the results (e.g., weighted score
combination or reciprocal-rank fusion). Hybrid consistently beats either method
alone because their failure modes are complementary. The kit references a
possible skill for this under a name to be confirmed (see Skills below).

**Reranking.**
After first-stage retrieval returns a candidate set, re-score the top-N with a
stronger, slower model (e.g., a cross-encoder) that reads query and chunk
together. Reranking trades a little latency for a large precision gain at the top
of the list. Documented here as a *pattern* — no dedicated kit skill; wire a
reranker into stage 2.

**Knowledge-graph RAG (KG-RAG).**
When relationships are central (entities, hierarchies, dependencies), retrieve over a
graph and walk edges to gather connected evidence, then feed the subgraph as
context. Useful for multi-hop questions a flat vector search would miss.
Documented as a *pattern* — no dedicated kit skill.

**Multi-vector retrieval.**
Represent a document with several vectors (per passage, per field, or per token,
as in late-interaction methods) instead of one averaged vector. Improves recall
on long or multi-topic documents at the cost of index size. Documented as a
*pattern* — no dedicated kit skill; the nearest referenced skill covers general
similarity search.

---

## Generic cache (CAG) patterns

**Cache eligibility.**
Decide *what* may be cached before *how*. A result is cache-eligible only when:
its inputs are stable, it contains no personal/private/tenant-scoped data by
default, and its cache key captures **every** dimension that makes it correct
(query, source version, scope, freshness window). If you can't enumerate the key
completely, the result is not eligible.

**Cache invalidation.**
Invalidate on the things that change correctness, not just on a timer. Combine a
TTL (bounds staleness) with content-version or content-hash signals (invalidate
when the underlying source changes) and explicit purge on known updates. Prefer
invalidating too eagerly over serving a confidently stale hit.

**Cache-bypass eval mode.**
Keep a switch that forces full live retrieval, ignoring all caches. Run your eval
set in bypass mode periodically and compare against cached-mode results: a
divergence means a cache is returning something retrieval would not — i.e., a
staleness or key-coverage bug. Never write to the cache from the bypass/fallback
path.

---

## Skills (referenced — see [SKILLS.md](SKILLS.md))

Referenced by name only. No third-party body is included here.

- `/rag-full-stack` — bundle-candidate after scrub audit (orchestrator).
- `/rag-engineer` — reference-only.
- `/rag-implementation` — reference-only.
- `/vector-database-engineer` — reference-only.
- `/llm-evaluation` — reference-only.
- `/advanced-evaluation` — reference-only.
- `/embedding-strategies` — reference-only.
- `/hybrid-search` — **mismatch**; the actual registry name may be
  `/hybrid-search-implementation`. Resolve before publishing any link.

> BM25, reranking, knowledge-graph RAG, and multi-vector retrieval are documented
> **above as prose patterns**. They have no dedicated kit skill, so this file
> deliberately ships **no** `/slash` link for them — no dead links.

---

## Do / Do Not

| Do | Do Not |
|---|---|
| Preserve source metadata from ingestion onward | Let a cache replace retrieval |
| Measure Recall@K, MRR, and precision on a fixed eval set | Cache private/dynamic/user-scoped data by default |
| Run cache-bypass evals to catch staleness | Claim outputs are hallucination-free |
| Cite the retrieved evidence behind an answer | Ship retrieval or prompt changes without eval gates |
| Fail closed when retrieval is insufficient | Bundle third-party skill bodies |

---

## Next planned cluster files

- `skills/qa-debug.md` — QA / testing / debugging cluster.
- `skills/security.md` — security / release-safety cluster.

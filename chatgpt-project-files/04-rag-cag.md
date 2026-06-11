# Brandon's Kung Fu — RAG/CAG (Project File)

> **Status:** private scaffold. Generic patterns only — no proprietary corpus,
> product, legal, or business context, and no third-party skill bodies.

Concise conductor guidance for retrieval and cache. The fuller cluster doc is
[`../skills/rag-cag.md`](../skills/rag-cag.md).

## Retrieval is the source of truth

A cache is a speed shortcut, never the authority. A cache miss must fall back to
live retrieval, and cached results must stay checkable against the index. If a
cache can return something retrieval would not, it has become a correctness
hazard.

## The four layers (quick view)

1. **Ingestion + chunking** — split on meaning; attach metadata (source, version,
   scope) at ingestion.
2. **Retrieval + ranking** — combine dense (semantic) and sparse (exact-term)
   search; rerank the top results for precision.
3. **Context assembly** — pack the best evidence under a token budget; keep source
   attribution so answers can cite.
4. **Evaluation + regression gates** — measure on a fixed set; block releases on
   regressions.

## Cache eligibility

A result is cacheable only when its inputs are stable, it holds no personal or
per-tenant data by default, and its cache key captures every dimension that makes
it correct (query, source version, scope, freshness). If you cannot list the full
key, it is not eligible.

## Cache invalidation

Invalidate on what changes correctness, not just on a timer. Combine a time bound
with content-version or content-hash signals, and purge on known updates. Prefer
invalidating too early over serving a confident stale hit.

## Cache-bypass evals

Keep a switch that forces full live retrieval, ignoring caches. Run the eval set
in bypass mode and compare to cached mode; a divergence means a cache is returning
something retrieval would not. Never write to the cache from a fallback path.

## Do / Do Not

| Do | Do Not |
|---|---|
| Keep retrieval authoritative | Let a cache replace retrieval |
| Measure Recall@K / MRR on a fixed set | Cache personal or per-tenant data by default |
| Run cache-bypass evals | Claim outputs are hallucination-free |
| Cite retrieved evidence | Ship retrieval changes without eval gates |

See `../skills/rag-cag.md` for the full patterns (hybrid search, reranking,
knowledge-graph and multi-vector retrieval).

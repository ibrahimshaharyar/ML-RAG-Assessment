# Production Thinking — RAG System Q&A

---

### 1. How would you handle hallucinations in RAG?

Hallucinations happen when the LLM generates information not present in the retrieved context. Several layers of defence are useful:

**Prompt constraints**: The system prompt explicitly instructs the LLM to answer using only the provided context and to say "I don't have information on that" when the context is insufficient. Temperature is kept low (0.2) to reduce creative generation.

**Faithfulness scoring**: After each response, a faithfulness check can be run — either via an LLM-as-judge or a library like `ragas`. Responses below a threshold (e.g. < 0.7) can be flagged or withheld.

**Source attribution**: Every answer includes the source document(s) it was drawn from. Users can verify the answer against the original doc, and engineers can audit cases where sources seem irrelevant to the answer.

**Retrieval quality gates**: If the top retrieved chunk has a cosine similarity below a minimum threshold (e.g. 0.3), the system should respond with a fallback message rather than passing poor context to the LLM.

---

### 2. How would you update embeddings when documents change?

The ingestion pipeline (`rag/ingest.py`) handles this, but for production with frequent updates:

**Full re-indexing**: For small knowledge bases (< 5,000 docs), simply re-run `ingest.py` after any change. ChromaDB's `from_documents` overwrites the collection cleanly. This can be automated via a CI/CD GitHub Actions workflow triggered on commits to `knowledge_base/`.

**Incremental updates**: For larger knowledge bases, track a hash (MD5/SHA256) of each file's content. On each run, only re-embed documents whose hash has changed. Store the hash index alongside ChromaDB.

**Version-safe deployments**: Keep the old collection alive under a versioned name (e.g. `support_docs_v1`) while the new one (`support_docs_v2`) is being built. Swap the active collection name in config only after the new index is fully ready, ensuring zero-downtime updates.

---

### 3. How would you detect retrieval failures?

A retrieval failure occurs when the system returns chunks that are not relevant to the question, leading to poor or hallucinated answers. Ways to detect this:

**Similarity threshold checks**: After retrieval, check the cosine similarity of the top-1 chunk against the query. If it falls below a threshold (e.g. 0.35), log it as a likely retrieval failure and return a fallback response.

**Source mismatch monitoring**: Log the question and retrieved sources for every request. If the same question repeatedly retrieves different or unexpected sources, it signals instability in the index or chunking.

**User feedback signals**: Add a simple thumbs up/down feedback button to the UI or API response. Negative feedback correlated with specific queries highlights retrieval failures quickly.

**Automated regression testing**: Run `eval/evaluate.py` as part of CI. A drop in context recall below a threshold (e.g. < 85%) after a knowledge base update triggers an alert before the change ships to production.

---

### 4. How would you scale to 10 million documents?

At 10M documents, ChromaDB running locally is no longer viable. The changes needed:

**Managed vector store**: Switch to a distributed vector database like Pinecone, Weaviate, or Qdrant. These support horizontal sharding, approximate nearest neighbour (ANN) search (e.g. HNSW), and can handle hundreds of millions of vectors with sub-100ms retrieval.

**Embedding at scale**: Use batch embedding with parallel workers (e.g. via Celery or Ray). If using a hosted embedding API, implement rate limiting and retry logic. For self-hosted embedding, deploy the model on GPU instances and batch the requests.

**Chunking strategy**: At this scale, chunk IDs should be deterministic (based on a hash of document content + position), enabling idempotent re-indexing. A metadata store (e.g. PostgreSQL) should track which documents have been indexed and when.

**Tiered retrieval**: Use a two-stage retrieval approach — first retrieve a larger candidate set cheaply (top-50 via ANN), then re-rank using a cross-encoder model (e.g. `cross-encoder/ms-marco-MiniLM-L-6-v2`) to select the final top-5. This trades off speed for precision at large scales.

---

### 5. How would you reduce the cost of LLM usage?

**Choose a smaller/cheaper model**: We already use `llama-3.1-8b-instant` via Groq (free tier). For paid deployments, `gpt-4o-mini` is ~20x cheaper than `gpt-4` with minimal quality loss for Q&A tasks.

**Cache frequent answers**: Store (query_embedding, answer) pairs in Redis. For incoming queries, check if a sufficiently similar query has been answered before (cosine similarity > 0.97). Return the cached answer instead of calling the LLM. This can eliminate 30–50% of LLM calls for typical support Q&A workloads.

**Limit context size**: Only pass the top-3 chunks instead of top-5 to the LLM when the question is simple. Fewer tokens = lower cost. This can be dynamic — short questions get fewer chunks; ambiguous ones get more.

**Prompt compression**: Use a prompt compressor (e.g. LLMLingua) to shorten retrieved chunks while preserving key information, reducing input tokens by 30–50% with minimal impact on answer quality.

**Async batching**: For non-real-time use cases (e.g. batch report generation), group multiple queries and process them together. Some LLM providers offer batch API pricing at 50% discount.

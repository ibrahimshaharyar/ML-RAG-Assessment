# ML RAG Assessment — Customer Support Assistant

A production-ready Retrieval-Augmented Generation (RAG) system that answers customer support questions using a knowledge base of 30 markdown documents.

**Live stack:** HuggingFace Embeddings · ChromaDB · Groq Llama 3 · FastAPI · Docker

---

## Quick Start

### Prerequisites
- Python 3.11, conda
- A free [Groq API key](https://console.groq.com)

### 1. Set up environment

```bash
conda create -n rag_assessment python=3.11 -y
conda activate rag_assessment
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set GROQ_API_KEY=gsk_...
```

### 3. Build the vector store

```bash
python -m rag.ingest
```

Loads all 30 docs from `knowledge_base/`, chunks, embeds, and stores in ChromaDB. First run downloads the embedding model (~90MB).

### 4. Run the API + chat UI

```bash
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000** — you'll see the chat interface.

### 5. Or run with Docker

```bash
docker-compose up --build
```

Then open **http://localhost:8000**.

---

## Project Structure

```
.
├── knowledge_base/        # 30 markdown support documents
├── rag/
│   ├── ingest.py          # Load → chunk → embed → store to ChromaDB
│   ├── retrieve.py        # Query ChromaDB, return top-k chunks
│   └── query.py           # Full pipeline: retrieve + Groq LLM → answer
├── app/
│   └── main.py            # FastAPI server (GET / serves chat UI, POST /ask)
├── frontend/
│   └── index.html         # ChatGPT-style chat interface
├── eval/
│   ├── evaluate.py        # Evaluation: context recall, cosine sim, faithfulness
│   └── test_questions.json # 20 Q&A test pairs
├── docs/
│   ├── system_design.md   # Architecture, MLOps, scaling, evaluation
│   └── production_thinking.md  # Production Q&A (hallucinations, scaling, cost)
├── config.yaml            # Tunable parameters (chunk size, model, top-k)
├── .env.example           # Environment variable template
├── Dockerfile
└── docker-compose.yml
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/`      | Chat UI     |
| `GET`  | `/health` | Health check |
| `POST` | `/ask`   | Submit a question |

**POST /ask** example:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset my password?"}'
```

Response:
```json
{
  "question": "How do I reset my password?",
  "answer": "To reset your password, go to the login page and click Forgot Password...",
  "sources": ["02_password_reset.md"]
}
```

---

## Evaluation Results

Run the evaluation suite:
```bash
python -m eval.evaluate
```

| Metric | Score |
|--------|-------|
| Context Recall | **100%** (20/20 correct docs retrieved) |
| Avg Cosine Similarity | 0.51 |
| Answer Relevance | **89.3%** |
| Faithfulness | **95.0%** |

---

## Configuration

All tuneable parameters are in `config.yaml`:

```yaml
chunking:
  chunk_size: 500
  chunk_overlap: 50

retrieval:
  top_k: 5

llm:
  model: llama-3.1-8b-instant
  temperature: 0.2

embeddings:
  model: all-MiniLM-L6-v2
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Groq — `llama-3.1-8b-instant` (free) |
| Embeddings | HuggingFace — `all-MiniLM-L6-v2` (free, local) |
| Vector Store | ChromaDB (persistent) |
| API Framework | FastAPI + Uvicorn |
| Containerisation | Docker + Docker Compose |
| Evaluation | Custom eval with LLM-as-judge |

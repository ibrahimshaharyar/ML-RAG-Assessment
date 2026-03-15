# ML RAG Assessment

A production-grade Retrieval-Augmented Generation (RAG) customer support assistant built with Python, LangChain, ChromaDB, and OpenAI.

---

## Project Structure

```
ml-rag-assessment/
├── docs/                          # Part 1 & 4 documents
│   ├── system_design.md
│   └── production_thinking.md
├── knowledge_base/                # 30 markdown knowledge base docs
├── rag/
│   ├── ingest.py                  # Chunk, embed, store to ChromaDB
│   ├── retrieve.py                # Query ChromaDB, return top-k chunks
│   └── query.py                   # CLI: question → answer
├── eval/
│   ├── test_questions.json
│   └── evaluate.py                # Retrieval recall + answer quality
├── app/
│   └── main.py                    # FastAPI: POST /ask
├── config.yaml                    # All tuneable parameters
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## Quickstart

### 1. Clone & Setup

```bash
git clone https://github.com/YOUR_USERNAME/ml-rag-assessment.git
cd ml-rag-assessment

python3.11 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Ingest Documents

```bash
python rag/ingest.py
```

### 4. Ask a Question (CLI)

```bash
python rag/query.py "How do I reset my password?"
```

### 5. Run the API Server

```bash
uvicorn app.main:app --reload --port 8000
```

Then send a request:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset my password?"}'
```

---

## Docker

### Build & Run

```bash
# First, ingest documents into ChromaDB
python rag/ingest.py

# Then build and run the container
docker-compose up --build
```

The API will be available at `http://localhost:8000`

---

## Configuration

All parameters are in `config.yaml`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `chunking.chunk_size` | 500 | Characters per chunk |
| `chunking.chunk_overlap` | 50 | Overlap between chunks |
| `retrieval.top_k` | 5 | Number of chunks to retrieve |
| `llm.model` | `gpt-4o-mini` | OpenAI model to use |
| `embeddings.model` | `text-embedding-3-small` | Embedding model |

---

## Evaluation

```bash
python eval/evaluate.py
```

Outputs retrieval recall and answer relevance scores.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11 |
| RAG Framework | LangChain 0.2.16 |
| Vector Store | ChromaDB 0.5.15 |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| API | FastAPI 0.115.0 |
| Deployment | Docker + Render |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ | Your OpenAI API key |
| `CHROMA_PERSIST_DIR` | Optional | Path for ChromaDB (default: `./chroma_db`) |
| `COLLECTION_NAME` | Optional | ChromaDB collection name (default: `support_docs`) |

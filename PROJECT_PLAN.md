# ML Assessment — RAG Project Plan

## Overview
Build a Production-grade RAG (Retrieval-Augmented Generation) customer support assistant
using Python, ChromaDB, LangChain, and OpenAI. Deployed via Docker on Render.

---

## Task-by-Task Breakdown

### Phase 0 — Project Setup
1. Create folder structure (see below)
2. Initialize Git repo + `.gitignore` + `.env` (not committed)
3. Set up Python 3.11 virtual environment
4. Install and pin all libraries in `requirements.txt`
5. Create `config.yaml` with all tuneable parameters
6. Generate 20–30 markdown knowledge base documents

### Phase 1 — RAG Pipeline (Part 2)
7. `rag/ingest.py` — Load markdown files → chunk → embed → store in ChromaDB
8. `rag/retrieve.py` — Query ChromaDB → return top-k relevant chunks
9. `rag/query.py` — CLI: take user question → retrieve → send to LLM → print answer
10. End-to-end test: `python rag/query.py "How do I reset my password?"`
11. Write `README.md`

### Phase 2 — MLOps Engineering (Part 3, Options B & C)
12. `eval/evaluate.py` — Evaluate retrieval recall + answer relevance on test set
13. `app/main.py` — FastAPI app with `POST /ask` endpoint
14. `Dockerfile` — Containerize the FastAPI app
15. `docker-compose.yml` — Orchestrate app + ChromaDB volume
16. Local Docker test: build → run → hit the endpoint

### Phase 3 — System Design Document (Part 1)
17. `docs/system_design.md` — Full architecture document with diagram
    - RAG architecture, MLOps, Scaling, Evaluation sections

### Phase 4 — Production Thinking (Part 4)
18. `docs/production_thinking.md` — Answer all 5 production questions

### Phase 5 — Final Polish
19. Full end-to-end test
20. Docker container verified working
21. GitHub push verified (no secrets, no large files)

---

## Python & Library Versions (Render-Safe)

> These versions are tested to be compatible with Python 3.11 and Render's Docker environment.

```
# requirements.txt

python==3.11.x   # (set in Dockerfile)

# Core
langchain==0.2.16
langchain-community==0.2.16
langchain-openai==0.1.23
openai==1.45.0

# Vector Store
chromadb==0.5.15

# Embeddings (if using local HuggingFace instead of OpenAI)
sentence-transformers==3.0.1

# Document loading
unstructured==0.15.0

# API
fastapi==0.115.0
uvicorn==0.30.6

# Evaluation
ragas==0.1.21
datasets==2.21.0

# Utils
python-dotenv==1.0.1
pyyaml==6.0.2
tiktoken==0.7.0
numpy==1.26.4
pandas==2.2.2
```

### Why these specific versions?
- **Python 3.11** — Stable, widely supported on Render, avoids Python 3.12 breaking changes
- **numpy==1.26.4** — Last stable before 2.x; prevents `numpy._core` ModuleNotFoundError on Render
- **chromadb==0.5.15** — Stable release with full SQLite persistence support
- **langchain==0.2.16** — Stable non-breaking LTS-style release
- **openai==1.45.0** — Compatible with the new `openai` v1 client API

---

## Folder Structure

```
ml-rag-assessment/
│
├── docs/
│   ├── system_design.md          # Part 1: Architecture document
│   └── production_thinking.md    # Part 4: Production Q&A
│
├── knowledge_base/               # Your 20-30 markdown documents
│   ├── account_management.md
│   ├── billing_faq.md
│   ├── password_reset.md
│   └── ... (more .md files)
│
├── rag/
│   ├── __init__.py
│   ├── ingest.py                 # Chunk + embed + store to ChromaDB
│   ├── retrieve.py               # Query ChromaDB, return top-k chunks
│   └── query.py                  # CLI: question → retrieve → LLM → answer
│
├── eval/
│   ├── __init__.py
│   ├── test_questions.json       # Q&A pairs for evaluation
│   └── evaluate.py               # Retrieval recall + answer quality metrics
│
├── app/
│   ├── __init__.py
│   └── main.py                   # FastAPI: POST /ask, GET /health
│
├── chroma_db/                    # ChromaDB persisted data (git-ignored)
│
├── .env                          # API keys (NEVER committed)
├── .env.example                  # Template for env vars (committed)
├── .gitignore
├── config.yaml                   # Chunking, model, retrieval settings
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## How to Get 20–30 Markdown Documents

You do NOT need to scrape or download anything. **Generate them yourself** — they simulate a company's support knowledge base. Here are the topics to create:

```
knowledge_base/
  01_account_creation.md
  02_password_reset.md
  03_two_factor_auth.md
  04_login_issues.md
  05_account_deletion.md
  06_billing_overview.md
  07_subscription_plans.md
  08_invoice_download.md
  09_payment_methods.md
  10_refund_policy.md
  11_api_key_management.md
  12_rate_limits.md
  13_webhook_setup.md
  14_sdk_quickstart.md
  15_authentication_guide.md
  16_data_export.md
  17_gdpr_compliance.md
  18_privacy_policy.md
  19_security_overview.md
  20_sso_setup.md
  21_team_management.md
  22_role_permissions.md
  23_audit_logs.md
  24_integrations_overview.md
  25_slack_integration.md
  26_zapier_integration.md
  27_error_codes_reference.md
  28_contact_support.md
  29_sla_policy.md
  30_changelog.md
```

> I can generate all 30 markdown files for you automatically — just say the word.

---

## ChromaDB Configuration

ChromaDB will be used in **persistent mode** (saved to disk, not in-memory).

```yaml
# config.yaml
vector_store:
  provider: chromadb
  persist_directory: ./chroma_db
  collection_name: support_docs

chunking:
  chunk_size: 500
  chunk_overlap: 50

retrieval:
  top_k: 5

llm:
  provider: openai
  model: gpt-4o-mini       # cheaper than gpt-4, still excellent
  temperature: 0.2

embeddings:
  provider: openai
  model: text-embedding-3-small
```

**Why `gpt-4o-mini`?** Fast, cheap, and accurate for Q&A tasks. Reduces cost significantly.

---

## Git Repository — Avoiding Push Errors

### `.gitignore` (critical entries)
```gitignore
# Secrets
.env

# ChromaDB data (large binary files)
chroma_db/

# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
env/

# OS
.DS_Store
Thumbs.db

# Large model files
*.bin
*.pt
*.onnx
*.pkl

# Jupyter
.ipynb_checkpoints/

# Docker
*.log
```

### Rules to follow:
1. **Never commit `.env`** — use `.env.example` with placeholder values instead
2. **Never commit `chroma_db/`** — it's a binary database, will bloat Git history
3. **Use `git status` before every commit** to verify what you're staging
4. Run `pip freeze > requirements.txt` after installing anything new
5. Use meaningful commit messages: `feat: add ingest pipeline`, `fix: retrieval top-k bug`

### Initial Git Setup Commands:
```bash
git init
git add .gitignore
git commit -m "chore: initial project structure"

git remote add origin https://github.com/YOUR_USERNAME/ml-rag-assessment.git
git branch -M main
git push -u origin main
```

---

## Docker Setup (for Render Deployment)

### `Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-build the ChromaDB index if docs are bundled
# RUN python rag/ingest.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `docker-compose.yml`
```yaml
version: "3.9"

services:
  rag-app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./chroma_db:/app/chroma_db
      - ./knowledge_base:/app/knowledge_base
```

### Render Deployment Notes:
- Set environment variables (like `OPENAI_API_KEY`) in **Render Dashboard → Environment**
- Use a **Docker** service type on Render
- Mount a persistent disk at `/app/chroma_db` so embeddings survive restarts
- Make sure `Dockerfile` is at the root of the repo

---

## Environment Variables (`.env.example`)
```env
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_PERSIST_DIR=./chroma_db
COLLECTION_NAME=support_docs
```

---

## Summary Checklist

| # | Task | Status |
|---|------|--------|
| 1 | Project structure + Git setup | ⬜ |
| 2 | Generate 30 markdown docs | ⬜ |
| 3 | `rag/ingest.py` | ⬜ |
| 4 | `rag/retrieve.py` | ⬜ |
| 5 | `rag/query.py` (CLI) | ⬜ |
| 6 | `app/main.py` (FastAPI) | ⬜ |
| 7 | `eval/evaluate.py` | ⬜ |
| 8 | `Dockerfile` + `docker-compose.yml` | ⬜ |
| 9 | `docs/system_design.md` | ⬜ |
| 10 | `docs/production_thinking.md` | ⬜ |
| 11 | Full test + Docker build | ⬜ |
| 12 | Push to GitHub | ⬜ |

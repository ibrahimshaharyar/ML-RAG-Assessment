"""
app/main.py — FastAPI server exposing the RAG pipeline via REST API.

Endpoints:
    GET  /health      — Health check
    POST /ask         — Submit a question, get an answer + sources
"""

import yaml
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from rag.retrieve import load_vectorstore
from rag.query import generate_answer, load_config

# ── Startup ───────────────────────────────────────────────────────────────────
load_dotenv()

# Shared state: load vectorstore once at startup for performance
_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the ChromaDB vectorstore once when the server starts."""
    print("🚀 Loading ChromaDB vectorstore...")
    config = load_config()
    _state["config"] = config
    _state["vectorstore"] = load_vectorstore(config)
    print("✅ Vectorstore loaded. Server ready.")
    yield
    _state.clear()


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ML RAG Assessment API",
    description="Customer support RAG assistant — ask questions about our knowledge base.",
    version="1.0.0",
    lifespan=lifespan,
)


# ── Schemas ───────────────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str

    class Config:
        json_schema_extra = {
            "example": {"question": "How do I reset my password?"}
        }


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    """Returns 200 OK if the server is running."""
    return {"status": "ok", "message": "RAG API is running"}


@app.post("/ask", response_model=AskResponse, tags=["RAG"])
def ask(request: AskRequest):
    """
    Submit a question and receive an answer generated from the knowledge base.

    - **question**: The question to ask (string, required)
    """
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if len(question) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Question is too long. Maximum 1000 characters.",
        )

    try:
        result = generate_answer(
            question=question,
            config=_state["config"],
            vectorstore=_state["vectorstore"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your question: {str(e)}",
        )

    return AskResponse(
        question=result["question"],
        answer=result["answer"],
        sources=result["sources"],
    )

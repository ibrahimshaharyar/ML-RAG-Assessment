"""
app/main.py
FastAPI server exposing the RAG pipeline via REST API
and serving the chat frontend UI.

Endpoints:
    GET  /          — Chat UI (frontend)
    GET  /health    — Health check
    POST /ask       — Submit a question, get an answer + sources
"""

from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

from rag.retrieve import load_vectorstore
from rag.query import generate_answer, load_config

load_dotenv()

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

_state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading ChromaDB vectorstore...")
    config = load_config()
    _state["config"] = config
    _state["vectorstore"] = load_vectorstore(config)
    print("Vectorstore loaded. Server ready.")
    yield
    _state.clear()


app = FastAPI(
    title="ML RAG Assessment API",
    description="Customer support RAG assistant.",
    version="1.0.0",
    lifespan=lifespan,
)

# Serve the frontend
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]


@app.get("/", include_in_schema=False)
def serve_ui():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "RAG API is running"}


@app.post("/ask", response_model=AskResponse, tags=["RAG"])
def ask(request: AskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if len(question) > 1000:
        raise HTTPException(status_code=400, detail="Question is too long. Maximum 1000 characters.")

    try:
        result = generate_answer(
            question=question,
            config=_state["config"],
            vectorstore=_state["vectorstore"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

    return AskResponse(
        question=result["question"],
        answer=result["answer"],
        sources=result["sources"],
    )

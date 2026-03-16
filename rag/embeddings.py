"""
rag/embeddings.py
Lightweight ONNX-based embeddings using ChromaDB's built-in model.
Same all-MiniLM-L6-v2 as before but runs via ONNX Runtime — no PyTorch needed.
This keeps memory well under Render's 512MB free tier limit.
"""

from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
from langchain_core.embeddings import Embeddings


class ONNXEmbeddings(Embeddings):
    """Wraps ChromaDB's built-in ONNX embedding function for LangChain compatibility."""

    def __init__(self):
        self._fn = ONNXMiniLM_L6_V2()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._fn(texts)

    def embed_query(self, text: str) -> list[float]:
        return self._fn([text])[0]

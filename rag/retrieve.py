"""
retrieve.py
Loads a persisted ChromaDB vectorstore and returns the most
relevant chunks for a given query using cosine similarity.

Standalone test:
    python -m rag.retrieve "How do I reset my password?"
"""

import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def load_vectorstore(config):
    persist_dir = config["vector_store"]["persist_directory"]
    collection = config["vector_store"]["collection_name"]
    model_name = config["embeddings"]["model"]

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    return Chroma(
        collection_name=collection,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )


def retrieve(query, config, vectorstore=None):
    """
    Returns the top-k most relevant document chunks for a query.
    Accepts an optional pre-loaded vectorstore to avoid reloading on each call.
    """
    if vectorstore is None:
        vectorstore = load_vectorstore(config)

    top_k = config["retrieval"]["top_k"]
    return vectorstore.similarity_search(query, k=top_k)


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m rag.retrieve \"your question here\"")
        sys.exit(1)

    query = sys.argv[1]
    config = load_config()
    results = retrieve(query, config)

    print(f"\nQuery: {query}\n")
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "unknown")
        print(f"[{i}] Source: {source}")
        print(doc.page_content[:300])
        print()


if __name__ == "__main__":
    main()

"""
ingest.py
Loads markdown files from the knowledge base, splits them into chunks,
embeds them using HuggingFace, and stores everything in ChromaDB.

Run this once before querying:
    python -m rag.ingest
"""

import os
import glob
import yaml
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from rag.embeddings import ONNXEmbeddings

load_dotenv()

CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def load_documents(docs_dir, extension="*.md"):
    pattern = os.path.join(docs_dir, extension)
    filepaths = sorted(glob.glob(pattern))

    if not filepaths:
        raise FileNotFoundError(f"No markdown files found in: {docs_dir}")

    documents = []
    for filepath in filepaths:
        loader = TextLoader(filepath, encoding="utf-8")
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = os.path.basename(filepath)
        documents.extend(docs)

    print(f"Loaded {len(documents)} documents from {docs_dir}")
    return documents


def chunk_documents(documents, chunk_size, chunk_overlap):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap})")
    return chunks


def embed_and_store(chunks, config):
    persist_dir = config["vector_store"]["persist_directory"]
    collection = config["vector_store"]["collection_name"]
    model_name = config["embeddings"]["model"]

    print("Embedding chunks with ONNX all-MiniLM-L6-v2 (lightweight, no PyTorch) ...")

    embeddings = ONNXEmbeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection,
        persist_directory=persist_dir,
    )

    print(f"Stored in ChromaDB at {persist_dir} (collection: {collection})")
    return vectorstore


def main():
    config = load_config()

    project_root = Path(__file__).parent.parent
    docs_dir = str(project_root / config["knowledge_base"]["docs_directory"].lstrip("./"))

    documents = load_documents(docs_dir, config["knowledge_base"]["file_extension"])
    chunks = chunk_documents(
        documents,
        chunk_size=config["chunking"]["chunk_size"],
        chunk_overlap=config["chunking"]["chunk_overlap"],
    )
    embed_and_store(chunks, config)
    print("Ingestion complete. ChromaDB is ready.")


if __name__ == "__main__":
    main()

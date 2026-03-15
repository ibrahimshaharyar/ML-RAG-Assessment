"""
query.py
Full RAG pipeline: takes a question, retrieves relevant chunks from
ChromaDB, and generates an answer using Groq's Llama model.

Usage:
    python -m rag.query "How do I reset my password?"
"""

import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from rag.retrieve import load_config, load_vectorstore, retrieve

load_dotenv()

SYSTEM_PROMPT = """You are a helpful customer support assistant.
Answer the user's question using ONLY the context provided below.
If the answer is not covered in the context, say: "I don't have information on that in our knowledge base."
Be concise, clear, and friendly."""


def build_messages(question, chunks):
    context = "\n\n---\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in chunks
    )
    return [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {question}"),
    ]


def generate_answer(question, config, vectorstore=None):
    chunks = retrieve(question, config, vectorstore)

    if not chunks:
        return {
            "question": question,
            "answer": "I couldn't find relevant information in the knowledge base.",
            "sources": [],
        }

    messages = build_messages(question, chunks)

    llm = ChatGroq(
        model=config["llm"]["model"],
        temperature=config["llm"]["temperature"],
        max_tokens=config["llm"]["max_tokens"],
    )

    response = llm.invoke(messages)

    sources = list(dict.fromkeys(
        doc.metadata.get("source", "unknown") for doc in chunks
    ))

    return {
        "question": question,
        "answer": response.content,
        "sources": sources,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m rag.query \"your question here\"")
        sys.exit(1)

    question = sys.argv[1]
    config = load_config()
    vectorstore = load_vectorstore(config)

    result = generate_answer(question, config, vectorstore)

    print(f"\nQuestion: {result['question']}\n")
    print(f"Answer:\n{result['answer']}\n")
    print(f"Sources: {', '.join(result['sources'])}\n")


if __name__ == "__main__":
    main()

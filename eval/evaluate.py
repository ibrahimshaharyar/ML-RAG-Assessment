"""
evaluate.py
Evaluates the RAG pipeline on a set of test questions.

Measures:
  - Context Recall: did the correct source document appear in top-k results?
  - Avg Cosine Similarity: how closely matched are retrieved chunks to the query?
  - Answer Relevance: does the generated answer address the question? (via Groq)
  - Faithfulness: is the answer grounded in the retrieved context? (via Groq)

Usage:
    python -m eval.evaluate
"""

import sys
import json
import time
import yaml
import numpy as np
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage

from rag.retrieve import load_config, load_vectorstore, retrieve
from rag.query import generate_answer

load_dotenv()

TEST_FILE = Path(__file__).parent / "test_questions.json"


def load_test_questions():
    with open(TEST_FILE, "r") as f:
        return json.load(f)


def compute_cosine_similarity(vec_a, vec_b):
    a = np.array(vec_a)
    b = np.array(vec_b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


def evaluate_retrieval(test_cases, config, vectorstore, embeddings_model):
    """
    For each question, check if the expected source appears in top-k results.
    Also compute average cosine similarity of retrieved chunks to the query.
    """
    recalls = []
    similarities = []

    for case in test_cases:
        question = case["question"]
        expected = case["expected_source"]

        chunks = retrieve(question, config, vectorstore)
        retrieved_sources = [c.metadata.get("source", "") for c in chunks]

        # Context recall — did we retrieve the right doc?
        hit = expected in retrieved_sources
        recalls.append(1 if hit else 0)

        # Cosine similarity — embed query and compare to each chunk
        query_vec = embeddings_model.embed_query(question)
        chunk_sims = []
        for chunk in chunks:
            chunk_vec = embeddings_model.embed_query(chunk.page_content)
            chunk_sims.append(compute_cosine_similarity(query_vec, chunk_vec))

        if chunk_sims:
            similarities.append(np.mean(chunk_sims))

    return {
        "context_recall": round(np.mean(recalls), 4),
        "recall_details": recalls,
        "avg_cosine_similarity": round(np.mean(similarities), 4),
    }


def evaluate_answer_quality(test_cases, config, vectorstore, llm):
    """
    Uses the LLM to score answer relevance and faithfulness for each question.
    Returns scores between 0.0 and 1.0.
    """

    relevance_prompt = """You are an evaluator. Given a question and an answer, rate how well the answer addresses the question.
Return ONLY a number between 0.0 and 1.0 (e.g. 0.85). No explanation."""

    faithfulness_prompt = """You are an evaluator. Given a context and an answer, rate how well the answer is grounded in the context without making things up.
Return ONLY a number between 0.0 and 1.0 (e.g. 0.90). No explanation."""

    relevance_scores = []
    faithfulness_scores = []

    for i, case in enumerate(test_cases):
        question = case["question"]

        result = generate_answer(question, config, vectorstore)
        answer = result["answer"]
        context = "\n\n".join(
            c.page_content for c in retrieve(question, config, vectorstore)
        )

        # Score relevance
        try:
            r_response = llm.invoke([
                SystemMessage(content=relevance_prompt),
                HumanMessage(content=f"Question: {question}\n\nAnswer: {answer}"),
            ])
            relevance_scores.append(float(r_response.content.strip()))
        except Exception:
            relevance_scores.append(0.0)

        # Score faithfulness
        try:
            f_response = llm.invoke([
                SystemMessage(content=faithfulness_prompt),
                HumanMessage(content=f"Context:\n{context}\n\nAnswer: {answer}"),
            ])
            faithfulness_scores.append(float(f_response.content.strip()))
        except Exception:
            faithfulness_scores.append(0.0)

        # Small delay to avoid rate limiting
        time.sleep(0.5)

        if (i + 1) % 5 == 0:
            print(f"  Evaluated {i + 1}/{len(test_cases)} questions...")

    return {
        "avg_answer_relevance": round(np.mean(relevance_scores), 4),
        "avg_faithfulness": round(np.mean(faithfulness_scores), 4),
    }


def print_report(retrieval_results, quality_results, total):
    correct = sum(retrieval_results["recall_details"])
    print("\n" + "=" * 50)
    print("RAG Evaluation Report")
    print("=" * 50)
    print(f"Questions tested     : {total}")
    print(f"Context Recall       : {retrieval_results['context_recall']:.2%}  ({correct}/{total} correct docs retrieved)")
    print(f"Avg Cosine Similarity: {retrieval_results['avg_cosine_similarity']:.4f}")
    print(f"Answer Relevance     : {quality_results['avg_answer_relevance']:.2%}")
    print(f"Faithfulness         : {quality_results['avg_faithfulness']:.2%}")
    print("=" * 50 + "\n")


def main():
    print("Loading config and models...")
    config = load_config()

    embeddings_model = HuggingFaceEmbeddings(
        model_name=config["embeddings"]["model"],
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vectorstore = load_vectorstore(config)

    llm = ChatGroq(
        model=config["llm"]["model"],
        temperature=0.0,
        max_tokens=10,
    )

    test_cases = load_test_questions()
    print(f"Running evaluation on {len(test_cases)} test questions...\n")

    print("Step 1/2: Evaluating retrieval...")
    retrieval_results = evaluate_retrieval(test_cases, config, vectorstore, embeddings_model)

    print("Step 2/2: Evaluating answer quality...")
    quality_results = evaluate_answer_quality(test_cases, config, vectorstore, llm)

    print_report(retrieval_results, quality_results, len(test_cases))


if __name__ == "__main__":
    main()

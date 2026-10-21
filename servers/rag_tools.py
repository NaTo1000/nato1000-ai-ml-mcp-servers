"""
RAG (Retrieval-Augmented Generation) Tools MCP Server for NATO1000
Document chunking, retrieval simulation, and prompt construction.
"""
from fastmcp import FastMCP
from typing import List, Dict, Any
import re

mcp = FastMCP(name="NATO1000 RAG Tools")

@mcp.tool()
def chunk_documents(texts: List[str], chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, Any]]:
    """Split documents into overlapping chunks for retrieval."""
    chunks = []
    for doc_id, text in enumerate(texts):
        words = text.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            chunks.append({
                "doc_id": doc_id,
                "chunk_id": len(chunks),
                "text": chunk_text,
                "start": i,
                "length": len(chunk_text)
            })
    return chunks

@mcp.tool()
def simulate_retrieval(query: str, chunks: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    """Simple keyword-overlap retrieval simulation (replace with real embeddings in production)."""
    query_words = set(re.findall(r'\w+', query.lower()))
    scored = []
    for chunk in chunks:
        chunk_words = set(re.findall(r'\w+', chunk["text"].lower()))
        overlap = len(query_words & chunk_words)
        scored.append({**chunk, "score": overlap})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]

@mcp.tool()
def build_rag_prompt(query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    """Construct a RAG prompt with context from retrieved chunks."""
    context = "\n\n".join([f"[Source {c['doc_id']}-{c['chunk_id']}]: {c['text']}" for c in retrieved_chunks])
    return f"""Use the following context to answer the question.

Context:
{context}

Question: {query}

Answer based only on the context above. If the answer is not in the context, say so."""

if __name__ == "__main__":
    mcp.run()

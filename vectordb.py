import os
import re
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

FAISS_DB_PATH    = "vectorstore/db_faiss"
EMBEDDING_MODEL  = "all-MiniLM-L6-v2"
PDF_PATH         = "ASISSE ChatBot-2025-11-26 1.pdf"


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_file(path: str):
    loader = PDFPlumberLoader(path)
    return loader.load()


def create_chunks(documents):
    documents = sorted(documents, key=lambda d: d.metadata.get("page", 0))
    full_text = " ".join([doc.page_content for doc in documents])
    full_text = re.sub(r"\s+", " ", full_text)

    pattern = r"Qn:\s*(.*?)\s*Ans:\s*(.*?)(?=Qn:|$)"
    matches = re.findall(pattern, full_text, re.DOTALL)

    chunks = []
    for i, (question, answer) in enumerate(matches):
        question = question.strip()
        answer   = answer.strip()
        if len(question) < 5 or len(answer) < 5:
            continue
        chunks.append(Document(
            page_content=f"Question: {question}\nAnswer: {answer}",
            metadata={"question": question, "chunk_id": i}
        ))

    print(f"[vectordb] Total Q&A chunks: {len(chunks)}")
    return chunks


def build_and_save():
    """Parse PDF → create chunks → embed → save FAISS index to disk."""
    print("[vectordb] Building index from PDF (this runs only once)...")
    documents = load_file(PDF_PATH)
    chunks    = create_chunks(documents)
    embeddings = get_embedding_model()
    db = FAISS.from_documents(chunks, embeddings)
    os.makedirs(FAISS_DB_PATH, exist_ok=True)
    db.save_local(FAISS_DB_PATH)
    print(f"[vectordb] Index saved to {FAISS_DB_PATH}")
    return db


def load_faiss():
    """Load from disk if exists, otherwise build and save first."""
    embeddings = get_embedding_model()
    # ── KEY FIX: load from disk instead of rebuilding every time ──
    if os.path.exists(os.path.join(FAISS_DB_PATH, "index.faiss")):
        print("[vectordb] Loading existing index from disk...")
        return FAISS.load_local(FAISS_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        return build_and_save()


# Load once when imported — fast on subsequent runs
faiss_db = load_faiss()
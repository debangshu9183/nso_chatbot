import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from vectordb import faiss_db
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")  # must match .env exactly
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

model = ChatGroq(api_key=groq_api_key, model="llama-3.3-70b-versatile")

# ── Prompt ────────────────────────────────────────────────────────
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant for ASISSE survey documentation.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't have information on that."

Context:
{context}

Question: {question}
""")

# ── Retrieve & format ─────────────────────────────────────────────
def retrieve_chunks(query, top_k=3):
    return faiss_db.similarity_search(query, k=top_k)

def format_context(chunks):
    return "\n\n".join([chunk.page_content for chunk in chunks])

# ── RAG Chain ─────────────────────────────────────────────────────
rag_chain = (
    {
        "context":  lambda x: format_context(retrieve_chunks(x["question"])),
        "question": lambda x: x["question"]
    }
    | prompt
    | model
    | StrOutputParser()
)

def ask(question: str) -> str:
    return rag_chain.invoke({"question": question})


# ── CLI mode ──────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        query = input("\nYou: ").strip()
        if query.lower() in ["exit", "quit"]:
            break
        print(f"\nBot: {ask(query)}")
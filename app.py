"""
app.py — FastAPI backend for ASISSE RAG Chatbot
Run: uvicorn app:app --reload --port 8000
Then open: http://127.0.0.1:8000
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rag_pipeline import ask

# Resolve paths relative to this file — works no matter where you run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="ASISSE Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    answer = ask(req.question)
    return ChatResponse(answer=answer)


@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)


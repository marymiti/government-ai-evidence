
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Government AI Evidence Service",
    version="0.1.0"
)


class Question(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ask")
def ask(data: Question):
    return {
        "question": data.question,
        "answer": "The evidence retrieval system is being built.",
        "status": "development"
    }

from evidence_service import retrieve_evidence


@app.post("/evidence/query")
def evidence_query(data: Question):
    return retrieve_evidence(data.question)


import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATA_FILE = Path(__file__).parent / "data" / "evidence.json"

with DATA_FILE.open(encoding="utf-8") as file:
    DOCUMENTS = json.load(file)

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)

corpus = [
    document["section"] + " " + document["text"]
    for document in DOCUMENTS
]

document_vectors = vectorizer.fit_transform(corpus)


def retrieve_evidence(question: str):
    if not question.strip():
        return {
            "classification": "AMBIGUOUS",
            "status": "CLARIFICATION_REQUIRED",
            "answer": "Please provide a specific question.",
            "citations": []
        }

    query_vector = vectorizer.transform([question])

    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]

    best_index = int(similarities.argmax())
    best_score = float(similarities[best_index])

    if best_score < 0.15:
        return {
            "classification": "OUT_OF_SCOPE",
            "status": "REFUSED",
            "answer": "No sufficiently relevant evidence was found.",
            "citations": []
        }

    document = DOCUMENTS[best_index]

    return {
        "classification": "IN_SCOPE",
        "status": "EVIDENCE_RETRIEVED",
        "answer": document["text"],
        "citations": [
            {
                "document_id": document["id"],
                "section": document["section"],
                "source": document["source"]
            }
        ],
        "retrieval_score": round(best_score, 4)
    }

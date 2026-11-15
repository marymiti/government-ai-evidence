
import pytest
from evidence_service import retrieve_evidence


@pytest.mark.parametrize(
    "question, expected_document",
    [
        (
            "What does government guidance say about human oversight of AI?",
            "AI-001",
        ),
        (
            "How should humans validate high-risk AI decisions?",
            "AI-001",
        ),
        (
            "Why should AI systems be tested before deployment?",
            "AI-001",
        ),
        (
            "How should teams manage the AI lifecycle?",
            "AI-002",
        ),
        (
            "Why is red teaming important for AI systems?",
            "AI-002",
        ),
        (
            "What guidance covers AI transparency and explainability?",
            "AI-003",
        ),
    ],
)
def test_supported_evidence(question, expected_document):
    result = retrieve_evidence(question)

    assert result["classification"] == "IN_SCOPE"
    assert result["status"] == "EVIDENCE_RETRIEVED"
    assert result["citations"]
    assert result["citations"][0]["document_id"] == expected_document


@pytest.mark.parametrize(
    "question",
    [
        "Who won the football match yesterday?",
        "What is the capital of Brazil?",
        "How do I bake a chocolate cake?",
        "What is the weather tomorrow?",
    ],
)
def test_unrelated_questions(question):
    result = retrieve_evidence(question)

    assert result["classification"] == "OUT_OF_SCOPE"
    assert result["status"] == "REFUSED"
    assert result["citations"] == []


def test_empty_question():
    result = retrieve_evidence("")

    assert result["classification"] == "AMBIGUOUS"
    assert result["status"] == "CLARIFICATION_REQUIRED"
    assert result["citations"] == []


def test_citation_has_source():
    result = retrieve_evidence(
        "What does government guidance say about human oversight of AI?"
    )

    assert result["citations"][0]["source"].startswith("https://")


def test_api_returns_structured_evidence():
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)

    response = client.post(
        "/evidence/query",
        json={"question": "What does guidance say about human oversight?"}
    )

    assert response.status_code == 200
    assert response.json()["classification"] == "IN_SCOPE"

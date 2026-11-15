
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ask_endpoint():
    response = client.post(
        "/ask",
        json={"question": "What was net migration in 2025?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "What was net migration in 2025?"
    assert data["status"] == "development"


def test_missing_question():
    response = client.post("/ask", json={})

    assert response.status_code == 422


def test_invalid_question_type():
    response = client.post(
        "/ask",
        json={"question": 123}
    )

    assert response.status_code == 422


def test_unknown_endpoint():
    response = client.get("/nonexistent")

    assert response.status_code == 404

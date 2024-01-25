from fastapi.testclient import TestClient
from api.main import app
import os

client = TestClient(app)

EXAMPLE_URL = os.environ.get("EXAMPLE_URL")


def test_config_endpoint_update_llm():
    response = client.post(
        "/config",
        json={"temperature": 0.5, "top_k": 5, "top_p": 0.8, "max_length": 256},
    )
    assert response.status_code == 200
    assert response.json() is not None


def test_config_endpoint_load_url():
    response = client.post(
        "/config",
        json={"url": EXAMPLE_URL},
    )
    assert response.status_code == 200
    assert response.json() is not None


def test_chat_endpoint():
    response = client.post("/chat", json={"question": "What is the WRF model?"})
    assert response.status_code == 200
    assert "response" in response.json()

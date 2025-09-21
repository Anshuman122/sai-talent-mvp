from fastapi.testclient import TestClient
from ..app.main import app

client = TestClient(app)

def test_get_results_for_existing_athlete():

    response = client.get("/api/v1/results/1")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["id"] == 1
    assert json_response["name"] == "Test Athlete"
    assert "results" in json_response

def test_get_results_for_non_existent_athlete():
    response = client.get("/api/v1/results/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Athlete not found"}

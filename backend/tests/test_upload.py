from fastapi.testclient import TestClient
import pytest
from ..app.main import app
from pathlib import Path
import os

client = TestClient(app)


DUMMY_VIDEO_FILENAME = "test_video.mp4"

@pytest.fixture(scope="module", autouse=True)
def create_dummy_video():
    
    
    with open(DUMMY_VIDEO_FILENAME, "wb") as f:
        f.write(b"dummy video content")
    yield
    
    os.remove(DUMMY_VIDEO_FILENAME)
    for f in Path("uploaded_videos").glob("*"):
        os.remove(f)


def test_upload_video_success():


    client.post("/api/v1/athlete/", json={"name": "Test Athlete", "age": 20, "gender": "male"})

    with open(DUMMY_VIDEO_FILENAME, "rb") as f:
        response = client.post(
            "/api/v1/upload/",
            files={"video_file": (DUMMY_VIDEO_FILENAME, f, "video/mp4")},
            data={"athlete_id": 1, "test_name": "situps"},
        )
    assert response.status_code == 202
    json_response = response.json()
    assert "message" in json_response
    assert json_response["message"] == "Video accepted. Analysis is in progress."
    assert "file_path" in json_response
    assert os.path.exists(json_response["file_path"])

def test_upload_video_athlete_not_found():

    with open(DUMMY_VIDEO_FILENAME, "rb") as f:
        response = client.post(
            "/api/v1/upload/",
            files={"video_file": (DUMMY_VIDEO_FILENAME, f, "video/mp4")},
            data={"athlete_id": 999, "test_name": "vertical_jump"},
        )
    assert response.status_code == 404
    assert response.json() == {"detail": "Athlete not found."}

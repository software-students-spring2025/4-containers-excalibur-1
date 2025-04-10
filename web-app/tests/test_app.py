import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app


def test_upload_image():
    client = app.test_client()

    fake_image = (
        "data:image/png;base64,"
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
    )

    response = client.post("/upload", json={"image": fake_image})
    data = response.get_json()

    assert response.status_code == 200
    assert "id" in data
    assert "timestamp" in data

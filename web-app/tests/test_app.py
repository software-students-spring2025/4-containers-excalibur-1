import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from app import app


def test_upload_image():
    client = app.test_client()
    fake_image = "data:image/jpeg;base64," + "aGVsbG8gd29ybGQ="  # base64 fake data
    response = client.post("/upload", json={"image": fake_image})
    data = response.get_json()
    
    assert response.status_code == 200
    assert "id" in data
    assert "timestamp" in data

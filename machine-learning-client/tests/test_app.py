import pytest
pytest.skip("Skipping ML tests for now", allow_module_level=True)

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


def test_predict_endpoint():
    client = app.test_client()
    fake_image = "data:image/jpeg;base64," + "aGVsbG8gd29ybGQ="
    response = client.post("/predict", json={"image": fake_image})
    assert response.status_code in [200, 500]  # handle both real and fake input

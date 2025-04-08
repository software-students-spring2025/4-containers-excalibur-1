from flask import Flask, render_template, request, jsonify
from fer.fer import FER
import base64
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)
detector = FER()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        img_base64 = data["image"].split(",")[1]
        img_bytes = base64.b64decode(img_base64)
        pil_image = Image.open(BytesIO(img_bytes)).convert("RGB")
        img_np = np.array(pil_image)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Run detection
        emotions = detector.detect_emotions(img_bgr)
        if emotions:
            full_emotions = emotions[0]['emotions']  # Get emotion dict
            return jsonify(full_emotions)
        else:
            return jsonify({"error": "No face detected"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import CORS to handle cross-origin requests
from fer.fer import FER
import base64
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from pymongo import MongoClient
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes and origins (can be restricted as needed)
CORS(app)

# Emotion detector
detector = FER()

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017/")  # Connecting to MongoDB in docker container
db = client['emotion_db']  # Database name
collection = db['emotion_data']  # Collection name

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

        # Run emotion detection
        emotions = detector.detect_emotions(img_bgr)
        if emotions:
            full_emotions = emotions[0]['emotions']  # Get emotion dict
            
            # Prepare data to be saved in MongoDB
            emotion_data = {
                "emotions": full_emotions,
                "timestamp": datetime.utcnow()  # Save the timestamp of when the data is collected
            }

            # Insert into MongoDB
            collection.insert_one(emotion_data)

            return jsonify(full_emotions)
        else:
            return jsonify({"error": "No face detected"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict_from_webapp", methods=["POST"])
def predict_from_webapp():
    try:
        data = request.get_json()
        img_base64 = data["image"].split(",")[1]
        img_bytes = base64.b64decode(img_base64)
        pil_image = Image.open(BytesIO(img_bytes)).convert("RGB")
        img_np = np.array(pil_image)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Run emotion detection
        emotions = detector.detect_emotions(img_bgr)
        if emotions:
            full_emotions = emotions[0]['emotions']  # Get emotion dict
            
            # Prepare data to be saved in MongoDB
            emotion_data = {
                "emotions": full_emotions,
                "timestamp": datetime.utcnow()  # Save the timestamp of when the data is collected
            }

            # Insert into MongoDB
            collection.insert_one(emotion_data)

            return jsonify(full_emotions)
        else:
            return jsonify({"error": "No face detected"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

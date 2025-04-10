from flask import Flask, render_template, request, jsonify
import base64
from pymongo import MongoClient
from datetime import datetime, timezone

app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["emotion_db"]
img_collection = db["images"]
result_collection = db["results"]

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    try:
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"error": "Invalid image data"}), 400

        image_field = data["image"]
        if "," not in image_field:
            return jsonify({"error": "Invalid image format"}), 400

        image_data = image_field.split(",", 1)[1]
        img_doc = {
            "image": image_data,
            "timestamp": datetime.now(timezone.utc),
            "analyzed": False
        }
        result = img_collection.insert_one(img_doc)
        return jsonify({
            "status": "Image uploaded successfully!",
            "timestamp": img_doc["timestamp"].isoformat(),
            "id": str(result.inserted_id)
        })
    except Exception as e:
        import traceback
        print("Error in /upload:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/result")
def get_result():
    pass

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3001)

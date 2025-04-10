from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timezone
from emoji import get_emojis_from_faces  # Assuming you want to process with emojis

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")  # Connect to MongoDB using the service name 'mongodb'
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
            "analyzed": False,
        }
        result = img_collection.insert_one(img_doc)
        return jsonify(
            {
                "status": "Image uploaded successfully!",
                "timestamp": img_doc["timestamp"].isoformat(),
                "id": str(result.inserted_id),
            }
        )
    except Exception as e:
        import traceback
        print("Error in /upload:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route("/get_emoji", methods=["POST"])
def get_emoji():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing emotion data"}), 400

        result = get_emojis_from_faces(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
'''
@app.route("/result", methods=["GET"])
def get_result():
    try:
        # Retrieve the latest result from MongoDB
        latest_result = result_collection.find_one(sort=[("timestamp", -1)])  # Sorting by timestamp to get the latest result
        if latest_result:
            # Return the result, including emotions and timestamp
            return jsonify({
                "emotions": latest_result.get("emotions", {}),
                "timestamp": latest_result.get("timestamp"),
            })
        else:
            return jsonify({"error": "No results found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
'''
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3001)

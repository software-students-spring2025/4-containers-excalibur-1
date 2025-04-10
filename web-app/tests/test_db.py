import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
client = MongoClient(MONGO_URI)


def test_mongodb_connection_write_and_cleanup():
    db = client["facemoji"]
    collection = db["image_data"]

    doc = {"_id": "test-entry", "emotion": "happy"}
    collection.insert_one(doc)

    found = collection.find_one({"_id": "test-entry"})
    assert found is not None
    assert found["emotion"] == "happy"

    collection.delete_one({"_id": "test-entry"})
    assert collection.find_one({"_id": "test-entry"}) is None

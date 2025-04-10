from pymongo import MongoClient

def test_mongodb_connection_write_and_cleanup():
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["facemoji"]
    collection = db["image_data"]

    doc = {"_id": "test-entry", "emotion": "happy"}
    collection.insert_one(doc)

    found = collection.find_one({"_id": "test-entry"})
    assert found is not None
    assert found["emotion"] == "happy"

    collection.delete_one({"_id": "test-entry"})
    assert collection.find_one({"_id": "test-entry"}) is None

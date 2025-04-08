from flask import Flask, render_template
import pymongo
import os

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = pymongo.MongoClient(mongo_uri)
db = client["face_db"]

@app.route("/")
def home():
    return render_template("base.html")
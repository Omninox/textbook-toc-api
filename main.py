from pymongo import MongoClient
from flask import Flask, jsonify
import settings

client = MongoClient(settings.MONGO_URI)

db = client['textbookTOCs']
collection = db.textbooks

app = Flask(__name__)

@app.route("/")
def hello():
    textbooks = []
    for textbook in collection.find():
        print(textbook)
        textbooks.append(textbook)
    return jsonify(len(textbooks))

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
    
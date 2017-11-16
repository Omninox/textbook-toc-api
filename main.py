from pymongo import MongoClient
from flask import Flask, jsonify, render_template, request, redirect
import settings
# import io
import csv
import scripts

client = MongoClient(settings.MONGO_URI)

db = client['textbookTOCs']
collection = db.textbooks

app = Flask(__name__)

DEFAULTS = {
    'data': 'hello world'
}

@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template("upload.html")

@app.route("/textbooknew", methods=['POST'])
def handle_csv():
    text = request.form['isbn']
    toc_data = request.files['toc_file']
    Contents = scripts.TOC(toc_data)
    Contents.populate()
    print(Contents.chapters)
    # print(toc_data)
    # toc_stream = io.StringIO(toc_data.stream.read().decode('Unicode'), newline=None)
    # csv_input = csv.reader(toc_data)
    # for row in csv_input:
    #     print(row)
    # print('Some text was returned: ' + text)
    # print(csv_input)
    return redirect("/")

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
    
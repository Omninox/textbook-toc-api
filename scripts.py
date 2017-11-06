# upload textbook to DB
from pymongo import MongoClient
import settings
import csv

client = MongoClient(settings.MONGO_URI)

db = client['textbookTOCs']
collection = db.textbooks

class TOC:
    def __init__(self, file_name):
        with open('./assets/' + file_name, 'rU') as csvfile:
            # toc_reader=csvfile.read()
            toc_reader = csv.reader(csvfile, delimiter=",")
            for row in toc_reader:
                print(row)

zumdahl = TOC('stats.csv')
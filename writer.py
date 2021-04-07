import os
import csv
import pandas
from openpyxl.workbook import Workbook
from pymongo import MongoClient

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ATLAS_URI = os.environ.get("ATLAS_URI")

connection = MongoClient(ATLAS_URI)
db = connection["test"]

cursor = db.data.find()
mongo_docs = list(cursor)

docs = pandas.DataFrame(columns=[])
for num, doc in enumerate( mongo_docs ):
    doc["_id"] = str(doc["_id"])
    doc_id = doc["_id"]
    series_obj = pandas.Series( doc, name=doc_id )
    docs = docs.append( series_obj )

docs.to_csv("./data/input.csv", ",")
docs.to_excel("./data/output.xlsx")
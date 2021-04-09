import os
import dns
from pymongo import MongoClient

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ATLAS_URI = os.environ.get("ATLAS_URI")

connection = MongoClient(ATLAS_URI)
myDb1 = connection["test"]
myDb2 = connection["test2"]

for item in myDb2.professionals.find({},{"Estabelecimento":1}):
    estabelecimento = item["Estabelecimento"]
    if myDb1.data.find_one({"Nome":estabelecimento}) or myDb1.data.find_one({"Nome Empresarial":estabelecimento}):
        print(estabelecimento)
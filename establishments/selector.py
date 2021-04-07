import os
import dns
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ATLAS_URI = os.environ.get("ATLAS_URI")

connection = MongoClient(ATLAS_URI)
myDb = connection["test"]

page = requests.get("http://cnes2.datasus.gov.br/Lista_Es_Municipio.asp?VEstado=35&VCodMunicipio=352900&NomeEstado=SAO%20PAULO")
contents = page.content

soup = BeautifulSoup(contents, "html.parser")
table = soup.find("table", attrs={"align": "cener", "width":"100%", "border":"0", "cellpadding":"1", "cellspacing":"0"})

for row in table.find_all("tr"):  

    name = row.find("a").contents[0]
    link = row.find("a")["href"]
    link = "http://cnes2.datasus.gov.br/"+link

    if myDb.establishments.find_one({"link": str(link)}):
        print("já registrado")
    else:
        myDb.establishments.insert_one({
            "name" : str(name),
            "link" : str(link),
            "collected" : False
        })
        print(name)
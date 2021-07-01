import os
import dns
import lxml
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from pymongo import MongoClient
from bs4 import BeautifulSoup

options = Options()
binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options.set_preference("browser.download.folderList",2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir","/Data")
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel")
options.binary = binary
firefox = webdriver.Firefox(executable_path=r'C:\Users\Andrew Fernandes\AppData\Local\Programs\Python\Python39\geckodriver.exe',options=options)

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ATLAS_URI = os.environ.get("ATLAS_URI")

connection = MongoClient(ATLAS_URI)
myDb = connection["test2"]

page = requests.get("http://cnes2.datasus.gov.br/Mod_Ind_Profissional_com_CBO.asp")
contents = page.content

soup = BeautifulSoup(contents, "lxml")
select = soup.select("select[id=cboOcupacao] > option")

for option in select:
    text = option.text
    value = option["value"]

    if text.startswith("MEDICO"):
        print(text)
        firefox.get("http://cnes2.datasus.gov.br/Mod_Ind_Profissional_Listar.asp?Vcbo="+value+"&VListar=1&VEstado=35&VMun=352900")
        contents = firefox.page_source
        
        soup = BeautifulSoup(contents, "lxml")
        table = soup.find("table", attrs={"border":"1", "width":"620", "align": "center", "cellpadding":"1", "cellspacing":"0"})

        for row in table.find_all("tr"):
            name = row.find("a")

            if name is not None:
                name = row.find("a").contents[0]
                if myDb.professionals.find_one({"professional": str(name)}):
                    continue
                else:
                    link = firefox.find_element_by_link_text(str(name))
                    link.click()
                    
                    profile_page = firefox.page_source
                    soup = BeautifulSoup(profile_page, "lxml")
                    div = soup.find("div", attrs={"id": "conteudo", "class": "janela_popup"})
                    table = div.find("table", attrs={"id": "example", "class": "display dataTable"})
                    fields = []

                    for row in table.find_all("tr"):
                        for item in row.find_all("td"):
                            fields.append(item.text)
                            if len(fields) > 10:
                                speciality = fields[2]
                                establishment = fields[5]
                                sus = fields[10]
                                if myDb.professionals.find_one({"establishment": str(establishment)}):
                                    continue
                                else:
                                    myDb.professionals.insert_one({
                                        "professional" : str(name),
                                        "establishment" : str(establishment),
                                        "speciality" : str(speciality),
                                        "sus" : str(sus),
                                    })
                                    print(establishment)
                        #print(fields)
                        fields.clear()
                        
                    firefox.back()
            else:
                continue
import os
import dns
import lxml
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ATLAS_URI = os.environ.get("ATLAS_URI")

connection = MongoClient(ATLAS_URI)
myDb = connection["test"]

for data in myDb.establishments.find({'collected': False}):

    page = requests.get(str(data['link']))
    contents = page.content
    soup = BeautifulSoup(contents, "lxml")
    table = soup.find("table", attrs={"bgcolor": "white", "border":"0", "align": "center", "cellpadding": "1", "cellspacing": "0", "width": "760"})

    nome = table.select("tr:nth-of-type(2) > td:nth-of-type(1) > font")[0].text
    cnes = table.select("tr:nth-of-type(2) > td:nth-of-type(2) > font")[0].text
    #cnpj
    cnpj = table.select("tr:nth-of-type(2) > td:nth-of-type(3) > font")[0].text
    if cnpj == " ":
        cnpj = "--"

    nomeEmpresarial = table.select("tr:nth-of-type(4) > td:nth-of-type(1) > font")[0].text
    cpf = table.select("tr:nth-of-type(4) > td:nth-of-type(2) > font")[0].text
    personalidade = table.select("tr:nth-of-type(4) > td:nth-of-type(3) > font")[0].text

    logradouro = table.select("tr:nth-of-type(6) > td:nth-of-type(1) > font")[0].text
    numero = table.select("tr:nth-of-type(6) > td:nth-of-type(2) > font")[0].text
    #telefone
    telefone = table.select("tr:nth-of-type(6) > td:nth-of-type(3) > font")[0]
    if telefone is not None and len(telefone) > 0:
        telefone = table.select("tr:nth-of-type(6) > td:nth-of-type(3) > font")[0].text
    else:
        telefone = "--"

    #complemento
    complemento = table.select("tr:nth-of-type(8) > td:nth-of-type(1) > font")[0]
    if complemento is not None and len(complemento) > 0:
        complemento = table.select("tr:nth-of-type(8) > td:nth-of-type(1) > font")[0].text
    else:
        complemento = "--"
    
    bairro = table.select("tr:nth-of-type(8) > td:nth-of-type(2) > font")[0].text
    cep = table.select("tr:nth-of-type(8) > td:nth-of-type(3) > font")[0].text
    municipio = table.select("tr:nth-of-type(8) > td:nth-of-type(4) > a > font")[0].text
    uf = table.select("tr:nth-of-type(8) > td:nth-of-type(5) > font")[0].text

    tipoEstabelecimento = table.select("tr:nth-of-type(10) > td:nth-of-type(1) > font")[0].text
    #sub tipo estabelecimento
    subTipoEstabelecimento = table.select("tr:nth-of-type(10) > td:nth-of-type(2) > font")[0]
    if subTipoEstabelecimento is not None and len(subTipoEstabelecimento) > 0:
        subTipoEstabelecimento = table.select("tr:nth-of-type(10) > td:nth-of-type(2) > font")[0].text
    else:
        subTipoEstabelecimento = "--"
    
    gestao = table.select("tr:nth-of-type(10) > td:nth-of-type(3) > font")[0].text
    dependencia = table.select("tr:nth-of-type(10) > td:nth-of-type(4) > font")[0].text

    #numero alvara
    numeroAlvara = table.select("tr:nth-of-type(12) > td:nth-of-type(1) > font")[0]
    if numeroAlvara is not None and len(numeroAlvara) > 0:
        numeroAlvara = table.select("tr:nth-of-type(12) > td:nth-of-type(1) > font")[0].text
    else:
        numeroAlvara = "--"
    #orgao expedidor
    orgaoExpedidor = table.select("tr:nth-of-type(12) > td:nth-of-type(2) > font")[0]
    if orgaoExpedidor is not None and len(orgaoExpedidor) > 0:
        orgaoExpedidor = table.select("tr:nth-of-type(12) > td:nth-of-type(2) > font")[0].text
    else:
        orgaoExpedidor = "--"
    #data expedicao
    dataExpedicao = table.select("tr:nth-of-type(12) > td:nth-of-type(3) > font")[0]
    if dataExpedicao is not None and len(dataExpedicao) > 0:
        dataExpedicao = table.select("tr:nth-of-type(12) > td:nth-of-type(3) > font")[0].text
    else:
        dataExpedicao = "--"

    if myDb.data.find_one({"Nome": nome}):
        print("já registrado")
    else:
        myDb.data.insert_one({
            "Nome" : nome,
            "CNES" : cnes,
            "CNPJ" : cnpj,
            "Nome Empresarial" : nomeEmpresarial,
            "CPF" : cpf,
            "Personalidade" : personalidade,
            "Logradouro" : logradouro,
            "Número" : numero,
            "Telefone" : telefone,
            "Complemento": complemento,
            "Bairro": bairro,
            "CEP": cep,
            "Município": municipio,
            "UF": uf,
            "Tipo Estabelecimento": tipoEstabelecimento,
            "Sub Tipo Estabelecimento": subTipoEstabelecimento,
            "Gestão": gestao,
            "Dependência": dependencia,
            "Número Alvará": numeroAlvara,
            "Orgão Expedidor": orgaoExpedidor,
            "Data Expedição": dataExpedicao,
        })
        myDb.establishments.update_one({'link': str(data['link'])},{'$set':{'collected':True}})
        print(nome)
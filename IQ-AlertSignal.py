# Imports
from operator import truediv
from iqoptionapi.stable_api import IQ_Option
import json
from datetime import datetime
import socket
import threading
import time
import sys
import requests


def IQ_Conectar():
    
    global API
    conta_email = "gamesteryet@hotmail.com"
    conta_senha = "Aa457711@"
    balanco = "REAL"

    API = IQ_Option(conta_email, conta_senha)

    print("")
    print("> Conectando-se a IQ Option..")

    check, reason = API.connect()

    if check == False:
        print("- Falha ao conectar-se, razao: " + reason)
        return False

    print("Conectado com sucesso!")

    API.change_balance(balanco)  # REAL #TOURNAMENT #PRACTICE

    return True

if IQ_Conectar() == False:
    sys.exit()


def Assets_Refresh_Openeds():
    global assets_opened
    assets_opened=API.get_all_open_time()

def Assets_Care_CheckAsset(asset_name):
    for i in range(0, len(assets_care)):
        if assets_care[i]["name"] == asset_name:
            return True
    
    return False


def Assets_Care_Update():

    url = "https://www.smart2trader.com/api/tiago_iq_asset_alert/GetAssets.php"

    r = requests.get(url)

    if r.status_code != 200:
        return False

    json = r.json()

    if json["status"] != "success":
        return False

    for i in range(0, len(json["msg"])):
        asset_name = json["msg"][i]["name"]
        asset_class = json["msg"][i]["class"]
        if Assets_Care_CheckAsset(asset_name) == False:
            assets_len = len(assets_care)
            assets_care.append(assets_len)
            assets_care[0]["name"] = asset_name
            assets_care[0]["class"] = asset_class
            assets_care[0]["on"] = False

    print("> Assets_Care_Update")
    print(assets_care)
        

assets_care = []

while True:
    
    Assets_Refresh_Openeds()
    Assets_Care_Update()

    for i in range(0, len(assets_care)):
        print("Verificando ativo | "+assets_care[i]["name"]+" / " + assets_care[i]["class"])
        print(assets_opened[assets_care[i]["class"]][assets_care[i]["name"]]["open"])
        time.sleep(10)
        pass

    #time.sleep(60*15) # 15 minutos
    
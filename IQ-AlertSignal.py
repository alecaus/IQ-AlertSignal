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
    conta_email = "alexandrecaus@hotmail.com"
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


def Assets_Refresh_Openeds():
    global assets_opened
    if API.check_connect() == False:
        print("Não está conectado")
        if IQ_Conectar() == False:
             print("Falha em realizar nova conexão..")
        else:
            print("Reconectado com sucesso!")
            #elegram_Alertar("Reconectado com sucesso!")
    else:
        print("Está conectado")

    assets_opened=API.get_all_open_time()
    #print(assets_opened)

def AssetsCare_CheckAsset(asset_name, asset_class):
    for i in range(0, len(assets_care)):
        if assets_care[i]["name"] == asset_name and assets_care[i]["class"] == asset_class:
            return True
    
    return False


def AssetsCare_Update():

    url = "https://www.smart2trader.com/api/tiago_iq_asset_alert/GetAssets.php"

    r = requests.get(url)

    if r.status_code != 200:
        return False

    json = r.json()

    print("> Dados obtidos: ")
    print(json)

    if json["status"] != "success":
        return False

    try:
        len(json["msg"])
    except:
        print("> Não existem ativos para acompanhar..")
        return False

    for i in range(0, len(json["msg"])):
        asset_name = json["msg"][i]["name"]
        asset_class = json["msg"][i]["class"]

        if AssetsCare_CheckAsset(asset_name, asset_class) == False:
            assets_len = len(assets_care)
            assets_care.append(assets_len)
            assets_care[assets_len] = {}
            assets_care[assets_len]["name"] = asset_name
            assets_care[assets_len]["class"] = asset_class
            assets_care[assets_len]["on"] = False

    for i in range(0, len(assets_care)):

        if i > len(assets_care)-1: 
            continue

        asset_class = assets_care[i]["class"]
        asset_name = assets_care[i]["name"]

        found = False

        for i2 in range(0, len(json["msg"])):
            if assets_care[i]["name"] == json["msg"][i2]["name"] and assets_care[i]["class"] == json["msg"][i2]["class"]:
                found = True 
    
        if found == False:
            print("Deixou de existir ativo: ", asset_name)
            assets_care.pop(i)


def Telegram_Alertar(mensagem):
    token = "5143782959:AAFnoNU58LuHvpNMOKtFlf4V2QXxxi75SfU"
    url = f"https://api.telegram.org/bot{token}"
    params = {"chat_id": "-1001661767638", "text": mensagem}
    r = requests.get(url + "/sendMessage", params=params)
    print("> Notificação Telegram Enviada")
    print("- " + mensagem)


if IQ_Conectar() == False:
    sys.exit()


def ObterPayout(par, tipo, timeframe = 1):
	if tipo == 'turbo':
		a = API.get_all_profit()
        
		return int(100 * a[par]['turbo'])
		
	elif tipo == 'digital':
	
		API.subscribe_strike_list(par, timeframe)
		while True:
			d = API.get_digital_current_profit(par, timeframe)
			if d != False:
				d = int(d)
				break
			time.sleep(1)
		API.unsubscribe_strike_list(par, timeframe)
		return d

assets_care = []

meus_ativos = {}
meus_ativos["digital"] = {}
meus_ativos["turbo"] = {}

while True:

    #time.sleep(5)
    
    Assets_Refresh_Openeds()

    if AssetsCare_Update() == False:
        time.sleep(60*2) # 2 minutos
        continue

    for key in assets_opened["digital"]:
         #print(assets_opened["turbo"][i])
          if assets_opened["digital"][key]["open"] == False:
               continue
        

          payout = ObterPayout(key,"digital")
          
          if payout <= 90:
            continue
          
          if key in meus_ativos["digital"]:
               if payout <= meus_ativos["digital"][key]:
                    meus_ativos["digital"][key] = payout
                    continue
               
               meus_ativos["digital"][key] = payout
               
               Telegram_Alertar(key + "/" + "Digital | Payout de " + str(payout) + "%")
          else:
               meus_ativos["digital"][key] = payout
               Telegram_Alertar(key + "/" + "Digital | Payout de " + str(payout) + "%")

# 

    for key in assets_opened["turbo"]:
         #print(assets_opened["turbo"][i])
          if assets_opened["turbo"][key]["open"] == False:
               continue
        

          payout = ObterPayout(key,"turbo")
          
          if payout <= 90:
            continue
          
          if key in meus_ativos["turbo"]:
               if payout <= meus_ativos["turbo"][key]:
                    meus_ativos["turbo"][key] = payout
                    continue
               
               meus_ativos["turbo"][key] = payout
               
               Telegram_Alertar(key + "/" + "Turbo | Payout de " + str(payout) + "%")
          else:
               meus_ativos["turbo"][key] = payout
               Telegram_Alertar(key + "/" + "Turbo | Payout de " + str(payout) + "%")
               
# 


            #Telegram_Alertar(key + " / " + "Digital | Payout de " + str(payout))


    for i in range(0, len(assets_care)):
        status = assets_opened[assets_care[i]["class"]][assets_care[i]["name"]]["open"]
        #print("> Verificando ativo | "+assets_care[i]["name"]+" / " + assets_care[i]["class"])
        #print("> Status: ", status)
       # print(payout(str(assets_care[i]["name"]),str(assets_care[i]["class"])))

        if assets_care[i]["on"] == False and status == True:
            # Envia notificação
            print("> Enviando notificação..")
            Telegram_Alertar(assets_care[i]["name"]+"-"+assets_care[i]["class"]+" | Disponível!")
            payouts = payout(assets_care[i]["name"],assets_care[i]["class"])

         #   if payouts >= 92:
         #        Telegram_Alertar(assets_care[i]["name"]+"-"+assets_care[i]["class"]+" | Payout de " + str(payouts))

            assets_care[i]["on"] = True    


        if status != True:
            assets_care[i]["on"] = False

    time.sleep(60*2) # 2 minutos

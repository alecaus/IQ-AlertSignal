# Imports
from iqoptionapi.stable_api import IQ_Option
import json
from datetime import datetime
import socket
import threading
import time
import sys


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

while True:
    time.sleep(5)
    print("..")
# Imports
from iqoptionapi.stable_api import IQ_Option
import json
from datetime import datetime
import socket
import threading
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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
        messagebox.showerror(title="Falha ao fazer Login", message=reason)
        return False

    print("Conectado com sucesso!")

    API.change_balance(balanco)  # REAL #TOURNAMENT #PRACTICE

    return True

if IQ_Conectar() == False:
    sys.exit()
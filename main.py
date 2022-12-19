import os
import datetime
import pandas as pd
from email.message import EmailMessage
import smtplib
import PySimpleGUI as sg
import json


def firstData():
    #Create a directory 
    os.chdir(r'C:')
    if os.path.isdir("payBills"):
        if os.path.isdir("payBills\allDataBills.json"):
            return False
        return os.path.abspath('\.')
    else:
        return True
        os.mkdir("payBills")

    #Make a Json archive with the colunms and where all the data is saved
    with open('allDataBills.json','w') as archive:
        dataBills = [{
        "item":"",
        "valor":"",
        "cartao":"",
        "dia":"",
        "parcelas":"",
        "snapshot":""
    }]
        archive.write(json.dumps(dataBills))

print(firstData())
    
    
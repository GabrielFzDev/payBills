import os
import datetime
import pandas as pd
import json
import matplotlib.pyplot as plt

#If is you a first time in the system
def firstData() -> str:
    #Create a directory 
    os.chdir(r'C:\\')
    if os.path.isdir("payBills"):
        os.chdir(r'C:\\payBills')
        for archives in os.listdir():
            if archives == 'allDataBills.json':
                return 'Already exist'
    else:
        print('Creating Diretory')
        os.mkdir("payBills")
    #Make a Json archive with the colunms and where all the data is saved
    print('Creating json data')
    with open('allDataBills.json','a+') as archive:
        dataBills = [{
        "item":"",
        "valor":"",
        "cartao":"",
        "dia":"",
        "parcelas":"",
        "snapshot":""
        }]
        archive.write(json.dumps(dataBills))
    return 'Database Created'

#Read all the data, if you dont have, creaating is automatic
def readData():
    # dataBase = pd.DataFrame
    #Try Except for prevent the error of dont existing archive data
    try:
        os.chdir(r'C:\\payBills')
        dataBase = pd.read_json('allDataBills.json')

    except (FileNotFoundError,ValueError) as err:
        print(err)
        print('You dont have the archive. Creating...')
        print(firstData())
    
    return dataBase

#Para dar append tem q ser um dataframe
def appendData(data):
    os.chdir(r'C:\\payBills')
    try:
        database = readData()
        data = pd.concat([database,data],ignore_index=True)
        data = data.to_json('allDataBills.json')
    except Exception as err:
        print(err)
    print('Data Inserted')
    
def deleteData(line):
    os.chdir(r'C:\\payBills')
    database = readData()
    database = database.drop(line)
    database.to_json('allDataBills.json')
    print('Data deleted')

def modifyngData(data):
    os.chdir(r'C:\\payBills')
    database = readData()
    database.update(data)
    data = data.to_json('allDataBills.json')
    print('Data Modified')

def getImageGraph():
    df = readData()
    df = df[['valor','dia']].groupby('dia',as_index=False).sum()
    figure = plt.figure(facecolor='#1c1e23')
    figure.set_facecolor('#1c1e23')

    plt.figure(0,facecolor="#1c1e23")
    plt.yticks(color='#ffff')
    plt.xticks(color='#ffff')
    ax = plt.gca()
    df.plot(kind='line', x='dia', y='valor', color='#ffff', ax=ax, figsize=(5.5,3))
    axies = plt.axes(ax)
    axies.set_facecolor("#1c1e23")
    plt.savefig('grafico.png')
    return r'C:\\payBills\grafico.png'

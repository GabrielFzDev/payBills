import PySimpleGUI as sg
import datetime
import os
import bdJson as bd
import pandas as pd

def timeNow():
    return datetime.datetime.strftime(datetime.datetime.now(),'%d/%m/%y')

def tableFormat():
    allData = bd.readData()
    allData = allData.to_dict(orient='split')

    return allData

#Variaveis usadas
allData = tableFormat()
#Tema da Janela
sg.theme('DarkGrey13')

#Layout de Entrada
newValues = [
    [sg.Text(timeNow(),key='LabelDatetime')],
    
    [sg.Text('Item',key='LabelItem',font='Arial')],
    [sg.Input('',(30,50),key='inputItem')],

    [sg.Text('Valor do Item',key='LabelValor',font='Arial')],
    [sg.Input('',(30,50),key='inputValor',)],

    [sg.Text('Dia da Compra',key='LabelDia',font='Arial')],
    [sg.Input('',(30,50),key='inputDia')],
]

tableValues = [
    [sg.Table(allData['data'],headings=allData['columns'],key='table')]
]

layout = [
    [sg.Column(newValues),sg.VSeparator(),sg.Column(tableValues)]
]
window = sg.Window("",layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    print(event,values)
window.close()
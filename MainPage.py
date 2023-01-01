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

def popupParcelas():

    col_layout = [[sg.Button('OK',enable_events=True)]]
    layout = [
        [sg.Text("Coloque o numero de Parcelas:\nSomente numeros plis")],
        [sg.Input("",key='InputParcelas',size=(20,1))],
        [sg.Column(col_layout, expand_x=True, element_justification='right')],
    ]
    window = sg.Window("Prediction", layout, use_default_focus=False, finalize=True, modal=True)
    event, values = window.read()
    window.close()
    return values

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
    [sg.Spin([i for i in range(1,3000)], size=(10,50),initial_value=10.90, k='SpinNumberValue')],

    [sg.Text('Cartao Utlizado',font='Arial')],
    [sg.Combo(values=('Cartao XP','Cartao VA','Cartao VR','Nubank Farias','Nubank Carol','Safra'),key='Cards', size=(30,1))],

    [sg.Text('Dia da Compra',font='Arial')],
    [sg.Input(key='-IN2-', size=(19,1)), sg.CalendarButton('Calendario',  target='-IN2-', locale='de_br', begin_at_sunday_plus=1,format=('%d/%m/%Y') )],

    [sg.Text('Parcelas',font='Arial')],
    [sg.Radio('Sim',key='PopUpParcelas',group_id='RadioParcelas',enable_events=True),sg.Radio('Nao',key='ParcelasNao',group_id='RadioParcelas',enable_events=True)],

]

tableValues = [
    [sg.Table(allData['data'],headings=allData['columns'],key='table',size=(120,20),enable_click_events=True)]
]

layout = [
    [sg.Column(newValues),sg.VSeparator(),sg.Column(tableValues)]
]
window = sg.Window("",layout)

while True:
    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == 'PopUpParcelas':
        popup_prediction('industry', 'observation')
    if event == 'parcelasNao':
        parcela = 1
    print(event,values)
window.close()
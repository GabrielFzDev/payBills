import PySimpleGUI as sg
import datetime
import os
import bdJson as bd
import pandas as pd

def timeNow():
    return datetime.datetime.strftime(datetime.datetime.now(),'%d/%m/%y')

def tableFormat():
    allData = bd.readData()
    allData['snapshot'] = pd.to_datetime(allData['snapshot'],unit='ms')
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

#Layout de Entrada de Dados
newValues = [
    #Horario
    [sg.Text(timeNow(),key='LabelDatetime')],
    
    #item, Compra
    [sg.Text('Compra',key='LabelItem',font='Arial')],
    [sg.Input('',(30,50),key='inputItem')],

    #Valor da Compra
    [sg.Text('Valor da Compra',key='LabelValor',font='Arial')],
    [sg.Spin([i for i in range(1,3000)], size=(10,50),initial_value=10.90, k='SpinNumberValue')],

    #Qual cartao foi utilizado
    [sg.Text('Cartao Utlizado',font='Arial')],
    [sg.Combo(values=('Cartao XP','Cartao VA','Cartao VR','Nubank Farias','Nubank Carol','Safra'),key='Cards', size=(30,1))],

    #Dia da Compra
    [sg.Text('Dia da Compra',font='Arial')],
    [sg.Input(key='-IN2-', size=(19,1)), sg.CalendarButton('Calendario',  target='-IN2-', locale='de_br', begin_at_sunday_plus=1,format=('%d/%m/%Y') )],

    #Em quantas parcelas foi feito
    [sg.Text('Parcelas',font='Arial')],
    [sg.Radio('Sim',key='PopUpParcelas',group_id='RadioParcelas',enable_events=True),sg.Radio('Nao',key='ParcelasNao',group_id='RadioParcelas',enable_events=True)],

    #Botao de inserir no banco
    [sg.Button('Inserir',key='Submit',enable_events=True,button_color='#1c231d')]
]

#Tabela que mostra o q esta no banco + botao de delete e modificar
tableValues = [
    [sg.Table(allData['data'],headings=allData['columns'],key='table',size=(170,18),enable_click_events=True)],
    [sg.Button('Modify',size=(20,1),button_color='#23211c'),sg.Button('Delete',key='deleteLine',enable_events=True,size=(20,1),button_color='#231c21')]
]

#Layout final com um separador
layout = [
    [sg.Column(newValues),sg.VSeparator(),sg.Column(tableValues)],
]

window = sg.Window("",layout)

while True:
    #Aqui cai os eventos e os inputs
    event, values = window.read()

    #Se o evento for sair, para a execucao
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    #Se a pessoa colocar tem parcelas entao abre um popup para colocar o numero de parcelas
    if event == 'PopUpParcelas':
        parcelas = popupParcelas()
        parcelas = parcelas['InputParcelas']
    #Se nao tiver parcelas entao a parcela eh só 1
    if event == 'ParcelasNao':
        parcelas = 1
    #Botao de submit para poder inserir os dados, para inserir tem q passar como Dataframe
    if event == 'Submit':
        df = [{
        'item':values['inputItem'],
        'valor':values['SpinNumberValue'],
        'cartao':values['Cards'],
        'dia':values['-IN2-'],
        'parcelas':parcelas,
        'snapshot':datetime.datetime.now()
        }]
        bd.appendData(pd.DataFrame(df))
        #Atualizando a tabela
        allData = tableFormat()
        window['table'].update(allData['data'])
    if type(event) == tuple:
        clickedIndex = event[2][0]
    if event == 'deleteLine':
        bd.deleteData(clickedIndex)
        allData = tableFormat()
        window['table'].update(allData['data'])
    print(event,values)
    
window.close()
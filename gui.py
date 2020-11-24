import PySimpleGUI as sg
import os.path

sg.theme('DarkTeal4') 

def read_logfile():
    path = "logs/log.txt"
    if os.path.isfile(path):
        file = open(path, "r").read()
        msg = file
        return msg
    else:
        return "Log file not generated"

def update_file():
    path = "logs/status.txt"
    if os.path.isfile(path):
        file = open(path, "r").read().split("\n")[:-1]
        msg = ""
        for server in file:
            status = server.split(" ")
            msg += 'Host: ' + status[0] + '\nServer: ' + status[1] + '\nActive: ' + status[2] + '\nOpen Connections: ' + status[3] + "\n\n"
        return msg
    else:
        return "Wating for status response..."

tab1_layout = [[sg.Multiline('Fetching data...', key='-TAB1 TEXT-', size=(100, 42), font=('Helvetica 14'), pad=(2,2))]]
tab2_layout = [[sg.Multiline('Fetching log file...', key='-TAB2 TEXT-', size=(100, 42), font=('Helvetica 14'), pad=(2,2))], [sg.Button('Generate logs', key='READ', font = ('Helvetica 14'))]]

layout = [  [ sg.Text('Load Balancer Console', font = ('Helvetica 20 bold'), justification='center', key = '-TITLE-') ],
            [ sg.TabGroup([ [sg.Tab('Sever Status', tab1_layout)], [sg.Tab('Logs', tab2_layout)] ]) ],
            [ sg.Button('Exit', size = (4,1), font=('Helvetica 14')) ]]

window = sg.Window('LoadBalancer', layout, finalize=True, resizable=True)

window['-TITLE-'].expand(True, True, True)

while True:
    event, values = window.read(timeout = 30)
    msg = update_file()
    window['-TAB1 TEXT-'].update(msg)

    if event == 'READ':
        log = read_logfile()
        window['-TAB2 TEXT-'].update(log)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

#!/usr/bin/env python3
from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, Markup, Response, g
from flask_socketio import SocketIO, emit
from multiprocessing import Process
import satyrn.core.run as Run
import satyrn.core.html as Html
import satyrn.core.ledger as Ledger
import time, os, sys, webbrowser, argparse, logging, sqlite3
import logging

DATABASE = 'database.db'
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
parser = argparse.ArgumentParser(description='Display python information live in browser.')
parser.add_argument('file', metavar='F',
                            help='python file to run')
args = parser.parse_args()

url = 'localhost:5000'

app = Flask(__name__)
log = logging.getLogger('werkzeug')


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'secret!'
socketio= SocketIO(app)

executionCounter=0
myFile=args.file
fileLocation=myFile
globalScope={}
localScope={}
allCellsList={}
ledger=[]
myDir=os.path.dirname(os.path.abspath(__file__))
@app.route('/')
def home():
    css=HtmlFormatter().get_style_defs('.highlight')
    response=Response(render_template('main.html', css=css))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies
    return response
@socketio.on('connect')
def connect():
    print('Connected to client')
    socketio.emit('showAll', {})
#    display()
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
@socketio.on('checkOnUpdate') 
def checkOnUpdate():
    '''
    lastModified=os.path.getmtime(fileLocation)
    timeSinceModified=int(time.time()-lastModified)
    if timeSinceModified<=1:
        time.sleep(1)
        update()
        time.sleep(1)
        emit('check complete')
    else:
        time.sleep(1)
        emit('check complete')
        '''
def main():
    ledger=[]
    def checkChanged():
        GlobalScope={}
        LocalScope={}
        while True:
            lastModified=os.path.getmtime(fileLocation)
            timeSinceModified=int(time.time()-lastModified)
            if timeSinceModified<=1 or executionCounter<1:
                time.sleep(1)
                update(GlobalScope, LocalScope)
                time.sleep(1)
            else:
                time.sleep(1)
    def startFlask():
        socketio.run(app, port=5000)#, debug=True)
#        webbrowser.open_new_tab(url)
    try:
        print('Starting flask process...')
        flask=Process(target=startFlask)
        flask.start()
        '''
        print('Starting check process...')
        check=Process(target=checkChanged)
        check.start()
        '''
    except KeyboardInterrupt:
        '''
        print('Terminating check loop.')
        check.terminate()
        check.join()
        print('Terminated check loop.')
        '''
        print("Terminating flask server.")
        flask.terminate()
        flask.join()
        print("Terminated flask server.")
    checkChanged()

def display():
    global allCellsList
    html=Html.convertLedgerToHtml(allCellsList)
    print('\nAll Cells List:\n%s' % html)
    socketio.emit('showAll', html)
def update(GlobalScope, LocalScope):
    global ledger
    global allCellsList
    global executionCounter
    global globalScope
    global localScope
    testContent=''
    with open(fileLocation, 'r') as file_content:
        testContent=file_content.read()
    '''
    Look at the file to see if anything has changed
    with reference to the ledger. 
    If there is a change, update the ledger, and return
    a list of the cells that need to execute.
    '''
    newLedger, allCellsList=Ledger.updateLedgerPop(allCellsList, testContent, ledger, myDir)
    '''
    Take the cells that need to execute, and
    convert their text to html for display.
    '''
    htmlAllCells=Html.convertLedgerToHtml(allCellsList)
    ledger=newLedger
    '''
    Send a list of the cells that will run to the
    client so it can show loading.
    '''
    socketio.emit('showLoading', htmlAllCells)
    '''
    Run the newly changed cells and return their output.
    '''
#    output=Run.runNewCells(allCellsList, ledger, globalScope, localScope, myDir)
    output=Run.runNewCells(allCellsList, ledger, GlobalScope, LocalScope, myDir)
#    output=Run.runNewCells(allCellsList, ledger, myDir)
    output=Html.output(output)
    #print('\nOutput list:\n %s' % output)
    socketio.emit('showOutput', output)
    Ledger.updateChanged(allCellsList)
    executionCounter += 1
    print('The number of code executions is %d' % executionCounter)
    display()

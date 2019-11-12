#!/usr/bin/env python3
from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, Markup, Response, g
import python_live.util
from flask_socketio import SocketIO, emit
from multiprocessing import Process
import time, os, sys, webbrowser, argparse, logging, sqlite3

DATABASE = 'database.db'
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
parser = argparse.ArgumentParser(description='Display python information live in browser.')
parser.add_argument('file', metavar='F',
                            help='python file to run')
args = parser.parse_args()

url = 'localhost:5000'

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

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
    update(first=True)
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
@socketio.on('checkOnUpdate') 
def checkOnUpdate():
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
def main():
    ledger=[]
    def startFlask():
        socketio.run(app, port=5000, debug=True)
        webbrowser.open_new_tab(url)
    try:
        flask=Process(target=startFlask)
        flask.start()
    except KeyboardInterrupt:
        print("Terminating flask server.")
        flask.terminate()
        flask.join()
def update(first=False):
        global ledger
        global allCellsList
        testContent=''
        with open(fileLocation, 'r') as file_content:
            testContent=file_content.read()
        newLedger, allCellsList=python_live.util.updateLedgerPop(allCellsList, testContent, ledger, myDir)
        htmlAllCells=python_live.util.convertLedgerToHtml(allCellsList, myDir)
        ledger=newLedger
        emit('showLoading', htmlAllCells)
        output=python_live.util.runNewCells(allCellsList, ledger, globalScope, localScope, myDir, first)
        emit('showOutput', output)


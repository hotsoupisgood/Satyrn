#!/usr/bin/env python3
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
ledgerScope={}
ledger=[]
myDir=os.path.dirname(os.path.abspath(__file__))
@app.route('/')
def home():
#    jsloc, css, body=python_live.util.update(myFile, ledger, ledgerScope, myDir)
    testContent=''
    with open(watchedFile, 'r') as content_file:
        testContent=content_file.read()
    newCellsToRun, allCellsList=python_live.util.updateLedgerPop(testContent, ledger, myDir)
    response=Response(render_template('main.html', jsloc=jsloc, css=css, body=body))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies
    return response
@socketio.on('connect')
def connect():
    print('Connected to client')
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
@socketio.on('checkOnUpdate') 
def checkOnUpdate():
    lastModified=os.path.getmtime(fileLocation)
    timeSinceModified=int(time.time()-lastModified)
    if timeSinceModified<=1:
        testContent=''
        with open(watchedFile, 'r') as file_content:
            testContent=content_file.read()
            emit('check complete')
            newCellsToRun, allCellsList=updateLedgerPop(file_content, ledger, myDir)
            for cell in newCellsToRun:
                emit('showLoading', cell['hash')
    else:
        time.sleep(1)
        emit('check complete')
def main():
    def startFlask():
        socketio.run(app, port=5000, debug=True)
    try:
        flask=Process(target=startFlask)
        flask.start()
    except KeyboardInterrupt:
        print("Terminating flask server.")
        flask.terminate()
        flask.join()
    webbrowser.open_new_tab(url)

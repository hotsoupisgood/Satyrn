#!/usr/bin/env python3
from flask import Flask, render_template, Markup, Response, g
import sqlite3
import python_live.util
from flask_socketio import SocketIO, emit
from multiprocessing import Process
import time
import os
import sys
import webbrowser
import argparse
import logging

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

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

cur=None
myFile=args.file
fileLocation=myFile
ledgerScope={}
ledger=[]
myDir=os.path.dirname(os.path.abspath(__file__))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
@app.route('/')
def home():
    cur = get_db().cursor()
    jsloc, css, body=python_live.util.update(myFile, ledger, ledgerScope, myDir)
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
        emit('check complete', True)
    else:
        time.sleep(1)
        emit('check complete', False)
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

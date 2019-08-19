#!/usr/bin/env python3
from flask import Flask, render_template, Markup, Response
#from .util import getHtml, duplicate, displayArray
import python_live.util
#from python_live.util.util import getHtml, duplicate, displayArray
from flask_socketio import SocketIO, emit
from multiprocessing import Process
import time
import os
import sys
import webbrowser
import argparse

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

@app.route('/')
def home():
    jsloc, css, body, stdout, stderr = python_live.util.displayArray(myFile)
    response=Response(render_template('main.html', jsloc=jsloc, css=css, body=Markup(body), stderr=Markup(stderr), stdout=Markup(stdout))
)
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
    if timeSinceModified<=2:
        emit('check complete', True)
        print('Send Help')
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

from flask import Flask, render_template, Markup
from util import getHtml, duplicate, displayArray
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
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

myFile=args.file
fileLocation=myFile

@app.route('/')
def home():
    jsloc, css, body, stdout, stderr = displayArray(myFile)
    return render_template('main.html', jsloc=jsloc, css=css, body=Markup(body), stderr=Markup(stderr), stdout=Markup(stdout))
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
    print(timeSinceModified)
    if timeSinceModified<=2:
        emit('reload')
        time.sleep(5)
        print('Send Help')
def main():
#if __name__ == '__main__':
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

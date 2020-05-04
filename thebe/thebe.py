#!/usr/bin/env python3

from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, Response, g
from flask_socketio import SocketIO, emit
from multiprocessing import Process
import thebe.core.update as Update
import thebe.core.args as args
import thebe.core.vim as vim
import thebe.core.data as data
import thebe.core.file as fm
import thebe.core.constants as Constants
import tempfile, time, os, sys, webbrowser, logging, logging.config, json

port = args.getPort()
target_name = args.getFile()

#Initialize flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_handlers = False)

#Configure logging
logging.basicConfig(filename = os.path.dirname(__file__)+'/logs/all.log', level = logging.INFO)
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

#Determine what kind of file working with
target_name, is_ipynb = fm.setup(target_name)

#Initialize some variables
isActive = False
Cells = []#Constants.getIpynb()
LocalScope = {}
GlobalScope = {}

'''
Set some headers and get and send css for all of the HtmlFormatter components.
'''
@app.route('/')
def home():
    css=HtmlFormatter().get_style_defs('.highlight')
    response=Response(render_template('main.html', css=css))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # HTTP 1.1.
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0" # Proxies
    return response

'''
Connect and disconnect events.
'''
@socketio.on('connect')
def connect():
    logging.info('Connected to client')
    #Show
    Update.checkUpdate(socketio, target_name, connected = True, isIpynb = is_ipynb, \
            GlobalScope = GlobalScope, LocalScope = LocalScope, Cells = Cells)
    #Start pinging
    socketio.emit('ping client')

@socketio.on('disconnect')
def disconnect():
    logging.info('Client disconnected')

'''
Ping back and forth from client to server.
Checks whether or not the file has been saved and running it when changed.
'''
@socketio.on('check if saved')
def check():
    ('Check if target updated...')
    Update.checkUpdate(socketio, target_name, isIpynb = is_ipynb, \
            GlobalScope = GlobalScope, LocalScope = LocalScope, Cells = Cells)
    socketio.emit('ping client')

'''
Run flask and socketio.
'''
def main():
    ledger=[]
    def startFlask():
        socketio.run(app, port=port, debug=False)
#        webbrowser.open_new_tab(url)
    try:
        logging.info('Starting flask process...')
        flask = Process(target = startFlask)
        flask.start()
    except KeyboardInterrupt:
        logging.info("Terminating flask server.")
        flask.terminate()
        flask.join()
        logging.info("Terminated flask server.")

#!/usr/bin/env python3

from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, Response, g
from flask_socketio import SocketIO, emit
from multiprocessing import Process
import thebe.core.update as Update
import thebe.core.args as args
import thebe.core.cli as cli
import thebe.core.vim as vim
from thebe.core.output import outputController
import thebe.core.ledger as ledger
from thebe.core.vim import Vim
import tempfile, time, os, sys, webbrowser, logging, json

#outputController.open()
#logging.INFO('testing')
#outputController.open()
#logging.INFO(' more testing')
#s1,e1 = outputController.close()
#s2,e2 = outputController.close()
#logging.INFO('s1:\t%s\te1\t%s\ns2:\t%s\te2\t%s\n'%(s1,e1,s2,e2))
#sys.exit()

port = args.getPort()
target_loc = args.getFile()

#Initialize flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#Configure logging
logging.basicConfig(filename = os.path.dirname(__file__)+'/logs/all.log', level = logging.INFO)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#Determine what kind of file working with
target_ext = cli.test_file(target_loc)
vim = Vim()
if target_ext == 'ipynb':
    ipynb = cli.load_ipynb(target_loc)
    ipynb_loc = target_loc
    temp_loc = vim.write_temp(ledger.toThebe(ipynb), ipynb_loc.split('.')[0])
    target_loc = temp_loc
    vim.open()


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
    logging.INFO('Connected to client')
    #Show
    Update.checkUpdate(socketio, target_loc, connected=True)
    #Start pinging
    socketio.emit('ping client')

@socketio.on('disconnect')
def disconnect():
    logging.INFO('Client disconnected')

'''
Ping back and forth from client to server.
Checks whether or not the file has been saved and running it when changed.
'''
@socketio.on('check if saved')
def check():
    ('Check if target updated...')
    Update.checkUpdate(socketio, target_loc)
    socketio.emit('ping client')

'''
Run flask and socketio.
'''
def main():
    ledger=[]
    def startFlask():
        socketio.run(app, port=port)#, debug=True)
#        webbrowser.open_new_tab(url)
    try:
        logging.INFO('Starting flask process...')
        flask = Process(target = startFlask)
        flask.start()
    except KeyboardInterrupt:
        logging.INFO('Deleting temporary file.')
        vim.removeTemp()
        logging.INFO("Terminating flask server.")
        flask.terminate()
        flask.join()
        logging.INFO("Terminated flask server.")

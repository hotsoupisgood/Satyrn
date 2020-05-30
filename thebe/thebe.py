#!/usr/bin/env python3

from jupyter_client.manager import start_new_kernel
from pygments.formatters import HtmlFormatter
from flask import Flask, render_template, Response, g
from flask_socketio import SocketIO, emit
from multiprocessing import Process
import thebe.core.update as Update
import thebe.core.args as args
import thebe.core.logger as Logger
from thebe.core.jupyter_wrapper import jupyter_client_wrapper
import tempfile, time, os, sys, webbrowser, logging, logging.config, json

port = args.getPort()
input_filename = args.getFile()

#Initialize flask
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_handlers = False)

# Set up the execution engine
jupyter = jupyter_client_wrapper(input_filename)
jupyter.setSocket(socketio)

#Configure logging
logger = Logger.getLogger('sockets.log', __name__)
#logging.basicConfig(filename = os.path.dirname(__file__)+'/logs/all.log', level = logging.DEBUG)
#logging.basicConfig(level = logging.INFO)
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

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
    logger.info('Connected to client')
    #Show
    jupyter.execute(update = 'connected')
#    Update.checkUpdate(socketio, target_name, connected = True, isIpynb = is_ipynb, \
#            GlobalScope = GlobalScope, LocalScope = LocalScope, Cells = Cells, jc=jupyter_client)
    #Start pinging
#    socketio.emit('ping client')

@socketio.on('disconnect')
def disconnect():
    logger.info('Client disconnected')

'''
Ping back and forth from client to server.
Checks whether or not the file has been saved and running it when changed.
'''
@socketio.on('check if saved')
def check():
    logger.info('Check if target updated...')
    Update.checkUpdate(socketio, target_name, isIpynb = is_ipynb, \
            GlobalScope = GlobalScope, LocalScope = LocalScope, Cells = Cells, jc=jupyter_client)
    socketio.emit('ping client')

'''
'''
@socketio.on('run_all')
def run_all():
    '''
    Restart the kernel, and clear saved code.
    '''
    # Restart the kernel after active is set
    kernel_manager.restart_kernel()
    message = jupyter_client.get_iopub_msg(timeout=1)['content']
    message = jupyter_client.get_iopub_msg(timeout=1)['content']
    logger.info('Restarting kernel')
    Update.checkUpdate(socketio, target_name, isIpynb = is_ipynb, \
            GlobalScope = GlobalScope, LocalScope = LocalScope, Cells = Cells, jc=jupyter_client,\
            runAll = True)

'''
Run flask and socketio.
'''
def main():
    ledger=[]
    socketio.run(app, port=port, debug=False)

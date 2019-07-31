from flask import Flask, render_template, Markup
from util import getHtml, duplicate, displayArray
from flask_socketio import SocketIO, emit
from multiprocessing import Process
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def home():
    jsloc, css, body = displayArray()
    return render_template('main.html', jsloc=jsloc, css=css, body=Markup(body))
@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

if __name__ == '__main__':
    def startModifiedCheck():
        MYDIR = os.path.dirname(os.path.abspath(__file__))
        print('Hello world')
        while True:
            if os.path.getmtime(os.path.join(MYDIR, 'test.py'))<=5:
                emit('reload')
                print('Send Help')
    def startFlask():
        socketio.run(app, port=5001, debug=True)
    try:
        flask=Process(target=startFlask)
        flask.start()
        modifiedCheck=Process(target=startModifiedCheck)
        modifiedCheck.start()
    except KeyboardInterrupt:
        print("Terminating flask server.")
        flask.terminate()
        flask.join()
        modifiedCheck.terminate()
        modifiedCheck.join()

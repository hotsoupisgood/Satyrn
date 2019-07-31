from flask import Flask, render_template, Markup
from util import getHtml, duplicate, displayArray
from flask_socketio import SocketIO, emit
from multiprocessing import Process
import time
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def home():
    jsloc, css, body = displayArray()
    return render_template('main.html', jsloc=jsloc, css=css, body=Markup(body))
@socketio.on('connect')
def connect():
    print('We are connected')
    emit('after connect',  {'data':'Lets dance'})

if __name__ == '__main__':
    def startModifiedCheck():
        myDir = os.path.dirname(os.path.abspath(__file__))
        myFile='test.py'
        fileLocation=os.path.join(myDir, myFile)
        while True:
            lastModified=os.path.getmtime(fileLocation)
            timeSinceModified=int(time.time()-lastModified)
            print(timeSinceModified)
            time.sleep(2)
            if timeSinceModified<=5:
                emit('reload')
                print('Send Help')
    def startFlask():
        socketio.run(app, port=5001, debug=True)
    try:
        modifiedCheck=Process(target=startModifiedCheck)
        modifiedCheck.start()
        flask=Process(target=startFlask)
        flask.start()
    except KeyboardInterrupt:
        print("Terminating flask server.")
        flask.terminate()
        flask.join()
        modifiedCheck.terminate()
        modifiedCheck.join()

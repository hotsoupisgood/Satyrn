from flask import Flask, render_template, Markup
from util import getHtml, duplicate, displayArray, startModifiedCheck
from flask_socketio import SocketIO, emit
from multiprocessing import Process
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#Initialize processes
modifiedCheck=Process()

@app.route('/')
def home():
    jsloc, css, body = displayArray()
    return render_template('main.html', jsloc=jsloc, css=css, body=Markup(body))
@socketio.on('connect')
def connect():
    modifiedCheck=Process(target=startModifiedCheck)
    modifiedCheck.start()
    print('We are connected')
    
        
@socketio.on('disconnect')
def disconnect():
    modifiedCheck.terminate()
    modifiedCheck.join()
    print('Client disconnected')

if __name__ == '__main__':
    def startFlask():
        socketio.run(app, port=5000, debug=True)
    try:
        flask=Process(target=startFlask)
        flask.start()
    except KeyboardInterrupt:
        print("Terminating flask server.")
        flask.terminate()
        flask.join()
        modifiedCheck.terminate()
        modifiedCheck.join()

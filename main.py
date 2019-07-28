import subprocess
import sys
from flask import Flask
from flask import url_for
app = Flask(__name__)
from util import getHtml


@app.route('/')
def displayArray():
    subprocess.call([sys.executable, 'test.py'])
    rawArray=getHtml('test.py')
    displayText=''
    for x in rawArray:
        displayText=displayText+'<pre>'+''.join(x)+'</pre>'+'<img src="'+url_for('static', filename='testplot.png')+'">'
    return displayText

if __name__ == '__main__':
    app.run(debug=True)

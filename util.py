import importlib
import re
import subprocess
import sys
from flask import url_for
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def displayArray():
    fs=open('temp.py', 'w')

    rawArray=getHtml('test.py')
    plotCount=rawArray.pop()
    fs.write(duplicate(rawArray))
    subprocess.call([sys.executable, 'temp.py'])

    displayText=''
    css='<head><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script><script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js" ></script><script type="text/javascript" src="'+url_for('static', filename='main.js')+'"></script><style>'+HtmlFormatter().get_style_defs('.highlight')+'body {margin: 20px 50px;}img{width:90vw;}</style></head>'
    for x in rawArray:
        displayText=displayText+highlight(''.join(x), PythonLexer(), HtmlFormatter())
        if plotCount>0:
            displayText+='<img src="'+url_for('static', filename='testplot.png')+'">'
            plotCount-=1
    displayText='<body>'+displayText+'</body>'
    return css+displayText
def getHtml(fileName):
    fs=open(fileName, 'r')
    
    newFile=[]
    newBlock=[]
    plotCount=0
    for line in fs:
        if 'plt.plot' in line:
            plotCount+=1
            newBlock.append(line)
            newBlock.append("plt.savefig('static/plot"+str(len(newFile))+".png')")
            newFile.append(newBlock)
            newBlock=[]
        else:
            newBlock.append(line)
    newFile.append(newBlock)
    newFile.append(plotCount)
    return newFile
def  duplicate(structure):
    assembledText=''
    for x in structure:
        assembledText=assembledText+''.join(x)
    return assembledText

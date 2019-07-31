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
    for x in rawArray:
        displayText=displayText+highlight(''.join(x), PythonLexer(), HtmlFormatter())
        if plotCount>0:
            displayText+='<img src="'+url_for('static', filename='testplot.png')+'">'
            plotCount-=1
    return url_for('static', filename='main.js'),HtmlFormatter().get_style_defs('.highlight'), displayText
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

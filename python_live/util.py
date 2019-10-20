####
import glob
from hashlib import md5
from io import StringIO
import re
from subprocess import Popen, PIPE
import sys
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO
import time
import os

ledger = {}
myDir = os.path.dirname(os.path.abspath(__file__))
####

def displayArray(myFile):
    myDir = os.path.dirname(os.path.abspath(__file__))
    allPlots=sorted(glob.glob(myDir+'/static/plot[0-9].png'), key=os.path.getmtime)
    print(allPlots)
    for f in allPlots:
        os.remove(f)
    rawArray=getHtml(myFile)
    plotCount=rawArray.pop()
    strCode=duplicate(rawArray)
    process = Popen(['python3','-u', '-c', strCode], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    stdout=stdout.decode('utf-8')
    stderr=stderr.decode('utf-8')

    allPlots=glob.glob(myDir+'/static/plot[0-9].png')
    allPlots.sort(key=os.path.getmtime)
    allPlots.reverse()
    plotCount=len(allPlots)
    displayText=''
    for x in rawArray:
        displayText=displayText+highlight(''.join(x), PythonLexer(), HtmlFormatter())
        if plotCount>0:
            displayText+='<img src="'+url_for('static', filename=os.path.basename(allPlots.pop()))+'">'
            plotCount-=1
    if plotCount>0:
        for x in allPlots:
            displayText+='<img src="'+url_for('static', filename=os.path.basename(x))+'">'
    return url_for('static', filename='main.js'),HtmlFormatter().get_style_defs('.highlight'), displayText, highlight(stdout, BashLexer(), HtmlFormatter()), highlight(stderr, BashLexer(), HtmlFormatter())
def addSavePlot(fileString):
    fileArrayWithPlot=[]
    plotCount=0
    for line in fileString.split():
        if '###p' in line:
            fileArrayWithPlot.append("plt.savefig('"+myDir+"/static/plot"+str(plotCount)+".png')\n")
            plotCount+=1
        else:
            fileArrayWithPlot.append(line)
    flatArray='\n'.join(fileArrayWithPlot)
    return flatArray

def updateLedger(fileString, ledger):
    allCellsDict={}
    newCellsToRun=[]
    cellDelimiter='####'
    regex='(.*?)(?=\n####\n)'
    for cell in re.findall(regex, fileString, re.S):
        cellHash=md5(cell.encode()).hexdigest()
        allCellsDict[cellHash]=cell
    for cellHash in allCellsDict.keys():
        if cellHash not in ledger:
            newCellsToRun.append(cellHash)
            ledger[cellHash]=allCellsDict[cellHash]
    return newCellsToRun, ledger
ledgerScope={}
def doit():
    ledger={}
    newCellsToRun, ledger=updateLedger('test.py', ledger)
    runNewCells(newCellsToRun, ledger)
def runNewCells(newCellsToRun, ledger):
    for cell in newCellsToRun:
        cellToRun=ledger[cell]
        cellToRun=addSavePlot(cellToRun)
        exec(cellToRun, globals(), ledgerScope)
doit()
####
def  duplicate(structure):
    assembledText=''
    for x in structure:
        assembledText=assembledText+''.join(x)
    return assembledText

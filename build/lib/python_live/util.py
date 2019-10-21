from itertools import zip_longest
import datetime
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


def update(watchedFile, ledger, ledgerScope, myDir):
    testContent=''
    with open(watchedFile, 'r') as content_file:
        testContent=content_file.read()
    newCellsToRun, ledger=updateLedgerPop(testContent, ledger, myDir)
    print(newCellsToRun)
    output=runNewCells(newCellsToRun, ledger, ledgerScope, myDir)
    print(output)
    mainHtml, cssHtml, bodyHtml=convertLedgerToHtml(ledger, output, myDir)
    print(bodyHtml)
    return mainHtml, cssHtml, bodyHtml
def addSavePlot(fileString, myDir):
    fileArrayWithPlot=[]
    plotCount=0
    savefigText="plt.savefig('"+myDir+"/static/plot"+str(plotCount)+".png')"
    match = re.compile(r"###p")
    items = re.findall(match, fileString)
    for item in items:
        savefigText="plt.savefig('"+myDir+"/static/plot"+str(plotCount)+".png')"
        fileString=fileString.replace(item, savefigText)
    return fileString 
def updateLedgerPop(fileString, ledger, myDir):
    allCellsList=[]
    newCellsToRun=[]
    cellDelimiter='####\n'
    for cell in list(filter(None, fileString.split(cellDelimiter))):
        cellHash=md5(cell.encode()).hexdigest()
        allCellsList.append({'hash':cellHash, 'code':cell, 'datetime':datetime.datetime.now()})
    newCellsToRun=[currentCell if currentCell!=ledgerCell else None for currentCell, ledgerCell in zip_longest(allCellsList, ledger, fillvalue=None)]
    return newCellsToRun, allCellsList
def convertLedgerToHtml(ledger, std, myDir):
    allPlots=glob.glob(myDir+'/static/plot[0-9].png')
    allPlots.sort(key=os.path.getmtime)
    allPlots.reverse()
    plotCount=len(allPlots)
    displayText=''
    for cell in ledger:
        cellStd=std.pop(0)
        displayText+=highlight(cell['code'], PythonLexer(), HtmlFormatter())
        displayText+=highlight(cellStd['stdout'], BashLexer(), HtmlFormatter())
        displayText+=highlight(cellStd['stderr'], BashLexer(), HtmlFormatter())
        displayText+='<img src="'+url_for('static', filename=os.path.basename(allPlots.pop()))+'">'
    cssCode=HtmlFormatter().get_style_defs('.highlight')
    mainUrl=url_for('static', filename='main.js')
    return mainUrl, cssCode, displayText
def runNewCells(newCellsToRun, ledger, ledgerScope, myDir):
    cellOutput=[]
    print(ledger)
    for cell in newCellsToRun:
        cellToRun=addSavePlot(cell['code'], myDir)
        redirected_output=sys.stdout=StringIO()
        redirected_error=sys.stderr=StringIO()
        try:
            exec(cellToRun, globals(), ledgerScope)
            cellOutput.append({'stdout':redirected_output.getvalue(), 'stderr':redirected_error.getvalue()})
        except Exception as e:
            cellOutput.append({'stdout':redirected_output.getvalue(), 'stderr':str(e)})
        finally:
            sys.stdout=sys.__stdout__
            sys.stderr=sys.__stderr__

    return cellOutput

from itertools import zip_longest
import time
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
    print(ledger)
    output=runNewCells(newCellsToRun, ledger, ledgerScope, myDir)
#    print(output)
    mainHtml, cssHtml, bodyHtml=convertLedgerToHtml(ledger, output, myDir)
#    print(bodyHtml)
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
        allCellsList.append({'hash':cellHash, 'code':cell, 'datetime': time.strftime("%x %X", time.gmtime()), 'changed': False})
    newCellsToRun=getNewCellsToRun(ledger, allCellsList)
    return newCellsToRun, allCellsList
def getNewCellsToRun(ledger, allCellsList):
    newCellsToRun=[]
    for currentCell, ledgerCell in zip_longest(allCellsList, ledger, fillvalue=None):
        print(currentCell, ledgerCell)
        if currentCell!=ledgerCell:
            currentCell['changed']=True
        newCellsToRun.append(currentCell)
    return newCellsToRun
def convertLedgerToHtml(ledger, std, myDir):
    allPlots=glob.glob(myDir+'/static/plot[0-9].png')
    allPlots.sort(key=os.path.getmtime)
    allPlots.reverse()
    plotCount=len(allPlots)
    htmlBodyArray=[]
    for cell in ledger:
        cellStd=std.pop(0)
        htmlBodyArray.append({'datetime': cell['datetime'], 'code':highlight(cell['code'], PythonLexer(), HtmlFormatter()), 'stdout': highlight(cellStd['stdout'], BashLexer(), HtmlFormatter()), 'stderr': highlight(cellStd['stderr'], BashLexer(), HtmlFormatter()), 'plots': '<img src="'+url_for('static', filename=os.path.basename(allPlots.pop(0)))+'">'})
    cssCode=HtmlFormatter().get_style_defs('.highlight')
    mainUrl=url_for('static', filename='main.js')
    return mainUrl, cssCode, htmlBodyArray
def runNewCells(newCellsToRun, ledger, ledgerScope, myDir):
    cellOutput=[]
#    print(ledger)
    for cell in newCellsToRun:
        cellToRun=addSavePlot(cell['code'], myDir)
        redirected_output=sys.stdout=StringIO()
        redirected_error=sys.stderr=StringIO()
        try:
            exec(cellToRun, globals(), ledgerScope)
            cellOutput.append({'stdout':redirected_output.getvalue(), 'stderr': ''})
        except Exception as e:
            cellOutput.append({'stdout':'', 'stderr':str(e)})
        finally:
            sys.stdout=sys.__stdout__
            sys.stderr=sys.__stderr__
    return cellOutput

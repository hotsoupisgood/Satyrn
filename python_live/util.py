from itertools import zip_longest
import time, sys, datetime, glob, re, sys, time, os, copy
from hashlib import md5
from io import StringIO
from subprocess import Popen, PIPE
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO

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
def updateLedgerPop(oldAllCells, fileString, ledger, myDir):
    allCellsList=[]
    newLedger=[]
    newCellsToRun=[]
    cellDelimiter='####\n'
    for cell in list(filter(None, fileString.split(cellDelimiter))):
        cellHash=md5(cell.encode()).hexdigest()
        newLedger.append(cellHash)
        isChanged=False
        stdout='none'
        stderr='none'
        if cellHash not in ledger:
            isChanged=True
        for oldCell in oldAllCells:
            print(oldCell['stdout'])
            print(oldCell['hash'])
            if oldCell['hash']==cellHash:
                stdout=oldCell['stdout']
                stdtr=oldCell['stderr']
        allCellsList.append({'hash':cellHash, 'code':cell, 'plot':'None', 'datetime': time.strftime("%x %X", time.gmtime()), 'changed': isChanged, 'stdout':stdout, 'stderr':stderr})
    newCellsToRun=getNewCellsToRun(ledger, allCellsList)
    return newLedger, allCellsList
def getNewCellsToRun(ledger, allCellsList):
    newCellsToRun=[]
    for currentCell, ledgerCell in zip_longest(allCellsList, ledger, fillvalue=None):
        if currentCell['hash']!=ledgerCell:
            currentCell['changed']=True
        newCellsToRun.append(currentCell)
    return newCellsToRun
def convertLedgerToHtml(allCellsList, myDir):
    # Return a deep copy of allCellsList with code replaced with html-ized code
    tempCells=copy.deepcopy(allCellsList)
    allPlots=glob.glob(myDir+'/static/plot[0-9].png')
    allPlots.sort(key=os.path.getmtime)
    allPlots.reverse()
    for cell in tempCells:
        cell['code']=highlight(cell['code'], PythonLexer(), HtmlFormatter())
        if allPlots:
            cell['plot']='<img src="'+url_for('static', filename=os.path.basename(allPlots.pop(0)))+'">'
        else:
            cell['plot']=''
    plotCount=len(allPlots)
    return tempCells 
def runNewCells(newCellsToRun, ledger, globalScope, localScope, myDir, first=False):
    cellOutput=[]
    for cell in newCellsToRun or first==True:
        if cell['changed'] is True:
            cellToRun=addSavePlot(cell['code'], myDir)
#            stdout, stderr, globalScope, localScope=runWithCmd(cellToRun, globalScope, localScope)
            stdout, stderr=runWithExec(cellToRun, globalScope, localScope)
            cellOutput.append({'stdout':stdout, 'stderr':stderr})
            for newCell in newCellsToRun:
                if newCell['hash']==cell['hash']:
                    newCell['stdout']=stdout
                    newCell['stderr']=stderr
        else:
            cellOutput.append('')
    return cellOutput
def runWithCmd(cellCode, ledgerScope, localScope):
    setContextLoop='ledgerScope='+str(ledgerScope)+'\nfor scopeVar in ledgerScope.items():\n\tglobals()[scopeVar]=ledgerScope[scopeVar]\n'
    cellCode=setContextLoop+cellCode
    printContext='\nprint(globals())\nprint(locals())'
    process = Popen(['python3','-u', '-c', cellCode], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    stdout=stdout.decode('utf-8')
    stderr=stderr.decode('utf-8')
    splitStdout=stdout.split('\n')
    print(splitStdout)
    localScope=splitStdout[-1]
    globalScope=splitStdout[-2]
    return stdout, stderr, globalScope, localScope
def runWithExec(cellCode, globalScope, localScope):
    redirected_output=sys.stdout=StringIO()
    redirected_error=sys.stderr=StringIO()
    stdout=''
    stderr=''
    try:
        sys.path.append(os.getcwd())
        exec(cellCode, globalScope, localScope)
#        exec(cellCode, globals(), locals())
        stdout=redirected_output.getvalue()
        stderr=''
    except Exception as e:
        stdout=redirected_output.getvalue()
        stderr=str(e)
    finally:
        sys.path.pop()
        sys.stdout=sys.__stdout__
        sys.stderr=sys.__stderr__
    return stdout, stderr

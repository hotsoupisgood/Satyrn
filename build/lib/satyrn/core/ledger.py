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
import satyrn.core.constants as Constant

def updateChanged(cellsList):
    for cell in cellsList:
        cell['changed']=False
def updateLedgerPop(oldAllCells, fileString, ledger, myDir):
    allCellsList=[]
    newLedger=[]
    newCellsToRun=[]
    cellDelimiter='####\n'
    for cellCount, cell in enumerate(list(filter(None, fileString.split(cellDelimiter)))):
        cellHash=md5(cell.encode()).hexdigest()
        newLedger.append(cellHash)
        isChanged=False
        stdout=''
        stderr=''
        if cellHash not in ledger:
            isChanged=True
        for oldCell in oldAllCells:
#            print(oldCell['stdout'])
#            print(oldCell['hash'])
            if oldCell['hash']==cellHash:
                stdout=oldCell['stdout']
                stdtr=oldCell['stderr']
        allCellsList.append({'cellCount':str(cellCount), 'hash':cellHash, 'code':cell, 'plot':'', 'datetime': time.strftime("%x %X", time.gmtime()), 'changed': isChanged, 'stdout':stdout, 'stderr':stderr, 'image/png':''})
    newCellsToRun=getNewCellsToRun(ledger, allCellsList)
    return newLedger, allCellsList
def getNewCellsToRun(ledger, allCellsList):
    newCellsToRun=[]
    for currentCell, ledgerCell in zip_longest(allCellsList, ledger, fillvalue=None):
        if currentCell['hash']!=ledgerCell:
            currentCell['changed']=True
        newCellsToRun.append(currentCell)
    return newCellsToRun

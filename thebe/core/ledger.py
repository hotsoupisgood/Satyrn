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
import thebe.core.constants as Constants
import copy

def update(oldCellList, fileContent):
    '''
    '''

    cellList=[]
    sourceList=getSourceList(oldCellList)

    for cellCount, source in enumerate(list(filter(None, fileContent.split(Constants.CellDelimiter)))):
        #Hash to be used for identifying priviously run code
#        cellSource=hashCode(source)
        #Set outputs
        cell=setOutputs(oldCellList, source, sourceList)

        #Set Code
        cell['source']=source

        #Set cell count(it's order in the cell list)
        cellList.append(cell)
        cell['cellCount']=str(cellCount)

    return cellList

def getSourceList(cellList):
    '''
    Form the hashes from the cell list into a list
    '''
    return [cell['source'] for cell in cellList]

def setOutputs(oldCellList, cellSource, sourceList):
    '''
    Set outputs of cell depending on whether it has been run before 
    '''
    return assembleCell(oldCellList, sourceList, cellSource)

def assembleCell(oldCellList, sourceList, cellSource):
    '''
    If the source preexists, set new cell to old cell
    If not, set changed, and last changed time.
    '''

    cell=copy.deepcopy(Constants.Cell)

    try:
        x=sourceList.index(cellSource.splitlines(True))
        cell=oldCellList[x]

    except ValueError:
        cell['changed']=True
        cell['last_changed']=time.strftime("%x %X", time.gmtime())

    return cell

#Hash the string of code
def hashSource(source):
    return md5(source.encode()).hexdigest()

#Old func for pre=try/catch
def isChanged(cellSource, sourceList):
        try:
            sourceList.index(cellSource)
            return True
        except ValueError:
            return False

#Old func 
def getNewCellsToRun(ledger, allCellsList):
    newCellsToRun=[]
    for currentCell, ledgerCell in zip_longest(allCellsList, ledger, fillvalue=None):
        if currentCell['hash']!=ledgerCell:
            currentCell['changed']=True
#            print(oldCell['stdout'])
#            print(oldCell['hash'])
        newCellsToRun.append(currentCell)
    return newCellsToRun

#Old func for when using dict of lists
def dictToList(cellDict):
    cellList=[]
    keys=cellDict.keys()
    values=cellDict.values()
    for cell in np.array(values).t:
        cellList.append(dict(zip(keys, cell)))
    return cellList        

def updateChanged(changedList):
    changedList=[False for x in changedList]

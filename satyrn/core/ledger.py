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
import satyrn.core.constants as Constants
import copy

def dictToList(cellDict):
    cellList=[]
    keys=cellDict.keys()
    values=cellDict.values()
    for cell in np.array(values).t:
        cellList.append(dict(zip(keys, cell)))
    return cellList        

#def updateCells(oldCellDict, fileContent):
def update(oldCellList, fileContent):
    cellList=[]
#    cellDict=copy.deepcopy(Constant.CellDict)
    hashList=getHashList(oldCellList)
    for cellCount, code in enumerate(list(filter(None, fileContent.split(Constants.CellDelimiter)))):
        #Id list
#        cellDict['id'].append(cellCount)  
        #Append code
#        cellDict['code'].append(code)
        #Hash to be used for identifying priviously run code
        cellHash=hashCode(code)
        #Set outputs
        cell=setOutputs(oldCellList, cellList, cellHash, hashList)
        #Set Code
        cell['code']=code
        #That cell count(it's order in the cell list)
        cell['cellCount']=str(cellCount)
        cellList.append(cell)
#    return hashList, cellList
    return cellList

#Form the hashes from the cell list into a list
def getHashList(cellList):
    return [cell['hash'] for cell in cellList]

#Set outputs of cell depending on whether it has been run before 
def setOutputs(oldCellList, cellList, cellHash, hashList, dl='list'):
    #for one cell
    if dl=='list':
        return assembleCell(oldCellList, hashList, cellHash)
    else:
        cellDict['hash'].append(cellHash)
        try:
            x=oldCellDict['hash'].index(cellHash)
            cellDict['changed'].append(False)
            cellDict['stdout'].append(oldCellDict['stdout'][x])
            cellDict['stderr'].append(oldCellDict['stderr'][x])
            cellDict['image/png'].append(oldCellDict['image/png'][x])
        except IndexError:
            cellDict['changed'].append(True)
            cellDict['stdout'].append('')
            cellDict['stderr'].append('')
            cellDict['image/png'].append('')

#More if the hash exists set new cell to old cell
def assembleCell(oldCellList, hashList, cellHash):
        cell=copy.deepcopy(Constants.Cell)
        '''
        If the current cell existed before, fill its outputs.
        '''

        try:
            x=hashList.index(cellHash)
            cell=oldCellList[x]
            cell['changed']=True
        except ValueError:
            cell['time']=time.strftime("%x %X", time.gmtime())
            cell['hash']=cellHash
        return cell

def isChanged(cellHash, hashList):
        try:
            hashList.index(cellHash)
            return True
        except ValueError:
            return False
#    if cellHash in hashList:
#        return False
#    else:
#        return True

def getNewCellsToRun(ledger, allCellsList):
    newCellsToRun=[]
    for currentCell, ledgerCell in zip_longest(allCellsList, ledger, fillvalue=None):
        if currentCell['hash']!=ledgerCell:
            currentCell['changed']=True
#            print(oldCell['stdout'])
#            print(oldCell['hash'])
        newCellsToRun.append(currentCell)
    return newCellsToRun

def hashCode(code):
    return md5(code.encode()).hexdigest()

def updateChanged(changedList):
    changedList=[False for x in changedList]

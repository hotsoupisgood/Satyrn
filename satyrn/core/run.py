from itertools import zip_longest
import copy
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

gs={}
ls={}
def getPlotData(globalScope, localScope):
    code=Constant.GetPlot
    redirected_output=sys.stdout=StringIO()
    redirected_error=sys.stderr=StringIO()
    stdout=''
    stderr=''
    try:
        sys.path.append(os.getcwd())
        exec(code, globalScope, localScope)
        stdout=redirected_output.getvalue()
        stderr=''
    except Exception as e:
        stdout=redirected_output.getvalue()
        stderr=str(e)
    sys.path.pop()
    sys.stdout=sys.__stdout__
    sys.stderr=sys.__stderr__
    if stdout==Constant.EmptyGraph:
        stdout=''
    return stdout
def runNewCells(cellsToRun, ledger, globalScope, localScope, myDir):
    cellOutput=[]
    cgs=copy.deepcopy(gs)
    for cellCount, cell in enumerate(cellsToRun):
        stdout, stderr, plotData=runWithExec(cell['code'], globalScope, localScope)
#        print('equil %s' % eq)
#        cgs=copy.deepcopy(gs)
        if not cell['changed']==True:
            stdout=cellsToRun[cellCount]['stdout']
            stderr=cellsToRun[cellCount]['stderr']
            plotData=cellsToRun[cellCount]['image/png']
        # Keep the master list updated
        cellsToRun[cellCount]['stdout']=stdout
        cellsToRun[cellCount]['stderr']=stderr
        cellsToRun[cellCount]['image/png']=plotData
        cellOutput.append({'stdout':stdout, 'stderr':stderr, 'image/png':plotData})
    return cellOutput
def runWithExec(cellCode, globalScope, localScope):
    #runs one cell of code and return plotdata and std out/err
    redirected_output=sys.stdout=StringIO()
    redirected_error=sys.stderr=StringIO()
    stdout=''
    stderr=''
    try:
        sys.path.append(os.getcwd())
        exec(cellCode, globalScope, localScope)
        stdout=redirected_output.getvalue()
        stderr=''
    except Exception as e:
        stdout=redirected_output.getvalue()
        stderr=str(e)
    finally:
        sys.path.pop()
        sys.stdout=sys.__stdout__
        sys.stderr=sys.__stderr__
    plotData=getPlotData(globalScope, localScope)
    return stdout, stderr, plotData

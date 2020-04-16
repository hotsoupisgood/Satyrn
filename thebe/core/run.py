from itertools import zip_longest
import time, sys, datetime, glob, re, sys, time, os, copy, logging
from hashlib import md5
from io import StringIO
from subprocess import Popen, PIPE
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO
import thebe.core.constants as Constant
from thebe.core.output import outputController 


def runNewCells(cellsToRun, globalScope, localScope):
    '''
    Run each changed cell, returning the output.
    '''

    cellOutput = []
    for cellCount, cell in enumerate(cellsToRun):
        #Keep the master list updated
        if cell['changed']:

            stdout, stderr, plotData = runWithExec(cell['source'], globalScope, localScope)

            clearOutputs(cell)

            fillPlot(cell, plotData)
            fillStdOut(cell, stdout)
            fillErr(cell, stderr)

            # How does ipython do this?
            cell['changed']=False

            cell['source'] = cell['source'].splitlines(True)

        cellOutput.append(cell)
#    print('After run:\t%s'%[cell['image/png'][-10:] for cell in cellsToRun])

    return cellOutput

def runWithExec(cellCode, globalScope, localScope):
    '''
    runs one cell of code and return plotdata and std out/err
    '''

#    redirected_output=sys.stdout=StringIO()
#    redirected_error=sys.stderr=StringIO()
#
    stdout=''
    stderr=''
    def execPros():
        exec(cellCode, globalScope, localScope)

    outputController.open()
    try:
        sys.path.append(os.getcwd())
        exec(cellCode, globalScope, localScope)
        stdout, stderr = outputController.close()
#        stdout=redirected_output.getvalue()
#        stderr=''

    except Exception as e:
        stdout, stderr = outputController.close()
#        stdout=redirected_output.getvalue()
#        stderr=str(e)

    finally:
        sys.path.pop()
#        sys.stdout=sys.__stdout__
#        sys.stderr=sys.__stderr__

    plotData=getPlotData(globalScope, localScope)

    return stdout, stderr, plotData
def collectOutput(function):
    outputController.open()
    returns = () = function()
    outputController.close()
    return returns

def getPlotData(globalScope, localScope):
    '''
    '''

    code=Constant.GetPlot
    redirected_output=sys.stdout=StringIO()
    redirected_error=sys.stderr=StringIO()
    stdout=''
    stderr=''
    sys.path.append(os.getcwd())
    try:
        exec(code, globalScope, localScope)
        stdout=redirected_output.getvalue().rstrip()
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

def clearOutputs(cell):
    '''
    Replace list of outputs with an empty one.
    '''
    cell['outputs'] = []

def fillPlot(cell, plot):
    '''
    If an image exists in the plot variable, create and return a plot cell.
    '''
    if plot:
        output = Constant.getDisplayOutput()
        output['data']['image/png'] = plot
        cell['outputs'].append(output)

def fillStdOut(cell, stdOut):
    '''
    If an output exists in the stdOut variable, create and return a stdOut cell.
    '''
    if stdOut:
        output = Constant.getExecuteOutput()
        output['data']['text/plain'] = stdOut.splitlines(True)
        cell['outputs'].append(output)

def fillErr(cell, err):
    '''
    If an output exists in the err variable, create and return a err cell.
    '''
    if err:
        output = Constant.getErrorOutput()
        output['traceback'] = err.splitlines(True)
        cell['outputs'].append(output)

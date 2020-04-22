from itertools import zip_longest
from multiprocessing import Process
import time, sys, datetime, glob, re, sys, time, os, copy, logging, threading
from hashlib import md5
from io import StringIO
from subprocess import Popen, PIPE
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO
import thebe.core.constants as Constant
import thebe.core.output as output 
#from thebe.core.output import outputController 

def runNewCells(cellsToRun, globalScope, localScope):
    '''
    Run each changed cell, returning the output.
    '''

    cellOutput = []
    for cellCount, cell in enumerate(cellsToRun):
        #Keep the master list updated
        if cell['changed']:
            logging.info('Running cell #%s'%(cellCount,))
            stdout, stderr, plotData = runWithExec(cell['source'], globalScope, localScope)

            clearOutputs(cell)

            fillPlot(cell, plotData)
            fillStdOut(cell, stdout)
            fillErr(cell, stderr)

            # How does ipython do this?
            cell['changed']=False

#            logging.debug('Cell source, in output class:\t%s\n'%(cell['source']))

        cellOutput.append(cell)

    return cellOutput

def runWithExec(cellCode, globalScope, localScope):
    '''
    runs one cell of code and return plotdata and std out/err
    '''
    
    #Save the old output location
    oldstdout = sys.stdout

    #Redirect system output, and initialize system error
    stdout = sys.stdout=StringIO()
    stderr = ''

    #Append the current working directory to path(not sure if this is necessary)
    sys.path.append(os.getcwd())

    try:
        print('before start')
        exec(''.join(cellCode), globalScope, localScope)
        print('after start')
    except Exception as e:
        stderr = str(e)

    finally:
        sys.path.pop()

        sys.stdout = oldstdout

        stdout = stdout.getvalue() 

    plotData = getPlotData(globalScope, localScope)

    localScope = {} if localScope == None else localScope

    return stdout, stderr, plotData

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
    If an output exists in the stdOut variable append new output to cell reference.
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

class RunController:
    def __init__(self):
        self.localScope = {}
        self.globalScope = {}
        self.isActive = False

    def runNewCells(cellsToRun, globalScope, localScope):
        '''
        Run each changed cell, returning the output.
        '''

        cellOutput = []
        for cellCount, cell in enumerate(cellsToRun):
            #Keep the master list updated
            if cell['changed']:
                logging.info('Running cell #%s'%(cellCount,))
                stdout, stderr, plotData = runWithExec(cell['source'], globalScope, localScope)

                clearOutputs(cell)

                fillPlot(cell, plotData)
                fillStdOut(cell, stdout)
                fillErr(cell, stderr)

                # How does ipython do this?
                cell['changed']=False

    #            logging.debug('Cell source, in output class:\t%s\n'%(cell['source']))

            cellOutput.append(cell)

        return cellOutput

    def runWithExec(self, cellCode, globalScope, localScope):
        '''
        runs one cell of code and return plotdata and std out/err
        '''
        
        #Save the old output location
        oldstdout = sys.stdout
    
        #Redirect system output, and initialize system error
        stdout = sys.stdout=StringIO()
        stderr = ''

        #Append the current working directory to path(not sure if this is necessary)
        sys.path.append(os.getcwd())

        try:
            print('before start')
            exec(''.join(cellCode), globalScope, localScope)
            print('after start')
        except Exception as e:
            stderr = str(e)

        finally:
            sys.path.pop()

            sys.stdout = oldstdout

            stdout = stdout.getvalue() 

        plotData = getPlotData(globalScope, localScope)

        localScope = {} if localScope == None else localScope

        return stdout, stderr, plotData

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
        If an output exists in the stdOut variable append new output to cell reference.
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

import thebe.core.database as Database
import thebe.core.run as Run
import thebe.core.html as Html
import thebe.core.data as data
import thebe.core.constants as Constants 
import os, time, logging, json, threading

def checkUpdate(socketio, fileLocation, connected=False, \
        isIpynb=False, GlobalScope=None, LocalScope=None, Cells=None):
#    print('cells:\n-------------------------------\n%s'%(Cells,))
    '''
    Combines isModified and update functions. 
    '''
    
    '''
    If code is currently being executed,
    stop checkUpdate. Send some feedback to client.
    '''
#    if GlobalScope == None or LocalScope == None or Cells == None:
    Cells, iGlobalScope, iLocalScope  = Database.getLedger(fileLocation)
    isActive = Database.getIsActive(fileLocation)
    #Get file target information from database if it exists

    #If it's modified or if it's the first time it has run, update.
    if isModified(fileLocation):
        if isActive:
            logging.info('flashing')
            socketio.emit('flash')
        else:
            thread = update(socketio, fileLocation, GlobalScope, LocalScope, Cells, isIpynb)

    elif connected==True:
        if not isActive:
            if not GlobalScope:
                thread = update(socketio, fileLocation, GlobalScope, LocalScope, Cells, isIpynb)
            else: 
                socketio.emit('show all', Cells)
        else:
            socketio.emit('show all', Cells)

    else:
        pass
    time.sleep(.5)

#Run code and send code and outputs to client
def update(socketio, fileLocation, GlobalScope, LocalScope, Cells, isIpynb):
    isActive = Database.setIsActive(fileLocation)

    '''
    Get some variables from database
    '''

    '''
    Get target file
    '''
    fileContent=''
    with open(fileLocation, 'r') as file_content:
        fileContent=file_content.read()
    '''
    Look at the file to see if anything has changed
    in the data.
    Return an updated ipynb,
    with proper changed values.
    '''
    Cells = data.update(Cells, fileContent)
    socketio.emit('show all', Cells)

    '''
    Send a list of the cells that will run to the
    client so it can show what is loading.
    '''
#    socketio.emit('show loading', htmlAllCells)

    def runThread(Cells, GlobalScope, LocalScope):
        '''
        Run the newly changed cells and return their output.
        '''
        Cells = Run.runNewCells(socketio, Cells, GlobalScope, LocalScope)

        '''
        Send output to client
        '''
        #socketio.emit('show output', output)
        executions = Database.getExecutions(fileLocation)
        executions += 1
        logging.info('The number of code executions is %d' % executions)
    #    html=Html.convertLedgerToHtml(Cells)
        socketio.emit('show all', Cells)

        '''
        Update the database with the fresh code.
        '''
        Database.setActive(fileLocation, False)
        Database.update(fileLocation, Cells, GlobalScope, LocalScope, executions)
        if isIpynb:
            updateIpynb(fileLocation, Cells)
    t = threading.Thread(target = runThread, args = (Cells, GlobalScope, LocalScope))
    t.start()
    return t

def updateIpynb(fileLocation, Cells):
    '''
    Write the new changes to the ipynb file.
    '''
    with open(fileLocation.split('.')[0]+'.ipynb', 'w') as f:
        ipynb = Constants.getIpynb()
        ipynb['cells'] = Cells
        json.dump(ipynb, f)

def isModified(fileLocation, x=.5):
    '''
    Return true if the target file has been modified in the past x amount of time
    '''

    lastModified=os.path.getmtime(fileLocation)
    timeSinceModified=int(time.time()-lastModified)

    if timeSinceModified<=x:
        return True
    else:
        return False


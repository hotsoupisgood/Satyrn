import thebe.core.database as Database
import thebe.core.run as Run
import thebe.core.html as Html
import thebe.core.ledger as Ledger
import os
import time

def checkUpdate(socketio, fileLocation, connected=False):
    '''
    Combines isModified and update functions. 
    '''

    #Get file target information from database if it exists
    Cells, GlobalScope, LocalScope  = Database.getLedger(fileLocation)

    #If it's modified or if it's the first time it has run, update.
    if isModified(fileLocation) or not GlobalScope:
        time.sleep(1)
        update(socketio, fileLocation, GlobalScope, LocalScope, Cells)
        time.sleep(1)

    elif connected==True:
        html=Html.convertLedgerToHtml(Cells)
        socketio.emit('show all', html)

    else:
        time.sleep(1)

def isModified(fileLocation, x=1):
    '''
    Return true if the target file has been modified in the past x amount of time
    '''

    lastModified=os.path.getmtime(fileLocation)
    timeSinceModified=int(time.time()-lastModified)

    if timeSinceModified<=x:
        return True
    else:
        return False

#Run code and send code and outputs to client
def update(socketio, fileLocation, GlobalScope, LocalScope, Cells):
    #print('gspre %s' % GlobalScope)
    '''
    Get some variables from database
    '''
    executions=Database.getExecutions(fileLocation)

    '''
    Get target file
    '''
    fileContent=''
    with open(fileLocation, 'r') as file_content:
        fileContent=file_content.read()
    '''
    Look at the file to see if anything has changed
    in the ledger.
    If there is a change, return updated ledger, and a list
    of cells that need executing.
    '''
    Cells=Ledger.update(Cells, fileContent)

    '''
    Send a list of the cells that will run to the
    client so it can show what is loading.
    '''
#    socketio.emit('show loading', htmlAllCells)

    '''
    Run the newly changed cells and return their output.
    '''
    output=Run.runNewCells(Cells, GlobalScope, LocalScope)
#    print('After run:\t%s'%[cell['stdout'] for cell in Cells])
    #output=Run.cells(Cells, GlobalScope, LocalScope)

    '''
    Send output to client
    '''
    #print('\nOutput list:\n %s' % output)
    #socketio.emit('show output', output)
#    Ledger.updateChanged(Cells)
    executions += 1
    print('The number of code executions is %d' % executions)
#    html=Html.convertLedgerToHtml(Cells)
    socketio.emit('show all', Cells)

    '''
    Update the database with the fresh code.
    '''
    Database.update(fileLocation, Cells, GlobalScope, LocalScope, executions)


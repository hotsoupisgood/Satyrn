import os, json, logging

def setup(targetName):
    '''
    Checks if the command line argument file is ipynb format,
    if it is, write a new file of the same prefix to the same
    directory, containing only the source files in thebe format.
    Return that new file name and a true flag.

    If .py file extension, return the same file
    name that was inputted and a false flag.
    '''
    if isIpynb(targetName):
        ipynbFileContent = loadIpynb(targetName)
        tempName = write_temp(ledger.toThebe(ipynbFileContent), targetName)
        return tempName, True
    else:
        return targetName, False

        
def isIpynb(targetLocation):
    '''
    Return the target's file extension. 
    If input is incorrect, explain, and quit the application.
    '''
    if os.path.isfile(targetLocation):
        try:
            return test_extension(targetLocation) == 'ipynb'
        except ValueError:
            logging.info('Please use a valid file extension. (.ipynb or .py)')
            sys.exit()
    else:
        logging.info('Thebe only works with files, not directories. Please try again with a file. (.ipynb or .py)')
        sys.exit()

def test_extension(targetLocation):
    '''
    '''

    targetExtension=targetLocation.split('.')[1]
    if targetExtension=='ipynb':
        return 'ipynb'
    elif targetExtension=='py':
        return 'py'
    else:
        logging.info('Please use a valid file extension. (.ipynb or .py)')
        sys.exit()

def loadIpynb(targetLocation):
    '''
    Return the ipynb file as a dictionary.
    '''

    data = {}
    with open(targetLocation) as ipynb_data:
        data = json.load(ipynb_data)
    return data

def write_temp(initialData, fileName):
    '''
    Create a temporary file and load it with our initial data from the ipynb file.
    Open vim in our temporary file.
    '''
    filePrefix = getPrefix(fileName)
    tempName = '%s.py'%(targetPrefix)

    try:
        open(tempName, 'w') as f:
            f.write(initialData)
    except KeyboardInterrupt:
        removeTemp()

    return tempName

def removeTemp(:
    '''
    '''
    os.remove(tempName)

def getPrefix(fileName):
    return targetName.split('.')[0]


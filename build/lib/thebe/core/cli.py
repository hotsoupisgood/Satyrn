import os, json, logging
        
def test_file(targetLocation):
    '''
    Return the relevant extension. 
    If input is incorrect, explain, and quit the application.
    '''
    if os.path.isfile(targetLocation):
        try:
            return test_extension(targetLocation)
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

def load_ipynb(targetLocation):
    '''
    Return the ipynb file as a dictionary.
    '''

    data = {}
    with open(targetLocation) as ipynb_data:
        data = json.load(ipynb_data)
    return data

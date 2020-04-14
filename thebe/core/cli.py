import os, json
def test_file_input(targetLocation):
    if os.path.isfile(targetLocation):
        try:
            test_extension(targetLocation)
        except ValueError:
            print('Please use a valid file extension. (.ipynb or .py)')
            sys.exit()
    else:
        print('Thebe only works with files, not directories. Please try again with a file. (.ipynb or .py)')
        sys.exit()
def test_extension(targetLocation):
    targetExtension=targetLocation.split('.')[1]
    if targetExtension=='ipynb':
        print('Is .ipynb')
        load_ipynb(targetLocation)
    elif targetExtension=='py':
        print('Is .py')
    else:
        print('Please use a valid file extension. (.ipynb or .py)')
        sys.exit()
def load_ipynb(targetLocation):
    data = {}
    with open(targetLocation) as ipynb_data:
        data = json.load(ipynb_data)
    return data

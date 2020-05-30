from jupyter_client.manager import start_new_kernel
import thebe.core.file as File
import thebe.core.constants as Constant
import thebe.core.output as output 
import thebe.core.logger as Logger
import thebe.core.database as Database
import thebe.core.html as Html
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer, MarkdownLexer
from pygments.formatters import HtmlFormatter
import pypandoc, time, sys, datetime, glob, re, sys, time, os, copy, logging, threading, queue, json

class jupyter_client_wrapper:
    def __init__(self, fileName):
        # Setting up self.loggers
        self.logger = Logger.getLogger('update.log', 'main')
        self.mess_logger = Logger.getLogger('mess.log', 'mess')
        self.status_logger = Logger.getLogger('status.log', 'status')
        self.execute_logger = Logger.getLogger('execute.log', 'execute')


        self.kernel_manager, self.jupyter_client = start_new_kernel()
        # Determine what kind of file working with
        self.fileLocation, is_ipynb = File.setup(fileName)

        # Initialize some variables
        self.isActive = False
        self.executionThread = None
        self.Cells = []
        self.executions = 0

        # Initialize local and global scope for old
        # execution engine
        self.LocalScope = {}
        self.GlobalScope = {}

    '''
    -------------------------------
    Setter functions
    -------------------------------
    '''
    def setSocket(self, socketio):
        self.socketio = socketio

    '''
    -------------------------------
    Execution pre-preprocessing
    -------------------------------
    '''

    def execute(self, update = 'changed'):
        #self.Cells = Database.getCells(self.fileLocation)

        if update == 'changed':
            self.mess_logger.info('executing with changed argument')
            self._execute_changed()
        elif update == 'all':
            self._execute_all()
        elif update == 'connected':
            self.mess_logger.info('executing with connected argument')
            self._execute_connected()
        else:
            pass

        time.sleep(.5)

    '''
    -------------------------------
    Execution pre-preprocessing - Helpers
    -------------------------------
    '''

    def _execute_changed(self):
        if self.isActive and self._isModified():
            self.logger.info('flashing')
            self.socketio.emit('flash')
        else:
            self.isActive = True
            self._execute(self)

    def _execute_all(self):
        self.logger.info('Run All Has Been Triggered!')
        if self.isActive:
            self.socketio.emit('flash')
        else:
            self.isActive = True
            self.Cells = []
            self._execute(self, runAll)

    def _execute_connected(self):
        if not self.Cells and not self.isActive:
            self.isActive = True
            self._execute(self)
        else: 
            self.socketio.emit('show all', self._convert())
        time.sleep(.5)

    '''
    -------------------------------
    Execution - Main - Helpers
    -------------------------------
    '''

    def _execute(self, update = 'changed'):
        '''
        Execute cells based on 'update' value
        '''
        self.status_logger.info('Updating...')
        self._update(self._getFileContent(), update)
        self.status_logger.info('Showing...')
        self.socketio.emit('show all', self._convert())
        '''
        Send a list of the cells that will run to the
        client so it can show what is loading.
        '''
        self.status_logger.info('Executing...')
        self.executionThread = threading.Thread(target = self._executeThread)
        self.executionThread.daemon = True
        self.executionThread.start()

    def _update(self, fileContent, update):
        '''
        Update the 'Cells' variable with new data from
        the Thebe file
        '''
        self.logger.info('file content: %s'%(fileContent,))

        # 'cells' is for the new cells
        cells = []

        # Ignore code that comes before the first delimiter
        ignoreFirst = self._ignoreFirst(fileContent)

        for cellCount, source in enumerate(fileContent.split(Constant.CellDelimiter)):
            # Ignore the first source if a cell delimiter
            # does not preceed it
            if ignoreFirst:
                ignoreFirst = False
                continue

            #Split source by line
            source = source.splitlines(True)

            if self._validSource(source):
                # Get copy of cell initially populated
                cell = copy.deepcopy(Constant.Cell)


                cell = self._setMarkdown(source, cell)
                cell = self._setChanged(source, cell)

                # This activates if the user clicks the run all button
                if update == 'all':
                    cell['changed'] = True

                # Set execution counter if it exists previously
                try:
                    cell['execution_count'] = self.Cells[cellCount]['execution_count'] 
                except IndexError:
                    pass
                cells.append(cell)

        self.Cells = cells
        self.execute_logger.info('Cells: "%s"'%(str(self.Cells)[0:20],))

    def _executeThread(self):
        '''
        Run the newly changed cells and return their output.
        '''
        self.logger.info('------------------\nOutput before update\n-------------------------------\n%s'%([cell['outputs'] for cell in self.Cells],))
        self.Cells = self._runNewCells()
        self.logger.info('------------------\nOutput after update\n-------------------------------\n%s'%([cell['outputs'] for cell in self.Cells],))
#        self.executions = Database.getExecutions(self.fileLocation)
        self.executions += 1
        self.logger.info('The number of code executions is %d' % self.executions)
#        self.socketio.emit('show all', self._convert())

        '''
        Update the database with the fresh code.
        And outputs.
        '''
#        Database.setActive(self.fileLocation, False)
#        Database.update(self.fileLocation, self.Cells, GlobalScope, LocalScope, executions)
        self._updateIpynb()
    '''
    -------------------------------
    Actual execution
    -------------------------------
    '''
    def _runNewCells(self):
        '''
        Run each changed cell, returning the output.
        '''

        # Append cells containing updated output to this
        newCells = []

        # Toggle to true when the users code produces an
        # error so code execution can stop
        kill = False

        for cellCount, cell in enumerate(self.Cells):

            # Run changed code if it is not markdown
            # and no prior cell has triggered an error
            if cell['changed']:
                self.socketio.emit('message', 'Running cell #%s...'%(cellCount))
                self.socketio.emit('loading', cellCount)
                if cell['cell_type'] != 'markdown' and not kill:
                    self.logger.info('\n------------------------\nRunning cell #%s\nIn directory: %s\nWith code:\n%s\n-------------------------------'%(cellCount, os.getcwd(), cell['source']))

                    # Execute the code from the cell, stream 
                    # outputs using socketio, and return output
                    outputs = self._jExecute(cell['source'])

                    # Prevent subsequent execution of code
                    # if in error was found
                    if self._hasError(outputs):
                        kill = True

                    # Add output data to cell
                    cell['outputs'] = outputs

                    # How does ipython do this?
                    cell['changed'] = False
                    cell['execution_count'] = cell['execution_count'] + 1
                    self.logger.info('exe co: %s'%(cell['execution_count'],))

            # Append run cell the new cell list
            newCells.append(cell)

        # Stop the front end loading
        self.socketio.emit('stop loading')

        return newCells

    def _jExecute(self, code):
        '''
        '''

        code = ''.join(code)

        # Execute the code
        msg_id = self.jupyter_client.execute(code)

        # Collect the response payload
        # reply = self.jupyter_client.get_shell_msg(msg_id)

        # Get the execution status
        # When the execution state is "idle" it is complete
        io_msg_content = self.jupyter_client.get_iopub_msg(timeout=1)['content']

        # We're going to catch this here before we start polling
        if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
            self.logger.debug('No output!')

        # Initialize the temp variable
        temp = {}

        # Initialize outputs
        outputs = []

        # Continue polling for execution to complete
        # which is indicated by having an execution state of "idle"
        while True:
            # Save the last message content. This will hold the solution.
            # The next one has the idle execution state indicating the execution
            # is complete, but not the stdout output
            temp = io_msg_content

            # Check the message for various possibilities
            if 'data' in temp: # Indicates completed operation
                if 'image/png' in temp['data']:
                    plotData =  temp['data']['image/png']
                    output = self._getPlotOutput(plotData)
                    outputs.append(output)

                    self.socketio.emit('output', output)

            if 'name' in temp and temp['name'] == "stdout": # indicates output
                # Create output for server use
                output = self._getStdOut(temp['text'])
                outputs.append(output)

                # Send HTML output for immediate front end use
                htmlOutput = copy.deepcopy(output)
                htmlOutput['data']['text/plain'] = [Html.convertText(text, ttype = 'bash') for text in htmlOutput['data']['text/plain']]
                self.socketio.emit('output', htmlOutput)

            if 'evalue' in temp: # Indicates error

                # Create output for server use
                output = getErr(temp['evalue'])
                outputs.append(output)

                # Send HTML output for immediate front end use
                htmlOutput = deepcopy(output)
                htmlOutput['evalue'] = [Html.convertText(text, ttype = 'bash') for text in htmlOutput['evalue']]
                self.socketio.emit('output', htmlOutput)
                
                # If there is an error than it is pointless 
                # to keep on running code
                break

            # Poll the message
            try:
                self.logger.info('Retrieving message...')
                io_msg_content = self.jupyter_client.get_iopub_msg()['content']
                time.sleep(.1)

                if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
                    break

            except queue.Empty:
                break

        return outputs

    '''
    -------------------------------
    Execution helper functions
    -------------------------------
    '''
    def _hasError(self, outputs):
        '''
        If an error cell exists in outputs
        return true
        '''
        for output in outputs:
            if 'evalue' in output:
                return True
        return False

    def _fillPlot(cell, plot):
        '''
        If an image exists in the plot variable, create and return a plot cell.
        '''
        if plot:
            output = Constant.getDisplayOutput()
            output['data']['image/png'] = plot
            cell['outputs'].append(output)
        return cell

    def _getPlotOutput(self, plot):
        '''
        '''
        output = Constant.getDisplayOutput()
        output['data']['image/png'] = plot
        return output

    def _getStdOut(self, stdOut):
        output = Constant.getExecuteOutput()
        output['data']['text/plain'] = stdOut.splitlines(True)
        return output

    def _getErr(err):
        output = Constant.getErrorOutput()
        output['evalue'] = err.splitlines(True)
        return output
    '''
    -------------------------------
    Preprocessing helper functions
    -------------------------------
    '''

    def _getFileContent(self):
        fileContent = ''
        with open(self.fileLocation, 'r') as file_content:
            fileContent = file_content.read()
        return fileContent

    def _update_all(self):
        # 'cells' is for the new cells
        cells = []


    def _ignoreFirst(self, fileContent):
        # Ignore code that comes before the first delimiter
        if not fileContent.startswith(Constant.CellDelimiter):
            self.logger.info('Ignoring first...')
            return True
        else:
            return False

    def _getSourceList(self):
        '''
        Form the hashes from the cell list into a list
        '''
        return [cell['source'] for cell in self.Cells]

    def _toThebe(self, ipynb):
        '''
        Take in a ipynb dictionary, and returns a string in thebe format.
        (Cell sources to delimited by our Constants.CellDelimiter)
        '''

        output = ''
        for cell in ipynb['cells']:
            if cell['cell_type'] == 'markdown':
                output = ''. join(\
                        (output, \
                        (Constant.CellDelimiter + 'm\n' + \
                        ''.join(cell['source']))\
                        ))
            else:
                output = ''. join(\
                        (output, \
                        (Constant.CellDelimiter + '\n' + \
                        ''.join(cell['source']))\
                        ))
        return output
        

    def _setChanged(self, source, cell):
        '''
        Detect if a cell has been changed
        '''
        try:
            x = self._getSourceList().index(source)
            cell = self.Cells[x]

        except ValueError:
            cell['changed'] = True
            cell['last_changed'] = time.strftime("%x %X", time.gmtime())

        return cell

    def _setMarkdown(self, source, cell):
        '''
        Determine if a cell is marked down
        '''

        # Detect if cell is Markdown
        if source[0] == 'm\n':
            # Remove the markdown identifier
            source.pop(0)
            # Set cell as markdown
            cell['cell_type'] = 'markdown'
        else:
            # Remove the new line after the delimiter
            source.pop(0)

        #Set sourceCode
        cell['source'] = source

        return cell

    def _validSource(self, source):
        '''
        Return false if source list is all Just new lines
        '''
        for s in source:
            if s != '\n':
                return True
        return False

    def _updateIpynb(self):
        '''
        Write the new changes to the ipynb file.
        '''
        cCells = copy.deepcopy(self.Cells)

        # Remove extra attributes created by thebe.
        self._sanitize(cCells)
        

        # Save cells into a ".ipynb" file
        with open(File.getPrefix(self.fileLocation)+'.ipynb', 'w') as f:
            # Get the jupyter cell list wrapper
            ipynb = Constant.getIpynb()
            # Wrap cells
            ipynb['cells'] = cCells
            # Overwrite old ipynb file
            json.dump(ipynb, f, indent=True)

    def _sanitize(self, Cells):
        '''
        Remove the extra attributes that thebe uses,
        that Jupyter does not
        '''
        for i, cell in enumerate(Cells):
            del Cells[i]['execution_count']
            del Cells[i]['changed']

    '''
    -------------------------------
    HTML conversion
    -------------------------------
    '''

    def _convert(self):
        self.status_logger.info('Inside update...')
        '''
        Return a deep copy of cellList with code replaced with html-ized code
        '''

        # Deep copy cells so the original is not converted to HTML
        tempCells=copy.deepcopy(self.Cells)


        for cell in tempCells:
            # Preprocessing a code cell
            if cell['cell_type'] == 'code':
                # Highlight the Python syntax
                cell['source'] = \
                        [highlight(source, PythonLexer(), HtmlFormatter()) for source in cell['source']] 
                
                # Highlight standard output and error
                for output in cell['outputs']:
                    # Highlight the standard output
                    if output['output_type'] == 'execute_result':
                        output['data']['text/plain'] = \
                                [highlight(text, BashLexer(), HtmlFormatter()) \
                                for text in output['data']['text/plain']]
                    # Highlight the error
                    if output['output_type'] == 'error':
                        output['traceback'] = \
                                [highlight(text, BashLexer(), HtmlFormatter()) \
                                for text in output['traceback']]

            # Preprocessing a markdown cell
            if cell['cell_type'] == 'markdown':

                # Flatten the list so multi line latex delimiters 
                # are not separated by HTML elements as this would
                # break MathJax.
                cell['source'] = ''.join(cell['source'])

                # Remove any html that could interupt 
                # markdown conversion
                clean = re.compile('<.*>.*</.*>')
                cell['source'] = re.sub(clean, '', cell['source']) 

                # Convert the markdown

                # These arguments are used to let pypandoc
                # know to ignore latex
                pdoc_args = ['--standalone', '--mathjax'] 
                # Convert from markdown to HTML
                cell['source'] = \
                        pypandoc.convert_text(cell['source'], \
                        'html', format = 'md',\
                        extra_args = pdoc_args)

        return tempCells 

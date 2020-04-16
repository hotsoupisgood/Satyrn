import os,sys, tempfile
from io import StringIO
from thebe.core.output import outputController
from multiprocessing import Process
from subprocess import call, check_output

class Vim:
    def __init__(self):
        self.temp_loc = ''
        self.target_prefix = ''

    def write_temp(self, initial_data, targetPrefix):
        '''
        Create a temporary file and load it with our initial data from the ipynb file.
        Open vim in our temporary file.
        '''

        self.target_prefix = targetPrefix

        # Open a temporary file to communicate through
        with tempfile.NamedTemporaryFile(prefix=self.target_prefix, suffix=".thebe", dir=os.getcwd(), delete=False) as tf:

            # Write the initial content to the file I/O buffer
            tf.write(initial_data.encode())

            # Flush the I/O buffer to make sure the data is written to the file
            tf.flush()

            self.temp_loc = tf.name

            tf.close()

        return self.temp_loc

    def open(self):
        '''
        '''
        print('This is the location of the temporary file:\t%s'%(self.temp_loc))

        def callVim():
            # Open the file with the text editor
    #        outputController.open()
            so = sys.stdout = StringIO()
            EDITOR = os.environ.get('EDITOR','vim')
            call([EDITOR, self.temp_loc])
    #        outputController.close()

        try:
            print('Starting vim process...')
            vim = Process(target = callVim)
            vim.start()

        except KeyboardInterrupt:
            print("Terminating vim server.")
            vim.terminate()
            vim.join()
            print("Terminated flask server.")

    def removeTemp(self):
        '''
        '''
        os.unlink(self.temp_loc)

import os
from subprocess import call

def run(initial_data):
    # Get the text editor from the shell, otherwise default to Vim
    EDITOR = os.environ.get('EDITOR','vim')

    # Open a temporary file to communicate through
    with tempfile.NamedTemporaryFile(suffix=".tmp", delete=False) as tf:

        # Write the initial content to the file I/O buffer
        tf.write(initial_data.encode())

        # Flush the I/O buffer to make sure the data is written to the file
        tf.flush()

        print(tf.name)
        # Open the file with the text editor
        call([EDITOR, tf.name])

        tf.close()
        with open(tf.name) as f:
            print(f.read())
        os.unlink(tf.name)

import os
import subprocess
from tempfile import NamedTemporaryFile

def get_external_content(filename=None, initial_content=''):
    """
    Read external content from the user's EDITOR, defaulting to vi. Initial
    content may be specified by giving a list of lines or a string to write at
    the beginning of the tmpfile created in the process.
    Raises an IOError if an error occured.
    """
    if filename:
        fp = open(filename, 'rw')
    else:
        fp = NamedTemporaryFile()
        filename = fp.name

    # write initial content
    if initial_content:
        if isinstance(initial_content, (list, tuple)):
            fp.writelines(initial_content)
        else:
            fp.write(initial_content)
        fp.seek(0)

    # edit tmpfile
    editor = os.environ.get('EDITOR', 'vi')
    if subprocess.call([editor, filename]) != 0:
        raise IOError('EDITOR exited with a non-zero status')

    return fp.read()

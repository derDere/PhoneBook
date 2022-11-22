"""Contains const values
"""

import uuid
from os.path import expanduser, join

FOLDER_NAME = "phonebook"
FILE_EXTENSINON = ".jcontact"

def get_folder_path() -> str:
    """Returns the path to the phonebook folder.

    Returns:
        str: Full path to the phonebook folder.
    """
    path = join(expanduser("~"), FOLDER_NAME)
    return path

def get_path(filename:str) -> str:
    """Returns the path for a given file name.

    Args:
        filename (str): target file name.

    Returns:
        str: full path.
    """
    path = join(expanduser("~"), FOLDER_NAME, filename + FILE_EXTENSINON)
    return path

def new_file_name() -> str:
    """Returns a new Filename.

    Returns:
        _type_: the full path to a new file.
    """
    return get_path(str(uuid.uuid4()))

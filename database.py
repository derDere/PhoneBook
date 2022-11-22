"""Contains all functions and classes to store and manage all data from your phone book.
"""

import os
from os.path import isfile, exists

import path_config
from entry import Entry


class Database:
    """This class represents one database manager object used to manage your phonebook
    """

    def __init__(self) -> None:
        self.contacts = {}
        self.folder = path_config.get_folder_path()
        if not exists(self.folder):
            os.makedirs(self.folder)
        if exists(self.folder):
            self.files = [
                f for f in os.listdir(self.folder)
                if (
                    isfile(f) and
                    (f.lower()[-len(path_config.FILE_EXTENSINON):] == path_config.FILE_EXTENSINON)
                )
            ]
        else:
            self.files = []
        for file in self.files:
            contact, success = Entry.load(file)
            if success:
                self.contacts[file] = contact

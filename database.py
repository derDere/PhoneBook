"""Contains all functions and classes to store and manage all data from your phone book.
"""

import os
from os.path import expanduser, isfile, exists
from entry import Entry


class Database:
    """This class represents one database manager object used to manage your phonebook
    """

    FOLDER_PATH = "~/phonebook"

    def __init__(self) -> None:
        self.contacts = {}
        self.folder = expanduser(Database.FOLDER_PATH)
        if exists(self.folder):
            self.files = [f for f in os.listdir(self.folder) if (isfile(f) and (f.lower()[-4:] == ".vcf"))]
        else:
            self.files = []
        for file in self.files:
            contact, success = Entry.load(file)
            if success:
                self.contacts[file] = contact

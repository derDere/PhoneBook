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
        self.contacts = []
        self.folder = path_config.get_folder_path()
        if not exists(self.folder):
            os.makedirs(self.folder)
            self.files = []
        else:
            self.files = [
                f for f in os.listdir(self.folder)
                if (
                    isfile(f) and
                    (f.lower()[-len(path_config.FILE_EXTENSINON):] == path_config.FILE_EXTENSINON)
                )
            ]
        for file in self.files:
            entry, success = Entry.load(file)
            if success:
                self.contacts.append(entry)

    def search(self, search_str:str) -> list:
        """Returns a list of entries matching the search string.

        Args:
            search_str (str): A string to search possible flags: "all:", "#all:", "org:", "add:", "#add:", "#:", "@:"

        Returns:
            list: Sorted list of entries
        """
        result = [entry for entry in self.contacts if entry.match(search_str)]
        result.sort(key = lambda e: e.display())
        return result

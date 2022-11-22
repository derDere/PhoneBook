import os
from contact import *
from os.path import expanduser, isfile, exists


FOLDER_PATH = "~/phonebook"


class Database:

    def __init__(self) -> None:
        self.contacts = {}
        self.folder = expanduser(FOLDER_PATH)
        if exists(self.folder):
            self.files = [f for f in os.listdir(self.folder) if (isfile(f) and (f.lower()[-4:] == ".vcf"))]
        else:
            self.files = []
        for file in self.files:
            contact, success = Contact.Load(file)
            if success:
                self.contacts[file] = contact